#!/usr/bin/env python3
"""Palest Ink - Safari History Collector

Reads Safari's SQLite History database and extracts browsing records.
Note: Requires Full Disk Access permission on macOS.
"""

import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone, timedelta

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")
SAFARI_HISTORY = os.path.expanduser("~/Library/Safari/History.db")

# Safari timestamps are seconds since 2001-01-01 (Core Data / NSDate epoch)
CORE_DATA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)


def safari_time_to_datetime(safari_ts):
    """Convert Safari/Core Data timestamp to Python datetime."""
    if not safari_ts or safari_ts <= 0:
        return None
    try:
        return CORE_DATA_EPOCH + timedelta(seconds=safari_ts)
    except (OSError, ValueError, OverflowError):
        return None


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


def should_exclude(url, exclude_patterns):
    for pattern in exclude_patterns:
        if url.startswith(pattern):
            return True
    return False


def collect():
    if not os.path.exists(SAFARI_HISTORY):
        return

    config = load_config()
    if not config.get("collectors", {}).get("safari", True):
        return

    last_visit_id = config.get("safari_last_visit_id", 0)
    exclude_patterns = config.get("exclude_patterns", {}).get("urls", [])

    # Copy DB to avoid lock
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".db")
    os.close(tmp_fd)
    try:
        shutil.copy2(SAFARI_HISTORY, tmp_path)
    except (PermissionError, OSError) as e:
        print(f"[safari] Cannot access Safari history: {e}")
        print("[safari] Please grant Full Disk Access to Terminal/iTerm in System Settings.")
        os.unlink(tmp_path)
        return

    try:
        conn = sqlite3.connect(tmp_path)
        conn.row_factory = sqlite3.Row

        # Safari schema: history_items (id, url, ...) + history_visits (id, history_item, visit_time, ...)
        rows = conn.execute("""
            SELECT hv.id, hi.url, hi.domain_expansion, hv.visit_time, hv.title
            FROM history_visits hv
            JOIN history_items hi ON hv.history_item = hi.id
            WHERE hv.id > ?
            ORDER BY hv.id
        """, (last_visit_id,)).fetchall()

        new_last_id = last_visit_id
        records_by_file = {}

        for row in rows:
            vid = row["id"]
            url = row["url"] or ""
            title = row["title"] or row["domain_expansion"] or ""
            vtime = row["visit_time"]

            if should_exclude(url, exclude_patterns):
                new_last_id = max(new_last_id, vid)
                continue

            dt = safari_time_to_datetime(vtime)
            if dt is None:
                new_last_id = max(new_last_id, vid)
                continue

            record = {
                "ts": dt.isoformat(),
                "type": "web_visit",
                "source": "safari_collector",
                "data": {
                    "url": url,
                    "title": title,
                    "visit_duration_seconds": 0,
                    "browser": "safari",
                    "content_pending": True
                }
            }

            datafile = get_datafile(dt)
            if datafile not in records_by_file:
                records_by_file[datafile] = []
            records_by_file[datafile].append(record)
            new_last_id = max(new_last_id, vid)

        conn.close()

        for datafile, records in records_by_file.items():
            with open(datafile, "a") as f:
                for record in records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

        config["safari_last_visit_id"] = new_last_id
        save_config(config)

        if rows:
            print(f"[safari] Collected {len(rows)} visits (last_id: {new_last_id})")

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    collect()
