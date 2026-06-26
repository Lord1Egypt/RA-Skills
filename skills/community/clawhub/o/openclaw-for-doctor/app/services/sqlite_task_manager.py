from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from threading import Lock
from uuid import uuid4

from app.core.models import StoredTask, TaskExecutionProfile, TaskRequest, TaskResult, TaskStatus


class SQLiteTaskManager:
    """SQLite-backed task store for persistence across restarts."""

    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        if self.db_path.parent and str(self.db_path.parent) not in {"", "."}:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_updated_at ON tasks(updated_at DESC)"
            )

    def _save(self, task: StoredTask) -> None:
        payload = task.model_dump_json()
        updated_at = task.updated_at.isoformat()
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO tasks(task_id, task_json, updated_at)
                VALUES(?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    task_json=excluded.task_json,
                    updated_at=excluded.updated_at
                """,
                (task.task_id, payload, updated_at),
            )

    def _load(self, task_id: str) -> StoredTask:
        row = self._conn.execute(
            "SELECT task_json FROM tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise KeyError(task_id)
        return StoredTask.model_validate_json(row["task_json"])

    def create(self, request: TaskRequest) -> StoredTask:
        task_id = str(uuid4())
        task = StoredTask(task_id=task_id, request=request, status=TaskStatus.queued)
        with self._lock:
            self._save(task)
        return task

    def set_profile(self, task_id: str, profile: TaskExecutionProfile) -> None:
        with self._lock:
            task = self._load(task_id)
            task.profile = profile
            task.updated_at = datetime.utcnow()
            self._save(task)

    def mark_running(self, task_id: str) -> None:
        with self._lock:
            task = self._load(task_id)
            task.status = TaskStatus.running
            task.attempts += 1
            task.updated_at = datetime.utcnow()
            self._save(task)

    def mark_completed(self, task_id: str, result: TaskResult) -> None:
        with self._lock:
            task = self._load(task_id)
            task.status = TaskStatus.completed
            task.result = result
            task.updated_at = datetime.utcnow()
            self._save(task)

    def mark_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            task = self._load(task_id)
            task.status = TaskStatus.failed
            task.error = error
            task.updated_at = datetime.utcnow()
            self._save(task)

    def mark_cancelled(self, task_id: str, reason: str) -> None:
        with self._lock:
            task = self._load(task_id)
            task.status = TaskStatus.cancelled
            task.error = reason
            task.updated_at = datetime.utcnow()
            self._save(task)

    def requeue(self, task_id: str) -> None:
        with self._lock:
            task = self._load(task_id)
            task.status = TaskStatus.queued
            task.error = None
            task.result = None
            task.updated_at = datetime.utcnow()
            self._save(task)

    def get(self, task_id: str) -> StoredTask:
        with self._lock:
            return self._load(task_id)

    def list(self) -> list[StoredTask]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT task_json FROM tasks ORDER BY updated_at DESC"
            ).fetchall()
        return [StoredTask.model_validate_json(row["task_json"]) for row in rows]
