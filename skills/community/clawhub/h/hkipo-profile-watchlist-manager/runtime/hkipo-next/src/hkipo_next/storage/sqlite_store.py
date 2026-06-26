"""SQLite-backed persistence for parameter versions."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from hkipo_next.contracts.scoring import ParameterSet, ParameterVersion


class SQLiteStore:
    """Persist parameter versions and active selection in SQLite."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS parameter_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version_id TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 0
                );

                CREATE UNIQUE INDEX IF NOT EXISTS idx_parameter_versions_active
                ON parameter_versions(is_active)
                WHERE is_active = 1;
                """
            )

    def has_parameter_versions(self) -> bool:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM parameter_versions").fetchone()
        return bool(row["total"])

    def save_parameter_set(
        self,
        parameter_set: ParameterSet,
        *,
        activate: bool = False,
    ) -> ParameterVersion:
        self.initialize()
        created_at = datetime.now(timezone.utc)
        with self._connect() as connection:
            version_id = self._next_version_id(connection, parameter_set.name)
            if activate:
                connection.execute("UPDATE parameter_versions SET is_active = 0 WHERE is_active = 1")
            connection.execute(
                """
                INSERT INTO parameter_versions (name, version_id, created_at, payload_json, is_active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    parameter_set.name,
                    version_id,
                    created_at.isoformat(),
                    json.dumps(parameter_set.model_dump(mode="json"), ensure_ascii=False),
                    int(activate),
                ),
            )
            row = connection.execute(
                "SELECT * FROM parameter_versions WHERE version_id = ?",
                (version_id,),
            ).fetchone()
        return self._row_to_parameter_version(row)

    def list_parameter_sets(self) -> list[ParameterVersion]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM parameter_versions ORDER BY created_at DESC, id DESC"
            ).fetchall()
        return [self._row_to_parameter_version(row) for row in rows]

    def get_parameter_set(self, version_id: str) -> ParameterVersion | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM parameter_versions WHERE version_id = ?",
                (version_id,),
            ).fetchone()
        return self._row_to_parameter_version(row) if row is not None else None

    def get_active_parameter_set(self) -> ParameterVersion | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM parameter_versions WHERE is_active = 1 LIMIT 1"
            ).fetchone()
        return self._row_to_parameter_version(row) if row is not None else None

    def set_active_parameter_set(self, version_id: str) -> ParameterVersion:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM parameter_versions WHERE version_id = ?",
                (version_id,),
            ).fetchone()
            if row is None:
                raise KeyError(version_id)
            connection.execute("UPDATE parameter_versions SET is_active = 0 WHERE is_active = 1")
            connection.execute(
                "UPDATE parameter_versions SET is_active = 1 WHERE version_id = ?",
                (version_id,),
            )
            row = connection.execute(
                "SELECT * FROM parameter_versions WHERE version_id = ?",
                (version_id,),
            ).fetchone()
        return self._row_to_parameter_version(row)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _row_to_parameter_version(row: sqlite3.Row) -> ParameterVersion:
        payload = json.loads(row["payload_json"])
        return ParameterVersion(
            **payload,
            parameter_version=row["version_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            is_active=bool(row["is_active"]),
        )

    @staticmethod
    def _next_version_id(connection: sqlite3.Connection, name: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "params"
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM parameter_versions WHERE version_id LIKE ?",
            (f"{slug}-v%",),
        ).fetchone()
        next_number = int(row["total"]) + 1
        return f"{slug}-v{next_number:03d}"
