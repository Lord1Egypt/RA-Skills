#!/usr/bin/env python3
"""
统一批注聚合层。

输入：主链输出的正式报告文件（format-review-report.json, terminology-review-report.json, style-deviation-report.json, ...）
输出：统一的 UnifiedAnnotation 列表，用于后续批注注入。
"""
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from annotation_anchor_infra import infer_target_path, materialize_report_anchors
from contracts import (
    ConfidenceLevel,
    DiffType,
    HumanReviewRequired,
    SourceType,
    UnifiedAnnotation,
    normalize_anchor_dict,
)
from style_profile_runtime import lookup_style_basis
from style_prompt_contract import merge_style_suggestion
from style_units_runtime import extract_style_units, load_structure_map


STYLE_DEVIATION_FILENAME = "style-deviation-report.json"
STYLE_REVIEW_FILENAME = "style-review-report.json"
STYLE_PROFILE_FILENAME = "style-profile.json"


def upgrade_reports_with_structured_anchors(output_dir: Path) -> Dict[str, Dict[str, int]]:
    return materialize_report_anchors(output_dir, infer_target_path(output_dir))


def load_format_report(path: Path) -> List[UnifiedAnnotation]:
    """从 format-review-report.json 加载格式问题。优先吃 annotationItems。"""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    annotations = []
    if isinstance(data.get("annotationItems"), list):
        for item in data["annotationItems"]:
            annotations.append(UnifiedAnnotation(
                id=item.get("id", ""),
                source=SourceType(item.get("source", "format")),
                issue_type=item.get("issue_type") or item.get("issueType") or "unknown",
                location_hint=item.get("location_hint") or item.get("locationHint"),
                source_text=item.get("source_text") or item.get("sourceText") or "",
                problem=item.get("problem", ""),
                suggestion=item.get("suggestion", ""),
                basis=item.get("basis", ""),
                risk=item.get("risk", ""),
                human_review_required=HumanReviewRequired(item.get("human_review_required", "recommended")),
                confidence=ConfidenceLevel(item.get("confidence", "medium")),
                severity=item.get("severity", "medium"),
                anchor=normalize_anchor_dict(item.get("anchor")),
            ))
        return annotations
    for issue in data.get("issues", []):
        annotations.append(UnifiedAnnotation.from_format_issue(issue))
    return annotations


def load_terminology_report(path: Path) -> List[UnifiedAnnotation]:
    """从 terminology-review-report.json 加载术语问题。优先吃 annotationItems。"""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    annotations = []
    if isinstance(data.get("annotationItems"), list):
        for item in data["annotationItems"]:
            annotations.append(UnifiedAnnotation(
                id=item.get("id", ""),
                source=SourceType(item.get("source", "terminology")),
                issue_type=item.get("issue_type") or item.get("issueType") or "unknown",
                location_hint=item.get("location_hint") or item.get("locationHint"),
                source_text=item.get("source_text") or item.get("sourceText") or "",
                problem=item.get("problem", ""),
                suggestion=item.get("suggestion", ""),
                basis=item.get("basis", ""),
                risk=item.get("risk", ""),
                human_review_required=HumanReviewRequired(item.get("human_review_required", "recommended")),
                confidence=ConfidenceLevel(item.get("confidence", "medium")),
                severity=item.get("severity", "medium"),
                anchor=normalize_anchor_dict(item.get("anchor")),
                term_issue=item.get("term_issue") or item.get("termIssue"),
            ))
        return annotations
    for issue in data.get("issues", []):
        annotations.append(UnifiedAnnotation.from_term_issue(issue))
    return annotations


def _safe_confidence(value: Any, default: str = "medium") -> ConfidenceLevel:
    raw = getattr(value, "value", value) or default
    try:
        return ConfidenceLevel(raw)
    except Exception:
        return ConfidenceLevel(default)


