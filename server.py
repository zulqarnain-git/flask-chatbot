# --- FINAL WORKING CODE - USING OPENROUTER (NO CREDIT CARD NEEDED) ---

from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests
import json

# --- SETUP ---
load_dotenv()
app = Flask(__name__)

# --- CONFIGURE THE API KEY ---
API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- ROUTES ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.form.get("message", "")
    bot_response = ""

    # This is the URL for the OpenRouter service
    url = "https://openrouter.ai/api/v1/chat/completions"

    # This is the data structure the new API expects
    data = {
        "model": "mistralai/mistral-7b-instruct:free", # A popular free model
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        api_response = requests.post(url, headers=headers, json=data)
        api_response.raise_for_status()

        response_data = api_response.json()
        bot_response = response_data['choices'][0]['message']['content']

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {api_response.text}")
        bot_response = "Sorry, there was an error with the API key or the free service."
    except Exception as e:
        print(f"An error occurred: {e}")
        bot_response = "A general error occurred. Please check the server console for details."

    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response
    )

# --- RUN THE APP ---
if __name__ == "__main__":
    app.run(debug=True)