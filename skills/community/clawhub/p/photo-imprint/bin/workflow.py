#!/usr/bin/env python3
"""Read-only workflow status/next-step reporter.

The reporter recognizes conventional project filenames and never performs a
transition.  In particular, approval state is reported rather than inferred.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from renderer_receipt import load as load_receipt, validate as validate_receipt


def read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def numbered_pages(directory: Path) -> set[int]:
    pages: set[int] = set()
    if not directory.is_dir():
        return pages
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in {".png", ".webp", ".jpg", ".jpeg"} and path.stem.isdigit():
            pages.add(int(path.stem))
    return pages


def inspect(project: Path) -> dict[str, Any]:
    full_receipt = project / "full-renderer-receipt.json"
    legacy_receipt = project / "renderer-receipt.json"
    # Support both project/ and project/work/ layouts — SKILL.md uses work/
    work = project / "work"
    def pick(name: str, *alts: Path) -> Path:
        for p in alts:
            if p.is_file():
                return p
        return alts[0]
    names = {
        "resolved_config": pick("resolved_config", work / "resolved-config.json", project / "resolved-config.json"),
        "manifest": pick("manifest", work / "manifest.json", project / "manifest.json"),
        "render_plan": pick("render_plan", work / "render-plan.json", project / "render-plan.json"),
        "production_plan": pick("production_plan", work / "production-plan.md", project / "production-plan.md"),
        "approval_state": pick("approval_state", work / "approval-state.json", project / "approval-state.json"),
        "renderer_receipt": full_receipt if full_receipt.is_file() else legacy_receipt,
        "composition_manifest": pick("composition_manifest", work / "composition-manifest.json", project / "final" / "composition-manifest.json"),
        "review_checklist": pick("review_checklist", work / "review-checklist.json", project / "qa" / "review-checklist.json"),
        "staging_manifest": pick("staging_manifest", work / "staging-manifest.json", project / "staging-manifest.json"),
        "release": project / "dist" / "carousel.zip",
    }
    files = {key: path.is_file() for key, path in names.items()}
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "project": str(project.resolve()),
        "read_only": True,
        "gate_bypassed": False,
        "files": files,
        "gate_status": None,
        "blocked_render_pages": [],
        "next": None,
        "reason": None,
    }
    if not project.is_dir():
        result.update(next="create_project", reason="project directory does not exist")
        return result
    if not files["resolved_config"]:
        result.update(next="resolve_config", reason="resolved-config.json is missing")
        return result
    if not files["manifest"]:
        result.update(next="preprocess_sources", reason="manifest.json is missing")
        return result
    if not files["render_plan"]:
        result.update(next="build_render_plan", reason="render-plan.json is missing")
        return result
    plan = read_object(names["render_plan"], "render plan")
    pages = plan.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("render-plan.json has no pages")
    page_numbers = [page.get("page") for page in pages if isinstance(page, dict)]
    if len(page_numbers) != len(pages) or not all(isinstance(page, int) and page > 0 for page in page_numbers):
        raise ValueError("render-plan.json has invalid page numbers")
    result["planned_pages"] = page_numbers
    if not files["production_plan"] or not files["approval_state"]:
        result.update(next="build_production_plan", reason="production plan or approval state is missing")
        return result
    state = read_object(names["approval_state"], "approval state")
    gate = state.get("status")
    result["gate_status"] = gate
    blocked = state.get("blocked_render_pages", [])
    result["blocked_render_pages"] = blocked if isinstance(blocked, list) else []

    receipt_state = "missing"
    receipt_valid = False
    receipt_output_pages: set[int] = set()
    if files["renderer_receipt"]:
        receipt = load_receipt(names["renderer_receipt"])
        receipt_state = str(receipt.get("status"))
        receipt_errors = validate_receipt(receipt, check_files=True, require_rendered_output=False)
        receipt_valid = not receipt_errors
        result["renderer_receipt_errors"] = receipt_errors
        if receipt_valid:
            for entry in receipt.get("rendered_outputs", []):
                if not isinstance(entry, dict):
                    continue
                name = str(entry.get("name", ""))
                match = re.fullmatch(r"(?:page-)?(\d+)", name)
                if match:
                    receipt_output_pages.add(int(match.group(1)))
                    continue
                path_value = entry.get("path")
                if isinstance(path_value, str) and Path(path_value).stem.isdigit():
                    receipt_output_pages.add(int(Path(path_value).stem))
    result["renderer_receipt_status"] = receipt_state
    result["renderer_receipt_valid"] = receipt_valid

    if gate == "plan_ready_sample_not_registered":
        if receipt_state in {"missing", "renderer_not_configured"}:
            result.update(next="configure_renderer", reason="a valid rendered-output receipt does not exist")
        elif not receipt_valid:
            result.update(next="repair_renderer_receipt", reason="renderer receipt is invalid")
        else:
            sample = state.get("sample_page", page_numbers[0])
            if sample not in receipt_output_pages:
                result.update(next="render_sample", reason="valid receipt does not register the sample page output")
                return result
            composed = project / "sample" / f"{int(sample):02d}.png"
            if not composed.is_file():
                result.update(next="compose_sample", reason="renderer output is registered but composed sample is missing")
            else:
                result.update(next="register_sample", reason="sample exists but is not registered in the review gate")
        return result
    if gate == "sample_ready_not_shown":
        result.update(next="present_plan_and_sample", reason="plan decisions and sample must be discussed together")
        return result
    if gate == "awaiting_explicit_user_approval":
        result.update(next="await_explicit_user_approval", reason="pages 2..N remain blocked until explicit approval")
        return result
    if gate in {"gate_invalidated_by_revision"}:
        result.update(next="rebuild_and_review_sample", reason="a shared/sample change invalidated prior approval")
        return result
    if gate not in {"batch_approved", "revision_in_progress", "revision_completed"}:
        result.update(next="inspect_gate_state", reason=f"unrecognized or non-runnable gate status: {gate!r}")
        return result

    composed_pages = numbered_pages(project / "final")
    missing_composed = sorted(set(page_numbers) - composed_pages)
    result["composed_pages"] = sorted(composed_pages)
    if missing_composed:
        if not receipt_valid or not set(missing_composed).issubset(receipt_output_pages):
            result.update(next="render_approved_pages", reason=f"approved pages lack valid renderer outputs: {missing_composed}")
        else:
            result.update(next="compose_approved_pages", reason=f"renderer outputs exist but composed pages are missing: {missing_composed}")
        return result
    if not files["composition_manifest"]:
        result.update(next="repair_composition", reason="complete pages lack the required composition manifest")
        return result
    if not files["review_checklist"]:
        result.update(next="run_qa", reason="complete composed set has no review checklist")
        return result
    checklist = read_object(names["review_checklist"], "review checklist")
    page_status = checklist.get("page_level_compliance", {}).get("status")
    set_status = checklist.get("set_level_cohesion", {}).get("status")
    if page_status != "pass" or set_status != "pass":
        result.update(next="complete_qa_review", reason="page-level and set-level QA must both pass")
        return result
    if not files["staging_manifest"]:
        result.update(next="stage_verified_outputs", reason="QA passed but staging hashes are not locked")
        return result
    if not files["release"]:
        result.update(next="package_verified", reason="verified staging is ready for packaging")
        return result
    result.update(next="complete", reason="release exists after approval, QA, and staging gates")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only carousel workflow status reporter")
    parser.add_argument("command", choices=("status", "next"))
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = inspect(args.project)
        if args.command == "status":
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({
                "next": report["next"],
                "reason": report["reason"],
                "gate_status": report["gate_status"],
                "blocked_render_pages": report["blocked_render_pages"],
                "gate_bypassed": False,
                "read_only": True,
            }, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError) as exc:
        print(f"Workflow status blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
