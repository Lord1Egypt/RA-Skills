# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

import os
import urllib.parse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback") 
SCOPE = "w_member_social profile openid"  # Reverted to working scopes

def generate_auth_url():
    """Generates the LinkedIn OAuth authorization URL."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": "openclaw_auth_state"
    }
    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return url

def get_access_token(auth_code):
    """Exchanges the authorization code for an access token."""
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET environment variables are required.")
        exit(1)

    print("\n--- LinkedIn OAuth 2.0 Access Token Generator ---\n")
    
    auth_url = generate_auth_url()
    print("1. Please open the following URL in your browser to authorize the app:\n")
    print(auth_url)
    
    print(f"\n2. After authorizing, you will be redirected to: {REDIRECT_URI}")
    print("3. Copy the 'code' parameter from the redirected URL (e.g., ...?code=AQ_...)")
    
    try:
        auth_code = input("\nPaste the authorization code here: ").strip()
    except EOFError:
        print("\nInput cancelled.")
        exit(1)
    
    if auth_code:
        try:
            print("\nExchanging code for access token...")
            token_data = get_access_token(auth_code)
            
            access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in")
            
            print("\n✅ Access Token Generated Successfully!")
            print("-" * 60)
            print(f"Token: {access_token}")
            print("-" * 60)
            print(f"Expires in: {expires_in} seconds (~{int(expires_in/86400)} days)")
            
        except requests.exceptions.HTTPError as e:
            print(f"\n❌ Error exchanging code for token: {e}")
            if e.response.content:
                print(f"Details: {e.response.json()}")
        except Exception as e:
             print(f"\n❌ Unexpected error: {e}")

    else:
        print("No code provided. Exiting.")
