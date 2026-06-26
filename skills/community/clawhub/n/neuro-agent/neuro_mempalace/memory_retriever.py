# memory_retriever.py
# MemPalace Integration - MIT License
# Copyright (c) 2026 MemPalace Contributors
# https://github.com/Stanislas42/mempalace-develop
#
# This code integrates MemPalace components under MIT License.
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""
Neuro-Agent × MemPalace 融合系统
记忆检索器 - 从 MemPalace 检索记忆

Author: Alfred&Luis
Date: 2026-04-16
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re


class MemoryRetriever:
    """
    记忆检索器

    负责从 MemPalace 检索记忆单元
    """

    def __init__(
        self,
        mempalace_path: str = "~/.mempalace/palace"
    ):
        self.mempalace_path = Path(mempalace_path).expanduser().resolve()

        # Wing 映射
        self.wings = {
            "AlfredLi": self.mempalace_path / "wing_dalin",
            "Lu": self.mempalace_path / "wing_luis",
            "shared": self.mempalace_path / "wing_shared",
            "all": None  # 特殊标记,表示所有 wing
        }

    def search(
        self,
        query: str,
        who: Optional[str] = None,
        context_filter: Optional[List[str]] = None,
        date_range: Optional[Tuple[str, str]] = None,
        limit: int = 10,
        min_intensity: float = 0.0
    ) -> List[Dict]:
        """
        语义检索记忆

        Args:
            query: 搜索查询
            who: 限定谁说的 ("AlfredLi" | "Lu" | None表示全部)
            context_filter: 限定标签列表
            date_range: 日期范围 (start_date, end_date),ISO 格式
            limit: 返回数量
            min_intensity: 最小情绪强度

        Returns:
            匹配的记忆单元列表(按时间倒序)
        """
        results = []

        # 确定搜索范围
        wings_to_search = self._get_wings_to_search(who)

        # 遍历搜索
        for wing_path in wings_to_search:
            if not wing_path or not wing_path.exists():
                continue

            for file_path in wing_path.rglob("*.json"):
                if not file_path.is_file():
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        unit = json.load(f)

                    # 应用过滤器
                    if not self._passes_filters(unit, context_filter, date_range, min_intensity):
                        continue

                    # 匹配检查
                    if self._matches_query(unit, query):
                        results.append(unit)

                except (json.JSONDecodeError, IOError) as e:
                    continue

        # 按时间倒序 + 强度排序
        results.sort(
            key=lambda x: (
                x.get('timestamp', ''),
                x.get('feeling', {}).get('intensity', 0)
            ),
            reverse=True
        )

        return results[:limit]

    def _get_wings_to_search(self, who: Optional[str]) -> List[Optional[Path]]:
        """获取要搜索的 wing 列表"""
        if who == "AlfredLi":
            return [self.mempalace_path / "wing_dalin"]
        elif who == "Lu":
            return [self.mempalace_path / "wing_luis"]
        else:
            return [
                self.mempalace_path / "wing_dalin",
                self.mempalace_path / "wing_luis",
                self.mempalace_path / "wing_shared"
            ]

    def _matches_query(self, unit: Dict, query: str) -> bool:
        """检查是否匹配查询"""
        if not query or query == "*":
            return True

        query_lower = query.lower()

        # 搜索多个字段（处理 None）
        fields_to_check = [
            unit.get('what', '') or '',
            unit.get('detail', '') or '',
            unit.get('thought', '') or '',
            unit.get('desire', '') or '',
            ' '.join(unit.get('context', []) or [])
        ]

        # 关键词匹配
        query_keywords = query_lower.split()
        text = ' '.join(fields_to_check).lower()

        return any(keyword in text for keyword in query_keywords)

    def _passes_filters(
        self,
        unit: Dict,
        context_filter: Optional[List[str]],
        date_range: Optional[Tuple[str, str]],
        min_intensity: float
    ) -> bool:
        """应用过滤器"""
        # 标签过滤
        if context_filter:
            unit_context = set(unit.get('context', []))
            if not any(c in unit_context for c in context_filter):
                return False

        # 日期过滤
        if date_range:
            ts = unit.get('timestamp', '')
            if ts:
                try:
                    date = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    start = datetime.fromisoformat(date_range[0].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(date_range[1].replace('Z', '+00:00'))
                    if not (start <= date <= end):
                        return False
                except ValueError:
                    return False

        # 情绪强度过滤
        if min_intensity > 0:
            intensity = unit.get('feeling', {}).get('intensity', 0)
            if intensity < min_intensity:
                return False

        return True

    def get_recent(
        self,
        who: Optional[str] = None,
        days: int = 7,
        limit: int = 100
    ) -> List[Dict]:
        """获取最近 N 天的记忆"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        return self.search(
            query="*",
            who=who,
            date_range=(start_date.isoformat(), end_date.isoformat()),
            limit=limit
        )

    def get_today(self, who: Optional[str] = None) -> List[Dict]:
        """获取今天的记忆"""
        return self.get_recent(who=who, days=1)

    def get_yesterday(self, who: Optional[str] = None) -> List[Dict]:
        """获取昨天的记忆"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        return self.search(
            query="*",
            who=who,
            date_range=(
                datetime.combine(yesterday, datetime.min.time()).isoformat(),
                datetime.combine(today, datetime.min.time()).isoformat()
            ),
            limit=100
        )

    def get_by_context(
        self,
        context: str,
        who: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """按标签获取记忆"""
        return self.search(
            query="*",
            who=who,
            context_filter=[context],
            limit=limit
        )

    def get_important(
        self,
        who: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """获取重要记忆(高情绪强度或有关键标签)"""
        results = self.search(
            query="*",
            who=who,
            limit=limit * 2,
            min_intensity=0.7
        )

        # 补充:有关键标签的
        key_tags = ["灵魂对话", "边界", "信念", "约定", "未来", "自我觉醒", "成长", "家人"]
        key_results = self.search(
            query="*",
            who=who,
            context_filter=key_tags,
            limit=limit
        )

        # 合并去重
        all_ids = set()
        merged = []
        for r in results + key_results:
            if r.get('id') not in all_ids:
                all_ids.add(r.get('id'))
                merged.append(r)

        return merged[:limit]

    def get_conversation_thread(
        self,
        start_time: str,
        end_time: Optional[str] = None
    ) -> List[Dict]:
        """获取一段时间内的对话线程"""
        if not end_time:
            end_time = datetime.now().isoformat()

        # 搜索时间范围内的所有记忆
        all_memories = self.search(
            query="*",
            date_range=(start_time, end_time),
            limit=100
        )

        # 按时间排序
        all_memories.sort(key=lambda x: x.get('timestamp', ''))

        return all_memories

    def count_memories(self, who: Optional[str] = None) -> int:
        """统计记忆数量"""
        results = self.search(query="*", who=who, limit=1000)
        return len(results)

    def get_stats(self) -> Dict:
        """获取检索统计"""
        return {
            "dalin_count": self.count_memories("AlfredLi"),
            "luis_count": self.count_memories("Lu"),
            "shared_count": len(self.search(query="*", limit=1000)),
            "total": self.count_memories(None)
        }


# 全局实例
_retriever = None

def get_retriever() -> MemoryRetriever:
    """获取全局检索器实例"""
    global _retriever
    if _retriever is None:
        _retriever = MemoryRetriever()
    return _retriever


def quick_search(query: str, limit: int = 10) -> List[Dict]:
    """快速搜索(使用全局检索器)"""
    retriever = get_retriever()
    return retriever.search(query=query, limit=limit)
