#!/usr/bin/env python3
"""Planter-side wrapper: run stack tools/verify_all_kernel_layers.py"""
from __future__ import annotations

import subprocess
import sys

from _stack_paths import resolve_stack_root


def main() -> int:
    stack = resolve_stack_root(None)
    tool = stack / "tools" / "verify_all_kernel_layers.py"
    if not tool.is_file():
        print(
            "Missing tools/verify_all_kernel_layers.py — pull latest stack or run seeder verify alone.",
            file=sys.stderr,
        )
        return 1
    extra = sys.argv[1:]
    return subprocess.call([sys.executable, str(tool), *extra], cwd=str(stack))


if __name__ == "__main__":
    raise SystemExit(main())
