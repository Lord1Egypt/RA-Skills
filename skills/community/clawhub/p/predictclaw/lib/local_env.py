from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values


def resolve_local_env_path(base_dir: Path) -> Path:
    override = os.getenv("PREDICTCLAW_ENV_FILE")
    if override:
        return Path(override).expanduser()
    return base_dir / ".env"


def load_local_env(base_dir: Path) -> Path:
    env_path = resolve_local_env_path(base_dir)
    if not env_path.exists():
        return env_path

    for key, value in dotenv_values(env_path).items():
        if value is None:
            continue
        os.environ.setdefault(key, value)

    return env_path
