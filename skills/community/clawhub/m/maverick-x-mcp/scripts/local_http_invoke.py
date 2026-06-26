#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Start a skill-local HTTP MCP server, then invoke mcporter."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_IDLE_TIMEOUT_SECONDS = 300
DEFAULT_START_TIMEOUT_SECONDS = 30


def _sha256(value: str, length: int | None = None) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return digest if length is None else digest[:length]


@contextlib.contextmanager
def _locked_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return payload


def _first_server(config: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise RuntimeError("mcporter.json has no mcpServers entry")
    server_key = next(iter(servers))
    server = servers[server_key]
    if not isinstance(server, dict):
        raise RuntimeError(f"mcpServers.{server_key} must be an object")
    return server_key, server


def _state_dir(server_key: str, base_url: str) -> Path:
    root = (
        os.environ.get("XDG_RUNTIME_DIR")
        or os.environ.get("TMPDIR")
        or tempfile.gettempdir()
    )
    state_id = f"{server_key}-{_sha256(base_url, 8)}"
    return Path(root) / "local-http-mcp" / state_id


def _health_url(base_url: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    return urllib.parse.urlunparse(
        parsed._replace(path="/health", params="", query="", fragment="")
    )


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _read_pid(path: Path) -> int | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    try:
        return int(payload["pid"])
    except Exception:
        return None


def _write_pid(path: Path, pid: int, base_url: str) -> None:
    payload = {"pid": pid, "baseUrl": base_url, "startedAt": time.time()}
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    os.replace(tmp, path)


def _probe(url: str, timeout: float = 1.0) -> bool:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 300
    except (OSError, urllib.error.URLError, urllib.error.HTTPError):
        return False


def _terminate(pid: int, *, grace_seconds: float = 2.0) -> None:
    if not _pid_alive(pid):
        return
    with contextlib.suppress(ProcessLookupError):
        os.kill(pid, signal.SIGTERM)
    deadline = time.time() + grace_seconds
    while time.time() < deadline:
        if not _pid_alive(pid):
            return
        time.sleep(0.1)
    with contextlib.suppress(ProcessLookupError):
        os.kill(pid, signal.SIGKILL)


def _start_server(
    server_script: Path, host: str, port: int, state: Path, base_url: str
) -> int:
    log_path = state / "server.log"
    log_handle = log_path.open("ab")
    command = [
        "uv",
        "run",
        "--script",
        str(server_script),
        "--host",
        host,
        "--port",
        str(port),
    ]
    process = subprocess.Popen(
        command,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )
    _write_pid(state / "server.pid", process.pid, base_url)
    return process.pid


def _ensure_server(
    server_key: str, server: dict[str, Any], skill_dir: Path
) -> tuple[Path, int]:
    base_url = str(server.get("baseUrl") or server.get("url") or "")
    parsed = urllib.parse.urlparse(base_url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost"}
        or not parsed.port
    ):
        raise RuntimeError(
            f"{server_key} must use a fixed loopback http://host:port/mcp baseUrl"
        )

    state = _state_dir(server_key, base_url)
    state.mkdir(parents=True, exist_ok=True)
    pid_path = state / "server.pid"
    server_script = skill_dir / "scripts" / "server.py"
    if not server_script.exists():
        raise RuntimeError(f"missing local MCP server script: {server_script}")

    health = _health_url(base_url)
    pid = _read_pid(pid_path)
    if pid and _pid_alive(pid) and _probe(health):
        return state, pid
    if pid and _pid_alive(pid):
        _terminate(pid)

    pid = _start_server(server_script, parsed.hostname, parsed.port, state, base_url)
    deadline = time.time() + float(
        os.environ.get(
            "LOCAL_HTTP_MCP_START_TIMEOUT_SECONDS", DEFAULT_START_TIMEOUT_SECONDS
        )
    )
    while time.time() < deadline:
        if not _pid_alive(pid):
            raise RuntimeError(
                f"{server_key} local MCP server exited before readiness; see {state / 'server.log'}"
            )
        if _probe(health):
            return state, pid
        time.sleep(0.2)
    _terminate(pid)
    raise RuntimeError(
        f"{server_key} local MCP server did not become ready; see {state / 'server.log'}"
    )


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    with path.open("a", encoding="utf-8"):
        os.utime(path, (now, now))


def _spawn_reaper(state: Path, pid: int, timeout_seconds: int) -> None:
    if timeout_seconds <= 0:
        return
    subprocess.Popen(
        [
            sys.executable,
            __file__,
            "--reap",
            str(state),
            str(pid),
            str(timeout_seconds),
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )


def _reap(state: Path, expected_pid: int, timeout_seconds: int) -> int:
    stamp = state / "last-used"
    pid_path = state / "server.pid"
    time.sleep(max(1, timeout_seconds))
    try:
        age = time.time() - stamp.stat().st_mtime
    except FileNotFoundError:
        age = timeout_seconds + 1
    if age < timeout_seconds:
        return 0
    current_pid = _read_pid(pid_path)
    if current_pid != expected_pid:
        return 0
    if current_pid and _pid_alive(current_pid):
        _terminate(current_pid)
    with contextlib.suppress(FileNotFoundError):
        pid_path.unlink()
    return 0


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--reap", nargs=3, metavar=("STATE_DIR", "PID", "TIMEOUT"))
    args, remaining = parser.parse_known_args(argv)
    args.mcporter_args = remaining
    return args


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    if args.reap:
        state_dir, pid, timeout = args.reap
        return _reap(Path(state_dir), int(pid), int(timeout))
    if not args.mcporter_args:
        raise RuntimeError("mcporter arguments are required")

    skill_dir = Path(__file__).resolve().parents[1]
    config_path = skill_dir / "mcporter.json"
    config = _load_json(config_path)
    server_key, server = _first_server(config)
    base_url = str(server.get("baseUrl") or server.get("url") or "")
    state = _state_dir(server_key, base_url)
    lock_path = state / "start.lock"

    with _locked_file(lock_path):
        state, pid = _ensure_server(server_key, server, skill_dir)

    stamp = state / "last-used"
    _touch(stamp)
    env = os.environ.copy()
    env["MCPORTER_CONFIG"] = str(config_path)
    completed = subprocess.run(["mcporter", *args.mcporter_args], env=env, check=False)
    _touch(stamp)
    timeout = int(
        os.environ.get(
            "LOCAL_HTTP_MCP_IDLE_TIMEOUT_SECONDS", DEFAULT_IDLE_TIMEOUT_SECONDS
        )
    )
    _spawn_reaper(state, pid, timeout)
    return completed.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except RuntimeError as exc:
        print(f"local_http_invoke.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
