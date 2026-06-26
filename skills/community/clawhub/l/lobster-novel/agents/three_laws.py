#!/usr/bin/env python3
"""
three_laws.py — 防幻觉三定律 写前校验 + 写后校验

统一三定律定义，提供 PreWriteValidator 和 PostWriteValidator，
确保每个章节的写作不违反已有设定。

Usage:
    from agents.three_laws import THREE_LAWS, PreWriteValidator, PostWriteValidator

    # 写前校验
    validator = PreWriteValidator(project_dir)
    warnings = validator.check_outline(chapter_number, outline_text, story_state)

    # 写后校验
    pv = PostWriteValidator(project_dir)
    violations = pv.check_commit(chapter_number, commit, story_state)
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger(__name__)

from core.story_state import StoryState, CharacterState, HookState
from core.contract import ChapterCommit


# ═══════════════════════════════════════════════════════════════
#  死亡状态精确检测（模块级函数，供 PreWriteValidator 和 PostWriteValidator 共用）
# ═══════════════════════════════════════════════════════════════

_DEATH_STATE_PATTERNS: tuple[str, ...] = (
    "已死亡", "确认死亡", "已被击杀", "被击杀", "已死",
    "死亡",  # 保留泛匹配兜底，依赖下面的精确对比逻辑
)


def _is_death_state(state_str: str) -> bool:
    """精确检测状态是否为死亡（避免"死亡之气"等误检）。"""
    s = state_str.strip()
    if s == "死亡":
        return True
    for pat in _DEATH_STATE_PATTERNS:
        if pat in s:
            after = s[s.index(pat) + len(pat):]
            if after and after[0] in "的之、，":
                return False
            return True
    return False


# ═══════════════════════════════════════════════════════════════
#  统一三定律（唯一权威版本）
# ═══════════════════════════════════════════════════════════════

THREE_LAWS: list[str] = [
    "大纲即法律：严格遵循大纲设定，不擅自添加未规划的情节、角色、地点或物品",
    "设定即物理：已有的人物能力、世界观规则、时间线、物品性质必须前后一致，不得矛盾",
    "发明需识别：任何新增的实体、地点、能力必须在章节记录中以【新增】标记明确标注",
]

THREE_LAWS_EN: list[str] = [
    "OUTLINE IS LAW: Do not add unplanned plots, characters, locations, or items beyond the outline.",
    "SETTING IS PHYSICS: Character abilities, world rules, timelines, and item properties must remain consistent.",
    "INVENTIONS MUST BE FLAGGED: Any new entity, location, or ability must be explicitly marked with [NEW] in the chapter record.",
]

# 三定律的快捷描述（用于 report）
LAW_LABELS = ["大纲即法律", "设定即物理", "发明需识别"]


# ═══════════════════════════════════════════════════════════════
#  Data classes
# ═══════════════════════════════════════════════════════════════


@dataclass
class LawViolation:
    """A single violation of the Three Laws."""

    law_index: int  # 0=大纲, 1=设定, 2=标记
    severity: str  # P0 / P1 / P2
    category: str  # 违规类型
    description: str
    suggestion: str = ""
    source: str = ""  # 哪个文件/章节触发的


@dataclass
class ValidationReport:
    """Pre-write or post-write validation result."""

    passed: bool = True
    violations: list[LawViolation] = field(default_factory=list)

    @property
    def p0_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "P0")

    @property
    def p1_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "P1")

    def to_prompt_block(self) -> str:
        """Format violations as a prompt block for injection into writing context."""
        if not self.violations:
            return ""
        lines = ["【⚠️ 三定律预检警告】"]
        for v in self.violations:
            icon = {"P0": "🔴", "P1": "🟡", "P2": "🔵"}.get(v.severity, "⚪")
            law = LAW_LABELS[v.law_index] if v.law_index < len(LAW_LABELS) else f"定律{v.law_index+1}"
            lines.append(f"  {icon} [{law}] {v.description}")
            if v.suggestion:
                lines.append(f"    修: {v.suggestion}")
        lines.append("")
        return "\n".join(lines)

    def to_text(self) -> str:
        """Detailed report."""
        lines = ["## 三定律校验报告"]
        lines.append(f"结果: {'✅ 通过' if self.passed else '❌ 发现违规'}")
        lines.append(f"违规: {len(self.violations)} 条 (P0={self.p0_count}, P1={self.p1_count})")
        for v in self.violations:
            lines.append(f"\n  [{v.severity}] [{LAW_LABELS[v.law_index]}] {v.description}")
            if v.suggestion:
                lines.append(f"    建议: {v.suggestion}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  PreWriteValidator — 写前校验（基于大纲+state）
# ═══════════════════════════════════════════════════════════════


class PreWriteValidator:
    """
    在写章节之前，根据大纲和现有 story-state 进行三定律校验。

    检测内容：
      - 大纲引用了 bible/story-state 中不存在的角色/地点（Law 1）
      - 大纲提议的事件与角色当前状态矛盾（Law 2）
      - 大纲引入了新实体但没有注明标记（Law 3）
    """

    def __init__(self, project_dir: str | Path) -> None:
        self.project_dir = Path(project_dir)
        self._bible: dict = {}

    # ── 公开 API ──────────────────────────────────────────────

    def check_outline(
        self,
        chapter_number: int,
        outline: str,
        story_state: StoryState,
    ) -> ValidationReport:
        """
        对即将写的章节大纲进行三定律校验。

        Parameters
        ----------
        chapter_number : int
            当前章节号
        outline : str
            章节大纲文本
        story_state : StoryState
            当前 story state

        Returns
        -------
        ValidationReport
        """
        violations: list[LawViolation] = []
        self._load_bible()

        # ── Law 1: 大纲即法律 ──────────────────────────────────
        v1 = self._check_law1_outline(chapter_number, outline, story_state)
        violations.extend(v1)

        # ── Law 2: 设定即物理 ──────────────────────────────────
        v2 = self._check_law2_setting(chapter_number, outline, story_state)
        violations.extend(v2)

        # ── Law 3: 发明需识别 ──────────────────────────────────
        v3 = self._check_law3_flag(chapter_number, outline, story_state)
        violations.extend(v3)

        passed = not any(v.severity == "P0" for v in violations)
        return ValidationReport(passed=passed, violations=violations)

    # ── Law 1: 大纲即法律 ──────────────────────────────────────

    def _check_law1_outline(
        self, chapter: int, outline: str, state: StoryState,
    ) -> list[LawViolation]:
        """检查大纲是否引用了不存在的角色/地点。"""
        violations: list[LawViolation] = []

        known_chars = set()
        for cid, ch in state.characters.items():
            if ch.name:
                known_chars.add(ch.name)
        for name in self._bible.get("characters", {}):
            known_chars.add(name)

        # Heuristic: look for potential character names in outline
        potential_names = _extract_unknown_entities(outline, known_chars)
        for name in potential_names:
            violations.append(LawViolation(
                law_index=0,
                severity="P1",
                category="未知角色/地点",
                description=f"大纲中出现已知角色/地点以外的名称「{name}」——如果这是新实体，请在章节中标记【新增】",
                suggestion=f"确认 {name} 是大纲规划的实体，或在写作时标记【新增{name}】",
                source=f"Ch{chapter} outline",
            ))

        return violations

    # ── Law 2: 设定即物理 ──────────────────────────────────────

    def _check_law2_setting(
        self, chapter: int, outline: str, state: StoryState,
    ) -> list[LawViolation]:
        """检查大纲是否与已有设定矛盾。"""
        violations: list[LawViolation] = []

        # 检查角色状态一致性
        for cid, ch in state.characters.items():
            if not ch.name or ch.status != "active":
                continue

            # 角色已死亡或消失？check status
            if ch.state and _is_death_state(ch.state) and ch.name in outline:
                violations.append(LawViolation(
                    law_index=1,
                    severity="P0",
                    category="角色状态冲突",
                    description=f"「{ch.name}」的状态为「{ch.state}」，但大纲中仍引用此人",
                    suggestion="检查是否搞错了角色，或确认该角色以其他形式（幻象/回忆）出现",
                    source=f"Ch{chapter} outline / char_{cid}",
                ))

            # 角色消失超过15章未出现
            if ch.last_appearance > 0 and ch.last_appearance < chapter - 15:
                if ch.name in outline:
                    violations.append(LawViolation(
                        law_index=1,
                        severity="P1",
                        category="角色长期未出现",
                        description=f"「{ch.name}」已连续 {chapter - ch.last_appearance} 章未出现（上次Ch{ch.last_appearance}），"
                                    f"大纲中提及此人可能需要重新引入",
                        suggestion="在章节中给一个过渡性出场理由，避免突兀",
                        source=f"Ch{chapter} outline / char_{cid}",
                    ))

        return violations

    # ── Law 3: 发明需识别 ──────────────────────────────────────

    def _check_law3_flag(
        self, chapter: int, outline: str, state: StoryState,
    ) -> list[LawViolation]:
        """检查是否需要对新增内容做标记。"""
        violations: list[LawViolation] = []

        # 如果大纲内容很多但完全没有"新增"标记，提示
        new_keywords = ["新增", "新出现", "新发现", "新引入", "unknown", "new"]
        has_new_flag = any(kw in outline for kw in new_keywords)

        # 如果大纲较长（>50 chars）但没有标记，且可能包含新实体
        if len(outline) > 50 and not has_new_flag and chapter > 1:
            violations.append(LawViolation(
                law_index=2,
                severity="P2",
                category="可能遗漏新增标记",
                description="大纲较长但未包含明显的「新增」标记。如果本章引入了新实体/地点，请标记",
                suggestion="在 writing prompt 中明确说明哪些是已有实体，哪些是新增",
                source=f"Ch{chapter} outline",
            ))

        return violations

    # ── 辅助 ───────────────────────────────────────────────────

    def _load_bible(self) -> None:
        """Load bible.json if available."""
        bpath = self.project_dir / "bible.json"
        if bpath.exists():
            try:
                self._bible = json.loads(bpath.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("bible.json 加载失败: %s", exc)
                self._bible = {}


# ═══════════════════════════════════════════════════════════════
#  PostWriteValidator — 写后校验（基于已写文本+commit）
# ═══════════════════════════════════════════════════════════════


class PostWriteValidator:
    """
    在章节写完后，对已提取的 ChapterCommit 进行三定律校验。

    检测内容：
      - 新增了未规划的角色/物品但没有标记（Law 1 + Law 3）
      - 已经已有的设定矛盾（Law 2）
      - 伏笔未正确兑现或凭空消失（Law 2）
    """

    def __init__(self, project_dir: str | Path) -> None:
        self.project_dir = Path(project_dir)

    def check_commit(
        self,
        chapter_number: int,
        commit: ChapterCommit,
        story_state: StoryState,
    ) -> ValidationReport:
        """
        对已写章节的 commit 进行三定律校验。

        Parameters
        ----------
        chapter_number : int
            章节号
        commit : ChapterCommit
            DataAgent 提取的 commit
        story_state : StoryState
            当前 story state

        Returns
        -------
        ValidationReport
        """
        violations: list[LawViolation] = []

        # ── 前置守卫 ──────────────────────────────────────────
        if commit is None:
            violations.append(LawViolation(
                law_index=0, severity="P1", category="commit 为空",
                description=f"Ch{chapter_number} 的 commit 为 None，无法进行写后校验",
                source=f"Ch{chapter_number} commit",
            ))
            return ValidationReport(passed=False, violations=violations)

        # ── 空 entity_delta 启发式检查 ────────────────────────
        new_chars = commit.entity_delta.new_characters
        new_locs = commit.entity_delta.new_locations
        new_items = commit.entity_delta.new_items
        if not new_chars and not new_locs and not new_items and len(commit.events) > 3:
            violations.append(LawViolation(
                law_index=0, severity="P2",
                category="可能遗漏新增实体提取",
                description=f"Ch{chapter_number} 有 {len(commit.events)} 个事件但 entity_delta 为空，"
                            f"DataAgent 可能遗漏了新增实体提取",
                suggestion="检查 DataAgent 是否正确提取了新角色/地点/物品，或手动补全 entity_delta",
                source=f"Ch{chapter_number} commit / entity_delta",
            ))

        # ── Law 2 + 3: 检查是否有未标记的新实体 ──────────────
        violations.extend(self._check_new_entities(chapter_number, commit, story_state))

        # ── Law 2: 检查角色状态连续性 ─────────────────────────
        violations.extend(self._check_state_continuity(chapter_number, commit, story_state))

        # ── Law 2: 检查伏笔结算 ───────────────────────────────
        violations.extend(self._check_hook_consistency(chapter_number, commit, story_state))

        passed = not any(v.severity == "P0" for v in violations)
        return ValidationReport(passed=passed, violations=violations)

    def _check_new_entities(
        self, chapter: int, commit: ChapterCommit, state: StoryState,
    ) -> list[LawViolation]:
        """检查新实体是否在 hooks_created 中有匹配的标记。"""
        violations: list[LawViolation] = []

        new_chars = commit.entity_delta.new_characters
        new_locs = commit.entity_delta.new_locations
        new_items = commit.entity_delta.new_items

        all_new = new_chars + new_locs + new_items

        # 每个新增应该对应一个 hook_created 描述
        hook_descs = [h.lower() for h in commit.hooks_created]
        for entity in all_new:
            name = entity.get("name", entity.get("id", ""))
            if not name:
                continue

            # 检查这个实体是否在 hooks_created 中有对应描述
            matched = False
            for hd in hook_descs:
                if name.lower() in hd:
                    matched = True
                    break

            # 也检查事件描述中是否有标记
            for evt in commit.events:
                if f"【新增】" in evt.description and name in evt.description:
                    matched = True
                    break

            if not matched:
                violations.append(LawViolation(
                    law_index=2,  # 发明需识别
                    severity="P1",
                    category="未标记的新实体",
                    description=f"新增实体「{name}」未在 hooks_created 中找到对应的描述标记",
                    suggestion=f"在 hooks_created 或事件描述中加入「【新增】{name}」标注",
                    source=f"Ch{chapter} commit / entity_delta",
                ))

        return violations

    def _check_state_continuity(
        self, chapter: int, commit: ChapterCommit, state: StoryState,
    ) -> list[LawViolation]:
        """检查角色状态变化是否合理。"""
        violations: list[LawViolation] = []

        for cid, new_state in commit.state_delta.character_states.items():
            if cid in state.characters:
                old_state = state.characters[cid]
                # 精确检测旧状态是否真的是死亡
                if old_state.state and _is_death_state(old_state.state):
                    # 新状态不应该恢复为活跃
                    if "受伤" not in new_state and "死亡" not in new_state:
                        violations.append(LawViolation(
                            law_index=1,
                            severity="P0",
                            category="角色死而复生",
                            description=f"「{old_state.name}」之前的状态为「{old_state.state}」(Ch{old_state.last_appearance})，"
                                        f"但本章将其恢复为「{new_state}」——除非有明确的复活剧情，否则可能是幻觉",
                            suggestion="如果是回忆/闪回/幻象，请在事件的 strand 标注",
                            source=f"Ch{chapter} commit / {cid}",
                        ))

        return violations

    def _check_hook_consistency(
        self, chapter: int, commit: ChapterCommit, state: StoryState,
    ) -> list[LawViolation]:
        """检查已兑现的伏笔是否真实存在。"""
        violations: list[LawViolation] = []

        for hook_desc in commit.hooks_resolved:
            # 在 state.hooks 中查找匹配
            found = False
            for hid, hook in state.hooks.items():
                if hook.status not in ("活跃", "active", "pending"):
                    continue
                if hook.description == hook_desc or hook_desc in hook.description:
                    found = True
                    break

            if not found:
                # 可能是幻象兑现 — 在 state 中加这个 hook 才能兑现
                violations.append(LawViolation(
                    law_index=1,
                    severity="P1",
                    category="伏笔来源不明",
                    description=f"试图兑现的伏笔「{hook_desc[:50]}」在 story-state 中未找到活跃匹配",
                    suggestion="检查是否搞错了伏笔描述，或先将其注册到 hooks 再兑现",
                    source=f"Ch{chapter} commit / hooks_resolved",
                ))

        return violations


# ═══════════════════════════════════════════════════════════════
#  Entity name extraction heuristic
# ═══════════════════════════════════════════════════════════════

# Common Chinese words that appear frequently but are NOT entity names
_STOP_NAMES = {"大纲", "章节", "主角", "配角", "地点", "物品", "事件",
               "新增", "标记", "设定", "剧情", "对话", "战斗", "探索",
               "准备", "出现", "发现", "前往", "返回", "进入", "离开",
               "第一", "第二", "第三", "最后", "开始", "结束", "然后", "突然",
               "这片", "这座", "那个", "这个", "这些", "那些", "什么", "如何",
               "已经", "可以", "想要", "需要", "知道", "觉得", "以为", "应该"}

# Strong role words only — removed problematic words like 来/去/走/想/站/坐
# that cause too many false positives in Chinese narrative text
_STRONG_ROLE_WORDS = {"说", "道", "问", "答", "叫", "喊", "喝道", "说道", "问道"}

# Allow names with middle dot (·) like "艾琳娜·烬羽"
_NAME_CHARS = r"[\u4e00-\u9fff·]"  # Chinese chars + middle dot


def _extract_unknown_entities(text: str, known: set[str]) -> list[str]:
    """
    Heuristic: extract potential entity names from outline text
    that are NOT in the known set.

    Supports:
      - Chinese names 2-5 chars (e.g. "林风", "伊莎贝拉")
      - Names with middle dot (e.g. "艾琳娜·烬羽")
      - Names appearing before strong role words (说/道/问/答/叫/喊)
    """
    # Build set of single characters that are role word triggers
    role_chars: set[str] = set()
    for rw in _STRONG_ROLE_WORDS:
        for ch in rw:
            role_chars.add(ch)

    found: list[str] = []
    for i, ch in enumerate(text):
        if ch not in role_chars and ch != "」":
            continue
        # Walk backward: collect contiguous CJK chars that are NOT role triggers
        block_end = i
        j = i - 1
        while j >= 0:
            c = text[j]
            is_cjk = c == "·" or ("\u4e00" <= c <= "\u9fff")
            if not is_cjk or c in role_chars:
                break  # stop at non-CJK or role word char
            j -= 1
        block_start = j + 1
        block_len = block_end - block_start
        if block_len < 2:
            continue
        # Try all possible name lengths from this block (up to 7 for names with ·)
        for name_len in range(min(7, block_len), 1, -1):
            name = text[block_end - name_len:block_end]
            if name[-1] in role_chars:
                continue
            found.append(name)
            break  # Take longest valid name

    # Deduplicate and filter
    result = []
    seen = set()
    for name in found:
        if name in seen:
            continue
        seen.add(name)
        if name in known or name in _STOP_NAMES:
            continue
        result.append(name)
    return result


# ═══════════════════════════════════════════════════════════════
#  Prompt block helpers
# ═══════════════════════════════════════════════════════════════


def format_three_laws_block(lang: str = "zh") -> str:
    """Format three laws as a prompt injection block."""
    laws = THREE_LAWS if lang == "zh" else THREE_LAWS_EN
    lines = ["【创作纪律 — 防幻觉三定律】"]
    for i, law in enumerate(laws, 1):
        lines.append(f"  {i}. {law}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="防幻觉三定律校验")
    parser.add_argument("--dir", default=".", help="项目目录")
    parser.add_argument("--chapter", type=int, default=0, help="当前章节号")
    parser.add_argument("--pre", help="预检模式：传入大纲文本")
    parser.add_argument("--post", help="写后校验模式：传入 chapter.md 文件")
    args = parser.parse_args()

    project = Path(args.dir)
    state = StoryState.load(project)

    if args.pre:
        print(f"【写前校验】Ch{args.chapter or '?'}\n")
        pv = PreWriteValidator(project)
        report = pv.check_outline(args.chapter or 0, args.pre, state)
        print(report.to_text())
        if report.violations:
            print(f"\n{report.to_prompt_block()}")

    elif args.post:
        print(f"【写后校验】Ch{args.chapter or '?'}\n")
        text = Path(args.post).read_text(encoding="utf-8")
        from agents.data_agent import DataAgent
        da = DataAgent(project)
        commit = da.extract_commit(text, args.chapter or 0, f"Ch{args.chapter}", state)
        pv = PostWriteValidator(project)
        report = pv.check_commit(args.chapter or 0, commit, state)
        print(report.to_text())

    else:
        parser.print_help()
