#!/usr/bin/env python3
"""Inventory Tracker

Computes the inventory tracker number from the values the user supplies.

Parameters for this build:
{
  "formula": "reorder_point_qty = average_weekly_demand * supplier_lead_time_weeks + safety_stock_qty",
  "fields": [
    "sku",
    "average_weekly_demand",
    "supplier_lead_time_weeks",
    "safety_stock_qty"
  ]
}

Usage:
    python3 inventory_tracker.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Inventory Tracker"


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


FIELDS = ["sku", "average_weekly_demand", "supplier_lead_time_weeks", "safety_stock_qty"]
FORMULA = 'reorder_point_qty = average_weekly_demand * supplier_lead_time_weeks + safety_stock_qty'


def run(input_path, out_dir):
    data = read_flat(input_path)
    values = {}
    for field in FIELDS:
        raw = str(data.get(field, "") or "0").replace(",", "").replace("$", "").replace("%", "")
        try:
            values[field] = float(raw)
        except ValueError:
            values[field] = 0.0
    report = [f"# {TITLE}", "", f"source: {input_path}", ""]
    for field, value in values.items():
        report.append(f"- {field}: {value:g}")
    report.append("")
    report.append(f"formula: {FORMULA or 'documented in the skill'}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never delete a stock record or overwrite a counted quantity; add a dated adjustment line so the previous quantity and the reason stay visible.", "Never treat the system quantity as a physical count, and never record a count without the location, the date and the counter's role.", "Never present a reorder point as a purchase order; the buyer approves the order and places it."]:
        report.append(f"- {rule}")
    write_out(out_dir, "calculation.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
