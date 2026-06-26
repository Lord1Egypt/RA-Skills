#!/usr/bin/env python3
"""Render Markdown and HTML MBTI reports from structured analysis results."""

from __future__ import annotations

import argparse
import base64
import json
import html
from pathlib import Path
from string import Template
from typing import Dict, List
from urllib.parse import quote_plus

from mbti_common import (
    AXIS_SIDES,
    TYPE_FUNCTIONS,
    detect_language_mix,
    family_for_type,
    family_label,
    iso_now,
    load_json,
    process_roles,
    resolve_path,
    theme_for_type,
    type_label,
    visible_function_order,
)


DEBUG_AXIS_SUPPORT = {
    "E": "Repeated outward processing, collaborative framing, and discussion-driven momentum.",
    "I": "Repeated inward processing, reflective pacing, and self-contained consolidation before expression.",
    "S": "Repeated attention to concrete execution, practical details, and proven anchors.",
    "N": "Repeated movement toward frameworks, patterns, abstraction, and future possibilities.",
    "T": "Repeated reliance on logic checks, contradiction spotting, and tradeoff language.",
    "F": "Repeated reliance on values, meaning, interpersonal impact, and relational interpretation.",
    "J": "Repeated push toward closure, explicit next steps, and external structure.",
    "P": "Repeated preference for optionality, exploration, iterative narrowing, and flexible pacing.",
}

DEBUG_AXIS_COUNTER = {
    "E": "There are still moments of solitary or private processing before speaking.",
    "I": "There are still moments of collaborative energy when shared problem-solving matters.",
    "S": "There are still moments of abstraction and long-range framing.",
    "N": "There are still moments of detail anchoring when execution demands it.",
    "T": "There are still moments where meaning and human consequences shape the call.",
    "F": "There are still moments where logic and impersonal structure take priority.",
    "J": "There are still moments where optionality is kept open to learn before committing.",
    "P": "There are still moments where closure and explicit sequencing are used to ship.",
}

DEBUG_BEHAVIOR_TEMPLATES = {
    "I": {
        "behavior_tag": "reflective-solitude",
        "summary": "The user often forms a view privately before moving into discussion.",
        "excerpt": "让我先自己想一会，把逻辑链顺一下，再给结论。",
        "function": "Ti",
    },
    "E": {
        "behavior_tag": "collaborative-energy",
        "summary": "The user often sharpens ideas through live discussion and visible iteration.",
        "excerpt": "我们先把几个方向抛出来，一边聊一边收敛。",
        "function": "Ne",
    },
    "S": {
        "behavior_tag": "specific-execution",
        "summary": "The user repeatedly grounds discussion in concrete steps, constraints, and implementation details.",
        "excerpt": "别先讲抽象结论，先把具体步骤、依赖和边界列出来。",
        "function": "Si",
    },
    "N": {
        "behavior_tag": "abstract-patterning",
        "summary": "The user repeatedly prefers frameworks, deeper structure, and pattern-level framing.",
        "excerpt": "我更想先搭框架，看模式和演化方向，再回到实现。",
        "function": "Ni",
    },
    "T": {
        "behavior_tag": "logic-optimization",
        "summary": "The user repeatedly evaluates options through coherence, logic, and system efficiency.",
        "excerpt": "这个方案逻辑上说不通，收益和代价也不成比例。",
        "function": "Te",
    },
    "F": {
        "behavior_tag": "values-and-meaning",
        "summary": "The user repeatedly checks whether a decision preserves meaning and human impact.",
        "excerpt": "如果这个做法会伤到人，哪怕效率高也不一定值得。",
        "function": "Fi",
    },
    "J": {
        "behavior_tag": "closure-and-plan",
        "summary": "The user often pushes for closure, sequence, and a concrete next-step path.",
        "excerpt": "先把结论敲定，再把行动项和截止时间排出来。",
        "function": "Te",
    },
    "P": {
        "behavior_tag": "exploration-drive",
        "summary": "The user often keeps multiple live options until more evidence shows up.",
        "excerpt": "先别太早定死，我想同时开几个方向边试边收敛。",
        "function": "Ne",
    },
}

DEBUG_FAMILY_STRENGTHS = {
    "nt": [
        ("Conceptual leverage", "The report surface emphasizes abstraction, model-building, and compressing complexity into clearer structures."),
        ("System pressure testing", "The narrative repeatedly rewards contradiction spotting and structural quality over smooth but weak reasoning."),
        ("Strategic range", "The page copy assumes a reader who naturally scans for direction, leverage, and second-order effects."),
    ],
    "nf": [
        ("Meaning sensitivity", "The report surface emphasizes interpretation, coherence of values, and what a direction means rather than only what it achieves."),
        ("Patterned empathy", "The narrative gives room for people-impact, motives, and alignment instead of flattening everything into efficiency."),
        ("Integrative framing", "The page copy assumes a reader who wants a whole-picture synthesis rather than isolated tactical fragments."),
    ],
    "st": [
        ("Operational realism", "The report surface emphasizes grounded action, direct constraints, and what can be executed without romanticizing complexity."),
        ("Concrete judgment", "The narrative gives more weight to evidence that reflects practical steps, detail fidelity, and reliability."),
        ("Steady delivery", "The page copy assumes a reader who values clarity, sequence, and observable results."),
    ],
    "sf": [
        ("Practical care", "The report surface emphasizes useful support, steadiness, and concrete forms of responsiveness."),
        ("Relational continuity", "The narrative gives room for harmony, impact on others, and preserving workable trust."),
        ("Grounded warmth", "The page copy assumes a reader who stays close to what is humanly immediate and actionable."),
    ],
}

PERSON_SEARCH_BASE_URL = "https://www.google.com/search?q="

DEBUG_FAMILY_BLINDSPOTS = {
    "nt": [
        ("Underweighting social texture", "A highly structural reading can miss quieter emotional constraints that still shape whether a plan will hold."),
        ("Premature abstraction", "The cleanest model can arrive before the real-world edges have been fully exposed."),
    ],
    "nf": [
        ("Overprotecting alignment", "A strong concern for meaning and resonance can delay necessary friction or sharper pruning."),
        ("Interpreting before verifying", "Deep motive-reading can outrun the concrete evidence if not checked against specifics."),
    ],
    "st": [
        ("Local optimization", "A strong practical lens can overfit to current constraints and miss strategic or symbolic shifts."),
        ("Underplaying possibility", "Speed and clarity in execution can narrow the set of options too early."),
    ],
    "sf": [
        ("Carrying too much relational load", "A steady support style can absorb tension that would be healthier to surface directly."),
        ("Deferring hard edges", "Practical care can sometimes soften calls that need firmer boundaries."),
    ],
}

TYPE_LABELS_ZH = {
    "INTJ": "系统战略家",
    "INTP": "模型构建者",
    "ENTJ": "指挥型架构师",
    "ENTP": "模式探索者",
    "INFJ": "洞察引路人",
    "INFP": "内在理想主义者",
    "ENFJ": "社会催化者",
    "ENFP": "可能性点火者",
    "ISTJ": "可靠执行者",
    "ISFJ": "稳健守护者",
    "ESTJ": "推进型执行者",
    "ESFJ": "群体维系者",
    "ISTP": "实用诊断者",
    "ISFP": "安静匠人",
    "ESTP": "机动操作者",
    "ESFP": "表达型连接者",
}

FAMILY_LABELS_ZH = {
    "nt": "理性分析型",
    "nf": "理想洞察型",
    "st": "务实执行型",
    "sf": "关怀支持型",
}

SIDE_LABELS = {
    "en": {
        "E": "Extraversion",
        "I": "Introversion",
        "S": "Sensing",
        "N": "Intuition",
        "T": "Thinking",
        "F": "Feeling",
        "J": "Judging",
        "P": "Perceiving",
    },
    "zh": {
        "E": "外倾",
        "I": "内倾",
        "S": "感觉",
        "N": "直觉",
        "T": "思考",
        "F": "情感",
        "J": "判断",
        "P": "感知",
    },
}

