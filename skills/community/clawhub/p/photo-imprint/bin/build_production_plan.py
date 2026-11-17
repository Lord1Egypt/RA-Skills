#!/usr/bin/env python3
"""Write the mandatory human-readable production plan and initialize its review gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workflow_contracts import digest, load_object, validate_production_brief, validate_style_contract


def md_list(values: object) -> str:
    if not isinstance(values, list) or not values:
        return "- **MISSING**"
    return "\n".join(f"- {value}" for value in values)


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def caption_summary(page: dict[str, Any], configured_lines: list[str]) -> str:
    data, statuses = page.get("caption_data") or {}, page.get("caption_status") or {}
    return "; ".join(
        f"{field}={data.get(field) if data.get(field) not in (None, '') else '—'} [{statuses.get(field) or ('proposed' if data.get(field) else 'missing')}]"
        for field in configured_lines
    ) if configured_lines else "disabled"


def validate_plan(plan: dict[str, Any]) -> list[str]:
    pages = plan.get("pages")
    if not isinstance(pages, list) or not pages:
        return ["render plan requires a non-empty pages array"]
    errors = validate_style_contract(plan.get("sample_style_contract"))
    previous = None
    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            errors.append(f"page {index} is not an object")
            continue
        number, capture = page.get("page", index), page.get("capture_time")
        if not isinstance(capture, str) or not capture:
            errors.append(f"page {number}: capture_time is required")
        elif previous is not None and capture < previous:
            errors.append(f"page {number}: capture_time is not in ascending EXIF order")
        previous = capture or previous
        errors.extend(f"page {number}: {msg}" for msg in validate_production_brief(page.get("production_brief")))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-plan", required=True, type=Path, help="Full render plan JSON")
    parser.add_argument("--output", required=True, type=Path, help="Mandatory production-plan Markdown")
    parser.add_argument("--state-output", required=True, type=Path, help="Review-gate state JSON")
    args = parser.parse_args()
    try:
        plan = load_object(args.render_plan, "render plan")
        errors = validate_plan(plan)
        if errors:
            raise ValueError("\n".join(errors))
    except ValueError as exc:
        print(f"Production-plan validation failed:\n{exc}", file=sys.stderr)
        return 2

    pages = plan["pages"]
    configured_lines = plan.get("modules", {}).get("caption", {}).get("lines", []) if plan.get("modules", {}).get("caption", {}).get("enabled") else []
    contract = plan["sample_style_contract"]
    canvas = plan.get("composition", {}).get("canvas", {})
    lines = [
        "# Carousel Production Plan", "",
        "> **Review status: DRAFT — batch rendering is blocked.**",
        "> This Markdown must exist. It may be shown directly or faithfully summarized, but its decisions and the composed first-page sample must be discussed together before approval.", "",
        "## Build summary", "",
        f"- Preset: `{plan.get('preset')}`",
        "- Profiles: " + ", ".join(f"{k}=`{v}`" for k, v in plan.get("profile_ids", {}).items()),
        f"- Canvas: {canvas.get('width')} × {canvas.get('height')} ({canvas.get('aspect_ratio')})",
        "- Page order: EXIF capture time ascending",
        f"- Sample page: {pages[0].get('page')} (`{Path(str(pages[0].get('source_path'))).name}`)", "",
        "## Frozen sample visual-method contract", "",
        "### Mark and edge quality", md_list(contract["mark_edge_quality"]), "",
        "### Negative space", md_list(contract["negative_space_rules"]), "",
        "### Fill and tonal behavior", md_list(contract["fill_tonal_rules"]), "",
        "### Background cleanliness", md_list(contract["background_cleanliness"]), "",
        f"- Frame/border policy: {contract['frame_border_policy']}",
        f"- Abstraction level: {contract['abstraction_level']}",
        "- The generated first page is approval evidence only and must never become a style-reference image.", "",
        "## Style-reference technique roles and subject exclusions", "",
    ]
    refs = plan.get("style_references", [])
    if refs:
        for ref in refs:
            identity = ref.get("id", "unnamed")
            lines.append(f"- `{identity}` technique roles: " + "; ".join(ref.get("technique_roles", [])))
            lines.append(f"- `{identity}` subject exclusions: " + "; ".join(ref.get("subject_exclusions", [])))
    else:
        lines.append("- No approved image reference is configured; text rules only.")
    lines += ["", "## Ordered page decisions", ""]
    for page in pages:
        brief = page["production_brief"]
        lines += [
            f"### Page {page.get('page')} — `{Path(str(page.get('source_path'))).name}`", "",
            f"- EXIF: {page.get('capture_time')}", f"- Placement: {page.get('placement')}",
            f"- Subject priority: {brief.get('subject_priority')}", f"- Thumbnail read: {brief.get('thumbnail_read')}",
            "- Preserve anchors:", md_list(brief.get("preserve_anchors")),
            "- Material/depth cues:", md_list(brief.get("material_depth_cues")),
            "- Source-grounded structural lines:",
        ]
        for entry in brief.get("structural_lines", []):
            lines.append(f"- {entry.get('element')} — `{entry.get('operation')}`")
        lines += [
            "- Abstract or omit:", md_list(brief.get("abstract_or_omit")),
            "- Forbidden inventions:", md_list(brief.get("forbidden_inventions")),
            f"- Caption fields/status: {caption_summary(page, configured_lines)}", "",
        ]
    lines += [
        "## First-page sample contract", "",
        f"- Render page {pages[0].get('page')} only.",
        "- Use its source photo, approved reference technique roles, page brief, and frozen visual-method contract.",
        "- Normalize and validate the clean plate before deterministic composition.",
        "- Discuss the plan decisions and composed sample together; the Markdown file itself need not be sent if its decisions are faithfully communicated.", "",
        "## Mandatory approval gate", "",
        "1. Communicate every page decision and the frozen visual-method contract, either by presenting this artifact or by a faithful summary.",
        "2. Discuss the first-page sample in the same review interaction.",
        "3. Record the presentation mode and discussion evidence with `review_gate.py mark-shown`.",
        "4. Do not infer approval from silence, reaction, or partial approval.",
        "5. Record the user's exact explicit approval before pages 2..N.", "",
        "## Acceptance dimensions", "",
        "- **Page-level compliance:** every page satisfies its own production brief and full/phone review checks.",
        "- **Set-level cohesion:** the complete ordered set passes paper, style, typography, rhythm, and overall visual-unity checks.",
        "- Packaging is blocked until both dimensions are complete and passing.", "",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    render_path = args.render_plan.resolve()
    state = {
        "schema_version": "2.0.0", "status": "plan_ready_sample_not_registered",
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "render_plan_path": str(render_path), "render_plan_sha256": digest(render_path),
        "production_plan_path": str(args.output.resolve()), "production_plan_sha256": digest(args.output.resolve()),
        "sample_style_contract_sha256": canonical_hash(contract),
        "sample_page": pages[0]["page"], "sample_path": None, "sample_sha256": None,
        "explicit_approval": None, "permitted_render_pages": [pages[0]["page"]],
        "blocked_render_pages": [page["page"] for page in pages[1:]], "revision_ledger": [],
    }
    args.state_output.parent.mkdir(parents=True, exist_ok=True)
    args.state_output.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote production plan to {args.output}")
    print(f"Initialized review gate at {args.state_output}; only page {pages[0]['page']} is permitted")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
