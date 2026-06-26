"""
State persistence helpers for init results/preferences.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

STATE_DIR = Path("state")


def _ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def state_file(provider: str) -> Path:
    """Return path to provider specific state file."""
    safe = provider.lower().replace("/", "_")
    return STATE_DIR / f"{safe}_state.json"


def write_state(provider: str, data: Dict[str, Any]) -> None:
    """Persist state to disk."""
    _ensure_state_dir()
    path = state_file(provider)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def read_state(provider: str) -> Dict[str, Any]:
    """Load provider state if present."""
    path = state_file(provider)
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
