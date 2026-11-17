#!/usr/bin/env python3
"""Read a CSV keeping each record's true physical START line in the file.

Standard library only. Generated skills may import `read_with_lines` or copy
it. Line numbers are physical lines of the original file: the header is line 1
(base "file") or the first data record is 1 (base "data"). A record whose
quoted cell spans several lines is numbered by the line where it STARTS, blank
lines still consume physical lines, and numbers never come from the position
after de-duplication, sorting or grouping.

    python -B scripts/csv_source_lines.py input.csv [--base file|data]

prints JSON: [{"line": 2, "row": {...}}, ...]. Exit 2 on unreadable input.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path


def read_with_lines(text: str, base: str = "file"):
    """Return (header, [(start_line, dict_row), ...]) from CSV text."""
    if base not in {"file", "data"}:
        raise ValueError("base must be 'file' or 'data'")
    reader = csv.reader(io.StringIO(text, newline=""))
    header = next(reader, None)
    if not header:
        raise ValueError("empty CSV")
    records, previous, ordinal = [], reader.line_num, 0
    for cells in reader:
        start, previous = previous + 1, reader.line_num   # start of this record
        if not cells:                                     # blank physical line
            continue
        ordinal += 1
        if len(cells) != len(header):
            raise ValueError(f"record starting at line {start} has {len(cells)} cells, expected {len(header)}")
        records.append((start if base == "file" else ordinal, dict(zip(header, cells))))
    return header, records


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--base", choices=["file", "data"], default="file")
    args = parser.parse_args()
    try:
        _, records = read_with_lines(args.path.read_bytes().decode("utf-8-sig"), args.base)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps([{"line": line, "row": row} for line, row in records], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
