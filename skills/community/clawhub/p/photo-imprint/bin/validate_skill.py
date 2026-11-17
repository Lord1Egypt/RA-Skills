#!/usr/bin/env python3
"""Validate all carousel presets, profiles, and style reference metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from resolve_config import (
    CONCERNS,
    PROFILE_DIRS,
    load_json,
    resolve_preset,
    validate_reference_asset,
    validate_reference_metadata,
)
from workflow_contracts import validate_style_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Print a JSON report")
    args = parser.parse_args()
    root = args.skill_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    counts = {"presets": 0, "profiles": 0, "style_references": 0, "workflow_gate_files": 0}

    required_review_gate_files = (
        "bin/build_production_plan.py", "bin/review_gate.py", "bin/render_scope.py",
        "bin/clean_plate.py", "bin/compose.py", "bin/renderer_receipt.py",
        "bin/check_environment.py", "bin/workflow.py", "bin/review_checklist.py",
        "bin/revision_scope.py", "bin/package_verified.py", "requirements.txt",
        "references/review-gate.md", "references/quality-checks.md",
        "tests/fixtures/generic-visual-cases.json",
    )
    for relative in required_review_gate_files:
        path = root / relative
        if path.is_file():
            counts["workflow_gate_files"] += 1
        else:
            errors.append(f"missing mandatory review-gate file: {path}")

    ids: dict[str, set[str]] = {concern: set() for concern in CONCERNS}
    for concern, folder in PROFILE_DIRS.items():
        directory = root / "profiles" / folder
        if not directory.is_dir():
            errors.append(f"missing profile directory: {directory}")
            continue
        for path in sorted(directory.glob("*.json")):
            counts["profiles"] += 1
            try:
                profile = load_json(path)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if profile.get("profile_type") != concern:
                errors.append(f"{path}: expected profile_type '{concern}'")
            profile_id = profile.get("id")
            if not isinstance(profile_id, str) or not profile_id:
                errors.append(f"{path}: missing id")
            elif profile_id in ids[concern]:
                errors.append(f"duplicate {concern} id: {profile_id}")
            else:
                ids[concern].add(profile_id)
            if profile_id and path.stem != profile_id:
                errors.append(f"{path}: filename must match id '{profile_id}'")

            if concern == "style":
                for message in validate_style_contract(profile.get("sample_style_contract_defaults"), f"{path}.sample_style_contract_defaults"):
                    errors.append(message)
                cleanup = profile.get("plate_normalization")
                if not isinstance(cleanup, dict) or cleanup.get("mode") not in {"paper-key-soft", "alpha-required", "disabled"}:
                    errors.append(f"{path}: plate_normalization.mode must be paper-key-soft, alpha-required, or disabled")
                references = profile.get("references")
                if references == [] and profile.get("reference_status") == "pending-selection":
                    warnings.append(f"style references pending selection: {profile_id}")
                    continue
                if not isinstance(references, list) or not references:
                    errors.append(
                        f"{path}: style requires a non-empty references array, "
                        "or reference_status 'pending-selection'"
                    )
                    continue

                seen_reference_ids = set()
                for index, reference in enumerate(references, start=1):
                    if not isinstance(reference, dict):
                        errors.append(f"{path}: reference {index} must be an object")
                        continue
                    reference_id = reference.get("id")
                    ref_rel = reference.get("image")
                    source_rel = reference.get("source_metadata")
                    roles = reference.get("technique_roles")
                    if not isinstance(reference_id, str) or not reference_id:
                        errors.append(f"{path}: reference {index} requires id")
                    elif reference_id in seen_reference_ids:
                        errors.append(f"{path}: duplicate reference id '{reference_id}'")
                    else:
                        seen_reference_ids.add(reference_id)
                    if not isinstance(ref_rel, str) or not isinstance(source_rel, str):
                        errors.append(f"{path}: reference {reference_id or index} requires image and source_metadata")
                        continue
                    if not isinstance(roles, list) or not roles or not all(isinstance(role, str) and role for role in roles):
                        errors.append(f"{path}: reference {reference_id or index} requires technique_roles")

                    ref_path, source_path = root / ref_rel, root / source_rel
                    source = None
                    try:
                        source = load_json(source_path)
                        errors.extend(validate_reference_metadata(reference, source, source_path))
                        if source.get("redistributable") is not True:
                            warnings.append(f"private reference: {profile_id}/{reference_id}")
                    except ValueError as exc:
                        errors.append(str(exc))

                    if not ref_path.is_file():
                        is_unbundled = bool(source and source.get("bundled") is False)
                        if is_unbundled:
                            warnings.append(f"unbundled style reference: {profile_id}/{reference_id}")
                        else:
                            errors.append(f"missing reference: {ref_path}")
                    else:
                        counts["style_references"] += 1
                        if source is not None:
                            errors.extend(validate_reference_asset(ref_path, source, source_path))

    preset_paths = sorted((root / "presets").glob("*.json"))
    if not preset_paths:
        errors.append("no presets found")
    with TemporaryDirectory() as temp:
        for preset in preset_paths:
            counts["presets"] += 1
            try:
                resolved, preset_warnings = resolve_preset(
                    root,
                    preset,
                    allow_missing_unbundled_reference=True,
                )
                Path(temp, f"{resolved['preset']}.json").write_text(json.dumps(resolved), encoding="utf-8")
                defaults = resolved.get("workflow_defaults", {})
                if resolved.get("preset") == "travel-food-journal":
                    required_defaults = {
                        "ordering", "plan", "approval", "renderer", "composition",
                        "plate_pipeline", "qa", "revision", "packaging"
                    }
                    missing_defaults = sorted(required_defaults - set(defaults))
                    if missing_defaults:
                        errors.append(f"{preset}: default workflow missing {', '.join(missing_defaults)}")
                    watermark = resolved.get("modules", {}).get("watermark", {})
                    if watermark.get("enabled") is not False or watermark.get("text"):
                        errors.append(f"{preset}: reusable default watermark must be disabled and empty")
                    renderer = defaults.get("renderer", {})
                    if renderer.get("backend_configured_by_default") is not False:
                        errors.append(f"{preset}: reusable default must not claim a renderer backend")
                    if renderer.get("validated_receipt_required_for_rendered_output") is not True:
                        errors.append(f"{preset}: rendered outputs must require a validated renderer receipt")
                    if renderer.get("external_reference_processing_requires_explicit_consent") is not True:
                        errors.append(f"{preset}: external reference processing must require explicit consent")
                    if defaults.get("composition", {}).get("strip_exif_gps_xmp") is not True:
                        errors.append(f"{preset}: deterministic outputs must strip EXIF/GPS/XMP")
                warnings.extend(f"{preset.name}: {message}" for message in preset_warnings)
            except ValueError as exc:
                errors.append(f"{preset}: {exc}")

    report = {"ok": not errors, "counts": counts, "warnings": sorted(set(warnings)), "errors": errors}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            f"Presets: {counts['presets']}; profiles: {counts['profiles']}; "
            f"style references: {counts['style_references']}; workflow-gate files: {counts['workflow_gate_files']}"
        )
        for warning in report["warnings"]:
            print(f"Warning: {warning}")
        if errors:
            print("Errors:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
        else:
            print("Skill validation passed")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
