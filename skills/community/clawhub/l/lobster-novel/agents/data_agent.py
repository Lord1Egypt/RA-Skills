from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.contract import (
    ChapterCommit,
    ChapterCommitEvent,
    EntityDelta,
    StateDelta,
    save_commit,
)
from core.story_state import StoryState


# ---------------------------------------------------------------------------
# Known markers
# ---------------------------------------------------------------------------

_DIALOGUE_MARKERS = {"说", "道", "问", "回答"}
_ACTION_KEYWORDS = {"推", "拉", "走", "跑", "站", "蹲", "握", "举", "打开", "关闭", "拿", "放"}
_REVELATION_KEYWORDS = {"发现", "知道", "意识到", "明白", "看到"}
_TRANSITION_KEYWORDS = {"最后", "终于", "从此", "这是"}
_EMOTION_KEYWORDS = {"哭", "笑", "沉默", "颤抖", "紧", "深呼"}
_WORLD_BUILDING_KEYWORDS = {"世界", "规则", "力量", "历史", "传说"}

_KNOWN_LOCATIONS = {
    "灰港镇", "铁匠铺", "码头", "盐碱地", "荒地", "灯塔",
    "酒馆", "教堂", "广场", "城墙", "港口", "市场",
    "议事厅", "老城区", "新城区", "旅馆", "钟楼", "墓地",
    "军营", "地牢", "下水道", "神庙", "祭坛",
}
_TIME_MARKERS = {
    "清晨", "午后", "黄昏", "傍晚", "深夜", "黎明",
    "天亮", "天黑", "日出", "日落", "早晨", "中午", "晚上",
}
_LOCATION_KEYWORDS = list(_KNOWN_LOCATIONS) + [
    "森林", "山谷", "河畔", "桥头", "山洞", "矿洞",
    "城堡", "塔楼", "花园", "庭院", "大殿",
]
_HOOK_CREATE_PATTERNS = ["留下了一个", "记住了", "标记了", "预示"]
_HOOK_RESOLVE_PATTERNS = [
    "兑现", "终于", "解开了", "找到了答案",
    "消散", "解体", "消失", "缩回地下", "闭合", "关闭",
    "完成了任务", "回到了", "路通了", "母亲", "穿过光门",
]

# ---------------------------------------------------------------------------
# Name-extraction exclusions (common non-character phrases matching the regex)
# ---------------------------------------------------------------------------

_NAME_EXCLUSIONS = {
    # 中文功能词/代词/句子碎片（防注册为角色名）
    "她", "他", "它", "这", "那", "我", "你", "我们", "他们", "她们",
    "它们", "自己", "什么", "怎么", "这样", "那样", "那个", "这个",
    "不是", "就是", "但是", "可是", "只是", "还是", "或者", "而且",
    "因为", "所以", "然后", "之后", "之前", "时候", "地方", "东西",
    "一个", "一些", "一点", "那种", "这些", "那些", "那么", "这么",
    "没有", "可以", "应该", "能够", "需要", "可能", "已经", "正在",
    "看到", "听到", "感到", "觉得", "知道", "发现", "开始", "结束",
    "继续", "停下", "走出", "进入", "回到", "离开", "穿过", "打开",
    "看见", "听见", "像是", "不像", "不像", "仿佛", "好像", "似乎",
    "盖子", "传来", "传来", "告诉", "回答", "解释", "描述", "补充",
    "这个", "那个", "哪个", "这些", "那些",
    "可以", "可是", "还是", "就是", "但是", "而且", "或者",
    "因为", "所以", "如果", "虽然", "然而", "不过", "只是",
    "什么", "怎么", "这样", "那样", "这么", "那么",
    "他们", "她们", "它们", "我们", "你们", "大家",
    "没有", "还有", "已经", "知道", "觉得", "看见",
    "需要", "想要", "开始", "继续", "后来", "接着",
    "刚才", "立刻", "马上", "突然", "然后", "最后",
    "前面", "后面", "左边", "右边", "上面", "下面",
    "一眼", "一下", "第一", "第二", "首先", "其次",
    "比如", "例如", "据说", "所谓", "可谓", "便是",
    "算是", "说是", "凡是", "算是","总是","全是","倒是","就是",
}


