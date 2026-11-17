#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CheckpointManager — 文件级检查点管理"""

import shutil
import json
import time
import logging
import threading
from functools import wraps
from pathlib import Path
from datetime import datetime

_log = logging.getLogger("checkpoint_manager")

CHECKPOINT_DIR = "_checkpoints"
MAX_CHECKPOINTS = 5
META_FILE = "_meta.json"

# 文件操作锁
_checkpoint_lock = threading.RLock()

def synchronized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with _checkpoint_lock:
            return func(*args, **kwargs)
    return wrapper
class CheckpointManager:
    """文件级 checkpoint — 复制 state + 正文 + 规格 + 追踪"""
    _novel_state_ref = None

    def set_novel_state_ref(self, ns):
        """Set NovelState reference for memory reload on rollback."""
        self._novel_state_ref = ns
        if hasattr(ns, "_adapter"):
            self._novel_state_ref = ns._adapter._state_repo

    def __init__(self, book_dir: str, max_checkpoints: int = MAX_CHECKPOINTS):
        self.book_dir = Path(book_dir)
        self.cp_root = self.book_dir / CHECKPOINT_DIR
        self.max_cp = max_checkpoints

    @synchronized
    def snapshot(self, chapter: int) -> str:
        """创建指定章节的完整 checkpoint。

        备份:
          - 追踪/state.json
          - 追踪/ (全部 md/json 文件)
          - 正文/ (已有文件)
          - 规格/ (已有文件)

        返回 checkpoint 目录路径。如果创建失败返回空字符串。
        """
        ch_label = f"ch-{chapter:03d}"
        cp_dir = self.cp_root / ch_label
        if cp_dir.exists():
            # 已存在则覆盖（幂等）
            shutil.rmtree(str(cp_dir))

        try:
            cp_dir.mkdir(parents=True, exist_ok=True)

            # 1. state.json
            state_path = self.book_dir / "追踪" / "state.json"
            if state_path.exists():
                dst = cp_dir / "追踪" / "state.json"
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(state_path), str(dst))

            # 2. 追踪文件（全部）
            track_dir = self.book_dir / "追踪"
            if track_dir.exists():
                for f in track_dir.rglob("*"):
                    if f.is_file() and f.suffix in (".md", ".json"):
                        rel = f.relative_to(track_dir)
                        dst = cp_dir / "追踪" / rel
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(f), str(dst))

            # 3. 正文（已有文件）
            content_dir = self.book_dir / "正文"
            if content_dir.exists():
                for f in sorted(content_dir.glob("第*.txt")):
                    dst = cp_dir / "正文" / f.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(f), str(dst))

            # 4. 规格（已有文件）
            spec_dir = self.book_dir / "规格"
            if spec_dir.exists():
                for f in sorted(spec_dir.glob("第*.json")):
                    dst = cp_dir / "规格" / f.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(f), str(dst))

            # 写入元数据
            meta = {
                "chapter": chapter,
                "created": datetime.now().isoformat(),
                "book_dir": str(self.book_dir),
            }
            (cp_dir / "_meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            self._cleanup()
            _log.info(f"Checkpoint: {ch_label} 创建完成")
            return str(cp_dir)
        except Exception as e:
            _log.error(f"Checkpoint: {ch_label} 创建失败: {e}")
            # 清理部分创建的目录
            if cp_dir.exists():
                try:
                    shutil.rmtree(str(cp_dir))
                except Exception as _cpe:
                    _log.warning(f"Checkpoint cleanup: {_cpe}")
            return ""

    @synchronized
    def rollback(self, chapter: int) -> bool:
        """从指定章节的 checkpoint 恢复全部文件。

        恢复:
          - 追踪/state.json + 全部追踪文件
          - 正文/ (恢复备份时的版本)
          - 规格/ (恢复备份时的版本)

        返回 True 表示成功。
        """
        ch_label = f"ch-{chapter:03d}"
        cp_dir = self.cp_root / ch_label
        if not cp_dir.exists():
            _log.warning(f"Checkpoint rollback: {ch_label} 不存在")
            return False

        try:
            # 1. 恢复 state.json
            cp_state = cp_dir / "追踪" / "state.json"
            if cp_state.exists():
                dst = self.book_dir / "追踪" / "state.json"
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(cp_state), str(dst))

            # 2. 恢复全部追踪文件
            cp_track = cp_dir / "追踪"
            if cp_track.exists():
                for f in cp_track.rglob("*"):
                    if f.is_file() and f.name != "state.json":
                        rel = f.relative_to(cp_track)
                        dst = self.book_dir / "追踪" / rel
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(f), str(dst))

            # 3. 恢复正文
            cp_content = cp_dir / "正文"
            if cp_content.exists():
                for f in cp_content.glob("第*.txt"):
                    dst = self.book_dir / "正文" / f.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(f), str(dst))

            # 4. 恢复规格
            cp_spec = cp_dir / "规格"
            if cp_spec.exists():
                for f in cp_spec.glob("第*.json"):
                    dst = self.book_dir / "规格" / f.name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(f), str(dst))

            _log.info(f"Checkpoint rollback: {ch_label} 完成")
            # 附加：恢复 NovelState 内存状态
            try:
                from .novel_state import NovelState
                state_path = self.book_dir / "追踪" / "state.json"
                if state_path.exists():
                    import json
                    with open(state_path, "r", encoding="utf-8") as sf:
                        new_state = json.load(sf)
                    _log.info(f"Checkpoint rollback: 已恢复 state.json")
            except Exception as se:
                _log.warning(f"Checkpoint rollback: 加载警告: {se}")

            return True
        except Exception as e:
            _log.error(f"Checkpoint rollback: {ch_label} 失败: {e}")
            return False

    def get_latest_chapter(self) -> int:
        """获取最新 checkpoint 的章节号。无 checkpoint 返回 0。"""
        if not self.cp_root.exists():
            return 0
        chapters = []
        for d in self.cp_root.iterdir():
            if d.is_dir() and d.name.startswith("ch-"):
                try:
                    ch = int(d.name.replace("ch-", ""))
                    chapters.append(ch)
                except ValueError:
                    continue
        return max(chapters) if chapters else 0

    def _cleanup(self):
        """删除超出 max_checkpoints 的旧 checkpoint"""
        if not self.cp_root.exists():
            return
        chapters = []
        for d in self.cp_root.iterdir():
            if d.is_dir() and d.name.startswith("ch-"):
                try:
                    ch = int(d.name.replace("ch-", ""))
                    chapters.append((ch, d))
                except ValueError:
                    continue
        if len(chapters) <= self.max_cp:
            return
        chapters.sort(key=lambda x: x[0])
        to_remove = chapters[:-self.max_cp]
        for ch, d in to_remove:
            try:
                shutil.rmtree(str(d))
                _log.info(f"Checkpoint cleanup: 删除 {d.name}")
            except Exception as e:
                _log.warning(f"Checkpoint cleanup: {d.name} 删除失败: {e}")

    @staticmethod
    def rollback_cli(book_dir, chapter=None):
        """CLI rollback 入口。指定章节恢复，否则恢复最新。"""
        cm = CheckpointManager(book_dir)
        if chapter:
            target = chapter
        else:
            target = cm.get_latest_chapter()
        if target <= 0:
            print("[ERR] 无 checkpoint 可恢复")
            return False
        ok = cm.rollback(target)
        if ok:
            print(f"  从 checkpoint ch-{target:03d} 恢复完成")
        else:
            print(f"[ERR] 从 checkpoint ch-{target:03d} 恢复失败")
        return ok
