from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import threading
from typing import Any

from .bridge_client import BridgeClient
from .config import WebhookProxyConfig

LOGGER = logging.getLogger(__name__)


class _WebhookHandler(BaseHTTPRequestHandler):
    bridge_client: BridgeClient
    bridge_secret: str
    inbound_secret: str | None

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/bhmailer/webhook":
            self.send_response(404)
            self.end_headers()
            return

        if self.inbound_secret:
            provided = self.headers.get("x-webhook-secret", "")
            auth = self.headers.get("authorization", "")
            bearer = auth.removeprefix("Bearer ").strip() if auth.startswith("Bearer ") else ""
            if provided != self.inbound_secret and bearer != self.inbound_secret:
                self.send_response(401)
                self.end_headers()
                return

        try:
            content_length = int(self.headers.get("content-length", "0"))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            payload = json.loads(body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("payload must be object")

            response = self.bridge_client.forward_bhmailer_webhook(
                payload=payload,
                secret=self.bridge_secret,
            )
            encoded = json.dumps(response).encode("utf-8")
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
        except Exception as error:
            LOGGER.exception("webhook proxy failed error=%s", error)
            encoded = json.dumps({"ok": False, "error": str(error)}).encode("utf-8")
            self.send_response(500)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.debug("webhook_proxy %s", format % args)


def start_webhook_proxy(config: WebhookProxyConfig, bridge_client: BridgeClient) -> threading.Thread:
    _WebhookHandler.bridge_client = bridge_client
    _WebhookHandler.bridge_secret = config.shared_secret
    _WebhookHandler.inbound_secret = config.inbound_secret
    server = ThreadingHTTPServer((config.host, config.port), _WebhookHandler)

    def _run() -> None:
        LOGGER.info("webhook proxy listening on http://%s:%s/bhmailer/webhook", config.host, config.port)
        server.serve_forever(poll_interval=0.5)

    thread = threading.Thread(target=_run, name="webhook-proxy", daemon=True)
    thread.start()
    return thread
