#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from inventory import load_inventory_state
from paths import KitchenCompassPaths, resolve_data_root

from planner import (
    PRESETS,
    build_plan,
    can_add,
    load_catalog,
    planner_defaults,
    render_plan_markdown,
    score_recipe,
    write_outputs,
)

__all__ = ["PRESETS", "build_plan", "can_add", "score_recipe", "render_plan_markdown", "write_outputs"]


def build_parser() -> argparse.ArgumentParser:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "--data-root",
        help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.",
    )
    pre_parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    pre_args, _ = pre_parser.parse_known_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(pre_args.data_root, verbose=pre_args.verbose))
    default_preset, default_dinners_per_week, default_prioritize_inventory = planner_defaults(paths)

    parser = argparse.ArgumentParser(description="Build lean weekly dinner plans from the portable Kitchen Compass query catalog.", parents=[pre_parser])
    parser.add_argument("--preset", choices=sorted(PRESETS), default=default_preset)
    parser.add_argument("--dinners-per-week", type=int, default=default_dinners_per_week)
    parser.add_argument("--include-aspirational", action="store_true", help="Allow aspirational dinners into the candidate pool.")
    parser.add_argument("--json", action="store_true", help="Print plan JSON instead of markdown.")
    parser.add_argument("--write-views", action="store_true", help="Write example planner outputs for all presets under generated/planner/.")
    parser.add_argument("--history-file", help="Override the meal history JSONL path.")
    parser.add_argument("--ignore-history", action="store_true", help="Disable history-aware scoring for this run.")
    inventory_group = parser.add_mutually_exclusive_group()
    inventory_group.add_argument("--prioritize-inventory", dest="prioritize_inventory", action="store_true", help="Increase the weight of strong inventory matches without overriding hard planner constraints.")
    inventory_group.add_argument("--no-prioritize-inventory", dest="prioritize_inventory", action="store_false", help="Keep inventory as a light planning nudge.")
    parser.set_defaults(prioritize_inventory=default_prioritize_inventory)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    payload = load_catalog(paths.generated_query_dir / "recipe-catalog.json")
    history_path = Path(args.history_file).expanduser().resolve() if args.history_file else paths.history_file
    inventory_state = load_inventory_state(paths)

    if args.write_views:
        write_outputs(paths, payload, args.dinners_per_week, history_path, args.ignore_history, inventory_state, args.prioritize_inventory)

    plan = build_plan(
        payload,
        args.preset,
        args.dinners_per_week,
        include_aspirational=args.include_aspirational,
        history_path=history_path,
        ignore_history=args.ignore_history,
        inventory_state=inventory_state,
        prioritize_inventory=args.prioritize_inventory,
    )
    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(render_plan_markdown(plan))


if __name__ == "__main__":
    main()
