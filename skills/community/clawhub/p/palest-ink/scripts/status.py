#!/usr/bin/env python3
"""Palest Ink - Status Checker

Shows collection status, data volume, and system health.

Usage:
    python3 status.py
"""

import json
import os
import subprocess
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")
CLEANUP_FLAG = os.path.join(PALEST_INK_DIR, "tmp", "cleanup_needed")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def count_today_records():
    now = datetime.now()
    path = os.path.join(DATA_DIR, now.strftime("%Y"), now.strftime("%m"), f"{now.strftime('%d')}.jsonl")
    if not os.path.exists(path):
        return 0, {}
    counts = {}
    total = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                rtype = record.get("type", "unknown")
                counts[rtype] = counts.get(rtype, 0) + 1
                total += 1
            except json.JSONDecodeError:
                pass
    return total, counts


def get_data_size():
    """Get total size of data directory."""
    total = 0
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total


def check_cleanup_needed():
    """Return flag info dict if cleanup is needed, else None."""
    if not os.path.exists(CLEANUP_FLAG):
        return None
    try:
        with open(CLEANUP_FLAG, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def check_cron():
    """Check if cron job is installed."""
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True, timeout=5
        )
        return "palest-ink" in result.stdout
    except (subprocess.TimeoutExpired, OSError):
        return False


def check_git_hooks():
    """Check if git hooks are configured."""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "core.hooksPath"],
            capture_output=True, text=True, timeout=5
        )
        hooks_path = result.stdout.strip()
        return hooks_path == os.path.join(PALEST_INK_DIR, "hooks")
    except (subprocess.TimeoutExpired, OSError):
        return False


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    print("=" * 50)
    print("  Palest Ink (淡墨) - Status")
    print("=" * 50)
    print()

    # Data directory
    if not os.path.exists(PALEST_INK_DIR):
        print("Status: NOT INSTALLED")
        print(f"Run install.sh to set up Palest Ink.")
        return

    config = load_config()
    collectors = config.get("collectors", {})

    # Today's records
    total, counts = count_today_records()
    data_bytes = get_data_size()
    print(f"Data directory: {DATA_DIR}")
    print(f"Data size: {format_size(data_bytes)}")
    print()

    # Cleanup warning
    cleanup_flag = check_cleanup_needed()
    if cleanup_flag is not None:
        flag_size = cleanup_flag.get("size_human", "")
        size_note = f" ({flag_size} MB)" if flag_size else ""
        print("=" * 50)
        print(f"  ⚠️  CLEANUP RECOMMENDED")
        print(f"  Data{size_note} is approaching the 2 GB limit.")
        print(f"  Run cleanup to remove oldest records:")
        print(f"    python3 ~/.palest-ink/bin/cleanup.py --dry-run")
        print(f"    python3 ~/.palest-ink/bin/cleanup.py")
        print("=" * 50)
        print()

    print(f"Today's records: {total}")
    if counts:
        for rtype, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {rtype}: {count}")
    print()

    # Collector status
    print("Collectors:")
    cron_active = check_cron()
    hooks_active = check_git_hooks()

    print(f"  git_hooks:  {'ACTIVE' if hooks_active else 'INACTIVE'} (core.hooksPath)")
    print(f"  cron:       {'ACTIVE' if cron_active else 'INACTIVE'} (every 3 min)")
    print(f"  chrome:     {'enabled' if collectors.get('chrome', True) else 'disabled'}")
    print(f"  safari:     {'enabled' if collectors.get('safari', True) else 'disabled'}")
    print(f"  shell:      {'enabled' if collectors.get('shell', True) else 'disabled'}")
    print(f"  vscode:     {'enabled' if collectors.get('vscode', True) else 'disabled'}")
    print(f"  git_scan:   {'enabled' if collectors.get('git_scan', True) else 'disabled'}")
    print(f"  content:    {'enabled' if collectors.get('content', True) else 'disabled'}")
    print()

    # Last cron run
    cron_log = os.path.join(PALEST_INK_DIR, "cron.log")
    if os.path.exists(cron_log):
        try:
            with open(cron_log, "r") as f:
                lines = f.readlines()
            # Find last "Starting collection" or "Collection complete"
            for line in reversed(lines):
                if "Collection complete" in line or "Starting collection" in line:
                    print(f"Last cron: {line.strip()}")
                    break
        except OSError:
            pass

    # Tracked repos
    tracked = config.get("tracked_repos", [])
    if tracked:
        print(f"\nTracked repos ({len(tracked)}):")
        for repo in tracked:
            print(f"  {repo}")


if __name__ == "__main__":
    main()
