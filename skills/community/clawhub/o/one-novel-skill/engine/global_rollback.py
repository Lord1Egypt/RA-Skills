#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
global_rollback.py — 全局回滚上下文管理器

追踪整个章节生成过程中的所有副作用（文件写入/状态变更/引擎副作用），
确保任何异常都能触发完整的回滚。
"""

import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

_log = logging.getLogger("global_rollback")


class SideEffectTracker:
    """副作用追踪器"""

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self._written_files: List[Tuple[Path, Optional[Path]]] = []  # (path, backup_path)
        self._temp_files: List[Path] = []
        self._state_snapshot: Optional[Dict] = None
        self._rollback_actions: List[Tuple[str, Any]] = []

    def track_file_write(self, rel_path: str, content: str):
        """追踪文件写入"""
        path = self.book_dir / rel_path
        backup = None
        if path.exists():
            backup = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(str(path), str(backup))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self._written_files.append((path, backup))

    def track_temp_file(self, path: Path):
        """追踪临时文件"""
        self._temp_files.append(path)

    def track_state_snapshot(self, state_dict: Dict):
        """保存状态快照"""
        import copy
        self._state_snapshot = copy.deepcopy(state_dict)

    def register_rollback_action(self, name: str, action: Any):
        """注册自定义回滚操作"""
        self._rollback_actions.append((name, action))

    def rollback_all(self):
        """回滚所有追踪的副作用"""
        _log.warning(f"GlobalRollback: rolling back {len(self._written_files)} files, "
                     f"{len(self._temp_files)} temps, {len(self._rollback_actions)} actions")

        # 1. 恢复被覆盖的文件
        for path, backup in reversed(self._written_files):
            try:
                if backup and backup.exists():
                    if path.exists():
                        path.unlink()
                    backup.rename(path)
                elif path.exists():
                    path.unlink()
            except Exception as e:
                _log.error(f"GlobalRollback: failed to restore {path}: {e}")

        # 2. 清理临时文件
        for tmp in self._temp_files:
            try:
                if tmp.exists():
                    tmp.unlink(missing_ok=True)
            except Exception as e:
                _log.error(f"GlobalRollback: failed to clean {tmp}: {e}")

        # 3. 恢复状态快照
        if self._state_snapshot is not None:
            state_path = self.book_dir / "state.json"
            try:
                import json
                state_path.write_text(
                    json.dumps(self._state_snapshot, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
            except Exception as e:
                _log.error(f"GlobalRollback: failed to restore state: {e}")

        # 4. 执行自定义回滚操作
        for name, action in self._rollback_actions:
            try:
                if callable(action):
                    action()
                _log.debug(f"GlobalRollback: executed {name}")
            except Exception as e:
                _log.error(f"GlobalRollback: failed {name}: {e}")


class GlobalRollbackContext:
    """全局回滚上下文管理器

    用法:
        tracker = SideEffectTracker(book_dir)
        with GlobalRollbackContext(tracker):
            # 所有副作用操作
            tracker.track_file_write("正文/第005章.txt", text)
            # ...
        # 如果发生异常，自动回滚所有追踪的副作用
    """

    def __init__(self, tracker: SideEffectTracker, on_rollback: callable = None):
        self._tracker = tracker
        self._on_rollback = on_rollback
        self._has_exception = False

    def __enter__(self) -> SideEffectTracker:
        return self._tracker

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _log.error(f"GlobalRollback triggered by {exc_type.__name__}: {exc_val}")
            self._tracker.rollback_all()
            if self._on_rollback:
                self._on_rollback(exc_val)
            self._has_exception = True
        return False  # re-raise exception

    @property
    def rolled_back(self) -> bool:
        return self._has_exception