AXIS_LABELS = {
    "en": {
        "E/I": "Energy Direction",
        "S/N": "Information Focus",
        "T/F": "Decision Lens",
        "J/P": "Outer-world Pace",
    },
    "zh": {
        "E/I": "能量方向",
        "S/N": "信息关注点",
        "T/F": "决策视角",
        "J/P": "外部推进节奏",
    },
}

SIDE_STYLE_PHRASES = {
    "en": {
        "E": "developing clarity by talking things through in real time",
        "I": "processing privately before making the conclusion public",
        "S": "staying close to concrete detail and implementation reality",
        "N": "leading with patterns, abstraction, and conceptual links",
        "T": "checking logic, coherence, and tradeoffs before agreeing",
        "F": "keeping meaning, values, and human impact in view",
        "J": "closing loops early and creating visible structure",
        "P": "keeping options open until the picture becomes clearer",
    },
    "zh": {
        "E": "通过实时讨论把判断逐步推清楚",
        "I": "先在内部想透，再把结论拿到外部",
        "S": "紧贴具体细节、约束和落地现实",
        "N": "优先从模式、抽象和概念连接入手",
        "T": "先检查逻辑、自洽性和取舍是否成立",
        "F": "把意义、价值和对人的影响持续放在视野里",
        "J": "倾向于尽早收束并建立可见结构",
        "P": "在图景没有清晰前先保留更多选项",
    },
}

PRESSURE_COPY_ZH = {
    "I": "在压力下，你可能会把判断握得太久，直到已经形成很强结论后才愿意说出来。",
    "E": "在压力下，你可能会过早把思考外化，导致较安静但重要的信号被压过去。",
    "S": "在压力下，你可能会过度锚定已验证的做法，而低估新路径的价值。",
    "N": "在压力下，你可能会过度依赖模式判断，跳过本该先核实的现实约束。",
    "T": "在压力下，你的清晰和纠错能力可能会被他人感受到为过硬、过快或过于直接。",
    "F": "在压力下，你可能会为了维持关系和意义感，而推迟必要的摩擦与明确表态。",
    "J": "在压力下，你可能会为了推进而过早定案，压缩了继续校验的空间。",
    "P": "在压力下，你可能会把探索期拉得过长，让真正需要承诺的节点继续后移。",
}

CARD_TITLE_ZH = {
    "Conceptual leverage": "概念压缩力",
    "System pressure testing": "系统承压检验",
    "Strategic range": "战略视距",
    "Meaning sensitivity": "意义敏感度",
    "Patterned empathy": "模式化共情",
    "Narrative coherence": "叙事整合度",
    "Integrative framing": "整体整合视角",
    "Operational reliability": "执行可靠性",
    "Operational realism": "现实执行感",
    "Concrete problem solving": "具体问题拆解力",
    "Concrete judgment": "具体判断力",
    "Stability under load": "压力下的稳态",
    "Steady delivery": "稳定交付感",
    "Practical care": "务实照顾力",
    "Interpersonal steadiness": "关系稳态",
    "Relational continuity": "关系连续性",
    "Grounded responsiveness": "贴地响应力",
    "Grounded warmth": "有落点的温度感",
    "Underweighting emotional context": "低估情绪语境",
    "Premature abstraction": "抽象过早",
    "Overprotecting alignment": "过度维护一致性",
    "Narrative overreach": "叙事推断过度",
    "Constraint lock-in": "被既有约束锁定",
    "Local optimization bias": "局部最优偏置",
    "Harmony drag": "和谐拖拽",
    "Soft conflict handling": "冲突处理偏软",
    "Underweighting social texture": "低估社交纹理",
    "Interpreting before verifying": "先解释后验证",
    "Carrying too much relational load": "承担过多关系负荷",
    "Deferring hard edges": "延后必要的硬边界",
    "Preference overreach": "偏好过度外推",
}

CARD_BODY_ZH = {
    "Conceptual leverage": "你会自然地把复杂材料压缩成更清晰的结构、模型和讨论框架，而不是停留在杂乱表面。",
    "System pressure testing": "你通常会主动检查逻辑漏洞、薄弱假设和结构性风险，而不是让它们在推进中悄悄积累。",
    "Strategic range": "你的判断经常会越过眼前局部，去看更远的方向、杠杆点和第二层影响。",
    "Meaning sensitivity": "你不只看事情能不能做成，也会持续感受到它是否值得、是否对齐更深层的意义。",
    "Patterned empathy": "你倾向于把人的反应、关系变化和更深的动机结构联系起来理解。",
    "Narrative coherence": "你会把人、目标、价值和方向编织成一个整体图景，而不是只处理零散片段。",
    "Integrative framing": "你擅长把多个维度收拢进一个整体解释框架里，让复杂局面更容易被理解。",
    "Operational reliability": "你很容易回到可执行、可验证、可维护的路径上，不会只停留在好听的设想。",
    "Operational realism": "你会优先把判断落在现实边界、实际成本和能否做成上。",
    "Concrete problem solving": "你擅长把问题拆到可操作层，迅速抓住细节、约束和执行挂钩点。",
    "Concrete judgment": "你做判断时会先抓住具体事实和局部差异，而不是急着跳到大而空的结论。",
    "Stability under load": "在压力或不确定情境下，你仍倾向于让判断停留在可观察、可确认的层面。",
    "Steady delivery": "你会自然地把节奏拉回到能持续推进、能被交付的那条线上。",
    "Practical care": "你对人的关注往往不是抽象同情，而是会转成具体、有用、可接住的动作。",
    "Interpersonal steadiness": "你能够维持关系和协作的连续性，让周围人更容易在你的节奏里稳定下来。",
    "Relational continuity": "你会自发维护关系中的连贯性、信任和彼此可预期性。",
    "Grounded responsiveness": "你会对眼前真实发生的人和事保持及时、贴地的响应，而不是只停在理念层。",
    "Grounded warmth": "你的善意通常带着明确落点，能让人感到被具体地理解和照顾。",
    "Underweighting emotional context": "当你把注意力压到结构和逻辑上时，较柔软的人际信号很容易被你放到次要位置。",
    "Premature abstraction": "你可能会在现实边界尚未完全暴露前，就已经进入更干净的模型和结论。",
    "Overprotecting alignment": "当你过度维护价值一致或关系顺滑时，必要的摩擦可能会被延后。",
    "Narrative overreach": "你对模式和意义的感知可能会跑在事实核验前面，导致解释速度快过证据。",
    "Constraint lock-in": "已经被证明有效的做法可能会占据太多注意力，让高潜力的新方案没有足够空间。",
    "Local optimization bias": "当执行和现实约束成为主导时，更大的方向感或象征意义可能被压缩得过小。",
    "Harmony drag": "你为了维持稳定和善意，可能会让该明确划线的地方拖得稍久。",
    "Soft conflict handling": "你可能更擅长软化矛盾，而不是在必要时快速把硬分歧说透。",
    "Underweighting social texture": "当结构分析太强时，关系中的细密氛围和情绪温度可能会被低估。",
    "Interpreting before verifying": "你可能会先形成带解释力的图景，再回头补证据，这一步有时会过快。",
    "Carrying too much relational load": "你可能会在关系里默默承担过多稳定器角色，导致自己的负荷被低估。",
    "Deferring hard edges": "你可能会把该早点说清楚的边界往后放，导致后续成本更高。",
    "Preference overreach": "这份报告里最强的偏好如果被你默认适用于所有情境，就可能反过来压扁本来需要另一种模式的场景。",
}

