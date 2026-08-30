import streamlit as st
from google import genai
import os

# 1. Page Configuration & Custom UI Styling
st.set_page_config(
    page_title="SMART CHATBOT",
    page_icon="🤖",
    layout="wide",
    menu_items={}
)

# Custom CSS for premium landing page
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stStatusWidget"],
    div[data-testid="stMainMenu"] {
        display: none !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(168, 85, 247, 0.18), transparent 28%),
            radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.12), transparent 30%),
            linear-gradient(135deg, #f8fafc 0%, #eef2ff 35%, #f5f3ff 100%);
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-shell {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.10);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .brand-badge {
        display: inline-block;
        background: rgba(168, 85, 247, 0.18);
        border: 1px solid rgba(196, 181, 253, 0.35);
        color: #ddd6fe;
        border-radius: 999px;
        padding: 8px 16px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(2.7rem, 5vw, 5rem);
        line-height: 0.96;
        font-weight: 900;
        letter-spacing: -0.06em;
        margin: 0;
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 30%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.7;
        color: #475569;
        max-width: 620px;
        margin-top: 1.1rem;
    }

    .cta-row {
        margin-top: 1.7rem;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 1.3rem;
        min-height: 180px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
    }

    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
    }

    .feature-card h4 {
        margin: 0 0 0.5rem;
        color: #0f172a;
        font-size: 1.06rem;
    }

    .feature-card p {
        margin: 0;
        color: #475569;
        line-height: 1.6;
        font-size: 0.92rem;
    }

    .bot-panel {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(224,231,255,0.65));
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 28px;
        padding: 1.2rem;
        box-shadow: 0 20px 50px rgba(88, 28, 135, 0.16);
        height: 100%;
    }

    .chat-window {
        background: rgba(248, 250, 252, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 20px;
        padding: 1rem;
        height: 360px;
        overflow: hidden;
    }

    .chat-bubble {
        max-width: 82%;
        border-radius: 16px;
        padding: 0.8rem 0.9rem;
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .bot {
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(96, 165, 250, 0.28);
        color: #1e3a8a;
        margin-right: auto;
    }

    .user {
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid rgba(196, 181, 253, 0.38);
        color: #4c1d95;
        margin-left: auto;
    }

    .mini-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0.8rem;
        border-radius: 12px;
        background: rgba(248, 250, 252, 0.04);
        border: 1px solid rgba(148, 163, 184, 0.12);
        margin-top: 0.8rem;
    }

    .mini-stat strong {
        font-size: 1.25rem;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.auth-card) {
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 22px;
        padding: 30px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
    }

    .title-text {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a855f7, #ec4899, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle-text {
        font-size: 0.95rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 25px;
    }

    .stTextInput > label,
    .stTextArea > label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        color: #000000 !important;
        border: 1px solid rgba(148, 163, 184, 0.45) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.08) !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #4b5563 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        background: #ffffff !important;
        color: #0f172a !important;
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.18) !important;
    }

    .stChatInput textarea,
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid rgba(148, 163, 184, 0.5) !important;
        border-radius: 12px !important;
        box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.08) !important;
    }

    .stChatInput textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #475569 !important;
        opacity: 1 !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease-in-out !important;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #4f46e5, #9333ea) !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(147, 51, 234, 0.5) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

DEFAULT_GEMINI_API_KEY = "AQ.Ab8RN6IKvTpAbHUyfN4CU_71WeQpsbT1yrldJ64IWqtK2RJNxg"

# 2. Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_database" not in st.session_state:
    # Default demo credentials: username -> password
    st.session_state.user_database = {"admin": "admin123", "student": "hackathon"}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = DEFAULT_GEMINI_API_KEY
os.environ["GEMINI_API_KEY"] = st.session_state.gemini_api_key

# Load Custom Knowledge Base
knowledge_data = ""
if os.path.exists("knowledge.txt"):
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_data = f.read()

