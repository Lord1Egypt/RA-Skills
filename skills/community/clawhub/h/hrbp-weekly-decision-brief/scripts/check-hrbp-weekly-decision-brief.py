#!/usr/bin/env python3
"""Reject structurally incomplete HRBP weekly decision briefs."""

from pathlib import Path
import re
import sys

REQUIRED_HEADINGS = (
    "## Brief metadata", "## Executive readout", "## Decision items",
    "## Manager follow-ups", "## Watchlist", "## Verifier findings",
    "## Human disposition", "## Receipt",
)
REQUIRED_ITEM_FIELDS = (
    "Verified facts", "Source references", "Interpretation / working hypothesis",
    "Missing facts", "Written policy layer", "Operating practice layer",
    "Accountable owner", "Next question or action",
    "Human review / escalation boundary",
)

def value_after(label, block):
    match = re.search(rf"^- {re.escape(label)}:[ \t]*(.*)$", block, re.MULTILINE)
    return match.group(1).strip() if match else None

def main():
    if len(sys.argv) != 2:
        print("usage: check-hrbp-weekly-decision-brief.py BRIEF.md")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    errors = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")
    items = re.split(r"^### Decision item:", text, flags=re.MULTILINE)[1:]
    if not items:
        errors.append("at least one decision item is required")
    placeholders = {"", "[short neutral title]", "tbd", "unknown", "n/a"}
    for index, item in enumerate(items, start=1):
        for field in REQUIRED_ITEM_FIELDS:
            value = value_after(field, item)
            if value is None:
                errors.append(f"decision item {index}: missing field '{field}'")
            elif value.lower() in placeholders:
                errors.append(f"decision item {index}: unresolved field '{field}'")
    if "Status: DRAFT — HUMAN REVIEW REQUIRED" not in text:
        errors.append("brief must remain marked DRAFT — HUMAN REVIEW REQUIRED")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {path}")
    print("Structural completeness only; source validation and human judgment remain required.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
