from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .utils import TaskResult, checkpoint_path, load_json, write_json


def save_checkpoint(output_dir: Path, completed_task_ids: list[str], raw_results: list[TaskResult]) -> None:
    payload = {
        "completed_task_ids": completed_task_ids,
        "raw_results": [asdict(result) for result in raw_results],
    }
    write_json(checkpoint_path(output_dir), payload)


def load_checkpoint(output_dir: Path) -> dict | None:
    path = checkpoint_path(output_dir)
    if not path.exists():
        return None
    return load_json(path)


def clear_checkpoint(output_dir: Path) -> None:
    path = checkpoint_path(output_dir)
    if path.exists():
        path.unlink()
