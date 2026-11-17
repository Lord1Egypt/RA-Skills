#!/usr/bin/env python3
"""Pricing Presentation

Builds tracked links for pricing presentation.

Parameters for this build:
{
  "base": "https://yourco.com/pricing",
  "utm_source": "pricing-deck"
}

Usage:
    python3 pricing_presentation.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Pricing Presentation"


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


BASE = 'https://yourco.com/pricing'
UTM_SOURCE = 'pricing-deck'


def run(input_path, out_dir):
    rows = read_csv(input_path)
    report = [f"# {TITLE} tracked links", "", f"base: {BASE}", f"source: {UTM_SOURCE}", ""]
    for row in rows:
        slug = str(row.get("slug") or row.get("url") or "").strip()
        if not slug:
            continue
        campaign = str(row.get("campaign") or "default").strip()
        medium = str(row.get("medium") or "referral").strip()
        link = f"{BASE.rstrip('/')}/{slug.lstrip('/')}?utm_source={UTM_SOURCE}&utm_medium={medium}&utm_campaign={campaign}"
        report.append(f"- {link}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never show a price that is not the price the buyer will be charged.", "Never publish a savings claim without the baseline price and the period it was measured over.", "Never present a competitor's price without a like-for-like comparison."]:
        report.append(f"- {rule}")
    write_out(out_dir, "tracked-links.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
