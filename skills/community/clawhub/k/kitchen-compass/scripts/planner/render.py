from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from paths import KitchenCompassPaths, write_atomic

from planner.core import build_plan
from planner.presets import PRESETS


def render_plan_markdown(plan: dict[str, Any]) -> str:
    lines = [f"# {plan['preset_label']}", "", plan["description"], ""]
    lines.append(f"- Target dinners: {plan['dinners_per_week']}")
    lines.append(f"- Picked dinners: {plan['picked_count']}")
    lines.append(f"- Protein variety: {json.dumps(plan['summary']['protein_variety'], sort_keys=True)}")
    lines.append(f"- Role mix: {json.dumps(plan['summary']['role_mix'], sort_keys=True)}")
    lines.append(f"- Effort mix: {json.dumps(plan['summary']['effort_mix'], sort_keys=True)}")
    lines.append(f"- Friction mix: {json.dumps(plan['summary']['friction_mix'], sort_keys=True)}")
    inventory_summary = plan.get("inventory_summary") or {}
    lines.append(f"- Inventory items available: {inventory_summary.get('available_item_count', 0)}")
    lines.append(f"- Picks helped by inventory: {inventory_summary.get('supported_pick_count', 0)}")
    history_summary = plan.get("history_summary")
    if history_summary:
        lines.append(f"- History anchor date: {history_summary['anchor_date']}")
        lines.append(f"- Recent dinner events considered: {history_summary['recent_event_count']}")
        lines.append(f"- Recent protein counts: {json.dumps(history_summary['recent_protein_counts'], sort_keys=True)}")
        lines.append(f"- Recent role counts: {json.dumps(history_summary['recent_role_counts'], sort_keys=True)}")
    lines.append("")
    for idx, pick in enumerate(plan["picks"], start=1):
        lines.append(f"## Dinner {idx} — {pick['title']}")
        lines.append(f"- Why it made the cut: {'; '.join(pick['reasons'])}")
        lines.append(
            f"- Planning profile: {pick['effort']} effort, {pick['ingredient_friction']} friction, {pick['cost']} cost, {pick['status']}, {pick['serving_profile']}, role={pick['primary_structural_role']}"
        )
        if pick.get("last_seen"):
            lines.append(f"- Last seen in history: {pick['last_seen']}")
        lines.append(f"- Composition: {pick['composition']['note']}")
        inventory_support = pick.get('inventory_support', {})
        if inventory_support.get('total_bonus', 0) > 0:
            lines.append(
                "- Inventory support: "
                + "; ".join(
                    f"{match['explanation']} ({match['match_reason']})"
                    for match in inventory_support.get('matches', [])[:2]
                )
            )
        if pick['composition'].get('protein_add_on'):
            lines.append(f"- Protein add-on: {pick['composition']['protein_add_on']}")
        side = pick['composition'].get('side')
        if side:
            lines.append(f"- Suggested side: {side['title']} — {side['reason']}")
        lines.append(f"- Recipe: `{pick['path']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_example_bundle(
    payload: dict[str, Any],
    dinners_per_week: int,
    history_path: Path | None,
    ignore_history: bool,
    inventory_state: dict[str, Any] | None,
    prioritize_inventory: bool,
) -> dict[str, Any]:
    return {
        name: build_plan(
            payload,
            name,
            dinners_per_week,
            history_path=history_path,
            ignore_history=ignore_history,
            inventory_state=inventory_state,
            prioritize_inventory=prioritize_inventory,
        )
        for name in PRESETS
    }


def write_outputs(
    paths: KitchenCompassPaths,
    payload: dict[str, Any],
    dinners_per_week: int,
    history_path: Path | None,
    ignore_history: bool,
    inventory_state: dict[str, Any] | None,
    prioritize_inventory: bool,
) -> None:
    paths.ensure_runtime_dirs()
    bundle = build_example_bundle(payload, dinners_per_week, history_path, ignore_history, inventory_state, prioritize_inventory)
    write_atomic(paths.generated_planner_dir / "weekly-plans.json", json.dumps(bundle, indent=2) + "\n")

    overview_lines = ["# Kitchen Compass Weekly Planner v1 — Example Plans", ""]
    for name, plan in bundle.items():
        file_name = f"{name}.md"
        write_atomic(paths.planner_views_dir / file_name, render_plan_markdown(plan))
        overview_lines.append(f"- [{plan['preset_label']}](./{file_name})")
    overview_lines.append("")
    write_atomic(paths.planner_views_dir / "README.md", "\n".join(overview_lines))
