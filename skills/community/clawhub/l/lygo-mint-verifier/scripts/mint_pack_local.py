#!/usr/bin/env python3
"""Compat wrapper → mint_cli.py mint (no subprocess)."""
from __future__ import annotations

import sys

from mint_cli import main as mint_main


def main() -> None:
    # Rewrite argv: mint_pack_local.py --pack X → mint_cli.py mint --pack X
    sys.argv = [sys.argv[0], "mint", *sys.argv[1:]]
    raise SystemExit(mint_main())


if __name__ == "__main__":
    main()
