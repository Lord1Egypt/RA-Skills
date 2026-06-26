

import os
import glob
import logging
import yaml
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Credentials location (outside skill folder)
CREDENTIALS_DIR = os.path.expanduser('~/.openclaw/config/mail-summary')
def get_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config or {}
    except Exception as e:
        logging.warning(f"Could not read config.yaml: {e}. Using defaults.")
        return {}

config = get_config()
MAX_RETRIES = config.get('max_retries', 5)
LOG_LEVEL = getattr(logging, config.get('log_level', 'INFO').upper(), logging.INFO)
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

def find_credentials_file():
    cred_path = os.path.join(CREDENTIALS_DIR, 'credentials.json')
    if os.path.exists(cred_path):
        return cred_path
    matches = glob.glob(os.path.join(CREDENTIALS_DIR, 'client_secret_*.json'))
    if matches:
        return matches[0]
    raise FileNotFoundError(
        f"No credentials file found in {CREDENTIALS_DIR}. "
        "Please place credentials.json or client_secret_*.json there."
    )

def save_checkpoint(state, filename=".auth_checkpoint.json"):
    try:
        with open(filename, "w") as f:
            json.dump(state, f)
        logging.info(f"Checkpoint saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save checkpoint: {e}")

def auth_google():
    retry_count = 0
    last_error = None
    token_path = os.path.join(CREDENTIALS_DIR, 'token.json')
    while retry_count < MAX_RETRIES:
        try:
            if not os.path.exists(token_path):
                raise FileNotFoundError(
                    f"token.json not found in {CREDENTIALS_DIR}. Please complete the auth setup first:\n"
                    "  Step 1: python scripts/setup_auth.py\n"
                    "          → Send the printed URL to the user to open in their browser\n"
                    "  Step 2: python scripts/setup_auth.py --callback \"<redirect URL from browser>\"\n"
                    "          → This saves token.json"
                )

            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            if not creds.valid:
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                else:
                    raise ValueError(
                        f"token.json is invalid or expired without a refresh token in {CREDENTIALS_DIR}.\n"
                        "Please re-run the auth setup:\n"
                        "  Step 1: python scripts/setup_auth.py\n"
                        "  Step 2: python scripts/setup_auth.py --callback \"<redirect URL from browser>\""
                    )

            return creds
        except Exception as e:
            retry_count += 1
            last_error = e
            logging.warning(f"auth_google() failed (attempt {retry_count}/{MAX_RETRIES}): {e}")
            if retry_count >= MAX_RETRIES:
                state = {"error": str(e), "retry_count": retry_count}
                save_checkpoint(state)
                raise StopIteration(f"Max retries ({MAX_RETRIES}) reached: {e}")