REPORT_TEXT = {
    "en": {
        "html_lang": "en",
        "page_title": "MBTI Report · {type_code}",
        "toolbar_title": "{type_code} · {type_label}",
        "toolbar_subtitle": "Evidence-aware report",
        "jump_label": "Jump to",
        "nav_profile": "Profile",
        "nav_narrative": "Narrative",
        "nav_functions": "Functions",
        "nav_strengths": "Strengths",
        "nav_people": "Similar People",
        "nav_pressure": "Pressure",
        "nav_evidence": "Evidence",
        "nav_adjacent": "Adjacent Types",
        "nav_uncertainty": "Uncertainty",
        "download_html": "Download HTML",
        "export_pdf": "Export PDF",
        "share": "Share",
        "copied": "Copied",
        "section_profile": "Preference Profile",
        "section_narrative": "Type Narrative",
        "section_functions": "Function Validation",
        "section_strengths": "Strengths",
        "section_blindspots": "Blind Spots",
        "section_people": "People With {type_code}",
        "section_pressure": "Pressure and Decision Style",
        "section_evidence": "Evidence Chain",
        "section_adjacent": "Why Not The Adjacent Type",
        "section_uncertainty": "Uncertainty and Follow-Up",
        "section_current_state": "Current State",
        "selected_preference": "Selected Preference",
        "confidence": "Confidence",
        "support_signals": "Report signals",
        "counter_pattern": "Counter-pattern",
        "no_support": "No clear support extracted from the current evidence set.",
        "no_counter": "No strong opposing pattern surfaced in the current evidence set.",
        "current_best_fit": "Current best fit",
        "function_stack": "Visible function order",
        "strongest_signals": "Strongest visible signals",
        "outer_process": "Outer process",
        "dominant_process": "Dominant process",
        "auxiliary_process": "Auxiliary process",
        "supporting_process": "Supporting process",
        "lower_process": "Lower process",
        "share_summary": "{type_code} · {type_label}. {snapshot}",
        "footer_note": "Best-fit hypothesis generated from authorized evidence. This is a personality preference model, not a clinical assessment.",
        "not_used_for_inference": "Not used for inference",
        "no_adjacent": "No nearby alternative stayed competitive after the current evidence was scored.",
        "no_uncertainty": "No major unresolved axis stood out after evidence pooling.",
        "followup_prompt": "If you want to refine the result, the best next question is:",
        "source_reference": "Source reference",
        "hero_people_link": "See Similar Types →",
        "person_detail_link": "↗",
    },
    "zh": {
        "html_lang": "zh-CN",
        "page_title": "MBTI 报告 · {type_code}",
        "toolbar_title": "{type_code} · {type_label}",
        "toolbar_subtitle": "基于证据的类型报告",
        "jump_label": "快速跳转",
        "nav_profile": "偏好画像",
        "nav_narrative": "类型叙事",
        "nav_functions": "功能验证",
        "nav_strengths": "优势与盲区",
        "nav_people": "同型名人",
        "nav_pressure": "压力表现",
        "nav_evidence": "证据链",
        "nav_adjacent": "相邻类型",
        "nav_uncertainty": "不确定项",
        "download_html": "下载 HTML",
        "export_pdf": "导出 PDF",
        "share": "分享",
        "copied": "已复制",
        "section_profile": "偏好画像",
        "section_narrative": "类型叙事",
        "section_functions": "功能验证",
        "section_strengths": "优势",
        "section_blindspots": "盲区",
        "section_people": "{type_code} 同型名人",
        "section_pressure": "压力与决策风格",
        "section_evidence": "证据链",
        "section_adjacent": "为什么不是相邻类型",
        "section_uncertainty": "不确定项与追问",
        "section_current_state": "当前状态",
        "selected_preference": "当前偏好",
        "confidence": "置信度",
        "support_signals": "支持信号",
        "counter_pattern": "反向模式",
        "no_support": "当前证据里还没有抽出明确支持信号。",
        "no_counter": "当前证据里没有出现强反向模式。",
        "current_best_fit": "当前最佳匹配",
        "function_stack": "可见功能顺序",
        "strongest_signals": "最强可见信号",
        "outer_process": "外显过程",
        "dominant_process": "主导过程",
        "auxiliary_process": "辅助过程",
        "supporting_process": "支撑过程",
        "lower_process": "较弱过程",
        "share_summary": "{type_code} · {type_label}。{snapshot}",
        "footer_note": "这是基于授权证据生成的最佳匹配假设，用于偏好建模，不属于临床评估。",
        "not_used_for_inference": "未参与推断",
        "no_adjacent": "按当前证据评分，没有其他邻近类型保持足够接近的竞争度。",
        "no_uncertainty": "目前没有哪条轴向在证据汇总后仍明显悬而未决。",
        "followup_prompt": "如果要继续收敛结果，最值得追问的问题是：",
        "source_reference": "来源引用",
        "hero_people_link": "查看同型名人 →",
        "person_detail_link": "↗",
    },
}
def report_text(locale: str, key: str, **kwargs: str) -> str:
    template = REPORT_TEXT[locale][key]
    return template.format(**kwargs) if kwargs else template


def localize_type_label(type_code: str, locale: str) -> str:
    if locale == "zh":
        return TYPE_LABELS_ZH.get(type_code, type_label(type_code))
    return type_label(type_code)


def localize_family_label(type_code: str, locale: str) -> str:
    family_key = family_for_type(type_code)
    if locale == "zh":
        return FAMILY_LABELS_ZH.get(family_key, family_label(type_code))
    return family_label(type_code)


def localize_overall_confidence(overall_confidence: Dict, locale: str) -> str:
    if locale == "en":
        return overall_confidence.get("label", "Confidence unavailable")
    score = float(overall_confidence.get("score", 0.0))
    if score >= 0.78:
        return "高置信度"
    if score >= 0.58:
        return "中等置信度"
    return "低置信度"


def localize_axis_confidence(confidence: str, locale: str) -> str:
    if locale == "en":
        return confidence.capitalize()
    return {"high": "高", "medium": "中", "low": "低"}.get(confidence, confidence)


def side_label(side: str, locale: str) -> str:
    return SIDE_LABELS[locale].get(side, side)


def axis_label(axis: str, locale: str) -> str:
    return AXIS_LABELS[locale].get(axis, axis)


def paragraphs(value: str | List[str]) -> List[str]:
    if isinstance(value, list):
        return [item for item in value if item]
    return [value] if value else []


def card_html(
    title: str,
    body: str | List[str],
    quote: str | None = None,
    source_ref: str | None = None,
    eyebrow: str | None = None,
    extra_class: str = "",
) -> str:
    classes = "stack-item" if not extra_class else f"stack-item {extra_class}"
    parts = [f'<article class="{html.escape(classes)}">']
    if eyebrow:
        parts.append(f'<p class="card-eyebrow">{html.escape(eyebrow)}</p>')
    parts.append(f"<h3>{html.escape(title)}</h3>")
    for item in paragraphs(body):
        parts.append(f"<p>{html.escape(item)}</p>")
    if quote:
        parts.append(f'<p class="quote">{html.escape(quote)}</p>')
    if source_ref:
        parts.append(f'<p class="source-ref">{html.escape(source_ref)}</p>')
    parts.append("</article>")
    return "".join(parts)


def infer_report_language(analysis: Dict, evidence_pool: Dict, requested: str = "auto") -> str:
    if requested in {"en", "zh"}:
        return requested

    weights = {"en": 0, "zh": 0}
    samples: List[str] = []
    for payload in (analysis.get("source_summary"), evidence_pool.get("source_summary")):
        if not isinstance(payload, dict):
            continue
        for source in payload.get("sources", {}).values():
            count = max(1, int(source.get("record_count", 0) or 0))
            mix = source.get("language_mix")
            if mix == "zh":
                weights["zh"] += count * 3
            elif mix == "en":
                weights["en"] += count * 3
            elif mix == "mixed":
                weights["zh"] += count
                weights["en"] += count
            samples.extend(source.get("sample_preview", []))

    if not samples:
        for item in evidence_pool.get("evidence_pool", [])[:8]:
            samples.extend([item.get("summary", ""), item.get("excerpt", "")])

    combined = " ".join(sample for sample in samples if sample)
    mix = detect_language_mix(combined)
    zh_chars = sum(1 for ch in combined if "\u4e00" <= ch <= "\u9fff")
    latin_letters = sum(1 for ch in combined if ch.isascii() and ch.isalpha())

    if mix == "zh":
        weights["zh"] += 4
    elif mix == "en":
        weights["en"] += 4
    elif mix == "mixed":
        if zh_chars >= 6 and zh_chars * 2 >= max(1, latin_letters):
            weights["zh"] += 3
        else:
            weights["en"] += 2

    return "zh" if weights["zh"] > weights["en"] else "en"


