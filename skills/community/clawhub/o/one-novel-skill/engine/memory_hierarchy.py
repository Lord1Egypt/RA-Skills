#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_hierarchy.py — 四层记忆消歧 + 触发学习系统

SKILL.md 声明功能：
- 四层记忆消歧：宪法记忆(优先级最高) > 结构治理 > 项目运行 > 会话工作(最低)
- 宪法级设定不能被日常写作中的临时决策覆盖
- 触发学习：用户显式纠正、同一修正出现3次、用户说"记住这个"
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

_log = logging.getLogger("memory_hierarchy")


class MemoryLevel:
    """四层记忆级别"""

    CONSTITUTION = 1   # 宪法记忆：全书设定、世界观法则
    GOVERNANCE = 2     # 结构治理：总纲、卷规划
    OPERATIONAL = 3    # 项目运行：任务日志、伏笔、时间线
    WORKING = 4        # 会话工作：本章目标、场景链

    @classmethod
    def name(cls, level: int) -> str:
        return {1: "宪法记忆", 2: "结构治理", 3: "项目运行", 4: "会话工作"}.get(level, "未知")

    @classmethod
    def can_override(cls, higher_level: int, lower_level: int) -> bool:
        """高优先级(数字小)可以覆盖低优先级(数字大)，反之不行"""
        return higher_level < lower_level


class MemoryEntry:
    """单条记忆条目"""

    def __init__(self, key: str, value: Any, level: int = MemoryLevel.OPERATIONAL,
                 source: str = "", chapter: int = 0):
        self.key = key
        self.value = value
        self.level = level
        self.source = source
        self.chapter = chapter
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.update_count = 0
        self._locked = False  # 宪法级锁定

    def lock(self):
        """锁定宪法级记忆，禁止修改"""
        if self.level == MemoryLevel.CONSTITUTION:
            self._locked = True

    @property
    def is_locked(self) -> bool:
        return self._locked and self.level == MemoryLevel.CONSTITUTION


