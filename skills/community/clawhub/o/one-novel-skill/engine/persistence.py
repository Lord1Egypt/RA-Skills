"""
persistence.py — Unit of Work 事务管理器
Phase 2: 所有副作用的隔离区，commit 一起成功，rollback 一起撤销。
修复：原子写入（临时文件+重命名）、回滚异常不吞没、deepcopy异常兜底、save异常传播
"""
from pathlib import Path
from copy import deepcopy
from typing import Optional, List, Tuple
import logging

_log = logging.getLogger("persistence")


class UnitOfWork:
    """事务边界 — 封装文件写入 + 状态更新"""

    def __init__(self, novel_state):
        self.novel_state = novel_state
        # 状态快照（带异常兜底）
        try:
            self._state_snapshot = deepcopy(novel_state._state) if hasattr(novel_state, "_state") else {}
        except (TypeError, ValueError) as e:
            _log.error(f"UnitOfWork: deepcopy 失败 ({e})，降级为浅拷贝")
            self._state_snapshot = novel_state._state.copy() if hasattr(novel_state, "_state") and isinstance(novel_state._state, dict) else {}
        self._files_written: List[Tuple[Path, Optional[Path]]] = []  # (new_file, backup_file)
        self._committed = False

    def write_text_file(self, path: Path, content: str) -> bool:
        """原子写入: 临时文件+重命名，不如直接覆盖原文件以避免数据丢失"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        backup = None
        original_exists = path.exists()

        try:
            # 1. 备份原文件
            if original_exists:
                backup = path.with_suffix(path.suffix + ".bak")
                # 覆盖已有备份
                if backup.exists():
                    backup.unlink(missing_ok=True)
                path.rename(backup)

            # 2. 写入临时文件 + 重命名（原子操作）
            temp_path = path.with_suffix(path.suffix + ".tmp")
            temp_path.write_text(content, encoding="utf-8")
            temp_path.rename(path)

            self._files_written.append((path, backup))
            _log.debug(f"UnitOfWork: 写入成功 {path.name}")
            return True
        except Exception as e:
            _log.error(f"UnitOfWork.write_text_file 失败: {e}")
            # 恢复原文件
            if backup and backup.exists():
                if path.exists():
                    path.unlink(missing_ok=True)
                backup.rename(path)
            return False
        finally:
            # 清理临时文件
            temp_path = path.with_suffix(path.suffix + ".tmp")
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)

    def commit(self):
        """提交事务: 删除所有备份 + 保存状态"""
        if self._committed:
            return
        try:
            # 1. 删除备份
            for new_file, backup in self._files_written:
                if backup and backup.exists():
                    try:
                        backup.unlink(missing_ok=True)
                        _log.debug(f"UnitOfWork: 备份已删除 {backup.name}")
                    except OSError as e:
                        _log.warning(f"UnitOfWork: 备份删除失败 {backup}: {e}")

            # 2. 保存状态（捕获异常，传播到上层）
            if hasattr(self.novel_state, "save"):
                try:
                    self.novel_state.save()
                except Exception as e:
                    _log.error(f"UnitOfWork: novel_state.save() 失败: {e}")
                    raise  # 让上层感知提交失败

            self._committed = True
            _log.info("UnitOfWork: 提交成功")
        except Exception as e:
            _log.error(f"UnitOfWork commit 失败: {e}")
            raise

    def rollback(self):
        """回滚事务: 恢复所有备份，状态回退到快照"""
        if self._committed:
            _log.warning("UnitOfWork.rollback called after commit")
            return

        failed_rollbacks = []

        for new_file, backup in self._files_written:
            # 1. 删除新文件
            if new_file.exists():
                try:
                    new_file.unlink(missing_ok=True)
                except OSError as e:
                    failed_rollbacks.append(f"删除新文件失败 {new_file}: {e}")

            # 2. 恢复备份
            if backup and backup.exists():
                try:
                    backup.rename(new_file)
                except OSError as e:
                    failed_rollbacks.append(f"恢复备份失败 {backup} -> {new_file}: {e}")

        # 恢复状态快照
        if hasattr(self.novel_state, "_state"):
            self.novel_state._state = deepcopy(self._state_snapshot)
            _log.info("UnitOfWork: 状态已回滚")

        if failed_rollbacks:
            _log.error(f"UnitOfWork rollback 失败的文件: {'; '.join(failed_rollbacks)}")
        else:
            _log.info("UnitOfWork: 回滚完成")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器: 保留原异常，不覆盖"""
        try:
            if exc_type is not None:
                _log.info(f"UnitOfWork: 异常退出 ({exc_type.__name__})，回滚中")
                self.rollback()
            else:
                _log.info("UnitOfWork: 正常退出，提交中")
                self.commit()
        except Exception as e:
            _log.error(f"UnitOfWork __exit__ 失败: {e}")
            # 不覆盖原异常
            if exc_type is None:
                raise e from None
            # 原异常已存在，记录新异常但不覆盖
            _log.error(f"UnitOfWork: 原异常 ({exc_type.__name__}: {exc_val}) 被保留")
        # 不抑制异常传播
        return False
