#!/usr/bin/env python3
"""Validate MoSoCanvas v0.2 execution contracts without claiming visual quality."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from evidence import EvidenceError, load_object, load_registry, require_evidence
from review_integrity import validate_authorized_review

PHASES_AFTER_FREEZE = {
    "preflight", "execute", "independent-review", "decision", "accept"
}
PHASES_AFTER_EXECUTION = {"independent-review", "decision", "accept"}
GENERATIVE_OPERATIONS = {
    "masked-generative", "full-frame-generative", "full-regeneration"
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, label: str, blockers: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        blockers.append(f"{label} cannot be loaded: {exc}")
        return {}
    if not isinstance(value, dict):
        blockers.append(f"{label} must be a JSON object")
        return {}
    return value


def resolve_local(ref: str, base: Path) -> Path | None:
    if not ref or ref.startswith(("http://", "https://", "codex://")):
        return None
    path = Path(ref).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def flag_missing_keys(
    value: dict[str, Any], keys: tuple[str, ...], label: str, blockers: list[str]
) -> None:
    for key in keys:
        if key not in value:
            blockers.append(f"{label} missing required field: {key}")


def finish(
    args: argparse.Namespace, blockers: list[str], warnings: list[str]
) -> int:
    report = {
        "schema": "moso.preflight-report/0.4",
        "scope": "contract-integrity-only",
        "run_state": str(args.run_state.resolve()),
        "status": "block" if blockers else "pass",
        "blockers": blockers,
        "warnings": warnings,
        "not_evaluated": [
            "composition quality",
            "narrative effectiveness",
            "color and lighting quality",
            "physical plausibility",
            "AI residue",
            "user preference"
        ]
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if blockers else 0


def validate_release_evidence(
    state: dict[str, Any], registry_path: Path, blockers: list[str]
) -> None:
    try:
        _, indexed = load_registry(registry_path)
    except EvidenceError as exc:
        blockers.append(str(exc))
        return

    required: list[tuple[str, set[str]]] = []
    for field, kinds in (
        ("spec_ref", {"visual-spec"}),
        ("shot_plan_ref", {"shot-plan"}),
        ("series_plan_ref", {"series-plan"}),
        ("release_review_ref", {"artifact-review"}),
        ("user_decision_ref", {"user-decision"}),
    ):
        value = state.get(field)
        if value:
            required.append((str(value), kinds))
        elif field in {"spec_ref", "release_review_ref", "user_decision_ref"}:
            blockers.append(f"phase accept requires {field}")

    checkpoint = state.get("approved_checkpoint") or {}
    if checkpoint.get("role") not in {None, "none", "reference"}:
        required.append((
            str(checkpoint.get("source_ref", "")),
            {"artifact", "composition-proof"}
        ))

    output_ids: set[str] = set()
    independent_review_ids: set[str] = set()
    for attempt in state.get("generation_attempts") or []:
        execution = attempt.get("execution") or {}
        prompt_ref = execution.get("prompt_ref")
        if prompt_ref:
            required.append((str(prompt_ref), {"prompt"}))
        output_ref = execution.get("output_ref")
        if output_ref:
            output_ids.add(str(output_ref))
            required.append((str(output_ref), {"artifact"}))
        self_review_ref = attempt.get("self_review_ref")
        if self_review_ref:
            required.append((str(self_review_ref), {"artifact-review"}))
        review_ref = attempt.get("independent_review_ref")
        if review_ref:
            independent_review_ids.add(str(review_ref))
            required.append((str(review_ref), {"artifact-review"}))

    resolved: dict[str, Path] = {}
    for evidence_id, kinds in required:
        if not evidence_id:
            blockers.append("release evidence contains an empty id")
            continue
        try:
            _, path = require_evidence(evidence_id, indexed, registry_path, kinds)
            resolved[evidence_id] = path
        except EvidenceError as exc:
            blockers.append(str(exc))

    review_id = state.get("release_review_ref")
    decision_id = state.get("user_decision_ref")
    if review_id not in resolved or decision_id not in resolved:
        return
    if state.get("generation_attempts") and str(review_id) not in independent_review_ids:
        blockers.append(
            "release_review_ref must be an independent review from a recorded attempt"
        )
    try:
        review = load_object(resolved[str(review_id)], "release review")
        decision = load_object(resolved[str(decision_id)], "user decision")
    except EvidenceError as exc:
        blockers.append(str(exc))
        return

    spec_id = state.get("spec_ref")
    if spec_id in resolved:
        try:
            spec_document = load_object(resolved[str(spec_id)], "visual spec")
            if spec_document.get("schema") not in {
                "moso.visual-spec/0.1", "moso.visual-spec/0.2"
            }:
                blockers.append("registered visual spec has the wrong schema")
        except EvidenceError as exc:
            blockers.append(str(exc))

    shot_id = state.get("shot_plan_ref")
    if shot_id in resolved:
        try:
            shot_document = load_object(resolved[str(shot_id)], "shot plan")
            selection = shot_document.get("selection") or {}
            if selection.get("status") != "selected":
                blockers.append("registered shot plan must contain a selected composition")
            if selection.get("proof_type") not in {
                "three-value-thumbnail", "mass-map", "approved-layout"
            }:
                blockers.append("registered shot plan selection requires a composition proof")
            proof_ref = str(selection.get("proof_ref", ""))
            if not proof_ref:
                blockers.append("registered shot plan selection requires proof_ref")
            else:
                try:
                    require_evidence(
                        proof_ref, indexed, registry_path, {"composition-proof"}
                    )
                except EvidenceError as exc:
                    blockers.append(str(exc))
        except EvidenceError as exc:
            blockers.append(str(exc))

    series_id = state.get("series_plan_ref")
    if series_id in resolved:
        try:
            series_document = load_object(resolved[str(series_id)], "series plan")
            expected_frames = (state.get("output_requirements") or {}).get("frame_count")
            if series_document.get("frame_count") != expected_frames:
                blockers.append(
                    "registered series plan frame_count conflicts with output requirements"
                )
            pilot = series_document.get("pilot_gate") or {}
            if pilot.get("status") != "approved":
                blockers.append("registered series plan requires an approved pilot")
            pilot_review_ref = str(pilot.get("review_ref", ""))
            if not pilot_review_ref:
                blockers.append("approved pilot requires review_ref")
            else:
                try:
                    require_evidence(
                        pilot_review_ref, indexed, registry_path, {"artifact-review"}
                    )
                except EvidenceError as exc:
                    blockers.append(str(exc))
        except EvidenceError as exc:
            blockers.append(str(exc))

    reviewer = review.get("reviewer") or {}
    blind = review.get("blind_pass") or {}
    review_decision = review.get("decision") or {}
    if review.get("schema") != "moso.artifact-review/0.1":
        blockers.append("release review has the wrong schema")
    if reviewer.get("independent_from_generation") is not True:
        blockers.append("release review is not independent from generation")
    if reviewer.get("actual_artifact_inspected") is not True:
        blockers.append("release review did not inspect the actual artifact")
    if blind.get("prompt_hidden") is not True:
        blockers.append("release review did not perform a prompt-blind first pass")
    if review_decision.get("recommendation") != "accept":
        blockers.append("release review must recommend accept")
    if review_decision.get("release_authorized") is not True:
        blockers.append("release review does not authorize release")
    blockers.extend(
        validate_authorized_review(review, resolved[str(review_id)], registry_path)
    )

    artifact_id = str(review.get("artifact_ref", ""))
    try:
        require_evidence(artifact_id, indexed, registry_path, {"artifact"})
    except EvidenceError as exc:
        blockers.append(str(exc))
    checkpoint_id = str(checkpoint.get("source_ref", ""))
    if artifact_id not in output_ids | {checkpoint_id}:
        blockers.append("release review artifact is not a generated output or approved checkpoint")

    if decision.get("schema") != "moso.user-decision/0.1":
        blockers.append("user decision has the wrong schema")
    if decision.get("task_id") != state.get("task_id"):
        blockers.append("user decision task_id does not match run state")
    if decision.get("artifact_ref") != artifact_id:
        blockers.append("user decision artifact does not match release review")
    expected_user_decision = (state.get("quality_status") or {}).get("user_acceptance")
    if decision.get("decision") != expected_user_decision:
        blockers.append("user decision does not match quality_status.user_acceptance")
    if decision.get("actor") != "user":
        blockers.append("user decision actor must be user")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check structural readiness; this does not inspect or approve image aesthetics."
    )
    parser.add_argument("run_state", type=Path)
    parser.add_argument("--shot-plan", type=Path)
    parser.add_argument("--series-plan", type=Path)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    blockers: list[str] = []
    warnings: list[str] = []
    state = load_json(args.run_state, "run state", blockers)
    base = args.run_state.resolve().parent

    if state.get("schema") != "moso.run-state/0.4":
        blockers.append(
            "run state must migrate to moso.run-state/0.4; legacy self-review fields cannot "
            "authorize execution or acceptance"
        )
        if state.get("phase") == "accept":
            legacy_quality = state.get("quality_status") or {}
            if legacy_quality.get("user_acceptance") not in {
                "accepted", "accepted-with-tradeoff"
            }:
                blockers.append("legacy phase accept lacks actual user acceptance")
            blockers.append("legacy phase accept lacks an independent release review")
        return finish(args, blockers, warnings)

    flag_missing_keys(
        state,
        (
            "schema", "task_id", "mode", "phase", "approved_checkpoint",
            "allowed_changes", "protected_elements", "attempt_budget",
            "output_requirements", "verification", "direction_approval_status",
            "quality_status"
        ),
        "run state",
        blockers,
    )

    mode = state.get("mode")
    phase = state.get("phase")
    checkpoint = state.get("approved_checkpoint") or {}
    budget = state.get("attempt_budget") or {}
    quality = state.get("quality_status") or {}
    output = state.get("output_requirements") or {}

    if mode in {"production", "repair"}:
        if checkpoint.get("role") in {None, "none", "reference"}:
            blockers.append("production/repair requires an approved composition, pilot, mockup, master, or output")
        if not state.get("allowed_changes"):
            blockers.append("production/repair requires at least one allowed change")
        if not state.get("protected_elements"):
            blockers.append("production/repair requires protected elements")

    if mode == "repair":
        lineage = state.get("lineage") or {}
        if not lineage.get("parent_ref") or not lineage.get("operation"):
            blockers.append("repair requires lineage.parent_ref and lineage.operation")

    source_ref = checkpoint.get("source_ref", "")
    local_checkpoint = resolve_local(source_ref, base)
    if local_checkpoint:
        if not local_checkpoint.exists():
            blockers.append(f"checkpoint source does not exist: {local_checkpoint}")
        elif checkpoint.get("sha256"):
            if file_sha256(local_checkpoint).lower() != checkpoint["sha256"].lower():
                blockers.append("checkpoint sha256 does not match source")
        else:
            warnings.append("local checkpoint has no sha256")

    for asset in state.get("required_assets") or []:
        if asset.get("status") == "missing":
            blockers.append(f"required asset is missing: {asset.get('role', 'unknown')}")
        elif asset.get("status") in {"placeholder", "unverified"}:
            warnings.append(f"asset is not authoritative: {asset.get('role', 'unknown')}")

    for kind in ("generative", "repair"):
        used = budget.get(f"{kind}_used")
        allowed = budget.get(kind)
        if used is None or allowed is None:
            blockers.append(f"attempt_budget requires {kind} and {kind}_used")
        elif used > allowed:
            blockers.append(f"{kind} attempt budget exceeded: {used}>{allowed}")

    release_registry_mode = phase == "accept" and bool(
        args.registry or state.get("evidence_registry_ref")
    )
    shot_plan_path = args.shot_plan
    if (
        not shot_plan_path
        and state.get("shot_plan_ref")
        and not release_registry_mode
    ):
        shot_plan_path = resolve_local(state["shot_plan_ref"], base)
    if phase in PHASES_AFTER_FREEZE and mode in {"direction", "production"}:
        if not state.get("shot_plan_ref") and not shot_plan_path:
            blockers.append("post-freeze direction/production requires shot_plan_ref")
        elif shot_plan_path:
            shot = load_json(shot_plan_path, "shot plan", blockers)
            selection = shot.get("selection") or {}
            if selection.get("status") != "selected":
                blockers.append("shot plan must contain a selected composition")
            if selection.get("proof_type") not in {
                "three-value-thumbnail", "mass-map", "approved-layout"
            }:
                blockers.append("selected shot requires a composition proof")
            if not selection.get("proof_ref"):
                blockers.append("selected shot requires proof_ref")

    frame_count = output.get("frame_count", 1)
    series_plan_path = args.series_plan
    if (
        not series_plan_path
        and state.get("series_plan_ref")
        and not release_registry_mode
    ):
        series_plan_path = resolve_local(state["series_plan_ref"], base)
    if frame_count and frame_count > 1:
        if not state.get("series_plan_ref") and not series_plan_path:
            blockers.append("multi-frame output requires series_plan_ref")
        elif series_plan_path:
            series = load_json(series_plan_path, "series plan", blockers)
            if series.get("frame_count") != frame_count:
                blockers.append("series plan frame_count conflicts with output requirements")
            pilot = series.get("pilot_gate") or {}
            if phase in {"execute", "independent-review", "decision", "accept"}:
                if pilot.get("status") != "approved":
                    blockers.append("series expansion requires an approved pilot")
                if not pilot.get("review_ref"):
                    blockers.append("approved pilot requires an independent review_ref")

    attempts = state.get("generation_attempts") or []
    lineage = state.get("lineage") or {}
    is_generative = (
        (budget.get("generative") or 0) > 0
        or lineage.get("operation") in GENERATIVE_OPERATIONS
    )
    if is_generative and not attempts:
        blockers.append("generative execution requires generation_attempts")

    for index, attempt in enumerate(attempts, start=1):
        prefix = f"generation attempt {index}"
        brief = attempt.get("pre_generation_brief") or {}
        flag_missing_keys(
            brief,
            (
                "objective", "viewer_position", "first_read", "composition_geometry",
                "narrative_beat", "color_light_logic", "required_content",
                "protected_content", "main_risk", "communicated_to_user"
            ),
            f"{prefix} brief",
            blockers,
        )
        if brief.get("communicated_to_user") is not True:
            blockers.append(f"{prefix} brief must be communicated before generation")

        status = attempt.get("status")
        execution = attempt.get("execution") or {}
        if status in {"generated", "reviewed", "rejected"}:
            flag_missing_keys(
                execution,
                (
                    "backend", "interface", "model", "model_version", "prompt_ref",
                    "prompt_sha256", "parameters", "generated_at", "output_ref"
                ),
                f"{prefix} execution",
                blockers,
            )
        if phase in PHASES_AFTER_EXECUTION and status == "planned":
            blockers.append(f"{prefix} cannot remain planned after execution")
        if status == "reviewed":
            if not attempt.get("self_review_ref"):
                blockers.append(f"{prefix} reviewed status requires self_review_ref")
            if not attempt.get("independent_review_ref"):
                blockers.append(f"{prefix} reviewed status requires independent_review_ref")
            if (
                attempt.get("self_review_ref")
                and attempt.get("self_review_ref") == attempt.get("independent_review_ref")
            ):
                blockers.append(
                    f"{prefix} self review and independent review must be different evidence"
                )

    if phase in {"execute", "independent-review", "decision", "accept"}:
        if state.get("direction_approval_status") not in {
            "approved", "user-overrode", "not-required"
        }:
            blockers.append("execution cannot proceed while direction approval is pending")

    if phase == "accept":
        if quality.get("user_acceptance") not in {"accepted", "accepted-with-tradeoff"}:
            blockers.append("phase accept requires actual user acceptance")
        if quality.get("independent_review") not in {"pass", "conditional"}:
            blockers.append("phase accept requires an independent review pass or conditional pass")
        if not state.get("release_review_ref"):
            blockers.append("phase accept requires release_review_ref")
        if not state.get("user_decision_ref"):
            blockers.append("phase accept requires user_decision_ref")
        reviewed_attempts = [
            attempt for attempt in attempts if attempt.get("status") == "reviewed"
        ]
        if is_generative and not reviewed_attempts:
            blockers.append("phase accept requires at least one reviewed generative attempt")
        registry_path = args.registry
        if not registry_path and state.get("evidence_registry_ref"):
            registry_path = resolve_local(str(state["evidence_registry_ref"]), base)
        if not registry_path:
            blockers.append("phase accept requires a local evidence registry")
        else:
            validate_release_evidence(state, registry_path, blockers)

    return finish(args, blockers, warnings)


if __name__ == "__main__":
    raise SystemExit(main())
