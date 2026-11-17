#!/usr/bin/env python3
"""Cross-file integrity checks for release-authorizing artifact reviews."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from evidence import (
    EvidenceError,
    load_object,
    load_registry,
    require_evidence,
    verify_entry,
)


CATEGORIES = (
    "carrier",
    "composition",
    "narrative",
    "color_light",
    "material_physics",
    "ai_residue",
    "spec_fit",
)


def parse_time(value: Any, label: str, blockers: list[str]) -> datetime | None:
    if not isinstance(value, str):
        blockers.append(f"{label} must be an ISO 8601 date-time")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        blockers.append(f"{label} must be an ISO 8601 date-time")
        return None


def find_registered_review(
    review_path: Path,
    indexed: dict[str, dict[str, Any]],
    registry_path: Path,
) -> str | None:
    expected = review_path.resolve()
    for entry_id, entry in indexed.items():
        if entry.get("kind") != "artifact-review":
            continue
        try:
            candidate = verify_entry(entry, registry_path, {"artifact-review"})
        except EvidenceError:
            continue
        if candidate.resolve() == expected:
            return entry_id
    return None


def validate_authorized_review(
    review: dict[str, Any],
    review_path: Path,
    registry_path: Path | None,
) -> list[str]:
    """Return blockers proving whether an authorized review is evidence-bound."""

    blockers: list[str] = []
    decision = review.get("decision") or {}
    if decision.get("release_authorized") is not True:
        return blockers

    reviewer = review.get("reviewer") or {}
    blind = review.get("blind_pass") or {}
    spec = review.get("spec_pass") or {}

    if decision.get("recommendation") != "accept":
        blockers.append("release authorization requires recommendation=accept")
    if reviewer.get("kind") not in {
        "fresh-context-agent", "different-model", "human"
    }:
        blockers.append("release authorization requires an independent reviewer kind")
    if not reviewer.get("session_ref"):
        blockers.append("release authorization requires reviewer.session_ref")
    if not reviewer.get("identity_ref"):
        blockers.append("release authorization requires reviewer.identity_ref")
    if not review.get("artifact_sha256"):
        blockers.append("release authorization requires artifact_sha256")
    if not review.get("spec_ref"):
        blockers.append("release authorization requires spec_ref")
    if blind.get("prompt_hidden") is not True:
        blockers.append("release authorization requires a prompt-blind first pass")
    for category in CATEGORIES:
        findings = spec.get(category)
        if not isinstance(findings, list) or not findings:
            blockers.append(
                f"release authorization requires recorded findings for spec_pass.{category}"
            )

    if registry_path is None:
        blockers.append("release authorization requires an evidence registry")
        return blockers

    try:
        _, indexed = load_registry(registry_path)
    except EvidenceError as exc:
        blockers.append(str(exc))
        return blockers

    if find_registered_review(review_path, indexed, registry_path) is None:
        blockers.append("the supplied review file is not registered as artifact-review evidence")

    artifact_id = str(review.get("artifact_ref", ""))
    artifact_entry: dict[str, Any] | None = None
    try:
        artifact_entry, _ = require_evidence(
            artifact_id, indexed, registry_path, {"artifact"}
        )
    except EvidenceError as exc:
        blockers.append(str(exc))
    if artifact_entry is not None:
        media_type = str(artifact_entry.get("media_type", "")).lower()
        if not media_type.startswith("image/"):
            blockers.append("release review artifact evidence must have an image media_type")
        if str(review.get("artifact_sha256", "")).lower() != str(
            artifact_entry.get("sha256", "")
        ).lower():
            blockers.append("artifact_sha256 does not match registered artifact evidence")

    spec_ref = str(review.get("spec_ref", ""))
    if spec_ref:
        try:
            require_evidence(spec_ref, indexed, registry_path, {"visual-spec"})
        except EvidenceError as exc:
            blockers.append(str(exc))

    session_ref = str(reviewer.get("session_ref", ""))
    if not session_ref:
        return blockers
    try:
        _, session_path = require_evidence(
            session_ref, indexed, registry_path, {"review-session"}
        )
        session = load_object(session_path, "review session")
    except EvidenceError as exc:
        blockers.append(str(exc))
        return blockers

    if session.get("schema") != "moso.review-session/0.1":
        blockers.append("review session must use moso.review-session/0.1")
    if session.get("artifact_ref") != artifact_id:
        blockers.append("review session artifact_ref does not match the review")
    if session.get("reviewer_id") != reviewer.get("identity_ref"):
        blockers.append("review session reviewer_id does not match reviewer.identity_ref")
    if session.get("reviewer_kind") != reviewer.get("kind"):
        blockers.append("review session reviewer_kind does not match the review")
    if session.get("generation_context_id") == session.get("review_context_id"):
        blockers.append("review context must differ from generation context")
    if session.get("prompt_hidden") is not True:
        blockers.append("review session must hide the prompt")
    if session.get("source_hidden") is not True:
        blockers.append("review session must hide the source/system identity")

    started = parse_time(session.get("started_at"), "review session started_at", blockers)
    committed = parse_time(
        session.get("committed_at"), "review session committed_at", blockers
    )
    reviewed = parse_time(reviewer.get("reviewed_at"), "reviewer.reviewed_at", blockers)
    if started and committed and committed < started:
        blockers.append("review session committed_at precedes started_at")
    if committed and reviewed and reviewed < committed:
        blockers.append("reviewer.reviewed_at precedes review session committed_at")

    return blockers
