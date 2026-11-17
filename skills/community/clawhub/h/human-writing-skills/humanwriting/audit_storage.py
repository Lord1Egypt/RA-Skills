"""Confined paths and atomic, serialized writes for local audit packages."""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from functools import wraps
from pathlib import Path


def package_path(package: Path, value: str, label: str) -> Path:
    candidate = (package / value).resolve()
    try:
        candidate.relative_to(package.resolve())
    except ValueError as exc:
        raise ValueError(f"Task {label} must stay within the audit package.") from exc
    return candidate


def load_plan(package_dir):
    package = Path(package_dir).resolve()
    path = package_path(package, "agent-plan.json", "plan path")
    if not path.is_file():
        raise ValueError("Chunk audit package is missing agent-plan.json.")
    plan = json.loads(path.read_text(encoding="utf-8"))
    tasks = plan.get("tasks") if isinstance(plan, dict) else None
    if not isinstance(tasks, list) or not tasks or not all(isinstance(t, dict) for t in tasks):
        raise ValueError("Chunk audit agent plan contains no valid tasks.")
    ids = [t.get("task_id") for t in tasks]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Audit task IDs must be non-empty and unique.")
    for task in tasks:
        dependencies = task.get("depends_on", [])
        if not isinstance(dependencies, list) or any(
            not isinstance(i, str) or i not in ids or i == task["task_id"] for i in dependencies
        ):
            raise ValueError("Audit task dependencies must refer to other planned tasks.")
        if not isinstance(task.get("required_before_reconciliation", True), bool):
            raise ValueError("required_before_reconciliation must be a boolean.")
    if not any(t.get("required_before_reconciliation", True) for t in tasks):
        raise ValueError("Audit plan must contain required review tasks.")
    return package, plan, tasks


def atomic_write(path: Path, text: str) -> None:
    # A unique file avoids following a pre-existing, predictable .tmp symlink.
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def package_lock(package: Path):
    """OS locks are released on process exit and cover multiple MCP workers."""
    path = package_path(package, ".agent-state.lock", "lock path")
    with path.open("a+b") as stream:
        if os.name == "nt":
            import msvcrt

            if path.stat().st_size == 0:
                try:
                    stream.write(b"\0")
                    stream.flush()
                except OSError:
                    pass
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def serialized(function):
    @wraps(function)
    def wrapped(package_dir, *args, **kwargs):
        with package_lock(Path(package_dir).resolve()):
            return function(package_dir, *args, **kwargs)
    return wrapped
