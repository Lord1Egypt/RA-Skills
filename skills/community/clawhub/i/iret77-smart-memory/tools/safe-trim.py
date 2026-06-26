#!/usr/bin/env python3
"""
safe-trim.py — Trim an OpenClaw session file without cutting mid-tool-call.

Usage:
  python3 safe-trim.py <session_file> [--keep 60]
  python3 safe-trim.py --check <session_file>   # Check if session is in broken state

A "broken state" is when the session ends with an incomplete tool exchange:
  - Last message is a toolResult with no following assistant turn, OR
  - Last assistant message contains only toolCall blocks (no completion yet)

Safe to repair only if the file hasn't been modified in > 5 minutes
(otherwise a tool-call might still be running).
"""

import json
import sys
import shutil
import os
import time
from pathlib import Path


def is_broken(lines: list[str]) -> bool:
    """Return True if the session ends in an incomplete tool-call state."""
    last_roles = []
    last_types = []
    for line in reversed(lines[-10:]):
        try:
            entry = json.loads(line)
            msg = entry.get("message", {})
            role = msg.get("role", "")
            if not role:
                continue
            content = msg.get("content", [])
            types = [c.get("type") for c in content if isinstance(c, dict)]
            last_roles.append(role)
            last_types.append(types)
            if len(last_roles) >= 3:
                break
        except Exception:
            continue

    if not last_roles:
        return False

    last_role = last_roles[0]
    last_type_set = set(last_types[0]) if last_types else set()

    # Broken: ends with toolResult (no following assistant turn)
    if last_role == "toolResult":
        return True

    # Broken: ends with assistant turn that only has toolCall (no text completion)
    if last_role == "assistant" and last_type_set == {"toolCall"}:
        return True

    return False


def is_stale(session_file: str, min_age_seconds: int = 300) -> bool:
    """Return True if the file hasn't been modified in > min_age_seconds."""
    mtime = os.path.getmtime(session_file)
    age = time.time() - mtime
    return age > min_age_seconds


def safe_trim(session_file: str, keep_lines: int = 60) -> None:
    path = Path(session_file)
    if not path.exists():
        print(f"ERROR: {session_file} not found", file=sys.stderr)
        sys.exit(1)

    lines = path.read_text().splitlines(keepends=True)

    if len(lines) <= keep_lines:
        print(f"OK: {len(lines)} lines — nothing to trim")
        return

    # Backup
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)

    # Find safe cutpoints: assistant turns with no pending toolCall
    candidates = []
    for i, line in enumerate(lines):
        try:
            entry = json.loads(line)
            msg = entry.get("message", {})
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content", [])
            has_tool_call = any(
                isinstance(c, dict) and c.get("type") == "toolCall"
                for c in content
            )
            if not has_tool_call:
                candidates.append(i)
        except Exception:
            continue

    # Pick the last candidate that still leaves >= keep_lines lines after it
    cutpoint = None
    for i in reversed(candidates):
        if len(lines) - i >= keep_lines:
            cutpoint = i
            break

    if cutpoint is None:
        cutpoint = max(0, len(lines) - keep_lines)
        print(f"WARN: no safe cutpoint found, hard cut at line {cutpoint}")
    else:
        print(f"OK: safe cut at line {cutpoint} (assistant turn, no pending tool calls)")

    trimmed = lines[cutpoint:]
    path.write_text("".join(trimmed))
    print(f"Trimmed: {len(lines)} → {len(trimmed)} lines. Backup: {backup.name}")


def check_broken(session_file: str) -> None:
    """Check if session is in broken state and safe to repair."""
    path = Path(session_file)
    if not path.exists():
        print(f"ERROR: {session_file} not found", file=sys.stderr)
        sys.exit(1)

    lines = path.read_text().splitlines(keepends=True)
    broken = is_broken(lines)
    stale = is_stale(session_file, min_age_seconds=300)
    age_s = int(time.time() - os.path.getmtime(session_file))

    print(f"broken={broken} stale={stale} age={age_s}s lines={len(lines)}")
    if broken and stale:
        print("ACTION: REPAIR — safe to trim (broken + stale)")
        sys.exit(2)  # exit 2 = repair needed
    elif broken and not stale:
        print("ACTION: WAIT — broken but still active (modified < 5min ago)")
        sys.exit(3)  # exit 3 = wait
    else:
        print("ACTION: OK — session is healthy")
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Safely trim an OpenClaw session file")
    parser.add_argument("session_file", nargs="?", help="Path to .jsonl session file")
    parser.add_argument("--keep", type=int, default=60, help="Minimum lines to keep (default: 60)")
    parser.add_argument("--check", metavar="SESSION_FILE", help="Check if session is broken/stale")
    args = parser.parse_args()

    if args.check:
        check_broken(args.check)
    elif args.session_file:
        safe_trim(args.session_file, args.keep)
    else:
        parser.print_help()
        sys.exit(1)
