#!/usr/bin/env python3
"""可选导出依赖：自动安装 openpyxl，失败时不影响检索等核心功能。"""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from typing import Tuple

_INSTALL_ATTEMPTED: set[str] = set()


class ExportNotAvailable(Exception):
    """导出依赖不可用（可回退 CSV）。"""


def _try_install(package: str) -> bool:
    if package in _INSTALL_ATTEMPTED:
        return False
    _INSTALL_ATTEMPTED.add(package)

    commands: list[list[str]] = []
    uv = shutil.which("uv")
    if uv:
        commands.append([uv, "pip", "install", package, "-q"])
    commands.append([sys.executable, "-m", "pip", "install", package, "-q"])

    for cmd in commands:
        try:
            proc = subprocess.run(
                cmd,
                timeout=180,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                importlib.invalidate_caches()
                return True
        except (OSError, subprocess.TimeoutExpired):
            continue
    return False


def ensure_openpyxl() -> Tuple[bool, str | None]:
    try:
        import openpyxl  # noqa: F401
        return True, None
    except ImportError:
        if _try_install("openpyxl"):
            try:
                import openpyxl  # noqa: F401
                return True, None
            except ImportError:
                pass
        return (
            False,
            "无法加载 openpyxl（已尝试自动安装）。"
            f"可手动执行: {sys.executable} -m pip install openpyxl",
        )


def warm_export_dependencies() -> None:
    ensure_openpyxl()
