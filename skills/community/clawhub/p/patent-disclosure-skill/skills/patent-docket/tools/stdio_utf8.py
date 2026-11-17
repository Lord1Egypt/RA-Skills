# -*- coding: utf-8 -*-
"""Windows 终端 UTF-8：当前进程 stdio + 子进程 PYTHONUTF8。"""
from __future__ import annotations

import os
import subprocess
import sys
from typing import Any


def ensure_utf8_stdio() -> None:
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, TypeError):
            pass


def child_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(base) if base is not None else os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env


def run(cmd: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    kwargs.setdefault("encoding", "utf-8")
    kwargs.setdefault("errors", "replace")
    kwargs["env"] = child_env(kwargs.get("env"))
    kwargs.pop("text", None)
    return subprocess.run(cmd, **kwargs)
