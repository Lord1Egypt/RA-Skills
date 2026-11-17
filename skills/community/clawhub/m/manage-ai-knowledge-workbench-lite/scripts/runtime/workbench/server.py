"""Read-only loopback dashboard server."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import signal
import threading
from typing import Any
import uuid
import webbrowser

from .config import STATE_NAME, atomic_write_json, load_json, normalized, now_iso
from .result import make_result


LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def create_server(*, dashboard: Path, host: str, port: int, instance_id: str) -> ThreadingHTTPServer:
    if host not in LOOPBACK_HOSTS:
        raise ValueError("Dashboard server must bind to a loopback host.")
    dashboard = normalized(dashboard)
    route_map = {
        "/": (dashboard / "index.html", "text/html; charset=utf-8"),
        "/index.html": (dashboard / "index.html", "text/html; charset=utf-8"),
        "/assets/styles.css": (dashboard / "assets" / "styles.css", "text/css; charset=utf-8"),
        "/assets/app.js": (dashboard / "assets" / "app.js", "text/javascript; charset=utf-8"),
        "/api/data": (dashboard / "data.json", "application/json; charset=utf-8"),
    }

    class Handler(BaseHTTPRequestHandler):
        def _headers(self, status: int, content_type: str, length: int) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                "connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'",
            )
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802 - stdlib handler contract
            path = self.path.split("?", 1)[0]
            if path == "/healthz":
                payload = json.dumps(
                    {
                        "status": "ok",
                        "read_only": True,
                        "instance_id": instance_id,
                        "generated_at": now_iso(),
                    }
                ).encode("utf-8")
                self._headers(200, "application/json; charset=utf-8", len(payload))
                self.wfile.write(payload)
                return
            target = route_map.get(path)
            if not target or not target[0].is_file():
                payload = b"Not Found"
                self._headers(404, "text/plain; charset=utf-8", len(payload))
                self.wfile.write(payload)
                return
            payload = target[0].read_bytes()
            self._headers(200, target[1], len(payload))
            self.wfile.write(payload)

        def do_POST(self) -> None:  # noqa: N802 - stdlib handler contract
            payload = b"Method Not Allowed"
            self._headers(405, "text/plain; charset=utf-8", len(payload))
            self.wfile.write(payload)

        def log_message(self, _format: str, *_args: Any) -> None:
            return

    return ThreadingHTTPServer((host, port), Handler)


def _write_service_state(config: dict[str, Any], service: dict[str, Any]) -> Path:
    state_path = normalized(config["paths"]["internal"]) / STATE_NAME
    state = load_json(state_path)
    state["updated_at"] = now_iso()
    state["service"] = service
    atomic_write_json(state_path, state)
    return state_path


def serve(
    *,
    config: dict[str, Any],
    host: str | None,
    port: int | None,
    open_browser: bool,
    duration: float | None,
) -> tuple[dict[str, Any], int]:
    dashboard = normalized(config["paths"]["dashboard"])
    if not (dashboard / "index.html").is_file() or not (dashboard / "data.json").is_file():
        return make_result(
            status="not_ready",
            code="DASHBOARD_NOT_RENDERED",
            message="Render the dashboard before starting the server.",
            next_actions=[{"action": "render", "command": "render"}],
        ), 1
    selected_host = host or str(config["server"]["host"])
    selected_port = int(port if port is not None else config["server"]["port"])
    instance_id = str(uuid.uuid4())
    try:
        server = create_server(
            dashboard=dashboard,
            host=selected_host,
            port=selected_port,
            instance_id=instance_id,
        )
    except (OSError, ValueError) as exc:
        return make_result(
            status="error",
            code="SERVER_START_FAILED",
            message=str(exc),
        ), 1
    actual_port = int(server.server_address[1])
    service = {
        "status": "running",
        "pid": __import__("os").getpid(),
        "instance_id": instance_id,
        "host": selected_host,
        "port": actual_port,
        "read_only": True,
        "started_at": now_iso(),
    }
    state_path = _write_service_state(config, service)
    url = f"http://{selected_host}:{actual_port}/"

    old_handlers: dict[int, Any] = {}

    def request_shutdown(_signum: int, _frame: Any) -> None:
        threading.Thread(target=server.shutdown, daemon=True).start()

    for signal_name in (signal.SIGINT, signal.SIGTERM):
        try:
            old_handlers[signal_name] = signal.signal(signal_name, request_shutdown)
        except (OSError, ValueError):
            pass
    if duration is not None:
        threading.Timer(max(0.05, duration), server.shutdown).start()
    if open_browser:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.1)
    finally:
        server.server_close()
        stopped = {**service, "status": "stopped", "stopped_at": now_iso()}
        _write_service_state(config, stopped)
        for signal_name, old_handler in old_handlers.items():
            try:
                signal.signal(signal_name, old_handler)
            except (OSError, ValueError):
                pass
    return make_result(
        status="ok",
        code="SERVER_STOPPED",
        message="The read-only loopback dashboard server stopped cleanly.",
        artifacts=[str(dashboard / "index.html"), str(state_path)],
        data={"url": url, "instance_id": instance_id, "read_only": True},
    ), 0
