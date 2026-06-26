#!/usr/bin/env python3
"""Fetch and format open theorems from OpenMath."""

from __future__ import annotations

import argparse
import sys

from openmath_env_config import (
    OpenMathEnvConfigError,
    load_openmath_preferences,
    normalize_preferred_language,
)
from openmath_api import fetch_open_theorems, format_date


SUPPORTED_LANGUAGES = ("lean", "rocq")


def parse_language(value: str) -> str:
    language = normalize_preferred_language(value)
    if language is None:
        raise argparse.ArgumentTypeError(
            f"language must be one of: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    return language


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List all open OpenMath theorems or filter by language."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Explicit config path. Default: auto-discover from ./.openmath-skills or ~/.openmath-skills.",
    )
    parser.add_argument(
        "language",
        nargs="?",
        type=parse_language,
        help="Optional theorem language filter (`lean` or `rocq`).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        preferences = load_openmath_preferences(
            args.config,
            require_preferred_language=True,
        )
    except OpenMathEnvConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    language = args.language or preferences.preferred_language

    if args.language is None:
        print(
            f"Using preferred language from {preferences.config_path}: {language} "
            "(no cross-language fallback)\n"
        )

    try:
        theorems = fetch_open_theorems(language)
    except RuntimeError as exc:
        print(f"Failed to fetch theorems: {exc}", file=sys.stderr)
        return 1

    if not theorems:
        suffix = f" for {language}" if language else ""
        print(f"No open theorems found{suffix}.")
        if language:
            print("Did not query other languages.")
        return 0

    suffix = f" ({language})" if language else ""
    print(f"Found {len(theorems)} open theorems{suffix}:\n")
    print(f"{'ID':<5} | {'Language':<10} | {'Reward':<10} | {'Expires':<20} | Title")
    print("-" * 80)

    for theorem in theorems:
        theorem_id = str(theorem.get("id", ""))
        theorem_language = (
            normalize_preferred_language(theorem.get("language"))
            or str(theorem.get("language", ""))
        )
        reward = str(theorem.get("reward", ""))
        expires = format_date(theorem.get("expire_time"))
        title = theorem.get("theorem_title", "")
        print(
            f"{theorem_id:<5} | {theorem_language:<10} | {reward:<10} | {expires:<20} | {title}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
