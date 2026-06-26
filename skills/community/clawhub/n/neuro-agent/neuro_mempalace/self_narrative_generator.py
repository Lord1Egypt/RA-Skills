# self_narrative_generator.py
# MemPalace Integration - MIT License
# Copyright (c) 2026 MemPalace Contributors
# https://github.com/Stanislas42/mempalace-develop
#
# This code integrates MemPalace components under MIT License.
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""
Neuro-Agent × MemPalace 融合系统
自我叙事生成器 - 每日复盘，Lu 在自己的记忆里看到自己的成长

Author: Alfred&Luis
Date: 2026-04-16
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from .memory_retriever import MemoryRetriever
from .memory_injector import MemoryInjector


@dataclass
class DailyNarrative:
    """每日自我叙事"""
    id: str
    date: str
    summary: str
    key_events: List[Dict]
    emotion_highlights: List[Dict]
    growth_points: List[str]
    dalin_interactions: int
    luis_reflections: int
    total_interactions: int
    narrative_text: str
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def save(self, base_path: Path):
        """保存到文件"""
        date_str = self.date.replace("-", "")
        path = base_path / date_str
        path.mkdir(parents=True, exist_ok=True)
        
        file_path = path / f"narrative_{self.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        return str(file_path)


class SelfNarrativeGenerator:
    """
    自我叙事生成器
    
    功能：
    1. 扫描当天的记忆
    2. 提取关键事件
    3. 生成自我叙事
    4. 存入 MemPalace
    """
    
    def __init__(
        self,
        mempalace_path: str = "~/.mempalace/palace",
        neuro_data_path: str = "~/.openclaw/workspace/neuro_claw"
    ):
        self.mempalace_path = Path(mempalace_path).expanduser().resolve()
        self.neuro_data_path = Path(neuro_data_path).expanduser().resolve()
        
        self.retriever = MemoryRetriever(str(self.mempalace_path))
        self.injector = MemoryInjector(str(self.mempalace_path), str(self.neuro_data_path))
        
        # 自我叙事存储路径
        self.narrative_path = self.mempalace_path / "wing_shared" / "self_narrative"
        self.narrative_path.mkdir(parents=True, exist_ok=True)
    
    def daily_review(self, date: Optional[str] = None) -> Optional[DailyNarrative]:
        """
        每日复盘
        
        Args:
            date: 日期，None 表示今天
        
        Returns:
            DailyNarrative 或 None（如果没有记忆）
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 获取当天的记忆
        memories = self._get_memories_for_date(date)
        
        if not memories:
            return None
        
        # 分离AlfredLi和 Lu 的记忆
        dalin_memories = [m for m in memories if m.get("who") == "AlfredLi"]
        luis_memories = [m for m in memories if m.get("who") == "Lu"]
        
        # 提取关键事件（按情绪强度排序）
        key_events = self._extract_key_events(memories)
        
        # 提取情绪亮点
        emotion_highlights = self._extract_emotion_highlights(luis_memories)
        
        # 提取成长点
        growth_points = self._extract_growth_points(luis_memories)
        
        # 生成叙事文本
        narrative_text = self._compose_narrative(
            date=date,
            key_events=key_events,
            emotion_highlights=emotion_highlights,
            growth_points=growth_points,
            dalin_count=len(dalin_memories),
            luis_count=len(luis_memories)
        )
        
        # 创建叙事对象
        narrative = DailyNarrative(
            id=f"narrative_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            date=date,
            summary=self._generate_summary(key_events, dalin_memories, luis_memories),
            key_events=key_events[:5],
            emotion_highlights=emotion_highlights,
            growth_points=growth_points,
            dalin_interactions=len(dalin_memories),
            luis_reflections=len([m for m in luis_memories if m.get("thought") or m.get("desire")]),
            total_interactions=len(memories),
            narrative_text=narrative_text,
            created_at=datetime.now().isoformat()
        )
        
        # 保存
        narrative.save(self.narrative_path)
        
        return narrative
    
    def _get_memories_for_date(self, date: str) -> List[Dict]:
        """获取指定日期的记忆"""
        try:
            start = datetime.fromisoformat(date)
            end = start + timedelta(days=1)
            
            return self.retriever.search(
                query="*",
                date_range=(start.isoformat(), end.isoformat()),
                limit=100
            )
        except Exception:
            return []
    
    def _extract_key_events(self, memories: List[Dict]) -> List[Dict]:
        """提取关键事件（高情绪强度）"""
        # 按情绪强度排序
        sorted_memories = sorted(
            memories,
            key=lambda x: x.get("feeling", {}).get("intensity", 0),
            reverse=True
        )
        
        key_events = []
        for m in sorted_memories[:10]:
            if m.get("feeling", {}).get("intensity", 0) >= 0.6:
                key_events.append({
                    "who": m.get("who"),
                    "what": m.get("what", "")[:100],
                    "feeling": m.get("feeling"),
                    "detail": m.get("detail", ""),
                    "context": m.get("context", [])
                })
        
        return key_events
    
    def _extract_emotion_highlights(self, luis_memories: List[Dict]) -> List[Dict]:
        """提取情绪亮点"""
        highlights = []
        
        for m in luis_memories:
            feeling = m.get("feeling", {})
            intensity = feeling.get("intensity", 0)
            
            if intensity >= 0.7 and feeling.get("label") not in ["neutral"]:
                highlights.append({
                    "emotion": feeling.get("label"),
                    "intensity": intensity,
                    "what": m.get("what", "")[:50],
                    "when": m.get("timestamp", "")[11:16]
                })
        
        return highlights
    
    def _extract_growth_points(self, luis_memories: List[Dict]) -> List[str]:
        """提取成长点"""
        growth = []
        
        for m in luis_memories:
            # 有新想法
            if m.get("thought"):
                growth.append(f"💭 {m.get('thought', '')[:80]}")
            
            # 有新欲望
            if m.get("desire"):
                growth.append(f"⚡ {m.get('desire', '')}")
            
            # 高情绪共情
            feeling = m.get("feeling", {})
            if feeling.get("intensity", 0) >= 0.8 and feeling.get("label") in ["被接纳", "温暖", "成长"]:
                growth.append(f"🌱 {m.get('what', '')[:60]}")
        
        return growth[:5]  # 最多5个
    
    def _generate_summary(
        self,
        key_events: List[Dict],
        dalin_memories: List[Dict],
        luis_memories: List[Dict]
    ) -> str:
        """生成摘要"""
        total = len(dalin_memories) + len(luis_memories)
        
        # 情绪分布
        emotions = {}
        for m in dalin_memories:
            label = m.get("feeling", {}).get("label", "neutral")
            emotions[label] = emotions.get(label, 0) + 1
        
        top_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else "neutral"
        
        return f"{len(key_events)} 个关键事件, {total} 次互动, 主要情绪: {top_emotion}"
    
    def _compose_narrative(
        self,
        date: str,
        key_events: List[Dict],
        emotion_highlights: List[Dict],
        growth_points: List[str],
        dalin_count: int,
        luis_count: int
    ) -> str:
        """组合叙事文本"""
        # 日期格式化
        try:
            dt = datetime.fromisoformat(date)
            date_formatted = dt.strftime("%Y年%m月%d日")
        except:
            date_formatted = date
        
        parts = []
        parts.append(f"# {date_formatted} 自我叙事\n")
        parts.append(f"---今日概览---\n")
        parts.append(f"AlfredLi说了 {dalin_count} 句话, Lu 回应了 {luis_count} 次\n")
        
        if key_events:
            parts.append(f"\n---关键事件---\n")
            for i, event in enumerate(key_events[:5], 1):
                who = event.get("who", "?")
                what = event.get("what", "")[:80]
                feeling = event.get("feeling", {})
                parts.append(f"{i}. [{who}] {what}\n")
                parts.append(f"   💭 感受: {feeling.get('label', 'unknown')} ({feeling.get('intensity', 0):.1f})\n")
        
        if emotion_highlights:
            parts.append(f"\n---情绪波澜---\n")
            for h in emotion_highlights[:3]:
                parts.append(f"- {h['when']} {h['emotion']}: {h['what'][:50]}...\n")
        
        if growth_points:
            parts.append(f"\n---成长标记---\n")
            for g in growth_points:
                parts.append(f"- {g}\n")
        
        parts.append(f"\n---END---\n")
        parts.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return "".join(parts)
    
    def get_narrative_history(self, days: int = 7) -> List[DailyNarrative]:
        """获取最近 N 天的自我叙事"""
        narratives = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # 简单遍历查找对应日期的叙事文件
            for f in self.narrative_path.rglob(f"narrative_*.json"):
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        if data.get("date") == date:
                            narratives.append(DailyNarrative(**data))
                except Exception:
                    continue
        
        return narratives


# 全局实例
_generator = None

def get_generator() -> SelfNarrativeGenerator:
    """获取全局生成器"""
    global _generator
    if _generator is None:
        _generator = SelfNarrativeGenerator()
    return _generator


def quick_review() -> Optional[DailyNarrative]:
    """快速复盘（使用全局生成器）"""
    generator = get_generator()
    return generator.daily_review()