class MemoryHierarchyEngine:
    """四层记忆消歧引擎"""

    # === 宪法级记忆的默认项 ===
    CONSTITUTION_DEFAULTS = {
        "world_rules": {
            "key": "world_rules",
            "value": [],
            "description": "世界观核心法则——不可被日常写作覆盖",
            "examples": ["修炼需要灵石", "穿越后无法返回", "魔法有等价交换代价"],
        },
        "style_anchor": {
            "key": "style_anchor",
            "value": {},
            "description": "文风锚点——全书的语言风格基线",
            "examples": ["对话占比40%", "句长15-40字混合", "禁用词列表"],
        },
        "iron_rules": {
            "key": "iron_rules",
            "value": [],
            "description": "铁律——绝对不可违反的规则",
            "examples": ["P0禁用词", "角色死亡不可复活(除非有铺垫)", "世界观设定不可前后矛盾"],
        },
        "core_theme": {
            "key": "core_theme",
            "value": "",
            "description": "核心主题——全书要传达的中心思想",
        },
    }

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()
        self._memory_dir = self.book_dir / "追踪" / "记忆"
        self._memories: Dict[str, MemoryEntry] = {}
        self._conflict_log: List[Dict] = []

    # ====== 记忆读写（带优先级保护） ======

    def set(self, key: str, value: Any, level: int = MemoryLevel.OPERATIONAL,
            source: str = "", chapter: int = 0) -> bool:
        """写入记忆，自动检查优先级冲突

        Returns:
            True: 写入成功
            False: 被高优先级记忆阻止（冲突）
        """
        existing = self._memories.get(key)

        if existing:
            # 冲突检查：低优先级不能覆盖高优先级
            if existing.level < level and existing.is_locked:
                self._log_conflict(key, existing, value, level)
                _log.warning(
                    f"记忆冲突: [{MemoryLevel.name(existing.level)}] '{key}' "
                    f"被锁定，无法被[{MemoryLevel.name(level)}]覆盖"
                )
                return False

            # 同级覆盖：允许，但记录
            if existing.level == level:
                existing.value = value
                existing.updated_at = datetime.now().isoformat()
                existing.update_count += 1
                existing.source = source
                return True

            # 高优先级覆盖低优先级：允许
            if level < existing.level:
                existing.value = value
                existing.level = level
                existing.updated_at = datetime.now().isoformat()
                existing.update_count += 1
                existing.source = source
                _log.info(
                    f"记忆升级: '{key}' 从 [{MemoryLevel.name(existing.level)}] "
                    f"升级到 [{MemoryLevel.name(level)}]"
                )
                return True

        # 新建记忆
        entry = MemoryEntry(key=key, value=value, level=level, source=source, chapter=chapter)
        if level == MemoryLevel.CONSTITUTION:
            entry.lock()
        self._memories[key] = entry
        return True

    def get(self, key: str, default: Any = None) -> Any:
        """读取记忆"""
        entry = self._memories.get(key)
        return entry.value if entry else default

    def get_with_metadata(self, key: str) -> Optional[Dict]:
        """读取记忆（含元数据）"""
        entry = self._memories.get(key)
        if entry is None:
            return None
        return {
            "key": entry.key,
            "value": entry.value,
            "level": entry.level,
            "level_name": MemoryLevel.name(entry.level),
            "locked": entry.is_locked,
            "source": entry.source,
            "chapter": entry.chapter,
            "updated_at": entry.updated_at,
            "update_count": entry.update_count,
        }

    def exists(self, key: str) -> bool:
        return key in self._memories

    # ====== 批量操作 ======

    def get_by_level(self, level: int) -> Dict[str, Any]:
        """获取指定级别的所有记忆"""
        return {
            k: v.value for k, v in self._memories.items()
            if v.level == level
        }

    def get_all_grouped(self) -> Dict[str, Dict[str, Any]]:
        """获取按级别分组的所有记忆"""
        result = {}
        for level in range(1, 5):
            name = MemoryLevel.name(level)
            result[name] = self.get_by_level(level)
        return result

    def lock_constitution(self):
        """锁定所有宪法级记忆"""
        count = 0
        for entry in self._memories.values():
            if entry.level == MemoryLevel.CONSTITUTION:
                entry.lock()
                count += 1
        _log.info(f"已锁定 {count} 条宪法级记忆")

    # ====== 初始化宪法 ======

    def init_constitution(self, world_rules: List[str] = None,
                          style_anchor: Dict = None,
                          iron_rules: List[str] = None,
                          core_theme: str = "") -> Dict[str, bool]:
        """初始化宪法级记忆"""
        results = {}

        if world_rules:
            results["world_rules"] = self.set(
                "world_rules", world_rules,
                level=MemoryLevel.CONSTITUTION, source="初始化"
            )

        if style_anchor:
            results["style_anchor"] = self.set(
                "style_anchor", style_anchor,
                level=MemoryLevel.CONSTITUTION, source="初始化"
            )

        if iron_rules:
            results["iron_rules"] = self.set(
                "iron_rules", iron_rules,
                level=MemoryLevel.CONSTITUTION, source="初始化"
            )

        if core_theme:
            results["core_theme"] = self.set(
                "core_theme", core_theme,
                level=MemoryLevel.CONSTITUTION, source="初始化"
            )

        self.lock_constitution()
        return results

    # ====== 冲突管理 ======

    def _log_conflict(self, key: str, existing: MemoryEntry, new_value: Any, new_level: int):
        """记录冲突"""
        self._conflict_log.append({
            "key": key,
            "existing_level": MemoryLevel.name(existing.level),
            "existing_value": str(existing.value)[:100],
            "new_level": MemoryLevel.name(new_level),
            "new_value": str(new_value)[:100],
            "time": datetime.now().isoformat(),
            "resolved": False,
        })

    def get_conflicts(self) -> List[Dict]:
        """获取冲突日志"""
        return self._conflict_log[-20:]

    def resolve_conflict(self, key: str, choose: str = "existing") -> bool:
        """手动解决冲突"""
        for conflict in reversed(self._conflict_log):
            if conflict["key"] == key and not conflict["resolved"]:
                conflict["resolved"] = True
                return True
        return False

    # ====== 持久化 ======

    def save(self) -> bool:
        """持久化所有记忆到磁盘"""
        self._memory_dir.mkdir(parents=True, exist_ok=True)
        data = {}
        for key, entry in self._memories.items():
            data[key] = {
                "value": entry.value,
                "level": entry.level,
                "level_name": MemoryLevel.name(entry.level),
                "locked": entry.is_locked,
                "source": entry.source,
                "chapter": entry.chapter,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
                "update_count": entry.update_count,
            }
        path = self._memory_dir / "memory_hierarchy.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        _log.info(f"记忆已保存: {len(data)} 条 → {path}")
        return True

    def load(self) -> int:
        """从磁盘加载记忆"""
        path = self._memory_dir / "memory_hierarchy.json"
        if not path.exists():
            return 0
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            count = 0
            for key, info in data.items():
                entry = MemoryEntry(
                    key=key,
                    value=info.get("value"),
                    level=info.get("level", MemoryLevel.OPERATIONAL),
                    source=info.get("source", ""),
                    chapter=info.get("chapter", 0),
                )
                entry.created_at = info.get("created_at", "")
                entry.updated_at = info.get("updated_at", "")
                entry.update_count = info.get("update_count", 0)
                if info.get("locked"):
                    entry.lock()
                self._memories[key] = entry
                count += 1
            _log.info(f"记忆已加载: {count} 条")
            return count
        except Exception as e:
            _log.error(f"记忆加载失败: {e}")
            return 0

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        grouped = self.get_all_grouped()
        return {
            "verdict": "完成",
            "total_memories": len(self._memories),
            "by_level": {name: len(items) for name, items in grouped.items()},
            "conflicts": len(self._conflict_log),
            "locked_constitution": sum(
                1 for v in self._memories.values()
                if v.level == MemoryLevel.CONSTITUTION and v.is_locked
            ),
        }


