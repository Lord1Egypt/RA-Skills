#!/usr/bin/env python3
"""Verify final PDF structure without importing a general-purpose PDF parser."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from plan_io import load_plan, page_map


MAX_OUTPUT_BYTES = 256 * 1024 * 1024


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    pages = page_map(plan)
    if not args.pdf.is_file():
        raise ValueError(f"PDF not found: {args.pdf}")
    if args.pdf.stat().st_size > MAX_OUTPUT_BYTES:
        raise ValueError("PDF exceeds 256 MiB safety limit")
    data = args.pdf.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise ValueError("invalid PDF signature")
    if b"%%EOF" not in data[-128:]:
        raise ValueError("PDF EOF marker missing")
    page_count = len(re.findall(rb"/Type\s*/Page\b", data))
    if page_count != len(pages):
        raise ValueError(f"PDF has {page_count} pages; plan declares {len(pages)}")
    boxes = re.findall(rb"/MediaBox\s*\[\s*0\s+0\s+([0-9.]+)\s+([0-9.]+)\s*\]", data)
    if len(boxes) != page_count or any(float(w) <= 0 or float(h) <= 0 for w, h in boxes):
        raise ValueError("PDF page dimensions are missing or invalid")
    assigned = [note for note in plan["notes"] if int(note.get("finger", 0)) in {1, 2, 3, 4, 5}]
    anchored = [note for note in assigned if all(key in note for key in ("page", "page_x", "page_y"))]
    if len(anchored) != len(assigned):
        raise ValueError(f"{len(assigned) - len(anchored)} assigned notes lack page coordinates")
    print(f"Verified {page_count} page(s), {len(assigned)} anchored fingering marks.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
