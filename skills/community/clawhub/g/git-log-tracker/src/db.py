"""Shared database utilities for git-log-tracker."""

import sqlite3
from pathlib import Path

DEFAULT_DB_DIR = Path.home() / ".commit-logs"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "index.db"

SCHEMA_VERSION = 1


def _run_alembic_upgrade(db_path: Path) -> None:
    from alembic.config import Config
    from alembic import command

    migrations_dir = Path(__file__).parent / "migrations"
    cfg = Config()
    cfg.set_main_option("script_location", str(migrations_dir))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(cfg, "head")


def get_schema_version(db_path: Path) -> int:
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute("PRAGMA user_version").fetchone()[0]
    finally:
        conn.close()


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    current = conn.execute("PRAGMA user_version").fetchone()[0]
    if current < SCHEMA_VERSION:
        conn.close()
        _run_alembic_upgrade(db_path)
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    return conn
