#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deals import (
    combine_weekly_deal_briefs,
    default_weekly_deal_store_ids,
    load_stores_config,
    load_weekly_deal_input,
    normalize_weekly_deal_input,
    render_combined_weekly_deal_sheet_markdown,
)
from paths import KitchenCompassPaths, resolve_data_root, write_atomic



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the combined weekly deal sheet from saved per-store weekly brief inputs.")
    parser.add_argument("--data-root", help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--store", action="append", default=None, help="Optional store id filter. Repeat for multiple stores.")
    parser.add_argument("--json", action="store_true", help="Print combined JSON instead of markdown.")
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    config = load_stores_config(paths)
    selected_store_ids = args.store or default_weekly_deal_store_ids(config)
    if not selected_store_ids:
        raise SystemExit("No weekly deal stores are configured yet.")

    briefs = []
    for store_id in selected_store_ids:
        brief_path = paths.deal_store_briefs_dir / f"{store_id}.json"
        if not brief_path.exists():
            raise SystemExit(
                f"Missing per-store brief input for {store_id}: {brief_path}. Run prepare_weekly_deal_scan.py first and curate the file."
            )
        raw = load_weekly_deal_input(brief_path)
        raw_store_id = str(raw.get("store_id") or "").strip()
        if raw_store_id and raw_store_id != store_id:
            raise SystemExit(
                f"Per-store brief mismatch: file {brief_path} is for store_id={raw_store_id}, expected {store_id}."
            )
        briefs.append(normalize_weekly_deal_input(raw, config))

    combined = combine_weekly_deal_briefs(briefs)
    write_atomic(paths.generated_combined_deal_sheet_file, json.dumps(combined, indent=2) + "\n")
    write_atomic(paths.generated_combined_deal_sheet_markdown_file, render_combined_weekly_deal_sheet_markdown(combined))

    if args.json:
        print(json.dumps(combined, indent=2))
    else:
        print(render_combined_weekly_deal_sheet_markdown(combined))


if __name__ == "__main__":
    main()
