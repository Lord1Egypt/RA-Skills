#!/usr/bin/env python3
"""
Bundled launcher for the Jin10 skill.
"""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from jin10.cli import main


if __name__ == '__main__':
    raise SystemExit(main())
