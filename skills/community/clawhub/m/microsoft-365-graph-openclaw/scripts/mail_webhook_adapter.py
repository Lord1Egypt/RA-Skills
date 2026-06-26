#!/usr/bin/env python3
"""HTTP adapter for Microsoft Graph mail change notifications."""
import argparse
import json
import secrets
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import parse_qs, urlparse

from utils import STATE_DIR

DEFAULT_PATH = "/graph/mail"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8789
DEFAULT_QUEUE_FILE = STATE_DIR / "mail_webhook_queue.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def enqueue_events(queue_file: Path, events: List[Dict[str, Any]]) -> int:
    if not events:
        return 0
    ensure_parent(queue_file)
    with queue_file.open("a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return len(events)


def parse_notification_events(payload: Dict[str, Any], expected_client_state: str) -> Tuple[List[Dict[str, Any]], int]:
    accepted: List[Dict[str, Any]] = []
    rejected = 0
    for item in payload.get("value", []):
        if expected_client_state and item.get("clientState") != expected_client_state:
            rejected += 1
            continue
        resource_data = item.get("resourceData") or {}
        event = {
            "receivedAt": now_iso(),
            "subscriptionId": item.get("subscriptionId"),
            "changeType": item.get("changeType"),
            "resource": item.get("resource"),
            "messageId": resource_data.get("id"),
            "tenantId": item.get("tenantId"),
            "clientState": item.get("clientState"),
        }
        if event["messageId"]:
            accepted.append(event)
        else:
            rejected += 1
    return accepted, rejected


def build_handler(path: str, expected_client_state: str, queue_file: Path):
    class GraphWebhookHandler(BaseHTTPRequestHandler):
        def _send_text(self, code: int, body: str) -> None:
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _send_json(self, code: int, body: Dict[str, Any]) -> None:
            payload = json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _validate_path(self) -> bool:
            return urlparse(self.path).path == path

        def _maybe_validation_handshake(self) -> bool:
            query = parse_qs(urlparse(self.path).query)
            token = query.get("validationToken", [None])[0]
            if token is None:
                return False
            # Graph expects the raw validation token in plain text.
            self._send_text(200, token)
            return True

        def do_GET(self) -> None:
            if not self._validate_path():
                self._send_json(404, {"error": "not_found"})
                return
            if self._maybe_validation_handshake():
                return
            self._send_json(405, {"error": "method_not_allowed"})

        def do_POST(self) -> None:
            if not self._validate_path():
                self._send_json(404, {"error": "not_found"})
                return
            if self._maybe_validation_handshake():
                return

            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_json(400, {"error": "invalid_json"})
                return

            events, rejected = parse_notification_events(payload, expected_client_state)
            accepted = enqueue_events(queue_file, events)
            self._send_json(202, {"accepted": accepted, "rejected": rejected})

        def log_message(self, fmt: str, *args: Any) -> None:
            # Keep adapter logs concise and avoid raw payload leakage.
            print(f"[mail-webhook-adapter] {self.address_string()} - {fmt % args}")

    return GraphWebhookHandler


def serve(args: argparse.Namespace) -> None:
    client_state = args.client_state or secrets.token_urlsafe(24)
    queue_file = Path(args.queue_file).expanduser().resolve()
    print("Starting Graph mail webhook adapter")
    print(f"- listen: http://{args.host}:{args.port}{args.path}")
    print(f"- queue: {queue_file}")
    print(f"- clientState: {client_state}")
    print("Use this same clientState when creating subscriptions.")
    handler = build_handler(args.path, client_state, queue_file)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down webhook adapter...")
    finally:
        server.server_close()


def generate_client_state() -> None:
    """Print a new clientState value and exit (non-blocking)."""
    value = secrets.token_urlsafe(24)
    print(f"clientState: {value}")
    print("Use this value when creating subscriptions and in --client-state for setup.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Graph mail webhook adapter server.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_serve = sub.add_parser("serve", help="Start webhook adapter HTTP server.")
    p_serve.add_argument("--host", default=DEFAULT_HOST, help="Bind host.")
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port.")
    p_serve.add_argument("--path", default=DEFAULT_PATH, help="Webhook path.")
    p_serve.add_argument("--client-state", help="Expected Graph clientState value.")
    p_serve.add_argument(
        "--queue-file",
        default=str(DEFAULT_QUEUE_FILE),
        help="Queue file path (JSONL).",
    )

    sub.add_parser("generate-client-state", help="Print a new clientState value and exit.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "serve":
        serve(args)
    elif args.command == "generate-client-state":
        generate_client_state()


if __name__ == "__main__":
    main()
