#!/usr/bin/env python3
"""
Persistent MinerU/OpenVINO parse server.

The server keeps the OpenVINO GenAI MinerU pipeline resident across agent
invocations. The short-lived parse_client.py talks to it over a local IPC
channel, so repeated document parses avoid recompiling and reloading the model.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import traceback
from multiprocessing.connection import Listener
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor


bootstrap_local_vendor()

from parse_document import ParseConfig, find_mineru_model_dir, run_parse_pipeline


SERVER_VERSION = "0.3.0"
AUTHKEY = b"local-document-ai-openvino"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = int(os.environ.get("LOCAL_DOCUMENT_AI_SERVER_PORT", "47273"))
STATE_IDLE = "idle"
STATE_LOADING = "loading"
STATE_RUNNING = "running"
STATE_ERROR = "error"

SERVER_ADDRESS: tuple[str, int] = (SERVER_HOST, SERVER_PORT)

BASE_DIR = Path(__file__).resolve().parent.parent


def _configure_stream(stream: Any) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8")
        except Exception:
            pass


_configure_stream(sys.stdout)
_configure_stream(sys.stderr)


def _default_log_path() -> Path:
    return BASE_DIR / "tmp" / "persistent_parse_server.log"


def _log(log_path: Path, message: str) -> None:
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with log_path.open("a", encoding="utf-8") as stream:
            stream.write(f"[{timestamp}] [pid={os.getpid()}] {message}\n")
    except OSError:
        pass


class PersistentMinerURuntime:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.lock = threading.Lock()
        self.state = STATE_IDLE
        self.last_error = ""
        self.client: Any | None = None
        self.model_dir: Path | None = None
        self.device = os.environ.get("MINERU_OPENVINO_DEVICE", "CPU")
        self.image_analysis = os.environ.get("MINERU_OPENVINO_IMAGE_ANALYSIS", "0") == "1"
        self.loaded_at: float | None = None
        self.load_time_s: float | None = None
        self.request_count = 0

    def status(self) -> dict[str, Any]:
        return {
            "ok": True,
            "server_version": SERVER_VERSION,
            "pid": os.getpid(),
            "state": self.state,
            "loaded": self.client is not None,
            "model_dir": str(self.model_dir) if self.model_dir else None,
            "device": self.device,
            "image_analysis": self.image_analysis,
            "loaded_at": self.loaded_at,
            "load_time_s": self.load_time_s,
            "request_count": self.request_count,
            "last_error": self.last_error,
        }

    def ensure_loaded(self, debug: bool = False) -> tuple[Any, Path]:
        with self.lock:
            if self.client is not None and self.model_dir is not None:
                return self.client, self.model_dir

            self.state = STATE_LOADING
            self.last_error = ""
            t0 = time.time()
            _log(self.log_path, "loading MinerU OpenVINO runtime")
            try:
                model_dir = find_mineru_model_dir(BASE_DIR)
                if model_dir is None:
                    raise FileNotFoundError(
                        "MinerU OpenVINO model assets were not found. Set MINERU_OPENVINO_MODEL_DIR "
                        "or place the bundle under the skill models/ directory."
                    )
                from mineru_openvino_backend import OVMinerUClient

                client = OVMinerUClient(
                    model_dir=model_dir,
                    device=self.device,
                    image_analysis=self.image_analysis,
                    debug=debug,
                )
                self.client = client
                self.model_dir = model_dir
                self.loaded_at = time.time()
                self.load_time_s = round(self.loaded_at - t0, 3)
                self.state = STATE_IDLE
                _log(self.log_path, f"runtime loaded in {self.load_time_s}s from {model_dir}")
                return client, model_dir
            except Exception:
                self.state = STATE_ERROR
                self.last_error = traceback.format_exc()
                _log(self.log_path, f"runtime load failed:\n{self.last_error}")
                raise

    def parse(self, payload: dict[str, Any]) -> dict[str, Any]:
        client, model_dir = self.ensure_loaded(debug=bool(payload.get("debug")))
        config = ParseConfig(
            file=Path(str(payload["file"])).expanduser().resolve(),
            out=Path(str(payload["out"])).expanduser().resolve(),
            mode=str(payload.get("mode") or "parse"),
            engine_version=str(payload.get("engine_version") or "mineru2.5-openvino-persistent"),
            max_pages=payload.get("max_pages"),
            language_hint=payload.get("language_hint"),
            debug=bool(payload.get("debug")),
        )
        with self.lock:
            self.state = STATE_RUNNING
        t0 = time.time()
        try:
            status = run_parse_pipeline(config, mineru_client=client, model_dir=model_dir)
            self.request_count += 1
            status.update(
                {
                    "persistent_server": True,
                    "server_pid": os.getpid(),
                    "server_parse_time_s": round(time.time() - t0, 3),
                    "server_status": self.status(),
                }
            )
            return {"ok": True, "status": status}
        except Exception:
            self.last_error = traceback.format_exc()
            _log(self.log_path, f"parse failed:\n{self.last_error}")
            return {"ok": False, "message": self.last_error}
        finally:
            with self.lock:
                self.state = STATE_IDLE if self.client is not None else STATE_ERROR


class ParseServer:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.runtime = PersistentMinerURuntime(log_path)
        self.shutdown = False

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        op = request.get("op")
        if op == "status":
            return self.runtime.status()
        if op == "shutdown":
            self.shutdown = True
            return {"ok": True, "state": "shutting_down", "pid": os.getpid()}
        if op == "warmup":
            try:
                self.runtime.ensure_loaded(debug=bool(request.get("debug")))
            except Exception:
                return {"ok": False, "message": self.runtime.last_error}
            return self.runtime.status()
        if op == "parse":
            payload = request.get("payload") or {}
            if not isinstance(payload, dict):
                return {"ok": False, "message": "parse payload must be an object"}
            if not payload.get("file") or not payload.get("out"):
                return {"ok": False, "message": "parse payload requires file and out"}
            return self.runtime.parse(payload)
        return {"ok": False, "message": f"unsupported op: {op}"}

    def serve_forever(self) -> int:
        _log(self.log_path, f"server starting on {SERVER_ADDRESS!r}")
        with Listener(SERVER_ADDRESS, authkey=AUTHKEY) as listener:
            _log(self.log_path, "server ready")
            while not self.shutdown:
                conn = listener.accept()
                try:
                    request = conn.recv()
                    response = self.handle(request if isinstance(request, dict) else {})
                    conn.send(response)
                except Exception:
                    error = traceback.format_exc()
                    _log(self.log_path, f"request handling failed:\n{error}")
                    try:
                        conn.send({"ok": False, "message": error})
                    except Exception:
                        pass
                finally:
                    conn.close()
        _log(self.log_path, "server stopped")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the persistent local document AI parse server.")
    parser.add_argument("--log", default=str(_default_log_path()), help="Server log path")
    return parser.parse_args()


def main() -> int:
    ns = parse_args()
    log_path = Path(ns.log).expanduser().resolve()
    server = ParseServer(log_path)
    return server.serve_forever()


if __name__ == "__main__":
    raise SystemExit(main())
