#!/usr/bin/env python3
"""Image Manager - List and browse images."""
import sys
import os
import json
from pathlib import Path
from collections import Counter

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', '/home/admin/.openclaw/workspace'))
INDEX_FILE = WORKSPACE / 'media' / 'index.json'


def load_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"images": [], "version": 1}


def list_images(category=None, tags=None, limit=50):
    index = load_index()
    images = index["images"]

    if category:
        images = [img for img in images if img.get("category") == category]

    if tags:
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        tag_set = set(tags)
        images = [img for img in images if tag_set & set(img.get("tags", []))]

    # Sort by date, newest first
    images.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
    return images[:limit]


def show_stats():
    index = load_index()
    images = index["images"]

    print(f"📊 图片库统计")
    print(f"   总数: {len(images)} 张")
    print()

    # By category
    cats = Counter(img.get("category", "other") for img in images)
    print("📁 按类别:")
    for cat, count in cats.most_common():
        print(f"   {cat}: {count} 张")
    print()

    # By tag
    all_tags = []
    for img in images:
        all_tags.extend(img.get("tags", []))
    tag_counts = Counter(all_tags)
    print("🏷️ 热门标签:")
    for tag, count in tag_counts.most_common(10):
        print(f"   {tag}: {count} 张")

    total_size = sum(img.get("size_bytes", 0) for img in images)
    print(f"\n💾 总大小: {total_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='List indexed images')
    parser.add_argument('--category', '-c', help='Filter by category')
    parser.add_argument('--tags', '-t', help='Filter by tags')
    parser.add_argument('--limit', '-n', type=int, default=50, help='Max results')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if args.stats:
        show_stats()
        sys.exit(0)

    results = list_images(args.category, args.tags, args.limit)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif not results:
        print("图片库为空。用 save_image.py 添加图片。")
    else:
        print(f"📷 图片列表（{len(results)} 张）：\n")
        for img in results:
            tags_str = ', '.join(img.get('tags', []))
            desc = img.get('description', '')[:40]
            print(f"  [{img['category']}] {img['id']}")
            print(f"     {tags_str} | {desc}")
            print(f"     {img['saved_at'][:16]}")
            print()
