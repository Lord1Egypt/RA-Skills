from __future__ import annotations

import base64
import json
import os
import time
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

API_ROOT = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
DEFAULT_CREDS_PATH = Path.home() / ".openclaw" / "spotify-credentials.json"
DEFAULT_TOKEN_PATH = Path.home() / ".openclaw" / "spotify-token.json"


class SpotifyError(RuntimeError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_credentials(explicit_path: str | None = None) -> dict[str, str]:
    creds: dict[str, str] = {}
    if os.getenv("SPOTIFY_CLIENT_ID"):
        creds["client_id"] = os.environ["SPOTIFY_CLIENT_ID"]
    if os.getenv("SPOTIFY_CLIENT_SECRET"):
        creds["client_secret"] = os.environ["SPOTIFY_CLIENT_SECRET"]
    if os.getenv("SPOTIFY_REDIRECT_URI"):
        creds["redirect_uri"] = os.environ["SPOTIFY_REDIRECT_URI"]

    path = Path(explicit_path) if explicit_path else DEFAULT_CREDS_PATH
    if path.exists():
        file_creds = _read_json(path)
        for key in ("client_id", "client_secret", "redirect_uri"):
            if key not in creds and file_creds.get(key):
                creds[key] = str(file_creds[key])

    if "client_id" not in creds or "client_secret" not in creds or "redirect_uri" not in creds:
        raise SpotifyError(
            "Missing Spotify credentials. Set SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REDIRECT_URI "
            "or create ~/.openclaw/spotify-credentials.json"
        )
    return creds


def _basic_auth_header(client_id: str, client_secret: str) -> str:
    raw = f"{client_id}:{client_secret}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _post_form(url: str, data: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers=headers or {},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SpotifyError(f"Spotify HTTP {exc.code}: {body}") from exc


def save_token(token: dict[str, Any], path: str | None = None) -> Path:
    out = Path(path) if path else DEFAULT_TOKEN_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    token["saved_at"] = int(time.time())
    out.write_text(json.dumps(token, indent=2), encoding="utf-8")
    return out


def load_token(path: str | None = None) -> dict[str, Any]:
    token_path = Path(path) if path else DEFAULT_TOKEN_PATH
    if not token_path.exists():
        raise SpotifyError(f"Missing token file: {token_path}")
    return _read_json(token_path)


def refresh_token_if_needed(creds: dict[str, str], token: dict[str, Any], *, token_path: str | None = None) -> dict[str, Any]:
    expires_in = int(token.get("expires_in", 3600) or 3600)
    saved_at = int(token.get("saved_at", 0) or 0)
    if token.get("access_token") and time.time() < saved_at + expires_in - 120:
        return token

    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise SpotifyError("Token is expired and no refresh_token is available.")

    refreshed = _post_form(
        TOKEN_URL,
        {"grant_type": "refresh_token", "refresh_token": refresh_token},
        headers={"Authorization": _basic_auth_header(creds["client_id"], creds["client_secret"])},
    )
    refreshed["refresh_token"] = refreshed.get("refresh_token") or refresh_token
    save_token(refreshed, token_path)
    return refreshed


def get_access_token(creds_path: str | None = None, token_path: str | None = None) -> str:
    creds = load_credentials(creds_path)
    token = load_token(token_path)
    token = refresh_token_if_needed(creds, token, token_path=token_path)
    return token["access_token"]


def authorize(
    scopes: list[str],
    *,
    creds_path: str | None = None,
    token_path: str | None = None,
    open_browser: bool = True,
) -> dict[str, Any]:
    creds = load_credentials(creds_path)
    parsed = urllib.parse.urlparse(creds["redirect_uri"])
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 8888
    redirect_path = parsed.path or "/callback"
    result: dict[str, str] = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if urllib.parse.urlparse(self.path).path != redirect_path:
                self.send_response(404)
                self.end_headers()
                return
            if "error" in query:
                result["error"] = query["error"][0]
            elif "code" in query:
                result["code"] = query["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Spotify auth received. You can close this tab.")

        def log_message(self, format: str, *args: Any) -> None:
            return

    server = HTTPServer((host, port), CallbackHandler)
    params = {
        "client_id": creds["client_id"],
        "response_type": "code",
        "redirect_uri": creds["redirect_uri"],
        "scope": " ".join(scopes),
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    if open_browser:
        webbrowser.open(url)
    else:
        print(url)

    server.handle_request()
    server.server_close()

    if result.get("error"):
        raise SpotifyError(f"Spotify auth error: {result['error']}")
    if not result.get("code"):
        raise SpotifyError("No authorization code received.")

    token = _post_form(
        TOKEN_URL,
        {
            "grant_type": "authorization_code",
            "code": result["code"],
            "redirect_uri": creds["redirect_uri"],
        },
        headers={"Authorization": _basic_auth_header(creds["client_id"], creds["client_secret"])},
    )
    save_token(token, token_path)
    return token


def request_json(
    url: str,
    *,
    method: str = "GET",
    token: str | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise SpotifyError(f"Spotify API HTTP {exc.code}: {body_text}") from exc


def search_tracks(query: str, *, access_token: str, limit: int = 10, market: str | None = None) -> dict:
    params = {"q": query, "type": "track", "limit": limit}
    if market:
        params["market"] = market
    url = f"{API_ROOT}/search?" + urllib.parse.urlencode(params)
    return request_json(url, token=access_token)


def current_user(access_token: str) -> dict:
    return request_json(f"{API_ROOT}/me", token=access_token)


def create_playlist(
    name: str,
    *,
    access_token: str,
    public: bool = False,
    description: str = "",
) -> dict:
    return request_json(
        f"{API_ROOT}/me/playlists",
        method="POST",
        token=access_token,
        body={"name": name, "public": public, "description": description},
    )


def add_tracks_to_playlist(playlist_id: str, track_uris: list[str], *, access_token: str) -> dict:
    if not track_uris:
        return {"snapshot_id": None}
    return request_json(
        f"{API_ROOT}/playlists/{playlist_id}/items",
        method="POST",
        token=access_token,
        body={"uris": track_uris},
    )
