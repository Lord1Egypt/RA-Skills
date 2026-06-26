#!/usr/bin/env python3
"""
lobster-novel: Conflict detector (inspired by novel-writing).
Checks new chapter against bible/continuity for:
- Character state contradictions (dead/alive, location, relationships)
- World rule violations
- Timeline inconsistencies
- Previously established fact reversals
"""
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from bible import BibleManager
from continuity import ContinuityTracker


@dataclass
class FullAuditResult:
    """Full-novel audit result."""
    total_chapters: int = 0
    total_conflicts: int = 0
    p0_count: int = 0
    p1_count: int = 0
    p2_count: int = 0
    conflicts_by_category: Dict[str, int] = field(default_factory=dict)
    conflict_details: List[dict] = field(default_factory=list)

    def to_text(self) -> str:
        lines = [
            f"# Full Novel Consistency Audit",
            f"",
            f"Chapters checked: {self.total_chapters}",
            f"Total conflicts:  {self.total_conflicts}",
            f"  P0 (certain):   {self.p0_count}",
            f"  P1 (likely):    {self.p1_count}",
            f"  P2 (possible):  {self.p2_count}",
            f"",
        ]
        if self.conflicts_by_category:
            lines.append("## By Category")
            for cat, count in sorted(self.conflicts_by_category.items()):
                lines.append(f"  {cat}: {count}")
            lines.append("")
        if self.conflict_details:
            lines.append("## Details")
            for i, cd in enumerate(self.conflict_details[:20], 1):
                lines.append(f"  {i}. ch{cd['chapter']} [{cd['severity']}] [{cd['category']}]")
                lines.append(f"     {cd['description'][:70]}")
            if len(self.conflict_details) > 20:
                lines.append(f"     ... and {len(self.conflict_details) - 20} more")
        return "\n".join(lines)

from bible import BibleManager
from continuity import ContinuityTracker


@dataclass
class Conflict:
    severity: str       # P0 (certain) / P1 (likely) / P2 (possible)
    category: str       # character / world / timeline / fact
    description: str
    chapter: int = 0
    suggestion: str = ""

    def to_line(self) -> str:
        return f"  [{self.severity}] [{self.category}] {self.description}"


@dataclass
class FullAuditResult:
    """Full-novel audit result."""
    total_chapters: int = 0
    total_conflicts: int = 0
    p0_count: int = 0
    p1_count: int = 0
    p2_count: int = 0
    conflicts_by_category: Dict[str, int] = field(default_factory=dict)
    conflict_details: List[dict] = field(default_factory=list)

    def to_text(self) -> str:
        lines = [
            f"# Full Novel Consistency Audit",
            f"",
            f"Chapters checked: {self.total_chapters}",
            f"Total conflicts:  {self.total_conflicts}",
            f"  P0 (certain):   {self.p0_count}",
            f"  P1 (likely):    {self.p1_count}",
            f"  P2 (possible):  {self.p2_count}",
            f"",
        ]
        if self.conflicts_by_category:
            lines.append("## By Category")
            for cat, count in sorted(self.conflicts_by_category.items()):
                lines.append(f"  {cat}: {count}")
            lines.append("")
        if self.conflict_details:
            lines.append("## Details")
            for i, cd in enumerate(self.conflict_details[:20], 1):
                lines.append(f"  {i}. ch{cd['chapter']} [{cd['severity']}] [{cd['category']}]")
                lines.append(f"     {cd['description'][:70]}")
            if len(self.conflict_details) > 20:
                lines.append(f"     ... and {len(self.conflict_details) - 20} more")
        return "\n".join(lines)


