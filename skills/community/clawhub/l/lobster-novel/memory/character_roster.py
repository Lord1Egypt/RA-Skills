#!/usr/bin/env python3
"""
lobster-novel: 角色名册 & 配角利用率管理

核心能力：
  1) 角色分类：主角/重要配角/次要配角/龙套
  2) 每章出场统计 + 角色密度
  3) 利用率检测：角色连续N章不出场 → 标记为"沦为背景板"
  4) 新角色导入率监控
  5) 写作注入：生成角色状态摘要
"""
import json, re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime


# 角色重要级别
IMPORTANCE_LEVELS = {
    "protagonist": 4,      # 主角
    "major": 3,            # 重要配角
    "minor": 2,            # 次要配角
    "extra": 1,            # 龙套
}


@dataclass
class CharacterEntry:
    """角色档案条目"""
    name: str
    importance: str = "minor"           # protagonist / major / minor / extra
    first_appearance: int = 0           # 首次出场章节
    last_appearance: int = 0            # 最近出场章节
    total_appearances: int = 0          # 总出场次数
    description: str = ""               # 角色标签/特征
    tags: List[str] = field(default_factory=list)      # 标签（如：反派/盟友/CP/工具人）
    status: str = "active"             # active / disappeared / dead / cameo
    disappears_for: int = 0            # 当前已消失章数（当status=disappeared时有效）

    def been_absent_for(self, current_chapter: int) -> int:
        """累计缺席章数"""
        if self.status == "disappeared" or self.status == "active":
            return current_chapter - self.last_appearance
        return 0


@dataclass
class ChapterAppearance:
    """单章出场记录"""
    chapter: int
    characters: List[str]                     # 登场角色名列表
    new_characters: List[str] = field(default_factory=list)  # 本章新登场角色
    total_crowd: int = 0                      # 本章登场总人数
    density_note: str = ""                    # 密度评估


