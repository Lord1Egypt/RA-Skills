#!/usr/bin/env python3
"""Check shared OpenMath config before theorem discovery."""

from __future__ import annotations

import argparse
import sys

from openmath_env_config import OpenMathEnvConfigError, load_openmath_preferences


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check shared OpenMath config before theorem discovery."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Explicit config path. Default: auto-discover from ./.openmath-skills or ~/.openmath-skills.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        preferences = load_openmath_preferences(
            args.config,
            require_preferred_language=True,
        )
    except OpenMathEnvConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    print("Config:", preferences.config_path)
    print("Preferred Language:", preferences.preferred_language)
    print("OpenMath Site URL:", preferences.openmath_site_url)
    print("OpenMath API Host:", preferences.openmath_api_host)

    print("Status: ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
