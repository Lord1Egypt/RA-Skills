import os
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    print("Error: CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI must be set in .env")
    exit(1)

def get_access_token(auth_code):
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exchange LinkedIn OAuth Code for Access Token")
    parser.add_argument("code", help="The authorization code from the redirect URL")
    args = parser.parse_args()

    print(f"\nExchanging code: {args.code[:10]}...")
    try:
        token_data = get_access_token(args.code)
        print(f"\n✅ SUCCESS! Access Token:\n\n{token_data['access_token']}\n")
        print("Copy this token and update your .env file:")
        print(f"LINKEDIN_ACCESS_TOKEN={token_data['access_token']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
