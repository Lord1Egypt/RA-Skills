#!/usr/bin/env python3
"""Palest Ink - App Focus Collector

Tracks which application is in the foreground using osascript.
Merges duration in-place when the same app+window persists across runs.
"""

import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")

LOCK_APPS = {"loginwindow", "ScreenSaverEngine"}


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


def get_frontmost_app():
    """Return (app_name, window_title) of the frontmost application, or (None, None) on failure."""
    script = '''
tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
end tell
tell application frontApp
    try
        set winTitle to name of front window
    on error
        set winTitle to ""
    end try
end tell
return frontApp & "|||" & winTitle
'''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode != 0:
            return None, None
        output = result.stdout.strip()
        if "|||" in output:
            parts = output.split("|||", 1)
            return parts[0].strip(), parts[1].strip()
        return output, ""
    except (subprocess.TimeoutExpired, OSError):
        return None, None


def atomic_update_line(filepath, line_number, new_record):
    """Replace a specific line in a file atomically using a temp file."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        if line_number < 1 or line_number > len(lines):
            return False
        lines[line_number - 1] = json.dumps(new_record, ensure_ascii=False) + "\n"
        tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(filepath))
        try:
            with os.fdopen(tmp_fd, "w") as tmp_f:
                tmp_f.writelines(lines)
            os.replace(tmp_path, filepath)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            return False
        return True
    except (OSError, IOError):
        return False


def count_lines(filepath):
    """Count lines in a file."""
    try:
        with open(filepath, "r") as f:
            return sum(1 for _ in f)
    except (OSError, IOError):
        return 0


def collect():
    config = load_config()
    if not config.get("collectors", {}).get("app", True):
        return

    app_exclude = set(config.get("app", {}).get("exclude", [
        "loginwindow", "Dock", "SystemUIServer", "Finder", "ScreenSaverEngine"
    ]))

    app_name, window_title = get_frontmost_app()
    if app_name is None:
        return

    # Skip lock screen / screen saver
    if app_name in LOCK_APPS or app_name in app_exclude:
        return

    now = datetime.now(timezone.utc)
    now_str = now.isoformat()
    today_str = now.strftime("%Y-%m-%d")

    # Check if same app+window as last time
    last_app = config.get("app_last_app", "")
    last_window = config.get("app_last_window", "")
    last_ts_str = config.get("app_last_ts", "")
    last_line = config.get("app_last_record_line", -1)

    same_app = (app_name == last_app and window_title == last_window)

    if same_app and last_ts_str and last_line >= 1:
        # Determine if last record is from same day
        try:
            last_dt = datetime.fromisoformat(last_ts_str)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            last_day = last_dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            last_day = ""

        if last_day == today_str:
            # Try to merge duration into last record
            datafile = get_datafile(now)
            # Duration = time since last record ts
            try:
                elapsed = int((now - last_dt).total_seconds())
            except Exception:
                elapsed = 15  # fallback

            # Read existing record
            try:
                with open(datafile, "r") as f:
                    lines = f.readlines()
                if 1 <= last_line <= len(lines):
                    existing = json.loads(lines[last_line - 1])
                    prev_duration = existing.get("data", {}).get("duration_seconds", 0)
                    existing["data"]["duration_seconds"] = prev_duration + elapsed
                    if atomic_update_line(datafile, last_line, existing):
                        config["app_last_ts"] = now_str
                        save_config(config)
                        return
            except (OSError, json.JSONDecodeError):
                pass
            # Fallback: write new record below

    # Write new record
    datafile = get_datafile(now)
    record = {
        "ts": now_str,
        "type": "app_focus",
        "source": "app_collector",
        "data": {
            "app_name": app_name,
            "window_title": window_title,
            "duration_seconds": 15,
        }
    }

    with open(datafile, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    new_line = count_lines(datafile)
    config["app_last_app"] = app_name
    config["app_last_window"] = window_title
    config["app_last_ts"] = now_str
    config["app_last_record_line"] = new_line
    save_config(config)

    print(f"[app] {app_name} — {window_title[:60]}")


if __name__ == "__main__":
    collect()
