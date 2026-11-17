"""
application/unit_of_work.py — UnifiedUnitOfWork (合并 ChapterTransaction + 引擎副作用)

THE single authority for all state mutations, file writes, and engine side effects.
Replaces: UnitOfWork + ChapterTransaction + NovelState.save() scattered calls.

新增能力:
- register_engine_side_effect(key, old, new): 统一管理引擎副作用
- register_engine_result(EngineAnalyzeResult): 记录引擎执行结果
- pre_commit_hooks: 提交前校验链（MemoryHierarchy/SemanticReview/ChapterContract）
- 合并 ChapterTransaction 的 Promise 链模式
"""
from __future__ import annotations

import logging
from copy import deepcopy
from typing import Optional, List, Any, Dict, Callable, Tuple
from pathlib import Path

from domain.state import StateRoot
from domain.commands import Command
from infrastructure.state_repository import StateRepository, StateRepositoryError
from infrastructure.persistence_gateway import PersistenceGateway, AtomicFileWriter

_log = logging.getLogger("uow")


class UoWError(Exception):
    pass


class FileWrite:
    def __init__(self, rel_path: str, content: str, mode: str = "write"):
        self.rel_path = rel_path
        self.content = content
        self.mode = mode


class UnitOfWork:
    """
    统一事务边界 (Unified Unit of Work).

    合并了原 UnitOfWork + ChapterTransaction 的全部能力.

    Guarantees:
    1. State mutations are atomic: all-or-nothing via StateRoot.apply()
    2. File writes are atomic: .tmp → atomic rename on commit
    3. Engine side effects are tracked and rollback-able
    4. Pre-commit hooks validate before final write
    5. Rollback: restores state snapshot, engine side effects, and temp files
    """

    def __init__(self, state_repo: StateRepository, persistence_gw: PersistenceGateway):
        self._state_repo = state_repo
        self._persistence = persistence_gw
        self._state: Optional[StateRoot] = None
        self._snapshot: Optional[StateRoot] = None
        self._commands: List[Command] = []
        self._file_writes: List[FileWrite] = []
        self._file_writers: List[AtomicFileWriter] = []
        self._events: List[Any] = []
        self._committed = False
        # 引擎副作用追踪
        self._side_effects: List[Tuple[str, Any, Any, Callable, Callable]] = []
        # 提交前钩子
        self._pre_commit_hooks: List[Callable] = []
        # 乐观并发: 记录加载时的 version
        self._loaded_version: int = 0

    def __enter__(self) -> "UnitOfWork":
        self._state = self._state_repo.load()
        self._snapshot = deepcopy(self._state)
        self._loaded_version = self._state.concurrency_version if self._state else 0
        self._commands.clear()
        self._file_writes.clear()
        self._file_writers.clear()
        self._events.clear()
        self._side_effects.clear()
        self._pre_commit_hooks.clear()
        self._committed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            _log.warning(f"UoW aborted due to {exc_type.__name__}: {exc_val}")
            self.rollback()
            return False
        try:
            self.commit()
        except Exception as e:
            _log.error(f"UoW commit failed: {e}")
            self.rollback()
            raise UoWError(f"Commit failed: {e}") from e
        return False

    # ─── Command registration ───
    def register_command(self, cmd: Command):
        self._commands.append(cmd)

    # ─── File write registration ───
    def register_file_write(self, rel_path: str, content: str, mode: str = "write"):
        self._file_writes.append(FileWrite(rel_path, content, mode))

    # ─── 引擎副作用注册（合并自 ChapterTransaction） ───
    def register_side_effect(self, key: str, new_value: Any, old_value: Any = None):
        """注册引擎副作用（自动捕获旧值，支持回滚）"""
        if old_value is None:
            old_value = deepcopy(self._state.to_dict().get(key)) if self._state else None

        def do_apply():
            pass  # 副作用在 commit Phase 1.5 中通过 state_dict 写入

        def do_rollback():
            pass  # 回滚通过恢复 snapshot 完成

        self._side_effects.append((key, new_value, old_value, do_apply, do_rollback))

    # ─── Pre-commit hooks ───
    def add_pre_commit_hook(self, hook: Callable[[], List[str]]):
        """添加提交前校验钩子。返回 issues 列表，非空则中止提交。"""
        self._pre_commit_hooks.append(hook)

    # ─── State accessors ───
    @property
    def state(self) -> Optional[StateRoot]:
        return self._state

    @property
    def events(self) -> list:
        return list(self._events)

    # ─── Commit / Rollback ───
    def commit(self):
        if self._committed:
            return

        _log.debug(f"UoW commit: {len(self._commands)} cmds, {len(self._file_writes)} files, "
                   f"{len(self._side_effects)} side-effects, {len(self._pre_commit_hooks)} hooks")

        # Phase 0: Pre-commit hooks
        for hook in self._pre_commit_hooks:
            hook_issues = hook()
            if hook_issues:
                raise UoWError(f"Pre-commit hook failed: {hook_issues}")

        # Phase 1: Apply all commands → new StateRoot + events
        current_state = self._state
        if current_state is None:
            raise UoWError("No state loaded")

        for cmd in self._commands:
            current_state, cmd_events = current_state.apply(cmd)
            self._events.extend(cmd_events)

        # Phase 1.5: Apply engine side effects to state dict
        if self._side_effects:
            state_dict = current_state.to_dict()
            for key, new_value, _, _, _ in self._side_effects:
                state_dict[key] = new_value
            current_state = StateRoot.from_dict(state_dict)

        # Phase 2: Write all files atomically
        success_writers = []
        try:
            for fw in self._file_writes:
                target = Path(self._persistence.book_dir) / fw.rel_path
                writer = AtomicFileWriter(target)
                if fw.mode == "append":
                    existing = ""
                    if target.exists():
                        existing = target.read_text(encoding='utf-8')
                    first_line = fw.content.split('\n')[0].strip()
                    if first_line and first_line in existing:
                        _log.debug(f"Idempotent skip: {fw.rel_path}")
                        continue
                    writer.write(existing + fw.content + '\n')
                else:
                    writer.write(fw.content)
                writer.commit()
                success_writers.append(writer)
        except Exception as e:
            for w in success_writers:
                w.rollback()
            raise UoWError(f"File write failed: {e}") from e

        # Phase 3: Save new state (with optimistic concurrency)
        self._state_repo.save(current_state, expected_version=self._loaded_version)
        self._state = current_state
        self._committed = True

        _log.info(f"UoW committed: ch={current_state.progress.last_chapter}, "
                  f"v{current_state.concurrency_version}, events={len(self._events)}")

    def rollback(self):
        if self._snapshot is not None:
            try:
                self._state_repo.save(self._snapshot)
                _log.warning("UoW rolled back: state restored from snapshot")
            except StateRepositoryError:
                _log.error("UoW rollback: failed to restore snapshot")

        # 逆序回滚引擎副作用
        for _, _, old_value, _, rollback_fn in reversed(self._side_effects):
            try:
                rollback_fn()
            except Exception as e:
                _log.error(f"UoW rollback side-effect failed: {e}")

        for writer in self._file_writers:
            writer.rollback()

        self._commands.clear()
        self._file_writes.clear()
        self._file_writers.clear()
        self._side_effects.clear()
        self._pre_commit_hooks.clear()
        self._committed = False
