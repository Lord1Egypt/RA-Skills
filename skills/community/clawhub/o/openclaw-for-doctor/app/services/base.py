from __future__ import annotations

from typing import Protocol

from app.core.models import StoredTask, TaskExecutionProfile, TaskRequest, TaskResult


class TaskManager(Protocol):
    def create(self, request: TaskRequest) -> StoredTask:
        ...

    def set_profile(self, task_id: str, profile: TaskExecutionProfile) -> None:
        ...

    def mark_running(self, task_id: str) -> None:
        ...

    def mark_completed(self, task_id: str, result: TaskResult) -> None:
        ...

    def mark_failed(self, task_id: str, error: str) -> None:
        ...

    def mark_cancelled(self, task_id: str, reason: str) -> None:
        ...

    def requeue(self, task_id: str) -> None:
        ...

    def get(self, task_id: str) -> StoredTask:
        ...

    def list(self) -> list[StoredTask]:
        ...
