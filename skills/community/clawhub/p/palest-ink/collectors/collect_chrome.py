#!/usr/bin/env python3
"""Palest Ink - Chrome History Collector

Reads Chrome's SQLite History database and extracts browsing records.
Uses a high-water mark to avoid re-processing visited URLs.
"""

import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")
CHROME_HISTORY = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/Default/History"
)

# Chrome timestamps are microseconds since 1601-01-01 (WebKit epoch)
WEBKIT_EPOCH_OFFSET = 11644473600


def chrome_time_to_datetime(chrome_ts):
    """Convert Chrome/WebKit timestamp to Python datetime."""
    if not chrome_ts or chrome_ts <= 0:
        return None
    unix_ts = (chrome_ts / 1_000_000) - WEBKIT_EPOCH_OFFSET
    try:
        return datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    except (OSError, ValueError):
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
    """Get the JSONL data file path for a given datetime."""
    path = os.path.join(DATA_DIR, dt.strftime("%Y"), dt.strftime("%m"), f"{dt.strftime('%d')}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def should_exclude(url, exclude_patterns):
    """Check if URL matches any exclusion pattern."""
    for pattern in exclude_patterns:
        if url.startswith(pattern):
            return True
    return False


def collect():
    if not os.path.exists(CHROME_HISTORY):
        return

    config = load_config()
    if not config.get("collectors", {}).get("chrome", True):
        return

    last_visit_id = config.get("chrome_last_visit_id", 0)
    exclude_patterns = config.get("exclude_patterns", {}).get("urls", [])

    # Copy DB to avoid Chrome's lock
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".db")
    os.close(tmp_fd)
    try:
        shutil.copy2(CHROME_HISTORY, tmp_path)
        conn = sqlite3.connect(tmp_path)
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT v.id, u.url, u.title, v.visit_time, v.visit_duration
            FROM visits v
            JOIN urls u ON v.url = u.id
            WHERE v.id > ?
            ORDER BY v.id
        """, (last_visit_id,)).fetchall()

        new_last_id = last_visit_id
        records_by_file = {}

        for row in rows:
            vid = row["id"]
            url = row["url"] or ""
            title = row["title"] or ""
            vtime = row["visit_time"]
            vduration = row["visit_duration"]

            if should_exclude(url, exclude_patterns):
                new_last_id = max(new_last_id, vid)
                continue

            dt = chrome_time_to_datetime(vtime)
            if dt is None:
                new_last_id = max(new_last_id, vid)
                continue

            duration_sec = (vduration // 1_000_000) if vduration and vduration > 0 else 0

            record = {
                "ts": dt.isoformat(),
                "type": "web_visit",
                "source": "chrome_collector",
                "data": {
                    "url": url,
                    "title": title,
                    "visit_duration_seconds": duration_sec,
                    "browser": "chrome",
                    "content_pending": True
                }
            }

            datafile = get_datafile(dt)
            if datafile not in records_by_file:
                records_by_file[datafile] = []
            records_by_file[datafile].append(record)
            new_last_id = max(new_last_id, vid)

        conn.close()

        # Write records grouped by date file
        for datafile, records in records_by_file.items():
            with open(datafile, "a") as f:
                for record in records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # Update high-water mark
        config["chrome_last_visit_id"] = new_last_id
        save_config(config)

        if rows:
            print(f"[chrome] Collected {len(rows)} visits (last_id: {new_last_id})")

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    collect()