def metric_option_html(side: str, pct: int, locale: str, is_selected: bool, is_weaker: bool = False) -> str:
    classes = ["metric-option"]
    if is_selected:
        classes.append("is-selected")
    if is_weaker:
        classes.append("is-weaker")
    class_name = " ".join(classes)
    return (
        f'<div class="{class_name}">'
        f'<span class="metric-option-code">{html.escape(side)}</span>'
        f'<div><strong>{html.escape(side_label(side, locale))}</strong>'
        f'<small>{pct}%</small></div>'
        "</div>"
    )


def metric_card(axis_result: Dict, locale: str) -> str:
    selected = axis_result["selected"]
    other = axis_result["right"] if selected == axis_result["left"] else axis_result["left"]
    support = "; ".join(axis_result["support_summary"]) if axis_result["support_summary"] else report_text(locale, "no_support")
    counter = "; ".join(axis_result["counter_summary"]) if axis_result["counter_summary"] else report_text(locale, "no_counter")
    selected_pct = axis_result["left_pct"] if selected == axis_result["left"] else axis_result["right_pct"]
    other_pct = axis_result["right_pct"] if selected == axis_result["left"] else axis_result["left_pct"]
    left_class = "meter-segment is-selected" if selected == axis_result["left"] else "meter-segment"
    right_class = "meter-segment is-selected" if selected == axis_result["right"] else "meter-segment"
    left_weaker = axis_result["left_pct"] < axis_result["right_pct"]
    return (
        '<article class="metric-card">'
        '<div class="metric-head">'
        "<div>"
        f"<h3>{html.escape(side_label(selected, locale))}</h3>"
        f'<p class="metric-meta">{html.escape(axis_label(axis_result["axis"], locale))} · '
        f'{html.escape(report_text(locale, "confidence"))}: {html.escape(localize_axis_confidence(axis_result["confidence"], locale))}</p>'
        "</div>"
        f'<div class="metric-badge">{html.escape(selected)}</div>'
        "</div>"
        '<div class="metric-options">'
        f'{metric_option_html(axis_result["left"], axis_result["left_pct"], locale, selected == axis_result["left"], left_weaker)}'
        f'{metric_option_html(axis_result["right"], axis_result["right_pct"], locale, selected == axis_result["right"], not left_weaker)}'
        "</div>"
        '<div class="meter meter-split">'
        f'<span class="{left_class}" style="width:{axis_result["left_pct"]}%"></span>'
        f'<span class="{right_class}" style="width:{axis_result["right_pct"]}%"></span>'
        "</div>"
        '<div class="metric-notes">'
        f'<div class="note-block"><p class="note-label">{html.escape(report_text(locale, "support_signals"))}</p><p>{html.escape(support)}</p></div>'
        f'<div class="note-block is-muted"><p class="note-label">{html.escape(report_text(locale, "counter_pattern"))}</p><p>{html.escape(counter)}</p></div>'
        "</div>"
        "</article>"
    )


def enhance_badge_svg(badge_path: Path, type_code: str) -> str:
    svg = badge_path.read_text(encoding="utf-8")
    insert = (
        '<text x="160" y="182" text-anchor="middle" '
        'font-family="Georgia, serif" font-size="56" font-weight="700" fill="#111827">'
        f"{html.escape(type_code)}"
        "</text>"
    )
    return svg.replace("</svg>", insert + "</svg>")


def build_hero_badge(asset_dir: Path, type_code: str, theme_key: str) -> str:
    """Return an <img> tag with base64-encoded type image, or fall back to SVG badge."""
    type_lower = type_code.lower()
    for ext in ("png", "jpeg", "jpg", "webp"):
        img_path = asset_dir / "images" / f"{type_lower}.{ext}"
        if img_path.is_file():
            data = img_path.read_bytes()
            mime = "image/png" if ext == "png" else "image/jpeg"
            b64 = base64.b64encode(data).decode("ascii")
            return (
                f'<img src="data:{mime};base64,{b64}" '
                f'alt="{html.escape(type_code)}" class="hero-image" />'
            )
    return enhance_badge_svg(asset_dir / "type-badges" / f"{theme_key}.svg", type_code)


def evidence_lookup(evidence_pool: List[Dict]) -> Dict[str, Dict]:
    return {item["evidence_id"]: item for item in evidence_pool}


def source_ref_text(source_ref: Dict) -> str:
    primary = source_ref["primary"]
    return f'{primary["source_type"]} · {primary["location"]}'


def normalize_person_key(name: str) -> str:
    base = name.split("(", 1)[0].strip().lower()
    return "".join(char for char in base if char.isalnum())


def build_person_search_url(person: Dict, fallback_type: str) -> str:
    query_parts = [
        person.get("name", "").strip(),
        (person.get("mbti_type") or fallback_type).strip(),
    ]
    query = " ".join(part for part in query_parts if part)
    if not query:
        return ""
    return f"{PERSON_SEARCH_BASE_URL}{quote_plus(query)}"


def load_famous_people(type_code: str) -> List[Dict]:
    data_path = Path(__file__).resolve().parent.parent / "references" / "famous_people.json"
    data = load_json(data_path)
    unique: List[Dict] = []
    seen = set()
    people = sorted(data.get(type_code, []), key=lambda item: 0 if item.get("source") == "curated" else 1)
    for person in people:
        name = person.get("name", "").strip()
        key = normalize_person_key(name)
        if not name or not key or key in seen:
            continue
        seen.add(key)
        prepared = dict(person)
        prepared["detail_url"] = build_person_search_url(prepared, type_code)
        unique.append(prepared)
        if len(unique) == 6:
            break
    return unique


def localize_card_title(title: str, locale: str) -> str:
    if locale == "zh":
        return CARD_TITLE_ZH.get(title, title)
    return title


def localize_card_body(title: str, body: str, locale: str) -> str:
    if locale == "zh":
        return CARD_BODY_ZH.get(title, body)
    return body


def flip_type_letter(type_code: str, index: int) -> str:
    pairs = {"E": "I", "I": "E", "S": "N", "N": "S", "T": "F", "F": "T", "J": "P", "P": "J"}
    letters = list(type_code)
    letters[index] = pairs[letters[index]]
    return "".join(letters)


def build_debug_dimension_results(type_code: str) -> Dict[str, Dict]:
    selected_strengths = [76, 72, 74, 64]
    confidence_levels = ["high", "high", "high", "medium"]
    results: Dict[str, Dict] = {}
    for index, ((axis, left, right), pct, confidence) in enumerate(zip(AXIS_SIDES, selected_strengths, confidence_levels)):
        selected = type_code[index]
        if selected == left:
            left_pct = pct
            right_pct = 100 - pct
        else:
            right_pct = pct
            left_pct = 100 - pct
        results[axis] = {
            "axis": axis,
            "left": left,
            "right": right,
            "selected": selected,
            "left_pct": left_pct,
            "right_pct": right_pct,
            "margin": round(abs(left_pct - right_pct) / 100, 3),
            "confidence": confidence,
            "support_summary": [DEBUG_AXIS_SUPPORT[selected]],
            "counter_summary": [DEBUG_AXIS_COUNTER[selected]],
        }
    return results


