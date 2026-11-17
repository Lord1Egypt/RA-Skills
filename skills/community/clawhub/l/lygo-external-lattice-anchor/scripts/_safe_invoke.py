#!/usr/bin/env python3
"""
In-process script runner for skill-local Python tools.

- No os.system / shell
- No eval / exec of strings
- Fixed argv list only
- Optional allowlist: path must be under skill scripts/ or trusted stack root
"""
from __future__ import annotations

import io
import os
import runpy
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent


def is_allowed_script(path: Path, stack: Path | None = None) -> bool:
    path = path.resolve()
    if not path.is_file() or path.suffix.lower() != ".py":
        return False
    try:
        path.relative_to(SKILL_SCRIPTS)
        return True
    except ValueError:
        pass
    if stack is not None:
        try:
            path.relative_to(stack.resolve())
            return True
        except ValueError:
            return False
    return False


def run_python_script(
    path: Path,
    argv: list[str] | None = None,
    *,
    cwd: Path | None = None,
    stack: Path | None = None,
) -> tuple[int, str]:
    """
    Run a .py file in-process (runpy). Returns (exit_code, combined_stdout_stderr).
    """
    path = path.resolve()
    if not is_allowed_script(path, stack=stack):
        return 2, f"REFUSED: script not on allowlist: {path}"

    argv = argv or []
    # refuse shell metacharacters in args (defense in depth)
    for a in argv:
        if any(c in a for c in (";", "|", "&", "`", "$(", "\n", "\r")):
            return 2, f"REFUSED: unsafe argv character in {a!r}"

    out_buf = io.StringIO()
    err_buf = io.StringIO()
    old_argv = sys.argv[:]
    old_cwd = os.getcwd()
    code = 0
    try:
        if cwd is not None:
            os.chdir(str(cwd))
        sys.argv = [str(path), *argv]
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            try:
                runpy.run_path(str(path), run_name="__main__")
            except SystemExit as e:
                c = e.code
                if c is None:
                    code = 0
                elif isinstance(c, int):
                    code = c
                else:
                    code = 1
            except Exception as e:
                err_buf.write(f"{type(e).__name__}: {e}\n")
                code = 1
    finally:
        sys.argv = old_argv
        try:
            os.chdir(old_cwd)
        except OSError:
            pass

    text = out_buf.getvalue()
    err = err_buf.getvalue()
    if err:
        text = (text + "\n" + err).strip() + "\n" if text else err
    return code, text
