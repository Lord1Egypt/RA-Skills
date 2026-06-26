#!/usr/bin/env python3
"""
update_tracking.py — Deduplicate job URLs against a rolling tracking window.

Usage:
    python3 update_tracking.py \
        --urls "url1,url2,url3" \
        --tracking-file PATH \
        --window-days N

Reads the tracking file (JSON array of {url, shared_date} objects).
Filters out any URL already seen within the past window-days days.
Prints the NEW (not-yet-seen) URLs as a JSON array to stdout.
Appends the new URLs (with today's date) to the tracking file.

Exits 0 always (errors printed to stderr, empty array returned on failure).
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional


def load_tracking(tracking_path: Path) -> list:
    """Load tracking records. Returns empty list if file missing or invalid."""
    if not tracking_path.exists():
        return []
    try:
        with tracking_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(
                f"Warning: tracking file is not a JSON array, resetting.",
                file=sys.stderr,
            )
            return []
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read tracking file: {e}", file=sys.stderr)
        return []


def save_tracking(tracking_path: Path, records: list) -> None:
    """Write tracking records to file, creating parent dirs as needed."""
    tracking_path.parent.mkdir(parents=True, exist_ok=True)
    with tracking_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def parse_date(date_str: str) -> Optional[date]:
    """Parse ISO date string (YYYY-MM-DD). Returns None on failure."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate job URLs against a rolling tracking window."
    )
    parser.add_argument(
        "--urls",
        required=True,
        help="Comma-separated list of job URLs to check",
    )
    parser.add_argument(
        "--tracking-file",
        required=True,
        help="Path to the JSON tracking file",
    )
    parser.add_argument(
        "--window-days",
        type=int,
        required=True,
        help="Number of days to look back when deduplicating",
    )
    args = parser.parse_args()

    tracking_path = Path(os.path.expanduser(args.tracking_file))
    today = date.today()
    cutoff = today - timedelta(days=args.window_days)

    # Parse incoming URLs (strip whitespace, drop empties)
    incoming_urls = [u.strip() for u in args.urls.split(",") if u.strip()]

    # Load existing tracking records
    records = load_tracking(tracking_path)

    # Build set of recently-seen URLs (within window)
    seen_recently = set()
    for record in records:
        url = record.get("url", "")
        shared = parse_date(record.get("shared_date", ""))
        if url and shared and shared >= cutoff:
            seen_recently.add(url)

    # Filter to new-only URLs
    new_urls = [u for u in incoming_urls if u not in seen_recently]

    # Append new URLs to tracking records with today's date
    today_str = today.isoformat()
    for url in new_urls:
        records.append({"url": url, "shared_date": today_str})

    # Persist updated tracking file
    try:
        save_tracking(tracking_path, records)
    except OSError as e:
        print(f"Warning: could not save tracking file: {e}", file=sys.stderr)

    # Output new URLs as JSON array
    print(json.dumps(new_urls))
    sys.exit(0)


if __name__ == "__main__":
    main()
