#!/usr/bin/env python3
"""Standalone orchestrators for the three style stages.

Stage 1: refs -> style-profile.json
Stage 2: target + style-profile.json -> style-deviation-report.json
Stage 3: reports -> annotations.json -> annotated.docx
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List

from annotation_anchor_infra import materialize_report_anchors
from annotation_assembler import assemble_annotations, ensure_style_deviation_report, write_annotations_json
from chapter_scope import chapter_scope_label, filter_structure_map_by_chapter_scope, normalize_chapter_scope
from fused_review_runtime import run_fused_target_review
from paper_structure_anchor import build_paper_structure_map
from profilers.ref_style_profiler import write_style_profile
from runtime_config import normalize_runtime_config
from style_units_runtime import build_units_report, extract_style_units, load_structure_map


STYLE_PROFILE_FILENAME = "style-profile.json"
REF_STYLE_BASIS_FILENAME = "ref-style-basis.md"
TARGET_STRUCTURE_MAP_FILENAME = "target-structure-map.json"
ANNOTATIONS_FILENAME = "annotations.json"


def _ref_alias(ref_index: int) -> str:
    return f"ref-style-{int(ref_index):02d}"


def _normalized(config: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_runtime_config(config)


def _style_profile_path(output_dir: Path) -> Path:
    return output_dir / STYLE_PROFILE_FILENAME


def load_style_profile_into_output(config: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
    """Load an existing style-profile and materialize it into the current output dir.

    This is the single handoff contract between:
    - standalone refs style learning output
    - target-side style/fused review
    - downstream style-deviation assembly
    """
    explicit = str(config.get("styleProfilePath") or "").strip()
    if explicit:
        source_path = Path(explicit).expanduser().resolve()
    else:
        source_path = _style_profile_path(output_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"style profile not found: {source_path}")

    profile = json.loads(source_path.read_text(encoding="utf-8"))
    canonical_path = _style_profile_path(output_dir)
    canonical_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "styleProfilePath": str(canonical_path),
        "styleProfileSourcePath": str(source_path),
        "styleProfile": profile,
    }


def _target_structure_map_path(output_dir: Path, config: Dict[str, Any]) -> Path:
    explicit = str(config.get("targetStructureMapPath") or "").strip()
    if explicit:
        return Path(explicit).expanduser().resolve()
    return output_dir / TARGET_STRUCTURE_MAP_FILENAME


def _target_fingerprint(path: Path) -> Dict[str, Any]:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    stat = path.stat()
    return {
        "algorithm": "sha256",
        "sha256": digest.hexdigest(),
        "size": int(stat.st_size),
    }


def _normalize_scope_value(scope: Any) -> List[int] | None:
    normalized = normalize_chapter_scope(scope)
    return list(normalized) if normalized is not None else None


def _structure_map_matches_target(
    structure_map: Dict[str, Any],
    target_path: Path,
    fingerprint: Dict[str, Any],
    chapter_scope: List[int] | None,
) -> bool:
    if not isinstance(structure_map, dict):
        return False
    meta = structure_map.get("meta")
    if not isinstance(meta, dict):
        return False
    recorded_target = str(meta.get("targetPath") or "").strip()
    if recorded_target and recorded_target != str(target_path):
        return False
    recorded_fp = meta.get("targetFingerprint")
    if not isinstance(recorded_fp, dict):
        return False
    recorded_scope = _normalize_scope_value(meta.get("chapterScope"))
    return (
        str(recorded_fp.get("algorithm") or "") == str(fingerprint.get("algorithm") or "")
        and str(recorded_fp.get("sha256") or "") == str(fingerprint.get("sha256") or "")
        and int(recorded_fp.get("size") or -1) == int(fingerprint.get("size") or -2)
        and recorded_scope == chapter_scope
    )


def _stamp_target_fingerprint(structure_map: Dict[str, Any], target_path: Path, fingerprint: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(structure_map or {})
    meta = dict(payload.get("meta") or {})
    meta["targetPath"] = str(target_path)
    meta["targetFingerprint"] = dict(fingerprint)
    meta["targetFingerprintPolicy"] = "content-sha256"
    payload["meta"] = meta
    return payload


def prepare_target_style_units(config: Dict[str, Any]) -> Dict[str, Any]:
    normalized = _normalized(config)
    output_dir = Path(normalized["outputDir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    llm_config = normalized.get("llmConfig")
    chapter_scope = normalize_chapter_scope(config.get("chapterScope"))

    target_path = Path(normalized["target"]["path"]).expanduser().resolve()
    target_fingerprint = _target_fingerprint(target_path)
    source_structure_map_path = _target_structure_map_path(output_dir, config)
    canonical_structure_map_path = output_dir / TARGET_STRUCTURE_MAP_FILENAME
    structure_map: Dict[str, Any]
    structure_map_reuse = "rebuilt_missing"
    if source_structure_map_path.exists():
        candidate_map = load_structure_map(source_structure_map_path)
        if _structure_map_matches_target(candidate_map, target_path, target_fingerprint, chapter_scope):
            structure_map = candidate_map
            structure_map_reuse = "reused"
        else:
            structure_map = _stamp_target_fingerprint(
                build_paper_structure_map(target_path, llm_config=llm_config, chapter_scope=chapter_scope),
                target_path,
                target_fingerprint,
            )
            structure_map_reuse = "rebuilt_stale"
    else:
        structure_map_reuse = "rebuilt_missing"
        structure_map = build_paper_structure_map(target_path, llm_config=llm_config, chapter_scope=chapter_scope)
        structure_map = _stamp_target_fingerprint(structure_map, target_path, target_fingerprint)
    if structure_map_reuse == "reused":
        structure_map = _stamp_target_fingerprint(structure_map, target_path, target_fingerprint)
    structure_map = filter_structure_map_by_chapter_scope(structure_map, chapter_scope)
    canonical_structure_map_path.write_text(
        json.dumps(structure_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    units_report = build_units_report(structure_map, source_path=str(target_path))
    units_path = output_dir / "target-style-units.json"
    units_path.write_text(json.dumps(units_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "normalized": normalized,
        "outputDir": output_dir,
        "targetPath": target_path,
        "chapterScope": chapter_scope,
        "targetStructureMapPath": canonical_structure_map_path,
        "targetStructureMapSourcePath": str(source_structure_map_path),
        "targetStructureMapReuse": structure_map_reuse,
        "targetFingerprint": target_fingerprint,
        "targetStyleUnitsPath": units_path,
        "targetUnits": units_report["units"],
    }


def run_style_profile_stage(config: Dict[str, Any]) -> Dict[str, Any]:
    normalized = _normalized(config)
    output_dir = Path(normalized["outputDir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    llm_config = normalized.get("llmConfig")
    chapter_scope = normalize_chapter_scope(config.get("chapterScope"))
    ref_map_dir = output_dir / "style-ref-structure-maps"
    ref_map_dir.mkdir(parents=True, exist_ok=True)

    ref_configs = normalized.get("styleProfileRefs") or normalized["refs"]
    if not ref_configs:
        raise ValueError(
            "style profile learning requires refs. "
            "Please provide refs in config, or pass an existing styleProfilePath for target-side review."
        )

    ref_entries: List[Any] = []
    for ref_index, ref_cfg in enumerate(ref_configs, start=1):
        ref_path = Path(ref_cfg["path"]).expanduser().resolve()
        structure_map = build_paper_structure_map(ref_path, llm_config=llm_config, chapter_scope=chapter_scope)
        structure_map = filter_structure_map_by_chapter_scope(structure_map, chapter_scope)
        map_path = ref_map_dir / f"{ref_cfg['id']}.json"
        map_path.write_text(json.dumps(structure_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ref_entries.append(
            SimpleNamespace(
                id=ref_cfg["id"],
                alias=_ref_alias(ref_index),
                path=str(ref_path),
                structureMapPath=str(map_path),
            )
        )

    profile = write_style_profile(ref_entries, output_dir, llm_config=llm_config)
    return {
        "stage": "style_profile",
        "outputDir": str(output_dir),
        "styleProfilePath": str(_style_profile_path(output_dir)),
        "refStyleBasisPath": str(output_dir / REF_STYLE_BASIS_FILENAME),
        "refStructureMapDir": str(ref_map_dir),
        "refCount": len(ref_entries),
        "chapterScope": list(chapter_scope) if chapter_scope is not None else None,
        "chapterScopeLabel": chapter_scope_label(chapter_scope),
        "paragraphTypeCount": profile.get("meta", {}).get("paragraphTypeCount", 0),
    }


def run_style_annotation_stage(config: Dict[str, Any]) -> Dict[str, Any]:
    prepared = prepare_target_style_units(config)
    normalized = prepared["normalized"]
    output_dir = prepared["outputDir"]
    llm_config = normalized.get("llmConfig")
    chapter_scope = prepared["chapterScope"]
    target_path = prepared["targetPath"]
    structure_map_path = prepared["targetStructureMapPath"]
    structure_map_source_path = prepared["targetStructureMapSourcePath"]
    structure_map_reuse = prepared["targetStructureMapReuse"]
    target_units = prepared["targetUnits"]

    style_profile_bundle = load_style_profile_into_output(config, output_dir)
    style_profile_path = Path(style_profile_bundle["styleProfilePath"])
    style_profile = style_profile_bundle["styleProfile"]
    run_fused_target_review(
        output_dir=output_dir,
        target_units=target_units,
        style_profile=style_profile,
        ref_texts=[],
        ref_chapters=[],
        llm_config=llm_config,
        enabled_checks={"terminology": False, "logic": False, "style": True},
    )
    style_result = ensure_style_deviation_report(output_dir, target_path=target_path)
    return {
        "stage": "style_annotation",
        "outputDir": str(output_dir),
        "styleProfilePath": str(style_profile_path),
        "styleProfileSourcePath": style_profile_bundle["styleProfileSourcePath"],
        "targetStructureMapPath": str(structure_map_path),
        "targetStructureMapSourcePath": structure_map_source_path,
        "targetStructureMapReuse": structure_map_reuse,
        "targetFingerprint": prepared["targetFingerprint"],
        "targetStyleUnitsPath": str(output_dir / "target-style-units.json"),
        "styleDeviationPath": str(output_dir / "style-deviation-report.json"),
        "chapterScope": list(chapter_scope) if chapter_scope is not None else None,
        "chapterScopeLabel": chapter_scope_label(chapter_scope),
        "issueCount": len(style_result.get("issues", [])),
    }


def run_annotation_stage(config: Dict[str, Any]) -> Dict[str, Any]:
    normalized = _normalized(config)
    output_dir = Path(normalized["outputDir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(normalized["target"]["path"]).expanduser().resolve()

    anchor_summary = materialize_report_anchors(output_dir, target_path)
    annotations = assemble_annotations(output_dir, enabled_checks=normalized.get("enabledChecks"))
    annotations_path = output_dir / ANNOTATIONS_FILENAME
    write_annotations_json(annotations, annotations_path)

    if target_path.suffix.lower() == ".docx":
        annotated_docx = output_dir / f"{target_path.stem}-annotated.docx"
        from inject_word_comments import inject_comments  # type: ignore

        inject_comments(str(target_path), str(annotations_path), str(annotated_docx))
    else:
        annotated_docx = None

    return {
        "stage": "annotation_export",
        "outputDir": str(output_dir),
        "annotationsPath": str(annotations_path),
        "annotatedDocx": str(annotated_docx) if annotated_docx else None,
        "annotationCount": len(annotations),
        "anchorSummary": anchor_summary,
    }