class TriggeredLearningEngine:
    """触发学习引擎 — 从用户反馈中自动学习"""

    # === 学习触发器 ===
    TRIGGERS = {
        "explicit_correction": {
            "name": "显式纠正",
            "patterns": ["不要这样写", "改成", "改回", "不对", "错了", "重写", "不喜欢", "别用"],
            "action": "record_correction",
        },
        "three_strikes": {
            "name": "三次重复",
            "description": "同一修正出现3次，自动形成偏好",
            "threshold": 3,
            "action": "promote_to_preference",
        },
        "remember_this": {
            "name": "记住这个",
            "patterns": ["记住这个", "记住", "记下来", "别忘了", "以后都这样"],
            "action": "record_permanent_rule",
        },
    }

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else Path.cwd()
        self._learn_dir = self.book_dir / "追踪" / "学习"
        self._corrections: Dict[str, List[Dict]] = {}  # key: 修正类型, value: 历史记录
        self._preferences: Dict[str, Any] = {}  # 已形成的偏好
        self._permanent_rules: Dict[str, str] = {}  # 永久规则

    # ====== 记录修正 ======

    def record_correction(self, issue_type: str, original: str, corrected: str,
                          chapter: int = 0, source: str = "user") -> Dict:
        """记录一次用户修正"""
        record = {
            "type": issue_type,
            "original": original[:200],
            "corrected": corrected[:200],
            "chapter": chapter,
            "source": source,
            "time": datetime.now().isoformat(),
        }

        if issue_type not in self._corrections:
            self._corrections[issue_type] = []
        self._corrections[issue_type].append(record)

        # 检查是否达到3次触发阈值
        count = len(self._corrections[issue_type])
        triggered = count >= self.TRIGGERS["three_strikes"]["threshold"]

        if triggered and issue_type not in self._preferences:
            self._preferences[issue_type] = {
                "preference": f"避免: {original[:50]} → 倾向: {corrected[:50]}",
                "occurrence_count": count,
                "promoted_at": datetime.now().isoformat(),
            }
            _log.info(f"触发学习: '{issue_type}' 已出现{count}次，自动形成偏好")

        return {
            "recorded": True,
            "type": issue_type,
            "occurrence_count": count,
            "threshold_reached": triggered,
            "action": "preference_created" if triggered else "recorded",
        }

    def record_permanent_rule(self, rule_name: str, rule_content: str) -> Dict:
        """记录永久规则（用户说"记住这个"）"""
        self._permanent_rules[rule_name] = rule_content
        return {
            "rule_name": rule_name,
            "rule_content": rule_content[:200],
            "recorded_at": datetime.now().isoformat(),
        }

    def detect_trigger(self, user_message: str) -> Optional[Dict]:
        """检测用户消息中是否包含学习触发器"""
        for trigger_id, trigger_info in self.TRIGGERS.items():
            if "patterns" in trigger_info:
                for pattern in trigger_info["patterns"]:
                    if pattern in user_message:
                        return {
                            "trigger": trigger_id,
                            "trigger_name": trigger_info["name"],
                            "matched_pattern": pattern,
                            "action": trigger_info["action"],
                        }
        return None

    # ====== 查询 ======

    def get_correction_history(self, issue_type: str = None) -> List[Dict]:
        """获取修正历史"""
        if issue_type:
            return self._corrections.get(issue_type, [])
        return [
            {"type": k, "count": len(v), "latest": v[-1] if v else None}
            for k, v in self._corrections.items()
        ]

    def get_preferences(self) -> Dict[str, Any]:
        """获取所有已形成的偏好"""
        return dict(self._preferences)

    def get_permanent_rules(self) -> Dict[str, str]:
        """获取所有永久规则"""
        return dict(self._permanent_rules)

    def get_learnings_summary(self) -> str:
        """生成学习摘要（用于注入 Prompt）"""
        lines = ["【已学习的偏好】"]
        for key, pref in self._preferences.items():
            lines.append(f"  - {key}: {pref['preference']} (出现{pref['occurrence_count']}次)")

        if self._permanent_rules:
            lines.append("")
            lines.append("【永久规则】")
            for name, rule in self._permanent_rules.items():
                lines.append(f"  - {name}: {rule}")

        return "\n".join(lines) if len(lines) > 1 else ""

    # ====== 持久化 ======

    def save(self) -> bool:
        """持久化学习数据"""
        self._learn_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "corrections": self._corrections,
            "preferences": self._preferences,
            "permanent_rules": self._permanent_rules,
            "saved_at": datetime.now().isoformat(),
        }
        path = self._learn_dir / "triggered_learning.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2,
                                   default=str), encoding="utf-8")
        _log.info(f"学习数据已保存: {path}")
        return True

    def load(self) -> int:
        """加载学习数据"""
        path = self._learn_dir / "triggered_learning.json"
        if not path.exists():
            return 0
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._corrections = data.get("corrections", {})
            self._preferences = data.get("preferences", {})
            self._permanent_rules = data.get("permanent_rules", {})
            total = len(self._corrections)
            _log.info(f"学习数据已加载: {total} 类修正")
            return total
        except Exception as e:
            _log.error(f"学习数据加载失败: {e}")
            return 0

    # === 兼容 Engine 接口 ===

    def analyze(self, text: str = "", chapter: int = 1, **kwargs) -> Dict[str, Any]:
        """统一 analyze 接口（兼容 registry 规范）"""
        return {
            "verdict": "完成",
            "total_correction_types": len(self._corrections),
            "total_preferences": len(self._preferences),
            "total_permanent_rules": len(self._permanent_rules),
            "learnings": self.get_learnings_summary(),
        }
