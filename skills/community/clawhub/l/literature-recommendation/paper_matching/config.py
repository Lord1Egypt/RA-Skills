"""Configuration helpers for the recommender MVP."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional at import time
    load_dotenv = None


def _expand_path(value: str) -> Path:
    return Path(os.path.expanduser(value)).resolve()


def _load_environment() -> None:
    root = Path(__file__).resolve().parents[1]
    env_path = os.getenv("OPENCLAW_ENV_FILE", os.path.expanduser("~/.config/literature-recommendation/.env"))
    if load_dotenv is None:
        return
    load_dotenv(env_path, override=False)
    load_dotenv(root / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    db_dsn: str
    output_dir: Path
    recall_candidate_pool: int


def load_settings(
    db_dsn: str | None = None,
    output_dir: str | None = None,
) -> Settings:
    _load_environment()
    root = Path(__file__).resolve().parents[1]
    resolved_dsn = (db_dsn or os.getenv("OPENCLAW_DB_DSN", "")).strip()
    if not resolved_dsn:
        raise RuntimeError("OPENCLAW_DB_DSN is required for PostgreSQL backend.")
    return Settings(
        db_dsn=resolved_dsn,
        output_dir=_expand_path(output_dir or os.getenv("OPENCLAW_OUTPUT_DIR", str(root / "outputs"))),
        recall_candidate_pool=max(5, int(os.getenv("OPENCLAW_RECALL_CANDIDATE_POOL", "20"))),
    )
