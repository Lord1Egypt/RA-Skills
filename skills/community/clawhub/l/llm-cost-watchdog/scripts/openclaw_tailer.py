#!/usr/bin/env python3
"""
OpenClaw session tailer.

OpenClaw writes a JSONL event log per session at
    ~/.openclaw/agents/main/sessions/<session-id>.jsonl

Every assistant-role message in that log already carries:
    - model           (e.g. "claude-haiku-4-5")
    - provider
    - usage           (input/output/cacheRead/cacheWrite/totalTokens)
    - cost            (OpenClaw's own cost estimate)

This script watches the latest session file and, for each new assistant
message, writes a row to ~/.cost-watchdog/usage.jsonl. That gives the
cost-watchdog a full picture of OpenClaw spend without any SDK wrapping.

Cost handling:
    - If OpenClaw reports a `cost` block, we use it (authoritative — OpenClaw
      charges through the same endpoint the user is billed at).
    - Otherwise we price the usage through _pricing.get_price as a fallback.

Usage:
    python3 scripts/openclaw_tailer.py                # watch loop (tail -f)
    python3 scripts/openclaw_tailer.py --once         # catch up and exit
    python3 scripts/openclaw_tailer.py --session <id> # force a specific session file
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Iterable, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage_log  # noqa: E402
import _pricing   # noqa: E402
from io_utils import write_json_atomic, read_json  # noqa: E402


OPENCLAW_SESSIONS = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
STATE_FILE = usage_log.LOG_DIR / "openclaw-tailer.state.json"


def _latest_session_file() -> Optional[Path]:
    if not OPENCLAW_SESSIONS.exists():
        return None
    candidates = [
        p for p in OPENCLAW_SESSIONS.glob("*.jsonl")
        if "deleted" not in p.name and "reset" not in p.name
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _parse_message(event: dict) -> Optional[dict]:
    """Return the nested message dict if this event is a message, else None."""
    if event.get("type") != "message":
        return None
    msg = event.get("message")
    if isinstance(msg, str):
        try:
            msg = json.loads(msg)
        except json.JSONDecodeError:
            return None
    return msg if isinstance(msg, dict) else None


def _event_to_usage(event: dict, session_id: str, source_path: Path) -> Optional[dict]:
    """
    Convert one OpenClaw event to a usage_log entry, or None to skip.
    Only assistant messages with usage data are recorded.
    """
    msg = _parse_message(event)
    if not msg or msg.get("role") != "assistant":
        return None
    usage = msg.get("usage")
    if not isinstance(usage, dict):
        return None

    model = msg.get("model")
    provider = msg.get("provider")
    input_tokens = int(usage.get("input", 0))
    output_tokens = int(usage.get("output", 0))
    cache_read = int(usage.get("cacheRead", 0))
    cache_write = int(usage.get("cacheWrite", 0))

    # Prefer OpenClaw's cost if present; else price ourselves.
    reported_cost = usage.get("cost") if isinstance(usage.get("cost"), dict) else None
    if reported_cost:
        cost_input = float(reported_cost.get("input", 0.0))
        cost_output = float(reported_cost.get("output", 0.0))
        cost_total = float(reported_cost.get("total", cost_input + cost_output))
    else:
        price = _pricing.get_price(model) if model else None
        if price and price.unit == "token":
            cost_input = (input_tokens / 1_000_000) * price.input_per_1m
            cost_output = (output_tokens / 1_000_000) * price.output_per_1m
            cost_total = cost_input + cost_output
        else:
            cost_input = cost_output = cost_total = 0.0

    return {
        "ts": _parse_ts(event.get("timestamp") or msg.get("timestamp")),
        "source": "openclaw",
        "model": model,
        "provider": provider,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read,
        "cache_write_tokens": cache_write,
        "cost_input": cost_input,
        "cost_output": cost_output,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {
            "event_id": event.get("id"),
            "stop_reason": msg.get("stopReason"),
            "file": source_path.name,
            "cost_source": "openclaw" if reported_cost else "pricing_lookup",
        },
    }


def _parse_ts(value) -> float:
    """Best-effort: accept unix float or ISO-8601 string."""
    if value is None:
        return time.time()
    if isinstance(value, (int, float)):
        return float(value)
    try:
        from datetime import datetime
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError):
        return time.time()


# ---------------------------------------------------------------------------
# State — where we left off in the current session file
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    return read_json(STATE_FILE, default={})


def _save_state(state: dict) -> None:
    write_json_atomic(STATE_FILE, state, indent=0)


def _process_from_offset(path: Path, start_offset: int) -> tuple:
    """
    Read new lines from `path` starting at byte offset `start_offset`.
    For each assistant message with usage, append to usage_log.
    Returns (new_offset, new_rows).
    """
    session_id = path.stem
    new_rows = 0
    with path.open("rb") as f:
        f.seek(start_offset)
        for raw in f:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            entry = _event_to_usage(event, session_id, path)
            if entry is not None:
                usage_log.append_usage(entry)
                new_rows += 1
        new_offset = f.tell()
    return new_offset, new_rows


def tail_once(path: Optional[Path] = None) -> int:
    path = path or _latest_session_file()
    if path is None:
        print("No OpenClaw session found.", file=sys.stderr)
        return 0

    state = _load_state()
    key = str(path)
    offset = state.get(key, {}).get("offset", 0)

    # If the file shrank (rotation / reset), restart from 0.
    if offset > path.stat().st_size:
        offset = 0

    new_offset, rows = _process_from_offset(path, offset)
    state[key] = {"offset": new_offset, "updated_at": time.time()}
    _save_state(state)
    return rows


def watch(poll_interval: float = 2.0) -> None:
    print(f"Watching OpenClaw sessions at {OPENCLAW_SESSIONS}", file=sys.stderr)
    print(f"Logging to {usage_log.USAGE_LOG}", file=sys.stderr)
    last_path = None
    while True:
        path = _latest_session_file()
        if path and path != last_path:
            print(f"Active session: {path.name}", file=sys.stderr)
            last_path = path
        if path:
            rows = tail_once(path)
            if rows:
                print(f"  logged {rows} new assistant turn(s)", file=sys.stderr)
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Tail OpenClaw session logs into usage.jsonl")
    p.add_argument("--once", action="store_true", help="Process new events and exit")
    p.add_argument("--session", help="Force a specific session filename or absolute path")
    p.add_argument("--reset", action="store_true", help="Forget saved offsets and start over")
    p.add_argument("--interval", type=float, default=2.0, help="Watch poll interval (seconds)")
    args = p.parse_args()

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("Tailer state reset.", file=sys.stderr)

    target = None
    if args.session:
        cand = Path(args.session)
        if not cand.is_absolute():
            cand = OPENCLAW_SESSIONS / cand
        if not cand.exists():
            print(f"No such session file: {cand}", file=sys.stderr)
            return 1
        target = cand

    if args.once:
        rows = tail_once(target)
        print(f"Logged {rows} new row(s).", file=sys.stderr)
        return 0

    try:
        watch(poll_interval=args.interval)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
