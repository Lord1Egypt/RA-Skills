#!/usr/bin/env python3
"""One-command Fitbit setup. Handles credentials, auth, and initial sync.

Usage:
  # Interactive (agent guides user through it):
  uv run scripts/fitbit_setup.py

  # Non-interactive (agent passes all values):
  uv run scripts/fitbit_setup.py --client-id YOUR_ID --client-secret YOUR_SECRET

  # Exchange redirect URL after browser auth:
  uv run scripts/fitbit_setup.py --exchange "http://localhost:8080/callback?code=abc123"

  # Check setup status:
  uv run scripts/fitbit_setup.py --status
"""

import json
import os
import sys
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / ".env"
TOKEN_FILE = BASE_DIR / "data" / "fitbit_token.json"
DATA_DIR = BASE_DIR / "data" / "user_default"

SCOPES = [
    "activity", "heartrate", "sleep", "profile",
    "respiratory_rate", "oxygen_saturation", "temperature",
    "cardio_fitness",
]
REDIRECT_URI = "http://localhost:8080/callback"
AUTH_URL = "https://www.fitbit.com/oauth2/authorize"
TOKEN_URL = "https://api.fitbit.com/oauth2/token"


def load_credentials():
    """Load client ID and secret from .env file."""
    client_id = None
    client_secret = None
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("FITBIT_CLIENT_ID="):
                client_id = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("FITBIT_CLIENT_SECRET="):
                client_secret = line.split("=", 1)[1].strip().strip('"').strip("'")
    return client_id, client_secret


def save_credentials(client_id, client_secret):
    """Save credentials to .env file."""
    lines = []
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if not line.startswith("FITBIT_CLIENT_ID=") and not line.startswith("FITBIT_CLIENT_SECRET="):
                lines.append(line)
    lines.append(f"FITBIT_CLIENT_ID={client_id}")
    lines.append(f"FITBIT_CLIENT_SECRET={client_secret}")
    ENV_FILE.write_text("\n".join(lines) + "\n")


def get_auth_url(client_id):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "expires_in": "31536000",
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def extract_code(url):
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if "code" in params:
        return params["code"][0]
    fragment_params = urllib.parse.parse_qs(parsed.fragment)
    if "code" in fragment_params:
        return fragment_params["code"][0]
    raise ValueError(f"No auth code found in URL: {url}")


def exchange_code(client_id, client_secret, code):
    import httpx
    resp = httpx.post(
        TOKEN_URL,
        data={
            "client_id": client_id,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        auth=(client_id, client_secret),
    )
    resp.raise_for_status()
    return resp.json()


def save_token(token_data):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def load_token():
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def check_status():
    """Print setup status as JSON for the agent to parse."""
    client_id, client_secret = load_credentials()
    token = load_token()
    has_data = DATA_DIR.exists() and any(DATA_DIR.glob("*.json"))

    status = {
        "credentials_saved": bool(client_id and client_secret),
        "fitbit_authorized": bool(token),
        "user_id": token.get("user_id") if token else None,
        "data_synced": has_data,
        "data_files": len(list(DATA_DIR.glob("*.json"))) if DATA_DIR.exists() else 0,
        "setup_complete": bool(client_id and client_secret and token and has_data),
    }

    if not status["credentials_saved"]:
        status["next_step"] = "save_credentials"
        status["message"] = "Need Fitbit app credentials. User must create a Fitbit Developer App."
    elif not status["fitbit_authorized"]:
        status["next_step"] = "authorize"
        status["auth_url"] = get_auth_url(client_id)
        status["message"] = "Credentials saved. User needs to authorize via browser."
    elif not status["data_synced"]:
        status["next_step"] = "sync"
        status["message"] = "Authorized! Run fitbit_sync.py to pull data."
    else:
        status["next_step"] = "done"
        status["message"] = "Setup complete! Ready to analyze health data."

    print(json.dumps(status, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fitbit setup wizard")
    parser.add_argument("--client-id", help="Fitbit OAuth Client ID")
    parser.add_argument("--client-secret", help="Fitbit OAuth Client Secret")
    parser.add_argument("--exchange", help="Exchange redirect URL for token")
    parser.add_argument("--status", action="store_true", help="Check setup status")
    parser.add_argument("--auth-url", action="store_true", help="Print auth URL (requires saved credentials)")
    args = parser.parse_args()

    # Status check
    if args.status:
        check_status()
        return

    # Save credentials if provided
    if args.client_id and args.client_secret:
        save_credentials(args.client_id, args.client_secret)
        print(json.dumps({
            "success": True,
            "message": "Credentials saved!",
            "next_step": "authorize",
            "auth_url": get_auth_url(args.client_id),
        }, indent=2))
        return

    # Print auth URL
    if args.auth_url:
        client_id, _ = load_credentials()
        if not client_id:
            print(json.dumps({"error": "No credentials saved. Provide --client-id and --client-secret first."}))
            sys.exit(1)
        print(json.dumps({"auth_url": get_auth_url(client_id)}))
        return

    # Exchange redirect URL for token
    if args.exchange:
        client_id, client_secret = load_credentials()
        if not client_id or not client_secret:
            print(json.dumps({"error": "No credentials saved. Provide --client-id and --client-secret first."}))
            sys.exit(1)
        try:
            code = extract_code(args.exchange)
            tokens = exchange_code(client_id, client_secret, code)
            save_token(tokens)
            print(json.dumps({
                "success": True,
                "user_id": tokens.get("user_id"),
                "message": f"Authorized! Fitbit user: {tokens.get('user_id')}",
                "next_step": "sync",
            }, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
        return

    # No args — print status (agent will decide what to do)
    check_status()


if __name__ == "__main__":
    main()
