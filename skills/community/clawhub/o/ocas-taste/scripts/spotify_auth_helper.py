#!/usr/bin/env python3
"""
Spotify OAuth Authorization Code helper for ocas-taste.

The operator runs this ONE TIME in an environment with a browser (a desktop/laptop,
NOT the headless cron host). It performs the interactive Spotify login and
writes the resulting refresh token to:

  commons/data/ocas-taste/music/spotify_token.json

The companion bridge `apply_spotify_token_to_env.py` then copies that refresh
token into ~/.hermes/profiles/indigo/.env as SPOTIFY_REFRESH_TOKEN, which is
what the cron puller (spotify_history_puller.py) reads.

Usage:
  # Auto mode (default): opens browser, starts a local callback server.
  python3 spotify_auth_helper.py

  # Manual mode: prints the authorize URL, you paste the redirected URL back.
  python3 spotify_auth_helper.py --manual

After this succeeds, run the bridge:
  python3 apply_spotify_token_to_env.py

Requires: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
(env vars, read from the profile .env). REDIRECT_URI must match the Spotify
app's registered redirect URI (currently http://localhost:8888/callback).
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Refresh Spotify OAuth token and persist SPOTIFY_REFRESH_TOKEN.')
    print("Usage: spotify_auth_helper.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import os
import sys
import time
import json
import argparse
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo")))
TOKEN_FILE = HERMES_HOME / "commons/data/ocas-taste/music/spotify_token.json"
SCOPES = "user-read-recently-played"
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"


def get_env():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI") or "http://localhost:8888/callback"
    missing = [n for n, v in (
        ("SPOTIFY_CLIENT_ID", client_id),
        ("SPOTIFY_CLIENT_SECRET", client_secret),
        ("SPOTIFY_REDIRECT_URI", redirect_uri),
    ) if not v]
    if missing:
        print(f"ERROR: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("These must be present in ~/.hermes/profiles/indigo/.env", file=sys.stderr)
        sys.exit(1)
    return client_id, client_secret, redirect_uri


def build_authorize_url(client_id, redirect_uri, state):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": SCOPES,
        "redirect_uri": redirect_uri,
        "state": state,
    }
    return AUTH_ENDPOINT + "?" + urllib.parse.urlencode(params)


def exchange_code(code, client_id, client_secret, redirect_uri):
    resp = requests.post(
        TOKEN_ENDPOINT,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def write_token(data):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "token_type": data.get("token_type"),
        "scope": data.get("scope"),
        "expires_in": data.get("expires_in"),
        "expires_at": int(time.time()) + int(data.get("expires_in", 3600)),
    }
    TOKEN_FILE.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"OK: wrote tokens to {TOKEN_FILE}")
    if not payload["refresh_token"]:
        print("WARNING: response had no refresh_token — re-authorize and approve scope.",
              file=sys.stderr)
        sys.exit(1)


def run_manual(client_id, client_secret, redirect_uri):
    state = os.urandom(8).hex()
    url = build_authorize_url(client_id, redirect_uri, state)
    print("\nOpen this URL in your browser and authorize ocas-taste:\n")
    print("  " + url + "\n")
    pasted = input("After authorizing, paste the full redirected URL here: ").strip()
    if not pasted:
        print("No URL provided. Aborting.", file=sys.stderr)
        sys.exit(1)
    parsed = urllib.parse.urlparse(pasted)
    qs = urllib.parse.parse_qs(parsed.query)
    code = (qs.get("code") or [None])[0]
    err = (qs.get("error") or [None])[0]
    if err:
        print(f"Spotify returned an error: {err}", file=sys.stderr)
        sys.exit(1)
    if not code:
        print("Could not find 'code' in the pasted URL.", file=sys.stderr)
        sys.exit(1)
    data = exchange_code(code, client_id, client_secret, redirect_uri)
    write_token(data)


def run_auto(client_id, client_secret, redirect_uri):
    state = os.urandom(8).hex()
    url = build_authorize_url(client_id, redirect_uri, state)
    captured = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            captured["code"] = (qs.get("code") or [None])[0]
            captured["error"] = (qs.get("error") or [None])[0]
            captured["state"] = (qs.get("state") or [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>ocas-taste authorized.</h2>"
                             b"<p>You can close this window.</p></body></html>")

        def log_message(self, format, *args):  # noqa: A002 - match base signature
            pass  # quiet

    parsed = urllib.parse.urlparse(redirect_uri)
    port = parsed.port or 8888
    try:
        server = HTTPServer(("127.0.0.1", port), Handler)
    except OSError as e:
        print(f"Could not start local callback server on port {port}: {e}")
        print("Falling back to manual mode.\n")
        return run_manual(client_id, client_secret, redirect_uri)

    print(f"\nOpening browser to authorize ocas-taste...\n  {url}\n")
    try:
        webbrowser.open(url)
    except Exception:
        print("(Could not auto-open browser — open the URL above manually.)")

    server.handle_request()  # blocks until one request
    server.server_close()

    if captured.get("error"):
        print(f"Spotify returned an error: {captured['error']}", file=sys.stderr)
        sys.exit(1)
    if not captured.get("code"):
        print("No authorization code received from the callback.", file=sys.stderr)
        sys.exit(1)
    if captured.get("state") != state:
        print("State mismatch — possible CSRF. Aborting.", file=sys.stderr)
        sys.exit(1)
    data = exchange_code(captured["code"], client_id, client_secret, redirect_uri)
    write_token(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manual", action="store_true",
                    help="Do not open a browser; print the URL and read a pasted redirect.")
    args = ap.parse_args()

    client_id, client_secret, redirect_uri = get_env()

    if args.manual:
        run_manual(client_id, client_secret, redirect_uri)
    else:
        run_auto(client_id, client_secret, redirect_uri)

    print("\nNext: bridge the token into .env so the cron puller can read it:")
    print("  python3 apply_spotify_token_to_env.py")
    print("Then verify: hermes cron run e0a126b6c9f7")


if __name__ == "__main__":
    main()
