#!/usr/bin/env python3
"""Convert a JSON file into a Markdown table or report.

Usage:
    python json_to_md.py <input.json> [--title "Report Title"] [--out report.md]

Supported input shapes:
    - A top-level array of flat objects  -> one Markdown table
    - A top-level object whose values are arrays -> one table per key
    - A single flat object               -> a two-column key/value table
"""

import json
import sys


def escape_cell(value):
    """Make a value safe to embed in a Markdown table cell."""
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def table_from_records(records):
    """Build a GitHub-style Markdown table from a list of flat objects."""
    if not records:
        return "_No records._"
    keys = []
    for record in records:
        if isinstance(record, dict):
            for key in record:
                if key not in keys:
                    keys.append(key)
    if not keys:
        return "_No columns found._"
    header = "| " + " | ".join(escape_cell(k) for k in keys) + " |"
    separator = "|" + "|".join(" --- " for _ in keys) + "|"
    rows = []
    for record in records:
        if isinstance(record, dict):
            rows.append(
                "| " + " | ".join(escape_cell(record.get(k)) for k in keys) + " |"
            )
        else:
            rows.append("| " + escape_cell(record) + " |")
    return "\n".join([header, separator] + rows)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    path = args[0]
    title = "JSON Report"
    out_path = None

    i = 1
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        else:
            i += 1

    with open(path, "r", encoding="utf-8-sig") as fh:
        data = json.load(fh)

    parts = [f"# {title}", ""]

    if isinstance(data, list):
        parts.append(table_from_records(data))
    elif isinstance(data, dict):
        array_values = {k: v for k, v in data.items() if isinstance(v, list)}
        if array_values:
            for key, records in array_values.items():
                parts.append(f"## {key}")
                parts.append("")
                parts.append(table_from_records(records))
                parts.append("")
        else:
            parts.append("| Key | Value |")
            parts.append("| --- | --- |")
            for key, value in data.items():
                parts.append(f"| {escape_cell(key)} | {escape_cell(value)} |")
    else:
        parts.append("```json")
        parts.append(json.dumps(data, indent=2, ensure_ascii=False))
        parts.append("```")

    output = "\n".join(parts) + "\n"

    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(output)
        print(f"Wrote {out_path}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
