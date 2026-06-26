"""
三层记忆系统 (Three-Layer Memory System) v1.0
===============================================
解决"记忆沉淀"的工程问题：文件量 vs 信息完整性

┌─────────────────────────────────────────────┐
│  第一层：情绪胶囊                              │
│  高情绪事件、矛盾点、自我暴露、决策点           │
│  → 精确，量小，随时可查                       │
├─────────────────────────────────────────────┤
│  第二层：每日摘要                              │
│  每天自动生成结构化摘要                        │
│  → 轻量，AI总结                              │
├─────────────────────────────────────────────┤
│  第三层：完整日志（可选）                       │
│  每轮对话原始记录                              │
│  → 信息完整，仅本地部署建议开启                │
└─────────────────────────────────────────────┘

触发记忆沉淀的不仅是情绪强度，还有：
- 决策点（用户做了一个选择，哪怕语气平静）
- 观点变化（"我不吃辣了"→ 偏好改变）
- 关系变化（用户第一次说谢谢、第一次叫Agent的名字）
- 异常行为（用户平时话多，今天突然沉默了）
"""

import os
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, ClassVar
from enum import Enum


class MemoryImportance(Enum):
    LOW = 1        # 日常，无特别
    MEDIUM = 2     # 值得记录
    HIGH = 3       # 重要事件
    CRITICAL = 4   # 关键事件


class MemoryLayer(Enum):
    CAPSULE = "capsule"       # 情绪胶囊（第一层）
    DAILY_SUMMARY = "daily"   # 每日摘要（第二层）
    FULL_LOG = "fulllog"       # 完整日志（第三层）


