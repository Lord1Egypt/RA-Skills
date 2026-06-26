#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import date
from pathlib import Path

from deals import (
    deal_store_by_id,
    default_weekly_deal_store_ids,
    load_stores_config,
    normalize_brief_source,
    save_weekly_deal_input,
)
from paths import KitchenCompassPaths, resolve_data_root, write_atomic


def build_store_brief_stub(week_of: str, store: dict) -> dict:
    return {
        "version": 1,
        "week_of": week_of,
        "store_id": store["id"],
        "source": normalize_brief_source(None, store),
        "curated_by": "manual",
        "notes": "Curate only the relevant deals for this store this week. The combined sheet will group them by display category.",
        "items": [],
    }



def write_stub(path: Path, payload: dict, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return "skipped"
    save_weekly_deal_input(path, payload)
    return "wrote"



def build_scan_packet(paths: KitchenCompassPaths, config: dict, week_of: str, store_ids: list[str], stub_statuses: dict[str, str]) -> dict:
    weekly = config.get("weekly_deal_brief", {})
    stores = []
    for store_id in store_ids:
        store = deal_store_by_id(config, store_id)
        if not store:
            continue
        stores.append(
            {
                "store_id": store["id"],
                "store_label": store["label"],
                "retailer": store["retailer"],
                "source": store.get("source", {}),
                "retrieval_recipe": store.get("retrieval_recipe", {}),
                "input_file": str(Path("deals") / "store-briefs" / f"{store['id']}.json"),
                "stub_status": stub_statuses.get(store['id'], "unknown"),
            }
        )
    return {
        "version": 1,
        "week_of": week_of,
        "generated_at": date.today().isoformat(),
        "scan_schedule": weekly.get("scan_schedule", {}),
        "store_ids": store_ids,
        "stores": stores,
    }



def render_scan_packet_markdown(packet: dict) -> str:
    schedule = packet.get("scan_schedule") or {}
    lines = [
        "# Weekly Deal Scan Packet",
        "",
        f"- Week of: {packet.get('week_of') or 'not set'}",
        f"- Scan schedule: {schedule.get('day_of_week') or '-'} @ {schedule.get('time_local') or '-'} ({schedule.get('timezone') or '-'})",
        f"- Stores to scan: {', '.join(packet.get('store_ids', [])) or '-'}",
        "",
    ]
    for store in packet.get("stores", []):
        lines.append(f"## {store['store_label']}")
        lines.append("")
        lines.append(f"- Retailer: {store['retailer']}")
        lines.append(f"- Input file: {store['input_file']} ({store.get('stub_status', 'unknown')})")
        lines.append(f"- Source URL: {store.get('source', {}).get('url') or '-'}")
        recipe = store.get("retrieval_recipe") or {}
        if recipe.get("starting_url"):
            lines.append(f"- Retrieval start: {recipe['starting_url']}")
        if recipe.get("store_selector_hint"):
            lines.append(f"- Store selector hint: {recipe['store_selector_hint']}")
        if recipe.get("steps"):
            lines.append("- Steps:")
            for step in recipe.get("steps", []):
                lines.append(f"  - {step}")
        if recipe.get("known_friction"):
            lines.append(f"- Known friction: {', '.join(recipe['known_friction'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a weekly deal scan packet and per-store brief stubs for all selected stores.")
    parser.add_argument("--data-root", help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--week-of", help="Override the current week label, for example 2026-04-21.")
    parser.add_argument("--store", action="append", default=None, help="Optional store id filter. Repeat for multiple stores.")
    parser.add_argument("--force", action="store_true", help="Overwrite any existing per-store brief stubs.")
    parser.add_argument("--json", action="store_true", help="Print the scan packet as JSON instead of markdown.")
    parser.add_argument("--quiet", action="store_true", help="Print a one-line confirmation instead of the full scan packet.")
    parser.add_argument("--silent", action="store_true", help="Suppress all stdout output.")
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    paths.ensure_runtime_dirs()
    config = load_stores_config(paths)
    selected_store_ids = args.store or default_weekly_deal_store_ids(config)
    if not selected_store_ids:
        raise SystemExit("No weekly deal stores are configured yet.")
    week_of = args.week_of or date.today().isoformat()

    stub_statuses: dict[str, str] = {}
    for store_id in selected_store_ids:
        store = deal_store_by_id(config, store_id)
        if not store:
            raise SystemExit(f"Unknown weekly deal store: {store_id}")
        target = paths.deal_store_briefs_dir / f"{store_id}.json"
        stub_statuses[store_id] = write_stub(target, build_store_brief_stub(week_of, store), force=args.force)

    packet = build_scan_packet(paths, config, week_of, selected_store_ids, stub_statuses)
    write_atomic(paths.generated_deal_scan_file, json.dumps(packet, indent=2) + "\n")
    write_atomic(paths.generated_deal_scan_markdown_file, render_scan_packet_markdown(packet))

    if args.silent:
        return
    if args.quiet:
        print(f"prepared weekly deal scan for {week_of} across {len(selected_store_ids)} store(s)")
        return
    if args.json:
        print(json.dumps(packet, indent=2))
    else:
        print(render_scan_packet_markdown(packet))


if __name__ == "__main__":
    main()
