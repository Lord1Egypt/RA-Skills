"""
Personal Assistant Skill — Database Layer (Sprint 0)

SQLite 连接管理、建表、迁移、通用 CRUD 封装。
使用 Python 3 标准库 sqlite3 + pathlib。
"""

from __future__ import annotations
import sqlite3
import os
import stat
import json
from contextlib import contextmanager
from pathlib import Path

# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

DEFAULT_DB_DIR = Path.home() / ".hermes" / "data" / "personal_assistant"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "tasks.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"

# ---------------------------------------------------------------------------
# Database class
# ---------------------------------------------------------------------------

class Database:
    """Personal Assistant SQLite database manager."""

    def __init__(self, db_path=None):
        """
        Args:
            db_path: Path to SQLite database file.
                     Defaults to ~/.hermes/data/personal_assistant/tasks.db
        """
        if db_path is None:
            self.db_path = DEFAULT_DB_PATH
        else:
            self.db_path = Path(os.path.expanduser(str(db_path)))

        self._conn = None

    # --- Initialisation ----------------------------------------------------

    def init_db(self):
        """
        Execute schema.sql to create all tables.
        Sets WAL journal mode and enables foreign keys.
        Auto-creates parent directories.
        """
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = self._get_raw_conn()

        try:
            # Enable WAL and foreign keys
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")

            # Load and execute schema
            schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
            conn.executescript(schema_sql)

            conn.commit()
        finally:
            conn.close()

        # Set restrictive file permissions (owner rw only)
        self._set_permissions()

    def _set_permissions(self):
        """Set database file permissions to 0o600 (owner read/write only)."""
        try:
            os.chmod(self.db_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # Non-critical — best effort

    # --- Connection management ---------------------------------------------

    def _get_raw_conn(self):
        """Return a raw sqlite3 connection (no context manager)."""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_conn(self):
        """
        Context manager that yields a sqlite3 connection.
        Auto-commits on clean exit, rolls back on exception.
        """
        conn = self._get_raw_conn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # --- General CRUD ------------------------------------------------------

    def execute(self, sql, params=None):
        """Execute a write statement. Returns cursor for lastrowid access."""
        with self.get_conn() as conn:
            cursor = conn.execute(sql, params or ())
            return cursor

    def fetch_one(self, sql, params=None):
        """Fetch a single row, or None."""
        with self.get_conn() as conn:
            cursor = conn.execute(sql, params or ())
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetch_all(self, sql, params=None):
        """Fetch all rows as a list of dicts."""
        with self.get_conn() as conn:
            cursor = conn.execute(sql, params or ())
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def insert(self, table, data: dict) -> int:
        """
        Insert a row and return lastrowid.

        Args:
            table: Table name.
            data: Dict of column_name -> value.

        Returns:
            The id of the inserted row.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute(sql, values)
        return cursor.lastrowid

    def update(self, table, data: dict, where: str, where_params=None):
        """
        Update rows matching the WHERE clause.

        Args:
            table: Table name.
            data: Dict of column_name -> new_value.
            where: SQL WHERE clause (without the 'WHERE' keyword).
            where_params: Parameters for the WHERE clause.
        """
        set_clause = ", ".join(f"{col} = ?" for col in data.keys())
        values = list(data.values()) + (list(where_params) if where_params else [])

        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        self.execute(sql, values)

    def delete(self, table, where: str, where_params=None):
        """
        Delete rows matching the WHERE clause.

        Args:
            table: Table name.
            where: SQL WHERE clause (without the 'WHERE' keyword).
            where_params: Parameters for the WHERE clause.
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        self.execute(sql, where_params or ())

    # --- Database maintenance ----------------------------------------------

    def stats(self) -> dict:
        """
        Return dictionary with table row counts and database file size.

        Returns:
            {
                "tables": {"tasks": 42, "milestones": 10, ...},
                "db_size_bytes": 123456,
                "db_path": "/home/user/.hermes/data/personal_assistant/tasks.db"
            }
        """
        tables = [
            "tasks", "milestones", "progress_logs",
            "recurring_tasks", "okr_items", "reminder_log",
        ]
        table_counts = {}
        for table in tables:
            result = self.fetch_one(
                "SELECT COUNT(*) AS cnt FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            )
            if result and result["cnt"] > 0:
                result = self.fetch_one(f"SELECT COUNT(*) AS cnt FROM {table}")
                table_counts[table] = result["cnt"] if result else 0
            else:
                table_counts[table] = 0

        db_size = 0
        if self.db_path.exists():
            db_size = self.db_path.stat().st_size

        return {
            "tables": table_counts,
            "db_size_bytes": db_size,
            "db_path": str(self.db_path),
        }

    def export(self, output_path: str):
        """
        Export full SQL dump to a file.

        Args:
            output_path: Destination path for the SQL dump file.
        """
        output_path = Path(os.path.expanduser(output_path))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        conn = self._get_raw_conn()
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for line in conn.iterdump():
                    f.write(line + "\n")
        finally:
            conn.close()

    def import_(self, input_path: str):
        """
        Import from an SQL dump file. Replaces the existing database entirely.

        Args:
            input_path: Path to the SQL dump file to import.
        """
        input_path = Path(os.path.expanduser(input_path))
        if not input_path.exists():
            raise FileNotFoundError(f"Import file not found: {input_path}")

        dump_sql = input_path.read_text(encoding="utf-8")

        # Close any existing connection, delete the current db file,
        # then recreate from the dump.
        self.close()
        if self.db_path.exists():
            self.db_path.unlink()

        conn = self._get_raw_conn()
        try:
            # Disable foreign keys during import — iterdump()
            # outputs tables in alphabetical order which may
            # violate FK dependencies (e.g. milestones before tasks)
            conn.execute("PRAGMA foreign_keys=OFF")
            conn.executescript(dump_sql)
            conn.execute("PRAGMA foreign_keys=ON")
            conn.commit()
        finally:
            conn.close()

        self._set_permissions()

    def cleanup(self):
        """
        Maintenance: VACUUM the database and remove reminder_log entries
        older than 30 days.
        """
        # Remove old reminder logs (keep last 30 days) — use execute() for auto-commit
        self.execute(
            "DELETE FROM reminder_log WHERE reminder_date < date('now', 'localtime', '-30 days')"
        )
        # VACUUM must run outside a transaction
        conn = self._get_raw_conn()
        try:
            conn.isolation_level = None  # autocommit mode
            conn.execute("VACUUM")
        finally:
            conn.close()

    def close(self):
        """Close the persistent connection if open."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
