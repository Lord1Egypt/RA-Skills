#!/usr/bin/env python3
"""Spotify OAuth callback server. Run once to authorize, then tokens auto-refresh."""

import json
import os
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

CREDS_FILE = os.path.expanduser("~/.config/spotify/credentials.json")
TOKEN_FILE = os.path.expanduser("~/.config/spotify/tokens.json")
SCOPES = "user-modify-playback-state user-read-playback-state"

with open(CREDS_FILE) as f:
    creds = json.load(f)

CLIENT_ID = creds["client_id"]
CLIENT_SECRET = creds["client_secret"]
REDIRECT_URI = creds["redirect_uri"]


def get_auth_url():
    params = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    })
    return f"https://accounts.spotify.com/authorize?{params}"


def exchange_code(code):
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request("https://accounts.spotify.com/api/token", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        # Accept both /callback and / (Tailscale Serve may strip the path)
        if parsed.path not in ("/callback", "/"):
            self.send_response(404)
            self.end_headers()
            return

        params = urllib.parse.parse_qs(parsed.query)
        if "error" in params:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {params['error'][0]}".encode())
            return

        code = params.get("code", [None])[0]
        if not code:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code parameter")
            return

        try:
            tokens = exchange_code(code)
            with open(TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=2)

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html><body style="background:#0d0d1a;color:#e2e8f0;font-family:system-ui;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
            <div style="text-align:center">
                <h1 style="color:#22c55e">Connected!</h1>
                <p>Spotify is linked. You can close this tab.</p>
            </div>
            </body></html>
            """)
            print(f"\n✅ Tokens saved to {TOKEN_FILE}")
            print("You can close this server now.")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Token exchange failed: {e}".encode())
            print(f"❌ Error: {e}")

    def log_message(self, format, *args):
        pass  # suppress request logs


if __name__ == "__main__":
    if "--url" in sys.argv:
        print(get_auth_url())
        sys.exit(0)

    port = 8888
    print(f"Auth URL:\n{get_auth_url()}\n")
    print(f"Waiting for callback on port {port}...")
    server = HTTPServer(("0.0.0.0", port), CallbackHandler)
    try:
        # Handle up to 5 requests (health checks, favicon, then actual callback)
        for _ in range(5):
            server.handle_request()
            if os.path.exists(TOKEN_FILE):
                break
    except KeyboardInterrupt:
        pass
    server.server_close()
