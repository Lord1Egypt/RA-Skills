#!/usr/bin/env python3
"""
search.py — search visual memories by keyword

Usage:
  python search.py --query "login dark mode" [--limit 10]
"""

import argparse
import json
import os
import sqlite3

DB_PATH = os.path.expanduser("~/.multimodal-memory/metadata.db")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if not os.path.isfile(DB_PATH):
        print("No memories stored yet.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Split query into terms for broader matching
    terms = [t.strip() for t in args.query.split() if t.strip()]
    if not terms:
        print("Empty query.")
        return

    # Build WHERE clause: match any term in description OR tags
    clauses = []
    params = []
    for term in terms:
        clauses.append("(description LIKE ? OR tags LIKE ? OR url LIKE ?)")
        params += [f"%{term}%", f"%{term}%", f"%{term}%"]

    where = " OR ".join(clauses)
    rows = conn.execute(
        f"SELECT * FROM memories WHERE {where} ORDER BY created_at DESC LIMIT ?",
        params + [args.limit],
    ).fetchall()
    conn.close()

    if not rows:
        print(f"No memories found for: {args.query}")
        return

    print(f"Found {len(rows)} result(s) for '{args.query}':\n")
    for r in rows:
        tags = ", ".join(json.loads(r["tags"])) if r["tags"] else ""
        url_part = f"\n  URL         : {r['url']}" if r["url"] else ""
        img_part = f"\n  Image       : {r['image_path']}" if r["image_path"] else ""
        exists = ""
        if r["image_path"] and not os.path.isfile(r["image_path"]):
            exists = " [file missing]"

        print(f"[{r['id']}] {r['created_at']} — {r['source_type']}")
        print(f"  Description : {r['description']}")
        if tags:
            print(f"  Tags        : {tags}")
        if r["url"]:
            print(f"  URL         : {r['url']}")
        if r["image_path"]:
            print(f"  Image       : {r['image_path']}{exists}")
        print()


if __name__ == "__main__":
    main()
