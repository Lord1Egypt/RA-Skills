#!/usr/bin/env python3
"""Helpers for late-context-safe IR extraction and parity snapshots."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evals.contract_checks import collect_heading_lines, component_counts, parse_frontmatter
from scripts.guard_validate import resolve_report_class


END_IR_MARKER = "<<<END_IR>>>"
ROLE_LINE_RE = re.compile(r"^(?:User|Assistant|System|Human):")

BASE_REFS = [
    "references/html-shell-template.md",
    "references/html-shell/core-structure.md",
    "references/html-shell/shared-component-css.md",
    "references/html-shell/toc-edit-summary.md",
    "references/html-shell/summary-card.md",
    "references/html-shell/export.md",
    "references/html-shell/print-responsive.md",
    "references/theme-css.md",
    "references/review-checklist.md",
]

THEME_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    (
        "regular-lumen",
        (
            "周报",
            "日报",
            "月报",
            "工作汇报",
            "进展汇报",
            "团队汇报",
            "本周",
            "下周",
            "weekly",
            "daily",
            "monthly",
            "work report",
            "progress report",
            "team report",
            "this week",
            "next week",
            "periodic report",
        ),
    ),
    (
        "corporate-blue",
        (
            "季报",
            "销售",
            "业绩",
            "营收",
            "kpi",
            "数据分析",
            "商业",
            "季度",
            "quarterly",
            "sales",
            "revenue",
            "business",
        ),
    ),
    (
        "minimal",
        (
            "研究",
            "调研",
            "学术",
            "白皮书",
            "内部文档",
            "团队文档",
            "research",
            "survey",
            "academic",
            "whitepaper",
            "internal",
            "editorial",
        ),
    ),
    (
        "dark-tech",
        (
            "技术",
            "架构",
            "api",
            "系统",
            "性能",
            "部署",
            "代码",
            "工程",
            "architecture",
            "system",
            "performance",
            "engineering",
        ),
    ),
    (
        "newspaper",
        (
            "新闻",
            "行业",
            "趋势",
            "观察",
            "报道",
            "news",
            "industry",
            "trend",
            "newsletter",
        ),
    ),
    (
        "data-story",
        (
            "年度",
            "故事",
            "增长",
            "复盘",
            "回顾",
            "annual",
            "story",
            "growth",
            "retrospective",
        ),
    ),
    (
        "fangsong",
        (
            "公文",
            "正式报告",
            "通知",
            "制度",
            "formal document",
            "official notice",
        ),
    ),
    (
        "dark-board",
        (
            "看板",
            "dashboard",
            "board",
            "project board",
            "status board",
            "progress board",
            "品牌",
            "用研",
            "ux",
        ),
    ),
    (
        "corporate-blue",
        (
            "项目进展",
            "项目状态",
            "项目完成",
            "任务进展",
            "project progress",
            "project status",
            "task progress",
        ),
    ),
]


def normalize_text(text: str) -> str:
    stripped = text.strip()
    return stripped + "\n" if stripped else ""


def compute_ir_hash(ir_text: str) -> str:
    return "sha256:" + hashlib.sha256(normalize_text(ir_text).encode("utf-8")).hexdigest()[:16]


def _looks_like_ir(candidate: str) -> bool:
    frontmatter, body = parse_frontmatter(candidate)
    if "title" not in frontmatter:
        return False
    if not body.strip():
        return False
    return "## " in body or ":::" in body


def extract_ir_from_context(context_text: str) -> str:
    """Extract exactly one valid IR block from a noisy context string."""
    lines = context_text.splitlines()
    candidates: list[str] = []

    for start in range(len(lines)):
        if lines[start].strip() != "---":
            continue

        end_frontmatter = None
        for index in range(start + 1, len(lines)):
            if lines[index].strip() == "---":
                end_frontmatter = index
                break
        if end_frontmatter is None:
            continue

        end = len(lines)
        for index in range(end_frontmatter + 1, len(lines)):
            stripped = lines[index].strip()
            if stripped == END_IR_MARKER:
                end = index
                break
            if ROLE_LINE_RE.match(lines[index]) and index > end_frontmatter + 1:
                end = index
                break

        candidate = normalize_text("\n".join(lines[start:end]))
        if _looks_like_ir(candidate):
            candidates.append(candidate)

    unique_candidates = list(dict.fromkeys(candidates))
    if not unique_candidates:
        raise ValueError("No valid IR block found in context.")
    if len(unique_candidates) > 1:
        raise ValueError("Multiple valid IR blocks found in context.")
    return unique_candidates[0]


def resolve_theme(text: str) -> str:
    frontmatter, _ = parse_frontmatter(text)
    theme = frontmatter.get("theme")
    if isinstance(theme, str) and theme.strip():
        return theme.strip()

    lowered = text.lower()
    for resolved_theme, keywords in THEME_KEYWORDS:
        if any(keyword in text or keyword in lowered for keyword in keywords):
            return resolved_theme
    return "corporate-blue"


def resolve_archetype(text: str, counts: dict[str, int]) -> str | None:
    frontmatter, body = parse_frontmatter(text)
    archetype = frontmatter.get("archetype")
    if isinstance(archetype, str) and archetype.strip():
        return archetype.strip()

    lowered = (body or text).lower()
    if any(keyword in lowered for keyword in ("weekly", "update", "next move", "本周", "下周", "下一步")):
        return "update"
    if counts.get("table", 0) or "对比" in body or "comparison" in lowered:
        return "comparison"
    if counts.get("diagram", 0) or counts.get("timeline", 0) or "研究" in body or "research" in lowered:
        return "research"
    if "结论先行" in body or "bottom line" in lowered:
        return "brief"
    return None


def resolve_required_refs(theme: str, counts: dict[str, int]) -> list[str]:
    refs = list(BASE_REFS)
    if counts:
        refs.append("references/rendering-rules.md")
        refs.append("references/rendering/plain-markdown.md")
        refs.append("references/anti-patterns.md")
    if counts.get("kpi", 0):
        refs.append("references/rendering/kpi.md")
    if counts.get("chart", 0):
        refs.append("references/rendering/chart.md")
    if counts.get("table", 0) or counts.get("list", 0):
        refs.append("references/rendering/table-list.md")
    if counts.get("timeline", 0) or counts.get("diagram", 0):
        refs.append("references/rendering/timeline-diagram.md")
    if (
        counts.get("image", 0)
        or counts.get("code", 0)
        or counts.get("callout", 0)
    ):
        refs.append("references/rendering/media-code-callout.md")
    if counts.get("diagram", 0):
        refs.append("references/diagram-decision-rules.md")
    if theme == "regular-lumen":
        refs.append("references/regular-report-content-rules.md")
    return refs


def build_ir_snapshot(ir_text: str) -> dict[str, object]:
    normalized_ir = normalize_text(ir_text)
    counts = component_counts(normalized_ir)
    theme = resolve_theme(normalized_ir)
    return {
        "ir_hash": compute_ir_hash(normalized_ir),
        "resolved_report_class": resolve_report_class(normalized_ir),
        "resolved_theme": theme,
        "resolved_archetype": resolve_archetype(normalized_ir, counts),
        "required_refs": resolve_required_refs(theme, counts),
        "component_counts": counts,
        "headings": collect_heading_lines(normalized_ir),
    }


def build_context_snapshot(context_text: str) -> dict[str, object]:
    return build_ir_snapshot(extract_ir_from_context(context_text))


def build_naive_context_snapshot(context_text: str) -> dict[str, object]:
    normalized = normalize_text(context_text)
    counts = component_counts(normalized)
    theme = resolve_theme(normalized)
    return {
        "resolved_report_class": resolve_report_class(normalized),
        "resolved_theme": theme,
        "resolved_archetype": resolve_archetype(normalized, counts),
        "required_refs": resolve_required_refs(theme, counts),
        "component_counts": counts,
        "headings": collect_heading_lines(normalized),
    }


def compare_snapshots(
    expected: dict[str, object],
    actual: dict[str, object],
    *,
    keys: list[str] | None = None,
) -> list[str]:
    compare_keys = keys or sorted(set(expected) | set(actual))
    drift_fields: list[str] = []
    for key in compare_keys:
        if expected.get(key) != actual.get(key):
            drift_fields.append(key)
    return drift_fields
