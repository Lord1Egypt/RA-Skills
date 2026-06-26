#!/usr/bin/env python3
"""
build_paste_doc.py — Generates a paste-ready beehiiv publish doc
from a finalized article file.

Usage:
    python3 build_paste_doc.py <article_file> <publish_date> [output_file]

    publish_date format: YYYY-MM-DD
    output_file: optional, defaults to <article_file stem>-PASTE.md

The script reads Meta Title, Meta Description, and URL Slug from
the article file header block, then prepends the paste-ready block.

Expected article header format (at top of file):
    Meta Title: Your Title Here
    Meta Description: Your description here.
    URL Slug: your-url-slug-here
    Primary Keyword: your keyword here
"""

import sys
import re
import os
from datetime import datetime

def extract_meta(content):
    meta = {}
    patterns = {
        'title':       r'(?i)^meta[_\s-]?title:\s*(.+)$',
        'description': r'(?i)^meta[_\s-]?description:\s*(.+)$',
        'slug':        r'(?i)^url[_\s-]?slug:\s*(.+)$',
        'keyword':     r'(?i)^primary[_\s-]?keyword:\s*(.+)$',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.MULTILINE)
        meta[key] = match.group(1).strip().strip('"\'') if match else None
    return meta

def build_paste_doc(article_path, publish_date, output_path=None):
    with open(article_path, 'r') as f:
        content = f.read()

    meta = extract_meta(content)

    missing = [k for k, v in meta.items() if v is None]
    if missing:
        print(f"⚠️  Missing fields in article header: {', '.join(missing)}")
        print("   Add them at the top of the file and re-run.")
        if 'title' in missing or 'description' in missing:
            sys.exit(1)

    # Validate lengths
    warnings = []
    if meta['title'] and len(meta['title']) > 60:
        warnings.append(f"Meta title is {len(meta['title'])} chars — trim to 60 max")
    if meta['description'] and len(meta['description']) > 160:
        warnings.append(f"Meta description is {len(meta['description'])} chars — trim to 160 max")

    # Format publish date
    try:
        dt = datetime.strptime(publish_date, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %-d, %Y')
    except ValueError:
        formatted_date = publish_date

    paste_block = f"""---
## 📋 BEEHIIV PASTE-READY BLOCK
**Publish Date:** {formatted_date}
**URL Slug:** {meta['slug'] or '⚠️ NOT SET — add URL Slug: line to article'}
**Meta Title:** {meta['title'] or '⚠️ NOT SET'}
**Meta Description:** {meta['description'] or '⚠️ NOT SET'}
**Primary Keyword:** {meta['keyword'] or '⚠️ NOT SET'}

### Steps to publish:
1. In beehiiv, create new post
2. Paste article body below the dashed line
3. Set URL slug exactly as shown above
4. Set meta title and description in SEO settings
5. Set publish date to {formatted_date}
6. Set visibility: **Web + Email** (not email-only)
---

"""

    output = paste_block + content

    if output_path is None:
        base = os.path.splitext(article_path)[0]
        output_path = f"{base}-PASTE.md"

    with open(output_path, 'w') as f:
        f.write(output)

    print(f"\n✅ Paste doc written to: {output_path}")
    if warnings:
        print("\n⚠️  Warnings:")
        for w in warnings:
            print(f"  • {w}")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 build_paste_doc.py <article_file> <publish_date> [output_file]")
        print("  publish_date: YYYY-MM-DD")
        sys.exit(1)
    output = sys.argv[3] if len(sys.argv) > 3 else None
    build_paste_doc(sys.argv[1], sys.argv[2], output)
