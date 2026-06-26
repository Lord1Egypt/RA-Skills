#!/usr/bin/env python3
"""Shared runtime for style-learning/style-annotation units.

Single responsibility:
- convert paper-structure-map paragraphs into minimal style-task units;
- keep one shared file contract for refs style learning and target style annotation;
- expose structured anchors derived from the same structure map.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from contracts import ANCHOR_CONTRACT_VERSION, AnchorKind
except Exception:
    from .contracts import ANCHOR_CONTRACT_VERSION, AnchorKind


def _text(value: Any) -> str:
    return str(value or "").strip()


def _path_parts(section_path: str) -> List[str]:
    return [part.strip() for part in str(section_path or "").split(" > ") if part.strip()]


def build_style_anchor(paragraph: Dict[str, Any]) -> Dict[str, Any]:
    physical = paragraph.get("physicalParagraph") or {}
    position = paragraph.get("physicalPosition") or {}
    anchor: Dict[str, Any] = {
        "contract_version": ANCHOR_CONTRACT_VERSION,
        "kind": AnchorKind.BODY_PARAGRAPH.value,
        "resolver": "paper_structure_map",
        "matched_from": "paper_structure_map",
        "node_id": physical.get("nodeId") or physical.get("paragraphId"),
        "presentation_node_id": physical.get("presentationNodeId") or physical.get("nodeId") or physical.get("paragraphId"),
        "presentation_kind": physical.get("presentationKind") or "body_paragraph",
        "paragraph_index": physical.get("paragraphIndex"),
        "xml_paragraph_index": physical.get("xmlParagraphIndex"),
        "section_path": _path_parts(position.get("sectionPath") or paragraph.get("sectionPath") or ""),
    }
    if physical.get("reviewParagraphIndex") is not None:
        anchor["proxy_paragraph_index"] = physical.get("reviewParagraphIndex")
    return {key: value for key, value in anchor.items() if value not in (None, "", [])}


def build_style_unit(paragraph: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    functional = paragraph.get("functionalType") or {}
    section_expansion = paragraph.get("sectionExpansion") or {}
    position = paragraph.get("physicalPosition") or {}
    level2 = position.get("level2") or {}
    level3 = position.get("level3") or {}
    paragraph_type = _text(functional.get("paragraphType") or paragraph.get("styleLearningBucket"))
    text = _text(paragraph.get("text"))
    if not paragraph_type or not text:
        return None
    ordinal = position.get("paragraphOrdinalInSection") or paragraph.get("paragraphIndexInSection")
    location_hint = _text(paragraph.get("sectionPath"))
    if ordinal:
        location_hint = f"{location_hint} > 第{int(ordinal)}段" if location_hint else f"第{int(ordinal)}段"
    return {
        "unitId": _text(paragraph.get("id") or paragraph.get("paragraphId")),
        "paragraphId": _text(paragraph.get("paragraphId")),
        "paragraphType": paragraph_type,
        "sectionExpansionPattern": _text(section_expansion.get("pattern")),
        "sectionPath": _text(paragraph.get("sectionPath")),
        "chapterNumber": paragraph.get("chapterNumber"),
        "chapterTitle": _text(paragraph.get("chapterTitle")),
        "level2Title": _text(level2.get("title")),
        "level3Title": _text(level3.get("title")),
        "paragraphOrdinalInDocument": position.get("paragraphOrdinalInDocument") or paragraph.get("paragraphIndexInDocument"),
        "paragraphOrdinalInSection": ordinal,
        "positionAnchorType": _text((paragraph.get("positionAnchor") or {}).get("type")),
        "text": text,
        "textHash": _text(paragraph.get("textHash")),
        "locationHint": location_hint,
        "anchor": build_style_anchor(paragraph),
    }


def extract_style_units(structure_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    units: List[Dict[str, Any]] = []
    for paragraph in structure_map.get("paragraphs", []):
        if not isinstance(paragraph, dict):
            continue
        unit = build_style_unit(paragraph)
        if unit:
            units.append(unit)
    return units


def load_structure_map(path: str | Path) -> Dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"structure map must be a JSON object: {path}")
    return payload


def load_style_units(path: str | Path) -> List[Dict[str, Any]]:
    return extract_style_units(load_structure_map(path))


def build_units_report(structure_map: Dict[str, Any], *, source_path: str = "") -> Dict[str, Any]:
    units = extract_style_units(structure_map)
    return {
        "meta": {
            "module": "style_units_runtime",
            "version": "1.0-paper-structure-map-style-units",
            "sourcePath": source_path or ((structure_map.get("meta") or {}).get("targetPath")),
            "paragraphCount": len(units),
            "paragraphTypeCount": len({unit["paragraphType"] for unit in units}),
        },
        "units": units,
    }
