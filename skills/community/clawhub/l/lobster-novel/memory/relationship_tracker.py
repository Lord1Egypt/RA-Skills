#!/usr/bin/env python3
"""
lobster-novel: 关系网追踪

追踪角色间关系的动态变化：
  盟友→敌对  / 信任→背叛  / 陌生→亲密 等
每章记录关系状态变化，支持历史回溯。
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple


@dataclass
class Relationship:
    """两角色间的关系状态"""
    char_a: str
    char_b: str
    relation_type: str = "unknown"     # 盟友/敌对/师生/情侣/父子/主仆/陌生/暧昧
    trust_level: int = 50              # 0-100 信任度
    intimacy_level: int = 0            # 0-100 亲密程度
    power_balance: str = "平等"         # 平等/压制/被压制/敬仰/依赖
    status: str = "active"             # active / broken / dormant
    description: str = ""


@dataclass
class RelationshipChange:
    """一次关系变化事件"""
    chapter: int
    char_a: str
    char_b: str
    field: str              # 变化的字段
    old_value: str
    new_value: str
    reason: str = ""        # 变化原因（情节推动）
    note: str = ""


class RelationshipTracker:
    """关系追踪器"""

    FILE = "relationships.json"
    CHANGES_FILE = "relationship_changes.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.rels: Dict[str, Relationship] = self._load()
        self.changes: List[RelationshipChange] = self._load_changes()

    def _load(self) -> Dict[str, Relationship]:
        f = self.dir / self.FILE
        if not f.exists():
            return {}
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return {k: Relationship(**v) for k, v in data.items()}
        except Exception:
            return {}

    def save(self):
        f = self.dir / self.FILE
        f.write_text(json.dumps({k: asdict(v) for k, v in self.rels.items()},
                                 ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_changes(self) -> List[RelationshipChange]:
        f = self.dir / self.CHANGES_FILE
        if not f.exists():
            return []
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return [RelationshipChange(**c) for c in data]
        except Exception:
            return []

    def _save_changes(self):
        f = self.dir / self.CHANGES_FILE
        f.write_text(json.dumps([asdict(c) for c in self.changes],
                                 ensure_ascii=False, indent=2), encoding="utf-8")

    def _key(self, a: str, b: str) -> str:
        return "::".join(sorted([a, b]))

    def get(self, a: str, b: str) -> Optional[Relationship]:
        k = self._key(a, b)
        return self.rels.get(k)

    def set_relationship(self, a: str, b: str, rel: Relationship):
        """设置/更新关系"""
        k = self._key(a, b)
        rel.char_a = a
        rel.char_b = b
        self.rels[k] = rel
        self.save()

    def update_trust(self, a: str, b: str, new_trust: int, chapter: int,
                     reason: str = "") -> Optional[Relationship]:
        """变更信任度"""
        k = self._key(a, b)
        rel = self.rels.get(k)
        if not rel:
            return None
        old = rel.trust_level
        rel.trust_level = max(0, min(100, new_trust))
        self.save()
        self.changes.append(RelationshipChange(
            chapter=chapter, char_a=a, char_b=b,
            field="trust_level", old_value=str(old),
            new_value=str(rel.trust_level), reason=reason))
        self._save_changes()
        return rel

    def update_intimacy(self, a: str, b: str, new_intimacy: int, chapter: int,
                        reason: str = "") -> Optional[Relationship]:
        """变更亲密程度"""
        k = self._key(a, b)
        rel = self.rels.get(k)
        if not rel:
            return None
        old = rel.intimacy_level
        rel.intimacy_level = max(0, min(100, new_intimacy))
        self.save()
        self.changes.append(RelationshipChange(
            chapter=chapter, char_a=a, char_b=b,
            field="intimacy_level", old_value=str(old),
            new_value=str(rel.intimacy_level), reason=reason))
        self._save_changes()
        return rel

    def get_relationships_for(self, name: str) -> List[Relationship]:
        """获取某人的所有关系"""
        results = []
        for k, rel in self.rels.items():
            if name in k.split("::"):
                results.append(rel)
        return results

    def get_changes_for(self, name: str) -> List[RelationshipChange]:
        """获取某人的关系变化历史"""
        return [
            c for c in self.changes
            if c.char_a == name or c.char_b == name
        ]

    def summary(self, name: str) -> str:
        """某人关系网摘要"""
        rels = self.get_relationships_for(name)
        if not rels:
            return f"{name}暂无关系记录"
        lines = [f"{name}的关系网 ({len(rels)}条关系):"]
        for r in rels:
            other = r.char_b if r.char_a == name else r.char_a
            trust_bar = "█" * (r.trust_level // 10) + "░" * (10 - r.trust_level // 10)
            lines.append(f"  {other}: {r.relation_type} | 信任{trust_bar} {r.trust_level}% | 亲密{r.intimacy_level}%")
        return "\n".join(lines)

    def dump(self) -> str:
        """全部关系网"""
        lines = [f"关系网共{len(self.rels)}对关系\n"]
        for k, r in sorted(self.rels.items()):
            lines.append(f"  {r.char_a} ↔ {r.char_b}: {r.relation_type} [{r.status}]")
            lines.append(f"    信任: {r.trust_level}% 亲密: {r.intimacy_level}% 权力: {r.power_balance}")
        return "\n".join(lines)
