#!/usr/bin/env python3
"""Extract figure image URLs from an academic HTML paper.

Usage:
    python extract_figure_urls.py <html_path> <base_url>

- html_path: path to the downloaded HTML file
- base_url: the original HTML page URL (used to resolve relative image paths)

Output: prints each figure's index, resolved URL, and caption to stdout.
Also reports any inline SVG figures that have no downloadable image URL.
"""

import sys
import os
import re
from urllib.parse import urljoin


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <html_path> <base_url>", file=sys.stderr)
        sys.exit(1)

    html_path = sys.argv[1]
    # urljoin semantics: if base does NOT end with '/', it treats the last segment
    # as a file and resolves relative paths against its parent directory.
    # e.g. urljoin("https://arxiv.org/html/2605.29209", "2605.29209v1/x1.png")
    #   -> "https://arxiv.org/html/2605.29209v1/x1.png"  (correct)
    # Do NOT append '/' to the base URL — that would make urljoin treat the ID
    # as a directory, producing wrong paths.
    base_url = sys.argv[2]

    if not os.path.isfile(html_path):
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract all <figure> blocks
    figure_blocks = re.findall(r'<figure[^>]*>.*?</figure>', html, re.DOTALL | re.IGNORECASE)

    downloadable = []
    inline_svg = []

    for i, block in enumerate(figure_blocks):
        fig_idx = i + 1

        # Extract caption
        cap_match = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', block, re.DOTALL | re.IGNORECASE)
        caption = re.sub(r'<[^>]+>', '', cap_match.group(1)).strip()[:120] if cap_match else ''

        # Look for <img> tags
        srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', block, re.IGNORECASE)
        img_urls = []
        for src in srcs:
            if src.startswith('data:'):
                continue
            full_url = urljoin(base_url, src)
            img_urls.append(full_url)

        if img_urls:
            for url in img_urls:
                downloadable.append((fig_idx, url, caption))
        else:
            # Check if it contains inline SVG
            has_svg = bool(re.search(r'<svg[^>]*>', block, re.IGNORECASE))
            if has_svg:
                inline_svg.append((fig_idx, caption))

    # Output downloadable figures
    print(f"=== Downloadable figures: {len(downloadable)} ===")
    for idx, url, cap in downloadable:
        print(f"  [Figure {idx}] {url}")
        if cap:
            print(f"    Caption: {cap}")

    # Output inline SVG warnings
    if inline_svg:
        print(f"\n=== Inline SVG figures (no download URL, need SVG-to-PNG conversion): {len(inline_svg)} ===")
        for idx, cap in inline_svg:
            print(f"  [Figure {idx}] INLINE SVG")
            if cap:
                print(f"    Caption: {cap}")

    # Summary
    total = len(downloadable) + len(inline_svg)
    print(f"\nTotal figures: {total} ({len(downloadable)} downloadable, {len(inline_svg)} inline SVG)")


if __name__ == "__main__":
    main()
