#!/usr/bin/env python3
"""
task_logger.py — Per-task cost logger for Max / Lemnos AI Operations

HOW IT WORKS:
  Takes a snapshot of current session token usage BEFORE a task starts,
  then calculates the delta AFTER the task completes. Logs cost, tokens,
  and call count to task-log.jsonl with a task type label.

USAGE (Python):
  from task_logger import TaskLogger
  with TaskLogger("prospect_research", "Batch 7 — 15 NJ targets"):
      # do work
      pass

USAGE (Shell — two-step):
  python3 task_logger.py start "email_send" "FU4 — 4 follow-ups"  # prints snapshot ID
  python3 task_logger.py end <snapshot_id>                          # logs the delta

TASK TYPES:
  briefing            — 6:30 AM daily briefing
  email_send          — sending approved email batches
  email_draft         — writing/preparing email copy
  prospect_research   — finding and profiling new targets
  bounce_check        — running bounce detection
  tweet_draft         — drafting tweets for approval
  tweet_send          — posting via OpenTweet
  reddit_scan         — Reddit pain point scan
  reddit_draft        — drafting Reddit comments
  memory_update       — writing/updating memory files
  cost_report         — running cost reports
  reply_monitor       — checking for email replies
  linkedin_research   — researching LinkedIn targets
  trl_intel           — TRL/supplement market research
  aeramed_research    — AeraMed product/competitor research
  crypto_monitor      — crypto/market monitoring
  other               — catch-all
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from contextlib import contextmanager

SESSION_DIR = "/root/.openclaw/agents/main/sessions"
LOG_PATH = "/root/.openclaw/workspace/skills/lemnos-cost-guard/references/task-log.jsonl"
SNAPSHOT_DIR = "/root/.openclaw/workspace/skills/lemnos-cost-guard/references/snapshots"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


# ── Session reader ──────────────────────────────────────────────────────────

def read_session_totals():
    """Read current cumulative totals from all session JSONL files (today)."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    totals = {"calls": 0, "input": 0, "output": 0,
              "cache_read": 0, "cache_write": 0, "cost": 0.0}

    if not os.path.exists(SESSION_DIR):
        return totals

    for fname in os.listdir(SESSION_DIR):
        if not fname.endswith(".jsonl"):
            continue
        try:
            with open(os.path.join(SESSION_DIR, fname)) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        ts = obj.get("timestamp", obj.get("message", {}).get("timestamp", ""))
                        if not ts or ts[:10] != today:
                            continue
                        usage = obj.get("message", {}).get("usage", {})
                        if usage and "cost" in usage:
                            totals["calls"] += 1
                            totals["input"] += usage.get("input", 0)
                            totals["output"] += usage.get("output", 0)
                            totals["cache_read"] += usage.get("cacheRead", 0)
                            totals["cache_write"] += usage.get("cacheWrite", 0)
                            totals["cost"] += usage["cost"].get("total", 0)
                    except (json.JSONDecodeError, KeyError):
                        continue
        except (IOError, OSError):
            continue

    return totals


# ── Snapshot helpers ────────────────────────────────────────────────────────

def save_snapshot(task_type: str, description: str) -> str:
    """Save a pre-task snapshot. Returns snapshot_id."""
    snap_id = str(uuid.uuid4())[:8]
    snapshot = {
        "snapshot_id": snap_id,
        "task_type": task_type,
        "description": description,
        "timestamp_start": datetime.now(timezone.utc).isoformat(),
        "totals_before": read_session_totals()
    }
    snap_path = os.path.join(SNAPSHOT_DIR, f"{snap_id}.json")
    with open(snap_path, "w") as f:
        json.dump(snapshot, f)
    return snap_id


def load_snapshot(snap_id: str) -> dict:
    snap_path = os.path.join(SNAPSHOT_DIR, f"{snap_id}.json")
    with open(snap_path) as f:
        return json.load(f)


def delete_snapshot(snap_id: str):
    snap_path = os.path.join(SNAPSHOT_DIR, f"{snap_id}.json")
    if os.path.exists(snap_path):
        os.remove(snap_path)


# ── Log writer ──────────────────────────────────────────────────────────────

