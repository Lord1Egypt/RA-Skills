#!/usr/bin/env python3
"""Build deterministic per-page render briefs from a resolved config and manifest."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_contracts import digest, load_object, validate_production_brief, validate_style_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path, help="Resolved config JSON")
    parser.add_argument("--manifest", required=True, type=Path, help="Preprocessed manifest JSON")
    parser.add_argument("--output", required=True, type=Path, help="Render plan JSON")
    parser.add_argument("--allow-unconfirmed", action="store_true", help="Build a non-renderable draft plan")
    args = parser.parse_args()
    try:
        config = load_object(args.config, "config")
        manifest = load_object(args.manifest, "manifest")
        if config.get("resolved") is not True:
            raise ValueError("config was not produced by resolve_config.py")
        if manifest.get("preset") and manifest.get("preset") != config.get("preset"):
            raise ValueError("manifest and config preset ids do not match")
        items = manifest.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError("manifest.items must be a non-empty array")
    except ValueError as exc:
        print(f"Render-plan validation failed: {exc}", file=sys.stderr)
        return 2

    profiles = config["profiles"]
    theme, style, layers, composition = (profiles[name] for name in ("theme", "style", "layers", "composition"))
    modules = config.get("modules", {})
    canvas = composition["canvas"]
    flow = composition["subject"].get("horizontal_flow", ["center"])
    contract = manifest.get("sample_style_contract") or style.get("sample_style_contract_defaults")

    unresolved = validate_style_contract(contract)
    caption_fields = modules.get("caption", {}).get("lines", []) if modules.get("caption", {}).get("enabled") else []
    manifest_field = {"date": "date_label"}
    for index, item in enumerate(items, start=1):
        page = item.get("page", index) if isinstance(item, dict) else index
        if not isinstance(item, dict):
            unresolved.append(f"page {page}: item is not an object")
            continue
        if not item.get("capture_time"):
            unresolved.append(f"page {page}: capture time/order is unconfirmed")
        missing = [field for field in caption_fields if not item.get(manifest_field.get(field, field))]
        if missing:
            unresolved.append(f"page {page}: missing caption fields {', '.join(missing)}")
        unresolved.extend(f"page {page}: {msg}" for msg in validate_production_brief(item.get("production_brief")))
    if unresolved and not args.allow_unconfirmed:
        print("Render-plan validation failed:\n- " + "\n- ".join(unresolved), file=sys.stderr)
        return 2

    style_subject_exclusions = [
        exclusion
        for reference in style.get("references", [])
        if isinstance(reference, dict)
        for exclusion in reference.get("subject_exclusions", [])
        if isinstance(exclusion, str) and exclusion
    ]
    global_forbidden = list(dict.fromkeys(
        list(theme.get("forbid_invention", [])) +
        list(layers.get("layers", {}).get("subject", {}).get("forbidden_content", [])) +
        style_subject_exclusions
    ))
    pages = []
    for index, item in enumerate(items):
        placement = flow[index % len(flow)] if flow else "center"
        brief = item.get("production_brief") if isinstance(item.get("production_brief"), dict) else {}
        anchors = brief.get("preserve_anchors", [])
        omissions = brief.get("abstract_or_omit", [])
        cues = brief.get("material_depth_cues", [])
        inventions = brief.get("forbidden_inventions", [])
        structures = brief.get("structural_lines", [])
        structure_text = "; ".join(
            f"{entry.get('element')} [{entry.get('operation')}]" for entry in structures if isinstance(entry, dict)
        )
        contract_prompt = " ".join([
            "Approved sample style contract:",
            "mark/edge=" + "; ".join((contract or {}).get("mark_edge_quality", [])) + ".",
            "negative space=" + "; ".join((contract or {}).get("negative_space_rules", [])) + ".",
            "fill/tonal=" + "; ".join((contract or {}).get("fill_tonal_rules", [])) + ".",
            "background=" + "; ".join((contract or {}).get("background_cleanliness", [])) + ".",
            "frame/border=" + str((contract or {}).get("frame_border_policy")) + ".",
            "abstraction=" + str((contract or {}).get("abstraction_level")) + ".",
            "The generated sample is evidence of approval, never a style-reference image."
        ])
        prompt_parts = (
            theme.get("prompt_fragment", ""), style.get("positive_prompt", ""), contract_prompt,
            f"Subject priority: {brief.get('subject_priority')}." if brief.get("subject_priority") else "",
            f"Thumbnail read: {brief.get('thumbnail_read')}." if brief.get("thumbnail_read") else "",
            "Preserve anchors: " + "; ".join(anchors) + "." if anchors else "",
            "Material/depth cues: " + "; ".join(cues) + "." if cues else "",
            "Source-grounded structural lines: " + structure_text + "." if structure_text else "",
            "Abstract or omit: " + "; ".join(omissions) + "." if omissions else "",
            "Forbidden inventions: " + "; ".join(inventions) + "." if inventions else "",
            f"Render only the clean subject layer on transparency for a {canvas['width']}x{canvas['height']} composition.",
            f"Place the subject toward the {placement} in the lower portion; leave the composition profile's top whitespace empty.",
            layers.get("render_rule", ""),
        )
        negative = style.get("negative_prompt", "").rstrip(". ")
        all_forbidden = list(dict.fromkeys(global_forbidden + inventions))
        if all_forbidden:
            negative += ". Do not invent or render: " + ", ".join(all_forbidden)
        pages.append({
            "page": item.get("page", index + 1), "source_path": item.get("source_path"),
            "source_sha256": item.get("sha256"), "capture_time": item.get("capture_time"),
            "placement": placement, "production_brief": brief,
            "render_prompt": " ".join(part.strip() for part in prompt_parts if part),
            "negative_prompt": negative.strip() + ".",
            "plate_contract": {
                "format": "PNG", "width": canvas["width"], "height": canvas["height"],
                "transparent_background": layers.get("layers", {}).get("subject", {}).get("transparent", True),
                "contains_only": "subject",
                "normalization_policy": style.get("plate_normalization", {}),
            },
            "caption_data": {"location": item.get("location"), "subject": item.get("subject"), "date": item.get("date_label")}
                if modules.get("caption", {}).get("enabled") else None,
            "caption_status": item.get("caption_status", {}), "notes": item.get("notes"),
        })

    numbers = [page["page"] for page in pages]
    skill_root = Path(__file__).resolve().parents[1]
    reference_locks = []
    for reference in style.get("references", []):
        image = Path(str(reference.get("image", "")))
        metadata = Path(str(reference.get("source_metadata", "")))
        image = image if image.is_absolute() else skill_root / image
        metadata = metadata if metadata.is_absolute() else skill_root / metadata
        reference_locks.append({
            "id": reference.get("id"), "image_path": str(image.resolve()),
            "image_sha256": digest(image) if image.is_file() else None,
            "source_metadata_path": str(metadata.resolve()),
            "source_metadata_sha256": digest(metadata) if metadata.is_file() else None,
            "technique_roles": reference.get("technique_roles", []),
            "subject_exclusions": reference.get("subject_exclusions", []),
        })
    plan = {
        "schema_version": "2.0.0", "preset": config.get("preset"),
        "resolved_config_lock": {"path": str(args.config.resolve()), "sha256": digest(args.config.resolve())},
        "profile_ids": {key: value.get("id") for key, value in profiles.items()},
        "style_references": style.get("references", []), "style_reference_locks": reference_locks,
        "sample_style_contract": contract,
        "workflow_defaults": config.get("workflow_defaults", {}),
        "layer_order": layers.get("z_order"), "composition": composition, "modules": modules,
        "deterministic_finish_contract": {
            "apply_after_subject_render": True, "shared_background": True,
            "typography_generated_by_model": False,
            "cross_slide_route_assembled_before_crop": bool(modules.get("route", {}).get("enabled")),
        },
        "review_gate": {"status": "sample_only", "production_plan_required": True,
            "sample_page": numbers[0], "permitted_before_approval": [numbers[0]],
            "blocked_before_approval": numbers[1:], "explicit_user_approval_required": True,
            "inferred_acceptance_forbidden": True},
        "pages": pages,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote render plan for {len(pages)} pages to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