class ConflictDetector:
    """Static conflict detection against established bible/continuity."""

    def __init__(self, project_dir: Path):
        self.bible = BibleManager(project_dir)
        self.continuity = ContinuityTracker(project_dir)

    def check_chapter(self, chapter_num: int, text: str) -> List[Conflict]:
        """Run all conflict checks on a new chapter."""
        conflicts = []
        conflicts.extend(self._check_character_state(text))
        conflicts.extend(self._check_world_rules(text))
        conflicts.extend(self._check_hooks_overdue(chapter_num))
        conflicts.extend(self._check_timeline(text))
        return conflicts

    def _check_character_state(self, text: str) -> List[Conflict]:
        """Check if characters are in impossible states."""
        conflicts = []
        for name, char in self.bible.bible.characters.items():
            if not char.current_state:
                continue
            state = char.current_state.lower()

            # Dead characters shouldn't appear
            if "死" in state or "亡" in state or "dead" in state:
                if name in text:
                    conflicts.append(Conflict(
                        severity="P1",
                        category="character",
                        description=f"'{name}' is {state} but appears in chapter",
                        suggestion=f"Use flashback or ghost/POV if intentional",
                    ))

            # Unconscious characters shouldn't act
            if "昏迷" in state or "晕" in state or "沉睡" in state:
                if name in text and any(v in text for v in ["说", "走", "跑", "打", "跳", "睁"]):
                    conflicts.append(Conflict(
                        severity="P0",
                        category="character",
                        description=f"'{name}' is {state} but shows active behavior",
                    ))

        # One mention = dead, two different locations = conflict
        loc_mentions = set()
        for loc_word in ["地方", "位置", "在", "来到", "到达"]:
            mentions = re.findall(rf'{loc_word}([\u4e00-\u9fff]{{2,8}})', text)
            loc_mentions.update(mentions)
        if len(loc_mentions) > 4:
            conflicts.append(Conflict(
                severity="P1",
                category="character",
                description=f"Character jumps between {len(loc_mentions)} locations in one chapter: {', '.join(list(loc_mentions)[:4])}",
                suggestion="Review if scene transitions are clear",
            ))

        return conflicts

    def _check_world_rules(self, text: str) -> List[Conflict]:
        """Check if world rules defined in bible are broken."""
        conflicts = []
        bible = self.bible.bible

        if not bible.world_rules:
            return conflicts

        for rule in bible.world_rules:
            # Simple keyword-based: if rule mentions a forbidden action
            forbidden = re.findall(r'(不能|禁止|不可|严禁|无法)([\u4e00-\u9fff]{2,10})', rule)
            for neg, action in forbidden:
                # If the forbidden action appears in text without negation
                if action in text and not re.search(rf'(不能|禁止|不可|严禁|无法){action}', text):
                    conflicts.append(Conflict(
                        severity="P1",
                        category="world",
                        description=f"World rule '{rule[:40]}' may be violated: '{action}' used",
                        suggestion="Either obey the rule or show why it's broken this time",
                    ))

            # Check positive rules: if rule says "only X can Y", check Y without X
            only_matches = re.findall(r'(只有|唯一|仅仅)([\u4e00-\u9fff]{2,10})', rule)
            for only_token, subject in only_matches:
                action_match = re.search(r'(才能|可以|能够)([\u4e00-\u9fff]{2,10})', rule)
                if action_match:
                    action = action_match.group(2)
                    if action in text and subject not in text:
                        conflicts.append(Conflict(
                            severity="P1",
                            category="world",
                            description=f"Only '{subject}' should '{action}' per rule '{rule[:40]}'",
                        ))

        return conflicts

    def _check_hooks_overdue(self, chapter_num: int) -> List[Conflict]:
        """Flag hooks that are overdue for payoff."""
        conflicts = []
        from foreshadowing import ForeshadowTracker
        tracker = ForeshadowTracker(self.bible.dir)
        overdue = tracker.get_overdue(chapter_num, threshold=3)
        for h in overdue:
            conflicts.append(Conflict(
                severity="P2" if h.importance == "minor" else "P1",
                category="timeline",
                description=f"Hook overdue: '{h.description[:50]}' (planted ch{h.planted_chapter}, {h.overdue_by(chapter_num)} ch ago)",
                suggestion=f"Pay off this hook within next 2 chapters",
            ))
        return conflicts

    def _check_timeline(self, text: str) -> List[Conflict]:
        """Basic timeline consistency checks."""
        conflicts = []

        # Contradictory time markers in same chapter
        time_markers = re.findall(r'(清晨|早晨|上午|中午|下午|傍晚|黄昏|晚上|深夜|午夜|凌晨)', text)
        if len(set(time_markers)) >= 3:
            conflicts.append(Conflict(
                severity="P2",
                category="timeline",
                description=f"Multiple time markers in one chapter: {', '.join(set(time_markers))}",
                suggestion="Ensure chapter covers a single continuous time period",
            ))

        return conflicts

    def check_all(self, chapter_num: int, text: str) -> List[Conflict]:
        """Full check: run all checks and return sorted by severity."""
        conflicts = self.check_chapter(chapter_num, text)
        severity_order = {"P0": 0, "P1": 1, "P2": 2}
        conflicts.sort(key=lambda c: (severity_order.get(c.severity, 9), c.category))
        return conflicts

    def audit_all(self) -> FullAuditResult:
        """Full-novel audit: run conflict check on ALL written chapters.
        Inspired by 马良写作's 设定审计 (every 100k chars).
        """
        ch_dir = self.dir / "chapters"
        if not ch_dir.exists():
            return FullAuditResult()

        result = FullAuditResult()
        all_conflicts = []

        for f in sorted(ch_dir.glob("ch*.md")):
            ch_num = int(re.search(r'ch(\d+)', f.name).group(1)) if re.search(r'ch(\d+)', f.name) else 0
            text = f.read_text(encoding="utf-8")
            conflicts = self.check_all(ch_num, text)
            for c in conflicts:
                all_conflicts.append({
                    "chapter": ch_num,
                    "severity": c.severity,
                    "category": c.category,
                    "description": c.description,
                    "suggestion": c.suggestion,
                })
                result.conflicts_by_category[c.category] = \
                    result.conflicts_by_category.get(c.category, 0) + 1

        result.total_chapters = len(list(ch_dir.glob("ch*.md")))
        result.total_conflicts = len(all_conflicts)
        result.p0_count = sum(1 for c in all_conflicts if c["severity"] == "P0")
        result.p1_count = sum(1 for c in all_conflicts if c["severity"] == "P1")
        result.p2_count = sum(1 for c in all_conflicts if c["severity"] == "P2")
        result.conflict_details = all_conflicts
        return result

    def summary(self, chapter_num: int, text: str) -> str:
        """Human-readable summary of conflicts."""
        conflicts = self.check_all(chapter_num, text)
        if not conflicts:
            return f"# Chapter {chapter_num} Conflict Check ✅ No conflicts detected.\n"
        lines = [f"# Chapter {chapter_num} Conflict Check\n"]
        p0 = [c for c in conflicts if c.severity == "P0"]
        p1 = [c for c in conflicts if c.severity == "P1"]
        p2 = [c for c in conflicts if c.severity == "P2"]
        if p0:
            lines.append(f"## P0 (certain) — {len(p0)}")
            for c in p0:
                lines.append(c.to_line())
                if c.suggestion:
                    lines.append(f"    fix: {c.suggestion}")
        if p1:
            lines.append(f"## P1 (likely) — {len(p1)}")
            for c in p1:
                lines.append(c.to_line())
        if p2:
            lines.append(f"## P2 (possible) — {len(p2)}")
            for c in p2:
                lines.append(c.to_line())
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="chapter conflict checker")
    parser.add_argument("--dir", default="./my-novel")
    parser.add_argument("chapter", type=int)
    parser.add_argument("file", help="chapter md file")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    detector = ConflictDetector(Path(args.dir))
    print(detector.summary(args.chapter, text))