@dataclass
class MemoryEvent:
    """记忆事件"""
    id: str
    timestamp: str
    content: str
    importance: MemoryImportance
    layer: MemoryLayer
    tags: list = field(default_factory=list)

    # 附加信息
    user_emotion: str = ""
    agent_emotion: str = ""
    decisions: list = field(default_factory=list)
    outcome: str = ""

    # 关联
    related_capsule_id: Optional[str] = None
    source: str = "unknown"  # 来源：capsule_factory/yearning/self_narrative

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "timestamp": self.timestamp,
            "content": self.content,
            "importance": self.importance.value if isinstance(self.importance, MemoryImportance) else self.importance,
            "layer": self.layer.value if isinstance(self.layer, MemoryLayer) else self.layer,
            "tags": self.tags,
            "user_emotion": self.user_emotion,
            "agent_emotion": self.agent_emotion,
            "decisions": self.decisions,
            "outcome": self.outcome,
            "related_capsule_id": self.related_capsule_id,
            "source": self.source
        }
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MemoryEvent":
        d = dict(d)
        d["importance"] = MemoryImportance(d.get("importance", 2))
        d["layer"] = MemoryLayer(d.get("layer", "daily"))
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class ThreeLayerMemory:
    """
    三层记忆系统

    使用示例：

    # 本地部署（开三层）
    memory = ThreeLayerMemory(deployment="local")

    # 云端部署（只开两层）
    memory = ThreeLayerMemory(deployment="cloud")

    # 记录一个事件
    memory.record(
        content="用户分享了他的职业困惑",
        importance=MemoryImportance.HIGH,
        user_emotion="迷茫、焦虑",
        agent_emotion="关切",
        decisions=["先共情"],
        outcome="用户情绪缓和",
        tags=["职业", "迷茫"]
    )

    # 搜索记忆
    results = memory.search("职业")
    for r in results:
        print(f"[{r.importance.name}] {r.content}")

    # 获取每日摘要
    summary = memory.get_daily_summary("2026-04-14")

    # 生成结构化摘要（供自我叙事调用）
    structured = memory.generate_daily_summary("2026-04-14")
    """

    BASE_PATH: ClassVar[str] = "~/.openclaw/workspace/neuro_claw/memory"

    def __init__(
        self,
        base_path: Optional[str] = None,
        deployment: str = "cloud"
    ):
        self.base_path = os.path.expanduser(base_path or self.BASE_PATH)
        self.deployment = deployment

        self.capsule_path = os.path.join(self.base_path, "capsules")
        self.daily_path = os.path.join(self.base_path, "daily_summaries")
        self.fulllog_path = os.path.join(self.base_path, "full_logs")

        os.makedirs(self.capsule_path, exist_ok=True)
        os.makedirs(self.daily_path, exist_ok=True)
        if deployment == "local":
            os.makedirs(self.fulllog_path, exist_ok=True)

    # ─── 记录接口 ─────────────────────────────────────────────

    def record(
        self,
        content: str,
        importance: MemoryImportance,
        layer: MemoryLayer = None,
        user_emotion: str = "",
        agent_emotion: str = "",
        decisions: list = None,
        outcome: str = "",
        tags: list = None,
        related_capsule_id: str = None,
        source: str = "unknown",
        timestamp: str = None
    ) -> MemoryEvent:
        """
        记录一个记忆事件
        自动判断应该存储到哪一层
        """
        layer = layer or self._auto_select_layer(importance, user_emotion, decisions)
        timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")
        event_id = f"mem_{int(time.time()*1000)}"

        event = MemoryEvent(
            id=event_id,
            timestamp=timestamp,
            content=content,
            importance=importance,
            layer=layer,
            user_emotion=user_emotion,
            agent_emotion=agent_emotion,
            decisions=decisions or [],
            outcome=outcome,
            tags=tags or [],
            related_capsule_id=related_capsule_id,
            source=source
        )

        if layer == MemoryLayer.CAPSULE:
            self._append(self.capsule_path, event)
        elif layer == MemoryLayer.DAILY_SUMMARY:
            self._append(self.daily_path, event)
        elif layer == MemoryLayer.FULL_LOG:
            self._append(self.fulllog_path, event)

        return event

    def record_from_capsule(self, capsule_data: dict) -> MemoryEvent:
        """
        从情绪胶囊自动同步到记忆系统
        情绪胶囊创建时自动调用
        """
        content = capsule_data.get("content", {}).get("summary", str(capsule_data))
        
        # 判断重要性
        emotion = capsule_data.get("content", {}).get("emotion", {})
        intensity = emotion.get("intensity", 0.5)
        importance = MemoryImportance.HIGH if intensity > 0.7 else MemoryImportance.MEDIUM

        return self.record(
            content=content,
            importance=importance,
            layer=MemoryLayer.CAPSULE,
            user_emotion=emotion.get("label", ""),
            tags=capsule_data.get("tags", []),
            related_capsule_id=capsule_data.get("id"),
            source="capsule_factory"
        )

    # ─── 自动分层 ─────────────────────────────────────────────

    def _auto_select_layer(
        self,
        importance: MemoryImportance,
        user_emotion: str,
        decisions: list
    ) -> MemoryLayer:
        """自动判断应该存储到哪一层"""
        # CRITICAL / HIGH → 情绪胶囊
        if importance in (MemoryImportance.CRITICAL, MemoryImportance.HIGH):
            return MemoryLayer.CAPSULE

        # 高情绪词 → 情绪胶囊
        high_emotion_words = [
            "愤怒", "生气", "悲伤", "恐惧", "害怕",
            "喜悦", "兴奋", "开心", "快乐",
            "失望", "感动", "惊讶", "震惊",
            "自豪", "羞耻", "内疚"
        ]
        if any(word in user_emotion for word in high_emotion_words):
            return MemoryLayer.CAPSULE

        # 决策点 → 情绪胶囊（哪怕情绪不强烈）
        if decisions and len(decisions) > 0:
            return MemoryLayer.CAPSULE

        # 默认 → 每日摘要
        return MemoryLayer.DAILY_SUMMARY

    # ─── 查询接口 ─────────────────────────────────────────────

    def search(
        self,
        query: str,
        layers: list = None,
        limit: int = 20,
        importance_threshold: MemoryImportance = None
    ) -> list[MemoryEvent]:
        """
        搜索记忆
        后续接入向量检索优化，目前用关键词匹配
        """
        layers = layers or [MemoryLayer.CAPSULE, MemoryLayer.DAILY_SUMMARY]
        results = []

        for layer in layers:
            if layer == MemoryLayer.CAPSULE:
                results.extend(self._search_layer(self.capsule_path, query, importance_threshold))
            elif layer == MemoryLayer.DAILY_SUMMARY:
                results.extend(self._search_layer(self.daily_path, query, importance_threshold))
            elif layer == MemoryLayer.FULL_LOG and self.deployment == "local":
                results.extend(self._search_layer(self.fulllog_path, query, importance_threshold))

        # 按重要性排序
        results.sort(
            key=lambda x: (
                x.importance.value if isinstance(x.importance, MemoryImportance) else x.importance,
                x.timestamp
            ),
            reverse=True
        )
        return results[:limit]

    def _search_layer(
        self,
        layer_path: str,
        query: str,
        importance_threshold: MemoryImportance = None
    ) -> list[MemoryEvent]:
        results = []
        query_lower = query.lower()

        if not os.path.exists(layer_path):
            return results

        for fname in os.listdir(layer_path):
            if not fname.endswith(".jsonl"):
                continue
            path = os.path.join(layer_path, fname)
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        event = MemoryEvent.from_dict(data)
                    except Exception:
                        continue

                    # 关键词匹配
                    content_lower = event.content.lower()
                    tags_lower = " ".join(event.tags).lower()
                    
                    if query_lower in content_lower or query_lower in tags_lower:
                        if importance_threshold is None or event.importance.value >= importance_threshold.value:
                            results.append(event)

        return results

    def get_daily_summary(self, date: str) -> list[MemoryEvent]:
        """获取某日的所有记忆事件"""
        events = []
        for layer_path in [self.capsule_path, self.daily_path]:
            path = os.path.join(layer_path, f"{date}.jsonl")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                events.append(MemoryEvent.from_dict(data))
                            except Exception:
                                continue
        return sorted(events, key=lambda x: x.timestamp)

    def get_full_logs(self, date: str) -> list[MemoryEvent]:
        """获取完整日志（仅本地部署）"""
        if self.deployment != "local":
            return []
        return self._load_layer(self.fulllog_path, date)

    def generate_daily_summary(self, date: str) -> dict:
        """
        生成结构化每日摘要
        供自我叙事模块调用
        """
        events = self.get_daily_summary(date)
        if not events:
            return {"date": date, "summary": "今日无重要记录", "events": []}

        capsule_events = [e for e in events if e.layer == MemoryLayer.CAPSULE]
        daily_events = [e for e in events if e.layer == MemoryLayer.DAILY_SUMMARY]

        return {
            "date": date,
            "total_events": len(events),
            "capsule_count": len(capsule_events),
            "summary": f"今日共记录{len(events)}个事件，其中{len(capsule_events)}个重要",
            "important_events": [self._summarize_event(e) for e in capsule_events],
            "all_events": [self._summarize_event(e) for e in events],
            "emotions": list(set([e.user_emotion for e in events if e.user_emotion])),
            "decisions": list(set([d for e in events for d in e.decisions])),
            "tags": list(set([tag for e in events for tag in e.tags])),
            "outcomes": [e.outcome for e in events if e.outcome]
        }

    def _summarize_event(self, event: MemoryEvent) -> str:
        parts = [event.content[:50]]
        if event.user_emotion:
            parts.append(f"情绪:{event.user_emotion}")
        if event.decisions:
            parts.append(f"决定:{event.decisions[0][:20]}")
        return " | ".join(parts)

    # ─── 文件 I/O ─────────────────────────────────────────────

    def _append(self, layer_path: str, event: MemoryEvent):
        date = event.timestamp[:10]
        path = os.path.join(layer_path, f"{date}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

    def _load_layer(self, layer_path: str, date: str) -> list[MemoryEvent]:
        path = os.path.join(layer_path, f"{date}.jsonl")
        if not os.path.exists(path):
            return []
        events = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        events.append(MemoryEvent.from_dict(data))
                    except Exception:
                        continue
        return events

    # ─── 统计 ─────────────────────────────────────────────────

    def get_stats(self) -> dict:
        """获取记忆系统统计"""
        stats = {}
        for name, path in [
            ("capsules", self.capsule_path),
            ("daily", self.daily_path),
            ("fulllog", self.fulllog_path)
        ]:
            if not os.path.exists(path):
                stats[name] = {"files": 0, "events": 0}
                continue
            files = len([f for f in os.listdir(path) if f.endswith(".jsonl")])
            events = sum(1 for f in os.listdir(path) if f.endswith(".jsonl")
                         for line in open(os.path.join(path, f), encoding="utf-8") if line.strip())
            stats[name] = {"files": files, "events": events}
        return stats
