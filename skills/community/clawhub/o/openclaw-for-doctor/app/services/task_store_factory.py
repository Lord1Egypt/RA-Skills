from __future__ import annotations

from app.config import Settings
from app.services.base import TaskManager
from app.services.sqlite_task_manager import SQLiteTaskManager
from app.services.task_manager import InMemoryTaskManager


def create_task_manager(settings: Settings) -> TaskManager:
    if settings.task_store == "memory":
        return InMemoryTaskManager()
    return SQLiteTaskManager(settings.sqlite_db_path)
