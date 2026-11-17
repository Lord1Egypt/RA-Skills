#!/usr/bin/env python3
"""HVAC Quote Generator

Builds a line-item estimate with tax and margin for hvac quote generator.

Parameters for this build:
{
  "tax_rate": 0.07,
  "margin_pct": 0.35,
  "currency": "USD"
}

Usage:
    python3 hvac_quote_generator.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "HVAC Quote Generator"


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


TAX_RATE = 0.07
MARGIN = 0.35
CURRENCY = 'USD'


def run(input_path, out_dir):
    rows = read_csv(input_path)
    report = [f"# {TITLE} estimate", "", f"source: {input_path}", f"currency: {CURRENCY}", f"tax rate: {TAX_RATE}", f"target margin: {MARGIN}", ""]
    subtotal = 0.0
    for row in rows:
        try:
            amount = float(str(row.get("amount", "0") or "0").replace(",", "").replace("$", ""))
        except ValueError:
            amount = 0.0
        subtotal += amount
        report.append(f"- {row.get('item', 'line item')}: {amount:,.2f} {CURRENCY}")
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    report.append("")
    report.append(f"subtotal: {subtotal:,.2f} {CURRENCY}")
    report.append(f"tax: {tax:,.2f} {CURRENCY}")
    report.append(f"total: {total:,.2f} {CURRENCY}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never invent a price, an efficiency rating, a rebate, a discount or a tax rate; leave them as fields the user fills in.", "Never promise a savings percentage, a payback period or a monthly utility cost without the customer's own utility data.", "Never claim a manufacturer certification, a utility rebate or a warranty the contractor has not confirmed in writing."]:
        report.append(f"- {rule}")
    write_out(out_dir, "estimate.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
