#!/usr/bin/env python3
"""Shared chapter-scope parsing and filtering."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Optional, Set


ABSTRACT_SCOPE_TOKENS = {"0", "abstract", "摘要"}


def normalize_chapter_scope(raw: Any) -> Optional[List[int]]:
    if raw is None:
        return None

    values: List[Any]
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return None
        values = [part.strip() for part in text.split(",") if part.strip()]
    elif isinstance(raw, (list, tuple, set)):
        values = list(raw)
    else:
        values = [raw]

    normalized: List[int] = []
    seen: Set[int] = set()
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        lowered = text.lower()
        if lowered in ABSTRACT_SCOPE_TOKENS:
            number = 0
        else:
            try:
                number = int(text)
            except Exception as exc:
                raise ValueError(f"invalid chapter scope token: {value}") from exc
            if number < 0:
                raise ValueError(f"chapter number must be >= 0: {value}")
        if number not in seen:
            seen.add(number)
            normalized.append(number)
    return normalized or None


def chapter_scope_label(scope: Optional[Iterable[int]]) -> str:
    if not scope:
        return "all"
    labels = []
    for chapter_number in scope:
        labels.append("abstract" if int(chapter_number) == 0 else str(int(chapter_number)))
    return ",".join(labels)


def chapter_in_scope(chapter_number: Any, scope: Optional[Iterable[int]]) -> bool:
    if scope is None:
        return True
    try:
        number = int(chapter_number)
    except Exception:
        return False
    return number in set(int(item) for item in scope)


def filter_outline_by_chapter_scope(outline: List[Dict[str, Any]], scope: Optional[Iterable[int]]) -> List[Dict[str, Any]]:
    if scope is None:
        return list(outline)
    kept: List[Dict[str, Any]] = []
    visible_paths: Set[str] = set()
    scope_set = set(int(item) for item in scope)
    for node in outline:
        if not isinstance(node, dict):
            continue
        chapter_number = node.get("chapterNumber")
        if chapter_number is not None and chapter_in_scope(chapter_number, scope_set):
            kept.append(node)
            path = str(node.get("path") or "").strip()
            if path:
                visible_paths.add(path)
            continue
        section_kind = str(node.get("sectionKind") or "").strip().lower()
        raw_text = str(node.get("rawText") or node.get("title") or "").strip().lower()
        if 0 in scope_set and (section_kind in {"abstract", "front"} or raw_text in {"摘要", "abstract"}):
            kept.append(node)
            path = str(node.get("path") or "").strip()
            if path:
                visible_paths.add(path)
            continue
        path = str(node.get("path") or "").strip()
        if path and any(parent and path.startswith(parent + " > ") for parent in visible_paths):
            kept.append(node)
    return kept


def filter_section_classifications_by_scope(
    section_classifications: List[Dict[str, Any]],
    kept_paragraph_ids: Set[str],
) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for item in section_classifications:
        if not isinstance(item, dict):
            continue
        assignments = [
            assignment
            for assignment in item.get("paragraphAssignments", [])
            if isinstance(assignment, dict) and str(assignment.get("paragraphId") or "").strip() in kept_paragraph_ids
        ]
        if not assignments:
            continue
        cloned = deepcopy(item)
        cloned["paragraphAssignments"] = assignments
        filtered.append(cloned)
    return filtered


def filter_structure_map_by_chapter_scope(
    structure_map: Dict[str, Any],
    raw_scope: Any,
) -> Dict[str, Any]:
    scope = normalize_chapter_scope(raw_scope)
    if scope is None:
        return deepcopy(structure_map)

    filtered = deepcopy(structure_map)
    paragraphs = [
        paragraph
        for paragraph in filtered.get("paragraphs", [])
        if isinstance(paragraph, dict) and chapter_in_scope(paragraph.get("chapterNumber"), scope)
    ]
    kept_paragraph_ids = {
        str(paragraph.get("paragraphId") or "").strip()
        for paragraph in paragraphs
        if str(paragraph.get("paragraphId") or "").strip()
    }
    filtered["paragraphs"] = paragraphs
    filtered["sectionClassifications"] = filter_section_classifications_by_scope(
        filtered.get("sectionClassifications", []),
        kept_paragraph_ids,
    )
    filtered["outline"] = filter_outline_by_chapter_scope(filtered.get("outline", []), scope)
    meta = filtered.get("meta") if isinstance(filtered.get("meta"), dict) else {}
    meta["chapterScope"] = list(scope)
    meta["chapterScopeLabel"] = chapter_scope_label(scope)
    meta["paragraphCount"] = len(paragraphs)
    meta["sectionClassificationCount"] = len(filtered["sectionClassifications"])
    meta["outlineNodeCount"] = len(filtered["outline"])
    filtered["meta"] = meta
    return filtered
