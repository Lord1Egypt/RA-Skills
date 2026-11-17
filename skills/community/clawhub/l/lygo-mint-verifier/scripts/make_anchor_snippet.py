#!/usr/bin/env python3
"""Compat wrapper → mint_cli.py snippet (no subprocess)."""
from __future__ import annotations

import sys

from mint_cli import main as mint_main


def main() -> None:
    sys.argv = [sys.argv[0], "snippet", *sys.argv[1:]]
    raise SystemExit(mint_main())


if __name__ == "__main__":
    main()
