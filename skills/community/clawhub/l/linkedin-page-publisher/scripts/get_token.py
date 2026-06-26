#!/usr/bin/env python3
"""One-time OAuth 2.0 helper to get an access token for a LinkedIn Company Page.

Runs a tiny local HTTP server to catch the redirect, exchanges the code, and
prints both the access token and the refresh token. You only run this once
per environment — after that, the access token lives in env vars and the
refresh token renews it for the next year.

Usage:
    export LINKEDIN_CLIENT_ID=<your app's client id>
    export LINKEDIN_CLIENT_SECRET=<your app's client secret>
    python scripts/get_token.py

Setup prerequisites: see references/setup.md. TL;DR — you need a LinkedIn
Developer app with "Community Management API" access approved, and the
redirect URI `http://localhost:8765/callback` added under Auth settings.
"""

from __future__ import annotations

import http.server
import os
import secrets
import sys
import urllib.parse
import webbrowser
from threading import Event, Thread

import requests


REDIRECT_URI = "http://localhost:8765/callback"
SCOPES = ["w_organization_social", "r_organization_social", "rw_organization_admin"]
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    # Class-level stash so main() can read the result after the server stops.
    result: dict[str, str] = {}
    done: Event = Event()

    def log_message(self, format: str, *args) -> None:  # noqa: ARG002
        pass  # Suppress default noisy logging.

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        if "error" in params:
            msg = params.get("error_description", params["error"])[0]
            self.wfile.write(f"<h1>OAuth error</h1><pre>{msg}</pre>".encode())
            _CallbackHandler.result["error"] = msg
        elif "code" in params and "state" in params:
            _CallbackHandler.result["code"] = params["code"][0]
            _CallbackHandler.result["state"] = params["state"][0]
            self.wfile.write(
                b"<h1>You can close this tab.</h1>"
                b"<p>Token exchange is happening in your terminal.</p>"
            )
        else:
            self.wfile.write(b"<h1>Unexpected callback params.</h1>")
            _CallbackHandler.result["error"] = "missing code/state"

        _CallbackHandler.done.set()


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"error: {name} is not set.", file=sys.stderr)
        sys.exit(2)
    return value


def main() -> int:
    client_id = _require_env("LINKEDIN_CLIENT_ID")
    client_secret = _require_env("LINKEDIN_CLIENT_SECRET")

    state = secrets.token_urlsafe(16)
    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": " ".join(SCOPES),
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

    print("Opening browser for LinkedIn sign-in…")
    print(f"If it doesn't open automatically, visit:\n  {auth_url}\n")

    server = http.server.HTTPServer(("127.0.0.1", 8765), _CallbackHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    webbrowser.open(auth_url)

    try:
        if not _CallbackHandler.done.wait(timeout=300):
            print("timed out waiting for LinkedIn redirect.", file=sys.stderr)
            return 1
    except KeyboardInterrupt:
        print("cancelled.")
        return 1
    finally:
        server.shutdown()

    if "error" in _CallbackHandler.result:
        print(f"OAuth error: {_CallbackHandler.result['error']}", file=sys.stderr)
        return 1
    if _CallbackHandler.result.get("state") != state:
        print("state mismatch — possible CSRF. Aborting.", file=sys.stderr)
        return 1

    code = _CallbackHandler.result["code"]
    print("Got authorization code, exchanging for tokens…")

    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"token exchange failed ({resp.status_code}): {resp.text}", file=sys.stderr)
        return 1

    body = resp.json()
    print("\nSuccess. Save these — LinkedIn will not show them again.\n")
    print(f"LINKEDIN_ACCESS_TOKEN={body['access_token']}")
    if "refresh_token" in body:
        print(f"LINKEDIN_REFRESH_TOKEN={body['refresh_token']}")
    print(f"\nAccess token expires in {body.get('expires_in', '?')} seconds.")
    print("Add these to your shell profile or .env file.\n")
    print("Next step: find your Company Page's numeric ID at")
    print("  https://www.linkedin.com/company/<slug>/admin/  (visible in the URL)")
    print("and export it as LINKEDIN_ORG_ID.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
