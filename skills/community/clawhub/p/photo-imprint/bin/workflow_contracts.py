#!/usr/bin/env python3
"""Shared schema checks for carousel planning, revisions, QA, and release gates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

BRIEF_STRING_FIELDS = ("subject_priority", "thumbnail_read")
BRIEF_LIST_FIELDS = (
    "preserve_anchors", "abstract_or_omit", "material_depth_cues", "forbidden_inventions"
)
STYLE_CONTRACT_FIELDS = (
    "mark_edge_quality", "negative_space_rules", "fill_tonal_rules",
    "background_cleanliness", "frame_border_policy", "abstraction_level",
)
REVISION_OPERATIONS = {"remove", "retain_but_simplify", "add_as_secondary", "preserve_unchanged"}
REVISION_DOMAINS = {"page-content", "page-overlay", "sample", "style-reference", "shared-system", "source-order"}
LOCAL_REVISION_DOMAINS = {"page-content", "page-overlay"}
QA_PAGE_CHECKS = (
    "production_plan_compliance", "subject_integrity", "thumbnail_read", "material_depth_cues",
    "structural_lines", "forbidden_inventions", "background_uniformity", "rectangular_seam_risk",
    "border_frame_risk", "subject_to_paper_compositing", "full_size_viewed", "phone_scale_viewed",
)
QA_SET_CHECKS = (
    "visual_cohesion", "paper_consistency", "style_consistency", "typography_consistency",
    "order_and_dimensions", "cross_page_rhythm", "route_or_module_integrity",
)


def load_object(path: Path, label: str = "JSON") -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object: {path}")
    return value


def write_object(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def validate_production_brief(brief: object, prefix: str = "production_brief") -> list[str]:
    errors: list[str] = []
    if not isinstance(brief, dict):
        return [f"{prefix} is required"]
    for field in BRIEF_STRING_FIELDS:
        if not nonempty_string(brief.get(field)):
            errors.append(f"{prefix}.{field} is required")
    for field in BRIEF_LIST_FIELDS:
        if not string_list(brief.get(field)):
            errors.append(f"{prefix}.{field} requires one or more strings")
    lines = brief.get("structural_lines")
    if not isinstance(lines, list) or not lines:
        errors.append(f"{prefix}.structural_lines requires one or more objects")
    else:
        for index, item in enumerate(lines, start=1):
            if not isinstance(item, dict) or not nonempty_string(item.get("element")):
                errors.append(f"{prefix}.structural_lines[{index}] requires element")
                continue
            if item.get("operation") not in {"retain", "retain_but_simplify"}:
                errors.append(f"{prefix}.structural_lines[{index}].operation must be retain or retain_but_simplify")
    return errors


def validate_style_contract(contract: object, prefix: str = "sample_style_contract") -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return [f"{prefix} is required"]
    for field in STYLE_CONTRACT_FIELDS:
        value = contract.get(field)
        if field in {"mark_edge_quality", "negative_space_rules", "fill_tonal_rules", "background_cleanliness"}:
            if not string_list(value):
                errors.append(f"{prefix}.{field} requires one or more strings")
        elif not nonempty_string(value):
            errors.append(f"{prefix}.{field} is required")
    if contract.get("generated_page_is_style_reference") is not False:
        errors.append(f"{prefix}.generated_page_is_style_reference must be false")
    return errors


def validate_current_sources_and_captions(plan: object) -> list[str]:
    """Validate immutable source bytes and confirmed caption fields in a render plan."""
    if not isinstance(plan, dict):
        return ["render plan must be an object"]
    errors: list[str] = []
    pages = plan.get("pages")
    if not isinstance(pages, list) or not pages:
        return ["render plan must contain pages"]
    caption = plan.get("modules", {}).get("caption", {})
    caption_fields = caption.get("lines", []) if isinstance(caption, dict) and caption.get("enabled") else []
    for page in pages:
        if not isinstance(page, dict):
            errors.append("render plan page must be an object")
            continue
        number = page.get("page")
        source = Path(str(page.get("source_path", "")))
        expected = page.get("source_sha256")
        if not source.is_file() or not isinstance(expected, str) or digest(source) != expected:
            errors.append(f"page {number} source is missing or changed")
        if caption_fields:
            statuses = page.get("caption_status")
            data = page.get("caption_data")
            if not isinstance(statuses, dict) or not isinstance(data, dict):
                errors.append(f"page {number} caption confirmation record is missing")
                continue
            unconfirmed = [
                field for field in caption_fields
                if statuses.get(field) != "confirmed" or not nonempty_string(data.get(field))
            ]
            if unconfirmed:
                errors.append(f"page {number} caption fields are not confirmed: {', '.join(unconfirmed)}")
    return errors


def validate_approval_state(state: object) -> list[str]:
    """Validate the complete approval record required by release packaging."""
    if not isinstance(state, dict):
        return ["approval state must be an object"]
    errors: list[str] = []
    if state.get("schema_version") != "2.0.0":
        errors.append("schema_version must be 2.0.0")
    if state.get("status") not in {"batch_approved", "revision_in_progress", "revision_completed"}:
        errors.append("status does not permit packaging")
    for field in (
        "created_at_utc", "render_plan_path", "render_plan_sha256",
        "production_plan_path", "production_plan_sha256", "sample_style_contract_sha256",
        "sample_path", "sample_sha256", "sample_plate_path", "sample_plate_sha256",
        "sample_registered_at_utc", "presented_at_utc", "approved_at_utc",
    ):
        if not nonempty_string(state.get(field)):
            errors.append(f"{field} is required")
    if not isinstance(state.get("sample_page"), int):
        errors.append("sample_page must be an integer")
    for field in ("permitted_render_pages", "blocked_render_pages"):
        value = state.get(field)
        if not isinstance(value, list) or not all(isinstance(page, int) for page in value):
            errors.append(f"{field} must be an integer array")
    if state.get("blocked_render_pages") != []:
        errors.append("blocked_render_pages must be empty after batch approval")
    if not isinstance(state.get("revision_ledger"), list):
        errors.append("revision_ledger must be an array")
    plate_validation = state.get("sample_plate_validation")
    if not isinstance(plate_validation, dict) or plate_validation.get("blocking_pass") is not True:
        errors.append("sample_plate_validation is required and must pass")
    renderer = state.get("renderer_record")
    if not isinstance(renderer, dict):
        errors.append("renderer_record is required and must be an object")
    elif not nonempty_string(renderer.get("path")) or not nonempty_string(renderer.get("sha256")):
        errors.append("renderer_record requires path and sha256")
    approval = state.get("explicit_approval")
    if not isinstance(approval, dict) or approval.get("actor") != "user" or not nonempty_string(approval.get("text")):
        errors.append("explicit_approval must contain actor=user and non-empty text")
    presentation = state.get("presentation_record")
    required_coverage = {"ordered-page-briefs", "sample-style-contract", "sample-scope", "finish-qa-delivery"}
    if not isinstance(presentation, dict):
        errors.append("presentation_record is required")
    else:
        if presentation.get("mode") not in {"artifact", "faithful-summary"}:
            errors.append("presentation_record.mode is invalid")
        if not nonempty_string(presentation.get("note")):
            errors.append("presentation_record.note is required")
        if presentation.get("plan_decisions_communicated") is not True or presentation.get("sample_discussed") is not True:
            errors.append("presentation_record must confirm plan decisions and sample discussion")
        coverage = presentation.get("decision_coverage")
        if not isinstance(coverage, list) or not required_coverage.issubset(set(coverage)):
            errors.append("presentation_record.decision_coverage is incomplete")
    return errors


def validate_revision_changes(changes: object, valid_pages: set[int]) -> list[str]:
    errors: list[str] = []
    if not isinstance(changes, list) or not changes:
        return ["changes requires one or more revision operations"]
    for index, item in enumerate(changes, start=1):
        if not isinstance(item, dict):
            errors.append(f"changes[{index}] must be an object")
            continue
        if item.get("page") not in valid_pages:
            errors.append(f"changes[{index}].page is not in the render plan")
        if item.get("operation") not in REVISION_OPERATIONS:
            errors.append(f"changes[{index}].operation must be one of {sorted(REVISION_OPERATIONS)}")
        if item.get("domain") not in REVISION_DOMAINS:
            errors.append(f"changes[{index}].domain must be one of {sorted(REVISION_DOMAINS)}")
        if not nonempty_string(item.get("target")) or not nonempty_string(item.get("instruction")):
            errors.append(f"changes[{index}] requires target and instruction")
    return errors
