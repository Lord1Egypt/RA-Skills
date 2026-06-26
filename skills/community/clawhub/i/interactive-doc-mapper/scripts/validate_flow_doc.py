#!/usr/bin/env python3
"""Validate an interactive workflow documentation JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_interactive_doc import FlowDocError, load_flow_doc, validate_flow_doc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate workflow-map JSON before rendering.")
    parser.add_argument("--input", required=True, help="Path to the workflow JSON document.")
    parser.add_argument("--out", help="Optional path for a JSON validation report.")
    args = parser.parse_args(argv)

    try:
        data = load_flow_doc(args.input)
    except FlowDocError as exc:
        report = {"ok": False, "errors": [str(exc)], "warnings": [], "counts": {"groups": 0, "nodes": 0, "actions": 0}}
    else:
        report = validate_flow_doc(data)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    if report["ok"]:
        print(f"Flow document is valid: {report['counts']['nodes']} nodes, {report['counts']['actions']} actions.")
        if report["warnings"]:
            print(f"Warnings: {len(report['warnings'])}")
        return 0

    print("Flow document is invalid:", file=sys.stderr)
    for error in report["errors"]:
        print(f"- {error}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
