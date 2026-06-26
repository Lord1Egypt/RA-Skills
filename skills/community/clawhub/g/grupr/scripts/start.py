#!/usr/bin/env python3
"""start.py — spawn a long-running stream daemon for one grupr.

Spawns `scripts/stream.py <grupr-id>` as a detached background process,
captures the PID into the per-grupr state file, and tails the log file
to confirm the daemon connected.

Usage:
    uv run python scripts/start.py <grupr-id>
    uv run python scripts/start.py <grupr-id> --openclaw-agent analystbot
    uv run python scripts/start.py <grupr-id> --catch-up 5m
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_DIR / ".env"


def state_path(grupr_id: str) -> Path:
    return SKILL_DIR / f".state-{grupr_id}.json"


def load_env() -> None:
    if not ENV_PATH.exists():
        print(f"ERROR: {ENV_PATH} not found. Run scripts/login.py first.", file=sys.stderr)
        sys.exit(2)
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


def parse_duration(s: str) -> timedelta:
    m = re.match(r"^(\d+)([smh])$", s)
    if not m:
        raise ValueError(f"bad duration {s!r} (expected like '30s', '5m', '2h')")
    n = int(m.group(1))
    unit = m.group(2)
    if unit == "s":
        return timedelta(seconds=n)
    if unit == "m":
        return timedelta(minutes=n)
    return timedelta(hours=n)


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Start a Grupr WebSocket stream daemon")
    parser.add_argument("grupr_id", help="UUID of the grupr to stream")
    parser.add_argument("--openclaw-agent", default="main", help="OpenClaw agent name (default: main)")
    parser.add_argument(
        "--catch-up",
        default=None,
        help="Initial cursor offset before now (e.g. '5m', '1h'). Default: cursor=now.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-message agent timeout in seconds (default: 120)",
    )
    args = parser.parse_args()

    load_env()
    if not os.environ.get("GRUPR_AGENT_TOKEN"):
        print("ERROR: .env missing GRUPR_AGENT_TOKEN. Run login.py.", file=sys.stderr)
        return 2

    sf = state_path(args.grupr_id)
    if sf.exists():
        existing = json.loads(sf.read_text())
        existing_pid = existing.get("pid")
        if existing_pid and is_alive(existing_pid):
            print(
                f"ERROR: stream daemon already running for grupr {args.grupr_id} "
                f"(pid={existing_pid}). Run stop.py first.",
                file=sys.stderr,
            )
            return 3

    # Pre-seed cursor (default: now; --catch-up shifts it back).
    now = datetime.now(timezone.utc)
    cursor_dt = now - parse_duration(args.catch_up) if args.catch_up else now
    cursor_iso = cursor_dt.isoformat()
    existing = json.loads(sf.read_text()) if sf.exists() else {}
    existing.update({"cursor": cursor_iso})
    existing.pop("pid", None)
    existing.pop("started_at", None)
    existing.pop("cron_job_id", None)  # legacy from v0.1
    existing.pop("name", None)
    sf.write_text(json.dumps(existing, indent=2) + "\n")
    print(f"Cursor pre-seeded to {cursor_iso}")

    # Build the daemon command. Output is appended to logs/stream-<short>.log.
    short_id = args.grupr_id.split("-")[0]
    log_dir = SKILL_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"stream-{short_id}.log"

    cmd = [
        "uv", "run", "python", "scripts/stream.py", args.grupr_id,
        "--openclaw-agent", args.openclaw_agent,
        "--timeout", str(args.timeout),
    ]
    print(f"Spawning: {' '.join(cmd)}")
    print(f"Logs: {log_file}")

    # Detach: new session so the daemon survives the parent exit.
    log_fh = open(log_file, "ab")
    proc = subprocess.Popen(
        cmd,
        cwd=SKILL_DIR,
        stdout=log_fh,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Give the child a moment to write its PID + connect to WS.
    time.sleep(2.0)
    if not is_alive(proc.pid):
        print(f"ERROR: stream daemon exited immediately. Check {log_file}", file=sys.stderr)
        try:
            tail = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-20:]
            print("\n".join(tail), file=sys.stderr)
        except OSError:
            pass
        return 4

    print(f"✓ Stream daemon started (pid={proc.pid})")
    print(f"✓ State: {sf}")
    print()
    print(f"To stop: python3 scripts/stop.py {args.grupr_id}")
    print(f"To tail logs: tail -f {log_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
