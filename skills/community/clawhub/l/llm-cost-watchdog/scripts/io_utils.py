"""
Crash-safe, race-safe file I/O helpers.

Each writer in the skill used plain `open(path, 'w')` which lets two
processes (e.g. the tailer + the smart-budget manager) interleave writes
and corrupt shared state. `write_json_atomic` writes to a sibling temp
file and `os.replace`s it over the target — atomic on POSIX, so a reader
only ever sees a fully-written file.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def write_json_atomic(path: Path, data: Any, *, indent: int = 2) -> None:
    """
    Write `data` as JSON to `path`. Atomic on POSIX: readers never see a
    half-written file, and concurrent writers don't produce torn output —
    the last rename wins cleanly.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Tempfile in the same directory so os.replace is on the same filesystem.
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def read_json(path: Path, default: Any = None) -> Any:
    """Read JSON from `path`, returning `default` on any error."""
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default
