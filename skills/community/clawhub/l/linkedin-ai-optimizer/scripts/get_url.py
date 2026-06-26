import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
# The scope must match what your app is configured for in the developer portal
SCOPE = "w_member_social profile openid" 

if not CLIENT_ID or not REDIRECT_URI:
    print("Error: LINKEDIN_CLIENT_ID and LINKEDIN_REDIRECT_URI must be set in .env")
    exit(1)

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "state": "openclaw_auth_state",
    "scope": SCOPE,
}

url = f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

print("\n--- LinkedIn Authorization URL ---")
print("1. Open this URL in your browser:")
print(f"\n{url}\n")
print("2. After authorizing, you will be redirected to your Redirect URI.")
print("3. Copy the 'code' parameter from the URL.")
print("4. Then run: python3 exchange_token.py <code>")
