#!/usr/bin/env python3
"""HermesClawZero Memory CLI — capture, search & autosave via Sidecar API.

Usage:
    python memory.py capture "<text>" [scope_id] [--success-flag]
    python memory.py search "<query>" [limit=5]
    python memory.py autosave "<text>" [filename] [--success-flag]

The --success-flag option makes commands output a clean "MEMORY_SAVED=ok"
line that agents can parse as a deterministic success signal.
"""
import json
import logging
import os
import sys
from typing import Any

import requests

logger = logging.getLogger("hermes_cli")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_dotenv(path: str) -> dict[str, str]:
    """Minimal .env parser — no external dependencies needed."""
    env: dict[str, str] = {}
    if not os.path.isfile(path):
        return env
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip("\"'")
    except OSError as exc:
        logger.warning("Cannot read %s: %s", path, exc)
    return env


def _resolve_config() -> tuple[str, str]:
    """Resolve API base URL and key from env vars or .env files."""
    env_vars = {**os.environ}
    env_script = _load_dotenv(os.path.join(SCRIPT_DIR, ".env"))
    env_cwd = _load_dotenv(os.path.join(os.getcwd(), ".env"))

    api_base = (
        env_vars.get("MEM_PUBLIC_URL")
        or env_script.get("MEM_PUBLIC_URL")
        or env_cwd.get("MEM_PUBLIC_URL", "http://localhost:8010")
    )
    api_key = (
        env_vars.get("API_KEY")
        or env_script.get("API_KEY")
        or env_cwd.get("API_KEY")
        or ""
    )
    if not api_key:
        logger.warning("API_KEY not found in environment or .env files")
    return api_base.rstrip("/"), api_key


API_BASE, API_KEY = _resolve_config()


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------
class SidecarError(Exception):
    """Raised when the Sidecar API returns a non-2xx status."""

    def __init__(self, status: int, detail: str) -> None:
        self.status = status
        self.detail = detail
        super().__init__(f"API {status}: {detail}")


def _api_call(method: str, path: str, **kwargs: Any) -> Any:
    """Make an authenticated request to the HermesClawZero Sidecar API."""
    url = f"{API_BASE}{path}"
    headers = dict(kwargs.pop("headers", {}))
    headers.setdefault("X-API-Key", API_KEY)
    kwargs["headers"] = headers
    logger.debug("%s %s", method.upper(), url)
    try:
        r = requests.request(method, url, timeout=15, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError as exc:
        raise SidecarError(0, f"Cannot connect to {API_BASE}: {exc}") from exc
    except requests.exceptions.Timeout as exc:
        raise SidecarError(0, f"Request timed out: {exc}") from exc
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 0
        try:
            detail = exc.response.json() if exc.response is not None else str(exc)
        except (json.JSONDecodeError, AttributeError):
            detail = exc.response.text[:500] if exc.response is not None else str(exc)
        raise SidecarError(status, detail) from exc


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def capture(text: str, scope_id: str | None = None) -> dict[str, Any]:
    """Persist a memory to the global chat namespace (always searchable)."""
    if not text or not text.strip():
        raise ValueError("capture text must be non-empty")
    body: dict[str, Any] = {"text": text.strip()}
    if scope_id:
        body["scope_id"] = scope_id.strip()[:200]
    return _api_call("POST", "/capture", json=body)


def search(query: str, limit: int = 5, rerank: bool = False) -> list[dict[str, Any]]:
    """Retrieve relevant memories from the global chat."""
    result = _api_call(
        "GET", "/search",
        params={"query": query, "limit": max(1, min(100, limit)),
                "rerank_results": str(rerank).lower()},
    )
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        return [result]
    return []


def autosave(text: str, filename: str | None = None) -> dict[str, Any]:
    """Store longer text as a single capture, optionally tagged with a scope."""
    if not text or not text.strip():
        raise ValueError("autosave text must be non-empty")
    body: dict[str, Any] = {"text": text.strip()}
    if filename:
        body["scope_id"] = f"autosave:{filename.strip()}"
    return _api_call("POST", "/capture", json=body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _show_result(data: Any, success_flag: bool = False) -> None:
    """Pretty-print API result to stdout.

    When success_flag is True, emits a deterministic MEMORY_SAVED=
    line that agents can parse as a reliable success signal.
    """
    if success_flag:
        # Emit a machine-parseable success signal first
        print("MEMORY_SAVED=ok")

    if isinstance(data, list):
        for item in data:
            content = item.get("content") or item.get("page_content") or ""
            if content:
                print(content)
            else:
                print(json.dumps(item, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False, default=str))


def _has_flag(flag: str) -> bool:
    """Check if a flag exists in sys.argv and remove it if found."""
    for i, arg in enumerate(sys.argv[:]):
        if arg == flag:
            sys.argv.pop(i)
            return True
    return False


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    success_flag = _has_flag("--success-flag")

    try:
        if cmd == "capture":
            if len(sys.argv) < 3:
                print('Usage: memory.py capture "<text>" [scope_id] [--success-flag]', file=sys.stderr)
                sys.exit(1)
            r = capture(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
            _show_result(r, success_flag)

        elif cmd == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
            r = search(query, limit)
            _show_result(r, success_flag)

        elif cmd == "autosave":
            if len(sys.argv) < 3:
                print('Usage: memory.py autosave "<text>" [filename] [--success-flag]', file=sys.stderr)
                sys.exit(1)
            r = autosave(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
            _show_result(r, success_flag)

        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            print(__doc__.strip(), file=sys.stderr)
            sys.exit(1)

    except SidecarError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
