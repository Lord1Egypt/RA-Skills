import base64
import json
import os
import secrets
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

CONFIG_DIR = Path.home() / ".clawdbot" / "credentials" / "ticktick-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

OAUTH_BASE = "https://dida365.com/oauth"
API_BASE = "https://api.dida365.com/open/v1"
DEFAULT_REDIRECT_PORT = 8080
DEFAULT_REDIRECT_URI = f"http://localhost:{DEFAULT_REDIRECT_PORT}"


def generate_state() -> str:
    return f"ticktick-cli-{secrets.token_hex(16)}"


def load_config() -> dict | None:
    try:
        return json.loads(CONFIG_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    try:
        os.chmod(CONFIG_DIR, 0o700)
        os.chmod(CONFIG_FILE, 0o600)
    except OSError:
        pass


def get_valid_token() -> str:
    config = load_config()
    if not config:
        raise RuntimeError("Not authenticated. Run 'ticktick auth' to set up credentials.")
    if not config.get("accessToken"):
        raise RuntimeError("No access token found. Run 'ticktick auth' to authenticate.")

    # Check expiry with 5-minute buffer (timestamps stored as JS milliseconds)
    expiry = config.get("tokenExpiry")
    if expiry and time.time() * 1000 > expiry - 300_000:
        if config.get("refreshToken"):
            return _refresh_access_token(config)
        raise RuntimeError("Token expired. Run 'ticktick auth' to re-authenticate.")

    return config["accessToken"]


def _refresh_access_token(config: dict) -> str:
    credentials = base64.b64encode(
        f"{config['clientId']}:{config['clientSecret']}".encode()
    ).decode()

    resp = requests.post(
        f"{OAUTH_BASE}/token",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": config["refreshToken"],
        },
    )
    if not resp.ok:
        raise RuntimeError(f"Failed to refresh token: {resp.status_code} {resp.text}")

    data = resp.json()
    config["accessToken"] = data["access_token"]
    if "refresh_token" in data:
        config["refreshToken"] = data["refresh_token"]
    config["tokenExpiry"] = int(time.time() * 1000) + data["expires_in"] * 1000
    save_config(config)
    return config["accessToken"]


def setup_credentials(client_id: str, client_secret: str) -> None:
    config = load_config() or {}
    config["clientId"] = client_id
    config["clientSecret"] = client_secret
    config["redirectUri"] = DEFAULT_REDIRECT_URI
    save_config(config)
    print("Credentials saved successfully.")


def _exchange_code(config: dict, auth_code: str) -> None:
    credentials = base64.b64encode(
        f"{config['clientId']}:{config['clientSecret']}".encode()
    ).decode()
    redirect_uri = config.get("redirectUri", DEFAULT_REDIRECT_URI)

    resp = requests.post(
        f"{OAUTH_BASE}/token",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
    )
    if not resp.ok:
        raise RuntimeError(
            f"Failed to exchange code for token: {resp.status_code} - {resp.text}"
        )

    data = resp.json()
    config["accessToken"] = data["access_token"]
    config["refreshToken"] = data["refresh_token"]
    config["tokenExpiry"] = int(time.time() * 1000) + data["expires_in"] * 1000
    save_config(config)


def authenticate() -> None:
    config = load_config()
    if not config or not config.get("clientId") or not config.get("clientSecret"):
        raise RuntimeError(
            "No credentials found. Run 'ticktick auth --client-id <id> --client-secret <secret>' first."
        )

    redirect_uri = config.get("redirectUri", DEFAULT_REDIRECT_URI)
    port = int(urlparse(redirect_uri).port or DEFAULT_REDIRECT_PORT)
    state = generate_state()

    # Shared state between server thread and main thread
    result: dict = {"code": None, "error": None}
    event = threading.Event()

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            returned_state = params.get("state", [None])[0]
            code = params.get("code", [None])[0]
            error = params.get("error", [None])[0]

            if returned_state != state:
                self._respond(400, b"<html><body><h1>Auth Failed: Invalid state</h1></body></html>")
                result["error"] = "Invalid OAuth state."
            elif error:
                self._respond(400, f"<html><body><h1>Auth Failed: {error}</h1></body></html>".encode())
                result["error"] = f"OAuth error: {error}"
            elif code:
                self._respond(200, b"<html><body><h1>Authentication Successful! You can close this window.</h1></body></html>")
                result["code"] = code
            event.set()

        def _respond(self, status: int, body: bytes):
            self.send_response(status)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            pass  # suppress access log

    server = HTTPServer(("127.0.0.1", port), _Handler)
    server.timeout = 300  # so handle_request() returns after 5 min even with no request

    from urllib.parse import urlencode
    auth_url = (
        f"{OAUTH_BASE}/authorize?"
        + urlencode({
            "scope": "tasks:read tasks:write",
            "client_id": config["clientId"],
            "state": state,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        })
    )

    print("\nOpening browser for authentication...")
    print(f"If browser doesn't open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    # Serve exactly one request then stop
    def _serve():
        server.handle_request()

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()

    triggered = event.wait(timeout=300)
    server.server_close()

    if not triggered:
        raise RuntimeError("Authentication timed out. Please try again.")
    if result["error"]:
        raise RuntimeError(result["error"])

    _exchange_code(config, result["code"])
    print("Authentication successful! Tokens saved.")


def authenticate_manual() -> None:
    config = load_config()
    if not config or not config.get("clientId") or not config.get("clientSecret"):
        raise RuntimeError(
            "No credentials found. Run 'ticktick auth --client-id <id> --client-secret <secret> --manual' first."
        )

    redirect_uri = config.get("redirectUri", DEFAULT_REDIRECT_URI)
    state = generate_state()

    from urllib.parse import urlencode
    auth_url = (
        f"{OAUTH_BASE}/authorize?"
        + urlencode({
            "scope": "tasks:read tasks:write",
            "client_id": config["clientId"],
            "state": state,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        })
    )

    print("\n=== Manual Authentication ===\n")
    print("1. Open this URL in your browser:\n")
    print(auth_url)
    print("\n2. Authorize the app")
    print("3. You'll be redirected to a URL like: http://localhost:8080/?code=XXXXX&state=STATE")
    print("4. Copy that ENTIRE redirect URL and paste it below:\n")

    redirect_url = input("Paste redirect URL: ").strip()
    if not redirect_url:
        raise RuntimeError("No URL provided.")

    parsed = urlparse(redirect_url)
    params = parse_qs(parsed.query)

    returned_state = params.get("state", [None])[0]
    if not returned_state:
        raise RuntimeError("Missing state in redirect URL. Paste the full redirect URL.")
    if returned_state != state:
        raise RuntimeError("State mismatch. Please restart auth.")

    auth_code = params.get("code", [None])[0]
    if not auth_code:
        raise RuntimeError("No code found in URL.")

    print("\nExchanging code for tokens...")
    _exchange_code(config, auth_code)
    print("\n✓ Authentication successful! Tokens saved.")


def check_auth() -> bool:
    try:
        get_valid_token()
        return True
    except RuntimeError:
        return False


def logout() -> None:
    config = load_config()
    if config:
        config.pop("accessToken", None)
        config.pop("refreshToken", None)
        config.pop("tokenExpiry", None)
        save_config(config)
        print("Logged out successfully. Credentials preserved.")
    else:
        print("No configuration found.")
