#!/usr/bin/env python3
"""CLI for searching and querying the image vault."""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from image_db import get_db, init_db, search_images, get_all_categories, get_all_tags, get_stats


def main():
    parser = argparse.ArgumentParser(description="Search the image vault")
    sub = parser.add_subparsers(dest="cmd")

    sp_search = sub.add_parser("search", help="Search images")
    sp_search.add_argument("query", nargs="?", help="Search keyword")
    sp_search.add_argument("--category", "-c", help="Filter by category")
    sp_search.add_argument("--source", "-s", help="Filter by source")
    sp_search.add_argument("--from", dest="date_from", help="Date from (YYYY-MM-DD)")
    sp_search.add_argument("--to", dest="date_to", help="Date to (YYYY-MM-DD)")
    sp_search.add_argument("--tags", "-t", help="Comma-separated tags")
    sp_search.add_argument("--limit", "-l", type=int, default=50)
    sp_search.add_argument("--json", action="store_true", help="Output JSON")

    sub.add_parser("categories", help="List all categories")
    sub.add_parser("tags", help="List all tags")
    sub.add_parser("stats", help="Show vault statistics")

    args = parser.parse_args()
    init_db()
    conn = get_db()

    if args.cmd == "search":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        results = search_images(
            conn, query=args.query, category=args.category, source=args.source,
            date_from=args.date_from, date_to=args.date_to, tags=tags, limit=args.limit,
        )
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"Found {len(results)} image(s):\n")
            for img in results:
                tags_str = ", ".join(json.loads(img.get("tags", "[]"))) if img.get("tags") else ""
                print(f"  [{img['id']}] {img['filename']}")
                print(f"      Category: {img['category']} | Source: {img['source']}")
                if img.get("description"):
                    print(f"      Desc: {img['description'][:80]}")
                if tags_str:
                    print(f"      Tags: {tags_str}")
                print(f"      Path: {img['vault_path']}")
                print()

    elif args.cmd == "categories":
        cats = get_all_categories(conn)
        print("Categories:", ", ".join(cats) if cats else "(none)")

    elif args.cmd == "tags":
        tags = get_all_tags(conn)
        print("Tags:", ", ".join(tags) if tags else "(none)")

    elif args.cmd == "stats":
        stats = get_stats(conn)
        print(f"Total images: {stats['total']}")
        print("By category:")
        for cat, count in stats["categories"].items():
            print(f"  {cat}: {count}")
        print("By source:")
        for src, count in stats["sources"].items():
            print(f"  {src}: {count}")

    else:
        parser.print_help()

    conn.close()


if __name__ == "__main__":
    main()
