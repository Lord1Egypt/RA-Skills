#!/usr/bin/env python3
"""Generate a table of contents for a Markdown file.

Usage:
    python3 generate_toc.py <file.md> [--max-depth N] [--in-place]
"""
import argparse
import re
import sys


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def parse_headings(lines, max_depth):
    headings = []
    seen = {}
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        level = len(m.group(1))
        if level > max_depth:
            continue
        title = m.group(2).strip()
        anchor = slugify(title)
        if anchor in seen:
            seen[anchor] += 1
            anchor = f"{anchor}-{seen[anchor]}"
        else:
            seen[anchor] = 0
        headings.append((level, title, anchor))
    return headings


def build_toc(headings):
    lines = []
    for level, title, anchor in headings:
        indent = "  " * (level - 1)
        lines.append(f"{indent}- [{title}](#{anchor})")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown TOC")
    parser.add_argument("file", help="Path to Markdown file")
    parser.add_argument("--max-depth", type=int, default=3, help="Max heading depth (1-6)")
    parser.add_argument("--in-place", action="store_true", help="Insert/update TOC in the file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")

    headings = parse_headings(lines, args.max_depth)
    if not headings:
        print("No headings found.", file=sys.stderr)
        sys.exit(1)

    toc = build_toc(headings)

    if not args.in_place:
        print(toc)
        return

    toc_block = f"<!-- toc -->\n{toc}\n<!-- /toc -->"

    # Replace existing toc block
    pattern = r"<!-- toc -->.*?<!-- /toc -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, toc_block, content, flags=re.DOTALL)
    else:
        # Insert after first heading
        idx = None
        for i, line in enumerate(lines):
            if re.match(r"^#\s+", line):
                idx = i + 1
                break
        if idx is None:
            idx = 0
        lines.insert(idx, "")
        lines.insert(idx + 1, toc_block)
        lines.insert(idx + 2, "")
        new_content = "\n".join(lines)

    with open(args.file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"TOC updated in {args.file}", file=sys.stderr)


if __name__ == "__main__":
    main()
