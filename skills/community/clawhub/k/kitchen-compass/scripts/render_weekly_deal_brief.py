#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deals import (
    load_stores_config,
    normalize_weekly_deal_input,
    render_weekly_deal_brief_markdown,
)
from paths import KitchenCompassPaths, resolve_data_root, write_atomic



def write_text(path: Path, content: str) -> None:
    write_atomic(path, content)



def write_json(path: Path, payload: dict) -> None:
    write_text(path, json.dumps(payload, indent=2) + "\n")



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a manual weekly Kitchen Compass deal brief from saved store setup plus a curated input file.")
    parser.add_argument(
        "--data-root",
        help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--input", help="Curated weekly deal brief input JSON. Defaults to deals/weekly-deal-brief-input.json under the data root.")
    parser.add_argument("--output-json", help="Write normalized brief JSON here. Defaults to generated/deals/weekly-deal-brief-latest.json.")
    parser.add_argument("--output-markdown", help="Write rendered markdown here. Defaults to generated/deals/weekly-deal-brief-latest.md.")
    parser.add_argument("--json", action="store_true", help="Print the normalized brief JSON instead of markdown.")
    parser.add_argument("--stdout", action="store_true", help="Also print the rendered output to stdout after writing files.")
    return parser



def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    stores_config = load_stores_config(paths)

    input_path = Path(args.input).expanduser().resolve() if args.input else paths.deal_brief_input_file
    if not input_path.exists():
        raise SystemExit(f"Weekly deal brief input file not found: {input_path}")

    raw_payload = json.loads(input_path.read_text())
    brief = normalize_weekly_deal_input(raw_payload, stores_config)
    markdown = render_weekly_deal_brief_markdown(brief)

    output_json = Path(args.output_json).expanduser().resolve() if args.output_json else paths.generated_deals_dir / "weekly-deal-brief-latest.json"
    output_markdown = Path(args.output_markdown).expanduser().resolve() if args.output_markdown else paths.generated_deals_dir / "weekly-deal-brief-latest.md"
    write_json(output_json, brief)
    write_text(output_markdown, markdown)

    if args.json:
        print(json.dumps(brief, indent=2))
    elif args.stdout or not args.output_markdown:
        print(markdown)


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
