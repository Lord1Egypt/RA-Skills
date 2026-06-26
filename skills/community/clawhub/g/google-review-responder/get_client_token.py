#!/usr/bin/env python3
"""
One-time OAuth flow to get a refresh token for a new client.

Usage:
  python3 get_client_token.py

This opens a browser window for the client to log in with their Google
account and authorize access to their Business Profile. Once authorized,
it prints a refresh token to save in the client's config file.

Before running:
  1. Update CLIENT_ID and CLIENT_SECRET below with your Google Cloud project credentials
  2. pip install google-auth-oauthlib
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/business.manage"]

# ----- UPDATE THESE WITH YOUR GOOGLE CLOUD PROJECT CREDENTIALS -----
CLIENT_ID = "YOUR_CLIENT_ID.apps.googleusercontent.com"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
# -------------------------------------------------------------------

CLIENT_CONFIG = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8080"],
    }
}


def main():
    if "YOUR_CLIENT_ID" in CLIENT_ID:
        print("Error: Update CLIENT_ID and CLIENT_SECRET at the top of this script")
        print("with your Google Cloud project credentials before running.")
        return

    print("Opening browser for Google authorization...")
    print("Have the client log in with the Google account that owns their Business Profile.\n")

    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)
    creds = flow.run_local_server(port=8080)

    print(f"\nRefresh token: {creds.refresh_token}")
    print("\nSave this in the client's config file under 'refresh_token'.")
    print("This token does not expire unless the client revokes access.")


if __name__ == "__main__":
    main()
