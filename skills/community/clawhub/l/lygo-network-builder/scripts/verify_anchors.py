#!/usr/bin/env python3
"""ClawHub skill wrapper — runs stack lygo_network_builder_verify.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _stack_paths import resolve_stack_root


def main() -> int:
    root = resolve_stack_root()
    script = root / "tools" / "lygo_network_builder_verify.py"
    cp = subprocess.run([sys.executable, str(script)], cwd=root, check=False)
    return cp.returncode


if __name__ == "__main__":
    raise SystemExit(main())