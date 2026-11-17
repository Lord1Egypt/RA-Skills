#!/usr/bin/env python3
"""Med Spa Treatment Descriptions

Builds a structured treatment-brief from a brief and checks every field against its limit.

Parameters for this build:
{
  "fields": [
    "treatment_page",
    "status_block",
    "claim_checks",
    "consent_notes"
  ],
  "limits": {
    "treatment_page": 2200,
    "status_block": 400,
    "claim_checks": 600,
    "consent_notes": 400
  },
  "output": "treatment-brief"
}

Usage:
    python3 med_spa_treatment_descriptions.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Med Spa Treatment Descriptions"


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


FIELDS = ["treatment_page", "status_block", "claim_checks", "consent_notes"]
LIMITS = {"treatment_page": 2200, "status_block": 400, "claim_checks": 600, "consent_notes": 400}


def run(input_path, out_dir):
    data = read_flat(input_path)
    report = []
    report.append(f"# {TITLE}")
    report.append("")
    report.append(f"source: {input_path}")
    report.append("")
    missing = []
    for field in FIELDS:
        value = data.get(field, "")
        limit = LIMITS.get(field)
        if isinstance(value, list):
            value = "; ".join(str(v) for v in value)
        value = str(value or "")
        if not value:
            missing.append(field)
            report.append(f"- {field}: EMPTY")
        elif limit and len(value) > limit:
            report.append(f"- {field}: {len(value)} chars, limit {limit} - TOO LONG")
        else:
            report.append(f"- {field}: {len(value)} chars" + (f", limit {limit}" if limit else ""))
    report.append("")
    if missing:
        report.append("## Missing from the brief")
        for field in missing:
            report.append(f"- {field}")
    else:
        report.append("## All fields present")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never state FDA approval, FDA clearance or a regulatory mark unless the practice supplies the exact model and the status is confirmed in the FDA database.", "Never promise a result, a duration, a number of sessions, no downtime or a painless procedure.", "Never invent a before-and-after image, a patient quote, a review score, a price or a clinical result."]:
        report.append(f"- {rule}")
    write_out(out_dir, "treatment-brief.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
