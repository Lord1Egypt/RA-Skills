#!/usr/bin/env python3
"""
producthunt.py — Product Hunt feed source.

Fetches trending Product Hunt posts via browser automation.
PH requires JavaScript (Cloudflare protection), so this module outputs
structured JSON instructions for the agent to execute via browser tool.

Usage:
    python3 scripts/feed/source/producthunt.py [--days 7] [--output /tmp/ph_feed.json]
"""

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config

_CFG = load_config()

DEFAULT_OUTPUT = str(_CFG["feed_dir"] / "ph_feed.json")


def home_instructions(days: int = 7) -> dict:
    return {
        "action": "scrape_producthunt_feed",
        "steps": [
            f"Navigate to https://www.producthunt.com",
            "Wait for the page to fully load (2-3s)",
            "Scroll down 3 times, waiting 2s between each scroll to load more posts",
            "For each visible post (up to 30), extract:",
            "  - Product name",
            "  - Tagline / description",
            "  - Number of upvotes",
            "  - Number of comments",
            "  - Category / topic tags",
            "  - Product URL",
            "  - Date posted",
            f"Filter to posts from the last {days} days only",
            "Deduplicate by product URL",
            f"Output JSON to: {DEFAULT_OUTPUT}",
        ],
        "output_schema": {
            "items": [
                {
                    "source": "producthunt",
                    "author": "<maker name or '@producthunt' if no maker>",
                    "name": "product name",
                    "text": "tagline or short description",
                    "url": "product website URL",
                    "ph_url": "https://www.producthunt.com/posts/<slug>",
                    "topics": ["category tag(s) from PH"],
                    "upvotes": "integer",
                    "comments": "integer",
                    "date": "YYYY-MM-DD or relative string",
                    "made_on": "what the product is made/running on (e.g. 'Web', 'iOS', 'macOS')",
                }
            ]
        },
        "topics": {
            "AI": ["ai", "gpt", "claude", "openai", "llm", "agent", "automation", "machine learning"],
            "Startups": ["startup", "founder", "saas", "b2b", "developer tools", "api"],
            "Productivity": ["productivity", "writing", "notes", "tasks", "calendar", "workflow"],
        },
        "output_file": DEFAULT_OUTPUT,
        "note": (
            "If Cloudflare blocks access, try: https://www.producthunt.com/tabs/best-of-month "
            "or search 'site:producthunt.com today' on Google and navigate to the results page."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Product Hunt feed — browser instructions")
    parser.add_argument(
        "--days", type=int, default=7,
        help="Only keep posts from the last N days (default: 7)",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output JSON path (agent saves results here)",
    )
    args = parser.parse_args()

    instructions = home_instructions(args.days)
    print(json.dumps(instructions, indent=2))


if __name__ == "__main__":
    main()
