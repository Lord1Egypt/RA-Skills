#!/usr/bin/env python3
"""Fitbit OAuth2 Authorization Flow for OpenClaw PHA Skill.

Usage:
  # Interactive: prints auth URL, waits for you to paste redirect URL
  uv run scripts/fitbit_auth.py

  # Non-interactive: exchange a redirect URL directly
  uv run scripts/fitbit_auth.py --exchange "http://localhost:8080/callback?code=abc123#_=_"
"""

import json
import os
import sys
import urllib.parse
from pathlib import Path

import httpx
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

CLIENT_ID = os.getenv("FITBIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("FITBIT_CLIENT_SECRET")
REDIRECT_URI = os.getenv("FITBIT_REDIRECT_URI", "http://localhost:8080/callback")
TOKEN_FILE = BASE_DIR / "data" / "fitbit_token.json"

SCOPES = [
    "activity", "heartrate", "sleep", "profile",
    "respiratory_rate", "oxygen_saturation", "temperature",
    "cardio_fitness",
]

AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
TOKEN_URL = "https://api.fitbit.com/oauth2/token"


def get_auth_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "expires_in": "31536000",  # 1 year
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def extract_code(url: str) -> str:
    """Extract auth code from redirect URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if "code" in params:
        return params["code"][0]
    # Sometimes code is in fragment
    fragment_params = urllib.parse.parse_qs(parsed.fragment)
    if "code" in fragment_params:
        return fragment_params["code"][0]
    raise ValueError(f"No auth code found in URL: {url}")


def exchange_code(code: str) -> dict:
    """Exchange authorization code for tokens."""
    resp = httpx.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    resp.raise_for_status()
    return resp.json()


def refresh_token(token_data: dict) -> dict:
    """Refresh an expired access token."""
    resp = httpx.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
            "client_id": CLIENT_ID,
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    resp.raise_for_status()
    new_tokens = resp.json()
    save_token(new_tokens)
    return new_tokens


def save_token(token_data: dict):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def load_token() -> dict | None:
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Set FITBIT_CLIENT_ID and FITBIT_CLIENT_SECRET in .env")
        print(f"  .env location: {BASE_DIR / '.env'}")
        sys.exit(1)

    # Non-interactive: exchange a redirect URL
    if len(sys.argv) > 1 and sys.argv[1] == "--exchange":
        if len(sys.argv) < 3:
            print("Usage: fitbit_auth.py --exchange 'REDIRECT_URL'")
            sys.exit(1)
        url = sys.argv[2]
        code = extract_code(url)
        print(f"Extracted code: {code[:10]}...")
        tokens = exchange_code(code)
        save_token(tokens)
        print(f"Success! User: {tokens.get('user_id', 'unknown')}")
        print(f"Token saved to {TOKEN_FILE}")
        return

    # Check if already authorized
    existing = load_token()
    if existing:
        print(f"Already authorized (user: {existing.get('user_id', 'unknown')})")
        print("To re-authorize, delete data/fitbit_token.json and run again.")
        return

    # Interactive: print URL and wait for paste
    auth_url = get_auth_url()
    print("=" * 60)
    print("FITBIT AUTHORIZATION")
    print("=" * 60)
    print()
    print("1. Open this URL in your browser:")
    print()
    print(f"   {auth_url}")
    print()
    print("2. Authorize the app on Fitbit's website")
    print()
    print("3. You'll be redirected to a page that FAILS to load.")
    print("   That's expected! Copy the FULL URL from your browser's address bar")
    print("   and paste it below.")
    print()

    redirect_url = input("Paste the redirect URL here: ").strip()
    if not redirect_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    code = extract_code(redirect_url)
    print(f"Got code: {code[:10]}...")
    tokens = exchange_code(code)
    save_token(tokens)
    print(f"\nSuccess! Logged in as user: {tokens.get('user_id', 'unknown')}")
    print(f"Token saved to {TOKEN_FILE}")


if __name__ == "__main__":
    main()
