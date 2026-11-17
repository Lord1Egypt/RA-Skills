#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_transaction.py — [DEPRECATED] 单章事务边界

逻辑已合并到 application/unit_of_work.py (UnifiedUnitOfWork).
此文件保留用于向后兼容导入，新代码请使用 UnitOfWork.
"""

import json
import logging
import copy
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any, Tuple

_log = logging.getLogger("chapter_transaction")


class ChapterTransaction:
    """单章事务 — 所有副作用在一个 Promise 链内"""

    def __init__(self, book_dir: str, novel_state, chapter: int):
        self.book_dir = Path(book_dir)
        self.state = novel_state
        self.chapter = chapter
        self._promises: List[Tuple[Callable, Callable]] = []
        self._state_snapshot: Optional[Dict] = None
        self._committed = False

    # ========== 注册副作用操作 ==========

    def write_file(self, rel_path: str, content: str):
        """注册文件写入（自动备份原文件）"""
        path = self.book_dir / rel_path
        backup = path.with_suffix(path.suffix + ".bak")

        def commit():
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                path.rename(backup)
            path.write_text(content, encoding="utf-8")

        def rollback():
            if backup.exists():
                if path.exists():
                    path.unlink()
                backup.rename(path)
            elif path.exists():
                path.unlink()

        self._promises.append((commit, rollback))
        _log.debug(f"TXN: 注册写入 {rel_path}")

    def write_text(self, rel_path: str, text: str):
        """注册文本文件写入（正文类，跳过备份，用 .tmp 原子写）
        v1.6: 修复 Windows rename 冲突 — 先删除目标文件
        """
        path = self.book_dir / rel_path
        tmp_path = path.with_suffix(path.suffix + ".tmp")

        def commit():
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path.write_text(text, encoding="utf-8")
            # Windows 兼容: rename 前先删除已存在的目标文件
            if path.exists():
                path.unlink()
            tmp_path.rename(path)

        def rollback():
            if tmp_path.exists():
                tmp_path.unlink()
            if path.exists():
                path.unlink()

        self._promises.append((commit, rollback))

    def update_state(self, key: str, new_value: Any, old_value: Any = None):
        """注册状态变更（带快照，确保幂等）"""
        if old_value is None:
            old_value = copy.deepcopy(self.state._NovelState__state.get(key, {}))

        def commit():
            self.state._NovelState__state[key] = new_value

        def rollback():
            self.state._NovelState__state[key] = old_value

        self._promises.append((commit, rollback))

    def mark_chapter_done(self, chapter: int):
        """注册章节完成标记（纳入事务 Promise 链 — 第三轮审查修复）"""
        progress = self.state._NovelState__state.setdefault("progress", {})
        old_written = progress.get("written", 0)
        old_last = progress.get("last_chapter", 0)
        old_list = list(progress.get("written_list", []))
        def commit():
            progress["written"] = chapter
            progress["last_chapter"] = chapter
            wl = progress.setdefault("written_list", [])
            if chapter not in wl:
                wl.append(chapter)
        def rollback():
            progress["written"] = old_written
            progress["last_chapter"] = old_last
            progress["written_list"] = old_list
        self._promises.append((commit, rollback))

    def update_tracker(self, tracker_rel_path: str, line_prefix: str, new_line: str):
        """注册追踪文件追加（带去重，解决非幂等问题）

        如果文件中已存在包含 line_prefix 的行，则跳过追加。
        """
        path = self.book_dir / tracker_rel_path
        original_content = ""

        def commit():
            nonlocal original_content
            if path.exists():
                original_content = path.read_text(encoding="utf-8")
                # 去重检查
                if line_prefix and line_prefix in original_content:
                    _log.debug(f"TXN: 追踪去重跳过 {tracker_rel_path} ({line_prefix})")
                    return
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as f:
                f.write(new_line + "\n")

        def rollback():
            if not original_content:
                # 文件之前不存在 → 删除
                if path.exists():
                    path.unlink()
            else:
                # 恢复原始内容
                path.write_text(original_content, encoding="utf-8")

        self._promises.append((commit, rollback))

    # ========== 事务控制 ==========

    def __enter__(self):
        # 保存 state 快照
        self._state_snapshot = copy.deepcopy(self.state._NovelState__state)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback(exc_val)
        # 不阻止异常传播 — 让上层决定是否继续
        return False

    def commit(self):
        """提交所有注册的操作"""
        if self._committed:
            return
        _log.info(f"TXN: commit ch{self.chapter} ({len(self._promises)} ops)")
        for commit_fn, _ in self._promises:
            try:
                commit_fn()
            except Exception as e:
                _log.error(f"TXN: commit 操作失败 ({e})，全部回滚")
                self.rollback(e)
                raise RuntimeError(f"事务提交失败: {e}") from e
        # 最终写 state.json
        try:
            self.state.save()
        except Exception as e:
            _log.error(f"TXN: state 保存失败 ({e})，全部回滚")
            self.rollback(e)
            raise
        self._committed = True
        _log.info(f"TXN: ch{self.chapter} 提交成功")

    def rollback(self, reason: Optional[Exception] = None):
        """回滚所有已注册的操作（逆序）"""
        if self._committed:
            return
        _log.warning(f"TXN: rollback ch{self.chapter} ({reason})")
        # 逆序回滚
        for commit_fn, rollback_fn in reversed(self._promises):
            try:
                rollback_fn()
            except Exception as e:
                _log.error(f"TXN: rollback 操作失败 ({e})")
        # 恢复 state 快照
        if self._state_snapshot is not None:
            self.state._NovelState__state = copy.deepcopy(self._state_snapshot)
            _log.info("TXN: state 已从快照恢复")
        _log.info(f"TXN: ch{self.chapter} 回滚完成")


# ===== 替代原有的 mark_chapter_done（幂等版本） =====
def mark_chapter_idempotent(state, chapter: int) -> bool:
    """幂等版标记章节完成 — written 统一为 int，written_list 用于去重"""
    progress = state._state.setdefault("progress", {})
    last_ch = progress.get("last_chapter", 0)
    if chapter <= last_ch:
        _log.warning(f"幂等跳过 ch{chapter}")
        return False
    # 统一: written 为 int（已完成章节数），written_list 为 list（去重用）
    wl = progress.setdefault("written_list", [])
    if chapter in wl:
        _log.warning(f"幂等跳过 ch{chapter}（已在 written_list 中）")
        return False
    wl.append(chapter)
    progress["written"] = chapter  # int
    progress["written_list"] = wl   # list
    progress["last_chapter"] = chapter
    return True
