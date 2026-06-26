from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import AppConfig, MalSecrets
from .mal_client import TokenResponse


class OAuthCallbackError(RuntimeError):
    pass


@dataclass(slots=True)
class OAuthCallbackResult:
    code: str
    state: str | None
    query: dict[str, list[str]]


@dataclass(slots=True)
class PersistedTokenPaths:
    access_token_path: Path
    refresh_token_path: Path


class _SingleCallbackServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], expected_state: str | None):
        super().__init__(server_address, _CallbackHandler)
        self.expected_state = expected_state
        self.result: OAuthCallbackResult | None = None
        self.error: str | None = None
        self.done = threading.Event()


class _CallbackHandler(BaseHTTPRequestHandler):
    server: _SingleCallbackServer

    def log_message(self, format: str, *args: Any) -> None:  # pragma: no cover - noisy stdlib hook
        return

    def do_GET(self) -> None:  # noqa: N802 - stdlib interface
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self._send_text(404, "Not found")
            return

        query = parse_qs(parsed.query, keep_blank_values=True)
        state = query.get("state", [None])[0]
        error = query.get("error", [None])[0]
        code = query.get("code", [None])[0]

        if self.server.expected_state and state != self.server.expected_state:
            self.server.error = "OAuth callback state mismatch"
            self._send_html(400, "<h1>MAL auth failed</h1><p>State mismatch. Return to the terminal.</p>")
            self.server.done.set()
            return

        if error:
            description = query.get("error_description", [""])[0]
            self.server.error = f"OAuth callback returned error={error}: {description}".strip()
            self._send_html(400, "<h1>MAL auth failed</h1><p>The authorization page returned an error. Return to the terminal.</p>")
            self.server.done.set()
            return

        if not code:
            self.server.error = "OAuth callback did not include a code"
            self._send_html(400, "<h1>MAL auth failed</h1><p>No authorization code was returned. Return to the terminal.</p>")
            self.server.done.set()
            return

        self.server.result = OAuthCallbackResult(code=code, state=state, query=query)
        self._send_html(200, "<h1>MAL auth complete</h1><p>You can close this tab and return to the terminal.</p>")
        self.server.done.set()

    def _send_text(self, status: int, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_html(self, status: int, body: str) -> None:
        encoded = f"<!doctype html><html><body>{body}</body></html>".encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def write_secret_file(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(value.strip() + "\n")
        temp_path = Path(tmp.name)
    os.chmod(temp_path, 0o600)
    temp_path.replace(path)
    os.chmod(path, 0o600)


def persist_token_response(token: TokenResponse, secrets: MalSecrets) -> PersistedTokenPaths:
    write_secret_file(secrets.access_token_path, token.access_token)
    if token.refresh_token:
        write_secret_file(secrets.refresh_token_path, token.refresh_token)
    return PersistedTokenPaths(
        access_token_path=secrets.access_token_path,
        refresh_token_path=secrets.refresh_token_path,
    )


def wait_for_oauth_callback(host: str, port: int, expected_state: str | None, timeout_seconds: float = 300.0) -> OAuthCallbackResult:
    server = _SingleCallbackServer((host, port), expected_state=expected_state)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
    thread.start()
    try:
        if not server.done.wait(timeout_seconds):
            raise TimeoutError(f"Timed out waiting for MAL OAuth callback after {timeout_seconds:.0f}s")
        if server.error:
            raise OAuthCallbackError(server.error)
        if server.result is None:
            raise OAuthCallbackError("OAuth callback finished without a result")
        return server.result
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1.0)


def format_auth_flow_prompt(config: AppConfig, authorization_url: str, timeout_seconds: float) -> str:
    return "\n".join(
        [
            "Starting local MAL OAuth callback listener.",
            f"bind_host={config.mal.bind_host}",
            f"redirect_uri={config.mal.redirect_uri}",
            f"timeout_seconds={int(timeout_seconds)}",
            "",
            "Open this URL in a browser that can reach the redirect_uri host:",
            authorization_url,
            "",
            "Waiting for a single /callback hit...",
        ]
    )
