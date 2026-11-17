#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_memory.py — 语义记忆

从情节记忆中提炼的高层创作洞察（长期记忆）。
"""

import logging
from typing import List, Dict, Optional

_log = logging.getLogger("semantic_memory")


class SemanticMemory:
    """语义记忆 — 从情节记忆中提炼的高层创作洞察"""

    def __init__(self):
        self._insights: List[Dict] = []
        self._max_insights = 50

    def add(self, insight: str, source_chapter: int = 0):
        """添加一条创作洞察"""
        self._insights.append({
            "content": insight,
            "source": f"ch{source_chapter}" if source_chapter else "system",
        })
        # 限制容量
        if len(self._insights) > self._max_insights:
            self._insights = self._insights[-self._max_insights:]

    def get_all(self) -> str:
        """获取所有洞察文本"""
        if not self._insights:
            return ""
        parts = ["【语义记忆（创作洞察）】"]
        for ins in self._insights[-20:]:
            parts.append(f"  - {ins['content']} ({ins['source']})")
        return "\n".join(parts)

    def search(self, keyword: str) -> List[str]:
        """搜索相关洞察"""
        return [i["content"] for i in self._insights if keyword in i["content"]]

    def to_dict(self) -> dict:
        return {"insights": self._insights}

    def load_from_dict(self, data: dict):
        self._insights = data.get("insights", [])
