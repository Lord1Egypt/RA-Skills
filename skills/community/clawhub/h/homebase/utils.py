"""
Shared utilities for Homebase.
"""
import json
import os
import re
import tempfile
import time as _time
from typing import Any


# ─── Atomic JSON writes ─────────────────────────────────────────────────────
#
# Every state file write goes through this. Reason: a naked
# ``open(path, "w") + json.dump`` will leave a truncated/empty file behind if
# the process is killed mid-write (cron timeout, OOM, sigkill, disk full).
# The next run then crashes on JSONDecodeError. For a skill that runs
# unattended for weeks, that single failure mode is the difference between
# "self-heals" and "wakes you up Saturday morning".
#
# How to apply: replace
#     with open(path, "w") as f:
#         json.dump(data, f, indent=2)
# with
#     write_json_atomic(path, data)

def write_json_atomic(path: str, data: Any, indent: int = 2) -> None:
    """Write JSON to ``path`` atomically: tempfile in same dir → fsync → rename."""
    dir_path = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp.", suffix=".json", dir=dir_path)
    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(data, tmp, indent=indent, default=str)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

# Note: All LLM interactions have been removed from this skill.
# Python tools must return raw or structured data to the OpenClaw agent,
# which uses whichever model OpenClaw is configured with to reason about the data.


# ─── Retry helper ───────────────────────────────────────────────────────────

def retry_with_backoff(fn, retries: int = 3, delays: tuple = (1, 2, 4)):
    """
    Retry a function call up to `retries` times with specified delays between attempts.
    No delay before first attempt. Raises the last exception if all retries fail.

    Usage:
        response = retry_with_backoff(lambda: fn(...), retries=3, delays=(1, 2, 4))
    """
    last_error = None
    for attempt in range(retries):
        if attempt > 0:
            delay = delays[attempt - 1] if attempt - 1 < len(delays) else delays[-1]
            import time
            time.sleep(delay)
        try:
            return fn()
        except Exception as e:
            last_error = e
    raise last_error


# ─── Think tag cleaner ──────────────────────────────────────────────────────

def clean_think_tags(text: str) -> str:
    """
    Remove <think>...</think> tags and their content from a string.
    Also handles some variations like *thought* tags.
    Returns cleaned text with surrounding whitespace stripped.
    """
    cleaned = re.sub(r'<think>[^*]*\*\/?[^>]*\*\/?>', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'<think>[\s\S]*?</think>', '', cleaned)
    return cleaned.strip()
