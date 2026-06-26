#!/usr/bin/env python3
"""风格模仿主线共享提示词契约。

统一承载：
- refs-only 风格判断边界
- 去 AI 味儿时的事实驱动改写约束
- 风格比较层的输出 schema

这样风格比较、改写示范、批注串联都使用同一套主线规则，
避免把新增要求零散塞进单个提示词或局部规则。
"""

from __future__ import annotations

from typing import Any, Dict, List


STYLE_PROMPT_PROFILE_VERSION = "fact-driven-master-v5-sentence-rewrite"
STYLE_PROFILE_EXTRACTION_VERSION = "paragraph-type-style-mechanism-v2"


STYLE_PROFILE_AXES: List[str] = [
    "logic",
    "density",
    "linking",
    "closure",
    "tone",
    "rhythm",
    "evidence",
    "focus",
    "stance",
    "abstraction",
    "emotion",
    "units",
    "reader",
    "rhetoric",
    "persuasion",
    "markers",
]


STYLE_REWRITE_RULES: List[str] = [
    "Use refs-derived style facts only; do not replace them with generic writing advice.",
    "Every judgment must stay tied to verifiable content already present in the target paragraph.",
    "Do not add new facts, claims, data, or examples that are not supported by the current input.",
    "If certainty is weak, mark it explicitly as possible or tentative instead of asserting it as fact.",
    "Replace vague intensifiers with observable wording when revision is needed.",
    "Prefer cleaner sentence progression over stacked template transitions.",
    "You may reorder or compress existing information, but must not change the core meaning.",
    "Keep the register formal, restrained, and suitable for a computer-science master's thesis.",
    "Avoid hollow endings, decorative quotation marks, and empty rhetorical inflation.",
]


STYLE_OUTPUT_REQUIREMENTS: List[str] = [
    "rewriteVersion must provide one integrated improved paragraph when annotation is needed.",
    "rewriteVersion may only reorganize, trim, clarify, or rebalance existing information.",
    "structureAdjustments must list 2 to 4 concrete paragraph-level revision actions.",
    "suggestion must summarize the overall optimization direction for the whole paragraph.",
    "Each issueItem must include one exact sentenceText copied from the target paragraph.",
    "focusText may narrow the issue to a shorter phrase inside sentenceText, otherwise leave it empty.",
    "Each issueItem must include diffType using one of ~ + -.",
    "Each issueItem must include rewriteText that shows the local sentence-level revision example, unless deletion makes it empty.",
]


def build_style_rewrite_rules_block() -> str:
    return "\n".join(f"{idx}. {rule}" for idx, rule in enumerate(STYLE_REWRITE_RULES, start=1))


def build_style_output_requirements_block() -> str:
    return "\n".join(f"{idx}. {rule}" for idx, rule in enumerate(STYLE_OUTPUT_REQUIREMENTS, start=1))


def build_style_prompt_contract_block() -> str:
    return (
        "## Unified Revision Rules\n"
        f"{build_style_rewrite_rules_block()}\n\n"
        "## Output Requirements\n"
        f"{build_style_output_requirements_block()}"
    )


def build_style_profile_axes_block() -> str:
    return "\n".join(f"{idx}. {axis}" for idx, axis in enumerate(STYLE_PROFILE_AXES, start=1))


def merge_style_suggestion(issue: Dict[str, Any]) -> str:
    """把 richer 风格输出折叠成统一批注 suggestion 文本。"""
    summary = str(issue.get("suggestion") or issue.get("overallSuggestion") or "").strip()
    rewrite_version = str(issue.get("rewriteVersion") or "").strip()
    raw_adjustments = issue.get("structureAdjustments", [])
    if isinstance(raw_adjustments, str):
        raw_adjustments = [raw_adjustments]
    elif not isinstance(raw_adjustments, list):
        raw_adjustments = []
    adjustments = [str(item).strip() for item in raw_adjustments if str(item).strip()]
    raw_issue_items = issue.get("issueItems", [])
    if not isinstance(raw_issue_items, list):
        raw_issue_items = []
    issue_items = []
    for item in raw_issue_items:
        if not isinstance(item, dict):
            continue
        problem = str(item.get("problem") or "").strip()
        if problem:
            issue_items.append(problem)

    parts: List[str] = []
    if summary:
        parts.append(summary)
    if issue_items:
        parts.append("问题")
        parts.append("；".join(issue_items[:8]))
    if rewrite_version:
        parts.append("改写版本")
        parts.append(rewrite_version)
    if adjustments:
        parts.append("结构调整")
        parts.append("；".join(adjustments[:4]))
    return "\n".join(parts).strip()
