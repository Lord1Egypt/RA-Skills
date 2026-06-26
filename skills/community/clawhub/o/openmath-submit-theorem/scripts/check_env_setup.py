#!/usr/bin/env python3
"""Deprecated compatibility wrapper for check_authz_setup.py."""

from __future__ import annotations

import sys

from check_authz_setup import main as check_authz_main


def main(argv: list[str] | None = None) -> int:
    print(
        "Deprecated: use `python3 scripts/check_authz_setup.py` for OpenMath submission readiness checks.",
        file=sys.stderr,
    )
    return check_authz_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
