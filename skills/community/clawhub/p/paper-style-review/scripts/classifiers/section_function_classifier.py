#!/usr/bin/env python3
"""Section-level paragraph function classifier.

Unique responsibility:
- build non-overlapping section packages from physically anchored paragraphs;
- call LLM once per package to classify section expansion pattern and per-paragraph final type;
- return a single structured result that can be written back into the unified structure map.

The module does not determine physical structure. It consumes already-anchored
paragraphs and only performs semantic identity classification.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    from llm_client import call_llm_json
except Exception:
    from ..llm_client import call_llm_json


ABSTRACT_PARAGRAPH_TYPES: List[str] = [
    "abstract.background_context",
    "abstract.problem_statement",
    "abstract.research_objective",
    "abstract.method_overview",
    "abstract.contribution_item",
    "abstract.result_evidence",
    "abstract.conclusion_value",
]

CHAPTER1_PARAGRAPH_TYPES: List[str] = [
    "chapter1.background_trend",
    "chapter1.background_problem",
    "chapter1.background_evidence",
    "chapter1.background_need",
    "chapter1.background_significance",
    "chapter1.object_definition",
    "chapter1.object_scope",
    "chapter1.object_mechanism",
    "chapter1.object_limitation",
    "chapter1.research_objective",
    "chapter1.research_question",
    "chapter1.status_lead",
    "chapter1.status_category_frame",
    "chapter1.status_method_detail",
    "chapter1.status_comparison",
    "chapter1.status_limitation",
    "chapter1.status_gap",
    "chapter1.content_lead",
    "chapter1.content_problem_to_method",
    "chapter1.content_method_detail",
    "chapter1.content_expected_result",
    "chapter1.content_task_item",
    "chapter1.structure_lead",
    "chapter1.structure_chapter_map",
    "chapter1.structure_core_chapter",
    "chapter1.generic_lead",
    "chapter1.generic_detail",
    "chapter1.generic_transition",
]

SECTION_PARAGRAPH_TYPES: List[str] = [
    "section.lead",
    "section.background",
    "section.definition",
    "section.framework",
    "section.transition",
    "section.summary",
    "section.method_overview",
    "section.method_step",
    "section.mechanism_explanation",
    "section.component_description",
    "section.process_description",
    "section.implementation_detail",
    "section.experiment_setup",
    "section.metric_definition",
    "section.result_report",
    "section.result_analysis",
    "section.comparison_discussion",
    "section.result_summary",
    "section.concept_intro",
    "section.category_breakdown",
    "section.principle_explanation",
    "section.related_work_detail",
]

SECTION_EXPANSION_PATTERNS: List[str] = [
    "background_to_problem_to_need",
    "definition_to_breakdown",
    "lead_to_task_items",
    "problem_to_method",
    "method_to_steps",
    "framework_to_components",
    "setup_to_result_to_analysis",
    "related_work_to_gap",
    "chapter_map",
    "generic_progressive_exposition",
]


SECTION_FUNCTION_SYSTEM = """You are a thesis structure analyst.

Your only task is:
1. read one anchored thesis section package;
2. decide the section expansion pattern;
3. assign one final paragraph identity type to each paragraph.

Hard rules:
- You must classify by section position and local paragraph role together.
- You must only use the provided allowed paragraph types and allowed section patterns.
- Every paragraph must be assigned exactly one type.
- You must not merge, drop, or duplicate paragraphs.
- You must not rewrite the paragraph text.
- Abstract and Chapter 1 must be classified more finely than later chapters.
- Later chapters should use the unified section.* type family.
- Return JSON only.
"""


SECTION_FUNCTION_PROMPT = """## Task
Classify one thesis section package. Every paragraph in this package must be read exactly once and assigned exactly one final paragraph type.

## Section Anchor
- packageId: {package_id}
- anchorLevel: {anchor_level}
- sectionPath: {section_path}
- chapterTitle: {chapter_title}
- level2Title: {level2_title}
- level3Title: {level3_title}

## Allowed Section Expansion Patterns
{allowed_patterns}

## Allowed Paragraph Types
{allowed_types}

## Paragraphs
{paragraphs_block}

Return one JSON object with this schema:
{{
  "packageId": "{package_id}",
  "sectionExpansionPattern": "...",
  "sectionExpansionRationale": "...",
  "paragraphAssignments": [
    {{
      "paragraphId": "...",
      "paragraphOrdinalInSection": 1,
      "paragraphType": "...",
      "confidence": "high | medium | low",
      "rationale": "..."
    }}
  ]
}}

