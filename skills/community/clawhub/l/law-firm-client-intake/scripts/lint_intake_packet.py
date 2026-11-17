#!/usr/bin/env python3
"""Law Firm Client Intake Form

Lints a checklist or copy file for law firm client intake form: missing sections, long lines and banned phrases.

Parameters for this build:
{
  "required": [
    "Matter details",
    "Client identification",
    "Adverse parties",
    "Conflicts search",
    "Fee arrangement",
    "Trust account instructions",
    "Data handling",
    "Limits notice",
    "Prepared by and date"
  ],
  "max_chars": 120,
  "banned": [
    "you will win",
    "certain outcome",
    "best attorney",
    "expert in all areas",
    "risk free"
  ]
}

Usage:
    python3 law_firm_client_intake_form.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Law Firm Client Intake Form"


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


REQUIRED = ["Matter details", "Client identification", "Adverse parties", "Conflicts search", "Fee arrangement", "Trust account instructions", "Data handling", "Limits notice", "Prepared by and date"]
MAX_CHARS = 120
BANNED = ["you will win", "certain outcome", "best attorney", "expert in all areas", "risk free"]


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    report = [f"# {TITLE} lint", "", f"source: {input_path}", ""]
    found = [line.strip() for line in lines if line.strip()]
    problems = []
    for item in REQUIRED:
        if not any(item.lower() in line.lower() for line in found):
            problems.append(f"missing section: {item}")
    for number, line in enumerate(lines, 1):
        if len(line) > MAX_CHARS:
            problems.append(f"line {number} is {len(line)} chars (limit {MAX_CHARS})")
        low = line.lower()
        for phrase in BANNED:
            if phrase.lower() in low:
                problems.append(f"line {number} uses banned phrase: {phrase}")
    if problems:
        report.append("## Problems")
        report.extend(f"- {p}" for p in problems)
    else:
        report.append("## No problems found")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never collect a full Social Security number on an intake form; ask for the last four digits and get the rest through a secure channel.", "Never put a client name, address, phone number or matter detail in any file outside the firm's retention and confidentiality rules.", "Never present the intake as legal advice, an opinion on the merits or a promise of a result."]:
        report.append(f"- {rule}")
    write_out(out_dir, "lint-report.md", report)
    if problems:
        print(f"{len(problems)} problem(s) found")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