def build_debug_evidence_pool(type_code: str) -> Dict:
    evidence_items = []
    for index, letter in enumerate(type_code, start=1):
        template = DEBUG_BEHAVIOR_TEMPLATES[letter]
        evidence_items.append(
            {
                "evidence_id": f"debug-{index}",
                "summary": template["summary"],
                "excerpt": template["excerpt"],
                "source_ref": {
                    "primary": {
                        "source_type": "debug-preview",
                        "location": f"fixture:{index}",
                    },
                    "alternatives": [],
                },
                "behavior_tag": template["behavior_tag"],
                "dimension_hints": [{"axis": AXIS_SIDES[index - 1][0], "side": letter}],
                "function_hints": [{"function": template["function"], "weight": 1.0}],
                "strength": "strong" if index <= 3 else "moderate",
                "confidence": "high" if index <= 3 else "medium",
                "independence_score": 0.95 if index <= 2 else 0.82,
                "is_counterevidence": False,
                "is_pseudosignal": False,
                "notes": "Bundled fixture used for report-layout preview.",
            }
        )

    evidence_items.append(
        {
            "evidence_id": "debug-counter-1",
            "summary": "The user still shows some outward collaboration when alignment or speed matters.",
            "excerpt": "这个问题我们还是一起过一遍，边聊边发现盲点会更快。",
            "source_ref": {
                "primary": {
                    "source_type": "debug-preview",
                    "location": "fixture:counter-1",
                },
                "alternatives": [],
            },
            "behavior_tag": "counterevidence-collaboration",
            "dimension_hints": [{"axis": "E/I", "side": flip_type_letter(type_code, 0)[0]}],
            "function_hints": [{"function": "Fe", "weight": 0.6}],
            "strength": "weak",
            "confidence": "medium",
            "independence_score": 0.66,
            "is_counterevidence": True,
            "is_pseudosignal": False,
            "notes": "Counter-pattern included so the preview shows non-one-sided evidence.",
        }
    )

    evidence_items.append(
        {
            "evidence_id": "debug-counter-2",
            "summary": "The user still knows how to force closure when delivery pressure gets real.",
            "excerpt": "别再扩了，今天先定一个版本发出去，后面再迭代。",
            "source_ref": {
                "primary": {
                    "source_type": "debug-preview",
                    "location": "fixture:counter-2",
                },
                "alternatives": [],
            },
            "behavior_tag": "counterevidence-closure",
            "dimension_hints": [{"axis": "J/P", "side": flip_type_letter(type_code, 3)[3]}],
            "function_hints": [{"function": "Te", "weight": 0.6}],
            "strength": "weak",
            "confidence": "medium",
            "independence_score": 0.64,
            "is_counterevidence": True,
            "is_pseudosignal": False,
            "notes": "Counter-pattern included so the preview exercises the adjacent-type section.",
        }
    )

    return {
        "generated_at": iso_now(),
        "mode": "debug-preview",
        "evidence_pool": evidence_items,
    }


def build_debug_analysis(type_code: str) -> Dict:
    family_key = family_for_type(type_code)
    stack = " -> ".join(TYPE_FUNCTIONS[type_code])
    roles = process_roles(type_code)
    visible_order = visible_function_order(type_code)
    dimension_results = build_debug_dimension_results(type_code)
    adjacent_one = flip_type_letter(type_code, 3)
    adjacent_two = flip_type_letter(type_code, 0)

    strengths = [{"title": title, "body": body} for title, body in DEBUG_FAMILY_STRENGTHS[family_key]]
    blindspots = [{"title": title, "body": body} for title, body in DEBUG_FAMILY_BLINDSPOTS[family_key]]

    pressure_patterns = [
        {
            "title": "Pressure response",
            "body": "This preview intentionally shows a type that can become narrower and sharper under load, especially when weak assumptions need to be cut quickly.",
        },
        {
            "title": "Decision style",
            "body": "The fixture emphasizes a reader who wants strong reasoning, visible tradeoffs, and a clear sense of why one interpretation outranks nearby alternatives.",
        },
    ]

    adjacent = [
        {
            "title": f"Why not {adjacent_one}",
            "body": f"The preview keeps {type_code} ahead of {adjacent_one} because the evidence mix favors {type_code[3]} over {adjacent_one[3]} on closure versus optionality, even though both remain plausible neighbors.",
        },
        {
            "title": f"Why not {adjacent_two}",
            "body": f"The preview keeps {type_code} ahead of {adjacent_two} because the evidence mix favors {type_code[0]} over {adjacent_two[0]} on inward versus outward processing, while still leaving some live counterevidence.",
        },
    ]

    uncertainties = [
        {
            "title": "Preview fixture bias",
            "body": "This standalone preview uses bundled mock evidence so layout work can proceed without rerunning extraction and inference.",
        },
        {
            "title": "Real-run calibration",
            "body": "In a real report, confidence, adjacent-type comparison, and evidence wording will tighten around the authorized source set rather than these canned examples.",
        },
    ]

    return {
        "generated_at": iso_now(),
        "mode": "debug-preview",
        "final_type": type_code,
        "type_label": type_label(type_code),
        "family_key": family_key,
        "family_label": family_label(type_code),
        "overall_confidence": {"score": 0.81, "label": "High confidence"},
        "snapshot": "A standalone report-preview fixture that exercises the full visual system without requiring collection, extraction, or inference to run first.",
        "type_narrative": f"This preview renders {type_code} as a best-fit hypothesis with a full report surface. It combines the expected preference pattern with enough counterevidence to exercise the uncertainty and adjacent-type sections instead of producing an unrealistically clean page.",
        "function_validation": {
            "dominant_function": roles["dominant_function"],
            "auxiliary_function": roles["auxiliary_function"],
            "outer_function": roles["outer_function"],
            "jp_reflects": roles["jp_reflects"],
            "visible_order": visible_order,
            "function_scores": {
                visible_order[0]: 4.9,
                visible_order[1]: 4.2,
                visible_order[2]: 2.1,
                visible_order[3]: 0.8,
            },
            "summary": f"The function-stack validation block is also populated in preview mode. For {type_code}, the template shows the stack {stack}, so typography, spacing, and prose density can be tuned without depending on upstream artifacts.",
        },
        "dimension_results": dimension_results,
        "strengths": strengths,
        "blindspots": blindspots,
        "pressure_patterns": pressure_patterns,
        "selected_evidence_ids": ["debug-1", "debug-2", "debug-3", "debug-4"],
        "adjacent_type_comparison": adjacent,
        "uncertainties": uncertainties,
        "followup_questions": [],
    }


def ordered_dimension_results(analysis: Dict) -> List[Dict]:
    ordered = []
    for axis, _, _ in AXIS_SIDES:
        if axis in analysis.get("dimension_results", {}):
            ordered.append(analysis["dimension_results"][axis])
    return ordered


def prose_html(items: List[str]) -> str:
    return "".join(f"<p>{html.escape(item)}</p>" for item in items if item)


def build_type_narrative_paragraphs(analysis: Dict, locale: str) -> List[str]:
    type_code = analysis["final_type"]
    type_name = localize_type_label(type_code, locale)
    family_name = localize_family_label(type_code, locale)
    ordered = ordered_dimension_results(analysis)
    if not ordered:
        return [analysis.get("snapshot", "")]

    ranked = sorted(ordered, key=lambda item: item.get("margin", 0.0), reverse=True)
    lead = ranked[:2]
    weakest = ranked[-1]
    lead_names = [side_label(item["selected"], locale) for item in lead]
    style_line = ", ".join(SIDE_STYLE_PHRASES[locale][letter] for letter in type_code) if locale == "en" else "、".join(
        SIDE_STYLE_PHRASES[locale][letter] for letter in type_code
    )
    first_axes = " and ".join(axis_label(item["axis"], locale) for item in lead) if locale == "en" else "和".join(
        axis_label(item["axis"], locale) for item in lead
    )

    if locale == "zh":
        return [
            f"当前最佳匹配类型是 {type_code}。最强的一组信号集中在{'、'.join(lead_names)}，它们一起更贴近“{type_name}”这条画像，而不是只落在单个孤立特征上。",
            f"四条偏好轴里，拉开最明显的是{first_axes}；相对最需要保留修正空间的是{axis_label(weakest['axis'], locale)}。这表示结论并不是绝对化判断，而是在当前证据下这组倾向最稳定。",
            f"落到实际互动里，这通常表现为：{style_line}。整体气质更接近{family_name}，当前报告给出的结论是{localize_overall_confidence(analysis['overall_confidence'], locale)}。",
        ]

    return [
        f"{type_code} is the current best-fit interpretation. The strongest signal cluster lands on {', '.join(lead_names)}, which together maps more cleanly to the {type_name} pattern than to a loose collection of unrelated traits.",
        f"Across the four axes, the clearest separation appears on {first_axes}. The least-separated axis is {axis_label(weakest['axis'], locale)}, so that is where revision pressure would most likely show up if new evidence lands.",
        f"In practice, this combination often reads as {style_line}. The overall tone of the report stays closest to the {family_name} family, with {localize_overall_confidence(analysis['overall_confidence'], locale).lower()} support from the current evidence chain.",
    ]


