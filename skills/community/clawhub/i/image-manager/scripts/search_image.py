#!/usr/bin/env python3
"""Image Manager - Search images by tags, category, date, or keyword."""
import sys
import os
import json
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', '/home/admin/.openclaw/workspace'))
INDEX_FILE = WORKSPACE / 'media' / 'index.json'


def load_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"images": [], "version": 1}


def search(tags=None, category=None, date=None, keyword=None):
    index = load_index()
    results = index["images"]

    if tags:
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        tag_set = set(tags)
        results = [img for img in results if tag_set & set(img.get("tags", []))]

    if category:
        results = [img for img in results if img.get("category") == category]

    if date:
        results = [img for img in results if date in img.get("saved_at", "")]

    if keyword:
        kw = keyword.lower()
        results = [img for img in results if
                   kw in img.get("description", "").lower() or
                   any(kw in t.lower() for t in img.get("tags", []))]

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Search indexed images')
    parser.add_argument('--tags', '-t', help='Search by tags (comma-separated)')
    parser.add_argument('--category', '-c', help='Filter by category')
    parser.add_argument('--date', '-d', help='Filter by date (YYYY-MM-DD)')
    parser.add_argument('--keyword', '-k', help='Search by keyword in description/tags')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not any([args.tags, args.category, args.date, args.keyword]):
        print("Usage: python search_image.py --tags '包子' --category pets --date 2026-03-19 --keyword '白色'")
        sys.exit(0)

    results = search(args.tags, args.category, args.date, args.keyword)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("没有找到匹配的图片。")
        else:
            print(f"找到 {len(results)} 张图片：\n")
            for img in results:
                tags_str = ', '.join(img.get('tags', []))
                print(f"  📷 {img['id']}")
                print(f"     类别: {img['category']} | 标签: {tags_str}")
                print(f"     描述: {img.get('description', '无')}")
                print(f"     路径: {img['path']}")
                print(f"     时间: {img['saved_at']}")
                print()
