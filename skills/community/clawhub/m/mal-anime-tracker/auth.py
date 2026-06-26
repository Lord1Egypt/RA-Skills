import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we are in the skill directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def authorize(client_id, client_secret, code, code_verifier):
    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        print(f"ACCESS_TOKEN={token_data['access_token']}")
        print(f"REFRESH_TOKEN={token_data['refresh_token']}")
        logger.info("Authorization successful. Tokens generated.")
        return True
    else:
        logger.error(f"Authorization failed: {response.text}")
        return False

def refresh_access_token(client_id, client_secret, refresh_token):
    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        print(f"ACCESS_TOKEN={token_data['access_token']}")
        print(f"REFRESH_TOKEN={token_data['refresh_token']}")
        logger.info("Access token refreshed successfully.")
        return True
    else:
        logger.error(f"Failed to refresh token: {response.text}")
        return False
