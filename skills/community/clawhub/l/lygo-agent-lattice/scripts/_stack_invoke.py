#!/usr/bin/env python3
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
        if (p / "tools" / "agent_lattice_core.py").is_file():
            return p
        if (p / "tools" / "verify_living_mesh.py").is_file():
            return p
    return Path.cwd()


def invoke(tool_name: str, argv: list[str] | None = None) -> int:
    stack = stack_root()
    tool = stack / "tools" / tool_name
    if not tool.is_file():
        print(
            f'{{"verdict":"ERROR","reason":"missing_tool","tool":"{tool_name}","stack":"{stack}"}}',
            file=sys.stderr,
        )
        return 2
    return subprocess.call(
        [sys.executable, str(tool), *(argv if argv is not None else sys.argv[1:])],
        cwd=str(stack),
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(2)
    raise SystemExit(invoke(sys.argv[1], sys.argv[2:]))
