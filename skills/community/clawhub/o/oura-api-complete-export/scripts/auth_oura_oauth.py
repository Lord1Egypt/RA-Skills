#!/usr/bin/env python3
import argparse
import json
import os
import secrets
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests

AUTH_URL = "https://cloud.ouraring.com/oauth/authorize"
TOKEN_URL = "https://api.ouraring.com/oauth/token"
CONFIG_PATH = Path.home() / ".config" / "oura-oauth" / "config.json"


class CallbackHandler(BaseHTTPRequestHandler):
    code = None
    state = None
    error = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        CallbackHandler.code = (qs.get("code") or [None])[0]
        CallbackHandler.state = (qs.get("state") or [None])[0]
        CallbackHandler.error = (qs.get("error") or [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h3>Oura auth received. You can close this tab.</h3></body></html>")

    def log_message(self, format, *args):
        return


def run_server(host: str, port: int):
    server = HTTPServer((host, port), CallbackHandler)
    server.timeout = 1
    return server


def save_config(payload):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    os.chmod(CONFIG_PATH, 0o600)


def main():
    ap = argparse.ArgumentParser(description="Authenticate Oura OAuth app and store refresh/access tokens")
    ap.add_argument("--client-id", required=True)
    ap.add_argument("--client-secret", required=True)
    ap.add_argument("--redirect-uri", required=True)
    ap.add_argument("--scope", default="personal daily heartrate workout session tag")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    parsed = urllib.parse.urlparse(args.redirect_uri)
    if parsed.scheme != "http" or not parsed.hostname or not parsed.port:
        raise SystemExit("redirect-uri must be http://host:port/path for local callback capture")

    state = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": args.client_id,
        "redirect_uri": args.redirect_uri,
        "scope": args.scope,
        "state": state,
    }
    auth_link = AUTH_URL + "?" + urllib.parse.urlencode(params)

    server = run_server(parsed.hostname, parsed.port)
    stop = threading.Event()

    def server_loop():
        while not stop.is_set():
            server.handle_request()

    thread = threading.Thread(target=server_loop, daemon=True)
    thread.start()

    print("Open this URL to authorize:")
    print(auth_link)
    try:
        webbrowser.open(auth_link)
    except Exception:
        pass

    started = time.time()
    while time.time() - started < args.timeout:
        if CallbackHandler.error:
            stop.set()
            raise SystemExit(f"OAuth error: {CallbackHandler.error}")
        if CallbackHandler.code:
            break
        time.sleep(0.2)

    stop.set()

    if not CallbackHandler.code:
        raise SystemExit("Timed out waiting for OAuth callback")
    if CallbackHandler.state != state:
        raise SystemExit("State mismatch in callback")

    token_resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": CallbackHandler.code,
            "redirect_uri": args.redirect_uri,
            "client_id": args.client_id,
            "client_secret": args.client_secret,
        },
        timeout=30,
    )

    if token_resp.status_code >= 400:
        raise SystemExit(f"Token exchange failed: {token_resp.status_code} {token_resp.text[:500]}")

    tk = token_resp.json()
    payload = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "redirect_uri": args.redirect_uri,
        "scope": args.scope,
        "token": tk,
        "saved_at": int(time.time()),
    }
    save_config(payload)
    print(f"Saved OAuth config to {CONFIG_PATH}")


if __name__ == "__main__":
    main()
