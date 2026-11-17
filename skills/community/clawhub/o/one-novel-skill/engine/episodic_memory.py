#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
episodic_memory.py — 情节记忆（剧集记忆）

所有已完成的章节和事件的历史记录，支持持久化。
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

_log = logging.getLogger("episodic_memory")


class EpisodicMemory:
    """情节记忆 — 所有已完成的章节和事件"""

    def __init__(self, book_dir: str = ""):
        self._episodes: List[Dict] = []
        self._book_dir = Path(book_dir) if book_dir else None
        self._mem_file = self._book_dir / "追踪/episodic_memory.json" if self._book_dir else None
        self._max_entries = 50

    # ── 内存操作 ──────────────────────────────

    def record(self, chapter: int, summary: str, key_events: List[str] = None):
        """记录一条章节记忆"""
        self._episodes.append({
            "chapter": chapter,
            "summary": summary,
            "events": key_events or [],
        })
        # 持久化
        self._save()

    def get_recent(self, n: int = 5) -> str:
        """获取最近 n 章的记忆文本"""
        recent = self._episodes[-n:]
        if not recent:
            return ""
        parts = [f"最近 {len(recent)} 章回顾:"]
        for e in recent:
            parts.append(f"  ch{e['chapter']}: {e['summary'][:100]}")
        return "\n".join(parts)

    def get_relevant(self, chapter: int, count: int = 5) -> str:
        """获取指定章节之前的记忆"""
        recent = [e for e in self._episodes if e["chapter"] < chapter][-count:]
        if not recent:
            return ""
        parts = [f"第{e['chapter']}章: {e['summary'][:100]}" for e in recent]
        return "\n".join(parts)

    def search(self, keyword: str) -> List[Dict]:
        """搜索情节记忆"""
        return [e for e in self._episodes if keyword in str(e)]

    # ── 持久化 ──────────────────────────────

    def _save(self):
        """将内存同步到文件"""
        if not self._mem_file:
            return
        try:
            self._mem_file.parent.mkdir(parents=True, exist_ok=True)
            data = {"chapters": []}
            for ep in self._episodes[-self._max_entries:]:
                data["chapters"].append({
                    "chapter": ep["chapter"],
                    "summary": ep["summary"][:200],
                })
            self._mem_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            _log.warning(f"EpisodicMemory 持久化失败: {e}")

    def load(self):
        """从文件加载记忆"""
        if not self._mem_file or not self._mem_file.exists():
            return
        try:
            data = json.loads(self._mem_file.read_text(encoding="utf-8"))
            for c in data.get("chapters", []):
                self._episodes.append({
                    "chapter": c["chapter"],
                    "summary": c.get("summary", ""),
                    "events": [],
                })
        except Exception as e:
            _log.warning(f"EpisodicMemory 加载失败: {e}")

    def to_dict(self) -> dict:
        return {"episodes": self._episodes}

    def load_from_dict(self, data: dict):
        self._episodes = data.get("episodes", [])
