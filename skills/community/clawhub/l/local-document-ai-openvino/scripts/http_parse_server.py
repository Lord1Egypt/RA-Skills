#!/usr/bin/env python3
"""
FastAPI local service for the MinerU/OpenVINO parser.

This is the user-experience oriented service layer. It binds to 127.0.0.1 by
default, keeps the model resident, and exposes simple JSON endpoints that are
easy to call from CLIs, local UIs, desktop shells, and other agents.
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor


bootstrap_local_vendor()

from persistent_parse_server import PersistentMinerURuntime


SERVER_VERSION = "0.4.0"
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_HOST = os.environ.get("LOCAL_DOCUMENT_AI_HTTP_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LOCAL_DOCUMENT_AI_HTTP_PORT", "47274"))


def _default_log_path() -> Path:
    return BASE_DIR / "tmp" / "http_parse_server.log"


def _configure_stream(stream: Any) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8")
        except Exception:
            pass


_configure_stream(sys.stdout)
_configure_stream(sys.stderr)


def create_app(log_path: Path):
    try:
        from fastapi import FastAPI
    except Exception as exc:  # pragma: no cover - import guard for optional deps
        raise RuntimeError(
            "FastAPI is not installed. Run scripts/install_local_runtime.py or use --server-kind ipc."
        ) from exc

    app = FastAPI(
        title="Local Document AI OpenVINO",
        version=SERVER_VERSION,
        description="Local-only MinerU/OpenVINO document parsing service.",
    )
    runtime = PersistentMinerURuntime(log_path)

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"ok": True, "server": "http", "server_version": SERVER_VERSION}

    @app.get("/status")
    def status() -> dict[str, Any]:
        payload = runtime.status()
        payload.update({"server": "http", "server_version": SERVER_VERSION})
        return payload

    @app.post("/warmup")
    def warmup(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        try:
            runtime.ensure_loaded(debug=bool(payload.get("debug")))
        except Exception:
            return {"ok": False, "message": runtime.last_error, "server": "http"}
        result = runtime.status()
        result.update({"server": "http", "server_version": SERVER_VERSION})
        return result

    @app.post("/parse")
    def parse(payload: dict[str, Any]) -> dict[str, Any]:
        result = runtime.parse(payload)
        result["server"] = "http"
        result["server_version"] = SERVER_VERSION
        status = result.get("status")
        if isinstance(status, dict):
            status["server_transport"] = "http"
            status["service_version"] = SERVER_VERSION
        return result

    @app.post("/shutdown")
    def shutdown() -> dict[str, Any]:
        def _exit_later() -> None:
            os._exit(0)

        threading.Timer(0.2, _exit_later).start()
        return {"ok": True, "state": "shutting_down", "server": "http", "pid": os.getpid()}

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the local HTTP document AI service.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--log", default=str(_default_log_path()))
    return parser.parse_args()


def main() -> int:
    ns = parse_args()
    try:
        import uvicorn
    except Exception as exc:
        print(
            "uvicorn is not installed. Run scripts/install_local_runtime.py or use --server-kind ipc.",
            file=sys.stderr,
        )
        print(str(exc), file=sys.stderr)
        return 1

    app = create_app(Path(ns.log).expanduser().resolve())
    uvicorn.run(
        app,
        host=ns.host,
        port=ns.port,
        log_level=os.environ.get("LOCAL_DOCUMENT_AI_HTTP_LOG_LEVEL", "warning"),
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
