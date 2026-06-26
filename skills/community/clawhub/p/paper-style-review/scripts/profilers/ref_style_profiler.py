#!/usr/bin/env python3
"""参考语料 style-profile 生成器。

唯一主线：
- refs 先走统一 paper-structure-map；
- 从结构图谱中提取已完成物理锚定和 paragraphType 判定的段落；
- 再按 paragraphType 聚类；
- 每个 paragraphType 用 LLM 提取结构化风格机制画像；
- 下游统一消费这里输出的 style-profile.json / ref-style-basis.md。
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from llm_client import extract_style_profile_for_paragraph_type
    from paper_structure_anchor import build_paper_structure_map
    from style_prompt_contract import STYLE_PROFILE_EXTRACTION_VERSION
    from style_units_runtime import extract_style_units, load_structure_map
except Exception:
    from ..llm_client import extract_style_profile_for_paragraph_type
    from ..paper_structure_anchor import build_paper_structure_map
    from ..style_prompt_contract import STYLE_PROFILE_EXTRACTION_VERSION
    from ..style_units_runtime import extract_style_units, load_structure_map


MECHANISM_FIELDS: List[str] = [
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


def _cfg_int(cfg: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int(cfg.get(key, default))
    except Exception:
        return default


def _string(value: Any) -> str:
    return str(value or "").strip()


def _string_list(value: Any, limit: int | None = None) -> List[str]:
    items: List[str] = []
    if isinstance(value, list):
        for item in value:
            text = _string(item)
            if text:
                items.append(text)
    elif isinstance(value, str):
        text = value.strip()
        if text:
            items.append(text)
    if limit is not None:
        return items[:limit]
    return items


def _sample_group(items: List[Dict[str, Any]], max_samples: int) -> List[Dict[str, Any]]:
    if max_samples <= 0 or len(items) <= max_samples:
        return list(items)
    by_ref: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        ref_id = _string(item.get("refId") or item.get("refAlias") or "unknown")
        by_ref[ref_id].append(item)

    sampled: List[Dict[str, Any]] = []
    ordered_refs = sorted(by_ref)
    cursor = 0
    while len(sampled) < max_samples and ordered_refs:
        ref_id = ordered_refs[cursor % len(ordered_refs)]
        if by_ref[ref_id]:
            sampled.append(by_ref[ref_id].pop(0))
        cursor += 1
        ordered_refs = [key for key in ordered_refs if by_ref[key]]
    return sampled


def _load_ref_structure_map(ref: Any, llm_config: Dict[str, Any] | None = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    structure_map_path = _string(getattr(ref, "structureMapPath", None) or (ref.get("structureMapPath") if isinstance(ref, dict) else None))
    if structure_map_path:
        structure_map = load_structure_map(structure_map_path)
    else:
        structure_map = build_paper_structure_map(Path(ref.path), llm_config=llm_config)
    paragraphs = []
    for unit in extract_style_units(structure_map):
        unit = dict(unit)
        unit["refId"] = getattr(ref, "id", None) if not isinstance(ref, dict) else ref.get("id")
        unit["refAlias"] = getattr(ref, "alias", None) if not isinstance(ref, dict) else ref.get("alias")
        if not _string(unit.get("refAlias")):
            unit["refAlias"] = "匿"
        paragraphs.append(unit)
    return structure_map, paragraphs


def _normalize_mechanisms(raw: Dict[str, Any]) -> Dict[str, str]:
    mechanisms = raw.get("mechanisms") or {}
    output: Dict[str, str] = {}
    for field in MECHANISM_FIELDS:
        text = _string(mechanisms.get(field))
        if text:
            output[field] = text
    return output


def _normalize_llm_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "oneLine": _string(raw.get("oneLine")),
        "mechanisms": _normalize_mechanisms(raw),
        "formula": _string(raw.get("formula")),
        "rules": _string_list(raw.get("rules"), limit=5),
        "signatureTraits": _string_list(raw.get("signatureTraits"), limit=3),
        "confidence": _string(raw.get("confidence") or "medium") or "medium",
        "confidenceNotes": _string(raw.get("confidenceNotes")),
    }


def _basis_items_for_profile(
    paragraph_type: str,
    profile: Dict[str, Any],
    support_refs: List[str],
    next_basis_id: int,
) -> List[Dict[str, Any]]:
    basis_items: List[Dict[str, Any]] = []
    analysis = profile.get("analysis") or {}
    one_line = _string(analysis.get("oneLine"))
    if one_line:
        basis_items.append(
            {
                "basisId": f"basis-{next_basis_id:03d}",
                "dimension": "oneLine",
                "paragraphType": paragraph_type,
                "claim": one_line,
                "supportedByRefs": support_refs,
                "confidence": analysis.get("confidence", "medium"),
            }
        )
        next_basis_id += 1
    for field, text in (analysis.get("mechanisms") or {}).items():
        text = _string(text)
        if not text:
            continue
        basis_items.append(
            {
                "basisId": f"basis-{next_basis_id:03d}",
                "dimension": field,
                "paragraphType": paragraph_type,
                "claim": text,
                "supportedByRefs": support_refs,
                "confidence": analysis.get("confidence", "medium"),
            }
        )
        next_basis_id += 1
    formula = _string(analysis.get("formula"))
    if formula:
        basis_items.append(
            {
                "basisId": f"basis-{next_basis_id:03d}",
                "dimension": "formula",
                "paragraphType": paragraph_type,
                "claim": formula,
                "supportedByRefs": support_refs,
                "confidence": analysis.get("confidence", "medium"),
            }
        )
    return basis_items


def build_style_profile(ref_docs: List[Any], llm_config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    cfg = dict(llm_config or {})
    sample_limit = _cfg_int(cfg, "styleProfileSampleLimit", 0)
    ref_parallelism = max(1, _cfg_int(cfg, "styleProfileRefParallelism", 1))
    profile_parallelism = max(1, _cfg_int(cfg, "styleProfileParallelism", 1))

    def _load_one(ref: Any) -> Dict[str, Any]:
        structure_map, paragraphs = _load_ref_structure_map(ref, llm_config=cfg)
        type_counter = Counter(item["paragraphType"] for item in paragraphs)
        return {
            "ref": ref,
            "structureMap": structure_map,
            "paragraphs": paragraphs,
            "paragraphTypeCounts": dict(type_counter),
        }

    if ref_parallelism == 1:
        loaded_refs = [_load_one(ref) for ref in ref_docs]
    else:
        with ThreadPoolExecutor(max_workers=ref_parallelism) as executor:
            loaded_refs = list(executor.map(_load_one, ref_docs))

    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    all_paragraphs = 0
    for loaded in loaded_refs:
        for paragraph in loaded["paragraphs"]:
            grouped[paragraph["paragraphType"]].append(paragraph)
            all_paragraphs += 1

    def _profile_one(paragraph_type: str) -> Tuple[str, Dict[str, Any]]:
        items = grouped[paragraph_type]
        sampled = _sample_group(items, sample_limit)
        llm_profile = extract_style_profile_for_paragraph_type(
            paragraph_type=paragraph_type,
            paragraphs=sampled,
            config=cfg,
        )
        normalized_llm_profile = _normalize_llm_profile(llm_profile)
        expansion_counter = Counter(
            _string(item.get("sectionExpansionPattern"))
            for item in items
            if _string(item.get("sectionExpansionPattern"))
        )
        support_refs = sorted({_string(item.get("refAlias")) for item in items if _string(item.get("refAlias"))})
        section_paths = []
        seen_paths = set()
        for item in items:
            path = _string(item.get("sectionPath"))
            if not path or path in seen_paths:
                continue
            seen_paths.add(path)
            section_paths.append(path)
            if len(section_paths) >= 6:
                break
        paragraph_orders = sorted(
            {
                int(item.get("paragraphOrdinalInSection"))
                for item in items
                if item.get("paragraphOrdinalInSection") is not None
            }
        )
        return (
            paragraph_type,
            {
                "paragraphType": paragraph_type,
                "coverage": {
                    "paragraphs": len(items),
                    "refs": len(support_refs),
                },
                "supportRefs": support_refs,
                "context": {
                    "sectionExpansionPatterns": [
                        {"pattern": name, "count": count}
                        for name, count in expansion_counter.most_common(6)
                    ],
                    "sampleSectionPaths": section_paths,
                    "paragraphOrdersInSection": paragraph_orders[:8],
                },
                "analysis": normalized_llm_profile,
            },
        )

    ordered_paragraph_types = sorted(grouped)
    if profile_parallelism == 1:
        profiled_items = [_profile_one(paragraph_type) for paragraph_type in ordered_paragraph_types]
    else:
        with ThreadPoolExecutor(max_workers=profile_parallelism) as executor:
            profiled_items = list(executor.map(_profile_one, ordered_paragraph_types))

    paragraph_type_profiles: Dict[str, Dict[str, Any]] = {}
    basis_index: List[Dict[str, Any]] = []
    next_basis_id = 1
    for paragraph_type, profile in profiled_items:
        paragraph_type_profiles[paragraph_type] = profile
        new_basis = _basis_items_for_profile(paragraph_type, profile, profile.get("supportRefs") or [], next_basis_id)
        basis_index.extend(new_basis)
        next_basis_id += len(new_basis)

    refs_summary = []
    for loaded in loaded_refs:
        ref = loaded["ref"]
        structure_map = loaded["structureMap"]
        refs_summary.append(
            {
                "alias": getattr(ref, "alias", None) or "匿",
                "paragraphCount": len(loaded["paragraphs"]),
                "paragraphTypeCount": len(loaded["paragraphTypeCounts"]),
                "structureMapVersion": _string((structure_map.get("meta") or {}).get("version")),
            }
        )

    profile = {
        "meta": {
            "version": "3.0-paragraph-type-style-profile",
            "styleProfileExtractionVersion": STYLE_PROFILE_EXTRACTION_VERSION,
            "profileBasis": "paper-structure-map",
            "refCount": len(ref_docs),
            "paragraphCount": all_paragraphs,
            "paragraphTypeCount": len(paragraph_type_profiles),
            "compactProfile": True,
            "anonymizedRefs": True,
            "useRefsAsOnlyBasis": True,
        },
        "refs": refs_summary,
        "paragraphTypeProfiles": paragraph_type_profiles,
        "basisIndex": basis_index,
        "handoffSummary": {
            "paragraphTypes": sorted(paragraph_type_profiles),
            "focus": [
                "Style learning is grounded on paper-structure-map paragraphType.",
                "Each profile is learned from same-type paragraphs only.",
                "Only the matched paragraphType profile should be sent to the LLM in later style review.",
            ],
        },
    }
    return profile


def write_style_profile(ref_docs: List[Any], output_dir: str | Path, llm_config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = build_style_profile(ref_docs, llm_config=llm_config)
    (output_dir / "style-profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Ref Style Basis", ""]
    lines.append("## Enabled Refs")
    for ref in profile.get("refs", []):
        lines.append(f"- {ref.get('alias')}: {ref.get('paragraphCount', 0)} paragraphs, {ref.get('paragraphTypeCount', 0)} paragraph types")

    for paragraph_type in sorted(profile.get("paragraphTypeProfiles", {})):
        item = profile["paragraphTypeProfiles"][paragraph_type]
        analysis = item.get("analysis") or {}
        lines.extend(["", f"## {paragraph_type}"])
        coverage = item.get("coverage") or {}
        lines.append(f"- Covered refs: {coverage.get('refs', 0)} / {profile.get('meta', {}).get('refCount', 0)}")
        lines.append(f"- Sample paragraphs: {coverage.get('paragraphs', 0)}")
        if analysis.get("oneLine"):
            lines.append(f"- One-line style: {analysis.get('oneLine')}")
        if analysis.get("formula"):
            lines.append(f"- Formula: {analysis.get('formula')}")
        for field in MECHANISM_FIELDS:
            text = _string((analysis.get("mechanisms") or {}).get(field))
            if text:
                lines.append(f"- {field}: {text}")
        rules = _string_list(analysis.get("rules"))
        if rules:
            lines.append(f"- Rules: {'；'.join(rules[:5])}")
        traits = _string_list(analysis.get("signatureTraits"))
        if traits:
            lines.append(f"- Signature traits: {'；'.join(traits[:3])}")
    (output_dir / "ref-style-basis.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return profile


if __name__ == "__main__":
    print("Use from orchestrator.")
