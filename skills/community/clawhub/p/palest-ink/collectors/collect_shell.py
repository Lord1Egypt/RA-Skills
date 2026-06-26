#!/usr/bin/env python3
"""Palest Ink - Shell History Collector

Reads zsh/bash history files and extracts command records.
"""

import json
import os
import re
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")

# Possible history file locations
ZSH_HISTORY = os.path.expanduser("~/.zsh_history")
BASH_HISTORY = os.path.expanduser("~/.bash_history")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_datafile(dt):
    path = os.path.join(DATA_DIR, dt.strftime("%Y"), dt.strftime("%m"), f"{dt.strftime('%d')}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def should_exclude(cmd, patterns):
    for pattern in patterns:
        if re.match(pattern, cmd):
            return True
    return False


def parse_zsh_history(filepath, start_line):
    """Parse zsh extended history format: : timestamp:duration;command"""
    entries = []
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        # zsh history can have mixed encodings
        lines = raw.decode("utf-8", errors="replace").split("\n")
    except (OSError, IOError):
        return entries, start_line

    current_line = 0
    for line in lines:
        current_line += 1
        if current_line <= start_line:
            continue

        # Extended history format: : timestamp:duration;command
        match = re.match(r'^: (?P<ts>\d+):(?P<dur>\d+);(?P<cmd>.+)$', line)
        if match:
            ts = int(match.group("ts"))
            dur = int(match.group("dur"))
            cmd = match.group("cmd").strip()
            try:
                dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            except (OSError, ValueError):
                continue
            entries.append((dt, cmd, dur if dur > 0 else None))
        # Multi-line commands (continuation lines start with space or no colon prefix)
        elif entries and not line.startswith(": ") and line.strip():
            # Append to previous command
            prev_dt, prev_cmd, prev_dur = entries[-1]
            entries[-1] = (prev_dt, prev_cmd + "\n" + line, prev_dur)
        # Simple format (no timestamps) — treat each non-empty line as a command
        elif not line.startswith(": ") and line.strip() and not entries:
            # First line with no timestamp — this is simple format, switch to simple parser
            return _parse_zsh_simple(lines, start_line)

    return entries, current_line


def _parse_zsh_simple(lines, start_line):
    """Parse zsh simple history format (no timestamps, one command per line)."""
    entries = []
    now = datetime.now(timezone.utc)
    current_line = 0
    for line in lines:
        current_line += 1
        if current_line <= start_line:
            continue
        cmd = line.strip()
        if cmd:
            entries.append((now, cmd, None))
    return entries, current_line


def parse_bash_history(filepath, start_line):
    """Parse bash history (simple format, one command per line).
    If HISTTIMEFORMAT is set, timestamps appear as #timestamp on preceding line.
    """
    entries = []
    try:
        with open(filepath, "r", errors="replace") as f:
            lines = f.readlines()
    except (OSError, IOError):
        return entries, start_line

    current_line = 0
    pending_ts = None
    for line in lines:
        current_line += 1
        if current_line <= start_line:
            continue

        line = line.strip()
        if line.startswith("#") and line[1:].isdigit():
            pending_ts = int(line[1:])
            continue

        if line:
            if pending_ts:
                try:
                    dt = datetime.fromtimestamp(pending_ts, tz=timezone.utc)
                except (OSError, ValueError):
                    dt = datetime.now(timezone.utc)
                pending_ts = None
            else:
                dt = datetime.now(timezone.utc)
            entries.append((dt, line, None))

    return entries, current_line


def collect():
    config = load_config()
    if not config.get("collectors", {}).get("shell", True):
        return

    last_line = config.get("shell_last_line", 0)
    exclude_patterns = config.get("exclude_patterns", {}).get("commands", [])

    entries = []
    new_last_line = last_line

    # Try zsh first (more common on macOS), then bash
    if os.path.exists(ZSH_HISTORY):
        entries, new_last_line = parse_zsh_history(ZSH_HISTORY, last_line)
    elif os.path.exists(BASH_HISTORY):
        entries, new_last_line = parse_bash_history(BASH_HISTORY, last_line)

    if not entries:
        return

    records_by_file = {}
    count = 0

    for dt, cmd, duration in entries:
        if should_exclude(cmd, exclude_patterns):
            continue
        # Skip very long commands (likely data, not real commands)
        if len(cmd) > 1000:
            continue

        record = {
            "ts": dt.isoformat(),
            "type": "shell_command",
            "source": "shell_collector",
            "data": {
                "command": cmd,
                "duration_seconds": duration,
            }
        }

        datafile = get_datafile(dt)
        if datafile not in records_by_file:
            records_by_file[datafile] = []
        records_by_file[datafile].append(record)
        count += 1

    for datafile, records in records_by_file.items():
        with open(datafile, "a") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    config["shell_last_line"] = new_last_line
    save_config(config)

    if count > 0:
        print(f"[shell] Collected {count} commands")


if __name__ == "__main__":
    collect()
