"""Shared utility helpers for the ppt_skill package."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def get_logger(name: str) -> logging.Logger:
    """Create and return a consistent logger for all skill modules."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def timestamp_str() -> str:
    """Return a compact timestamp used in generated output filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_directory(path: str | Path) -> Path:
    """Ensure a directory exists and return it as a Path object."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def build_non_overwrite_path(path: str | Path, suffix: str = "_updated") -> Path:
    """Return a non-overwriting path by appending a suffix and timestamp."""
    src = Path(path)
    target_name = f"{src.stem}{suffix}_{timestamp_str()}{src.suffix}"
    return src.with_name(target_name)


def save_json(data: Dict[str, Any], output_path: str | Path) -> Path:
    """Persist dictionary content as UTF-8 JSON for debug logs."""
    out = Path(output_path)
    ensure_directory(out.parent)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
