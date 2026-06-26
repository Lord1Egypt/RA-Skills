from __future__ import annotations

import importlib.util
from pathlib import Path

from .utils import Task


def run_check(task: Task, workdir: Path, transcript: dict) -> dict:
    task_dir = Path(task.task_dir)
    spec = importlib.util.spec_from_file_location(f"gigo_check_{task.id}", task_dir / "check.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    fixtures = task_dir / "fixtures"
    return module.evaluate(workdir, transcript, fixtures)

