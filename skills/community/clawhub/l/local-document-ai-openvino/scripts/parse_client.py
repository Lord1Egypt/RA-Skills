#!/usr/bin/env python3
"""
Short-lived client for persistent_parse_server.py.

This preserves the parse_document.py CLI contract while routing heavy MinerU
inference through a local resident process.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from multiprocessing.connection import Client
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor


bootstrap_local_vendor()

AUTHKEY = b"local-document-ai-openvino"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = int(os.environ.get("LOCAL_DOCUMENT_AI_SERVER_PORT", "47273"))
SERVER_ADDRESS: tuple[str, int] = (SERVER_HOST, SERVER_PORT)
HTTP_HOST = os.environ.get("LOCAL_DOCUMENT_AI_HTTP_HOST", "127.0.0.1")
HTTP_PORT = int(os.environ.get("LOCAL_DOCUMENT_AI_HTTP_PORT", "47274"))
HTTP_BASE_URL = f"http://{HTTP_HOST}:{HTTP_PORT}"
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
SERVER_SCRIPT = SCRIPTS_DIR / "persistent_parse_server.py"
HTTP_SERVER_SCRIPT = SCRIPTS_DIR / "http_parse_server.py"
DEFAULT_CONNECT_TIMEOUT = 300.0
HTTP_BOOT_TIMEOUT = 15.0
POLL_INTERVAL = 0.3


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


def _default_http_log_path() -> Path:
    return BASE_DIR / "tmp" / "http_parse_server.log"


def _try_connect():
    try:
        return Client(SERVER_ADDRESS, authkey=AUTHKEY)
    except (FileNotFoundError, ConnectionRefusedError, OSError, EOFError):
        return None


def _pythonw_executable() -> str:
    if os.name != "nt":
        return sys.executable
    python_exe = Path(sys.executable)
    pythonw = python_exe.with_name("pythonw.exe")
    return str(pythonw if pythonw.exists() else python_exe)


def _hidden_startupinfo():
    if os.name != "nt" or not hasattr(subprocess, "STARTUPINFO"):
        return None
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= getattr(subprocess, "STARTF_USESHOWWINDOW", 0)
    startupinfo.wShowWindow = getattr(subprocess, "SW_HIDE", 0)
    return startupinfo


def _spawn_server(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    subprocess.Popen(
        [_pythonw_executable(), str(SERVER_SCRIPT), "--log", str(log_path)],
        cwd=str(BASE_DIR),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        startupinfo=_hidden_startupinfo(),
        creationflags=creationflags,
    )


def _spawn_http_server(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    subprocess.Popen(
        [
            _pythonw_executable(),
            str(HTTP_SERVER_SCRIPT),
            "--host",
            HTTP_HOST,
            "--port",
            str(HTTP_PORT),
            "--log",
            str(log_path),
        ],
        cwd=str(BASE_DIR),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        startupinfo=_hidden_startupinfo(),
        creationflags=creationflags,
    )


def _ensure_server(log_path: Path, timeout_s: float = DEFAULT_CONNECT_TIMEOUT):
    conn = _try_connect()
    if conn is not None:
        return conn

    _spawn_server(log_path)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        conn = _try_connect()
        if conn is not None:
            return conn
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"Timed out waiting for persistent parse server at {SERVER_ADDRESS!r}")


def _http_json(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    timeout_s: float = DEFAULT_CONNECT_TIMEOUT,
) -> dict[str, Any]:
    url = f"{HTTP_BASE_URL}{path}"
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        text = resp.read().decode("utf-8")
    return json.loads(text) if text.strip() else {"ok": True}


def _try_http_health(timeout_s: float = 1.0) -> bool:
    try:
        result = _http_json("GET", "/health", timeout_s=timeout_s)
    except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False
    return bool(result.get("ok"))


def _ensure_http_server(timeout_s: float = HTTP_BOOT_TIMEOUT) -> None:
    if _try_http_health():
        return
    _spawn_http_server(_default_http_log_path())
    deadline = time.time() + min(timeout_s, HTTP_BOOT_TIMEOUT)
    while time.time() < deadline:
        if _try_http_health():
            return
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"Timed out waiting for HTTP parse server at {HTTP_BASE_URL}")


def _request_ipc(
    op: str,
    payload: dict[str, Any] | None = None,
    start: bool = True,
    timeout_s: float = DEFAULT_CONNECT_TIMEOUT,
) -> dict[str, Any]:
    conn = _ensure_server(_default_log_path(), timeout_s=timeout_s) if start else _try_connect()
    if conn is None:
        return {"ok": False, "message": "persistent parse server is not running"}
    try:
        conn.send({"op": op, "payload": payload or {}})
        response = conn.recv()
    finally:
        conn.close()
    return response if isinstance(response, dict) else {"ok": False, "message": "invalid server response"}


def _request_http(
    op: str,
    payload: dict[str, Any] | None = None,
    start: bool = True,
    timeout_s: float = DEFAULT_CONNECT_TIMEOUT,
) -> dict[str, Any]:
    if start:
        _ensure_http_server(timeout_s=timeout_s)
    elif not _try_http_health():
        return {"ok": False, "message": "HTTP parse server is not running"}

    if op == "status":
        return _http_json("GET", "/status", timeout_s=timeout_s)
    if op == "warmup":
        return _http_json("POST", "/warmup", payload or {}, timeout_s=timeout_s)
    if op == "parse":
        return _http_json("POST", "/parse", payload or {}, timeout_s=timeout_s)
    if op == "shutdown":
        return _http_json("POST", "/shutdown", {}, timeout_s=timeout_s)
    return {"ok": False, "message": f"unsupported op: {op}"}


def _request(
    op: str,
    payload: dict[str, Any] | None = None,
    start: bool = True,
    timeout_s: float = DEFAULT_CONNECT_TIMEOUT,
    server_kind: str = "auto",
) -> dict[str, Any]:
    if server_kind == "http":
        return _request_http(op, payload=payload, start=start, timeout_s=timeout_s)
    if server_kind == "ipc":
        return _request_ipc(op, payload=payload, start=start, timeout_s=timeout_s)

    http_error = None
    try:
        response = _request_http(op, payload=payload, start=start, timeout_s=timeout_s)
        if response.get("ok"):
            response.setdefault("server_kind", "http")
            return response
        http_error = response.get("message")
    except Exception as exc:
        http_error = str(exc)

    try:
        response = _request_ipc(op, payload=payload, start=start, timeout_s=timeout_s)
        response.setdefault("server_kind", "ipc")
        if http_error and response.get("ok"):
            response.setdefault("http_fallback_reason", http_error)
        return response
    except Exception as exc:
        return {
            "ok": False,
            "message": f"auto server failed; http={http_error}; ipc={exc}",
            "server_kind": "auto",
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse through the persistent local document AI server.")
    parser.add_argument("--file", help="Input PDF or image path")
    parser.add_argument("--out", help="Output artifact directory")
    parser.add_argument("--mode", default="parse", choices=["parse", "to-code", "to-data"])
    parser.add_argument("--engine-version", default="mineru2.5-openvino-persistent")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--language-hint")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--status", action="store_true", help="Print server status and exit")
    parser.add_argument("--warmup", action="store_true", help="Start the server and load the MinerU/OpenVINO runtime")
    parser.add_argument("--shutdown", action="store_true", help="Ask the server to shut down and exit")
    parser.add_argument("--no-start", action="store_true", help="Do not auto-start the server for status requests")
    parser.add_argument("--connect-timeout", type=float, default=DEFAULT_CONNECT_TIMEOUT)
    parser.add_argument(
        "--server-kind",
        choices=["auto", "http", "ipc"],
        default=os.environ.get("LOCAL_DOCUMENT_AI_SERVER_KIND", "auto"),
        help="Server transport to use. auto prefers HTTP and falls back to the stdlib IPC server.",
    )
    return parser.parse_args()


def main() -> int:
    ns = parse_args()
    try:
        if ns.status:
            response = _request(
                "status",
                start=not ns.no_start,
                timeout_s=ns.connect_timeout,
                server_kind=ns.server_kind,
            )
            print(json.dumps(response, ensure_ascii=False))
            return 0 if response.get("ok") else 2
        if ns.warmup:
            response = _request(
                "warmup",
                payload={"debug": ns.debug},
                start=True,
                timeout_s=ns.connect_timeout,
                server_kind=ns.server_kind,
            )
            print(json.dumps(response, ensure_ascii=False))
            return 0 if response.get("ok") else 2
        if ns.shutdown:
            response = _request(
                "shutdown",
                start=False,
                timeout_s=ns.connect_timeout,
                server_kind=ns.server_kind,
            )
            print(json.dumps(response, ensure_ascii=False))
            return 0 if response.get("ok") else 2
        if not ns.file or not ns.out:
            raise ValueError("--file and --out are required unless --status or --shutdown is used")

        response = _request(
            "parse",
            payload={
                "file": str(Path(ns.file).expanduser().resolve()),
                "out": str(Path(ns.out).expanduser().resolve()),
                "mode": ns.mode,
                "engine_version": ns.engine_version,
                "max_pages": ns.max_pages,
                "language_hint": ns.language_hint,
                "debug": ns.debug,
            },
            start=True,
            timeout_s=ns.connect_timeout,
            server_kind=ns.server_kind,
        )
        if not response.get("ok"):
            print(json.dumps(response, ensure_ascii=False), file=sys.stderr)
            return 1
        status = response.get("status")
        if isinstance(status, dict):
            if response.get("server"):
                status.setdefault("server_transport", response.get("server"))
            if response.get("server_version"):
                status.setdefault("service_version", response.get("server_version"))
            if response.get("server_kind"):
                status.setdefault("server_kind", response.get("server_kind"))
        print(json.dumps(status or response, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "stage": "parse_client", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
