#!/usr/bin/env python3
"""
Reconstruct per-page source text from elements JSON (bypasses markdown truncation).

Usage:
  python build_page_text.py --elements recognition.json --page 16 [--output out.txt]

Output:
  Plain text reconstruction of the page, formatted as the per-page markdown file would be:
  - heading elements get "## " prefix
  - non-heading elements passed through as-is
  - elements separated by "\n\n"

Triggers: when a per-page markdown file contains "[truncated]" or an unclosed <table>,
the translation pipeline should fall back to this JSON reconstruction.
"""

import json, sys, argparse
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


def build_page_text(elements_data: dict, page_number: int) -> str:
    """Reconstruct page text from elements JSON."""
    pages = elements_data.get("pages", [])
    target = None
    for p in pages:
        if p["page_number"] == page_number:
            target = p
            break

    if target is None:
        raise ValueError(f"Page {page_number} not found in elements JSON")

    elems = sorted(target["elements"], key=lambda e: e.get("reading_order", 0))
    lines = []
    for el in elems:
        text = el["text"]
        label = el["label"]
        if label in ("sec", "sub_sec", "sub_sub_sec"):
            lines.append(f"## {text}")
        else:
            lines.append(text)

    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Reconstruct page text from elements JSON")
    parser.add_argument("--elements", required=True, help="PaddleOCR recognition JSON path")
    parser.add_argument("--page", type=int, required=True, help="Page number to reconstruct")
    parser.add_argument("--output", default=None, help="Optional output file path (default: stdout)")
    args = parser.parse_args()

    with open(args.elements, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    text = build_page_text(data, args.page)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
