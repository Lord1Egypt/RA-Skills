from __future__ import annotations

import shutil
from typing import Iterable


class MissingDependencyError(RuntimeError):
    pass


def which(name: str) -> str | None:
    return shutil.which(name)


def require_bin(name: str, hint: str | None = None) -> str:
    path = which(name)
    if path:
        return path
    message = f"Required binary not found: {name}"
    if hint:
        message += f". {hint}"
    raise MissingDependencyError(message)


def check_bins(names: Iterable[str]) -> dict[str, bool]:
    return {name: which(name) is not None for name in names}
