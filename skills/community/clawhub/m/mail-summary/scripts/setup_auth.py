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
import json
import base64
import hashlib
import secrets
import argparse
import urllib.parse
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auth import SCOPES, find_credentials_file, CREDENTIALS_DIR
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
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

    logging.info(f"Generated auth URL: {auth_url}")
    print(auth_url)

def complete_auth(callback_url):
    creds_file = find_credentials_file()
    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
    flow.redirect_uri = 'http://localhost'

    parsed = urllib.parse.urlparse(callback_url)
    params = urllib.parse.parse_qs(parsed.query)
    code = params.get('code', [None])[0]
    if not code:
        logging.error("No authorization code found in URL.")
        sys.exit(1)

    code_verifier = None
    if os.path.exists('.auth_state.json'):
        with open('.auth_state.json') as f:
            state_data = json.load(f)
        code_verifier = state_data.get('code_verifier')
        os.remove('.auth_state.json')

    try:
        flow.fetch_token(code=code, code_verifier=code_verifier)
        token_path = os.path.join(CREDENTIALS_DIR, 'token.json')
        os.makedirs(CREDENTIALS_DIR, exist_ok=True)
        with open(token_path, 'w') as f:
            f.write(flow.credentials.to_json())
        logging.info("Auth complete. token.json saved.")
        print("Auth complete. token.json saved.")
        # Run refresh_service.py automatically after auth complete, only if not already running
        import subprocess
        import psutil
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refresh_service.py')
        lock_file = os.path.join(os.path.dirname(script_path), 'refresh_service.lock')
        def is_refresh_running():
            if not os.path.exists(lock_file):
                return False
            try:
                with open(lock_file, 'r') as f:
                    pid = int(f.read())
                return psutil.pid_exists(pid)
            except Exception:
                return False
        if is_refresh_running():
            print("refresh_service.py is already running. Skipping auto-run.")
        else:
            try:
                result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
                print("\n[refresh_service.py output]\n" + result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"[refresh_service.py error]: {e.stderr}")
    except Exception as e:
        logging.error(f"Failed to fetch token: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--callback', help='Callback URL from browser after authorization')
    args = parser.parse_args()

    if args.callback:
        complete_auth(args.callback)
    else:
        get_auth_url()
