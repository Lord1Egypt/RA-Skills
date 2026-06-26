from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .checker import evaluate_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Linux Command Guard Elite")
    sub = parser.add_subparsers(dest="action", required=True)

    check = sub.add_parser("check", help="Evaluate a shell command")
    check.add_argument("command", help="The shell command to evaluate")
    check.add_argument("--json", action="store_true", help="Emit JSON")

    sub.add_parser("explain", help="Print security model summary")
    return parser


def _print_explanation() -> None:
    print("Linux Command Guard Elite")
    print("- allowlist first")
    print("- wrappers and interpreters blocked by default")
    print("- shell chaining, pipes, redirects, and command substitution blocked")
    print("- protected paths blocked")
    print("- high-risk binaries require manual approval")
    print("- still use sandboxing and least privilege")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.action == "explain":
        _print_explanation()
        return 0

    decision = evaluate_command(args.command)
    if args.json:
        print(json.dumps(asdict(decision), indent=2))
    else:
        status = "ALLOWED" if decision.allowed else "BLOCKED"
        print(f"{status}: {decision.reason}")
        if decision.matched_rule:
            print(f"rule: {decision.matched_rule}")
        if decision.base_command:
            print(f"base: {decision.base_command}")
        for detail in decision.details:
            print(f"detail: {detail}")
    return 0 if decision.allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
