#!/usr/bin/env python3
"""Compat wrapper → mint_cli.py backfill (no subprocess).

Does NOT inject --i-consent. Callers must pass --i-consent explicitly
for ledger writes (ClawHub security-audit Intent-Code Divergence fix).
"""
from __future__ import annotations

import sys

from mint_cli import main as mint_main


def main() -> None:
    # Pass-through only — never rewrite consent.
    sys.argv = [sys.argv[0], "backfill", *sys.argv[1:]]
    raise SystemExit(mint_main())


if __name__ == "__main__":
    main()
