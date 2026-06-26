#!/usr/bin/env python3
"""
Web-based OAuth flow for onboarding Google Business Profile clients.

Usage:
  1. Update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET below
  2. Run: python3 oauth_server.py
  3. Send client the link: http://your-vps-ip:5050/auth/start?client=their-business-name
  4. Client logs in, authorizes, and the refresh token is saved automatically

Requires:
  pip install flask google-auth google-auth-oauthlib requests
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, redirect, request, session

from google_auth_oauthlib.flow import Flow

# ---- UPDATE THESE ----
GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
# The public URL where this server is reachable (used for OAuth redirect)
# Example: "http://123.45.67.89:5050" or "https://yourdomain.com"
PUBLIC_URL = "http://YOUR_VPS_IP:5050"
# -----------------------

SCOPES = ["https://www.googleapis.com/auth/business.manage"]
REDIRECT_PATH = "/auth/callback"
CLIENTS_DIR = Path(__file__).parent / "clients"

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Allow HTTP for local/dev OAuth (Google normally requires HTTPS)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [f"{PUBLIC_URL}{REDIRECT_PATH}"],
    }
}


def get_flow():
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=f"{PUBLIC_URL}{REDIRECT_PATH}",
    )


@app.route("/auth/start")
def auth_start():
    """Client visits this URL to begin authorization."""
    client_name = request.args.get("client", "").strip()
    if not client_name:
        return (
            "<h2>Missing client name</h2>"
            "<p>Add <code>?client=business-name</code> to the URL.</p>"
            "<p>Example: <code>/auth/start?client=joes-pizza</code></p>"
        ), 400

    session["client_name"] = client_name

    flow = get_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["oauth_state"] = state
    return redirect(auth_url)


@app.route(REDIRECT_PATH)
def auth_callback():
    """Google redirects here after the client authorizes."""
    client_name = session.get("client_name", "unknown")

    flow = get_flow()
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    refresh_token = creds.refresh_token

    if not refresh_token:
        return (
            "<h2>Authorization issue</h2>"
            "<p>No refresh token received. The client may have already authorized "
            "this app before. Try revoking access at "
            '<a href="https://myaccount.google.com/permissions">Google Account Permissions</a> '
            "and trying again.</p>"
        ), 400

    # Save the client config
    CLIENTS_DIR.mkdir(parents=True, exist_ok=True)
    config_path = CLIENTS_DIR / f"{client_name}.json"

    config = {
        "business_name": client_name,
        "account_id": "NEEDS_LOOKUP",
        "location_id": "NEEDS_LOOKUP",
        "oauth_client_id": GOOGLE_CLIENT_ID,
        "oauth_client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "authorized_at": datetime.now(timezone.utc).isoformat(),
        "notes": "",
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    return (
        f"<h2>All set!</h2>"
        f"<p><strong>{client_name}</strong> has been authorized successfully.</p>"
        f"<p>You can close this window now.</p>"
        f"<p style='color: #666; font-size: 0.9em;'>"
        f"Config saved to: {config_path}</p>"
    )


@app.route("/")
def index():
    return (
        "<h2>Review Responder - Client Authorization</h2>"
        "<p>To authorize a new client, visit:</p>"
        "<pre>/auth/start?client=business-name</pre>"
        "<p>Replace <code>business-name</code> with a short ID for the client "
        "(no spaces, use hyphens).</p>"
    )


if __name__ == "__main__":
    if "YOUR_CLIENT_ID" in GOOGLE_CLIENT_ID:
        print("ERROR: Update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET")
        print("at the top of this script before running.")
        exit(1)

    if "YOUR_VPS_IP" in PUBLIC_URL:
        print("ERROR: Update PUBLIC_URL with your VPS's public IP or domain.")
        print("Example: PUBLIC_URL = 'http://123.45.67.89:5050'")
        exit(1)

    print(f"OAuth server running at {PUBLIC_URL}")
    print(f"Send clients to: {PUBLIC_URL}/auth/start?client=their-name")
    app.run(host="0.0.0.0", port=5050)
