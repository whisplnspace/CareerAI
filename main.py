import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain

# Load environment variables
load_dotenv()

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_recommendation(interests, skills, education, experience, goals):
    prompt = f"""
    Act as an AI career advisor and recommend career paths based on:
    - Interests: {interests}
    - Skills: {skills}
    - Education: {education}
    - Experience: {experience}
    - Career Goals: {goals}

    Provide:
    1. Career recommendations (Top 3 fields).
    2. Skills required and learning paths.
    3. Relevant AI courses and certifications.
    4. Potential job roles and salary insights.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


# Streamlit UI
st.set_page_config(page_title="AI Career Recommender", page_icon="🚀", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
    <style>
        .stTextArea>label { font-size: 18px; font-weight: bold; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; }
        .stSuccess { font-size: 16px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Header Section with Animation
st.title("🚀 AI Tutor & Career Recommender")
st.subheader("Your AI-powered guide to the perfect career path!")
rain(emoji="🎓", font_size=20, falling_speed=5, animation_length=2)

# User Inputs with Sidebar Layout
col1, col2 = st.columns(2)

with col1:
    interests = st.text_area("💡 What are your interests?", "e.g., AI, Data Science, Robotics")
    skills = st.text_area("🛠 What skills do you have?", "e.g., Python, Machine Learning, NLP")
with col2:
    education = st.text_area("🎓 What is your education background?", "e.g., Bachelor's in Computer Science")
    experience = st.text_area("💼 What is your work experience (if any)?", "e.g., 2 years in software development")
goals = st.text_area("🌍 What are your career goals?", "e.g., Become an AI Researcher, Work at Google")

add_vertical_space(2)

# Button to Generate Recommendation
if st.button("🔍 Get Career Recommendation"):
    if interests and skills and education and goals:
        with st.spinner("AI is analyzing your inputs... 🤖"):
            recommendation = get_gemini_recommendation(interests, skills, education, experience, goals)
        st.success("🎯 AI Career Recommendations:")
        st.write(recommendation)
    else:
        st.warning("⚠️ Please fill out all fields before submitting.")

add_vertical_space(2)

# Sidebar for Additional Resources
st.sidebar.markdown("### 📚 Additional Learning Resources")
st.sidebar.write("- [Coursera AI Courses](https://www.coursera.org)")
st.sidebar.write("- [Udacity AI Nanodegree](https://www.udacity.com)")
st.sidebar.write("- [Kaggle Learning](https://www.kaggle.com/learn)")
st.sidebar.write("- [Research Papers](https://scholar.google.com/)")

# Save user responses for future analysis
if st.button("💾 Save My Inputs"):
    user_data = {
        "Interests": interests,
        "Skills": skills,
        "Education": education,
        "Experience": experience,
        "Goals": goals
    }
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)
    st.success("✅ Your inputs have been saved for further analysis!")

st.sidebar.markdown("### 🌟 Developed with ❤️ using Streamlit & Google Gemini")
