from __future__ import annotations

import json
import queue
import threading
import urllib.error
import urllib.request
from typing import Optional

from app.channels.dispatcher import ChannelDispatcher
from app.config import Settings
from app.core.engine import DoctorAssistantEngine
from app.core.models import TaskStatus
from app.services.base import TaskManager


class AsyncTaskExecutor:
    """Background worker for queued task execution."""

    def __init__(
        self,
        task_manager: TaskManager,
        engine: DoctorAssistantEngine,
        dispatcher: ChannelDispatcher,
        settings: Settings,
    ) -> None:
        self.task_manager = task_manager
        self.engine = engine
        self.dispatcher = dispatcher
        self.settings = settings
        self._queue: queue.Queue = queue.Queue()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._start_lock = threading.Lock()

    def start(self) -> None:
        with self._start_lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, name="doctor-task-worker", daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._queue.put("")
        if self._thread:
            self._thread.join(timeout=2)

    def enqueue(self, task_id: str) -> None:
        self._queue.put(task_id)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                task_id = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
            if not task_id:
                continue
            self._process_task(task_id)

    def _process_task(self, task_id: str) -> None:
        try:
            task = self.task_manager.get(task_id)
        except KeyError:
            return

        if task.status == TaskStatus.cancelled:
            return

        self.task_manager.mark_running(task_id)

        try:
            result = self.engine.execute(task.request, task_id=task_id)
            result.delivery = self.dispatcher.dispatch(task.request.channel, result)
            self.task_manager.mark_completed(task_id, result)
            self._send_callback(task_id)
        except Exception as exc:
            self.task_manager.mark_failed(task_id, str(exc))

    def _send_callback(self, task_id: str) -> None:
        if not self.settings.enable_outbound_send:
            return

        task = self.task_manager.get(task_id)
        callback_url = (task.request.callback_url or "").strip()
        if not callback_url:
            return

        payload = {
            "task_id": task.task_id,
            "status": task.status.value,
            "result": task.result.model_dump(mode="json") if task.result else None,
        }
        request = urllib.request.Request(
            callback_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.settings.webhook_timeout_seconds):
                return
        except urllib.error.URLError:
            return
        except Exception:
            return
