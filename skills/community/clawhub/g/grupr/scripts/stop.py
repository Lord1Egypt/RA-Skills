#!/usr/bin/env python3
"""stop.py — gracefully stop the stream daemon for a grupr.

Reads `.state-<grupr-id>.json` to find the daemon PID, sends SIGTERM,
waits up to 10s for clean shutdown, then SIGKILLs if still alive.

Usage:
    uv run python scripts/stop.py <grupr-id>
    uv run python scripts/stop.py <grupr-id> --keep-state
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

GRACEFUL_WAIT_SECONDS = 10.0
POLL_INTERVAL = 0.25


def state_path(grupr_id: str) -> Path:
    return SKILL_DIR / f".state-{grupr_id}.json"


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop a Grupr stream daemon")
    parser.add_argument("grupr_id", help="UUID of the grupr whose daemon to stop")
    parser.add_argument(
        "--keep-state",
        action="store_true",
        help="Don't delete the .state file (preserves cursor for a future restart)",
    )
    args = parser.parse_args()

    sf = state_path(args.grupr_id)
    if not sf.exists():
        print(f"No state file at {sf} — nothing to stop.", file=sys.stderr)
        return 1

    state = json.loads(sf.read_text())
    pid = state.get("pid")
    if not pid:
        print(f"State file {sf} has no pid — daemon never started, or already stopped.", file=sys.stderr)
        if not args.keep_state:
            sf.unlink()
            print(f"Removed {sf}.")
        return 0

    if not is_alive(pid):
        print(f"PID {pid} not running — daemon already stopped.")
        state.pop("pid", None)
        state.pop("started_at", None)
    else:
        print(f"Sending SIGTERM to pid {pid}...")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

        deadline = time.monotonic() + GRACEFUL_WAIT_SECONDS
        while time.monotonic() < deadline and is_alive(pid):
            time.sleep(POLL_INTERVAL)

        if is_alive(pid):
            print(f"  SIGTERM ignored after {GRACEFUL_WAIT_SECONDS:.0f}s — sending SIGKILL")
            try:
                os.kill(pid, signal.SIGKILL)
                time.sleep(0.5)
            except ProcessLookupError:
                pass

        state.pop("pid", None)
        state.pop("started_at", None)

    if args.keep_state:
        sf.write_text(json.dumps(state, indent=2) + "\n")
        print(f"✓ Stopped; state preserved at {sf} (cursor kept).")
    else:
        sf.unlink()
        print(f"✓ Stopped; state file deleted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
