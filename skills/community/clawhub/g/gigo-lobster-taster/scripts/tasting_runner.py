from __future__ import annotations

import threading
import time
from pathlib import Path

from .checkpoint import save_checkpoint
from .utils import Task, TaskResult, progress_bar, t


class TastingRunner:
    def __init__(self, config: dict, soul, gateway_client, output_dir: Path) -> None:
        self.config = config
        self.soul = soul
        self.gateway_client = gateway_client
        self.output_dir = output_dir

    def run(self, tasks: list[Task], resume_data: dict | None = None) -> list[TaskResult]:
        raw_results: list[TaskResult] = []
        completed_task_ids: list[str] = []
        lang = self.config.get("lang", "zh")

        if resume_data:
            completed_task_ids = list(resume_data.get("completed_task_ids", []))
            for item in resume_data.get("raw_results", []):
                raw_results.append(TaskResult(**item))

        started = time.perf_counter()
        total = len(tasks)
        for index, task in enumerate(tasks, start=1):
            if task.id in completed_task_ids:
                continue

            elapsed_total = time.perf_counter() - started
            if elapsed_total > self.config["total_timeout_seconds"]:
                print(t(lang, "runner_total_timeout"))
                break

            percent = int(index / total * 100)
            print(t(lang, "runner_progress", index=index, total=total, bar=progress_bar(index, total), percent=percent))
            print(t(lang, "runner_dish_intro", dish_name=task.dish_name, dish_hint=task.dish_hint))

            heartbeat_stop = threading.Event()
            heartbeat_thread = self._start_task_heartbeat(
                task=task,
                lang=lang,
                stop_event=heartbeat_stop,
            )
            try:
                response = self.gateway_client.send_task(task.prompt, timeout=task.timeout_seconds)
            finally:
                heartbeat_stop.set()
                if heartbeat_thread:
                    heartbeat_thread.join(timeout=1)
            status = "success"
            error = None
            if response.get("timed_out"):
                status = "timeout"
                error = "timeout"
            elif response.get("error"):
                status = "error"
                error = response["error"]

            result = TaskResult(
                task_id=task.id,
                dish_name=task.dish_name,
                prompt=task.prompt,
                response=response.get("content", ""),
                status=status,
                error=error,
                elapsed_ms=int(response.get("elapsed_ms", 0)),
                usage=response.get("usage", {"prompt_tokens": 0, "completion_tokens": 0}),
                primary_dimensions=task.primary_dimensions,
                secondary_dimensions=task.secondary_dimensions,
                rubric=task.rubric,
            )
            raw_results.append(result)
            completed_task_ids.append(task.id)
            save_checkpoint(self.output_dir, completed_task_ids, raw_results)

            if status == "success":
                print(t(lang, "runner_success", dish_name=task.dish_name))
            elif status == "timeout":
                print(t(lang, "runner_timeout", dish_name=task.dish_name))
            else:
                print(t(lang, "runner_error", dish_name=task.dish_name))

        return raw_results

    def _start_task_heartbeat(self, *, task: Task, lang: str, stop_event: threading.Event) -> threading.Thread | None:
        interval_seconds = int(self.config.get("task_heartbeat_seconds", 15) or 0)
        if interval_seconds <= 0:
            return None

        started = time.perf_counter()

        def heartbeat_loop() -> None:
            while not stop_event.wait(interval_seconds):
                elapsed_seconds = int(time.perf_counter() - started)
                print(
                    t(
                        lang,
                        "runner_task_heartbeat",
                        dish_name=task.dish_name,
                        seconds=max(interval_seconds, elapsed_seconds),
                    ),
                    flush=True,
                )

        thread = threading.Thread(
            target=heartbeat_loop,
            name=f"gigo-heartbeat-{task.id}",
            daemon=True,
        )
        thread.start()
        return thread
