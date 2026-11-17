"""
Shared runtime paths and environment loading helpers.

This keeps all CLI scripts aligned on:
- project-relative default paths
- WANGQI_ENV_FILE override
- workspace-root .env fallback during local development
"""

import os
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = PROJECT_DIR.parent

DEFAULT_SKILL_PATH = str(PROJECT_DIR / "SKILL.md")
DEFAULT_CARDS_DIR = str(PROJECT_DIR / "data" / "cards")
DEFAULT_OVERRIDES_DIR = str(PROJECT_DIR / "data" / "overrides")
DEFAULT_PERSIST_DIR = str(PROJECT_DIR / "chroma_db")
DEFAULT_OUTPUT_DIR = str(PROJECT_DIR / "data" / "cards")
DEFAULT_EVALS_DIR = str(PROJECT_DIR / "evals")
DEFAULT_VECTOR_STORE_ID_PATH = str(PROJECT_DIR / ".vector_store_id")


def resolve_env_file() -> Tuple[Optional[Path], str, Optional[str]]:
    """Resolve the env file using runtime precedence."""
    explicit_env = os.getenv("WANGQI_ENV_FILE")
    explicit_path = None

    if explicit_env:
        explicit_path = Path(explicit_env).expanduser()
        if explicit_path.exists():
            return explicit_path.resolve(), "WANGQI_ENV_FILE", None

    workspace_env = WORKSPACE_DIR / ".env"
    if workspace_env.exists():
        warning = None
        if explicit_path is not None:
            warning = f"WANGQI_ENV_FILE not found: {explicit_path}"
        return workspace_env.resolve(), "workspace .env", warning

    if explicit_path is not None:
        return None, "WANGQI_ENV_FILE", f"WANGQI_ENV_FILE not found: {explicit_path}"

    return None, "workspace .env", "No .env file found"


def load_runtime_env(*, override: bool = False) -> Optional[Path]:
    """Load the resolved env file if present and return its path."""
    env_path, _, _ = resolve_env_file()
    if env_path is not None:
        load_dotenv(env_path, override=override)
    return env_path
