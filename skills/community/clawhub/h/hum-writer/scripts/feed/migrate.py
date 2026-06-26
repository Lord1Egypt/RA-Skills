#!/usr/bin/env python3
"""
migrate.py — One-shot migration to normalize feeds.json to the canonical FeedItem schema.

Rewrites feeds.json in-place, converting:
  - text / summary → content
  - is_thread_start / is_article / type → post_type
  - engagement.{likes,views,comments} → flat likes/views/replies
  - timestamp / date / scraped_at / published → timestamp

Safe to run multiple times (idempotent).

Usage:
    python3 scripts/feed/migrate.py
    python3 scripts/feed/migrate.py --input /path/to/feeds.json
"""
import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.schema import normalize_item

_CFG = load_config()


def migrate_feeds(feeds_path: Path) -> tuple[int, int]:
    """Normalize all items in feeds.json. Returns (total, changed) counts."""
    if not feeds_path.exists():
        print(f"[migrate] No file at {feeds_path} — nothing to do.")
        return 0, 0

    raw = feeds_path.read_text(encoding="utf-8")
    items: list[dict] = json.loads(raw)
    if not isinstance(items, list):
        print(f"[migrate] Unexpected format in {feeds_path} — skipping.")
        return 0, 0

    normalized = [normalize_item(item) for item in items]

    # Count how many actually changed
    changed = sum(1 for old, new in zip(items, normalized) if old != new)

    feeds_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(normalized), changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate feeds.json to unified FeedItem schema")
    parser.add_argument("--input", default=str(_CFG["feeds_file"]), help="Path to feeds.json")
    args = parser.parse_args()

    feeds_path = Path(args.input)
    print(f"[migrate] Normalizing {feeds_path}…")
    total, changed = migrate_feeds(feeds_path)
    print(f"[migrate] Done — {total} items, {changed} updated.")


if __name__ == "__main__":
    main()
