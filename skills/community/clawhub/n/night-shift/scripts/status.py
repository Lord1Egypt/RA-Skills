#!/usr/bin/env python3
"""
Night Shift Status CLI — reads night-state.json and subagent-tasks.json
to produce a human-readable summary.

Usage:
    python3 status.py [--json]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

DATA_DIR = _DATA_DIR
STATE_FILE = DATA_DIR / "night-state.json"
TASK_QUEUE_FILE = DATA_DIR / "subagent-tasks.json"
LOG_FILE = DATA_DIR / "night-shift.log"


def load_json(path, default=None):
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return default if default is not None else {}


def today_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def parse_iso(s):
    """Parse an ISO timestamp, returning None on failure."""
    if not s:
        return None
    try:
        # Handle both with and without Z suffix
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def build_summary() -> dict:
    state = load_json(STATE_FILE, {
        "last_run": None,
        "tasks": {},
        "failures": [],
        "permanent_failure_streak": 0,
        "alerts_sent": [],
    })
    queue = load_json(TASK_QUEUE_FILE, {
        "pending": [],
        "completed": [],
        "failed": [],
    })

    today = today_iso()
    now = datetime.now(timezone.utc)

    # Filter completed/failed tasks to today
    completed_today = []
    for t in queue.get("completed", []):
        ts = t.get("completed_at", "")
        if ts.startswith(today):
            completed_today.append(t)

    failed_today = []
    for t in queue.get("failed", []):
        ts = t.get("completed_at", "")
        if ts.startswith(today):
            failed_today.append(t)

    # Pending tasks
    pending = queue.get("pending", [])

    # Log file info
    log_info = {"exists": False, "size_mb": 0}
    if LOG_FILE.exists():
        log_info["exists"] = True
        log_info["size_mb"] = round(LOG_FILE.stat().st_size / (1024 * 1024), 2)

    # Last run
    last_run = state.get("last_run")
    last_run_dt = parse_iso(last_run)
    last_run_ago = None
    if last_run_dt:
        # Ensure both are offset-aware for subtraction
        aware_dt = last_run_dt.replace(tzinfo=timezone.utc) if last_run_dt.tzinfo is None else last_run_dt
        delta = now - aware_dt
        total_min = int(delta.total_seconds() / 60)
        if total_min < 60:
            last_run_ago = f"{total_min}m ago"
        else:
            hours, mins = divmod(total_min, 60)
            last_run_ago = f"{hours}h {mins}m ago"

    # Alerts
    alerts = state.get("alerts_sent", [])
    recent_alerts = [a for a in alerts if a.get("time", "").startswith(today)]

    return {
        "date": today,
        "last_run": last_run,
        "last_run_ago": last_run_ago,
        "completed_today": len(completed_today),
        "failed_today": len(failed_today),
        "failed_permanent_today": len([t for t in failed_today if t.get("status") == "failed_permanent"]),
        "pending": len(pending),
        "permanent_failure_streak": state.get("permanent_failure_streak", 0),
        "alerts_today": len(recent_alerts),
        "log_size_mb": log_info["size_mb"],
        "completed_tasks": completed_today,
        "failed_tasks": failed_today,
        "pending_tasks": pending,
        "recent_alerts": recent_alerts,
    }


def print_summary(summary: dict):
    """Print a human-readable summary."""
    print("🌙 Night Shift Status")
    print(f"   Date: {summary['date']}")
    print(f"   Last run: {summary['last_run_ago'] or summary['last_run'] or 'never'}")
    print()

    # Counts
    ok = summary["completed_today"]
    fail = summary["failed_today"]
    perm = summary["failed_permanent_today"]
    pend = summary["pending"]

    print(f"   Today: ✅ {ok} completed  ❌ {fail} failed ({perm} permanent)  ⏳ {pend} pending")
    print()

    # Completed tasks
    if summary["completed_tasks"]:
        print("   ✅ Completed today:")
        for t in summary["completed_tasks"][:10]:
            tid = t.get("task_id", "?")
            result = (t.get("result") or "")[:70]
            print(f"      {tid}: {result}")
        if len(summary["completed_tasks"]) > 10:
            print(f"      ... and {len(summary['completed_tasks']) - 10} more")
        print()

    # Failed tasks
    if summary["failed_tasks"]:
        print("   ❌ Failed today:")
        for t in summary["failed_tasks"]:
            tid = t.get("task_id", "?")
            err = (t.get("error") or t.get("status", "unknown"))[:70]
            retries = t.get("retry_count", 0)
            print(f"      {tid} (retries={retries}): {err}")
        print()

    # Pending tasks
    if summary["pending_tasks"]:
        print(f"   ⏳ Pending ({len(summary['pending_tasks'])}):")
        for t in summary["pending_tasks"][:10]:
            tid = t.get("task_id", "?")
            prompt = (t.get("prompt") or "")[:60]
            retries = t.get("retry_count", 0)
            print(f"      {tid} (retries={retries}): {prompt}...")
        if len(summary["pending_tasks"]) > 10:
            print(f"      ... and {len(summary['pending_tasks']) - 10} more")
        print()

    # Alerts
    if summary["recent_alerts"]:
        print(f"   📨 Alerts sent today: {summary['alerts_today']}")
        for a in summary["recent_alerts"][-3:]:
            print(f"      {a.get('task_id', '?')}: {a.get('error', '?')[:60]}")
        print()

    # Streak
    streak = summary["permanent_failure_streak"]
    if streak > 0:
        print(f"   🔥 Consecutive permanent failures: {streak}")
        print()

    # Log
    if summary["log_size_mb"] > 0:
        print(f"   📋 Log: {summary['log_size_mb']} MB")


def main():
    p = argparse.ArgumentParser(description="Night Shift status viewer")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    args = p.parse_args()

    summary = build_summary()

    if args.json:
        print(json.dumps(summary, indent=2, default=str))
    else:
        print_summary(summary)


if __name__ == "__main__":
    main()
