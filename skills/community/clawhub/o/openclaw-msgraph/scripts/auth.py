#!/usr/bin/env python3
"""
Microsoft Graph PKCE auth for OpenClaw msgraph skill.
Manages token lifecycle for personal Microsoft accounts.

Usage:
  python auth.py login    - Initiate PKCE auth flow (opens browser)
  python auth.py status   - Show current auth status
  python auth.py refresh  - Force token refresh
  python auth.py token    - Print current access token (for scripting)
"""

import os
import sys
import json
import hashlib
import secrets
import base64
import time
import urllib.parse
import urllib.request
import urllib.error
import http.server
import threading
import subprocess
from pathlib import Path
import configparser

# ── Config helper ──────────────────────────────────────────────────────────────

def load_config():
    config_file = Path(__file__).parent.parent / "config.ini"
    if not config_file.exists():
        print(f"ERROR: config.ini not found at {config_file}", file=sys.stderr)
        print("Copy config.example.ini to config.ini and set your Client ID.", file=sys.stderr)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_file)
    return config["msgraph"]

cfg = load_config()
CLIENT_ID = cfg["client_id"]
TENANT = cfg.get("tenant", "consumers")
SCOPES = cfg.get("scopes", "Mail.ReadWrite Calendars.ReadWrite offline_access User.Read")
TOKEN_FILE = Path.home() / ".openclaw" / "msgraph-tokens.json"
REDIRECT_PORT = int(cfg.get("redirect_port", "8765"))
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/callback"
AUTH_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"


# ── PKCE helpers ──────────────────────────────────────────────────────────────

def generate_pkce():
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def build_auth_url(code_challenge, state):
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "response_mode": "query",
        "state": state,
    }
    return AUTH_URL + "?" + urllib.parse.urlencode(params)


# ── Token storage ─────────────────────────────────────────────────────────────

def load_tokens():
    if TOKEN_FILE.exists():
        try:
            return json.loads(TOKEN_FILE.read_text())
        except Exception:
            return {}
    return {}


def save_tokens(tokens):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    TOKEN_FILE.chmod(0o600)


# ── Token exchange ─────────────────────────────────────────────────────────────

def exchange_code(code, code_verifier):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
        "scope": SCOPES,
    }, quote_via=urllib.parse.quote).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST",
                              headers={
                                  "Content-Type": "application/x-www-form-urlencoded",
                                  "Origin": "http://localhost:8765",
                              })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise


def do_refresh(refresh_token):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": SCOPES,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST",
                              headers={
                                  "Content-Type": "application/x-www-form-urlencoded",
                                  "Origin": "http://localhost:8765",
                              })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


# ── Public: get valid access token ────────────────────────────────────────────

def get_access_token():
    """Return a valid access token, refreshing if needed. Exits on failure."""
    tokens = load_tokens()
    if not tokens:
        print("ERROR: Not authenticated. Run: python auth.py login", file=sys.stderr)
        sys.exit(1)

    if time.time() < tokens.get("expires_at", 0) - 60:
        return tokens["access_token"]

    # Refresh
    try:
        new = do_refresh(tokens["refresh_token"])
        new["expires_at"] = time.time() + new.get("expires_in", 3600)
        new.setdefault("refresh_token", tokens["refresh_token"])
        save_tokens(new)
        return new["access_token"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR: Token refresh failed ({e.code}): {body}", file=sys.stderr)
        print("Re-run: python auth.py login", file=sys.stderr)
        sys.exit(1)


# ── Local callback server ─────────────────────────────────────────────────────

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    captured = {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/callback":
            params = dict(urllib.parse.parse_qsl(parsed.query))
            CallbackHandler.captured.update(params)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html><body style="font-family:sans-serif;text-align:center;margin-top:80px">
                <h2>&#10003; Authentication successful!</h2>
                <p>You can close this tab and return to your terminal.</p>
                </body></html>
            """)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silence server logs


def open_browser(url):
    """Open URL — handles WSL2 by using cmd.exe if available."""
    try:
        subprocess.run(["cmd.exe", "/c", "start", "", url],
                       capture_output=True, check=True)
        return
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        subprocess.run(["xdg-open", url], capture_output=True)
    except FileNotFoundError:
        pass


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_login():
    code_verifier, code_challenge = generate_pkce()
    state = secrets.token_urlsafe(16)
    auth_url = build_auth_url(code_challenge, state)

    # Start local server
    server = http.server.HTTPServer(("127.0.0.1", REDIRECT_PORT), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    print(f"\nOpening your browser for Microsoft login...")
    print(f"\nIf the browser doesn't open, paste this URL manually:\n\n  {auth_url}\n")
    open_browser(auth_url)

    print("Waiting for callback... (Ctrl+C to cancel)\n")
    timeout = 120
    start = time.time()
    try:
        while not CallbackHandler.captured and time.time() - start < timeout:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCancelled.")
        server.shutdown()
        sys.exit(1)

    server.shutdown()

    if not CallbackHandler.captured:
        print("ERROR: Timed out waiting for callback.")
        print("If your browser redirected but nothing happened, try again.")
        sys.exit(1)

    params = CallbackHandler.captured
    if "error" in params:
        print(f"ERROR: {params['error']}: {params.get('error_description', '')}")
        sys.exit(1)
    if params.get("state") != state:
        print("ERROR: State mismatch — possible CSRF.")
        sys.exit(1)

    code = params["code"]
    tokens = exchange_code(code, code_verifier)
    tokens["expires_at"] = time.time() + tokens.get("expires_in", 3600)
    save_tokens(tokens)
    print(f"✓ Authenticated! Tokens saved to {TOKEN_FILE}")


def cmd_status():
    tokens = load_tokens()
    if not tokens:
        print("Status: NOT authenticated")
        print("Run: python auth.py login")
        return
    expires_at = tokens.get("expires_at", 0)
    remaining = expires_at - time.time()
    if remaining > 0:
        print(f"Status: authenticated")
        print(f"Access token expires in: {int(remaining)}s")
    else:
        print("Status: access token expired (will auto-refresh on next use)")
    has_refresh = bool(tokens.get("refresh_token"))
    print(f"Refresh token: {'present' if has_refresh else 'MISSING'}")
    print(f"Token file: {TOKEN_FILE}")


def cmd_refresh():
    tokens = load_tokens()
    if not tokens or not tokens.get("refresh_token"):
        print("ERROR: No refresh token. Run: python auth.py login")
        sys.exit(1)
    print("Refreshing token...")
    new = do_refresh(tokens["refresh_token"])
    new["expires_at"] = time.time() + new.get("expires_in", 3600)
    new.setdefault("refresh_token", tokens["refresh_token"])
    save_tokens(new)
    print(f"✓ Token refreshed. Expires in {new.get('expires_in', 3600)}s")


def cmd_token():
    print(get_access_token())


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "login":
        cmd_login()
    elif cmd == "status":
        cmd_status()
    elif cmd == "refresh":
        cmd_refresh()
    elif cmd == "token":
        cmd_token()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python auth.py [login|status|refresh|token]")
        sys.exit(1)
