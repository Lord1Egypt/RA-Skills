from __future__ import annotations

from datetime import datetime
from threading import Lock
from typing import Dict
from uuid import uuid4

from app.core.models import StoredTask, TaskExecutionProfile, TaskRequest, TaskResult, TaskStatus


class InMemoryTaskManager:
    """Thread-safe in-memory task store for initialization stage."""

    def __init__(self) -> None:
        self._tasks: Dict[str, StoredTask] = {}
        self._lock = Lock()

    def create(self, request: TaskRequest) -> StoredTask:
        task_id = str(uuid4())
        task = StoredTask(task_id=task_id, request=request, status=TaskStatus.queued)
        with self._lock:
            self._tasks[task_id] = task
        return task

    def set_profile(self, task_id: str, profile: TaskExecutionProfile) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.profile = profile
            task.updated_at = datetime.utcnow()

    def mark_running(self, task_id: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.running
            task.attempts += 1
            task.updated_at = datetime.utcnow()

    def mark_completed(self, task_id: str, result: TaskResult) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.completed
            task.result = result
            task.updated_at = datetime.utcnow()

    def mark_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.failed
            task.error = error
            task.updated_at = datetime.utcnow()

    def mark_cancelled(self, task_id: str, reason: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.cancelled
            task.error = reason
            task.updated_at = datetime.utcnow()

    def requeue(self, task_id: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.queued
            task.error = None
            task.result = None
            task.updated_at = datetime.utcnow()

    def get(self, task_id: str) -> StoredTask:
        with self._lock:
            return self._tasks[task_id]

    def list(self) -> list[StoredTask]:
        with self._lock:
            return list(self._tasks.values())
