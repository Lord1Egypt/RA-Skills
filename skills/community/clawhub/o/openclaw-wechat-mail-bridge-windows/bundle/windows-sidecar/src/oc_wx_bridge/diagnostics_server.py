from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import threading
from typing import Any

from .adapters.base import WeChatDesktopAdapter
from .bridge_client import BridgeClient
from .config import DiagnosticsConfig

LOGGER = logging.getLogger(__name__)


class _DiagnosticsHandler(BaseHTTPRequestHandler):
    adapter: WeChatDesktopAdapter
    bridge_client: BridgeClient

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._handle_health()
            return
        if self.path == "/groups":
            self._handle_groups()
            return
        self.send_response(404)
        self.end_headers()

    def _handle_health(self) -> None:
        try:
            adapter_health = self.adapter.health().model_dump()
            bridge_health = self.bridge_client.health()
            payload = {
                "ok": True,
                "adapter": adapter_health,
                "bridge": bridge_health,
            }
            self._send_json(200, payload)
        except Exception as error:
            self._send_json(500, {"ok": False, "error": str(error)})

    def _handle_groups(self) -> None:
        try:
            groups = self.adapter.list_groups()
            payload = {
                "ok": True,
                "count": len(groups),
                "groups": [{"chatId": g.chat_id, "chatName": g.chat_name} for g in groups],
            }
            self._send_json(200, payload)
        except Exception as error:
            self._send_json(500, {"ok": False, "error": str(error)})

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.debug("diagnostics %s", format % args)


def start_diagnostics_server(
    config: DiagnosticsConfig,
    adapter: WeChatDesktopAdapter,
    bridge_client: BridgeClient,
) -> threading.Thread:
    _DiagnosticsHandler.adapter = adapter
    _DiagnosticsHandler.bridge_client = bridge_client
    server = ThreadingHTTPServer((config.host, config.port), _DiagnosticsHandler)

    def _run() -> None:
        LOGGER.info("diagnostics server listening on http://%s:%s", config.host, config.port)
        server.serve_forever(poll_interval=0.5)

    thread = threading.Thread(target=_run, name="diagnostics-server", daemon=True)
    thread.start()
    return thread

