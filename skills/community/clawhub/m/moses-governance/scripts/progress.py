#!/usr/bin/env python3
"""
progress.py — MO§ES™ Task Progress Tracker
Writes/reads progress.json after each governed action.
Gives sessions continuity across context windows.

Usage:
  python3 progress.py start "<task>"        # Start a new task
  python3 progress.py step "<action>"       # Log a completed step
  python3 progress.py status                # Show current progress
  python3 progress.py done                  # Mark task complete
  python3 progress.py reset                 # Clear progress state
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

PROGRESS_PATH = os.path.expanduser("~/.openclaw/governance/progress.json")


def ensure_dir():
    os.makedirs(os.path.dirname(PROGRESS_PATH), exist_ok=True)


def load() -> dict:
    if not os.path.exists(PROGRESS_PATH):
        return {}
    with open(PROGRESS_PATH) as f:
        return json.load(f)


def save(data: dict):
    ensure_dir()
    with open(PROGRESS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def cmd_start(args):
    if not args:
        print("[PROGRESS] Usage: progress.py start \"<task description>\"")
        sys.exit(1)
    task = " ".join(args)
    data = {
        "task": task,
        "started_at": now(),
        "status": "in_progress",
        "steps": [],
        "recovery_needed": False,
    }
    save(data)
    print(f"[PROGRESS] Task started: {task}")


def cmd_step(args):
    if not args:
        print("[PROGRESS] Usage: progress.py step \"<action completed>\"")
        sys.exit(1)
    data = load()
    if not data:
        print("[PROGRESS] No active task. Run: progress.py start \"<task>\"")
        sys.exit(1)
    action = " ".join(args)
    step = {
        "action": action,
        "at": now(),
        "hash": hashlib.sha256(f"{action}{now()}".encode()).hexdigest()[:16],
    }
    data.setdefault("steps", []).append(step)
    data["recovery_needed"] = False
    save(data)
    print(f"[PROGRESS] Step logged: {action}")
    print(f"  Total steps: {len(data['steps'])}")


def cmd_status(_args):
    data = load()
    if not data:
        print("[PROGRESS] No active task.")
        return
    print(f"[PROGRESS] Task    : {data.get('task', 'unknown')}")
    print(f"  Status   : {data.get('status', 'unknown')}")
    print(f"  Started  : {data.get('started_at', 'unknown')}")
    print(f"  Steps    : {len(data.get('steps', []))}")
    if data.get("recovery_needed"):
        print("  ⚠ RECOVERY NEEDED — last action failed, operator review required")
    if data.get("steps"):
        print("  Last step:", data["steps"][-1]["action"])


def cmd_done(_args):
    data = load()
    if not data:
        print("[PROGRESS] No active task.")
        sys.exit(1)
    data["status"] = "complete"
    data["completed_at"] = now()
    save(data)
    print(f"[PROGRESS] Task complete: {data.get('task')}")
    print(f"  Steps taken: {len(data.get('steps', []))}")


def cmd_reset(_args):
    if os.path.exists(PROGRESS_PATH):
        os.remove(PROGRESS_PATH)
    print("[PROGRESS] Progress cleared.")


def cmd_flag_recovery(_args):
    """Called by audit_stub on FAIL outcome — flags operator review needed."""
    data = load()
    if not data:
        return
    data["recovery_needed"] = True
    data["recovery_flagged_at"] = now()
    save(data)
    print("[PROGRESS] Recovery flag set — operator review required before next step.")


COMMANDS = {
    "start": cmd_start,
    "step": cmd_step,
    "status": cmd_status,
    "done": cmd_done,
    "reset": cmd_reset,
    "flag-recovery": cmd_flag_recovery,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    if cmd not in COMMANDS:
        print(f"Usage: progress.py [{'|'.join(COMMANDS)}]")
        sys.exit(1)
    COMMANDS[cmd](args)
