"""
Swallowed-error log. Any time tracker / http_capture / tailer catches an
exception it can't meaningfully handle (but mustn't let bubble up, because
that would break the user's LLM call), the detail goes here.

Format: JSON Lines at ~/.cost-watchdog/errors.jsonl.

Use `errors` on the CLI to surface recent entries — this is how silent
failures become visible.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import List, Optional, Union

LOG_DIR = Path(os.environ.get("CW_LOG_DIR", Path.home() / ".cost-watchdog"))
LOG_DIR.mkdir(parents=True, exist_ok=True)
ERRORS_LOG = LOG_DIR / "errors.jsonl"

MAX_LINES = 5000


def log_error(component: str,
              error: Union[str, BaseException],
              *,
              hint: Optional[str] = None,
              extra: Optional[dict] = None) -> None:
    """Append one error entry. Never raises."""
    try:
        if isinstance(error, BaseException):
            detail = "".join(traceback.format_exception_only(type(error), error)).strip()
            tb = "".join(traceback.format_tb(error.__traceback__))
        else:
            detail = str(error)
            tb = ""
        entry = {
            "ts": time.time(),
            "component": component,
            "error": detail,
            "traceback": tb,
            "hint": hint or "",
            "extra": extra or {},
        }
        line = json.dumps(entry, separators=(",", ":")) + "\n"
        with ERRORS_LOG.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        # Logging errors must never raise.
        pass
    else:
        _trim_if_huge()


def _trim_if_huge() -> None:
    """Keep only the last MAX_LINES entries. Cheap for a log that rarely grows."""
    try:
        if not ERRORS_LOG.exists():
            return
        # Only trim every ~100 writes.
        if int(time.time()) % 100 != 0:
            return
        lines = ERRORS_LOG.read_text(encoding="utf-8").splitlines()
        if len(lines) <= MAX_LINES:
            return
        keep = lines[-MAX_LINES:]
        # Atomic rewrite via io_utils would be nice but we already have
        # a self-contained fallback.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        try:
            from io_utils import write_json_atomic  # noqa: F401
            ERRORS_LOG.write_text("\n".join(keep) + "\n", encoding="utf-8")
        except ImportError:
            ERRORS_LOG.write_text("\n".join(keep) + "\n", encoding="utf-8")
    except Exception:
        pass


def read_recent(limit: int = 50) -> List[dict]:
    if not ERRORS_LOG.exists():
        return []
    try:
        lines = ERRORS_LOG.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(out) >= limit:
            break
    return out


def count_since(since: Optional[float] = None) -> int:
    if not ERRORS_LOG.exists():
        return 0
    n = 0
    try:
        with ERRORS_LOG.open(encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if since is None or entry.get("ts", 0) >= since:
                    n += 1
    except OSError:
        pass
    return n


def clear() -> None:
    if ERRORS_LOG.exists():
        ERRORS_LOG.unlink()
