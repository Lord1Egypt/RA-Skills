"""SQLite connection helper. Database lives at $GLANCE_HOME/data.db."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

GLANCE_HOME = Path(os.environ.get("GLANCE_HOME", Path.home() / ".glancely"))


def get_db_path() -> Path:
    """Return path to the shared SQLite database."""
    path = Path(os.environ.get("GLANCE_HOME", GLANCE_HOME))
    path.mkdir(parents=True, exist_ok=True)
    return path / "data.db"


def get_connection() -> sqlite3.Connection:
    """Return a connection to the shared database with WAL mode and foreign keys."""
    conn = sqlite3.connect(str(get_db_path()))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn
