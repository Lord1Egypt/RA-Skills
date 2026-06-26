from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class Settings:
    base_url: str
    api_token: str
    workspace_id: str
    config_file: str | None = None

    default_project: str | None = None
    projects: dict[str, str] = field(default_factory=dict)
    states: dict[str, str] = field(default_factory=dict)
    priorities: dict[str, str] = field(default_factory=dict)


def _load_yaml(path: str | None) -> dict[str, Any]:
    if not path:
        return {}

    file_path = Path(path).expanduser()
    if not file_path.exists():
        return {}

    if yaml is None:
        raise RuntimeError(
            "PyYAML is not installed. Install it first or avoid using PLANE_CONFIG_FILE."
        )

    with file_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid config format: expected dict in {file_path}")

    return data


def load_settings() -> Settings:
    base_url = os.getenv("PLANE_BASE_URL", "").strip()
    api_token = os.getenv("PLANE_API_TOKEN", "").strip()
    workspace_id = os.getenv("PLANE_WORKSPACE_ID", "").strip()
    config_file = os.getenv("PLANE_CONFIG_FILE", "").strip() or None

    if not base_url:
        raise RuntimeError("Missing env: PLANE_BASE_URL")
    if not api_token:
        raise RuntimeError("Missing env: PLANE_API_TOKEN")
    if not workspace_id:
        raise RuntimeError("Missing env: PLANE_WORKSPACE_ID")

    extra = _load_yaml(config_file)

    return Settings(
        base_url=base_url.rstrip("/"),
        api_token=api_token,
        workspace_id=workspace_id,
        config_file=config_file,
        default_project=extra.get("default_project"),
        projects=extra.get("projects", {}) or {},
        states=extra.get("states", {}) or {},
        priorities=extra.get("priorities", {}) or {},
    )