# -------------------------------------------------------------
# SCREEN 1: LOGIN & REGISTRATION
# -------------------------------------------------------------
# -------------------------------------------------------------
# SCREEN 1: LOGIN & REGISTRATION (Redesigned)
# -------------------------------------------------------------
if not st.session_state.authenticated:
    if st.session_state.show_signup:
        st.markdown("<div class='title-text'>✨ Create Your Account</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle-text'>Join the smart chatbot workspace</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            new_user = st.text_input("New Username", key="reg_user", placeholder="Choose a username")
            new_pass = st.text_input("New Password", type="password", key="reg_pass", placeholder="Choose a password")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")

            st.write("")
            if st.button("Create Account", use_container_width=True):
                if not new_user or not new_pass:
                    st.warning("All fields are required.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif new_user in st.session_state.user_database:
                    st.error("Username already registered.")
                else:
                    st.session_state.user_database[new_user] = new_pass
                    st.session_state.show_signup = False
                    st.success("Account created! You may now sign in.")
                    st.rerun()

            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
    else:
        st.markdown("<div class='brand-badge'>AI POWERED EXPERIENCE</div>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>SMART<br>CHATBOT</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-subtitle'>A premium AI assistant designed to answer questions, guide users, and deliver smart support with speed, accuracy, and confidence.</p>",
            unsafe_allow_html=True,
        )
        c1, _ = st.columns([1, 1])
        with c1:
            if st.button("Get Started", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()

        st.write("")
        cols = st.columns(3)
        with cols[0]:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h4>Instant Answers</h4>
                    <p>Get fast, relevant responses built from your knowledge base and custom instructions.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h4>Smart Intelligence</h4>
                    <p>Designed for real business support, decision-making, and guided conversations.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h4>Secure Access</h4>
                    <p>Personalized login and protected workspace support for a smooth, trustworthy experience.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        col1, col2, col3 = st.columns([1, 1.8, 1])

        with col2:
            st.markdown('<div class="auth-card"></div>', unsafe_allow_html=True)

            st.markdown("<div class='title-text'>✨ SMART CHATBOT</div>", unsafe_allow_html=True)
            st.markdown("<div class='subtitle-text'>Sign in to access your intelligent workspace</div>", unsafe_allow_html=True)

            tab_login, tab_register = st.tabs(["🔑 Log In", "📝 Sign Up"])

            with tab_login:
                login_username = st.text_input("Username", key="login_user", placeholder="Enter your username")
                login_password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")

                st.write("")
                if st.button("Sign In →", use_container_width=True, type="primary"):
                    if login_username in st.session_state.user_database and \
                       st.session_state.user_database[login_username] == login_password:
                        st.session_state.authenticated = True
                        st.session_state.current_user = login_username
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please verify your details.")

            with tab_register:
                new_user = st.text_input("New Username", key="reg_user", placeholder="Choose a username")
                new_pass = st.text_input("New Password", type="password", key="reg_pass", placeholder="Choose a password")
                confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")

                st.write("")
                if st.button("Create Account", use_container_width=True):
                    if not new_user or not new_pass:
                        st.warning("All fields are required.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    elif new_user in st.session_state.user_database:
                        st.error("Username already registered.")
                    else:
                        st.session_state.user_database[new_user] = new_pass
                        st.success("Account created! You may now sign in.")
# -------------------------------------------------------------
# SCREEN 2: CHATBOT INTERFACE (Visible only after logging in)
# -------------------------------------------------------------
else:
    # Sidebar: User Profile, Controls, and Settings
    with st.sidebar:
        st.write(f"👤 Logged in as: **{st.session_state.current_user}**")
        if st.button("Log Out", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.messages = []
            st.session_state.gemini_api_key = ""
            st.rerun()

        st.divider()
        st.header("⚙️ Configuration")
        st.success("Gemini API is ready to use.")
        if st.button("Reset API Key"):
            st.session_state.gemini_api_key = DEFAULT_GEMINI_API_KEY
            os.environ["GEMINI_API_KEY"] = st.session_state.gemini_api_key
            st.rerun()
        system_prompt = st.text_area(
            "Persona & Guidelines:",
            value=(
                "You are a highly capable AI assistant. Answer using the provided knowledge base as the primary source. "
                "Give detailed, multi-paragraph responses with clear explanations, examples, and practical points when relevant. "
                "If details are missing, say so honestly and avoid guessing."
            )
        )

    st.markdown(f"<h1 class='main-title'>🤖 Project Assistant</h1>", unsafe_allow_html=True)

    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    api_key = st.session_state.gemini_api_key or os.environ.get("GEMINI_API_KEY", DEFAULT_GEMINI_API_KEY)

    # Chat Input Field
    if prompt := st.chat_input("Ask a question about your project..."):
        if not api_key:
            st.info("Please enter your Gemini API key in the sidebar.")
            st.stop()

        # Display and record user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build prompt with Knowledge Base injection
        grounded_prompt = f"""
        --- START OF KNOWLEDGE BASE ---
        {knowledge_data}
        --- END OF KNOWLEDGE BASE ---

        User Question: {prompt}

        Instructions:
        - Answer in a clear, detailed, and natural way.
        - Use multiple paragraphs or bullet points when helpful.
        - Focus on accuracy from the knowledge base.
        - Keep the answer practical and readable.
        """

        # Call Gemini API
        client = genai.Client(api_key=api_key)
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=grounded_prompt,
                config={
                    "system_instruction": system_prompt,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "max_output_tokens": 800,
                },
            )
            st.markdown(response.text)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response.text})