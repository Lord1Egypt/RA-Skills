import os.path
import glob
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

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
        "No credentials file found. Please place credentials.json or client_secret_*.json in the project root."
    )

def auth_google():
    if not os.path.exists('token.json'):
        raise FileNotFoundError(
            "token.json not found. Please complete the auth setup first:\n"
            "  Step 1: python scripts/setup_auth.py\n"
            "          → Send the printed URL to the user to open in their browser\n"
            "  Step 2: python scripts/setup_auth.py --callback \"<redirect URL from browser>\"\n"
            "          → This saves token.json"
        )

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            raise ValueError(
                "token.json is invalid or expired without a refresh token.\n"
                "Please re-run the auth setup:\n"
                "  Step 1: python scripts/setup_auth.py\n"
                "  Step 2: python scripts/setup_auth.py --callback \"<redirect URL from browser>\""
            )

    return creds