def log_task(task_type: str, description: str, before: dict, after: dict,
             timestamp_start: str, timestamp_end: str, status: str = "ok"):
    """Calculate delta and append to task-log.jsonl."""
    delta_calls = after["calls"] - before["calls"]
    delta_input = after["input"] - before["input"]
    delta_output = after["output"] - before["output"]
    delta_cache_read = after["cache_read"] - before["cache_read"]
    delta_cache_write = after["cache_write"] - before["cache_write"]
    delta_cost = after["cost"] - before["cost"]

    entry = {
        "timestamp": timestamp_end,
        "date": timestamp_end[:10],
        "task_type": task_type,
        "description": description,
        "status": status,
        "calls": max(0, delta_calls),
        "input_tokens": max(0, delta_input),
        "output_tokens": max(0, delta_output),
        "cache_read_tokens": max(0, delta_cache_read),
        "cache_write_tokens": max(0, delta_cache_write),
        "cost_usd": round(max(0.0, delta_cost), 6),
        "duration_start": timestamp_start,
        "duration_end": timestamp_end,
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


# ── Context manager (Python usage) ─────────────────────────────────────────

class TaskLogger:
    """
    Context manager for per-task cost logging.

    Usage:
        with TaskLogger("prospect_research", "Batch 7 — 15 NJ targets"):
            do_work()
    """
    def __init__(self, task_type: str, description: str = "", status: str = "ok"):
        self.task_type = task_type
        self.description = description
        self.status = status
        self.before = None
        self.timestamp_start = None

    def __enter__(self):
        self.before = read_session_totals()
        self.timestamp_start = datetime.now(timezone.utc).isoformat()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        after = read_session_totals()
        status = "error" if exc_type else self.status
        entry = log_task(
            task_type=self.task_type,
            description=self.description,
            before=self.before,
            after=after,
            timestamp_start=self.timestamp_start,
            timestamp_end=datetime.now(timezone.utc).isoformat(),
            status=status
        )
        print(f"[task_logger] {self.task_type}: ${entry['cost_usd']:.4f} | "
              f"{entry['calls']} calls | {entry['output_tokens']:,} out tokens")
        return False  # don't suppress exceptions


# ── CLI interface ───────────────────────────────────────────────────────────

def cli_start(task_type: str, description: str):
    snap_id = save_snapshot(task_type, description)
    print(snap_id)  # caller captures this


def cli_end(snap_id: str, status: str = "ok"):
    snap = load_snapshot(snap_id)
    after = read_session_totals()
    entry = log_task(
        task_type=snap["task_type"],
        description=snap["description"],
        before=snap["totals_before"],
        after=after,
        timestamp_start=snap["timestamp_start"],
        timestamp_end=datetime.now(timezone.utc).isoformat(),
        status=status
    )
    delete_snapshot(snap_id)
    print(f"[task_logger] LOGGED: {snap['task_type']} | ${entry['cost_usd']:.4f} | "
          f"{entry['calls']} calls | {entry['output_tokens']:,} out tokens")


def cli_log(task_type: str, description: str, cost: float = 0.0,
            calls: int = 0, output_tokens: int = 0):
    """Direct log entry (for shell scripts that can't do delta tracking)."""
    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": now,
        "date": now[:10],
        "task_type": task_type,
        "description": description,
        "status": "ok",
        "calls": calls,
        "input_tokens": 0,
        "output_tokens": output_tokens,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost_usd": round(cost, 6),
        "duration_start": now,
        "duration_end": now,
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[task_logger] LOGGED: {task_type} | ${cost:.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  task_logger.py start <task_type> <description>")
        print("  task_logger.py end <snapshot_id> [status]")
        print("  task_logger.py log <task_type> <description> [--cost X] [--calls N] [--tokens N]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "start":
        task_type = sys.argv[2] if len(sys.argv) > 2 else "other"
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        cli_start(task_type, description)

    elif cmd == "end":
        snap_id = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "ok"
        cli_end(snap_id, status)

    elif cmd == "log":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("_cmd")
        parser.add_argument("task_type")
        parser.add_argument("description", nargs="?", default="")
        parser.add_argument("--cost", type=float, default=0.0)
        parser.add_argument("--calls", type=int, default=0)
        parser.add_argument("--tokens", type=int, default=0)
        args = parser.parse_args()
        cli_log(args.task_type, args.description, args.cost, args.calls, args.tokens)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
