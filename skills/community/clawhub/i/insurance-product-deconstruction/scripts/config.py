"""Load skill configuration from config.json."""

from __future__ import annotations

import json
from pathlib import Path

_config = None


def get_config() -> dict:
    global _config
    if _config is not None:
        return _config

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    if config_path.exists():
        _config = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        _config = {}

    # Expand ~ in paths
    for key in ["obsidian_output", "python_venv", "ocr_tools_dir"]:
        if key in _config and _config[key]:
            _config[key] = str(Path(_config[key]).expanduser())

    return _config


def get_obsidian_output() -> Path:
    return Path(get_config().get("obsidian_output", str(Path.home() / "Documents")))


def get_python_venv() -> str:
    return get_config().get("python_venv", "")


def get_ocr_tools_dir() -> Path | None:
    d = get_config().get("ocr_tools_dir", "")
    return Path(d) if d else None
