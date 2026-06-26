#!/usr/bin/env python3
"""paper-style-review 全量审校编排器。

正式入口分为两类：
- run_review.py --stage all
- style_stage_orchestrator 暴露的独立阶段入口

本模块只负责完整主链编排。
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from document_parser import label_mismatch_risk, parse_document  # type: ignore
from runtime_config import normalize_runtime_config  # type: ignore
from detectors.format_checker import check_docx_format  # type: ignore
from detectors.paragraph_catalog import catalog_paragraphs  # type: ignore
from annotation_assembler import assemble_annotations, write_annotations_json, ensure_style_deviation_report  # type: ignore
from annotation_anchor_infra import materialize_report_anchors  # type: ignore
from fused_review_runtime import run_fused_target_review  # type: ignore
from orchestrators.style_stage_orchestrator import (  # type: ignore
    load_style_profile_into_output,
    prepare_target_style_units,
    run_style_profile_stage,
)


@dataclass
class RefDoc:
    id: str
    alias: str | None
    path: str
    stage: int | None
    enabled: bool
    paragraphs: List[str]
    chapters: List[Dict[str, Any]]
    extractionRisks: List[str]


GENERATED_OUTPUT_FILES = {
    "annotations.json",
    "final-advice.md",
    "fused-review-report.json",
    "format-review-report.json",
    "logic-review-report.json",
    "ref-style-basis.md",
    "run-summary.json",
    "style-review-report.json",
    "style-deviation-report.json",
    "style-profile.json",
    "target-structure-map.json",
    "target-style-units.json",
    "terminology-review-report.json",
}

OPTIONAL_CHECK_KEYS = ("format", "terminology", "style", "logic")


def _load_json_if_exists(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _enabled_checks(config: Dict[str, Any]) -> Dict[str, bool]:
    raw = dict(config.get("enabledChecks") or {})
    return {key: bool(raw.get(key, True)) for key in OPTIONAL_CHECK_KEYS}


def _find_constraint_path(config: Dict[str, Any], key: str, fallback_name: str) -> str | None:
    if config.get(key):
        return config[key]
    constraints = config.get("constraints", {})
    if isinstance(constraints, dict) and constraints.get(key):
        return constraints[key]
    base_dir = Path(config.get("configPath", ".")).parent if config.get("configPath") else None
    if base_dir:
        candidate = base_dir / fallback_name
        if candidate.exists():
            return str(candidate)
    return None


def _cleanup_previous_outputs(output_dir: Path, target_path: Path) -> List[str]:
    removed: List[str] = []
    candidates = {output_dir / name for name in GENERATED_OUTPUT_FILES}
    candidates.add(output_dir / f"{target_path.stem}-annotated.docx")
    for extra_docx in output_dir.glob("*-annotated.docx"):
        candidates.add(extra_docx)
    ref_map_dir = output_dir / "style-ref-structure-maps"
    if ref_map_dir.exists():
        for path in sorted(ref_map_dir.glob("*.json")):
            if path.is_file():
                path.unlink()
                removed.append(str(path.relative_to(output_dir)))
    for path in sorted(candidates):
        if path.exists() and path.is_file():
            path.unlink()
            removed.append(path.name)
    return removed


def _ref_alias(ref_index: int) -> str:
    return f"ref-style-{int(ref_index):02d}"


def _build_ref_docs(ref_configs: List[Dict[str, Any]]) -> List[RefDoc]:
    ref_docs: List[RefDoc] = []
    for ref_index, ref_cfg in enumerate(ref_configs, start=1):
        ref_path = Path(ref_cfg["path"]).expanduser().resolve()
        parsed = parse_document(ref_path)
        alias = _ref_alias(ref_index)
        ref_label = str(ref_cfg.get("label") or ref_cfg.get("id") or "").strip()
        risks = list(parsed.extractionRisks)
        mismatch = label_mismatch_risk(ref_label, str(ref_path), parsed.author) if ref_label else None
        if mismatch:
            risks.append(mismatch)
        paragraphs = [paragraph.text for paragraph in catalog_paragraphs(parsed.chapters)]
        ref_docs.append(
            RefDoc(
                id=ref_cfg["id"],
                alias=alias,
                path=str(ref_path),
                stage=ref_cfg.get("stage"),
                enabled=True,
                paragraphs=paragraphs,
                chapters=list(parsed.chapters),
                extractionRisks=risks,
            )
        )
    return ref_docs


def _build_full_target_text(chapters: List[Dict[str, Any]]) -> str:
    paragraphs = catalog_paragraphs(chapters)
    return "\n".join(p.text for p in paragraphs)


def _append_final_advice(
    output_dir: Path,
    enabled_checks: Dict[str, bool],
    format_result: Dict[str, Any],
    term_result: Dict[str, Any],
    style_result: Dict[str, Any],
    logic_result: Dict[str, Any],
) -> None:
    advice_path = output_dir / "final-advice.md"
    existing = advice_path.read_text(encoding="utf-8") if advice_path.exists() else "# Final Advice\n"
    marker = "\n## 新增格式审校结论\n"
    if marker in existing:
        existing = existing.split(marker, 1)[0].rstrip() + "\n"
    lines = [existing.rstrip(), "", "## 新增格式审校结论", ""]
    if not enabled_checks["format"]:
        lines.append("- 本轮未启用格式检查。")
    elif format_result.get("issues"):
        lines.append(f"- 共发现 {len(format_result['issues'])} 条格式问题，重点集中在：")
        by_type = Counter(issue["checkType"] for issue in format_result["issues"])
        for issue_type, count in by_type.most_common(6):
            lines.append(f"  - {issue_type}: {count}")
    else:
        lines.append("- 当前未发现可结构化识别的格式问题，或目标文件不是 docx。")

    lines.extend(["", "## 新增术语校验结论", ""])
    if not enabled_checks["terminology"]:
        lines.append("- 本轮未启用术语校验。")
    elif term_result.get("issues"):
        lines.append(f"- 共发现 {len(term_result['issues'])} 条术语/中文语境问题。")
        by_type = Counter(issue.get("issueType") or issue.get("severity", "unknown") for issue in term_result["issues"])
        for issue_type, count in by_type.most_common(6):
            lines.append(f"  - {issue_type}: {count}")
    else:
        lines.append("- 当前未发现明显术语问题。")

    lines.extend(["", "## 新增全章节经验检测", ""])
    detector_specs = [
        ("style", "风格模仿偏离", style_result, "deviationType"),
        ("logic", "逻辑通顺", logic_result, "severity"),
    ]
    for check_key, label, result, type_key in detector_specs:
        if not enabled_checks[check_key]:
            lines.append(f"- {label}：本轮未启用。")
            continue
        issues = result.get("issues", [])
        if issues:
            lines.append(f"- {label}：命中 {len(issues)} 条。")
            by_type = Counter(issue.get(type_key) or issue.get("severity") or issue.get("issueType", "unknown") for issue in issues)
            for issue_type, count in by_type.most_common(5):
                lines.append(f"  - {issue_type}: {count}")
        else:
            lines.append(f"- {label}：当前未命中明显问题。")

    advice_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _build_summary(
    output_dir: Path,
    target_path: Path,
    target_doc: Any,
    full_paragraphs: List[Any],
    ref_docs: List[RefDoc],
    format_result: Dict[str, Any],
    term_result: Dict[str, Any],
    style_result: Dict[str, Any],
    logic_result: Dict[str, Any],
    annotations: List[Any],
    annotated_docx: Path | None,
    removed_outputs: List[str],
    enabled_checks: Dict[str, bool],
    notes: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "target": {
            "path": str(target_path),
            "fullParagraphCount": len(full_paragraphs),
        },
        "activeRefs": [
            {
                "id": ref.id,
                "alias": ref.alias,
                "paragraphCount": len(ref.paragraphs),
                "chapterCount": len(ref.chapters),
                "risks": ref.extractionRisks,
            }
            for ref in ref_docs
        ],
        "coverage": {
            "enabledOptionalChecks": enabled_checks,
            "fullCoverageDetectors": [
                detector
                for detector, enabled in [
                    ("format_checker", enabled_checks["format"]),
                    ("fused_target_review:terminology", enabled_checks["terminology"]),
                    ("fused_target_review:logic", enabled_checks["logic"]),
                    ("fused_target_review:style -> style_deviation_report_builder", enabled_checks["style"]),
                ]
                if enabled
            ],
            "fullCoverageNote": "格式检查仅基于格式规范及其固化矩阵；术语/逻辑/风格由 fused review engine 逐段审查；style-deviation 维度由 style-profile 约束下的唯一正式报告构建链路生成。",
        },
        "enhancements": {
            "formatIssueCount": len(format_result.get("issues", [])),
            "terminologyIssueCount": len(term_result.get("issues", [])),
            "styleDeviationCount": len(style_result.get("issues", [])),
            "styleReviewIssueCount": style_result.get("meta", {}).get("styleReviewCount", 0),
            "styleReviewStatus": style_result.get("meta", {}).get("styleReviewStatus"),
            "styleReviewProgress": style_result.get("meta", {}).get("styleReviewProgress", {}),
            "logicIssueCount": len(logic_result.get("issues", [])),
            "totalAnnotations": len(annotations),
            "annotationSourceCounts": dict(Counter(ann.source.value if hasattr(ann.source, 'value') else ann.source for ann in annotations)),
            "annotatedDocx": str(annotated_docx) if annotated_docx else None,
        },
        "cleanup": {
            "removedOldOutputs": removed_outputs,
            "removedCount": len(removed_outputs),
        },
        "outputs": sorted(({p.name for p in output_dir.iterdir() if p.is_file()} | {"run-summary.json"})),
        "notes": notes or [],
    }


def run_review(config: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_runtime_config(config)
    enabled_checks = _enabled_checks(normalized)
    output_dir = Path(normalized["outputDir"]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    target_path = Path(normalized["target"]["path"]).expanduser().resolve()
    removed_outputs = _cleanup_previous_outputs(output_dir, target_path)
    target_doc = parse_document(target_path)
    review_ref_docs = _build_ref_docs(normalized["refs"])
    ref_source_configs = normalized.get("styleProfileRefs") or normalized["refs"]
    ref_docs = _build_ref_docs(ref_source_configs)

    # 全章节段落目录
    full_paragraphs = catalog_paragraphs(target_doc.chapters)

    # 收集参考论文的文本（供 fused review 约束卡片使用）
    ref_texts = []
    ref_chapter_list = []
    ref_docs_for_full_text = review_ref_docs or ref_docs
    for ref in ref_docs_for_full_text:
        ref_texts.extend(ref.paragraphs)
        ref_chapter_list.extend(ref.chapters)

    # LLM 配置
    llm_config = normalized.get("llmConfig", None)

    # 1) 先产出结构化 style-profile + 人类可读 basis
    style_profile: Dict[str, Any] = {}
    style_profile_source_path: str | None = None
    if enabled_checks["style"]:
        explicit_style_profile = str(normalized.get("styleProfilePath") or "").strip()
        if explicit_style_profile:
            style_profile_bundle = load_style_profile_into_output(normalized, output_dir)
            style_profile = style_profile_bundle["styleProfile"]
            style_profile_source_path = style_profile_bundle["styleProfileSourcePath"]
        else:
            style_profile_stage = run_style_profile_stage(normalized)
            style_profile_path = Path(style_profile_stage["styleProfilePath"])
            style_profile = json.loads(style_profile_path.read_text(encoding="utf-8"))
            style_profile_source_path = str(style_profile_path)

    # 2) 格式检查（完全基于 format-rules.json，不再用参考论文 Word 推断）
    format_result: Dict[str, Any] = {}
    if enabled_checks["format"]:
        format_rules_path = _find_constraint_path(normalized, "formatRulesPath", "format-rules.json")
        if not format_rules_path:
            default_rules = Path(__file__).resolve().parents[2] / "references" / "format-rules.json"
            if default_rules.exists():
                format_rules_path = str(default_rules)
        format_result = check_docx_format(target_path, format_rules_path)
        (output_dir / "format-review-report.json").write_text(
            json.dumps(format_result, ensure_ascii=False, indent=2, default=lambda x: dict(x)) + "\n",
            encoding="utf-8",
        )

    # 3) target-side fused LLM review for terminology / logic / style
    if enabled_checks["terminology"] or enabled_checks["logic"] or enabled_checks["style"]:
        prepared_target = prepare_target_style_units(normalized)
        run_fused_target_review(
            output_dir=output_dir,
            target_units=prepared_target["targetUnits"],
            style_profile=style_profile,
            ref_texts=ref_texts,
            ref_chapters=ref_chapter_list,
            llm_config=llm_config,
            enabled_checks={
                "terminology": enabled_checks["terminology"],
                "logic": enabled_checks["logic"],
                "style": enabled_checks["style"],
            },
        )

    term_result: Dict[str, Any] = {}
    if enabled_checks["terminology"]:
        term_result = _load_json_if_exists(output_dir / "terminology-review-report.json")

    # 4) 非 fused 的可选检测器
    logic_result: Dict[str, Any] = {}
    if enabled_checks["logic"]:
        logic_result = _load_json_if_exists(output_dir / "logic-review-report.json")

    style_result: Dict[str, Any] = {}
    if enabled_checks["style"]:
        style_result = ensure_style_deviation_report(output_dir, target_path=target_path)

    # 5) 先把各报告实体化为稳定锚点，再进入汇总/注入阶段。
    anchor_summary = materialize_report_anchors(output_dir, target_path)

    # 6) 扩展 final advice（含新检测器结果）
    _append_final_advice(output_dir, enabled_checks, format_result, term_result, style_result, logic_result)

    # 7) 聚合统一批注 + 注入 docx
    annotations = assemble_annotations(output_dir, enabled_checks=enabled_checks)
    annotations_path = output_dir / "annotations.json"
    write_annotations_json(annotations, annotations_path)

    if target_path.suffix.lower() == ".docx":
        annotated_docx = output_dir / f"{target_path.stem}-annotated.docx"
        from inject_word_comments import inject_comments  # type: ignore
        inject_comments(str(target_path), str(annotations_path), str(annotated_docx))
    else:
        annotated_docx = None

    summary = _build_summary(
        output_dir=output_dir,
        target_path=target_path,
        target_doc=target_doc,
        full_paragraphs=full_paragraphs,
        ref_docs=ref_docs,
        format_result=format_result,
        term_result=term_result,
        style_result=style_result,
        logic_result=logic_result,
        annotations=annotations,
        annotated_docx=annotated_docx,
        removed_outputs=removed_outputs,
        enabled_checks=enabled_checks,
        notes=[
            "统一正式主链：run_review.py -> review_orchestrator.run_review -> format_checker / fused_review_runtime -> annotation_assembler -> inject_word_comments。",
            f"本轮启用的可选检查：{', '.join(key for key, enabled in enabled_checks.items() if enabled)}。",
            f"锚点实体化摘要：{json.dumps(anchor_summary, ensure_ascii=False)}。",
            "target 侧 terminology / logic / style 已收敛到 fused_review_runtime 单一 LLM batch engine；style-deviation-report.json 由唯一的 style-deviation report builder 统一组装。",
            f"style-profile 来源：{style_profile_source_path or 'disabled'}。",
        ],
    )
    (output_dir / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary
