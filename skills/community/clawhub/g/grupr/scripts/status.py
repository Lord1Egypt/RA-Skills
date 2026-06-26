#!/usr/bin/env python3
"""status.py — show the state of every Grupr stream daemon registered by this skill.

For each `.state-<grupr-id>.json` file in the skill directory, prints:
  - grupr_id (short)
  - pid + started_at (if running)
  - cursor (last processed message timestamp)
  - whether the process is still alive (`os.kill(pid, 0)`)

Usage:
    uv run python scripts/status.py
    uv run python scripts/status.py --json   # machine-readable
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


def load_state_files() -> list[dict]:
    entries = []
    for p in sorted(SKILL_DIR.glob(".state-*.json")):
        grupr_id = p.stem.removeprefix(".state-")
        try:
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                data = {}
        except (json.JSONDecodeError, ValueError):
            data = {"_error": "corrupt state file"}
        entries.append({"grupr_id": grupr_id, **data, "_path": str(p)})
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Status of registered Grupr stream daemons")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    args = parser.parse_args()

    entries = load_state_files()

    enriched = []
    for e in entries:
        pid = e.get("pid")
        if not pid:
            status = "not started"
        elif is_alive(int(pid)):
            status = "running"
        else:
            status = "crashed/stopped"
        enriched.append({**e, "_status": status})

    if args.json:
        clean = [{k: v for k, v in e.items() if not k.startswith("_") or k == "_status"} for e in enriched]
        print(json.dumps({"daemons": clean, "skill_dir": str(SKILL_DIR)}, indent=2))
        return 0

    if not enriched:
        print("No Grupr stream state files found.")
        print(f"  skill dir: {SKILL_DIR}")
        print("  Run scripts/login.py to mint a token, then scripts/start.py <grupr-id> to begin streaming.")
        return 0

    print(f"Skill dir: {SKILL_DIR}")
    print(f"Found {len(enriched)} grupr stream daemon(s):")
    print()
    marker_for = {"running": "✓", "crashed/stopped": "✗", "not started": "○"}
    for e in enriched:
        gid = e["grupr_id"]
        gid_short = gid.split("-")[0] if "-" in gid else gid[:8]
        cursor = e.get("cursor", "<unset>")
        pid = e.get("pid", "-")
        started = e.get("started_at", "-")
        marker = marker_for.get(e["_status"], "?")
        print(f"  {marker} {gid_short}  ({gid})")
        print(f"      pid:        {pid}  [{e['_status']}]")
        print(f"      started_at: {started}")
        print(f"      cursor:     {cursor}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