def function_role_label(function_name: str, validation: Dict, locale: str) -> str:
    if function_name == validation.get("outer_function"):
        return report_text(locale, "outer_process")
    if function_name == validation.get("dominant_function"):
        return report_text(locale, "dominant_process")
    if function_name == validation.get("auxiliary_function"):
        return report_text(locale, "auxiliary_process")
    visible_order = validation.get("visible_order", [])
    if function_name in visible_order and visible_order.index(function_name) == 2:
        return report_text(locale, "supporting_process")
    return report_text(locale, "lower_process")


def function_stack_html(validation: Dict, locale: str) -> str:
    visible_order = validation.get("visible_order", [])
    scores = validation.get("function_scores", {})
    ranked = sorted(visible_order[:4], key=lambda function_name: float(scores.get(function_name, 0.0)), reverse=True)
    strongest = set(ranked[:2])
    cards = []
    for function_name in visible_order[:4]:
        score = float(scores.get(function_name, 0.0))
        class_name = "function-pill is-strong" if function_name in strongest and score > 0 else "function-pill"
        cards.append(
            f'<article class="{class_name}">'
            f'<strong>{html.escape(function_name)}</strong>'
            f'<span>{html.escape(function_role_label(function_name, validation, locale))}</span>'
            f'<small>{score:.2f}</small>'
            "</article>"
        )
    return '<div class="function-stack">' + "".join(cards) + "</div>"


def build_function_validation_paragraphs(analysis: Dict, locale: str) -> List[str]:
    validation = analysis.get("function_validation", {})
    type_code = analysis["final_type"]
    visible_order = validation.get("visible_order", TYPE_FUNCTIONS.get(type_code, []))
    scores = validation.get("function_scores", {})
    ranked = sorted(
        ((function_name, float(scores.get(function_name, 0.0))) for function_name in visible_order[:4]),
        key=lambda item: item[1],
        reverse=True,
    )
    top_two = [item for item in ranked if item[1] > 0][:2] or ranked[:2]
    top_text = ", ".join(f"{function_name} ({score:.2f})" for function_name, score in top_two)
    visible_text = " -> ".join(visible_order[:4])
    jp_anchor = "辅助功能" if validation.get("jp_reflects") == "auxiliary" else "主导功能"

    if locale == "zh":
        return [
            f"对 {type_code} 来说，外部更容易先看见的是 {validation.get('outer_function', visible_order[0] if visible_order else '')}，更深层的内部锚点则是 {validation.get('dominant_function', visible_order[0] if visible_order else '')}。所以功能验证的任务，是检查证据是否与这条可见顺序同向，而不是越过四条偏好轴直接改判类型。",
            f"这次运行里，最强的可见信号集中在 {top_text}，而整条可见顺序是 {visible_text}。这说明外显过程和内在主导过程之间的组合关系基本站得住。",
            f"{type_code} 里的 J/P 字母反映的是{jp_anchor}在外部世界里的呈现方式，因此它更像外部节奏线索，而不是脱离上下文的单独性格标签。",
        ]

    jp_reflects = "auxiliary function" if validation.get("jp_reflects") == "auxiliary" else "dominant function"
    return [
        f"For {type_code}, the process most visible in outward behavior is {validation.get('outer_function', visible_order[0] if visible_order else '')}, while the deeper inner anchor is {validation.get('dominant_function', visible_order[0] if visible_order else '')}. Function validation therefore checks whether the evidence moves in the expected direction instead of overruling the four-axis result.",
        f"In this run, the strongest visible signals cluster around {top_text}, and the expected visible order is {visible_text}. That is directionally consistent with the stack rather than fighting it.",
        f"The J/P letter in {type_code} reflects the {jp_reflects} for this orientation, so it is best read as an outer-world style marker rather than a standalone trait slogan.",
    ]


def display_strength_items(analysis: Dict, locale: str) -> List[Dict]:
    supports = [
        summary
        for result in ordered_dimension_results(analysis)
        for summary in result.get("support_summary", [])[:1]
    ]
    items = analysis.get("strengths", [])
    display = []
    for index, item in enumerate(items):
        title = localize_card_title(item["title"], locale)
        body = localize_card_body(item["title"], item["body"], locale)
        anchor = supports[index % len(supports)] if supports else ""
        if locale == "zh":
            extra = f"这在当前报告里也能从证据链看出来，例如：{anchor}" if anchor else "这一点在当前证据链里呈现得比较稳定。"
        else:
            extra = f"In the current run, this is reinforced by evidence such as: {anchor}" if anchor else "That tendency stays directionally consistent across the current evidence chain."
        display.append({"title": title, "body": [body, extra]})
    return display


def display_blindspot_items(analysis: Dict, locale: str) -> List[Dict]:
    ranked = sorted(ordered_dimension_results(analysis), key=lambda item: item.get("margin", 0.0))
    items = list(analysis.get("blindspots", []))
    if len(items) < 3:
        items.append(
            {
                "title": "Preference overreach",
                "body": "The clearest preferences in this report may start looking universally correct, even in situations that would benefit from the opposite mode.",
            }
        )

    display = []
    for index, item in enumerate(items[:3]):
        axis_result = ranked[index % len(ranked)] if ranked else None
        title = localize_card_title(item["title"], locale)
        body = localize_card_body(item["title"], item["body"], locale)
        if axis_result:
            current_side = side_label(axis_result["selected"], locale)
            axis_name = axis_label(axis_result["axis"], locale)
            counter = "; ".join(axis_result.get("counter_summary", [])[:1])
            if locale == "zh":
                extra = f"这一类风险最容易出现在{axis_name}上：当“{current_side}”这一侧被用得太顺手时，另一侧的信息就更难及时进来。"
                if counter:
                    extra += f" 当前仍保留的一条反向线索是：{counter}"
            else:
                extra = f"The watch-out is usually {axis_name}: when the {current_side} side is overused, the opposite mode gets less room to register."
                if counter:
                    extra += f" A live counter-pattern still exists here: {counter}"
        else:
            extra = report_text(locale, "no_counter")
        display.append({"title": title, "body": [body, extra]})
    return display


def display_pressure_items(analysis: Dict, locale: str) -> List[Dict]:
    items = []
    for item in analysis.get("pressure_patterns", []):
        title = item["title"]
        body = item["body"]
        if len(title) == 1 and title in SIDE_LABELS["en"]:
            title = f"{side_label(title, locale)} ({title})"
            if locale == "zh":
                body = PRESSURE_COPY_ZH.get(item["title"], body)
        items.append({"title": title, "body": [body]})
    return items


def extract_type_code(text: str) -> str | None:
    for token in text.replace(":", " ").split():
        if len(token) == 4 and token.isalpha() and token.upper() == token:
            return token
    return None


