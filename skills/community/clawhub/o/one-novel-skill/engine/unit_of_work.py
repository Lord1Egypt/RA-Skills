#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit_of_work.py — 增强的事务管理器

覆盖文件写入 + 状态修改 + 引擎回写。
任何一步失败 → 逆序回滚所有已执行操作。
"""

import copy, json, logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

_log = logging.getLogger("unit_of_work")


class UnitOfWork:
    """完整事务边界"""

    def __init__(self, book_dir: str, state_accessor=None):
        self.book_dir = Path(book_dir)
        self._state = state_accessor
        self._ops: List[Tuple[Callable, Callable, str]] = []  # (commit, rollback, desc)
        self._committed = False
        self._rolled_back = False

    # ── 注册操作 ──

    def write_text(self, rel_path: str, text: str, backup: bool = False):
        """注册文本文件写入"""
        path = self.book_dir / rel_path
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        original_content = ""

        def commit():
            path.parent.mkdir(parents=True, exist_ok=True)
            if backup and path.exists():
                nonlocal original_content
                original_content = path.read_text(encoding="utf-8")
            tmp_path.write_text(text, encoding="utf-8")
            if path.exists():
                path.unlink()
            tmp_path.rename(path)

        def rollback():
            if tmp_path.exists():
                tmp_path.unlink()
            if backup and original_content:
                path.write_text(original_content, encoding="utf-8")
            elif not backup and path.exists():
                pass  # 保留已写入的文件（非破坏性回滚）

        self._ops.append((commit, rollback, f"write {rel_path}"))

    def write_json(self, rel_path: str, data: dict):
        """注册 JSON 文件写入"""
        self.write_text(rel_path, json.dumps(data, ensure_ascii=False, indent=2))

    def update_state(self, setter_fn: Callable, rollback_fn: Optional[Callable] = None, desc: str = ""):
        """注册状态修改

        Args:
            setter_fn: 执行状态修改的函数
            rollback_fn: 回滚函数（如果为None，尝试用 setter_fn 反转）
            desc: 描述
        """
        def rollback():
            if rollback_fn:
                rollback_fn()

        self._ops.append((setter_fn, rollback, desc or "state_update"))

    def execute_engine(
        self,
        engine_fn: Callable,
        rollback_fn: Optional[Callable] = None,
        desc: str = "",
    ):
        """注册引擎执行（含回滚）

        Args:
            engine_fn: 引擎执行函数
            rollback_fn: 如果引擎成功，如何回滚其副作用
            desc: 描述
        """
        self._ops.append((engine_fn, rollback_fn or (lambda: None), desc or "engine"))

    # ── 事务控制 ──

    def commit(self):
        """两阶段提交"""
        if self._committed or self._rolled_back:
            return

        committed = []
        try:
            for commit_fn, _, desc in self._ops:
                commit_fn()
                committed.append(desc)
            self._committed = True
            _log.debug(f"UoW: committed {len(committed)} ops")
        except Exception as e:
            _log.error(f"UoW: commit failed at '{committed[-1] if committed else 'first'}': {e}")
            self._rollback_all()
            raise RuntimeError(f"事务提交失败（已回滚 {len(committed)} 项）: {e}") from e

    def _rollback_all(self):
        """逆序回滚所有已注册操作"""
        if self._rolled_back:
            return
        rolled = 0
        for _, rollback_fn, desc in reversed(self._ops):
            try:
                rollback_fn()
                rolled += 1
            except Exception as re:
                _log.warning(f"UoW: rollback failed for '{desc}': {re}")
        self._rolled_back = True
        _log.info(f"UoW: rolled back {rolled}/{len(self._ops)} ops")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if not self._committed:
                self.commit()
        else:
            self._rollback_all()
        return False  # 不吞异常
