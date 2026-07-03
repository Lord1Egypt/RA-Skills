"""Data models for intent classification."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MatchRule:
    """A keyword or pattern rule for matching intents."""
    type: str  # "keyword" | "pattern"
    value: str
    weight: float = 1.0  # 匹配权重


@dataclass
class Intent:
    """Intent definition."""
    id: str
    name: str
    description: str
    category: str       # 一级分类: CODE, KNOW, TASK, CHAT
    sub_category: str   # 二级分类
    icon: str = "?"     # 展示图标
    keywords: list = field(default_factory=list)      # MatchRule 列表
    patterns: list = field(default_factory=list)      # regex 列表
    route_skill: str = ""           # 路由到的技能名
    route_description: str = ""     # 路由说明
    priority: int = 0               # 优先级(越大越优先)
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id, "name": self.name,
            "description": self.description,
            "category": self.category, "sub_category": self.sub_category,
            "icon": self.icon,
            "keywords": [{"type": k.type, "value": k.value, "weight": k.weight}
                         if isinstance(k, MatchRule) else k
                         for k in self.keywords],
            "patterns": self.patterns,
            "route_skill": self.route_skill,
            "route_description": self.route_description,
            "priority": self.priority, "enabled": self.enabled,
            "created_at": self.created_at, "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Intent":
        keywords = []
        for k in d.get("keywords", []):
            if isinstance(k, dict):
                keywords.append(MatchRule(**k))
            elif isinstance(k, str):
                keywords.append(MatchRule(type="keyword", value=k, weight=1.0))
        return cls(
            id=d["id"], name=d["name"], description=d.get("description", ""),
            category=d["category"], sub_category=d["sub_category"],
            icon=d.get("icon", "?"), keywords=keywords,
            patterns=d.get("patterns", []),
            route_skill=d.get("route_skill", ""),
            route_description=d.get("route_description", ""),
            priority=d.get("priority", 0), enabled=d.get("enabled", True),
            created_at=d.get("created_at", ""), updated_at=d.get("updated_at", ""),
        )


@dataclass
class ClassificationResult:
    """Classification output."""
    intent_id: str
    intent_name: str
    category: str
    sub_category: str
    icon: str
    confidence: float           # 0-1
    matched_keywords: list      # 命中的关键词
    matched_patterns: list      # 命中的正则
    route_skill: str
    route_description: str
    alternatives: list = field(default_factory=list)  # 备选分类

    def to_dict(self) -> dict:
        return {
            "intent_id": self.intent_id, "intent_name": self.intent_name,
            "category": self.category, "sub_category": self.sub_category,
            "icon": self.icon, "confidence": round(self.confidence, 4),
            "matched_keywords": self.matched_keywords,
            "matched_patterns": self.matched_patterns,
            "route_skill": self.route_skill,
            "route_description": self.route_description,
            "alternatives": [a.to_dict() for a in self.alternatives],
        }
