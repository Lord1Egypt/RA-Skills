from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from paths import ensure_skill_dirs, get_runtime_dir

JsonDict = Dict[str, Any]


class LockError(RuntimeError):
    pass


def _lock_path() -> Path:
    return get_runtime_dir() / 'switch.lock'


def acquire_lock(action: str) -> Path:
    ensure_skill_dirs()
    path = _lock_path()
    payload = {
        'pid': os.getpid(),
        'action': action,
        'started_at': datetime.now(timezone.utc).isoformat(),
    }
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            current = json.loads(path.read_text(encoding='utf-8', errors='ignore') or '{}')
        except Exception:
            current = {}
        stale = False
        pid = current.get('pid')
        if isinstance(pid, int):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                stale = True
            except PermissionError:
                stale = False
            except Exception:
                stale = False
        else:
            stale = True
        if stale:
            try:
                path.unlink(missing_ok=True)
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError as e:
                raise LockError(f'lock already exists: {path}') from e
        else:
            raise LockError(f'lock already exists: {path}')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return path


def release_lock() -> None:
    path = _lock_path()
    if path.exists():
        path.unlink()
