#!/usr/bin/env python3
"""Unified target-review LLM runtime.

Single mainline for target-side LLM review:
- batch paragraphs by local section scope;
- derive compact style-profile slices at runtime;
- call one fused LLM review per batch for terminology / logic / style;
- split fused results back into canonical report files consumed downstream.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from contracts import ConfidenceLevel, DiffType, HumanReviewRequired, SourceType, UnifiedAnnotation, normalize_anchor_dict
from llm_client import check_fused_review_batch
from style_profile_runtime import build_style_profile_slice, lookup_style_basis
from style_prompt_contract import STYLE_PROMPT_PROFILE_VERSION


FUSED_REVIEW_FILENAME = "fused-review-report.json"
TERMINOLOGY_REPORT_FILENAME = "terminology-review-report.json"
LOGIC_REPORT_FILENAME = "logic-review-report.json"
STYLE_REVIEW_FILENAME = "style-review-report.json"
FUSED_REVIEW_RUNTIME_VERSION = "1.1-target-fused-review-input-signature"
FUSED_REVIEW_INPUT_SIGNATURE_VERSION = "fused-review-input-signature-v1"


def _cfg_int(cfg: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int((cfg or {}).get(key, default))
    except Exception:
        return default


def _cfg_bool(cfg: Dict[str, Any], key: str, default: bool) -> bool:
    value = (cfg or {}).get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off", ""}
    return bool(value)


def _stable_json_hash(payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _chapter_scope_for_unit(unit: Dict[str, Any]) -> str:
    section_path = str(unit.get("sectionPath") or "").strip()
    chapter_title = str(unit.get("chapterTitle") or "").strip()
    return section_path or chapter_title or "unknown"


def _batch_limits_for_scope(scope_text: str) -> Tuple[int, int]:
    lowered = scope_text.lower()
    if "摘要" in scope_text or "abstract" in lowered or "第1章" in scope_text:
        return 3, 1800
    return 5, 2400


def _unit_payload(unit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "paragraphId": str(unit.get("paragraphId") or "").strip(),
        "paragraphType": str(unit.get("paragraphType") or "").strip(),
        "sectionPath": str(unit.get("sectionPath") or "").strip(),
        "chapterTitle": str(unit.get("chapterTitle") or "").strip(),
        "locationHint": str(unit.get("locationHint") or "").strip(),
        "text": str(unit.get("text") or "").strip(),
    }


def build_fused_review_batches(target_units: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    batches: List[Dict[str, Any]] = []
    current_items: List[Dict[str, Any]] = []
    current_scope = ""
    current_chars = 0
    batch_no = 0

    def flush() -> None:
        nonlocal batch_no, current_items, current_scope, current_chars
        if not current_items:
            return
        batch_no += 1
        section_path = str(current_items[0].get("sectionPath") or "").strip()
        chapter_title = str(current_items[0].get("chapterTitle") or "").strip()
        batches.append(
            {
                "batchId": f"fused-batch-{batch_no:04d}",
                "sectionPath": section_path,
                "chapterTitle": chapter_title,
                "paragraphs": list(current_items),
            }
        )
        current_items = []
        current_scope = ""
        current_chars = 0

    for unit in target_units:
        paragraph = _unit_payload(unit)
        text = paragraph["text"]
        if not text:
            continue
        scope_text = _chapter_scope_for_unit(unit)
        max_paragraphs, max_chars = _batch_limits_for_scope(scope_text)
        paragraph_chars = len(text)
        if current_items:
            scope_changed = scope_text != current_scope
            would_overflow = len(current_items) >= max_paragraphs or (current_chars + paragraph_chars) > max_chars
            if scope_changed or would_overflow:
                flush()
        if not current_items:
            current_scope = scope_text
        current_items.append(paragraph)
        current_chars += paragraph_chars
    flush()
    return batches


def _batch_signature_payload(
    batch: Dict[str, Any],
    *,
    enabled_checks: Dict[str, bool],
    style_profiles_by_type: Dict[str, Any],
    term_policy: Dict[str, Any],
    logic_reference: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "signatureVersion": FUSED_REVIEW_INPUT_SIGNATURE_VERSION,
        "stylePromptProfileVersion": STYLE_PROMPT_PROFILE_VERSION,
        "enabledChecks": {
            "terminology": bool(enabled_checks.get("terminology", False)),
            "logic": bool(enabled_checks.get("logic", False)),
            "style": bool(enabled_checks.get("style", False)),
        },
        "batchMeta": {
            "batchId": str(batch.get("batchId") or ""),
            "sectionPath": str(batch.get("sectionPath") or ""),
            "chapterTitle": str(batch.get("chapterTitle") or ""),
            "paragraphCount": len(batch.get("paragraphs") or []),
        },
        "paragraphs": list(batch.get("paragraphs") or []),
        "styleProfilesByType": style_profiles_by_type or {},
        "termPolicy": term_policy or {},
        "logicReference": logic_reference or {},
    }


def _build_batch_plan(
    batches: List[Dict[str, Any]],
    *,
    style_profile: Dict[str, Any],
    enabled_checks: Dict[str, bool],
    term_policy: Dict[str, Any],
    logic_reference: Dict[str, Any],
) -> List[Dict[str, Any]]:
    plans: List[Dict[str, Any]] = []
    for batch in batches:
        paragraph_types = [paragraph.get("paragraphType", "") for paragraph in batch.get("paragraphs", [])]
        style_slice = build_style_profile_slice(style_profile or {}, paragraph_types)
        signature_payload = _batch_signature_payload(
            batch,
            enabled_checks=enabled_checks,
            style_profiles_by_type=style_slice.get("profiles", {}),
            term_policy=term_policy,
            logic_reference=logic_reference,
        )
        plans.append(
            {
                "batch": batch,
                "styleSlice": style_slice,
                "signature": _stable_json_hash(signature_payload),
                "signaturePayload": signature_payload,
            }
        )
    return plans


def _build_run_input_signature(
    batch_plan: List[Dict[str, Any]],
    *,
    enabled_checks: Dict[str, bool],
) -> Dict[str, Any]:
    batch_signatures = {
        str(plan["batch"].get("batchId") or ""): str(plan.get("signature") or "")
        for plan in batch_plan
    }
    payload = {
        "signatureVersion": FUSED_REVIEW_INPUT_SIGNATURE_VERSION,
        "stylePromptProfileVersion": STYLE_PROMPT_PROFILE_VERSION,
        "enabledChecks": {
            "terminology": bool(enabled_checks.get("terminology", False)),
            "logic": bool(enabled_checks.get("logic", False)),
            "style": bool(enabled_checks.get("style", False)),
        },
        "batchSignatures": batch_signatures,
    }
    return {
        "version": FUSED_REVIEW_INPUT_SIGNATURE_VERSION,
        "sha256": _stable_json_hash(payload),
        "batchSignatures": batch_signatures,
    }


def _truncate_samples(texts: Iterable[str], *, max_items: int, max_chars: int) -> List[str]:
    items: List[str] = []
    total = 0
    for text in texts:
        value = str(text or "").strip()
        if not value:
            continue
        clipped = value[:140]
        if total + len(clipped) > max_chars and items:
            break
        items.append(clipped)
        total += len(clipped)
        if len(items) >= max_items:
            break
    return items


def build_term_policy_card(ref_texts: List[str]) -> Dict[str, Any]:
    return {
        "principles": [
            "Prefer standard Chinese academic terminology and avoid coined mixed compounds.",
            "Flag weak Chinese context, jargon-like marketing phrasing, and suspicious translationese.",
            "Do not flag stable technical abbreviations unless they lack Chinese anchoring or are contextually unstable.",
        ],
        "referenceUsageSamples": _truncate_samples(ref_texts, max_items=6, max_chars=700),
    }


def build_logic_reference_card(ref_chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
    sections: List[Dict[str, Any]] = []
    for chapter in ref_chapters[:3]:
        title = str(chapter.get("title") or "").strip()
        items = chapter.get("items", chapter.get("paragraphs", chapter.get("blocks", [])))
        samples: List[str] = []
        for item in items:
            if isinstance(item, dict):
                item_type = str(item.get("type") or "").strip()
                text = str(item.get("text") or "").strip()
            else:
                item_type = getattr(item, "type", "")
                text = str(getattr(item, "text", item) or "").strip()
            if item_type == "heading" or len(text) < 20:
                continue
            samples.append(text[:140])
            if len(samples) >= 3:
                break
        if title and samples:
            sections.append({"title": title, "samples": samples})
    return {"referenceSections": sections}


def _paragraph_lookup(target_units: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    for unit in target_units:
        paragraph_id = str(unit.get("paragraphId") or "").strip()
        if paragraph_id:
            lookup[paragraph_id] = unit
    return lookup


def _severity_rank(value: Any) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get(str(value or "").strip().lower(), 0)


def _safe_confidence(value: Any, default: str = "medium") -> ConfidenceLevel:
    raw = getattr(value, "value", value) or default
    try:
        return ConfidenceLevel(raw)
    except Exception:
        return ConfidenceLevel(default)


def _safe_diff_type(value: Any, default: DiffType = DiffType.REPLACE) -> DiffType:
    raw = getattr(value, "value", value) or default.value
    try:
        return DiffType(str(raw))
    except Exception:
        return default


def _normalize_terminology_issue(issue: Dict[str, Any], paragraph_lookup: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    paragraph_id = str(issue.get("paragraphId") or "").strip()
    paragraph = paragraph_lookup.get(paragraph_id)
    if not paragraph:
        return None
    return {
        "paragraphId": paragraph_id,
        "chapter": paragraph.get("chapterTitle", ""),
        "locationHint": paragraph.get("locationHint", ""),
        "term": str(issue.get("term") or "").strip(),
        "issueType": str(issue.get("issueType") or "external_verification_candidate").strip() or "external_verification_candidate",
        "sentenceText": str(issue.get("sentenceText") or "").strip(),
        "focusText": str(issue.get("focusText") or "").strip(),
        "sourceText": str(issue.get("focusText") or issue.get("sentenceText") or "").strip(),
        "problem": str(issue.get("problem") or "").strip(),
        "suggestion": str(issue.get("suggestion") or "").strip(),
        "severity": str(issue.get("severity") or "medium").strip().lower() or "medium",
        "anchor": normalize_anchor_dict(paragraph.get("anchor")),
    }


def _normalize_logic_issue(issue: Dict[str, Any], paragraph_lookup: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    paragraph_id = str(issue.get("paragraphId") or "").strip()
    paragraph = paragraph_lookup.get(paragraph_id)
    if not paragraph:
        return None
    related_paragraph_id = str(issue.get("relatedParagraphId") or "").strip()
    return {
        "paragraphId": paragraph_id,
        "relatedParagraphId": related_paragraph_id,
        "scope": str(issue.get("scope") or "paragraph").strip() or "paragraph",
        "chapter": paragraph.get("chapterTitle", ""),
        "locationHint": paragraph.get("locationHint", ""),
        "sentenceText": str(issue.get("sentenceText") or "").strip(),
        "focusText": str(issue.get("focusText") or "").strip(),
        "sourceText": str(issue.get("focusText") or issue.get("sentenceText") or "").strip(),
        "problem": str(issue.get("problem") or "").strip(),
        "suggestion": str(issue.get("suggestion") or "").strip(),
        "severity": str(issue.get("severity") or "medium").strip().lower() or "medium",
        "anchor": normalize_anchor_dict(paragraph.get("anchor")),
    }


def _normalize_style_issue(
    issue: Dict[str, Any],
    paragraph_lookup: Dict[str, Dict[str, Any]],
    style_profile: Dict[str, Any],
    batch_id: str,
) -> Optional[Dict[str, Any]]:
    paragraph_id = str(issue.get("paragraphId") or "").strip()
    paragraph = paragraph_lookup.get(paragraph_id)
    if not paragraph:
        return None
    paragraph_type = str(issue.get("paragraphType") or paragraph.get("paragraphType") or "").strip()
    deviation_type = str(issue.get("deviationType") or "general").strip() or "general"
    return {
        "paragraphId": paragraph_id,
        "paragraphType": paragraph_type,
        "chapter": paragraph.get("chapterTitle", ""),
        "locationHint": paragraph.get("locationHint", ""),
        "sourceText": str(issue.get("sourceText") or issue.get("focusText") or issue.get("sentenceText") or "").strip(),
        "sentenceText": str(issue.get("sentenceText") or "").strip(),
        "focusText": str(issue.get("focusText") or "").strip(),
        "problem": str(issue.get("problem") or "").strip(),
        "suggestion": str(issue.get("suggestion") or "").strip(),
        "rewriteText": str(issue.get("rewriteText") or "").strip(),
        "diffType": str(issue.get("diffType") or "~").strip() or "~",
        "severity": str(issue.get("severity") or "medium").strip().lower() or "medium",
        "deviationType": deviation_type,
        "basis": lookup_style_basis(style_profile, paragraph_type, deviation_type),
        "risk": "写作风格与 refs 偏离会削弱整体一致性和风格模仿可信度。",
        "evidenceLayer": "fusedReview",
        "sourceArtifact": FUSED_REVIEW_FILENAME,
        "stylePromptProfile": STYLE_PROMPT_PROFILE_VERSION,
        "batchId": batch_id,
        "anchor": normalize_anchor_dict(paragraph.get("anchor")),
    }


def _dedupe_issues(items: List[Dict[str, Any]], key_fields: List[str]) -> List[Dict[str, Any]]:
    seen = set()
    output: List[Dict[str, Any]] = []
    for item in items:
        key = tuple(str(item.get(field) or "") for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def _build_terminology_report(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    deduped = _dedupe_issues(issues, ["paragraphId", "term", "issueType", "problem", "sourceText"])
    annotation_items: List[Dict[str, Any]] = []
    for idx, issue in enumerate(deduped, start=1):
        annotation_items.append(
            UnifiedAnnotation(
                id=f"term-{idx:04d}",
                source=SourceType.TERMINOLOGY,
                issue_type=issue.get("issueType", "external_verification_candidate"),
                location_hint=issue.get("locationHint", ""),
                source_text=issue.get("sourceText", ""),
                problem=issue.get("problem", ""),
                suggestion=issue.get("suggestion", ""),
                basis="Fused AI terminology review",
                risk="术语不规范或中文语境不稳，会削弱论文的学术严谨性与专业表达。",
                human_review_required=HumanReviewRequired.RECOMMENDED,
                confidence=_safe_confidence(issue.get("severity", "medium")),
                severity=issue.get("severity", "medium"),
                anchor=issue.get("anchor"),
                term_issue=issue.get("term"),
                sentence_text=issue.get("sentenceText"),
                focus_text=issue.get("focusText"),
            ).to_dict()
        )
    return {
        "meta": {
            "detector": "fused_terminology_review",
            "version": "3.0-fused-target-review",
            "method": "Fused LLM target review terminology branch",
            "issueCount": len(deduped),
        },
        "issues": deduped,
        "annotationItems": annotation_items,
    }


def _build_logic_report(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    deduped = _dedupe_issues(issues, ["paragraphId", "scope", "problem", "sourceText"])
    annotation_items: List[Dict[str, Any]] = []
    for idx, issue in enumerate(deduped, start=1):
        annotation_items.append(
            UnifiedAnnotation(
                id=f"logic-{idx:04d}",
                source=SourceType.LOGIC,
                issue_type="logic_coherence",
                location_hint=issue.get("locationHint", ""),
                source_text=issue.get("sourceText", ""),
                problem=issue.get("problem", ""),
                suggestion=issue.get("suggestion", ""),
                basis="Fused AI logic review",
                risk="逻辑不通顺会影响论证的说服力和可信度",
                human_review_required=HumanReviewRequired.RECOMMENDED,
                confidence=_safe_confidence(issue.get("severity", "medium")),
                severity=issue.get("severity", "medium"),
                anchor=issue.get("anchor"),
                sentence_text=issue.get("sentenceText"),
                focus_text=issue.get("focusText"),
            ).to_dict()
        )
    return {
        "meta": {
            "detector": "fused_logic_review",
            "version": "3.0-fused-target-review",
            "method": "Fused LLM target review logic branch",
            "issueCount": len(deduped),
        },
        "issues": deduped,
        "annotationItems": annotation_items,
    }


def _build_style_review_report(
    style_issues: List[Dict[str, Any]],
    paragraph_lookup: Dict[str, Dict[str, Any]],
    *,
    run_status: str,
    completed_batch_ids: List[str],
    pending_batch_ids: List[str],
    errors: List[Dict[str, Any]],
) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for issue in style_issues:
        paragraph_id = str(issue.get("paragraphId") or "").strip()
        if paragraph_id:
            grouped.setdefault(paragraph_id, []).append(issue)

    report_issues: List[Dict[str, Any]] = []
    annotation_items: List[Dict[str, Any]] = []
    for group_no, (paragraph_id, issues) in enumerate(grouped.items(), start=1):
        paragraph = paragraph_lookup.get(paragraph_id) or {}
        issues_sorted = sorted(issues, key=lambda item: (-_severity_rank(item.get("severity")), item.get("sentenceText", "")))
        severity = issues_sorted[0].get("severity", "medium") if issues_sorted else "medium"
        deviation_types: List[str] = []
        for item in issues_sorted:
            deviation = str(item.get("deviationType") or "general").strip() or "general"
            if deviation not in deviation_types:
                deviation_types.append(deviation)
        grouped_issue = {
            "id": f"style-fused-{group_no:04d}",
            "paragraphId": paragraph_id,
            "paragraphType": paragraph.get("paragraphType", ""),
            "chapter": paragraph.get("chapterTitle", ""),
            "locationHint": paragraph.get("locationHint", ""),
            "sourceText": issues_sorted[0].get("sourceText", "") if issues_sorted else "",
            "problem": "；".join(item.get("problem", "") for item in issues_sorted if item.get("problem"))[:320],
            "suggestion": "；".join(item.get("suggestion", "") for item in issues_sorted if item.get("suggestion"))[:260],
            "severity": severity,
            "deviationType": deviation_types[0] if len(deviation_types) == 1 else "multiple",
            "issueItems": [
                {
                    "sentenceText": item.get("sentenceText", ""),
                    "focusText": item.get("focusText", ""),
                    "sourceText": item.get("sourceText", ""),
                    "problem": item.get("problem", ""),
                    "suggestion": item.get("suggestion", ""),
                    "rewriteText": item.get("rewriteText", ""),
                    "diffType": item.get("diffType", "~"),
                    "expectedProfileEvidence": [],
                    "observedTextEvidence": [],
                    "missingAnchors": [],
                    "violatedSequence": [],
                    "hitAvoidPatterns": [],
                    "severity": item.get("severity", "medium"),
                    "deviationType": item.get("deviationType", "general"),
                }
                for item in issues_sorted
            ],
            "basis": issues_sorted[0].get("basis", "") if issues_sorted else "",
            "risk": issues_sorted[0].get("risk", "") if issues_sorted else "",
            "stylePromptProfile": STYLE_PROMPT_PROFILE_VERSION,
            "sourceArtifact": FUSED_REVIEW_FILENAME,
            "anchor": normalize_anchor_dict(paragraph.get("anchor")),
        }
        report_issues.append(grouped_issue)
        annotation_items.append(
            UnifiedAnnotation(
                id=grouped_issue["id"],
                source=SourceType.STYLE_DEVIATION,
                issue_type=f"style_deviation_{grouped_issue['deviationType']}",
                location_hint=grouped_issue.get("locationHint", ""),
                source_text=grouped_issue.get("sourceText", ""),
                problem=grouped_issue.get("problem", ""),
                suggestion=grouped_issue.get("suggestion", ""),
                basis=grouped_issue.get("basis", ""),
                risk=grouped_issue.get("risk", ""),
                human_review_required=HumanReviewRequired.RECOMMENDED,
                confidence=_safe_confidence(grouped_issue.get("severity", "medium")),
                severity=grouped_issue.get("severity", "medium"),
                anchor=grouped_issue.get("anchor"),
            ).to_dict()
        )

    return {
        "meta": {
            "detector": "fused_style_review",
            "version": "6.0-fused-target-review",
            "method": "Fused LLM target review style branch aligned by paragraphType style slices",
            "stylePromptProfile": STYLE_PROMPT_PROFILE_VERSION,
            "issueCount": len(report_issues),
            "checkedParagraphCount": len(grouped),
            "completedBatchCount": len(completed_batch_ids),
            "pendingBatchCount": len(pending_batch_ids),
            "runStatus": run_status,
            "sourceArtifact": FUSED_REVIEW_FILENAME,
            "errors": errors,
        },
        "progress": {
            "batchSize": 1,
            "completedBatches": completed_batch_ids,
            "pendingBatches": pending_batch_ids,
            "nextBatchId": pending_batch_ids[0] if pending_batch_ids else None,
        },
        "issues": report_issues,
        "annotationItems": annotation_items,
    }


def _materialize_reports(
    *,
    output_dir: Path,
    terminology_issues: List[Dict[str, Any]],
    logic_issues: List[Dict[str, Any]],
    style_issues: List[Dict[str, Any]],
    paragraph_lookup: Dict[str, Dict[str, Any]],
    run_status: str,
    completed_batch_ids: List[str],
    pending_batch_ids: List[str],
    errors: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    term_report = _build_terminology_report(terminology_issues)
    logic_report = _build_logic_report(logic_issues)
    style_report = _build_style_review_report(
        style_issues,
        paragraph_lookup,
        run_status=run_status,
        completed_batch_ids=completed_batch_ids,
        pending_batch_ids=pending_batch_ids,
        errors=errors,
    )
    (output_dir / TERMINOLOGY_REPORT_FILENAME).write_text(json.dumps(term_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / LOGIC_REPORT_FILENAME).write_text(json.dumps(logic_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / STYLE_REVIEW_FILENAME).write_text(json.dumps(style_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "terminology": term_report,
        "logic": logic_report,
        "styleReview": style_report,
    }


def _load_existing_report(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _materialize_fused_report(
    *,
    output_path: Path,
    batches: List[Dict[str, Any]],
    batch_results: List[Dict[str, Any]],
    completed_batch_ids: List[str],
    errors: List[Dict[str, Any]],
    input_signature: Dict[str, Any],
) -> Dict[str, Any]:
    pending = [batch["batchId"] for batch in batches if batch["batchId"] not in completed_batch_ids]
    report = {
        "meta": {
            "module": "fused_review_runtime",
            "version": FUSED_REVIEW_RUNTIME_VERSION,
            "batchCount": len(batches),
            "completedBatchCount": len(completed_batch_ids),
            "pendingBatchCount": len(pending),
            "runStatus": "completed" if not pending else ("partial" if completed_batch_ids else "blocked"),
            "errors": errors,
            "inputSignature": input_signature,
        },
        "progress": {
            "completedBatches": completed_batch_ids,
            "pendingBatches": pending,
            "nextBatchId": pending[0] if pending else None,
        },
        "batches": batch_results,
    }
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def run_fused_target_review(
    *,
    output_dir: Path,
    target_units: List[Dict[str, Any]],
    style_profile: Optional[Dict[str, Any]],
    ref_texts: Optional[List[str]],
    ref_chapters: Optional[List[Dict[str, Any]]],
    llm_config: Optional[Dict[str, Any]],
    enabled_checks: Dict[str, bool],
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cfg = dict(llm_config or {})
    style_only_mode = bool(enabled_checks.get("style")) and not bool(enabled_checks.get("terminology")) and not bool(enabled_checks.get("logic"))
    output_path = output_dir / FUSED_REVIEW_FILENAME
    paragraph_lookup = _paragraph_lookup(target_units)
    batches = build_fused_review_batches(target_units)
    normalized_enabled_checks = {
        "terminology": bool(enabled_checks.get("terminology", False)),
        "logic": bool(enabled_checks.get("logic", False)),
        "style": bool(enabled_checks.get("style", False)),
    }
    term_policy = build_term_policy_card(ref_texts or [])
    logic_reference = build_logic_reference_card(ref_chapters or [])
    batch_plan = _build_batch_plan(
        batches,
        style_profile=style_profile or {},
        enabled_checks=normalized_enabled_checks,
        term_policy=term_policy,
        logic_reference=logic_reference,
    )
    input_signature = _build_run_input_signature(
        batch_plan,
        enabled_checks=normalized_enabled_checks,
    )

    resume_enabled = _cfg_bool(
        cfg,
        "fusedResume",
        _cfg_bool(cfg, "styleResume", True) if style_only_mode else True,
    )
    stop_on_error = _cfg_bool(
        cfg,
        "fusedStopOnError",
        _cfg_bool(cfg, "styleStopOnError", True) if style_only_mode else True,
    )
    max_batches = _cfg_int(
        cfg,
        "fusedMaxBatches",
        _cfg_int(cfg, "styleMaxBatches", 0) if style_only_mode else 0,
    )

    existing = _load_existing_report(output_path) if resume_enabled else {}
    existing_signature = ((existing.get("meta") or {}).get("inputSignature") or {}) if isinstance(existing, dict) else {}
    existing_signature_sha = str(existing_signature.get("sha256") or "").strip()
    current_signature_sha = str(input_signature.get("sha256") or "").strip()
    if not current_signature_sha or existing_signature_sha != current_signature_sha:
        existing = {}
    existing_batches = existing.get("batches", []) if isinstance(existing.get("batches"), list) else []
    batch_results = [item for item in existing_batches if isinstance(item, dict)]
    completed_batch_ids = list(existing.get("progress", {}).get("completedBatches", [])) if isinstance(existing.get("progress"), dict) else []
    errors = list(existing.get("meta", {}).get("errors", [])) if isinstance(existing.get("meta", {}).get("errors"), list) else []

    processed_this_run = 0

    for plan in batch_plan:
        batch = plan["batch"]
        batch_id = batch["batchId"]
        if batch_id in completed_batch_ids:
            continue
        if max_batches and processed_this_run >= max_batches:
            break
        style_slice = plan["styleSlice"]
        try:
            result = check_fused_review_batch(
                batch_meta={
                    "batchId": batch_id,
                    "sectionPath": batch.get("sectionPath", ""),
                    "chapterTitle": batch.get("chapterTitle", ""),
                    "paragraphCount": len(batch["paragraphs"]),
                },
                enabled_checks={
                    "terminology": normalized_enabled_checks["terminology"],
                    "logic": normalized_enabled_checks["logic"],
                    "style": normalized_enabled_checks["style"],
                },
                paragraphs=batch["paragraphs"],
                style_profiles_by_type=style_slice.get("profiles", {}),
                term_policy=term_policy,
                logic_reference=logic_reference,
                config=cfg,
            )
            batch_results.append(
                {
                    "batchId": batch_id,
                    "sectionPath": batch.get("sectionPath", ""),
                    "chapterTitle": batch.get("chapterTitle", ""),
                    "paragraphIds": [paragraph.get("paragraphId", "") for paragraph in batch["paragraphs"]],
                    "inputSignature": plan["signature"],
                    "result": result,
                }
            )
            completed_batch_ids.append(batch_id)
            processed_this_run += 1
            _materialize_fused_report(
                output_path=output_path,
                batches=batches,
                batch_results=batch_results,
                completed_batch_ids=completed_batch_ids,
                errors=errors,
                input_signature=input_signature,
            )
        except Exception as exc:
            errors.append({"batchId": batch_id, "error": str(exc)})
            _materialize_fused_report(
                output_path=output_path,
                batches=batches,
                batch_results=batch_results,
                completed_batch_ids=completed_batch_ids,
                errors=errors,
                input_signature=input_signature,
            )
            if stop_on_error:
                break

    terminology_issues: List[Dict[str, Any]] = []
    logic_issues: List[Dict[str, Any]] = []
    style_issues: List[Dict[str, Any]] = []

    for batch in batch_results:
        batch_id = str(batch.get("batchId") or "")
        result = batch.get("result") if isinstance(batch.get("result"), dict) else {}
        for raw_issue in result.get("terminologyIssues", []) if isinstance(result, dict) else []:
            if not enabled_checks.get("terminology", False):
                break
            normalized = _normalize_terminology_issue(raw_issue, paragraph_lookup)
            if normalized:
                terminology_issues.append(normalized)
        for raw_issue in result.get("logicIssues", []) if isinstance(result, dict) else []:
            if not enabled_checks.get("logic", False):
                break
            normalized = _normalize_logic_issue(raw_issue, paragraph_lookup)
            if normalized:
                logic_issues.append(normalized)
        for raw_issue in result.get("styleIssues", []) if isinstance(result, dict) else []:
            if not enabled_checks.get("style", False):
                break
            normalized = _normalize_style_issue(raw_issue, paragraph_lookup, style_profile or {}, batch_id)
            if normalized:
                style_issues.append(normalized)

    pending_batch_ids = [batch["batchId"] for batch in batches if batch["batchId"] not in completed_batch_ids]
    run_status = "completed" if not pending_batch_ids else ("partial" if completed_batch_ids else "blocked")
    split_reports = _materialize_reports(
        output_dir=output_dir,
        terminology_issues=terminology_issues,
        logic_issues=logic_issues,
        style_issues=style_issues,
        paragraph_lookup=paragraph_lookup,
        run_status=run_status,
        completed_batch_ids=completed_batch_ids,
        pending_batch_ids=pending_batch_ids,
        errors=errors,
    )
    fused_report = _materialize_fused_report(
        output_path=output_path,
        batches=batches,
        batch_results=batch_results,
        completed_batch_ids=completed_batch_ids,
        errors=errors,
        input_signature=input_signature,
    )
    return {
        "fusedReport": fused_report,
        "reports": split_reports,
    }
