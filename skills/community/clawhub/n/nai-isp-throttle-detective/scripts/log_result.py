#!/usr/bin/env python3
"""
log_result.py - Append speedtest results to a structured JSON log.

Usage:
  python3 speedtest.py | python3 log_result.py
  python3 log_result.py --input result.json
  python3 log_result.py --log /custom/path/log.jsonl
"""

import json
import os
import sys
from datetime import datetime

DEFAULT_LOG_DIR = os.path.expanduser("~/.isp-throttle-detective")
DEFAULT_LOG_FILE = os.path.join(DEFAULT_LOG_DIR, "speed_log.jsonl")


def get_log_path(config_path: str | None = None) -> str:
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
        return os.path.expanduser(cfg.get("log_file", DEFAULT_LOG_FILE))
    default_cfg = os.path.expanduser("~/.isp-throttle-detective/config.json")
    if os.path.exists(default_cfg):
        with open(default_cfg) as f:
            cfg = json.load(f)
        return os.path.expanduser(cfg.get("log_file", DEFAULT_LOG_FILE))
    return DEFAULT_LOG_FILE


def enrich_entry(raw: dict) -> dict:
    """Add day_of_week, hour, date fields for easier analysis."""
    ts_str = raw.get("timestamp_local") or raw.get("timestamp_utc", "")
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now()

    entry = dict(raw)
    entry["date"] = dt.strftime("%Y-%m-%d")
    entry["hour"] = dt.hour
    entry["day_of_week"] = dt.strftime("%A")  # Monday, Tuesday, etc.
    entry["day_num"] = dt.weekday()  # 0=Monday ... 6=Sunday
    return entry


def append_to_log(entry: dict, log_path: str) -> None:
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    args = sys.argv[1:]
    input_file = None
    log_path_override = None
    config_path = None

    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--log" and i + 1 < len(args):
            log_path_override = args[i + 1]
            i += 2
        elif args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
            i += 2
        else:
            i += 1

    # Read input
    if input_file:
        with open(input_file) as f:
            raw = json.load(f)
    elif not sys.stdin.isatty():
        raw = json.load(sys.stdin)
    else:
        print("Error: provide input via stdin or --input <file>", file=sys.stderr)
        sys.exit(1)

    log_path = log_path_override or get_log_path(config_path)
    entry = enrich_entry(raw)
    append_to_log(entry, log_path)

    # Summary to stderr
    speeds = [
        v["speed_mbps"]
        for v in entry.get("results", {}).values()
        if v.get("speed_mbps") is not None and v.get("category") != "upload"
    ]
    avg = round(sum(speeds) / len(speeds), 2) if speeds else "N/A"
    print(f"[log_result] Logged to {log_path}", file=sys.stderr)
    print(f"[log_result] Timestamp: {entry.get('timestamp_local', '?')}", file=sys.stderr)
    print(f"[log_result] Avg download speed: {avg} Mbps", file=sys.stderr)


if __name__ == "__main__":
    main()