Constraints:
- paragraphType must be chosen from the allowed paragraph types only.
- sectionExpansionPattern must be chosen from the allowed patterns only.
- paragraphAssignments must cover all paragraphs exactly once.
- Keep rationale short and concrete.
- Think in a low-cost, low-overthinking way: focus on section position, local role, and paragraph order.
- Return JSON only.
"""


@dataclass(frozen=True)
class SectionPackage:
    package_id: str
    anchor_level: str
    section_path: str
    chapter_title: str
    level2_title: str
    level3_title: str
    chapter_number: Optional[int]
    paragraphs: List[Dict[str, Any]]


def _cfg_int(cfg: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int(cfg.get(key, default))
    except Exception:
        return default


def _cfg_float(cfg: Dict[str, Any], key: str, default: float) -> float:
    try:
        return float(cfg.get(key, default))
    except Exception:
        return default


def _paragraph_sort_key(item: Dict[str, Any]) -> Tuple[int, int]:
    position = item.get("physicalPosition", {}) if isinstance(item.get("physicalPosition"), dict) else {}
    return (
        int(position.get("paragraphOrdinalInDocument") or item.get("paragraphIndexInDocument") or 0),
        int(position.get("paragraphOrdinalInSection") or item.get("paragraphIndexInSection") or 0),
    )


def _anchor_level(item: Dict[str, Any]) -> str:
    position = item.get("physicalPosition", {}) if isinstance(item.get("physicalPosition"), dict) else {}
    if position.get("level3", {}).get("title"):
        return "level3"
    if position.get("level2", {}).get("title"):
        return "level2"
    return "level1"


def _allowed_paragraph_types(package: SectionPackage) -> List[str]:
    if package.chapter_number == 0:
        return ABSTRACT_PARAGRAPH_TYPES
    if package.chapter_number == 1:
        return CHAPTER1_PARAGRAPH_TYPES
    return SECTION_PARAGRAPH_TYPES


def _package_max_paragraphs(cfg: Dict[str, Any]) -> int:
    return max(1, _cfg_int(cfg, "sectionFunctionPackageMaxParagraphs", 24))


def _package_max_chars(cfg: Dict[str, Any]) -> int:
    return max(1000, _cfg_int(cfg, "sectionFunctionPackageMaxChars", 12000))


def _split_section_rows(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
    if not rows:
        return []
    max_paragraphs = _package_max_paragraphs(cfg)
    max_chars = _package_max_chars(cfg)
    windows: List[List[Dict[str, Any]]] = []
    current: List[Dict[str, Any]] = []
    current_chars = 0
    for row in rows:
        text = str(row.get("text") or "")
        text_len = len(text)
        if current and (len(current) >= max_paragraphs or current_chars + text_len > max_chars):
            windows.append(current)
            current = []
            current_chars = 0
        current.append(row)
        current_chars += text_len
    if current:
        windows.append(current)
    return windows


def build_section_packages(paragraphs: List[Dict[str, Any]], cfg: Optional[Dict[str, Any]] = None) -> List[SectionPackage]:
    config = dict(cfg or {})
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    section_meta: Dict[str, Dict[str, Any]] = {}
    for paragraph in paragraphs:
        section_path = str(paragraph.get("sectionPath") or "").strip()
        if not section_path:
            continue
        grouped.setdefault(section_path, []).append(paragraph)
        if section_path not in section_meta:
            position = paragraph.get("physicalPosition", {}) if isinstance(paragraph.get("physicalPosition"), dict) else {}
            section_meta[section_path] = {
                "chapterTitle": paragraph.get("chapterTitle") or "",
                "chapterNumber": paragraph.get("chapterNumber"),
                "level2Title": ((position.get("level2") or {}).get("title") or ""),
                "level3Title": ((position.get("level3") or {}).get("title") or ""),
                "anchorLevel": _anchor_level(paragraph),
            }

    ordered_sections = sorted(
        grouped.keys(),
        key=lambda key: _paragraph_sort_key(sorted(grouped[key], key=_paragraph_sort_key)[0]),
    )
    packages: List[SectionPackage] = []
    seen_paragraph_ids: set[str] = set()
    package_counter = 0
    for section_path in ordered_sections:
        rows = sorted(grouped[section_path], key=_paragraph_sort_key)
        for row in rows:
            paragraph_id = str(row.get("paragraphId") or "")
            if not paragraph_id:
                raise ValueError(f"missing paragraphId in section package {section_path}")
            if paragraph_id in seen_paragraph_ids:
                raise ValueError(f"duplicate paragraphId detected across section packages: {paragraph_id}")
            seen_paragraph_ids.add(paragraph_id)
        meta = section_meta[section_path]
        row_windows = _split_section_rows(rows, config)
        for window in row_windows:
            package_counter += 1
            packages.append(
                SectionPackage(
                    package_id=f"section-pkg-{package_counter:04d}",
                    anchor_level=str(meta["anchorLevel"]),
                    section_path=section_path,
                    chapter_title=str(meta["chapterTitle"]),
                    level2_title=str(meta["level2Title"]),
                    level3_title=str(meta["level3Title"]),
                    chapter_number=meta["chapterNumber"],
                    paragraphs=[
                        {
                            "paragraphId": row.get("paragraphId"),
                            "paragraphOrdinalInSection": (
                                (row.get("physicalPosition") or {}).get("paragraphOrdinalInSection")
                                if isinstance(row.get("physicalPosition"), dict)
                                else row.get("paragraphIndexInSection")
                            ),
                            "text": row.get("text") or "",
                        }
                        for row in window
                    ],
                )
            )
    return packages


def _render_allowed_patterns() -> str:
    return "\n".join(f"- {item}" for item in SECTION_EXPANSION_PATTERNS)


def _render_allowed_types(types: List[str]) -> str:
    return "\n".join(f"- {item}" for item in types)


def _render_paragraphs_block(package: SectionPackage) -> str:
    rows = []
    for paragraph in package.paragraphs:
        rows.append(
            f"[paragraphId={paragraph['paragraphId']}][ordinal={paragraph['paragraphOrdinalInSection']}]\n{paragraph['text']}"
        )
    return "\n\n".join(rows)


def _normalize_assignment(
    package: SectionPackage,
    assignment: Dict[str, Any],
    allowed_types: List[str],
) -> Dict[str, Any]:
    paragraph_id = str(assignment.get("paragraphId") or "").strip()
    paragraph_type = str(assignment.get("paragraphType") or "").strip()
    if paragraph_type not in allowed_types:
        raise ValueError(f"invalid paragraphType '{paragraph_type}' for package {package.package_id}")
    paragraph_index = {
        str(item["paragraphId"]): int(item["paragraphOrdinalInSection"])
        for item in package.paragraphs
    }
    if paragraph_id not in paragraph_index:
        raise ValueError(f"unknown paragraphId '{paragraph_id}' in package {package.package_id}")
    confidence = str(assignment.get("confidence") or "medium").strip().lower()
    if confidence not in {"high", "medium", "low"}:
        confidence = "medium"
    return {
        "paragraphId": paragraph_id,
        "paragraphOrdinalInSection": paragraph_index[paragraph_id],
        "paragraphType": paragraph_type,
        "confidence": confidence,
        "rationale": str(assignment.get("rationale") or "").strip(),
    }


def _validate_assignment_coverage(package: SectionPackage, normalized: List[Dict[str, Any]]) -> None:
    expected_ids = [str(item["paragraphId"]) for item in package.paragraphs]
    actual_ids = [str(item["paragraphId"]) for item in normalized]

    if len(actual_ids) != len(expected_ids):
        raise ValueError(
            f"paragraphAssignments must cover each paragraph exactly once for package {package.package_id}: "
            f"expected_count={len(expected_ids)}, actual_count={len(actual_ids)}"
        )

    seen = set()
    duplicates: List[str] = []
    for paragraph_id in actual_ids:
        if paragraph_id in seen and paragraph_id not in duplicates:
            duplicates.append(paragraph_id)
        seen.add(paragraph_id)
    if duplicates:
        raise ValueError(
            f"paragraphAssignments contains duplicate paragraphId(s) for package {package.package_id}: {duplicates}"
        )

    missing = [paragraph_id for paragraph_id in expected_ids if paragraph_id not in seen]
    unexpected = [paragraph_id for paragraph_id in actual_ids if paragraph_id not in set(expected_ids)]
    if missing or unexpected:
        raise ValueError(
            f"paragraphAssignments must cover each paragraph exactly once for package {package.package_id}: "
            f"missing={missing}, unexpected={unexpected}"
        )


def _repair_instruction(package: SectionPackage, error_message: str) -> str:
    expected_ids = [str(item["paragraphId"]) for item in package.paragraphs]
    return (
        "\n\nValidation failed on the previous output.\n"
        f"Reason: {error_message}\n"
        "Re-check the full package and return the whole JSON again.\n"
        f"Required paragraphIds in this package, exactly once each: {expected_ids}\n"
        "Do not omit, duplicate, or rename any paragraphId.\n"
        "Keep paragraphAssignments complete.\n"
    )


def classify_section_package(package: SectionPackage, llm_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = dict(llm_config or {})
    max_tokens = _cfg_int(cfg, "sectionFunctionMaxTokens", 1400)
    temperature = _cfg_float(cfg, "sectionFunctionTemperature", 0.0)
    max_attempts = max(1, _cfg_int(cfg, "sectionFunctionMaxAttempts", 3))
    allowed_types = _allowed_paragraph_types(package)
    base_prompt = SECTION_FUNCTION_PROMPT.format(
        package_id=package.package_id,
        anchor_level=package.anchor_level,
        section_path=package.section_path,
        chapter_title=package.chapter_title or "",
        level2_title=package.level2_title or "",
        level3_title=package.level3_title or "",
        allowed_patterns=_render_allowed_patterns(),
        allowed_types=_render_allowed_types(allowed_types),
        paragraphs_block=_render_paragraphs_block(package),
    )
    last_error: Optional[Exception] = None
    repair_suffix = ""
    for _attempt in range(1, max_attempts + 1):
        prompt = base_prompt + repair_suffix
        result = call_llm_json(prompt, SECTION_FUNCTION_SYSTEM, cfg, temperature=temperature, max_tokens=max_tokens)
        try:
            if not isinstance(result, dict):
                raise ValueError(f"section classifier returned non-object for package {package.package_id}")
            pattern = str(result.get("sectionExpansionPattern") or "").strip()
            if pattern not in SECTION_EXPANSION_PATTERNS:
                raise ValueError(f"invalid sectionExpansionPattern '{pattern}' for package {package.package_id}")
            raw_assignments = result.get("paragraphAssignments", [])
            if not isinstance(raw_assignments, list):
                raise ValueError(f"paragraphAssignments must be a list for package {package.package_id}")
            normalized = [_normalize_assignment(package, item, allowed_types) for item in raw_assignments if isinstance(item, dict)]
            _validate_assignment_coverage(package, normalized)
            normalized.sort(key=lambda item: item["paragraphOrdinalInSection"])
            return {
                "packageId": package.package_id,
                "anchorLevel": package.anchor_level,
                "sectionPath": package.section_path,
                "chapterTitle": package.chapter_title,
                "level2Title": package.level2_title,
                "level3Title": package.level3_title,
                "sectionExpansionPattern": pattern,
                "sectionExpansionRationale": str(result.get("sectionExpansionRationale") or "").strip(),
                "paragraphAssignments": normalized,
            }
        except ValueError as exc:
            last_error = exc
            repair_suffix = _repair_instruction(package, str(exc))
    raise last_error or ValueError(f"section classifier failed for package {package.package_id}")


def classify_section_packages(
    paragraphs: List[Dict[str, Any]],
    llm_config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    cfg = dict(llm_config or {})
    packages = build_section_packages(paragraphs, cfg)
    parallelism = max(1, _cfg_int(cfg, "sectionFunctionParallelism", 2))
    if parallelism == 1:
        return [classify_section_package(package, cfg) for package in packages]
    with ThreadPoolExecutor(max_workers=parallelism) as executor:
        results = list(executor.map(lambda pkg: classify_section_package(pkg, cfg), packages))
    order = {package.package_id: idx for idx, package in enumerate(packages)}
    results.sort(key=lambda item: order.get(item.get("packageId"), 10**9))
    return results


def build_section_function_index(section_results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    mapping: Dict[str, Dict[str, Any]] = {}
    for section in section_results:
        for assignment in section.get("paragraphAssignments", []):
            paragraph_id = str(assignment.get("paragraphId") or "").strip()
            if not paragraph_id:
                continue
            mapping[paragraph_id] = {
                "paragraphType": assignment.get("paragraphType"),
                "confidence": assignment.get("confidence"),
                "rationale": assignment.get("rationale"),
                "sectionExpansionPattern": section.get("sectionExpansionPattern"),
                "sectionExpansionRationale": section.get("sectionExpansionRationale"),
                "packageId": section.get("packageId"),
            }
    return mapping
