from __future__ import annotations

from pathlib import Path


_SRC_PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "src" / "mal_updater"

if not _SRC_PACKAGE_ROOT.is_dir():
    raise ImportError(f"Expected src package directory at {_SRC_PACKAGE_ROOT}")

__path__ = [str(_SRC_PACKAGE_ROOT)]
