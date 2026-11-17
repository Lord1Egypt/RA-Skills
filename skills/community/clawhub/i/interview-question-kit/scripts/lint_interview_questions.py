#!/usr/bin/env python3
"""Interview Question Kit

Lints a checklist or copy file for interview question kit: missing sections, long lines and banned phrases.

Parameters for this build:
{
  "required": [
    "Role and outcomes",
    "Competencies",
    "Questions by stage",
    "Follow-up probes",
    "Scoring rubric",
    "Do-not-ask list"
  ],
  "max_chars": 300,
  "banned": [
    "How old are you",
    "Are you married",
    "Do you have children",
    "Do you plan to have children",
    "Do you have any disabilities",
    "What is your current salary",
    "What was your salary",
    "Are you pregnant",
    "What is your religion",
    "native speaker",
    "Are you a native"
  ]
}

Usage:
    python3 interview_question_kit.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Interview Question Kit"


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


REQUIRED = ["Role and outcomes", "Competencies", "Questions by stage", "Follow-up probes", "Scoring rubric", "Do-not-ask list"]
MAX_CHARS = 300
BANNED = ["How old are you", "Are you married", "Do you have children", "Do you plan to have children", "Do you have any disabilities", "What is your current salary", "What was your salary", "Are you pregnant", "What is your religion", "native speaker", "Are you a native"]


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
    for rule in ["Never include a question about race, color, religion, national origin, sex, sexual orientation, gender identity, pregnancy, disability, genetic information, age, marital status, number of children or a medical condition.", "Never score a candidate, rank candidates, set a hiring cut-off or recommend a hire.", "Never put a real candidate's name, resume, contact details or interview answers into the kit."]:
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