def _resolve_target_segments(output_dir: Path, target_segments: Optional[List[Any]] = None, target_path: Optional[Path] = None) -> List[Any]:
    if target_segments is not None:
        return list(target_segments)
    units_path = output_dir / "target-style-units.json"
    if units_path.exists():
        data = json.loads(units_path.read_text(encoding="utf-8"))
        units = data.get("units") if isinstance(data, dict) else None
        if isinstance(units, list):
            return units
    structure_map_path = output_dir / "target-structure-map.json"
    if structure_map_path.exists():
        return extract_style_units(load_structure_map(structure_map_path))
    inferred_target = target_path or infer_target_path(output_dir)
    if not inferred_target:
        return []
    return []


def _dedupe_style_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deduped: List[Dict[str, Any]] = []
    seen = set()
    for item in items:
        key = (
            item.get("deviationType") or item.get("issue_type") or item.get("issueType") or "",
            (item.get("locationHint") or item.get("location_hint") or "")[:120],
            (item.get("sourceText") or item.get("source_text") or "")[:160],
            (item.get("problem") or "")[:160],
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _normalize_style_issue(issue: Dict[str, Any], style_profile: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(issue)
    paragraph_type = str(normalized.get("paragraphType") or "").strip()
    deviation_type = str(normalized.get("deviationType") or "general").strip() or "general"
    normalized["basis"] = str(normalized.get("basis") or "").strip() or lookup_style_basis(style_profile, paragraph_type, deviation_type)
    normalized["risk"] = str(normalized.get("risk") or "").strip() or "写作风格与 refs 偏离会削弱整体一致性和风格模仿可信度。"
    normalized["evidenceLayer"] = "fusedStyleReview"
    normalized["sourceArtifact"] = STYLE_REVIEW_FILENAME
    return normalized


def _style_local_suggestion(local_suggestion: str, overall_suggestion: str) -> str:
    local = str(local_suggestion or "").strip()
    overall = str(overall_suggestion or "").strip()
    if local and overall and local != overall:
        return f"{local}\n整体方向：{overall}"
    return local or overall


def _style_diff_type(value: Any) -> DiffType:
    raw = str(value or "~").strip()
    try:
        return DiffType(raw)
    except Exception:
        return DiffType.REPLACE


def _annotation_items_from_style_issue(issue: Dict[str, Any]) -> List[Dict[str, Any]]:
    issue_items = issue.get("issueItems", [])
    if not isinstance(issue_items, list):
        issue_items = []

    annotations: List[Dict[str, Any]] = []
    for idx, issue_item in enumerate(issue_items, start=1):
        if not isinstance(issue_item, dict):
            continue
        sentence_text = str(issue_item.get("sentenceText") or "").strip()
        focus_text = str(issue_item.get("focusText") or "").strip()
        source_text = str(issue_item.get("sourceText") or "").strip() or focus_text or sentence_text or str(issue.get("sourceText") or "").strip()
        if not source_text:
            continue
        deviation_type = str(issue_item.get("deviationType") or issue.get("deviationType") or "general").strip() or "general"
        annotation = UnifiedAnnotation(
            id=f"{issue.get('id', 'style')}-issue-{idx:02d}",
            source=SourceType.STYLE_DEVIATION,
            issue_type=f"style_deviation_{deviation_type}",
            location_hint=issue.get("locationHint", ""),
            source_text=source_text,
            problem=str(issue_item.get("problem") or issue.get("problem") or "").strip(),
            suggestion=_style_local_suggestion(
                str(issue_item.get("suggestion") or "").strip(),
                str(issue.get("suggestion") or "").strip(),
            ),
            basis=issue.get("basis", "对照参考论文风格审查"),
            risk=issue.get("risk", "写作风格与 refs 偏离会削弱整体一致性"),
            human_review_required=HumanReviewRequired.RECOMMENDED,
            confidence=_safe_confidence(issue_item.get("severity") or issue.get("confidence") or issue.get("severity", "medium")),
            severity=str(issue_item.get("severity") or issue.get("severity") or "medium"),
            anchor=normalize_anchor_dict(issue.get("anchor")),
            diff_type=_style_diff_type(issue_item.get("diffType")),
            sentence_text=sentence_text or None,
            focus_text=focus_text or None,
            rewrite_text=str(issue_item.get("rewriteText") or "").strip() or None,
        )
        annotations.append(annotation.to_dict())

    if annotations:
        return annotations
    return [_annotation_from_style_issue(issue)]


def _annotation_from_style_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    annotation = UnifiedAnnotation(
        id=issue.get("id", ""),
        source=SourceType.STYLE_DEVIATION,
        issue_type=f"style_deviation_{issue.get('deviationType', 'general')}",
        location_hint=issue.get("locationHint", ""),
        source_text=issue.get("sourceText", ""),
        problem=issue.get("problem", ""),
        suggestion=merge_style_suggestion(issue),
        basis=issue.get("basis", "对照参考论文风格审查"),
        risk=issue.get("risk", "写作风格与 refs 偏离会削弱整体一致性"),
        human_review_required=HumanReviewRequired.RECOMMENDED,
        confidence=_safe_confidence(issue.get("confidence") or issue.get("severity", "medium")),
        severity=issue.get("severity", "medium"),
        anchor=normalize_anchor_dict(issue.get("anchor")),
        diff_type=_style_diff_type(issue.get("diffType")) if issue.get("diffType") else None,
        sentence_text=issue.get("sentenceText"),
        focus_text=issue.get("focusText"),
        rewrite_text=issue.get("rewriteText"),
    )
    return annotation.to_dict()


def synthesize_style_deviation_report(
    output_dir: Path,
    *,
    target_segments: Optional[List[Any]] = None,
    target_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """正式 style-deviation 组装层：只汇总 style-profile 约束下的 LLM comparator 结果。"""
    style_profile_path = output_dir / STYLE_PROFILE_FILENAME
    style_profile = json.loads(style_profile_path.read_text(encoding="utf-8")) if style_profile_path.exists() else {}
    resolved_segments = _resolve_target_segments(output_dir, target_segments=target_segments, target_path=target_path)

    assembled_path = output_dir / STYLE_DEVIATION_FILENAME
    raw_style_review_path = output_dir / STYLE_REVIEW_FILENAME
    raw_style_review = json.loads(raw_style_review_path.read_text(encoding="utf-8")) if raw_style_review_path.exists() else {}
    style_review_issues = [
        _normalize_style_issue(issue, style_profile)
        for issue in raw_style_review.get("issues", [])
        if isinstance(issue, dict)
    ] if isinstance(raw_style_review, dict) else []
    merged_issues = _dedupe_style_items(style_review_issues)
    merged_annotations: List[Dict[str, Any]] = []
    for issue in merged_issues:
        merged_annotations.extend(_annotation_items_from_style_issue(issue))

    llm_meta = raw_style_review.get("meta", {}) if isinstance(raw_style_review, dict) else {}
    llm_progress = raw_style_review.get("progress", {}) if isinstance(raw_style_review, dict) else {}
    report = {
        "meta": {
            "detector": "style_deviation_report_builder",
            "version": "3.0-llm-comparator-only",
            "method": "canonical style-deviation assembly from style-profile-grounded fused style review only",
            "issueCount": len(merged_issues),
            "styleReviewCount": len(merged_issues),
            "styleReviewStatus": llm_meta.get("runStatus") or ("missing" if not raw_style_review else None),
            "styleReviewProgress": llm_progress,
            "targetSegmentCount": len(resolved_segments),
            "sourceArtifacts": [
                name
                for name, exists in [
                    (STYLE_PROFILE_FILENAME, bool(style_profile)),
                    (STYLE_REVIEW_FILENAME, bool(raw_style_review)),
                ]
                if exists
            ],
        },
        "issues": merged_issues,
        "annotationItems": merged_annotations,
    }
    assembled_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def ensure_style_deviation_report(
    output_dir: Path,
    *,
    target_segments: Optional[List[Any]] = None,
    target_path: Optional[Path] = None,
) -> Dict[str, Any]:
    return synthesize_style_deviation_report(output_dir, target_segments=target_segments, target_path=target_path)


def load_style_deviation_report(path: Path) -> List[UnifiedAnnotation]:
    """从 style-deviation-report.json 加载对 refs 的风格偏离检测结果。优先吃 annotationItems。"""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    annotations = []
    if isinstance(data.get("annotationItems"), list):
        for item in data["annotationItems"]:
            annotations.append(UnifiedAnnotation(
                id=item.get("id", ""),
                source=SourceType(item.get("source", "style_deviation")),
                issue_type=item.get("issue_type") or item.get("issueType") or "style_deviation_general",
                location_hint=item.get("location_hint") or item.get("locationHint"),
                source_text=item.get("source_text") or item.get("sourceText") or "",
                problem=item.get("problem", ""),
                suggestion=item.get("suggestion", ""),
                basis=item.get("basis", "对照参考论文风格审查"),
                risk=item.get("risk", "写作风格与 refs 偏离会削弱整体一致性"),
                human_review_required=HumanReviewRequired(item.get("human_review_required", "recommended")),
                confidence=_safe_confidence(item.get("confidence", "medium")),
                severity=item.get("severity", "medium"),
                anchor=normalize_anchor_dict(item.get("anchor")),
                diff_type=_style_diff_type(item.get("diff_type") or item.get("diffType")) if (item.get("diff_type") or item.get("diffType")) else None,
                sentence_text=item.get("sentence_text") or item.get("sentenceText"),
                focus_text=item.get("focus_text") or item.get("focusText"),
                rewrite_text=item.get("rewrite_text") or item.get("rewriteText"),
            ))
        return annotations
    for issue in data.get("issues", []):
        annotations.append(UnifiedAnnotation(
            id=issue.get("id", f"style-{len(annotations)}"),
            source=SourceType.STYLE_DEVIATION,
            issue_type=f"style_deviation_{issue.get('deviationType', 'general')}",
            location_hint=issue.get("locationHint", ""),
            source_text=issue.get("sourceText", ""),
            problem=issue.get("problem", ""),
            suggestion=merge_style_suggestion(issue),
            basis=issue.get("basis", "对照参考论文风格审查"),
            risk=issue.get("risk", "写作风格与 refs 偏离会削弱整体一致性"),
            human_review_required=HumanReviewRequired.RECOMMENDED,
            confidence=_safe_confidence(issue.get("confidence") or issue.get("severity", "medium")),
            severity=issue.get("severity", "medium"),
            anchor=normalize_anchor_dict(issue.get("anchor")),
            diff_type=_style_diff_type(issue.get("diffType")) if issue.get("diffType") else None,
            sentence_text=issue.get("sentenceText"),
            focus_text=issue.get("focusText"),
            rewrite_text=issue.get("rewriteText"),
        ))
    return annotations


def load_logic_report(path: Path) -> List[UnifiedAnnotation]:
    """从 logic-review-report.json 加载逻辑问题。优先吃 annotationItems。"""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    annotations = []
    if isinstance(data.get("annotationItems"), list):
        for item in data["annotationItems"]:
            annotations.append(UnifiedAnnotation(
                id=item.get("id", ""),
                source=SourceType(item.get("source", "logic")),
                issue_type=item.get("issue_type") or item.get("issueType") or "logic_coherence",
                location_hint=item.get("location_hint") or item.get("locationHint"),
                source_text=item.get("source_text") or item.get("sourceText") or "",
                problem=item.get("problem", ""),
                suggestion=item.get("suggestion", ""),
                basis=item.get("basis", "基于通用逻辑通顺规则"),
                risk=item.get("risk", "逻辑跳步可能导致读者困惑"),
                human_review_required=HumanReviewRequired(item.get("human_review_required", "recommended")),
                confidence=ConfidenceLevel(item.get("confidence", "medium")),
                severity=item.get("severity", "medium"),
                anchor=normalize_anchor_dict(item.get("anchor")),
            ))
        return annotations
    for issue in data.get("issues", []):
        annotations.append(UnifiedAnnotation(
            id=issue.get("id", f"logic-{len(annotations)}"),
            source=SourceType.LOGIC,
            issue_type=issue.get("issueType", "logic_coherence"),
            location_hint=issue.get("locationHint", ""),
            source_text=issue.get("sourceText", ""),
            problem=issue.get("problem", ""),
            suggestion=issue.get("suggestion", ""),
            basis=issue.get("basis", "基于通用逻辑通顺规则"),
            risk=issue.get("risk", "逻辑跳步可能导致读者困惑"),
            human_review_required=HumanReviewRequired.RECOMMENDED,
            confidence=ConfidenceLevel(issue.get("confidence", "medium")),
            severity="medium",
            anchor=normalize_anchor_dict(issue.get("anchor")),
        ))
    return annotations


def deduplicate_annotations(annotations: List[UnifiedAnnotation]) -> List[UnifiedAnnotation]:
    """只去掉真正重复的批注，不能把不同来源/不同位置的问题吞掉。"""
    seen = defaultdict(list)
    for ann in annotations:
        key = (
            ann.source.value if hasattr(ann.source, 'value') else str(ann.source),
            ann.issue_type,
            (ann.location_hint or "")[:120],
            (ann.source_text or "")[:160],
            (ann.problem or "")[:160],
        )
        seen[key].append(ann)

    deduped = []
    severity_rank = {"low": 1, "medium": 2, "high": 3}
    confidence_rank = {"low": 1, "medium": 2, "high": 3}
    for _, group in seen.items():
        group.sort(
            key=lambda x: (
                confidence_rank.get(getattr(x.confidence, 'value', str(x.confidence)), 0),
                severity_rank.get(x.severity, 0),
                len(x.suggestion or ""),
            ),
            reverse=True,
        )
        deduped.append(group[0])
    return deduped


def _is_enabled(enabled_checks: Optional[Dict[str, bool]], key: str, default: bool = True) -> bool:
    if enabled_checks is None:
        return default
    return bool(enabled_checks.get(key, default))


def assemble_annotations(output_dir: Path, enabled_checks: Optional[Dict[str, bool]] = None) -> List[UnifiedAnnotation]:
    """从 output_dir 下的各类报告文件中聚合批注。"""
    all_annotations = []

    # 主链保证报告已完成锚点实体化；这里只做纯聚合。
    style_dev_path = output_dir / STYLE_DEVIATION_FILENAME

    # 格式问题
    format_path = output_dir / "format-review-report.json"
    if _is_enabled(enabled_checks, "format") and format_path.exists():
        all_annotations.extend(load_format_report(format_path))

    # 术语问题
    term_path = output_dir / "terminology-review-report.json"
    if _is_enabled(enabled_checks, "terminology") and term_path.exists():
        all_annotations.extend(load_terminology_report(term_path))

    # 风格偏离：只消费 orchestrator 已落盘的正式报告
    if _is_enabled(enabled_checks, "style") and style_dev_path.exists():
        all_annotations.extend(load_style_deviation_report(style_dev_path))

    logic_path = output_dir / "logic-review-report.json"
    if _is_enabled(enabled_checks, "logic") and logic_path.exists():
        all_annotations.extend(load_logic_report(logic_path))
    
    # 去重
    deduped = deduplicate_annotations(all_annotations)
    # 按位置排序（粗略按 location_hint）
    deduped.sort(key=lambda x: x.location_hint or "")
    
    return deduped


def write_annotations_json(annotations: List[UnifiedAnnotation], output_path: Path) -> None:
    """将 UnifiedAnnotation 列表写入 JSON 文件"""
    data = [ann.to_dict() for ann in annotations]
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="聚合各检测器报告为统一批注文件")
    parser.add_argument("--output-dir", required=True, help="包含各类报告文件的输出目录")
    parser.add_argument("--out", default="annotations.json", help="输出统一批注文件路径")
    parser.add_argument("--enable-checks", default="", help="逗号分隔的启用检查项，如 format,logic,style")
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    materialize_report_anchors(output_dir, infer_target_path(output_dir))
    enabled_checks = None
    if args.enable_checks.strip():
        enabled_checks = {
            "format": False,
            "terminology": False,
            "style": False,
            "logic": False,
        }
        for raw in args.enable_checks.split(","):
            key = raw.strip()
            if key:
                enabled_checks[key] = True
    annotations = assemble_annotations(output_dir, enabled_checks=enabled_checks)
    out_path = output_dir / args.out if not Path(args.out).is_absolute() else Path(args.out)
    write_annotations_json(annotations, out_path)
    print(f"聚合完成，共 {len(annotations)} 条批注，已写入 {out_path}")


if __name__ == "__main__":
    main()
