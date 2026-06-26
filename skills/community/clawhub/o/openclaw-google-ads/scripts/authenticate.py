#!/usr/bin/env python3
"""
Google Ads API Authentication Script
Handles OAuth flow and stores refresh token for API access.
"""

import os
import sys

# OAuth scopes for Google Ads API
SCOPES = ['https://www.googleapis.com/auth/adwords']

def main():
    # Import here so we can catch import errors
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Error: google-auth-oauthlib not installed")
        print("Run: pip install google-auth-oauthlib")
        sys.exit(1)
    
    # Load client credentials from environment
    client_id = os.environ.get('GOOGLE_ADS_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_ADS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set")
        print("Make sure OAuth credentials are configured")
        sys.exit(1)
    
    # Create client config dict
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    # Run OAuth flow
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    
    # Use local server flow
    credentials = flow.run_local_server(port=0)
    
    # Store refresh token
    refresh_token = credentials.refresh_token
    
    print(f"\n{'='*60}")
    print(f"REFRESH TOKEN: {refresh_token}")
    print(f"{'='*60}")
    print("\nDo not paste this into tracked files or plaintext workspace notes.")
    print("Store it using the approved secure credential workflow for this OpenClaw environment.")
    print("Expose it to the runtime through approved environment injection only.")

if __name__ == '__main__':
    main()
