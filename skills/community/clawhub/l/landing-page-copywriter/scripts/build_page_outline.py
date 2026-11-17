#!/usr/bin/env python3
"""Landing Page Copywriter

Builds a content outline for landing page copywriter from a keyword list.

Parameters for this build:
{
  "word_target": 800
}

Usage:
    python3 landing_page_copywriter.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Landing Page Copywriter"


def read_flat(path):
    """Read a small YAML-ish file: `key: value`, `- item` lists, '#' comments."""
    data, key = {}, None
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}")
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" in stripped:
            name, _, value = stripped.partition(":")
            name, value = name.strip(), value.strip().strip('"').strip("'")
            if value == "":
                data[name] = []
                key = name
            else:
                data[name] = value
                key = None
    return data


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_out(out_dir, name, lines):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {path}")
    return path


WORD_TARGET = 800


def run(input_path, out_dir):
    data = read_flat(input_path)
    keywords = data.get("keywords") or []
    if isinstance(keywords, str):
        keywords = [item.strip() for item in keywords.split(",") if item.strip()]
    report = [f"# {TITLE} outline", "", f"source: {input_path}", "", f"target words: {WORD_TARGET}", f"keywords: {len(keywords)}", ""]
    for index, keyword in enumerate(keywords, 1):
        share = max(80, WORD_TARGET // max(len(keywords), 1))
        report.append(f"## {index}. {keyword}")
        report.append(f"- section target: {share} words")
        report.append("- answer the query in the first 40 words")
        report.append("- add one example and one US-specific detail")
        report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never invent a testimonial, a review count, a star rating or a customer name.", "Never state a total price, a fee or a guarantee that the client's actual policy does not support.", "Never use fake countdown timers, fake stock counts or fake recent-activity notices."]:
        report.append(f"- {rule}")
    write_out(out_dir, "outline.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