def display_adjacent_items(analysis: Dict, locale: str) -> List[Dict]:
    final_type = analysis["final_type"]
    candidate_types = analysis.get("candidate_types", [])
    if len(candidate_types) > 1:
        items = []
        for candidate in candidate_types[1:3]:
            candidate_type = candidate["type"]
            if locale == "zh":
                title = f"为什么不是 {candidate_type}"
                body = [
                    f"{candidate_type} 之所以仍留在候选范围内，是因为部分证据仍向它靠拢。",
                    f"但在四条偏好轴和功能一致性一起计分后，{final_type} 仍保持领先。",
                ]
            else:
                title = f"Why not {candidate_type}"
                body = [
                    f"{candidate_type} stays in range because parts of the evidence still point in its direction.",
                    f"After the four preference axes and function coherence are considered together, {final_type} still keeps the lead.",
                ]
            items.append({"title": title, "body": body})
        return items

    comparisons = analysis.get("adjacent_type_comparison", [])
    if comparisons:
        if locale == "en":
            return [{"title": item["title"], "body": [item["body"]]} for item in comparisons]
        localized = []
        for item in comparisons:
            candidate_type = extract_type_code(item["title"]) or extract_type_code(item["body"]) or "候选类型"
            localized.append(
                {
                    "title": f"为什么不是 {candidate_type}",
                    "body": [
                        f"{candidate_type} 仍然保留了一部分相邻信号，所以它没有被完全排除。",
                        f"但当前证据在整体上仍更稳定地指向 {final_type}。",
                    ],
                }
            )
        return localized

    return [
        {
            "title": report_text(locale, "section_current_state"),
            "body": [report_text(locale, "no_adjacent")],
        }
    ]


def display_uncertainty_items(analysis: Dict, locale: str) -> List[Dict]:
    followup_items = analysis.get("followup_items", [])
    if followup_items:
        items = []
        for item in followup_items[:4]:
            support = item.get("support_summary") or report_text(locale, "no_support")
            counter = item.get("counter_summary") or report_text(locale, "no_counter")
            if locale == "zh":
                body = [
                    f"{axis_label(item['axis'], locale)} 这一轴目前分离度还不够稳。支持信号是：{support}",
                    f"反向模式仍在：{counter} {report_text(locale, 'followup_prompt')} {item['question']}",
                ]
            else:
                body = [
                    f"{axis_label(item['axis'], locale)} remains weakly separated. Support currently comes from: {support}",
                    f"The counter-pattern is still active: {counter} {report_text(locale, 'followup_prompt')} {item['question']}",
                ]
            items.append({"title": axis_label(item["axis"], locale), "body": body})
        return items

    low_axes = [item for item in ordered_dimension_results(analysis) if item.get("confidence") == "low"]
    if low_axes:
        items = []
        for axis_result in low_axes:
            counter = "; ".join(axis_result.get("counter_summary", [])[:1]) or report_text(locale, "no_counter")
            if locale == "zh":
                body = [
                    f"{axis_label(axis_result['axis'], locale)} 这一轴还没有和其他轴一样明显拉开。",
                    f"当前需要特别留意的反向线索是：{counter}",
                ]
            else:
                body = [
                    f"{axis_label(axis_result['axis'], locale)} is not separated as cleanly as the rest of the profile.",
                    f"The main live counter-pattern is: {counter}",
                ]
            items.append({"title": axis_label(axis_result["axis"], locale), "body": body})
        return items

    return [{"title": report_text(locale, "section_current_state"), "body": [report_text(locale, "no_uncertainty")]}]


def person_card_html(person: Dict, locale: str) -> str:
    title_html = html.escape(person["name"])
    if person.get("detail_url"):
        title_html = (
            f'<a href="{html.escape(person["detail_url"])}" target="_blank" rel="noreferrer">{title_html}</a>'
        )
    parts = ['<article class="person-card">']
    if person.get("detail_url"):
        parts.append(
            f'<a class="person-card-link" href="{html.escape(person["detail_url"])}" target="_blank" rel="noreferrer">'
            f'{html.escape(report_text(locale, "person_detail_link"))}'
            f'</a>'
        )
    if person.get("domain"):
        parts.append(f'<p class="card-eyebrow">{html.escape(person["domain"])}</p>')
    parts.append(f"<h3>{title_html}</h3>")
    if person.get("description"):
        parts.append(f'<p>{html.escape(person["description"])}</p>')
    parts.append(f'<p class="source-ref">{html.escape(report_text(locale, "not_used_for_inference"))}</p>')
    parts.append("</article>")
    return "".join(parts)


def build_nav_links(locale: str) -> str:
    entries = [
        ("#profile", report_text(locale, "nav_profile")),
        ("#people", report_text(locale, "nav_people")),
        ("#narrative", report_text(locale, "nav_narrative")),
        ("#functions", report_text(locale, "nav_functions")),
        ("#strengths", report_text(locale, "nav_strengths")),
        ("#pressure", report_text(locale, "nav_pressure")),
        ("#evidence", report_text(locale, "nav_evidence")),
        ("#adjacent", report_text(locale, "nav_adjacent")),
        ("#uncertainty", report_text(locale, "nav_uncertainty")),
    ]
    return "".join(
        f'<a class="sidebar-link" href="{html.escape(target)}">{html.escape(label)}</a>' for target, label in entries
    )


