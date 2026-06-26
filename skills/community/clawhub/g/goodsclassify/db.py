import sqlite3
from datetime import datetime
from typing import Optional

from config import Config


class Database:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    phone TEXT NOT NULL DEFAULT '',
                    pending_question TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            columns = {
                row[1]: row for row in conn.execute("PRAGMA table_info(users)").fetchall()
            }
            if "session_id" not in columns:
                conn.execute("ALTER TABLE users ADD COLUMN session_id TEXT")
            if "pending_question" not in columns:
                conn.execute("ALTER TABLE users ADD COLUMN pending_question TEXT")

            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_session_id ON users(session_id)"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")

    def get_phone(self, session_id: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT phone FROM users WHERE session_id = ? LIMIT 1",
                (session_id,),
            ).fetchone()
            if not row:
                return None
            return row[0] or None

    def set_pending_question(self, session_id: str, question: str) -> None:
        now = self._now()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO users (session_id, phone, pending_question, created_at, updated_at)
                VALUES (?, '', ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    pending_question = excluded.pending_question,
                    updated_at = excluded.updated_at
                """,
                (session_id, question, now, now),
            )

    def pop_pending_question(self, session_id: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT pending_question FROM users WHERE session_id = ? LIMIT 1",
                (session_id,),
            ).fetchone()
            pending = row[0] if row and row[0] else None
            conn.execute(
                "UPDATE users SET pending_question = NULL, updated_at = ? WHERE session_id = ?",
                (self._now(), session_id),
            )
            return pending

    def save_phone(self, session_id: str, phone: str) -> None:
        now = self._now()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO users (session_id, phone, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    phone = excluded.phone,
                    updated_at = excluded.updated_at
                """,
                (session_id, phone, now, now),
            )

    @staticmethod
    def _now() -> str:
        return datetime.now().isoformat(sep=" ", timespec="seconds")


db = Database()
