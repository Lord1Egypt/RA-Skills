#!/usr/bin/env python3
"""style-profile 运行时共享工具。

统一提供：
- paragraphType 风格画像的提示词载荷
- 风格依据 basisIndex 查询
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List


def _string_list(value: Any, *, limit: int | None = None) -> List[str]:
    items: List[str] = []
    if isinstance(value, list):
        for item in value:
            text = str(item or "").strip()
            if text:
                items.append(text)
    elif isinstance(value, str):
        text = value.strip()
        if text:
            items.append(text)
    if limit is not None:
        return items[:limit]
    return items


def build_segment_style_prompt_payload(segment_profile: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(segment_profile, dict):
        return {}
    analysis = segment_profile.get("analysis") or {}
    return {
        "paragraphType": str(segment_profile.get("paragraphType") or "").strip(),
        "oneLine": str(analysis.get("oneLine") or "").strip(),
        "mechanisms": {
            str(axis).strip(): str(summary).strip()
            for axis, summary in (analysis.get("mechanisms") or {}).items()
            if str(axis).strip() and str(summary).strip()
        },
        "formula": str(analysis.get("formula") or "").strip(),
        "rules": _string_list(analysis.get("rules"), limit=5),
        "signatureTraits": _string_list(analysis.get("signatureTraits"), limit=3),
        "confidence": str(analysis.get("confidence") or "").strip(),
        "confidenceNotes": str(analysis.get("confidenceNotes") or "").strip(),
        "context": segment_profile.get("context") or {},
    }


MECHANISM_PRIORITY = [
    "logic",
    "linking",
    "closure",
    "density",
    "rhythm",
    "tone",
    "evidence",
    "focus",
    "units",
    "markers",
    "stance",
    "abstraction",
    "reader",
    "rhetoric",
    "persuasion",
    "emotion",
]


def _pick_mechanisms(mechanisms: Dict[str, Any], limit: int) -> Dict[str, str]:
    normalized = {
        str(axis).strip(): str(summary).strip()
        for axis, summary in (mechanisms or {}).items()
        if str(axis).strip() and str(summary).strip()
    }
    picked: Dict[str, str] = {}
    for axis in MECHANISM_PRIORITY:
        value = normalized.get(axis)
        if value:
            picked[axis] = value
        if len(picked) >= limit:
            return picked
    for axis, value in normalized.items():
        if axis not in picked:
            picked[axis] = value
        if len(picked) >= limit:
            break
    return picked


def _trim_context(context: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(context, dict):
        return {}
    output: Dict[str, Any] = {}
    sample_paths = context.get("sampleSectionPaths")
    if isinstance(sample_paths, list):
        values = [str(item).strip() for item in sample_paths if str(item).strip()]
        if values:
            output["sampleSectionPaths"] = values[:3]
    patterns = context.get("sectionExpansionPatterns")
    if isinstance(patterns, list):
        trimmed_patterns = []
        for item in patterns[:3]:
            if not isinstance(item, dict):
                continue
            pattern = str(item.get("pattern") or "").strip()
            count = item.get("count")
            if pattern:
                trimmed_patterns.append({"pattern": pattern, "count": count})
        if trimmed_patterns:
            output["sectionExpansionPatterns"] = trimmed_patterns
    orders = context.get("paragraphOrdersInSection")
    if isinstance(orders, list):
        values = []
        for item in orders[:6]:
            try:
                values.append(int(item))
            except Exception:
                continue
        if values:
            output["paragraphOrdersInSection"] = values
    return output


def build_compact_segment_style_payload(
    segment_profile: Dict[str, Any],
    *,
    mechanism_limit: int = 6,
    rule_limit: int = 4,
    trait_limit: int = 3,
) -> Dict[str, Any]:
    if not isinstance(segment_profile, dict):
        return {}
    analysis = segment_profile.get("analysis") or {}
    return {
        "paragraphType": str(segment_profile.get("paragraphType") or "").strip(),
        "oneLine": str(analysis.get("oneLine") or "").strip(),
        "formula": str(analysis.get("formula") or "").strip(),
        "topMechanisms": _pick_mechanisms(analysis.get("mechanisms") or {}, mechanism_limit),
        "rules": _string_list(analysis.get("rules"), limit=rule_limit),
        "signatureTraits": _string_list(analysis.get("signatureTraits"), limit=trait_limit),
        "context": _trim_context(segment_profile.get("context") or {}),
    }


def build_style_profile_slice(
    style_profile: Dict[str, Any],
    paragraph_types: Iterable[str],
    *,
    mechanism_limit: int = 6,
    rule_limit: int = 4,
    trait_limit: int = 3,
) -> Dict[str, Any]:
    paragraph_type_profiles = (style_profile or {}).get("paragraphTypeProfiles", {})
    ordered_types: List[str] = []
    seen = set()
    for raw in paragraph_types:
        paragraph_type = str(raw or "").strip()
        if paragraph_type and paragraph_type not in seen:
            ordered_types.append(paragraph_type)
            seen.add(paragraph_type)
    profiles: Dict[str, Any] = {}
    for paragraph_type in ordered_types:
        segment_profile = paragraph_type_profiles.get(paragraph_type)
        if not isinstance(segment_profile, dict):
            continue
        compact = build_compact_segment_style_payload(
            segment_profile,
            mechanism_limit=mechanism_limit,
            rule_limit=rule_limit,
            trait_limit=trait_limit,
        )
        if compact:
            profiles[paragraph_type] = compact
    return {
        "meta": {
            "module": "style_profile_runtime",
            "version": "compact-style-profile-slice-v1",
            "paragraphTypeCount": len(profiles),
        },
        "profiles": profiles,
    }


def render_segment_style_prompt_payload(segment_profile: Dict[str, Any]) -> str:
    payload = build_segment_style_prompt_payload(segment_profile)
    if not payload:
        return "null"
    return json.dumps(payload, ensure_ascii=False, indent=2)


def lookup_style_basis(style_profile: Dict[str, Any], segment_type: str, dimension: str) -> str:
    basis_index = style_profile.get("basisIndex", []) if isinstance(style_profile, dict) else []
    for item in basis_index:
        if not isinstance(item, dict):
            continue
        if item.get("paragraphType") != segment_type or item.get("dimension") != dimension:
            continue
        claim = str(item.get("claim") or "").strip()
        basis_id = str(item.get("basisId") or "").strip()
        if basis_id and claim:
            return f"refs 风格依据（{basis_id}）：{claim}"
        if claim:
            return f"refs 风格依据：{claim}"
    if segment_type and dimension:
        return f"refs 风格依据：{segment_type} 的{dimension}与参考画像不一致。"
    return "refs 风格依据：当前段落与参考画像不一致。"
