#!/usr/bin/env python3
"""Interactive Strava OAuth login.

Env:
- STRAVA_CLIENT_ID
- STRAVA_CLIENT_SECRET
- STRAVA_REDIRECT_URI
Optional:
- STRAVA_SCOPES (default: activity:read_all)
- STRAVA_TOKEN_PATH

Writes token JSON to STRAVA_TOKEN_PATH.
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from strava_token import AUTH_URL, exchange_code_for_token, save_token, token_path


DEFAULT_SCOPES = "activity:read_all"


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
        raise SystemExit("Loopback mode requires STRAVA_REDIRECT_URI like http://127.0.0.1:<port>/<path>")
    if not u.port:
        raise SystemExit("Loopback mode requires an explicit port in STRAVA_REDIRECT_URI")

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
    ap.add_argument("--loopback", action="store_true", help="Use local 127.0.0.1 redirect (requires STRAVA_REDIRECT_URI to be a loopback URL)")
    args = ap.parse_args()

    client_id = must_env("STRAVA_CLIENT_ID")
    client_secret = must_env("STRAVA_CLIENT_SECRET")
    redirect_uri = must_env("STRAVA_REDIRECT_URI")

    scopes = os.environ.get("STRAVA_SCOPES", DEFAULT_SCOPES)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "approval_prompt": "auto",
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

    tok = exchange_code_for_token(code=code, client_id=client_id, client_secret=client_secret)
    p = save_token(tok, token_path())
    print(f"\n[OK] Token saved to: {p}")


if __name__ == "__main__":
    main()
