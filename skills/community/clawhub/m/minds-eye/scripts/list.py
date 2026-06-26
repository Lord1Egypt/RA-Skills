#!/usr/bin/env python3
"""
list.py — list recent visual memories

Usage:
  python list.py [--limit 20]
"""

import argparse
import json
import os
import sqlite3

DB_PATH = os.path.expanduser("~/.multimodal-memory/metadata.db")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if not os.path.isfile(DB_PATH):
        print("No memories stored yet.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?", (args.limit,)
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()

    if not rows:
        print("No memories stored yet.")
        return

    print(f"Showing {len(rows)} of {total} total memories:\n")
    for r in rows:
        tags = ", ".join(json.loads(r["tags"])) if r["tags"] else "—"
        url_part = f" | {r['url']}" if r["url"] else ""
        print(f"[{r['id']}] {r['created_at']} — {r['source_type']}{url_part}")
        print(f"  {r['description'][:160]}")
        print(f"  Tags: {tags}")
        if r["image_path"]:
            exists = "" if os.path.isfile(r["image_path"]) else " [missing]"
            print(f"  Image: {r['image_path']}{exists}")
        print()


if __name__ == "__main__":
    main()
