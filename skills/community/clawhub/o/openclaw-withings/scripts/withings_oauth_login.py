#!/usr/bin/env python3
"""Interactive Withings OAuth login.

Env:
- WITHINGS_CLIENT_ID
- WITHINGS_CLIENT_SECRET
- WITHINGS_REDIRECT_URI
Optional:
- WITHINGS_SCOPES (default: user.metrics user.activity)
- WITHINGS_TOKEN_PATH

Modes:
- default: copy/paste redirect URL or code
- --loopback: listen on loopback redirect URI (127.0.0.1)
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from withings_token import AUTH_URL, exchange_code_for_token, save_token, token_path


DEFAULT_SCOPES = "user.metrics user.activity"


def must_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v


def parse_code(user_input: str) -> str:
    s = user_input.strip()
    if s.startswith("http://") or s.startswith("https://"):
        u = urllib.parse.urlparse(s)
        q = urllib.parse.parse_qs(u.query)
        code = (q.get("code") or [None])[0]
        if code:
            return code
        raise SystemExit("Could not find ?code= in the pasted redirect URL")
    return s


def listen_for_code(redirect_uri: str, timeout_s: int = 180) -> str:
    u = urllib.parse.urlparse(redirect_uri)
    if u.scheme != "http" or u.hostname not in ("127.0.0.1", "localhost"):
        raise SystemExit("Loopback mode requires WITHINGS_REDIRECT_URI like http://127.0.0.1:<port>/<path>")
    if not u.port:
        raise SystemExit("Loopback mode requires an explicit port in WITHINGS_REDIRECT_URI")
    path = u.path or "/"

    got = {"code": None}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != path:
                self.send_response(404)
                self.end_headers()
                return
            q = urllib.parse.parse_qs(parsed.query)
            code = (q.get("code") or [None])[0]
            if code:
                got["code"] = code
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"OK. You can close this tab and return to OpenClaw.\n")
            else:
                self.send_response(400)
                self.end_headers()

        def log_message(self, fmt, *args):
            return

    httpd = HTTPServer((u.hostname, int(u.port)), Handler)
    httpd.timeout = 1

    import time

    deadline = time.time() + timeout_s
    while time.time() < deadline and not got["code"]:
        httpd.handle_request()

    try:
        httpd.server_close()
    except Exception:
        pass

    if not got["code"]:
        raise SystemExit("Timed out waiting for OAuth redirect. Use copy/paste mode instead.")
    return str(got["code"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--loopback", action="store_true", help="Use loopback redirect (same-machine browser authorization)")
    args = ap.parse_args()

    client_id = must_env("WITHINGS_CLIENT_ID")
    client_secret = must_env("WITHINGS_CLIENT_SECRET")
    redirect_uri = must_env("WITHINGS_REDIRECT_URI")

    scopes = os.environ.get("WITHINGS_SCOPES", DEFAULT_SCOPES)

    # Withings expects scope as comma-separated or space-separated; docs show space.
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scopes,
    }

    auth_url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    print("Open this URL in a browser and approve access:\n")
    print(auth_url)

    if args.loopback:
        print("\nWaiting for redirect on:")
        print(redirect_uri)
        code = listen_for_code(redirect_uri)
    else:
        print("\nAfter approval, paste either the full redirect URL or just the code:")
        code = parse_code(input("> "))

    tok = exchange_code_for_token(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    p = save_token(tok, token_path())
    print(f"\n[OK] Token saved to: {p}")


if __name__ == "__main__":
    main()
