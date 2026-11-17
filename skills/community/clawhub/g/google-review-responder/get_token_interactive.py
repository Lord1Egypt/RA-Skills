#!/usr/bin/env python3
"""
Interactive OAuth helper — run this ON YOUR LAPTOP (it needs a browser).

It asks for your Google Cloud Desktop client ID + secret at runtime (nothing
is saved to disk or printed back), opens a browser for you to sign in with the
Google account that MANAGES the practice's Business Profile, then prints:
  - your refresh token
  - your account_id and location_id(s)
...everything you need for the client config.

Before running:
  pip install google-auth-oauthlib requests
"""

import getpass
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/business.manage"]


def main():
    print("Paste your Google Cloud OAuth *Desktop* client credentials.")
    print("(Credentials page -> your Desktop OAuth client -> Client ID / Client secret)\n")
    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client secret (hidden as you type/paste): ").strip()

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080"],
        }
    }

    print("\nOpening browser. Sign in with the Google account that MANAGES the")
    print("practice's Business Profile. If you see an 'unverified app' screen,")
    print("click Advanced -> Go to <app> (unsafe) -> Continue. That's expected.\n")

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    creds = flow.run_local_server(port=8080, prompt="consent")
    token = creds.token

    print("\n" + "=" * 60)
    print("REFRESH TOKEN (save this):")
    print(creds.refresh_token)
    print("=" * 60)

    # Look up account(s)
    print("\nLooking up your Business Profile account(s) and location(s)...\n")
    h = {"Authorization": f"Bearer {token}"}
    try:
        ar = requests.get(
            "https://mybusinessaccountmanagement.googleapis.com/v1/accounts",
            headers=h, timeout=30,
        )
        accounts = ar.json().get("accounts", [])
        if not accounts:
            print("No accounts returned. Raw response:", ar.text[:500])
        for acct in accounts:
            name = acct.get("name", "")  # e.g. "accounts/123456789"
            print(f"ACCOUNT: {name}   ({acct.get('accountName','')})")
            lr = requests.get(
                f"https://mybusinessbusinessinformation.googleapis.com/v1/{name}/locations",
                headers=h,
                params={"readMask": "name,title,storefrontAddress"},
                timeout=30,
            )
            locs = lr.json().get("locations", [])
            if not locs:
                print("   (no locations or none returned)", lr.text[:300])
            for loc in locs:
                print(f"   LOCATION: {loc.get('name','')}   title: {loc.get('title','')}")
    except Exception as e:
        print("Account/location lookup failed (you can still use the refresh token):", e)

    print("\nDone. Send the account id, location id(s), and refresh token back to Claude")
    print("(or paste just the account/location ids and keep the token handy).")


if __name__ == "__main__":
    main()
