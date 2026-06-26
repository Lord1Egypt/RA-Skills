"""Helpers for locating and importing the untouched legacy workflow project."""

from __future__ import annotations

from pathlib import Path
import sys


def require_legacy_project_root(legacy_project_root: Path | None) -> Path:
    if legacy_project_root is None:
        raise RuntimeError(
            "could not locate openclaw_capture_workflow; set OPENCLAW_CAPTURE_LEGACY_PROJECT_ROOT"
        )
    if not (legacy_project_root / "src" / "openclaw_capture_workflow").exists():
        raise RuntimeError(f"legacy project root is invalid: {legacy_project_root}")
    return legacy_project_root.resolve()


def ensure_legacy_import_path(legacy_project_root: Path | None) -> Path:
    root = require_legacy_project_root(legacy_project_root)
    src_path = root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    return root


def legacy_scripts_dir(legacy_project_root: Path | None) -> Path:
    root = require_legacy_project_root(legacy_project_root)
    return root / "scripts"

