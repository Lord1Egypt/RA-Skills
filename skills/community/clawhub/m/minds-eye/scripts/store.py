#!/usr/bin/env python3
"""
store.py — save a visual memory to ~/.multimodal-memory/

Usage:
  python store.py --description TEXT --tags tag1,tag2 \
                  [--image-path PATH] [--source image|chart|website] [--url URL]
"""

import argparse
import json
import os
import shutil
import sqlite3
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.multimodal-memory")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
DB_PATH = os.path.join(DATA_DIR, "metadata.db")
MEMORY_MD = os.path.join(DATA_DIR, "memory.md")


def init():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path  TEXT,
            description TEXT    NOT NULL,
            tags        TEXT    NOT NULL DEFAULT '[]',
            source_type TEXT    NOT NULL DEFAULT 'image',
            url         TEXT,
            created_at  TEXT    NOT NULL
        )
    """)
    conn.commit()
    return conn


def copy_image(src: str) -> str:
    """Copy image into the managed images dir and return new absolute path."""
    if not src or not os.path.isfile(src):
        return src
    filename = os.path.basename(src)
    dst = os.path.join(IMAGES_DIR, filename)
    # Avoid overwriting by adding timestamp suffix if needed
    if os.path.exists(dst) and dst != os.path.abspath(src):
        name, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dst = os.path.join(IMAGES_DIR, f"{name}_{ts}{ext}")
    if os.path.abspath(src) != dst:
        shutil.copy2(src, dst)
    return dst


def update_memory_md(conn: sqlite3.Connection):
    """Write a human-readable summary of the latest 30 memories to memory.md."""
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM memories ORDER BY created_at DESC LIMIT 30"
    ).fetchall()

    lines = [
        "# Multimodal Memory — Recent Entries\n",
        f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n",
        f"_Total stored: {conn.execute('SELECT COUNT(*) FROM memories').fetchone()[0]}_\n\n",
    ]
    for r in rows:
        tags = ", ".join(json.loads(r["tags"])) if r["tags"] else ""
        url_part = f" | {r['url']}" if r["url"] else ""
        lines.append(f"## [{r['id']}] {r['created_at']} — {r['source_type']}{url_part}\n")
        lines.append(f"**Description:** {r['description']}\n")
        if tags:
            lines.append(f"**Tags:** {tags}\n")
        if r["image_path"]:
            lines.append(f"**Image:** {r['image_path']}\n")
        lines.append("\n")

    with open(MEMORY_MD, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--description", required=True)
    parser.add_argument("--tags", default="")
    parser.add_argument("--image-path", default="")
    parser.add_argument("--source", default="image", choices=["image", "chart", "website"])
    parser.add_argument("--url", default="")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    conn = init()

    saved_path = copy_image(args.image_path) if args.image_path else None

    cur = conn.execute(
        """
        INSERT INTO memories (image_path, description, tags, source_type, url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            saved_path,
            args.description,
            json.dumps(tags),
            args.source,
            args.url or None,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    record_id = cur.lastrowid

    update_memory_md(conn)
    conn.close()

    print(f"Saved memory id={record_id}")
    print(f"  Source      : {args.source}")
    if saved_path:
        print(f"  Image       : {saved_path}")
    if args.url:
        print(f"  URL         : {args.url}")
    print(f"  Tags        : {', '.join(tags)}")
    print(f"  Description : {args.description[:200]}")


if __name__ == "__main__":
    main()
