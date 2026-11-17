"""
infrastructure/state_repository.py — Single authority for state persistence

Replaces NovelState.save()/_load_or_create() with proper repository pattern.
All state IO flows through this one class. No other module touches state files directly.

v6 增强:
- 文件系统互斥锁 (os.mkdir atomicity)
- 乐观并发控制 (version check)
- 自动备份 (pre-save backup)
"""
from __future__ import annotations

import json
import os
import time
import shutil
import logging
import threading
import random
from pathlib import Path
from datetime import datetime
from copy import deepcopy
from typing import Optional

from domain.state import StateRoot
from domain.events import StateSavedEvent, RollbackEvent

_log = logging.getLogger("state_repo")


class StateRepositoryError(Exception):
    pass


class ConcurrentModificationError(StateRepositoryError):
    """Raised when state was modified by another process during save."""
    pass


class StateRepository:
    """
    Single source of truth for novel state persistence.
    
    v6: Added file-system mutex, optimistic concurrency, and auto-backup.
    """

    _LOCK_TIMEOUT = 5.0
    _LOCK_SLEEP = 0.05
    _MAX_SNAPSHOTS = 10
    _VOL_SIZE = 50
    _STATE_FILE = "state.json"

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir).resolve()
        self._state_path = self.book_dir / self._STATE_FILE
        self._tmp_dir = self.book_dir / ".tmp"
        self._snapshot_dir = self.book_dir / ".snapshots"
        self._backup_dir = self.book_dir / "_backup"
        self._lock_path = self._tmp_dir / "state.lock"
        self._thread_lock = threading.Lock()
        self._last_loaded_version: int = 0

    # ─── File Lock (using os.mkdir atomicity) ───

    def _acquire_lock(self) -> bool:
        start = time.time()
        while time.time() - start < self._LOCK_TIMEOUT:
            try:
                self._lock_path.mkdir(parents=True, exist_ok=False)
                return True
            except FileExistsError:
                meta = self._lock_path / "_meta.json"
                if meta.exists():
                    try:
                        if time.time() - meta.stat().st_mtime > self._LOCK_TIMEOUT * 2:
                            shutil.rmtree(str(self._lock_path), ignore_errors=True)
                            continue
                    except Exception:
                        pass
                time.sleep(self._LOCK_SLEEP + random.uniform(0, self._LOCK_SLEEP * 0.5))
            except OSError:
                time.sleep(self._LOCK_SLEEP)
        return False

    def _release_lock(self):
        try:
            shutil.rmtree(str(self._lock_path), ignore_errors=True)
        except Exception:
            pass

    # ─── Public API ───

    def load(self) -> StateRoot:
        _log.debug(f"Loading state from {self._state_path}")
        if self._state_path.exists():
            try:
                with open(self._state_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                state = StateRoot.from_dict(data)
                self._last_loaded_version = state.concurrency_version
                return state
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                _log.error(f"Corrupt state file: {e}, attempting backup restore")
                restored = self._restore_from_backup()
                if restored:
                    return restored
                return StateRoot.default()
        return StateRoot.default()

    def save(self, state: StateRoot, expected_version: int = None) -> StateSavedEvent:
        """
        Atomically save state to disk with concurrency protection.

        Args:
            state: The state to save
            expected_version: If provided, verifies no concurrent modification.
                              Raises ConcurrentModificationError if version mismatch.

        1. Auto-backup current state
        2. Optimistic concurrency check
        3. Write to .tmp file (under file lock)
        4. Atomic replace
        """
        _log.debug(f"Saving state to {self._state_path}")
        self._ensure_dirs()

        # Auto-backup
        self._auto_backup()

        # Optimistic concurrency check
        if expected_version is not None:
            current = self.load()
            if current.concurrency_version != expected_version:
                raise ConcurrentModificationError(
                    f"State modified concurrently: expected v{expected_version}, "
                    f"got v{current.concurrency_version}"
                )

        # Increment version
        state = state._bump_version()

        data = state.to_dict()
        data["meta"]["updated"] = datetime.now().isoformat()

        tmp_path = self._state_path.with_suffix('.tmp')

        with self._thread_lock:
            lock_acquired = self._acquire_lock()
            if not lock_acquired:
                _log.warning(f"save() 无法获取文件锁 (超时{self._LOCK_TIMEOUT}s)，强制写入")
            try:
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                tmp_path.replace(self._state_path)
                self._last_loaded_version = state.concurrency_version
            except OSError as e:
                _log.error(f"Failed to save state: {e}")
                if tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
                raise StateRepositoryError(f"Save failed: {e}") from e
            finally:
                if lock_acquired:
                    self._release_lock()

        return StateSavedEvent(
            chapter=state.progress.last_chapter,
            file_path=str(self._state_path)
        )

    def snapshot(self, chapter: int) -> Path:
        self._ensure_dirs()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        snap_path = self._snapshot_dir / f"ch{chapter:04d}_{ts}.json"
        with open(snap_path, 'w', encoding='utf-8') as f:
            json.dump(self.load().to_dict(), f, ensure_ascii=False, indent=2)
        _log.info(f"Snapshot saved: {snap_path}")
        self._cleanup_snapshots()
        return snap_path

    def rollback(self, chapter: int) -> tuple[StateRoot, RollbackEvent]:
        snapshots = sorted(self._snapshot_dir.glob("ch*.json"))
        if not snapshots:
            raise StateRepositoryError("No snapshots available for rollback")
        target = None
        for snap in reversed(snapshots):
            ch_str = snap.stem.split('_')[0][2:]
            try:
                if int(ch_str) <= chapter:
                    target = snap
                    break
            except ValueError:
                continue
        if target is None:
            raise StateRepositoryError(f"No snapshot found for chapter <= {chapter}")
        _log.warning(f"Rolling back to snapshot: {target}")
        with open(target, 'r', encoding='utf-8') as f:
            data = json.load(f)
        state = StateRoot.from_dict(data)
        self.save(state)
        event = RollbackEvent(
            reason=f"Manual rollback to chapter {chapter}",
            from_chapter=chapter,
            to_chapter=state.progress.last_chapter,
        )
        return state, event

    @property
    def last_loaded_version(self) -> int:
        return self._last_loaded_version

    # ─── Backup ───

    def _auto_backup(self):
        if not self._state_path.exists():
            return
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self._backup_dir / f"state_{ts}.json"
        try:
            shutil.copy2(str(self._state_path), str(backup_path))
        except OSError as e:
            _log.debug(f"Auto-backup skipped: {e}")
        # Cleanup old backups
        backups = sorted(self._backup_dir.glob("state_*.json"), key=lambda p: p.stat().st_mtime)
        while len(backups) > self._MAX_SNAPSHOTS:
            backups.pop(0).unlink(missing_ok=True)

    def _restore_from_backup(self) -> Optional[StateRoot]:
        backups = sorted(self._backup_dir.glob("state_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        for backup in backups:
            try:
                data = json.loads(backup.read_text(encoding='utf-8'))
                _log.warning(f"Restored state from backup: {backup.name}")
                return StateRoot.from_dict(data)
            except Exception:
                continue
        return None

    # ─── Private helpers ───

    def _ensure_dirs(self):
        self.book_dir.mkdir(parents=True, exist_ok=True)
        self._tmp_dir.mkdir(exist_ok=True)
        self._snapshot_dir.mkdir(exist_ok=True)
        self._backup_dir.mkdir(exist_ok=True)

    def _cleanup_snapshots(self):
        snapshots = sorted(self._snapshot_dir.glob("ch*.json"),
                          key=lambda p: p.stat().st_mtime)
        while len(snapshots) > self._MAX_SNAPSHOTS:
            oldest = snapshots.pop(0)
            oldest.unlink(missing_ok=True)
            _log.debug(f"Cleaned old snapshot: {oldest}")
