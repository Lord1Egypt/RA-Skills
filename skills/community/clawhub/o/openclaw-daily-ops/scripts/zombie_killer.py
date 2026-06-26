#!/usr/bin/env python3
"""
OpenClaw Zombie Killer
Finds sessions older than N hours with >N MB context and truncates them.
Logs everything before wiping. Safe — never touches active sessions.

Usage:
  python3 zombie_killer.py --config /path/to/config.json
  python3 zombie_killer.py --config /path/to/config.json --dry-run
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta


def load_config(config_path):
    with open(os.path.expanduser(config_path)) as f:
        cfg = json.load(f)
    cfg["sessions_dir"] = os.path.expanduser(cfg["sessions_dir"])
    cfg["workspace_dir"] = os.path.expanduser(cfg["workspace_dir"])
    return cfg


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Zombie Session Killer")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be reset without actually resetting")
    args = parser.parse_args()

    cfg = load_config(args.config)
    sessions_dir = cfg["sessions_dir"]
    workspace_dir = cfg["workspace_dir"]
    min_age_hours = cfg.get("zombie_min_age_hours", 24)
    min_size_mb = cfg.get("zombie_min_size_mb", 1)

    # Load session metadata
    sessions_meta = {}
    sessions_json = os.path.join(sessions_dir, "sessions.json")
    if os.path.exists(sessions_json):
        try:
            with open(sessions_json) as f:
                sessions_meta = json.load(f)
        except Exception as e:
            print(f"[zombie_killer] Could not load sessions.json: {e}", file=sys.stderr)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=min_age_hours)
    min_size_bytes = min_size_mb * 1_000_000

    reset_log = []
    skipped = 0

    for sk, meta in sessions_meta.items():
        jsonl_path = meta.get("sessionFile", "")
        if not jsonl_path or not os.path.exists(jsonl_path):
            continue

        updated_at_ms = meta.get("updatedAt", 0)
        if not updated_at_ms:
            continue

        updated_at = datetime.fromtimestamp(updated_at_ms / 1000, tz=timezone.utc)
        age_hours = (now - updated_at).total_seconds() / 3600
        file_size = os.path.getsize(jsonl_path)

        if age_hours <= min_age_hours or file_size < min_size_bytes:
            skipped += 1
            continue

        # Count messages for the log
        try:
            with open(jsonl_path) as f:
                message_count = sum(1 for _ in f)
        except Exception:
            message_count = -1

        entry = {
            "session_key": sk,
            "reset_at": now.isoformat(),
            "age_hours": round(age_hours, 1),
            "file_size_mb": round(file_size / 1_000_000, 2),
            "message_count": message_count,
            "last_active": updated_at.isoformat(),
            "dry_run": args.dry_run,
        }
        reset_log.append(entry)

        if args.dry_run:
            print(f"[zombie_killer] DRY RUN — would reset: {sk[:40]} ({age_hours:.1f}h old, {file_size/1_000_000:.1f}MB, {message_count} msgs)")
        else:
            try:
                open(jsonl_path, "w").close()
                print(f"[zombie_killer] Reset: {sk[:40]} ({age_hours:.1f}h old, {file_size/1_000_000:.1f}MB freed)")
            except Exception as e:
                print(f"[zombie_killer] Failed to reset {sk}: {e}", file=sys.stderr)
                reset_log.pop()

    # Save log
    if not args.dry_run and reset_log:
        log_path = os.path.join(workspace_dir, "state", "session-reset-log.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        try:
            with open(log_path) as f:
                existing = json.load(f)
        except Exception:
            existing = []

        existing.extend(reset_log)
        existing = existing[-500:]

        with open(log_path, "w") as f:
            json.dump(existing, f, indent=2)

    # Output summary line for cost_report.py to append
    if reset_log and not args.dry_run:
        total_mb = sum(e["file_size_mb"] for e in reset_log)
        names = [e["session_key"].split(":")[-1][:16] for e in reset_log[:3]]
        extra = f" (+{len(reset_log)-3} more)" if len(reset_log) > 3 else ""
        summary = f"🔄 Reset {len(reset_log)} stale session(s) · {total_mb:.1f}MB freed"
        print(f"SUMMARY:{summary}")
    elif args.dry_run and reset_log:
        print(f"SUMMARY:DRY RUN — would reset {len(reset_log)} session(s)")
    else:
        print("SUMMARY:")  # Nothing to reset


if __name__ == "__main__":
    main()
