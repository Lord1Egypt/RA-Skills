#!/usr/bin/env python3
"""
lobster-novel: Beat Sheet / story structure templates (inspired by Sudowrite).
Pre-built story structures that map chapter beats to narrative function.

Templates:
- Three-Act (三幕式): Setup → Confrontation → Resolution
- Hero's Journey (英雄之旅): 12 stages
- Save the Cat: 15 beats
- Kishotenketsu (起承転結): 4-act Chinese/Japanese structure
"""
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Beat:
    """A single story beat."""
    name: str
    chapter_range: tuple  # (start, end) — e.g. (1, 3) means chapters 1-3
    function: str         # what this beat accomplishes
    hook_type: str = ""   # question / reveal / danger / new_element / cliffhanger
    description: str = ""
    word_target: int = 2500
    emotional_tone: str = "neutral"

    def to_prompt(self, chapter_num: int) -> str:
        return (
            f"Beat: {self.name} (ch{chapter_num})\n"
            f"Function: {self.function}\n"
            f"Tone: {self.emotional_tone}\n"
            f"Hook: {self.hook_type or 'none'}\n"
        )


@dataclass
class BeatSheet:
    """A complete story structure template."""
    name: str
    description: str
    total_chapters: int
    beats: List[Beat] = field(default_factory=list)

    def validate(self) -> List[str]:
        """Check if the beat sheet covers all chapters."""
        errors = []
        covered = set()
        for b in self.beats:
            for ch in range(b.chapter_range[0], b.chapter_range[1] + 1):
                covered.add(ch)
        for ch in range(1, self.total_chapters + 1):
            if ch not in covered:
                errors.append(f"Chapter {ch} not covered by any beat")
        return errors

    def get_beat_for_chapter(self, chapter: int) -> Optional[Beat]:
        for b in self.beats:
            if b.chapter_range[0] <= chapter <= b.chapter_range[1]:
                return b
        return None

    def to_text(self) -> str:
        lines = [f"# {self.name}", self.description, "", "## Beats"]
        for i, b in enumerate(self.beats, 1):
            ch_range = f"ch{b.chapter_range[0]}-{b.chapter_range[1]}"
            lines.append(f"  {i:2d}. [{ch_range:>8}] {b.name}")
            lines.append(f"       {b.description[:70]}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# Built-in templates
# ═══════════════════════════════════════════════════════════════

def three_act_structure(total_chapters: int = 24) -> BeatSheet:
    """Three-Act structure (比例: 25%-50%-25%)."""
    a1_end = max(1, int(total_chapters * 0.25))
    a2_end = max(a1_end + 1, int(total_chapters * 0.75))
    midpoint = (a1_end + a2_end) // 2

    return BeatSheet(
        name="Three-Act (三幕式)",
        description="经典三幕结构: 建置→对抗→结局",
        total_chapters=total_chapters,
        beats=[
            Beat("Inciting Incident", (1, 2), "引入主角和世界，触发事件",
                 hook_type="question", emotional_tone="mysterious"),
            Beat("First Act Climax", (3, a1_end), "主角决定踏上旅程/接受挑战",
                 hook_type="reveal", emotional_tone="determined"),
            Beat("Rising Action", (a1_end + 1, midpoint - 1), "冲突升级，反派展现",
                 hook_type="danger", emotional_tone="tense"),
            Beat("Midpoint Twist", (midpoint, midpoint), "重大反转， stakes升高",
                 hook_type="reveal", emotional_tone="shocking"),
            Beat("Darkest Hour", (midpoint + 1, a2_end - 1), "主角面临最大挑战",
                 hook_type="danger", emotional_tone="desperate"),
            Beat("Second Act Climax", (a2_end, a2_end), "终极对决前的最后准备",
                 hook_type="cliffhanger", emotional_tone="resolved"),
            Beat("Final Confrontation", (a2_end + 1, min(a2_end + 2, total_chapters - 1)),
                 "与反派的最终对决", hook_type="reveal", emotional_tone="climax"),
            Beat("Resolution", (total_chapters - 1, total_chapters), "收束支线,新常态",
                 hook_type="", emotional_tone="peaceful"),
        ]
    )


def heros_journey(total_chapters: int = 24) -> BeatSheet:
    """Campbell's 12-stage Hero's Journey adapted for chapters."""
    c = total_chapters

    def ch(pos: float) -> int:
        return max(1, min(c, int(c * pos / 12)))

    return BeatSheet(
        name="Hero's Journey (英雄之旅)",
        description="坎贝尔12阶段英雄之旅",
        total_chapters=c,
        beats=[
            Beat("Ordinary World", (1, ch(1.5)), "展示主角日常",
                 hook_type="question", emotional_tone="neutral"),
            Beat("Call to Adventure", (ch(1.5) + 1, ch(2.5)), "冒险召唤",
                 hook_type="question", emotional_tone="mysterious"),
            Beat("Refusal", (ch(2.5) + 1, ch(3.5)), "拒绝召唤",
                 hook_type="", emotional_tone="hesitant"),
            Beat("Meeting Mentor", (ch(3.5) + 1, ch(4.5)), "遇上导师",
                 hook_type="reveal", emotional_tone="hopeful"),
            Beat("Crossing Threshold", (ch(4.5) + 1, ch(5.5)), "踏入未知世界",
                 hook_type="new_element", emotional_tone="excited"),
            Beat("Tests & Allies", (ch(5.5) + 1, ch(7)), "考验/结盟",
                 hook_type="danger", emotional_tone="adventurous"),
            Beat("Approach", (ch(7) + 1, ch(8)), "接近核心挑战",
                 hook_type="cliffhanger", emotional_tone="tense"),
            Beat("Ordeal", (ch(8) + 1, ch(9)), "最严峻的考验",
                 hook_type="reveal", emotional_tone="climax"),
            Beat("Reward", (ch(9) + 1, ch(10)), "获得奖励/成长",
                 hook_type="", emotional_tone="joyful"),
            Beat("Road Back", (ch(10) + 1, ch(11)), "回归之路，最后挑战",
                 hook_type="danger", emotional_tone="desperate"),
            Beat("Resurrection", (ch(11) + 1, ch(11.5)), "最后一次考验",
                 hook_type="reveal", emotional_tone="climax"),
            Beat("Return", (ch(11.5) + 1, c), "带着宝藏回归, 新常态",
                 hook_type="", emotional_tone="peaceful"),
        ]
    )


def save_the_cat(total_chapters: int = 24) -> BeatSheet:
    """Save the Cat's 15-beat structure by Blake Snyder."""
    c = total_chapters
    beats = [
        Beat("Opening Image", (1, 1), "主角生活的快照", emotional_tone="neutral"),
        Beat("Theme Stated", (2, 2), "暗示故事主题", hook_type="question", emotional_tone="thoughtful"),
        Beat("Set-Up", (3, int(c * 0.1)), "展示主角缺陷和世界", hook_type="", emotional_tone="neutral"),
        Beat("Catalyst", (int(c * 0.1) + 1, int(c * 0.1) + 1), "激励事件",
             hook_type="reveal", emotional_tone="shocking"),
        Beat("Debate", (int(c * 0.1) + 2, int(c * 0.18)), "犹豫和讨论",
             hook_type="question", emotional_tone="hesitant"),
        Beat("Break Into Act 2", (int(c * 0.18) + 1, int(c * 0.2)), "踏入新世界",
             hook_type="new_element", emotional_tone="excited"),
        Beat("B Story", (int(c * 0.2) + 1, int(c * 0.3)), "引入支线/爱情线",
             hook_type="", emotional_tone="warm"),
        Beat("Fun & Games", (int(c * 0.3) + 1, int(c * 0.45)), "探索新世界的乐趣",
             hook_type="", emotional_tone="fun"),
        Beat("Midpoint", (int(c * 0.45) + 1, int(c * 0.5)), "假胜利或假失败",
             hook_type="reveal", emotional_tone="shocking"),
        Beat("Bad Guys Close In", (int(c * 0.5) + 1, int(c * 0.6)), "反派逼近",
             hook_type="danger", emotional_tone="tense"),
        Beat("All Is Lost", (int(c * 0.6) + 1, int(c * 0.65)), "一切尽失",
             hook_type="cliffhanger", emotional_tone="desperate"),
        Beat("Dark Night of the Soul", (int(c * 0.65) + 1, int(c * 0.7)), "心灵的黑暗",
             hook_type="", emotional_tone="melancholic"),
        Beat("Break Into Act 3", (int(c * 0.7) + 1, int(c * 0.73)), "顿悟/反弹",
             hook_type="reveal", emotional_tone="determined"),
        Beat("Finale", (int(c * 0.73) + 1, int(c * 0.9)), "最终对决",
             hook_type="reveal", emotional_tone="climax"),
        Beat("Final Image", (int(c * 0.9) + 1, c), "与开场对比, 展示成长",
             hook_type="", emotional_tone="peaceful"),
    ]
    return BeatSheet(name="Save the Cat", description="Blake Snyder 15-beat结构",
                     total_chapters=c, beats=beats)


def kishotenketsu(total_chapters: int = 16) -> BeatSheet:
    """起承転結 — classic 4-act structure."""
    q_end = total_chapters // 4
    sh_end = total_chapters // 2
    ten_end = total_chapters * 3 // 4
    return BeatSheet(
        name="Kishotenketsu (起承転結)",
        description="经典四段结构: 起→承→転→結",
        total_chapters=total_chapters,
        beats=[
            Beat("起 (Introduction)", (1, q_end), "引入设定和人物",
                 hook_type="question", emotional_tone="peaceful"),
            Beat("承 (Development)", (q_end + 1, sh_end), "故事深入发展",
                 hook_type="reveal", emotional_tone="warm"),
            Beat("転 (Twist)", (sh_end + 1, ten_end), "转折和冲突",
                 hook_type="cliffhanger", emotional_tone="tense"),
            Beat("結 (Conclusion)", (ten_end + 1, total_chapters), "结局和收束",
                 hook_type="", emotional_tone="peaceful"),
        ]
    )


# Template registry
TEMPLATES = {
    "three-act": three_act_structure,
    "heros-journey": heros_journey,
    "save-the-cat": save_the_cat,
    "kishotenketsu": kishotenketsu,
}


def get_template(name: str, total_chapters: int = 24) -> Optional[BeatSheet]:
    """Get a beat sheet template by name."""
    fn = TEMPLATES.get(name)
    if fn:
        return fn(total_chapters)
    return None


def list_templates() -> str:
    lines = ["Available beat sheet templates:"]
    for name, fn in TEMPLATES.items():
        bs = fn()
        lines.append(f"  {name:<20} {bs.name}")
        lines.append(f"  {'':20} {bs.description}")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="beat sheet generator")
    parser.add_argument("template", nargs="?", default="list",
                        choices=["list"] + list(TEMPLATES.keys()))
    parser.add_argument("--chapters", type=int, default=24)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    if args.template == "list":
        print(list_templates())
    else:
        bs = get_template(args.template, args.chapters)
        if bs:
            print(bs.to_text())
            if args.validate:
                errors = bs.validate()
                if errors:
                    print("\nValidation errors:")
                    for e in errors:
                        print(f"  - {e}")
                else:
                    print("\n✅ All chapters covered")
