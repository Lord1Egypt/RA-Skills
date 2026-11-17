#!/usr/bin/env python3
"""Register the sample pair, record discussion, and gate pages 2..N."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image
from workflow_contracts import digest, load_object, validate_style_contract, write_object
from renderer_receipt import load as load_renderer_receipt, validate as validate_renderer_receipt
from clean_plate import analyze as analyze_plate, policy_from_config


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def verify_locked_files(state: dict[str, Any]) -> None:
    for stem in ("render_plan", "production_plan"):
        value, expected = state.get(f"{stem}_path"), state.get(f"{stem}_sha256")
        if not isinstance(value, str) or not isinstance(expected, str):
            raise ValueError(f"state is missing locked {stem} metadata")
        path = Path(value)
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f"locked {stem} changed; rebuild the production plan and sample before approval")
    plan = load_object(Path(state["render_plan_path"]), "render plan")
    config_lock = plan.get("resolved_config_lock", {})
    config_path = Path(str(config_lock.get("path", "")))
    if not config_path.is_file() or digest(config_path) != config_lock.get("sha256"):
        raise ValueError("resolved config changed; rebuild and re-review the plan+sample")
    for reference in plan.get("style_reference_locks", []):
        for stem in ("image", "source_metadata"):
            path = Path(str(reference.get(f"{stem}_path", "")))
            expected = reference.get(f"{stem}_sha256")
            if not path.is_file() or not isinstance(expected, str) or digest(path) != expected:
                raise ValueError(f"approved style reference {reference.get('id')} {stem} changed or is missing")
    errors = validate_style_contract(plan.get("sample_style_contract"))
    if errors:
        raise ValueError("invalid sample style contract: " + "; ".join(errors))
    if canonical_hash(plan["sample_style_contract"]) != state.get("sample_style_contract_sha256"):
        raise ValueError("sample style contract changed; rebuild and re-review")


def verify_receipt_scope(receipt: dict[str, Any], plan: dict[str, Any], sample_page: object) -> None:
    pages = [page for page in plan.get("pages", []) if isinstance(page, dict) and page.get("page") == sample_page]
    if len(pages) != 1:
        raise ValueError("sample page is not uniquely present in the render plan")
    expected_sources = {
        (str(Path(str(page.get("source_path", ""))).resolve()), page.get("source_sha256")) for page in pages
    }
    actual_sources = {
        (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
        for entry in receipt.get("sources", []) if isinstance(entry, dict)
    }
    if actual_sources != expected_sources:
        raise ValueError("renderer record sources do not exactly match the sample page source")
    expected_references = {
        (str(Path(str(entry.get("image_path", ""))).resolve()), entry.get("image_sha256"))
        for entry in plan.get("style_reference_locks", []) if isinstance(entry, dict)
    }
    actual_references = {
        (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
        for entry in receipt.get("references", []) if isinstance(entry, dict)
    }
    if actual_references != expected_references:
        raise ValueError("renderer record references do not exactly match the approved style references")


def readable_size(path: Path) -> tuple[int, int]:
    if not path.is_file():
        raise ValueError(f"image is missing: {path}")
    try:
        with Image.open(path) as image:
            return image.size
    except Exception as exc:
        raise ValueError(f"image is unreadable: {path}: {exc}") from exc


def canonical_plate_validation(plate_path: Path, config_path: Path) -> tuple[dict[str, Any], tuple[int, int]]:
    """Return the single canonical live plate-validation object stored and later rechecked by the gate."""
    policy, expected_size = policy_from_config(config_path)
    with Image.open(plate_path) as plate:
        analysis = analyze_plate(plate, policy)
        analysis["checks"]["dimensions"] = plate.size == expected_size
    analysis["blocking_pass"] = all(analysis["checks"].values())
    return analysis, expected_size


def command_register(args: argparse.Namespace) -> int:
    state = load_object(args.state, "review state")
    verify_locked_files(state)
    plan = load_object(Path(state["render_plan_path"]), "render plan")
    pages = plan.get("pages", [])
    if not pages or state.get("sample_page") != pages[0].get("page"):
        raise ValueError("state sample page does not match the first EXIF-ordered page")
    canvas = plan.get("composition", {}).get("canvas", {})
    expected = (canvas.get("width"), canvas.get("height"))
    if readable_size(args.sample) != expected:
        raise ValueError(f"composed sample dimensions do not match {expected}")
    if readable_size(args.sample_plate) != expected:
        raise ValueError(f"sample plate dimensions do not match {expected}")
    config_path = Path(str(plan.get("resolved_config_lock", {}).get("path", "")))
    with Image.open(args.sample_plate) as plate:
        if plate.mode not in {"RGBA", "LA"} or "A" not in plate.getbands():
            raise ValueError("sample plate must contain an alpha channel after normalization")
    plate_analysis, validation_size = canonical_plate_validation(args.sample_plate, config_path)
    if validation_size != expected:
        raise ValueError("render plan and resolved config disagree on expected dimensions")
    if not plate_analysis.get("blocking_pass"):
        raise ValueError("sample plate failed active normalization-policy validation")
    if not args.renderer_record.is_file():
        raise ValueError(f"renderer record is missing: {args.renderer_record}")
    receipt = load_renderer_receipt(args.renderer_record)
    receipt_errors = validate_renderer_receipt(receipt, check_files=True, require_rendered_output=True)
    if receipt_errors:
        raise ValueError("renderer record is invalid: " + "; ".join(receipt_errors))
    verify_receipt_scope(receipt, plan, state.get("sample_page"))
    plate_evidence = (str(args.sample_plate.resolve()), digest(args.sample_plate.resolve()))
    receipt_outputs = {
        (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
        for entry in receipt.get("rendered_outputs", []) if isinstance(entry, dict)
    }
    if receipt_outputs != {plate_evidence}:
        raise ValueError("sample renderer record outputs must contain exactly the normalized sample plate")
    renderer_record = {"path": str(args.renderer_record.resolve()), "sha256": digest(args.renderer_record.resolve())}
    state.update({
        "status": "sample_ready_not_shown", "sample_path": str(args.sample.resolve()),
        "sample_sha256": digest(args.sample.resolve()), "sample_plate_path": str(args.sample_plate.resolve()),
        "sample_plate_sha256": digest(args.sample_plate.resolve()), "sample_plate_validation": plate_analysis,
        "renderer_record": renderer_record,
        "sample_registered_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "explicit_approval": None, "permitted_render_pages": [pages[0].get("page")],
        "blocked_render_pages": [page.get("page") for page in pages[1:]],
    })
    write_object(args.state, state)
    print("Registered normalized sample plate and composed sample; discuss plan decisions and sample before approval")
    return 0


def verify_sample(state: dict[str, Any]) -> None:
    for key in ("sample", "sample_plate"):
        path_value, expected = state.get(f"{key}_path"), state.get(f"{key}_sha256")
        if not isinstance(path_value, str) or not isinstance(expected, str):
            raise ValueError(f"{key} metadata is missing")
        path = Path(path_value)
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f"registered {key} changed; register and discuss the revised sample pair")
    renderer = state.get("renderer_record")
    if not isinstance(renderer, dict):
        raise ValueError("registered renderer record is missing")
    path = Path(str(renderer.get("path", "")))
    if not path.is_file() or digest(path) != renderer.get("sha256"):
        raise ValueError("registered renderer record changed; register and discuss the revised sample pair")
    receipt = load_renderer_receipt(path)
    errors = validate_renderer_receipt(receipt, check_files=True, require_rendered_output=True)
    if errors:
        raise ValueError("registered renderer record is invalid: " + "; ".join(errors))
    plan = load_object(Path(state["render_plan_path"]), "render plan")
    verify_receipt_scope(receipt, plan, state.get("sample_page"))
    plate_path = Path(str(state.get("sample_plate_path", ""))).resolve()
    expected_output = {(str(plate_path), state.get("sample_plate_sha256"))}
    actual_outputs = {
        (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
        for entry in receipt.get("rendered_outputs", []) if isinstance(entry, dict)
    }
    if actual_outputs != expected_output:
        raise ValueError("sample renderer record outputs must contain exactly the normalized sample plate")
    current_analysis, _ = canonical_plate_validation(
        plate_path, Path(str(plan.get("resolved_config_lock", {}).get("path", "")))
    )
    if not current_analysis.get("blocking_pass") or current_analysis != state.get("sample_plate_validation"):
        raise ValueError("registered sample plate validation is missing, failed, or stale")
    evidence = (str(plate_path), state.get("sample_plate_sha256"))
    outputs = {
        (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
        for entry in receipt.get("rendered_outputs", []) if isinstance(entry, dict)
    }
    if evidence not in outputs:
        raise ValueError("registered renderer record no longer matches the sample plate")


def command_mark_shown(args: argparse.Namespace) -> int:
    state = load_object(args.state, "review state")
    verify_locked_files(state)
    if state.get("status") != "sample_ready_not_shown":
        raise ValueError("discussion can be recorded only after registering the sample pair")
    verify_sample(state)
    note = (args.discussion_note or args.presentation_note or "").strip()
    if not note:
        raise ValueError("discussion note is required")
    if not args.plan_decisions_communicated or not args.sample_discussed:
        raise ValueError("both plan decisions and the sample must have been communicated and discussed")
    required_coverage = {"ordered-page-briefs", "sample-style-contract", "sample-scope", "finish-qa-delivery"}
    coverage = set(args.decision_coverage or [])
    missing = sorted(required_coverage - coverage)
    if missing:
        raise ValueError("decision coverage is incomplete: " + ", ".join(missing))
    state.update({
        "status": "awaiting_explicit_user_approval",
        "presented_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "presentation_record": {"mode": args.presentation_mode, "note": note,
            "decision_coverage": sorted(coverage),
            "plan_decisions_communicated": True, "sample_discussed": True},
    })
    write_object(args.state, state)
    print("Recorded discussion of the plan decisions and sample; pages 2..N remain blocked")
    return 0


def command_approve(args: argparse.Namespace) -> int:
    state = load_object(args.state, "review state")
    verify_locked_files(state)
    if state.get("status") != "awaiting_explicit_user_approval":
        raise ValueError("approval is allowed only after the plan decisions and sample were discussed")
    verify_sample(state)
    text = args.approval_text.strip()
    if not args.explicit_user_approval:
        raise ValueError("missing --explicit-user-approval; never infer permission to render pages 2..N")
    if not text:
        raise ValueError("approval text must copy the user's explicit approval")
    plan = load_object(Path(state["render_plan_path"]), "render plan")
    remaining = [page.get("page") for page in plan.get("pages", [])[1:]]
    state.update({"status": "batch_approved", "approved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "explicit_approval": {"actor": "user", "text": text},
        "permitted_render_pages": remaining, "blocked_render_pages": []})
    write_object(args.state, state)
    print("Recorded explicit user approval; pages 2..N are now permitted")
    return 0


def command_status(args: argparse.Namespace) -> int:
    print(json.dumps(load_object(args.state, "review state"), indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze and discuss the production plan/sample before batch rendering")
    sub = parser.add_subparsers(dest="command", required=True)
    register = sub.add_parser("register-sample", help="Register normalized clean plate and composed first-page sample")
    register.add_argument("--state", required=True, type=Path)
    register.add_argument("--sample", required=True, type=Path, help="Composed first-page sample")
    register.add_argument("--sample-plate", required=True, type=Path, help="Normalized transparent sample plate")
    register.add_argument("--renderer-record", required=True, type=Path, help="Validated renderer receipt that hash-locks the sample plate")
    register.set_defaults(handler=command_register)
    shown = sub.add_parser("mark-shown", help="Record discussion of plan decisions and sample")
    shown.add_argument("--state", required=True, type=Path)
    shown.add_argument("--presentation-mode", required=True, choices=("artifact", "faithful-summary"))
    shown.add_argument("--discussion-note", help="Where/how the plan decisions and sample were discussed")
    shown.add_argument("--presentation-note", help=argparse.SUPPRESS)
    shown.add_argument("--plan-decisions-communicated", action="store_true")
    shown.add_argument("--sample-discussed", action="store_true")
    shown.add_argument("--decision-coverage", action="append", choices=(
        "ordered-page-briefs", "sample-style-contract", "sample-scope", "finish-qa-delivery"
    ), help="Repeat for every plan-decision group actually communicated")
    shown.set_defaults(handler=command_mark_shown)
    approve = sub.add_parser("approve", help="Record exact explicit user permission for pages 2..N")
    approve.add_argument("--state", required=True, type=Path)
    approve.add_argument("--approval-text", required=True)
    approve.add_argument("--explicit-user-approval", action="store_true")
    approve.set_defaults(handler=command_approve)
    status = sub.add_parser("status", help="Print gate state")
    status.add_argument("--state", required=True, type=Path)
    status.set_defaults(handler=command_status)
    args = parser.parse_args()
    try:
        return args.handler(args)
    except ValueError as exc:
        print(f"Review gate blocked: {exc}", file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