class DataAgent:
    """Extracts structured ChapterCommit data from chapter text using rule-based heuristics."""

    def __init__(self, project_dir: str | Path) -> None:
        self.project_dir = Path(project_dir)

    # ------------------------------------------------------------------
    # Main extraction
    # ------------------------------------------------------------------

    def extract_commit(
        self,
        chapter_text: str,
        chapter_number: int,
        chapter_title: str,
        story_state: StoryState,
    ) -> ChapterCommit:
        lines = chapter_text.split("\n")
        total_lines = len(lines)

        # 1. word_count
        word_count = sum(1 for ch in chapter_text if "\u4e00" <= ch <= "\u9fff")

        # 2. events
        events = self._extract_events(lines, story_state)
        if not events:
            first_line = lines[0].strip() if lines else ""
            events = [
                ChapterCommitEvent(
                    event_type="action",
                    description=(first_line[:80] if first_line else "(空章节)"),
                    strand="quest",
                )
            ]

        # 3. state_delta
        state_delta = self._extract_state_delta(lines, story_state)

        # 4. entity_delta
        entity_delta = self._extract_entity_delta(
            chapter_text, lines, story_state
        )

        # 5. summary_text
        summary_text = chapter_text[:100].replace("\n", " ").strip()

        # 6 / 7. hooks
        hooks_created = self._extract_hooks(lines, chapter_number)
        hooks_resolved = self._extract_hooks_resolved(lines)

        # 8. strand_ratios
        strand_ratios = self._calculate_strand_ratios(events)

        commit = ChapterCommit(
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            word_count=word_count,
            events=events,
            state_delta=state_delta,
            entity_delta=entity_delta,
            summary_text=summary_text,
            hooks_created=hooks_created,
            hooks_resolved=hooks_resolved,
            strand_ratios=strand_ratios,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Print brief summary
        print(
            f"[DataAgent] Chapter {chapter_number} — "
            f"{word_count} chars, {len(events)} events, "
            f"{len(state_delta.character_states)} characters, "
            f"{len(entity_delta.new_characters)} new entities"
        )
        return commit

    # ------------------------------------------------------------------
    # Event extraction
    # ------------------------------------------------------------------

    @staticmethod
    def _classify_line(
        line: str, known_chars: set[str]
    ) -> tuple[str, str, list[str], str | None]:
        """Return (event_type, description, entities_mentioned, strand_override)."""
        stripped = line.strip()
        desc = stripped[:80]

        entities = [c for c in known_chars if c in stripped]
        strand = None  # None means default "quest"

        # Try each event type in priority order
        # emotional_beat (before action so "颤抖" doesn't get caught as action)
        if any(kw in stripped for kw in _EMOTION_KEYWORDS):
            return "emotional_beat", desc, entities, strand

        # dialogue
        if any(kw in stripped for kw in _DIALOGUE_MARKERS) and stripped.endswith(
            ("。", "！", "？", "”", "」", "』")
        ):
            if any(kw in stripped for kw in _WORLD_BUILDING_KEYWORDS):
                strand = "constellation"
            else:
                strand = "fire"
            return "dialogue", desc, entities, strand

        if any(kw in stripped for kw in _WORLD_BUILDING_KEYWORDS):
            strand = "constellation"

        # revelation
        if any(kw in stripped for kw in _REVELATION_KEYWORDS):
            if strand is None:
                strand = "constellation" if any(
                    kw in stripped for kw in _WORLD_BUILDING_KEYWORDS
                ) else "quest"
            return "revelation", desc, entities, strand

        # action
        if any(kw in stripped for kw in _ACTION_KEYWORDS):
            return "action", desc, entities, strand

        # transition
        if any(kw in stripped for kw in _TRANSITION_KEYWORDS):
            return "transition", desc, entities, "quest"

        # Fallback — check if it looks like a sentence (ends with punctuation)
        if stripped and stripped[-1] in "。！？":
            if any(kw in stripped for kw in _WORLD_BUILDING_KEYWORDS):
                return "action", desc, entities, "constellation"
            return "action", desc, entities, strand

        return "", desc, entities, strand

    def _extract_events(
        self, lines: list[str], story_state: StoryState
    ) -> list[ChapterCommitEvent]:
        known_chars = set()
        for cid, ch in story_state.characters.items():
            known_chars.add(cid)
            known_chars.add(ch.name)

        events: list[ChapterCommitEvent] = []
        for i, raw_line in enumerate(lines):
            line = raw_line.strip()
            if not line:
                continue

            event_type, desc, entities, strand_override = self._classify_line(
                line, known_chars
            )
            if not event_type:
                continue

            strand = strand_override or "quest"

            events.append(
                ChapterCommitEvent(
                    event_type=event_type,
                    description=desc,
                    entities_mentioned=entities,
                    strand=strand,
                )
            )
        return events

    # ------------------------------------------------------------------
    # State delta
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_state_delta(
        lines: list[str], story_state: StoryState
    ) -> StateDelta:
        character_states: dict[str, str] = {}
        location: str | None = None
        time_progression: str | None = None

        full_text = "\n".join(lines)

        # Character presence
        for cid, ch in story_state.characters.items():
            if cid in full_text or ch.name in full_text:
                character_states[cid] = "present"

        # Location — scan for known location markers, take last occurrence
        last_loc_pos = -1
        for loc in _LOCATION_KEYWORDS:
            pos = full_text.rfind(loc)
            if pos > last_loc_pos:
                last_loc_pos = pos
                location = loc

        # Time — scan for time markers, take last occurrence
        last_time_pos = -1
        for tm in _TIME_MARKERS:
            pos = full_text.rfind(tm)
            if pos > last_time_pos:
                last_time_pos = pos
                time_progression = tm

        return StateDelta(
            character_states=character_states,
            location=location,
            time_progression=time_progression,
        )

    # ------------------------------------------------------------------
    # Entity delta
    # ------------------------------------------------------------------

    def _extract_entity_delta(
        self,
        chapter_text: str,
        lines: list[str],
        story_state: StoryState,
    ) -> EntityDelta:
        known_char_ids = set(story_state.characters.keys())
        known_char_names = {ch.name for ch in story_state.characters.values()}
        all_known_chars = known_char_ids | known_char_names

        # New characters: find potential name-patterns (2-4 char proper noun
        # followed by 是/说/叫/名为 at sentence-start or after punctuation)
        new_characters: list[dict[str, Any]] = []
        new_char_matches = re.findall(
            r"(?:^|[。！？，\n])([\u4e00-\u9fff]{2,4})(?:是|说|叫|名为)",
            chapter_text,
        )
        seen_names: set[str] = set()
        for name in new_char_matches:
            name = name.strip()
            if (
                name
                and name not in all_known_chars
                and name not in seen_names
                and name not in _NAME_EXCLUSIONS
                and not any(
                    kw in name for kw in _DIALOGUE_MARKERS | _ACTION_KEYWORDS
                )
            ):
                seen_names.add(name)
                new_characters.append(
                    {"id": name, "name": name, "role": "配角", "description": ""}
                )

        # New locations: find location keywords NOT already in the known set
        new_locations: list[dict[str, Any]] = []
        found_new_locs: set[str] = set()
        for loc in _LOCATION_KEYWORDS:
            if loc in chapter_text and loc not in _KNOWN_LOCATIONS and loc not in found_new_locs:
                found_new_locs.add(loc)
                new_locations.append(
                    {"id": loc, "name": loc, "description": ""}
                )

        return EntityDelta(
            new_characters=new_characters,
            new_locations=new_locations,
        )

    # ------------------------------------------------------------------
    # Hooks
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_hooks(
        lines: list[str], chapter_number: int
    ) -> list[str]:
        hooks: list[str] = []
        for line in lines:
            stripped = line.strip()
            for pattern in _HOOK_CREATE_PATTERNS:
                if pattern in stripped:
                    if stripped not in hooks:
                        hooks.append(stripped[:120])
                    break
        return hooks

    @staticmethod
    def _extract_hooks_resolved(lines: list[str]) -> list[str]:
        resolved: list[str] = []
        for line in lines:
            stripped = line.strip()
            for pattern in _HOOK_RESOLVE_PATTERNS:
                if pattern in stripped:
                    if stripped not in resolved:
                        resolved.append(stripped[:120])
                    break
        return resolved

    # ------------------------------------------------------------------
    # Strand ratios
    # ------------------------------------------------------------------

    @staticmethod
    def _calculate_strand_ratios(
        events: list[ChapterCommitEvent],
    ) -> dict[str, float]:
        total = len(events)
        if total == 0:
            return {"quest": 0.0, "fire": 0.0, "constellation": 0.0}

        counts: dict[str, int] = {"quest": 0, "fire": 0, "constellation": 0}
        for e in events:
            s = e.strand
            if s in counts:
                counts[s] += 1

        return {
            "quest": round(counts["quest"] / total, 4),
            "fire": round(counts["fire"] / total, 4),
            "constellation": round(counts["constellation"] / total, 4),
        }

    # ------------------------------------------------------------------
    # Save & integrate
    # ------------------------------------------------------------------

    def save_and_integrate(
        self, commit: ChapterCommit, story_state: StoryState
    ) -> None:
        save_commit(commit, self.project_dir)
        story_state.apply_commit(commit)
        story_state.save(self.project_dir)
        print(
            f"[DataAgent] Chapter {commit.chapter_number} commit saved and "
            f"integrated into story state."
        )
