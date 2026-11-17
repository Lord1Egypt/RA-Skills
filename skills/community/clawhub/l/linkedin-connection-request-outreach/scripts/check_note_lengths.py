#!/usr/bin/env python3
"""LinkedIn Connection Request Outreach

Measures a draft against the real per-channel limits for linkedin connection request outreach.

Parameters for this build:
{
  "limits": {
    "invitation_note": 300,
    "inmail_subject": 300,
    "inmail_body": 800,
    "profile_headline": 220,
    "connection_note_trimmed": 200
  }
}

Usage:
    python3 linkedin_connection_request_outreach.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "LinkedIn Connection Request Outreach"


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


LIMITS = {"invitation_note": 300, "inmail_subject": 300, "inmail_body": 800, "profile_headline": 220, "connection_note_trimmed": 200}


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    body = " ".join(line.strip() for line in text.splitlines() if line.strip())
    words = len(body.split())
    report = [f"# {TITLE} length check", "", f"source: {input_path}", "", f"characters: {len(body)}", f"words: {words}", ""]
    for channel, limit in LIMITS.items():
        state = "OK" if len(body) <= limit else f"OVER by {len(body) - limit}"
        report.append(f"- {channel}: limit {limit} - {state}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never run connection automation or an extension that clicks connect automatically; the platform's terms prohibit it and the account can be restricted.", "Never guess or pattern-match a personal email address to reach the prospect off-platform.", "Never claim a shared connection, a former employer or a referral that the rep cannot point to in the profile."]:
        report.append(f"- {rule}")
    write_out(out_dir, "length-check.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
