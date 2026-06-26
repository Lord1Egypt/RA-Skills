#!/usr/bin/env python3
"""Fetch detailed information for a specific OpenMath theorem."""

from __future__ import annotations

import argparse
import sys

from openmath_api import fetch_theorem_detail, format_datetime
from openmath_env_config import OpenMathEnvConfigError, load_openmath_preferences


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch a theorem detail record by ID.")
    parser.add_argument(
        "--config",
        default=None,
        help="Explicit config path. Default: auto-discover from ./.openmath-skills or ~/.openmath-skills.",
    )
    parser.add_argument("theorem_id", type=int, help="OpenMath theorem ID")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        load_openmath_preferences(
            args.config,
            require_preferred_language=True,
        )
    except OpenMathEnvConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    try:
        theorem = fetch_theorem_detail(args.theorem_id)
    except RuntimeError as exc:
        print(f"Failed to fetch theorem detail: {exc}", file=sys.stderr)
        return 1

    print(f"\nTheorem Detail [ID: {theorem.theorem_id}]")
    print("=" * 40)
    print(f"Title: {theorem.title}")
    print(f"Language: {theorem.language}")
    print(f"Reward: {theorem.reward}")
    print(f"Status: {theorem.status}")
    print(f"Expires: {format_datetime(theorem.expire_time)}")
    print(f"Proposer: {theorem.proposer_nickname or 'N/A'} ({theorem.proposer or 'N/A'})")
    print(f"Description:\n{theorem.description}")

    if theorem.theorem_code:
        print(f"\nFormal Definition ({theorem.language}):")
        print("-" * 40)
        print(theorem.theorem_code)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
