from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    env: str = "dev"
    api_token: str = ""
    task_store: str = "sqlite"
    sqlite_db_path: str = "./doctor_tasks.db"
    enable_outbound_send: bool = False
    webhook_timeout_seconds: float = 5.0


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        env=os.getenv("OPENCLAW_DOCTOR_ENV", "dev"),
        api_token=os.getenv("OPENCLAW_DOCTOR_API_TOKEN", "").strip(),
        task_store=os.getenv("OPENCLAW_DOCTOR_TASK_STORE", "sqlite").strip().lower(),
        sqlite_db_path=os.getenv("OPENCLAW_DOCTOR_DB_PATH", "./doctor_tasks.db").strip(),
        enable_outbound_send=_bool_env("OPENCLAW_DOCTOR_ENABLE_OUTBOUND_SEND", False),
        webhook_timeout_seconds=_float_env("OPENCLAW_DOCTOR_WEBHOOK_TIMEOUT_SECONDS", 5.0),
    )
