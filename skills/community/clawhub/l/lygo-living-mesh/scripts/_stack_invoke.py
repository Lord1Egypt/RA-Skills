#!/usr/bin/env python3
"""Locate LYGO stack and invoke a tools/*.py script."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    for p in HERE.parents:
        if (p / "tools" / "collect_living_mesh_badge.py").is_file():
            return p
        if (p / "tools" / "verify_all_kernel_layers.py").is_file():
            return p
        if (p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
            return p
    return Path.cwd()


def invoke(tool_name: str, argv: list[str] | None = None) -> int:
    stack = stack_root()
    tool = stack / "tools" / tool_name
    if not tool.is_file():
        print(
            f'{{"verdict":"ERROR","reason":"missing_tool","tool":"{tool_name}","stack":"{stack}","hint":"set LYGO_STACK_ROOT"}}',
            file=sys.stderr,
        )
        return 2
    cmd = [sys.executable, str(tool), *(argv if argv is not None else sys.argv[1:])]
    return subprocess.call(cmd, cwd=str(stack))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: _stack_invoke.py <tool.py> [args...]", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(invoke(sys.argv[1], sys.argv[2:]))
