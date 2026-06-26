"""Shared helpers for loading legacy modules lazily."""

from __future__ import annotations

import importlib
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any


LEGACY_MODULE_DIR = Path(__file__).resolve().parents[3] / "scripts" / "hkipo"


def ensure_legacy_module_path() -> None:
    if not LEGACY_MODULE_DIR.exists():
        raise FileNotFoundError(f"legacy module directory not found: {LEGACY_MODULE_DIR}")

    path = str(LEGACY_MODULE_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)


@lru_cache(maxsize=8)
def load_legacy_module(module_name: str) -> Any:
    ensure_legacy_module_path()
    return importlib.import_module(module_name)
