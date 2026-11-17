#!/usr/bin/env python3
"""Emit a renderable page subset while enforcing the first-sample approval gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from renderer_receipt import load as load_renderer_receipt, validate as validate_renderer_receipt
from review_gate import verify_receipt_scope, verify_sample


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object: {path}")
    return value


def verify_locked(path: Path, expected: object, label: str) -> None:
    if not path.is_file():
        raise ValueError(f"{label} is missing: {path}")
    if not isinstance(expected, str) or digest(path) != expected:
        raise ValueError(f"{label} changed after the review state was created; rebuild and re-review")


def verify_batch_inputs(plan: dict[str, Any], pages: list[dict[str, Any]]) -> None:
    caption = plan.get("modules", {}).get("caption", {})
    caption_fields = caption.get("lines", []) if caption.get("enabled") else []
    for page in pages:
        number = page.get("page")
        source = Path(str(page.get("source_path", "")))
        expected = page.get("source_sha256")
        if not source.is_file() or not isinstance(expected, str) or digest(source) != expected:
            raise ValueError(f"page {number} source is missing or changed; rebuild and re-review before batch rendering")
        if caption_fields:
            statuses = page.get("caption_status")
            data = page.get("caption_data")
            if not isinstance(statuses, dict) or not isinstance(data, dict):
                raise ValueError(f"page {number} caption confirmation record is missing")
            unconfirmed = [
                field for field in caption_fields
                if statuses.get(field) != "confirmed" or data.get(field) in (None, "")
            ]
            if unconfirmed:
                raise ValueError(
                    f"page {number} caption fields are not confirmed: {', '.join(unconfirmed)}"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-plan", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("sample", "batch"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        plan = load(args.render_plan, "render plan")
        state = load(args.state, "review state")
        if Path(state.get("render_plan_path", "")).resolve() != args.render_plan.resolve():
            raise ValueError("review state belongs to a different render plan")
        verify_locked(args.render_plan.resolve(), state.get("render_plan_sha256"), "render plan")
        production_plan = Path(state.get("production_plan_path", ""))
        verify_locked(production_plan, state.get("production_plan_sha256"), "production plan")
        config_lock = plan.get("resolved_config_lock", {})
        verify_locked(Path(str(config_lock.get("path", ""))), config_lock.get("sha256"), "resolved config")
        for reference in plan.get("style_reference_locks", []):
            verify_locked(Path(str(reference.get("image_path", ""))), reference.get("image_sha256"), f"style reference {reference.get('id')} image")
            verify_locked(Path(str(reference.get("source_metadata_path", ""))), reference.get("source_metadata_sha256"), f"style reference {reference.get('id')} metadata")
        pages = plan.get("pages")
        if not isinstance(pages, list) or not pages:
            raise ValueError("render plan has no pages")

        if args.mode == "sample":
            selected = pages[:1]
            status = state.get("status")
            if status not in {"plan_ready_sample_not_registered", "sample_ready_not_shown", "awaiting_explicit_user_approval"}:
                raise ValueError(f"sample scope is unavailable while gate status is {status!r}; revise the plan to reset the gate")
            gate_note = "Only the first EXIF-ordered page may be rendered. Show it with the production plan."
        else:
            if state.get("status") != "batch_approved":
                raise ValueError("pages 2..N require explicit user approval of both the plan and first-page sample")
            approval = state.get("explicit_approval")
            if not isinstance(approval, dict) or approval.get("actor") != "user" or not str(approval.get("text", "")).strip():
                raise ValueError("explicit user approval evidence is missing")
            sample_path = Path(state.get("sample_path", ""))
            verify_locked(sample_path, state.get("sample_sha256"), "registered composed first-page sample")
            sample_plate = Path(state.get("sample_plate_path", ""))
            verify_locked(sample_plate, state.get("sample_plate_sha256"), "registered normalized sample plate")
            renderer = state.get("renderer_record")
            if not isinstance(renderer, dict):
                raise ValueError("validated renderer receipt is required before batch rendering")
            renderer_path = Path(str(renderer.get("path", "")))
            verify_locked(renderer_path, renderer.get("sha256"), "renderer record")
            receipt = load_renderer_receipt(renderer_path)
            receipt_errors = validate_renderer_receipt(receipt, check_files=True, require_rendered_output=True)
            if receipt_errors:
                raise ValueError("renderer record is invalid: " + "; ".join(receipt_errors))
            verify_receipt_scope(receipt, plan, state.get("sample_page"))
            plate_evidence = (str(sample_plate.resolve()), state.get("sample_plate_sha256"))
            outputs = {
                (str(Path(str(entry.get("path", ""))).resolve()), entry.get("sha256"))
                for entry in receipt.get("rendered_outputs", []) if isinstance(entry, dict)
            }
            if plate_evidence not in outputs:
                raise ValueError("renderer record does not hash-lock the approved sample plate")
            verify_sample(state)
            if plan.get("sample_style_contract", {}).get("generated_page_is_style_reference") is not False:
                raise ValueError("sample style contract must forbid using a generated page as a style reference")
            verify_batch_inputs(plan, pages)
            expected_sample = pages[0].get("page")
            expected_batch = [page.get("page") for page in pages[1:]]
            if state.get("sample_page") != expected_sample:
                raise ValueError("approval state sample page does not match the first render-plan page")
            if state.get("permitted_render_pages") != expected_batch or state.get("blocked_render_pages") != []:
                raise ValueError("approval state authorization scope does not exactly match pages 2..N")
            selected = [page for page in pages if page.get("page") in state["permitted_render_pages"]]
            gate_note = (
                "Explicit approval verified; render only pages 2..N from this scope."
                if selected else
                "Explicit approval verified; this is a one-page carousel, so no additional render is required."
            )
    except ValueError as exc:
        print(f"Render scope blocked: {exc}", file=sys.stderr)
        return 3

    scoped = copy.deepcopy(plan)
    scoped.setdefault("review_gate", {}).update({
        "status": state.get("status"),
        "permitted_render_pages": [page.get("page") for page in selected],
        "explicit_approval_verified": args.mode == "batch",
    })
    scoped["render_scope"] = {
        "mode": args.mode,
        "page_numbers": [page.get("page") for page in selected],
        "gate_status": state.get("status"),
        "instruction": gate_note,
    }
    scoped["pages"] = selected
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scoped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.mode} render scope for pages {scoped['render_scope']['page_numbers']} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
