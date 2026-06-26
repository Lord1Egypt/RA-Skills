#!/usr/bin/env python3
"""
Enable Banking — HTTPS Callback Server
Listens for OAuth2 authorization callbacks and stores codes for pickup.

Usage:
    python callback_server.py                  # Start on port 8443
    python callback_server.py --port 9443      # Custom port

Endpoints:
    GET /callback?code=...&state=...   → Stores code in pending_callbacks/{state}.json
    GET /health                        → 200 OK
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SKILL_DIR = Path(__file__).resolve().parent.parent
KEYS_DIR = SKILL_DIR / ".keys"
CERT_FILE = KEYS_DIR / "callback.crt"
KEY_FILE = KEYS_DIR / "callback.key"
PENDING_DIR = SKILL_DIR / "pending_callbacks"


# ---------------------------------------------------------------------------
# Self-signed cert generation
# ---------------------------------------------------------------------------

def ensure_cert():
    """Generate self-signed cert if not present."""
    if CERT_FILE.exists() and KEY_FILE.exists():
        return
    print(f"🔐 Generating self-signed certificate...", file=sys.stderr)
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(KEY_FILE),
            "-out", str(CERT_FILE),
            "-days", "365",
            "-nodes",
            "-subj", "/CN=localhost",
        ],
        check=True,
        capture_output=True,
    )
    os.chmod(KEY_FILE, 0o600)
    os.chmod(CERT_FILE, 0o600)
    print(f"✅ Certificate created: {CERT_FILE}", file=sys.stderr)


# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------

class CallbackHandler(BaseHTTPRequestHandler):
    """Handles OAuth2 callbacks and health checks."""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
            return

        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            state = params.get("state", [None])[0]

            if code and state:
                # Save callback
                PENDING_DIR.mkdir(parents=True, exist_ok=True)
                callback_data = {
                    "code": code,
                    "state": state,
                    "receivedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
                path = PENDING_DIR / f"{state}.json"
                with open(path, "w") as f:
                    json.dump(callback_data, f, indent=2)
                os.chmod(path, 0o600)

                print(f"✅ Callback received: state={state}", file=sys.stderr)

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""<!DOCTYPE html>
<html><body style="font-family:sans-serif;text-align:center;padding:60px">
<h2>&#10003; Autorisierung erfolgreich!</h2>
<p>Sie k&ouml;nnen dieses Fenster schlie&szlig;en.</p>
<p style="color:#888;font-size:14px">Die Verbindung wird automatisch hergestellt.</p>
</body></html>""")
            else:
                error = params.get("error", ["unknown"])[0]
                print(f"❌ Callback error: {error}", file=sys.stderr)

                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"""<!DOCTYPE html>
<html><body style="font-family:sans-serif;text-align:center;padding:60px">
<h2>&#10007; Autorisierung fehlgeschlagen</h2>
<p>Fehler: {error}</p>
</body></html>""".encode())
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        """Log to stderr."""
        print(f"[callback-server] {args[0]}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Enable Banking — HTTPS Callback Server")
    parser.add_argument("--port", type=int, default=8443, help="Port (default: 8443)")
    parser.add_argument("--no-ssl", action="store_true", help="Run without SSL (HTTP only)")
    args = parser.parse_args()

    if not args.no_ssl:
        ensure_cert()

    try:
        server = HTTPServer(("0.0.0.0", args.port), CallbackHandler)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {args.port} already in use.", file=sys.stderr)
            sys.exit(1)
        raise

    if not args.no_ssl:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(CERT_FILE), str(KEY_FILE))
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        proto = "HTTPS"
    else:
        proto = "HTTP"

    print(f"🌐 Callback server running on {proto} port {args.port}", file=sys.stderr)
    print(f"   Health: {proto.lower()}://localhost:{args.port}/health", file=sys.stderr)
    print(f"   Callback: {proto.lower()}://localhost:{args.port}/callback", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    main()
