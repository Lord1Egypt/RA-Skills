#!/usr/bin/env python3
"""
create_pipeline_db.py — Create a Content Pipeline Notion database.

Creates a database with columns: Title, Platform, Status, Hook, Est. Read Time,
Published URL, Source, Sprint (or any custom tag column).

Configuration:
  NOTION_API_KEY          Notion integration token (required)
  NOTION_PARENT_PAGE_ID   Parent page ID to create the DB under (required)

Usage:
  python3 create_pipeline_db.py
  python3 create_pipeline_db.py --parent-id <page-id>
  python3 create_pipeline_db.py --seed-file seeds.json  # Optional: seed with initial items
"""
from __future__ import annotations

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"


def get_key() -> str:
    key = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_KEY")
    if key:
        return key
    raise RuntimeError("Set NOTION_API_KEY env var. Get one at https://www.notion.so/my-integrations")


def get_parent_id(override: str | None) -> str:
    page_id = override or os.environ.get("NOTION_PARENT_PAGE_ID")
    if not page_id:
        raise RuntimeError("Set NOTION_PARENT_PAGE_ID env var or pass --parent-id")
    return page_id


def headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def create_database(key: str, parent_page_id: str, db_title: str = "Content Pipeline") -> str:
    """Create the Content Pipeline database. Returns its ID."""
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": "✍️"},
        "title": [{"type": "text", "text": {"content": db_title}}],
        "properties": {
            "Title": {"title": {}},
            "Platform": {
                "select": {
                    "options": [
                        {"name": "Blog", "color": "blue"},
                        {"name": "LinkedIn", "color": "green"},
                        {"name": "Both", "color": "purple"},
                        {"name": "Newsletter", "color": "orange"},
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Seed", "color": "gray"},
                        {"name": "Draft", "color": "yellow"},
                        {"name": "Humanized", "color": "orange"},
                        {"name": "In Review", "color": "blue"},
                        {"name": "Published", "color": "green"},
                    ]
                }
            },
            "Source": {"rich_text": {}},
            "Hook": {"rich_text": {}},
            "Est. Read Time": {
                "select": {
                    "options": [
                        {"name": "< 1 min", "color": "green"},
                        {"name": "2-3 min", "color": "blue"},
                        {"name": "5-7 min", "color": "yellow"},
                        {"name": "10+ min", "color": "red"},
                    ]
                }
            },
            "Published URL": {"url": {}},
            "Tags": {"rich_text": {}},
        },
    }
    r = requests.post(f"{NOTION_API}/databases", headers=headers(key), json=payload)
    if r.status_code != 200:
        print(f"ERROR creating database: {r.status_code}: {r.text[:300]}", file=sys.stderr)
        sys.exit(1)
    db_id = r.json()["id"]
    print(f"✓ Created '{db_title}' database: {db_id}")
    return db_id


def add_page(key: str, db_id: str, title: str, platform: str = "Blog",
             status: str = "Seed", source: str = "", hook: str = "",
             read_time: str = "5-7 min", tags: str = "") -> str | None:
    """Add a page to the pipeline database."""
    payload = {
        "parent": {"database_id": db_id},
        "icon": {"type": "emoji", "emoji": "📝" if platform != "LinkedIn" else "💼"},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Platform": {"select": {"name": platform}},
            "Status": {"select": {"name": status}},
            "Source": {"rich_text": [{"text": {"content": source}}]},
            "Hook": {"rich_text": [{"text": {"content": hook}}]},
            "Est. Read Time": {"select": {"name": read_time}},
            "Tags": {"rich_text": [{"text": {"content": tags}}]},
        },
    }
    r = requests.post(f"{NOTION_API}/pages", headers=headers(key), json=payload)
    if r.status_code != 200:
        print(f"  ERROR adding '{title[:40]}': {r.status_code}: {r.text[:200]}", file=sys.stderr)
        return None
    page_id = r.json()["id"]
    print(f"  ✓ [{platform:10s}] [{status}] {title[:60]}")
    return page_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Notion Content Pipeline database")
    parser.add_argument("--parent-id", help="Override NOTION_PARENT_PAGE_ID")
    parser.add_argument("--title", default="Content Pipeline", help="Database title")
    parser.add_argument("--seed-file",
                        help="Path to JSON file with array of {title, platform, status, source, hook, read_time} items to seed")
    args = parser.parse_args()

    key = get_key()
    parent_id = get_parent_id(args.parent_id)

    print(f"=== Creating '{args.title}' database ===")
    db_id = create_database(key, parent_id, args.title)

    if args.seed_file:
        seeds = json.loads(open(args.seed_file).read())
        print(f"\n=== Seeding {len(seeds)} items ===")
        for seed in seeds:
            add_page(
                key=key,
                db_id=db_id,
                title=seed.get("title", "Untitled"),
                platform=seed.get("platform", "Blog"),
                status=seed.get("status", "Seed"),
                source=seed.get("source", ""),
                hook=seed.get("hook", ""),
                read_time=seed.get("read_time", "5-7 min"),
                tags=seed.get("tags", ""),
            )

    print(f"\n✅ Done. Database ID: {db_id}")
    print(f"   Set NOTION_PIPELINE_DB_ID={db_id} in your env to use it in other scripts.")


if __name__ == "__main__":
    main()
