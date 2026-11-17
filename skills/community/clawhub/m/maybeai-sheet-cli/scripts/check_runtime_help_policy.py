#!/usr/bin/env python3
"""Reject hidden compatibility commands from executable skill examples.

This intentionally contains only the retired/hidden command policy, not a
mirror of the public CLI command tree. The installed CLI's `--help` remains the
source of truth for the public surface.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (ROOT / "SKILL.md", ROOT / "README.md", *(ROOT / "references").glob("*.md"))

# Every pattern must be a command invocation that starts a Markdown code-block
# line. Plain-text migration warnings are allowed and encouraged.
HIDDEN_COMMAND_PATTERNS = (
    r"mbs\s+workbook\s+(?:import-plan|list-user-workbooks|metadata|manifest|capabilities|list-worksheets)\b",
    r"mbs\s+table\s+(?:headers|append-rows|upsert-rows|replace-records|create-from-query)\b",
    r"mbs\s+range\s+(?:set-formula|calculate|config)\b",
    r"mbs\s+column\s+width\b",
    r"mbs\s+formula\s+(?:batch-set|compile)\b",
    r"mbs\s+cell\s+note\s+(?:read|set|clear)\b",
    r"mbs\s+cell\s+note-(?:get|read|set|clear)\b",
    r"mbs\s+(?:excel_worksheet|excel-worksheet|excel-table|base-table|db-table|sheet|style)\b",
    r"mbs\s+worksheet\s+image\b",
    r"mbs\s+range\s+lineage\b[^\n]*--cell\b",
)
COMPILED_PATTERNS = tuple(re.compile(pattern, re.IGNORECASE) for pattern in HIDDEN_COMMAND_PATTERNS)


def fenced_code_lines(text: str) -> list[tuple[int, str]]:
    is_in_fence = False
    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            is_in_fence = not is_in_fence
            continue
        if is_in_fence:
            findings.append((line_number, line))
    return findings


def main() -> int:
    violations: list[str] = []
    for path in DOCUMENTS:
        if not path.exists():
            continue
        for line_number, line in fenced_code_lines(path.read_text()):
            normalized = line.lstrip("# ").strip()
            if any(pattern.search(normalized) for pattern in COMPILED_PATTERNS):
                violations.append(f"{path.relative_to(ROOT)}:{line_number}: {line.strip()}")
    if violations:
        print("Hidden compatibility command found in executable documentation:", file=sys.stderr)
        print("\n".join(violations), file=sys.stderr)
        return 1
    print("Runtime-help policy check passed: no hidden compatibility command examples found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