class CharacterRoster:
    """角色名册管理器"""

    ROSTER_FILE = "character_roster.json"
    APPEARANCE_FILE = "chapter_appearances.json"

    # 默认阈值
    DISAPPEAR_THRESHOLD = 5       # 连续5章不出场→标记为"消失"
    MAX_NEW_PER_CHAPTER = 3       # 每章最多引入3个新角色
    MAX_TOTAL_PER_CHAPTER = 12    # 每章最多12个角色出场
    MIN_TOTAL_ROSTER = 15         # 50万字以上小说至少15个有名有姓角色
    CRITICAL_ROSTER = 8           # 低于8个角色是严重问题

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.roster: Dict[str, CharacterEntry] = self._load_roster()
        self.appearances: List[ChapterAppearance] = self._load_appearances()

    def _load_roster(self) -> Dict[str, CharacterEntry]:
        f = self.dir / self.ROSTER_FILE
        if not f.exists():
            return {}
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return {k: CharacterEntry(**v) for k, v in data.items()}
        except Exception:
            return {}

    def _load_appearances(self) -> List[ChapterAppearance]:
        f = self.dir / self.APPEARANCE_FILE
        if not f.exists():
            return []
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return [ChapterAppearance(**a) for a in data]
        except Exception:
            return []

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / self.ROSTER_FILE).write_text(
            json.dumps({k: asdict(v) for k, v in self.roster.items()},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        (self.dir / self.APPEARANCE_FILE).write_text(
            json.dumps([asdict(a) for a in self.appearances],
                       ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 角色注册 ─────────────────────────────────────────────

    def register(self, name: str, importance: str = "minor",
                 description: str = "", tags: List[str] = None,
                 first_chapter: int = 0) -> CharacterEntry:
        """注册新角色"""
        entry = CharacterEntry(
            name=name,
            importance=importance,
            first_appearance=first_chapter,
            last_appearance=first_chapter,
            total_appearances=1 if first_chapter > 0 else 0,
            description=description,
            tags=tags or [],
        )
        self.roster[name] = entry
        self.save()
        return entry

    def update_importance(self, name: str, new_level: str) -> bool:
        """升级/降级角色重要度"""
        entry = self.roster.get(name)
        if not entry:
            return False
        entry.importance = new_level
        self.save()
        return True

    def update_tags(self, name: str, tags: List[str]):
        """更新角色标签"""
        entry = self.roster.get(name)
        if entry:
            entry.tags = tags
            self.save()

    # ── 出场记录 ─────────────────────────────────────────────

    def record_appearance(self, chapter: int, char_names: List[str]):
        """记录一章的出场角色"""
        names = list(set(char_names))  # 去重
        existing = [n for n in names if n in self.roster]
        new_names = [n for n in names if n not in self.roster]

        # 新角色自动注册为龙套
        for n in new_names:
            self.register(n, importance="extra",
                          first_chapter=chapter)

        for n in existing + new_names:
            entry = self.roster[n]
            entry.last_appearance = chapter
            entry.total_appearances += 1

        self.appearances.append(ChapterAppearance(
            chapter=chapter,
            characters=names,
            new_characters=new_names,
            total_crowd=len(names),
        ))
        self.save()

    def auto_classify(self, current_chapter: int, total_chapters_estimate: int = 0):
        """根据出场数据自动调整角色重要级别"""
        threshold_major = max(5, total_chapters_estimate * 0.3) if total_chapters_estimate else 10
        threshold_minor = max(2, total_chapters_estimate * 0.1) if total_chapters_estimate else 3

        for name, entry in self.roster.items():
            if entry.importance == "protagonist":
                continue  # 主角手动设定
            if entry.total_appearances >= threshold_major:
                self.roster[name].importance = "major"
            elif entry.total_appearances >= threshold_minor:
                self.roster[name].importance = "minor"

    def auto_detect_absences(self, current_chapter: int, threshold: int = None):
        """自动检测消失角色"""
        t = threshold or self.DISAPPEAR_THRESHOLD
        for name, entry in self.roster.items():
            if entry.status in ("dead", "cameo"):
                continue
            if entry.importance == "protagonist":
                continue
            absent = current_chapter - entry.last_appearance
            if absent >= t:
                entry.status = "disappeared"
                entry.disappears_for = absent
        self.save()

    # ── 查询 ─────────────────────────────────────────────────

    def get_counts(self) -> Dict[str, int]:
        """各类角色数量统计"""
        counts = {"protagonist": 0, "major": 0, "minor": 0, "extra": 0, "total": 0}
        for entry in self.roster.values():
            level = entry.importance
            if level in counts:
                counts[level] += 1
            counts["total"] += 1
        return counts

    def get_disappeared(self, min_absent: int = 3) -> List[Tuple[str, int, str]]:
        """获取消失角色列表: (name, absent_chapters, importance)"""
        return [
            (name, entry.disappears_for, entry.importance)
            for name, entry in self.roster.items()
            if entry.status == "disappeared" and entry.disappears_for >= min_absent
        ]

    def get_new_in_chapter(self, chapter: int) -> List[str]:
        """获取某章的新登场角色"""
        for a in self.appearances:
            if a.chapter == chapter:
                return a.new_characters
        return []

    def get_chapter_density(self, chapter: int) -> Optional[int]:
        """获取某章角色密度"""
        for a in self.appearances:
            if a.chapter == chapter:
                return a.total_crowd
        return None

    def get_underused_minors(self, current_chapter: int, min_appearances: int = 3) -> List[str]:
        """获取利用率不足的配角（出场次数＜预期）"""
        underused = []
        for name, entry in self.roster.items():
            if entry.importance == "protagonist":
                continue
            if entry.importance == "major" and entry.total_appearances < min_appearances:
                underused.append(name)
        return underused

    def get_suggested_returns(self, current_chapter: int) -> List[Tuple[str, int, str]]:
        """建议回归的角色（按消失时长排序）"""
        disappeared = self.get_disappeared(min_absent=3)
        disappeared.sort(key=lambda x: -x[1])
        return disappeared[:5]

    # ── 质量检查 ─────────────────────────────────────────────

    def quality_issues(self, current_chapter: int) -> List[dict]:
        """返回角色管理的质量问题列表"""
        issues = []
        counts = self.get_counts()

        # 总角色数不足
        if counts["total"] < self.CRITICAL_ROSTER:
            issues.append({
                "severity": "P0",
                "role": "角色检查",
                "category": "角色极度匮乏",
                "desc": f"全书仅{counts['total']}个有名有姓角色，至少需要{self.CRITICAL_ROSTER}+",
                "suggest": "增加配角，每个新卷引入3-5个新人"
            })
        elif counts["total"] < self.MIN_TOTAL_ROSTER:
            issues.append({
                "severity": "P1",
                "role": "角色检查",
                "category": "角色偏少",
                "desc": f"全书仅{counts['total']}个角色，建议{self.MIN_TOTAL_ROSTER}+",
                "suggest": "考虑在下一章引入新配角"
            })

        # 龙套过多（全是龙套没重要配角）
        if counts["extra"] > 0 and counts["major"] < 2:
            issues.append({
                "severity": "P1",
                "role": "角色检查",
                "category": "重要配角缺失",
                "desc": f"龙套{counts['extra']}人但重要配角仅{counts['major']}人",
                "suggest": "给几个龙套加戏升级为配角"
            })

        # 消失角色
        disappeared = self.get_disappeared()
        if disappeared:
            for name, absent, imp in disappeared[:5]:
                label = "重要配角" if imp == "major" else "配角"
                issues.append({
                    "severity": "P0" if imp == "major" else "P1",
                    "role": "角色检查",
                    "category": "角色利用率不足",
                    "desc": f"{label}{name}已连续{absent}章未登场",
                    "suggest": f"在第{current_chapter + 1}章安排{name}回归或交代去向"
                })

        # 新角色密度
        if self.appearances:
            last_app = self.appearances[-1]
            if len(last_app.new_characters) > self.MAX_NEW_PER_CHAPTER:
                issues.append({
                    "severity": "P1",
                    "role": "角色检查",
                    "category": "新角色过载",
                    "desc": f"第{last_app.chapter}章引入{len(last_app.new_characters)}个新角色，建议≤{self.MAX_NEW_PER_CHAPTER}",
                    "suggest": "新角色分批登场，先用现有角色推进剧情"
                })
            if last_app.total_crowd > self.MAX_TOTAL_PER_CHAPTER:
                issues.append({
                    "severity": "P1",
                    "role": "角色检查",
                    "category": "本章角色过密",
                    "desc": f"第{last_app.chapter}章{last_app.total_crowd}人出场，可能读起来乱",
                    "suggest": "场景分组，分批描写，避免同台拥挤"
                })

        # 各章角色密度趋势
        if len(self.appearances) >= 5:
            recent = self.appearances[-5:]
            avg_density = sum(a.total_crowd for a in recent) / len(recent)
            if avg_density < 2:
                issues.append({
                    "severity": "P1",
                    "role": "角色检查",
                    "category": "章节互动不足",
                    "desc": f"近5章平均每章仅{avg_density:.1f}人出场",
                    "suggest": "增加日常互动场景，让人物之间产生化学反应"
                })

        return issues

    # ── 写作注入 ─────────────────────────────────────────────

    def writing_prompt_block(self, current_chapter: int) -> str:
        """生成本章可用角色的提示块，供写章节时注入"""
        counts = self.get_counts()
        lines = [f"【角色状态】总计{counts['total']}个角色"]
        lines.append(f"  主角: {counts['protagonist']} / 重要配角: {counts['major']} / 配角: {counts['minor']} / 龙套: {counts['extra']}")

        disappeared = self.get_disappeared(min_absent=5)
        if disappeared:
            lines.append(f"  消失角色({len(disappeared)}): " +
                         ", ".join(f"{n}({a}章)" for n, a, _ in disappeared[:3]))

        returns = self.get_suggested_returns(current_chapter)
        if returns:
            lines.append(f"  建议安排回归: {', '.join(n for n, _, _ in returns)}")

        # 活跃角色
        if self.appearances:
            last_app = self.appearances[-1]
            recent_chars = list({n for a in self.appearances[-3:] for n in a.characters})
            major_active = [n for n in recent_chars
                          if self.roster.get(n) and self.roster[n].importance in ("protagonist", "major")]
            if major_active:
                lines.append(f"  近期活跃重要角色: {', '.join(major_active[:6])}")

        return "\n".join(lines)

    def summary(self) -> str:
        """完整可读摘要"""
        counts = self.get_counts()
        lines = [f"📋 角色名册: 共{counts['total']}人"]
        lines.append(f"  {'主角':>6}: {counts['protagonist']}")
        lines.append(f"  {'重要配角':>6}: {counts['major']}")
        lines.append(f"  {'配角':>6}: {counts['minor']}")
        lines.append(f"  {'龙套':>6}: {counts['extra']}")
        if self.appearances:
            total_ch = len(self.appearances)
            avg_density = sum(a.total_crowd for a in self.appearances) / total_ch
            lines.append(f"  写作{total_ch}章，平均每章{avg_density:.1f}个角色")
            if self.roster:
                active = sum(1 for e in self.roster.values() if e.status == "active")
                disappeared = sum(1 for e in self.roster.values() if e.status == "disappeared")
                lines.append(f"  活跃{active} / 消失{disappeared} / 已故{sum(1 for e in self.roster.values() if e.status == 'dead')}")
        return "\n".join(lines)

    def dump_all_characters(self) -> str:
        """全部角色列表"""
        lines = [f"{'角色名':<8} {'级别':<6} {'出场章数':<8} {'最近出场':<8} {'状态':<10} {'标签'}"]
        lines.append("-" * 60)
        for name, entry in sorted(self.roster.items(),
                                  key=lambda x: self._key(IMPORTANCE_LEVELS.get(x[1].importance, 0))):
            imp_cn = {"protagonist": "主角", "major": "重要配角", "minor": "配角", "extra": "龙套"}
            status_cn = {"active": "活跃", "disappeared": "消失", "dead": "已故", "cameo": "客串"}
            lines.append(
                f"{name:<8} {imp_cn.get(entry.importance, '?'):<6} "
                f"{entry.total_appearances:<8} "
                f"{'第' + str(entry.last_appearance) + '章' if entry.last_appearance else '未出场':<8} "
                f"{status_cn.get(entry.status, '?'):<10} "
                f"{'、'.join(entry.tags[:3])}"
            )
        return "\n".join(lines)

    @staticmethod
    def _key(level: int) -> int:
        return -level  # 排序用：主角排最前
