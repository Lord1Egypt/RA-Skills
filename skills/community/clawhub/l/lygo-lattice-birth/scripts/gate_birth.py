#!/usr/bin/env python3
"""Run example birth through gate in-process — dry-run training."""

from __future__ import annotations

import argparse
import json

from _stack_paths import resolve_stack_root, validate_local_json_path
from _stack_tools import load_tool


def main() -> int:
    ap = argparse.ArgumentParser(description="Gate a birth submission JSON")
    ap.add_argument("submission", nargs="?", help="Path to submission JSON")
    ap.add_argument("--example", action="store_true", help="Use built-in example birth")
    args = ap.parse_args()

    stack = resolve_stack_root()
    gate = load_tool(stack, "haven_star_chart_gate.py")

    if args.example:
        birth = load_tool(stack, "lygo_lattice_birth.py")
        ns = argparse.Namespace(
            slug="builder",
            champion="CHAMPION_LIGHTFATHER",
            equation=None,
            agent_id="lygo-lattice-birth",
            skill_slug="lygo-lattice-birth",
            gate=True,
        )
        return int(birth.cmd_example_birth(ns))

    if not args.submission:
        ap.print_help()
        return 2

    sub_path = validate_local_json_path(args.submission, stack=stack)
    sub = json.loads(sub_path.read_text(encoding="utf-8"))
    result = gate.validate_submission(sub)
    print(json.dumps(result, indent=2))
    return 0 if result.get("all_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())