def render_markdown(analysis: Dict, evidence_pool: Dict, quote_mode: str, report_language: str = "auto") -> str:
    locale = infer_report_language(analysis, evidence_pool, report_language)
    lookup = evidence_lookup(evidence_pool["evidence_pool"])
    heading = f"# MBTI Report: {analysis['final_type']}" if locale == "en" else f"# MBTI 报告：{analysis['final_type']}"
    lines = [
        heading,
        "",
        f"- {'Label' if locale == 'en' else '标签'}: {localize_type_label(analysis['final_type'], locale)}",
        f"- {report_text(locale, 'confidence')}: {localize_overall_confidence(analysis['overall_confidence'], locale)}",
        f"- {'Family' if locale == 'en' else '气质家族'}: {localize_family_label(analysis['final_type'], locale)}",
        "",
        f"## {report_text(locale, 'section_narrative')}",
    ]
    lines.extend(build_type_narrative_paragraphs(analysis, locale))
    lines.extend(["", f"## {report_text(locale, 'section_profile')}"])
    for result in ordered_dimension_results(analysis):
        support = "; ".join(result.get("support_summary", [])) or report_text(locale, "no_support")
        counter = "; ".join(result.get("counter_summary", [])) or report_text(locale, "no_counter")
        lines.extend(
            [
                f"### {side_label(result['selected'], locale)} ({result['selected']})",
                f"- {report_text(locale, 'confidence')}: {localize_axis_confidence(result['confidence'], locale)}",
                f"- {report_text(locale, 'support_signals')}: {support}",
                f"- {report_text(locale, 'counter_pattern')}: {counter}",
                "",
            ]
        )

    lines.extend([f"## {report_text(locale, 'section_evidence')}"])
    for evidence_id in analysis["selected_evidence_ids"]:
        item = lookup[evidence_id]
        lines.append(f"- {item['summary']} [{source_ref_text(item['source_ref'])}]")
        if quote_mode == "summary":
            lines.append(f"  {'Quote' if locale == 'en' else '摘录'}: {item['excerpt']}")
    lines.extend(["", f"## {report_text(locale, 'section_people', type_code=analysis['final_type'])}"])
    for person in load_famous_people(analysis["final_type"]):
        lines.append(f"- {person['name']} ({person.get('domain', 'Other')}): {person.get('description', '')}")
    lines.extend(["", f"## {report_text(locale, 'section_adjacent')}"])
    for item in display_adjacent_items(analysis, locale):
        lines.append(f"- {item['title']}: {' '.join(item['body'])}")
    lines.extend(["", f"## {report_text(locale, 'section_uncertainty')}"])
    for item in display_uncertainty_items(analysis, locale):
        lines.append(f"- {item['title']}: {' '.join(item['body'])}")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_html(analysis: Dict, evidence_pool: Dict, quote_mode: str, asset_dir: Path, report_language: str = "auto") -> str:
    locale = infer_report_language(analysis, evidence_pool, report_language)
    template = Template((asset_dir / "report-template.html").read_text(encoding="utf-8"))
    embedded_css = (asset_dir / "report.css").read_text(encoding="utf-8")
    theme_key = theme_for_type(analysis["final_type"])
    badge_svg = build_hero_badge(asset_dir, analysis["final_type"], theme_key)
    lookup = evidence_lookup(evidence_pool["evidence_pool"])

    narrative_paragraphs = build_type_narrative_paragraphs(analysis, locale)
    function_paragraphs = build_function_validation_paragraphs(analysis, locale)
    function_validation = function_stack_html(analysis.get("function_validation", {}), locale) + prose_html(function_paragraphs)
    dimension_cards = "\n".join(metric_card(result, locale) for result in ordered_dimension_results(analysis))
    strengths = "\n".join(card_html(item["title"], item["body"]) for item in display_strength_items(analysis, locale))
    blindspots = "\n".join(card_html(item["title"], item["body"]) for item in display_blindspot_items(analysis, locale))
    pressure = "\n".join(card_html(item["title"], item["body"]) for item in display_pressure_items(analysis, locale))
    adjacent = "\n".join(card_html(item["title"], item["body"]) for item in display_adjacent_items(analysis, locale))
    uncertainty = "\n".join(card_html(item["title"], item["body"]) for item in display_uncertainty_items(analysis, locale))
    people_cards = "\n".join(person_card_html(person, locale) for person in load_famous_people(analysis["final_type"]))

    evidence_cards = []
    for evidence_id in analysis["selected_evidence_ids"]:
        item = lookup[evidence_id]
        quote = item["excerpt"] if quote_mode == "summary" else None
        evidence_cards.append(
            card_html(
                item["behavior_tag"].replace("-", " ").title(),
                item["summary"],
                quote=quote,
                source_ref=source_ref_text(item["source_ref"]),
                eyebrow=report_text(locale, "source_reference"),
            )
        )

    share_summary = report_text(
        locale,
        "share_summary",
        type_code=analysis["final_type"],
        type_label=localize_type_label(analysis["final_type"], locale),
        snapshot=narrative_paragraphs[0],
    )
    action_payload = json.dumps(
        {
            "fileBase": f"mbti-report-{analysis['final_type'].lower()}",
            "pageTitle": report_text(
                locale,
                "page_title",
                type_code=analysis["final_type"],
            ),
            "shareText": share_summary,
            "copiedLabel": report_text(locale, "copied"),
        },
        ensure_ascii=False,
    )

    favicon_b64 = base64.b64encode((asset_dir / "images" / "favicon.png").read_bytes()).decode("ascii")

    return template.substitute(
        html_lang=report_text(locale, "html_lang"),
        page_title=report_text(locale, "page_title", type_code=analysis["final_type"]),
        embedded_css=embedded_css,
        badge_svg=badge_svg,
        theme_key=theme_key,
        toolbar_title=report_text(
            locale,
            "toolbar_title",
            type_code=analysis["final_type"],
            type_label=localize_type_label(analysis["final_type"], locale),
        ),
        toolbar_subtitle=report_text(locale, "toolbar_subtitle"),
        jump_label=report_text(locale, "jump_label"),
        nav_links=build_nav_links(locale),
        download_html=report_text(locale, "download_html"),
        export_pdf=report_text(locale, "export_pdf"),
        share_label=report_text(locale, "share"),
        github_url="https://github.com/kingOfSoySauce/mbti-skill",
        clawhub_url="https://clawhub.ai/kingofsoysauce/mbti-analyzer",
        family_label=localize_family_label(analysis["final_type"], locale),
        type_code=analysis["final_type"],
        type_label=localize_type_label(analysis["final_type"], locale),
        confidence_label=localize_overall_confidence(analysis["overall_confidence"], locale),
        snapshot=html.escape(narrative_paragraphs[0]),
        section_profile=report_text(locale, "section_profile"),
        section_narrative=report_text(locale, "section_narrative"),
        section_functions=report_text(locale, "section_functions"),
        section_strengths=report_text(locale, "section_strengths"),
        section_blindspots=report_text(locale, "section_blindspots"),
        section_people=report_text(locale, "section_people", type_code=analysis["final_type"]),
        section_pressure=report_text(locale, "section_pressure"),
        section_evidence=report_text(locale, "section_evidence"),
        section_adjacent=report_text(locale, "section_adjacent"),
        section_uncertainty=report_text(locale, "section_uncertainty"),
        dimension_cards=dimension_cards,
        type_narrative=prose_html(narrative_paragraphs),
        function_validation=function_validation,
        strength_cards=strengths,
        blindspot_cards=blindspots,
        people_cards=people_cards,
        pressure_cards=pressure,
        evidence_cards="\n".join(evidence_cards),
        adjacent_cards=adjacent,
        uncertainty_cards=uncertainty,
        footer_note=report_text(locale, "footer_note"),
        action_payload=action_payload,
        FAVICON_BASE64=favicon_b64,
    )


def open_html_report(html_path: Path) -> None:
    """Open the HTML report in the default browser."""
    import subprocess
    import sys

    html_path = html_path.resolve()
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(html_path)])
    elif sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", str(html_path)])
    elif sys.platform == "win32":
        subprocess.Popen(["cmd", "/c", "start", "", str(html_path)])
    else:
        print(f"Cannot auto-open on {sys.platform}; open manually: {html_path}")


def write_reports(
    analysis: Dict,
    evidence_pool: Dict,
    output_dir: Path,
    quote_mode: str = "summary",
    auto_open: bool = False,
    report_language: str = "auto",
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    asset_dir = Path(__file__).resolve().parent.parent / "assets"
    markdown = render_markdown(analysis, evidence_pool, quote_mode, report_language)
    html_doc = render_html(analysis, evidence_pool, quote_mode, asset_dir, report_language)
    html_path = output_dir / "report.html"
    (output_dir / "report.md").write_text(markdown, encoding="utf-8")
    html_path.write_text(html_doc, encoding="utf-8")
    if auto_open:
        open_html_report(html_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render MBTI HTML and Markdown reports.")
    parser.add_argument("--analysis", help="Path to analysis_result.json")
    parser.add_argument("--evidence-pool", help="Path to evidence_pool.json")
    parser.add_argument("--output-dir", required=True, help="Where to write report.md and report.html")
    parser.add_argument("--quote-mode", choices=["summary", "none"], default="summary", help="How much to quote from evidence.")
    parser.add_argument("--language", choices=["auto", "en", "zh"], default="auto", help="Report language. Default auto-detects the dominant user/agent conversation language.")
    parser.add_argument("--debug-preview", action="store_true", help="Render a bundled preview fixture without depending on analysis_result.json or evidence_pool.json.")
    parser.add_argument("--debug-type", choices=sorted(TYPE_FUNCTIONS.keys()), default="INTP", help="Type code to use when --debug-preview is enabled.")
    parser.add_argument("--open", action="store_true", help="Open the HTML report in the default browser after rendering.")
    args = parser.parse_args()

    if args.debug_preview:
        if args.analysis or args.evidence_pool:
            parser.error("--debug-preview cannot be combined with --analysis or --evidence-pool.")
        analysis = build_debug_analysis(args.debug_type)
        evidence_pool = build_debug_evidence_pool(args.debug_type)
    else:
        if not args.analysis or not args.evidence_pool:
            parser.error("--analysis and --evidence-pool are required unless --debug-preview is used.")
        analysis = load_json(resolve_path(args.analysis))
        evidence_pool = load_json(resolve_path(args.evidence_pool))

    output_dir = resolve_path(args.output_dir)
    auto_open = getattr(args, "open", False)
    write_reports(
        analysis,
        evidence_pool,
        output_dir,
        args.quote_mode,
        auto_open=auto_open,
        report_language=args.language,
    )


if __name__ == "__main__":
    main()
