"""Minimal configuration loader for the bundled crawler runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PROVIDERS_PATH = BASE_DIR / "configs" / "providers.yaml"


def load_provider_config(path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    """Load provider configuration from YAML."""

    config_path = Path(path) if path else DEFAULT_PROVIDERS_PATH
    if not config_path.exists():
        return {}
    payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        return {}
    return {str(key): value if isinstance(value, dict) else {} for key, value in payload.items()}
