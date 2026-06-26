#!/usr/bin/env python3
"""
parse_opml.py — Parse an OPML file and output a JSON list of feed metadata.

Usage:
    python3 parse_opml.py <opml_file>

Output (stdout): JSON array of objects with keys: title, xmlUrl, htmlUrl, category
"""

import sys
import json
import xml.etree.ElementTree as ET


def parse_opml(path: str) -> list[dict]:
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"[parse_opml] XML parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"[parse_opml] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    root = tree.getroot()
    feeds = []

    def walk(node, category=None):
        for outline in node.findall("outline"):
            xml_url = outline.get("xmlUrl", "").strip()
            title = (
                outline.get("title")
                or outline.get("text")
                or outline.get("xmlUrl", "")
            ).strip()
            html_url = outline.get("htmlUrl", "").strip()
            cat = outline.get("category", category or "").strip()

            if xml_url:
                feeds.append(
                    {
                        "title": title,
                        "xmlUrl": xml_url,
                        "htmlUrl": html_url,
                        "category": cat,
                    }
                )
            else:
                # It's a folder/category — recurse with category name
                folder_name = (outline.get("title") or outline.get("text", "")).strip()
                walk(outline, folder_name or category)

    body = root.find("body")
    if body is None:
        print("[parse_opml] No <body> element found in OPML.", file=sys.stderr)
        sys.exit(1)

    walk(body)
    return feeds


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <opml_file>", file=sys.stderr)
        sys.exit(1)

    feeds = parse_opml(sys.argv[1])
    print(json.dumps(feeds, indent=2))
    print(f"[parse_opml] Found {len(feeds)} feed(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
