"""
Auth setup - 2 steps:

Step 1: Get auth URL
  python scripts/setup_auth.py
  → prints URL for user to open in browser

Step 2: Complete auth with callback URL
  python scripts/setup_auth.py --callback "http://localhost/?code=..."
  → saves token.json
"""
import sys
import os
import glob
import json
import base64
import hashlib
import secrets
import argparse
import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

def find_credentials_file():
    if os.path.exists('credentials.json'):
        return 'credentials.json'
    matches = glob.glob('client_secret_*.json')
    if matches:
        return matches[0]
    raise FileNotFoundError(
        "No credentials file found. Place credentials.json or client_secret_*.json in the project root."
    )

def generate_pkce():
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()
    return code_verifier, code_challenge

def get_auth_url():
    creds_file = find_credentials_file()
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    flow.redirect_uri = 'http://localhost'

    code_verifier, code_challenge = generate_pkce()
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline',
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )

    with open('.auth_state.json', 'w') as f:
        json.dump({'code_verifier': code_verifier}, f)

    print(auth_url)

def complete_auth(callback_url):
    creds_file = find_credentials_file()
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    flow.redirect_uri = 'http://localhost'

    parsed = urllib.parse.urlparse(callback_url)
    params = urllib.parse.parse_qs(parsed.query)
    code = params.get('code', [None])[0]
    if not code:
        print("ERROR: No authorization code found in URL.")
        sys.exit(1)

    code_verifier = None
    if os.path.exists('.auth_state.json'):
        with open('.auth_state.json') as f:
            state_data = json.load(f)
        code_verifier = state_data.get('code_verifier')
        os.remove('.auth_state.json')

    flow.fetch_token(code=code, code_verifier=code_verifier)

    with open('token.json', 'w') as f:
        f.write(flow.credentials.to_json())
    print("Auth complete. token.json saved.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--callback', help='Callback URL from browser after authorization')
    args = parser.parse_args()

    if args.callback:
        complete_auth(args.callback)
    else:
        get_auth_url()
