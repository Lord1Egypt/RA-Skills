#!/usr/bin/env python3
"""Verify every content-addressed entry in a MoSoCanvas evidence registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidence import EvidenceError, verify_registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    blockers: list[str] = []
    entry_count = 0
    try:
        _, entries = verify_registry(args.registry)
        entry_count = len(entries)
    except EvidenceError as exc:
        blockers.append(str(exc))
    report = {
        "schema": "moso.evidence-validation/0.1",
        "registry": str(args.registry.resolve()),
        "status": "block" if blockers else "pass",
        "entries_verified": entry_count,
        "blockers": blockers
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
