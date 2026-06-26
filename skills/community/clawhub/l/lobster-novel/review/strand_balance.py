#!/usr/bin/env python3
"""
Strand 节奏量化系统

分析 Quest / Fire / Constellation 三条线索的占比、分布、连续性，
为写作决策提供数据支持。

Strand 定义:
  quest         — 主线任务 / 外部冲突
  fire          — 角色内心 / 情感线
  constellation — 世界谜题 / 背景设定

默认目标比例: quest=40%, fire=30%, constellation=30%
"""
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# 兼容直接执行和作为模块导入
import sys
try:
    from .quality_check import Issue
except ImportError:
    # 直接执行时 fallback 到同级导入
    _review_dir = Path(__file__).parent
    if str(_review_dir) not in sys.path:
        sys.path.insert(0, str(_review_dir))
    from quality_check import Issue

# ═══════════════════════════════════════════════════════════════
#  默认目标比例
# ═══════════════════════════════════════════════════════════════

DEFAULT_TARGETS = {
    "quest": 0.40,
    "fire": 0.30,
    "constellation": 0.30,
}

MAX_STREAK = 3  # 同一线索连续超过3章就警告


# ═══════════════════════════════════════════════════════════════
#  Data classes
# ═══════════════════════════════════════════════════════════════


@dataclass
class StrandAnalysis:
    """Per-chapter strand weight snapshot."""

    chapter: int
    quest: float = 0.0
    fire: float = 0.0
    constellation: float = 0.0

    def dominant(self) -> str:
        """Return the name of the dominant strand."""
        return max(
            {"quest": self.quest, "fire": self.fire, "constellation": self.constellation},
            key=lambda k: getattr(self, k),
        )


@dataclass
class StrandBalanceReport:
    """Full strand health report for a project."""

    issues: list[Issue] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)
    overall_score: int = 100

    # --- raw data ---
    chapter_analyses: list[StrandAnalysis] = field(default_factory=list)
    ratios: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_TARGETS))
    streaks: dict[str, int] = field(default_factory=lambda: {"quest": 0, "fire": 0, "constellation": 0})
    current_dominant: str = ""

    # --- warning flags ---
    has_streak_warning: bool = False
    has_imbalance_warning: bool = False
    has_starvation_warning: bool = False

    def to_issues(self) -> list[Issue]:
        """Interface compatibility: same as .issues property."""
        return self.issues

    def to_text(self) -> str:
        lines = ["## Strand 节奏分析\n"]
        lines.append(f"  整体评分: {self.overall_score}/100\n")

        # 比例
        lines.append("### 当前比例 vs 目标")
        for s in ["quest", "fire", "constellation"]:
            label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}[s]
            cur = self.ratios.get(s, 0)
            tgt = DEFAULT_TARGETS[s]
            bar_len = 20
            cur_bar = "█" * max(0, min(bar_len, int(cur * bar_len)))
            tgt_mark = " " * int(tgt * bar_len) + "│"
            lines.append(f"  {label:<6} {cur:>5.1%} (目标 {tgt:>3.0%}) {cur_bar}")
            lines.append(f"          {tgt_mark} ← 目标")

        # 连续情况
        lines.append("\n### 连续章节")
        for s in ["quest", "fire", "constellation"]:
            label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}[s]
            streak = self.streaks.get(s, 0)
            warn = " ⚠️" if streak > MAX_STREAK else ""
            lines.append(f"  {label}{'':>6}{streak} 章连续{warn}")

        if self.current_dominant:
            dominant_label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}.get(self.current_dominant, self.current_dominant)
            lines.append(f"\n  当前主导线索: {dominant_label}")

        # 问题列表
        if self.issues:
            lines.append("\n### 问题")
            for i in self.issues:
                lines.append(f"  [{i.severity}] {i.description}")
                if i.suggestion:
                    lines.append(f"    修: {i.suggestion}")

        return "\n".join(lines)


# ── 安全 int 转换（跳过非数字 key 如 "meta" / "total"）───────


def _safe_int(k: str) -> int:
    try:
        return int(k)
    except ValueError:
        return -1


# ═══════════════════════════════════════════════════════════════
#  StrandAnalyzer
# ═══════════════════════════════════════════════════════════════


class StrandAnalyzer:
    """
    Read story-state.json (or a dict) and produce a StrandBalanceReport.
    """

    def __init__(self, state_path: Optional[Path] = None) -> None:
        self.state_path = state_path

    # ── 从 story-state.json 加载 ────────────────────────────────

    def analyze_from_file(self, state_path: Path, current_chapter: Optional[int] = None) -> StrandBalanceReport:
        """Load story-state.json and run analysis."""
        if not state_path.exists():
            return StrandBalanceReport(
                issues=[Issue(role="Strand分析师", severity="P2", category="无状态文件",
                              description="story-state.json 不存在，无法分析 Strand 节奏")],
                scores={"Strand分析师": 0},
                overall_score=0,
            )
        raw = json.loads(state_path.read_text(encoding="utf-8"))
        return self.analyze(raw, current_chapter)

    # ── 从 dict 分析（供 QualityChecker 调用）───────────────────

    def analyze(self, state: dict, current_chapter: Optional[int] = None) -> StrandBalanceReport:
        """
        Analyze strand balance from a story-state dict.
        """
        issues: list[Issue] = []
        strands_raw = state.get("strands", {})
        chapters_raw = state.get("chapters", {})

        # 自动取最大章节号为当前章节
        chapter_nums = sorted(
            _safe_int(k) for k in chapters_raw if _safe_int(k) >= 0
        )
        if current_chapter is None:
            current_chapter = max(chapter_nums) if chapter_nums else 0

        # 提取 strand ratios
        ratios = {
            "quest": strands_raw.get("quest_ratio", DEFAULT_TARGETS["quest"]),
            "fire": strands_raw.get("fire_ratio", DEFAULT_TARGETS["fire"]),
            "constellation": strands_raw.get("constellation_ratio", DEFAULT_TARGETS["constellation"]),
        }
        streaks = {
            "quest": strands_raw.get("quest_streak", 0),
            "fire": strands_raw.get("fire_streak", 0),
            "constellation": strands_raw.get("constellation_streak", 0),
        }

        # 决定当前主导线索
        current_dominant = max(ratios, key=lambda k: ratios[k])

        # 逐章 strand_weights（跳过非数字 key）
        chapter_analyses: list[StrandAnalysis] = []
        for num in chapter_nums:
            ch = chapters_raw.get(str(num), {})
            weights = ch.get("strand_weights", {})
            chapter_analyses.append(StrandAnalysis(
                chapter=num,
                quest=weights.get("quest", 0),
                fire=weights.get("fire", 0),
                constellation=weights.get("constellation", 0),
            ))

        # ── 违规检测 ────────────────────────────────────────

        # 1. 单一线索过长连续
        has_streak_warning = False
        for strand, streak in streaks.items():
            if streak > MAX_STREAK:
                has_streak_warning = True
                label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}[strand]
                issues.append(Issue(
                    role="Strand分析师",
                    severity="P1",
                    category="线索连续过长",
                    description=f"「{label}」已连续 {streak} 章未出现（上限 {MAX_STREAK}）",
                    suggestion=f"在下一章加入 {label} 相关情节，或调整章节的 strand 分配",
                ))

        # 2. 比例失衡（偏离目标 >20%）
        has_imbalance_warning = False
        for strand, ratio in ratios.items():
            target = DEFAULT_TARGETS[strand]
            deviation = abs(ratio - target)
            if deviation > 0.15:  # 偏离目标 15% 以上
                has_imbalance_warning = True
                label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}[strand]
                direction = "过高" if ratio > target else "过低"
                issues.append(Issue(
                    role="Strand分析师",
                    severity="P2",
                    category="比例偏离",
                    description=f"「{label}」占比 {ratio:.0%}，目标 {target:.0%}，{direction} {deviation:.0%}",
                    suggestion=f"在近几章调整 {label} 权重，向目标 {target:.0%} 靠拢",
                ))

        # 3. 线索缺失（某线索多章未出现）
        has_starvation_warning = False
        for strand, streak in streaks.items():
            if streak > 5:  # 超过 5 章未出现
                has_starvation_warning = True
                label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}[strand]
                issues.append(Issue(
                    role="Strand分析师",
                    severity="P1",
                    category="线索长期缺失",
                    description=f"「{label}」已连续 {streak} 章未出现，可能丢失读者",
                    suggestion=f"尽快在 1-2 章内重拾 {label}，维持三条线的平衡交替",
                ))

        # 4. 权重和归一化检查（避免写入未归一化数据导致误导）
        for ca in chapter_analyses:
            total_w = ca.quest + ca.fire + ca.constellation
            if total_w == 0:
                # 全零权重 — 可能是未标注章节，跳过
                continue
            if total_w < 0.5 or total_w > 1.5:
                issues.append(Issue(
                    role="Strand分析师", severity="P2",
                    category="权重异常",
                    description=f"章节 {ca.chapter} 的 strand 权重和 {total_w:.2f} 偏离 1.0 过大",
                    suggestion="检查该章节的 strand_weights 是否正确填写",
                ))

        # 5. 活力评估（最近 5 章的多样性和节奏感）
        recent = [ca for ca in chapter_analyses if ca.chapter > current_chapter - 5 and ca.chapter <= current_chapter]
        if len(recent) >= 3:
            dominant_set = set(ca.dominant() for ca in recent)
            if len(dominant_set) <= 1:
                sole_strand = list(dominant_set)[0] if dominant_set else "(无数据)"
                label = {"quest": "主线", "fire": "情感", "constellation": "世界观"}.get(sole_strand, sole_strand)
                issues.append(Issue(
                    role="Strand分析师",
                    severity="P2",
                    category="节奏单调",
                    description=f"最近 {len(recent)} 章全部以「{label}」主导，缺乏线索切换",
                    suggestion="在 1-2 章内切换到其他线索，保持三条线交替推进",
                ))

        # 计算评分
        p0_count = sum(1 for i in issues if i.severity == "P0")
        p1_count = sum(1 for i in issues if i.severity == "P1")
        p2_count = sum(1 for i in issues if i.severity == "P2")
        overall = max(100 - p0_count * 20 - p1_count * 10 - p2_count * 5, 0)

        return StrandBalanceReport(
            issues=issues,
            scores={"Strand分析师": overall},
            overall_score=overall,
            chapter_analyses=chapter_analyses,
            ratios=ratios,
            streaks=streaks,
            current_dominant=current_dominant,
            has_streak_warning=has_streak_warning,
            has_imbalance_warning=has_imbalance_warning,
            has_starvation_warning=has_starvation_warning,
        )


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Strand 节奏量化分析")
    parser.add_argument("story_state", help="story-state.json 路径")
    parser.add_argument("--chapter", type=int, default=0, help="当前章节数（可选）")
    args = parser.parse_args()

    analyzer = StrandAnalyzer()
    report = analyzer.analyze_from_file(Path(args.story_state), args.chapter)
    print(report.to_text())
