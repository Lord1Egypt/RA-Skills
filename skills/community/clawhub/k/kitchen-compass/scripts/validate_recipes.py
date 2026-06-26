#!/usr/bin/env python3
from __future__ import annotations

import argparse

from paths import KitchenCompassPaths, resolve_data_root
from validation import validate_recipe_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Kitchen Compass recipe markdown files against the portable v1 contract."
    )
    parser.add_argument(
        "--data-root",
        help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    recipe_paths = sorted(path for path in paths.recipes_dir.glob("*.md") if not path.name.startswith("_"))

    if not recipe_paths:
        print(f"No recipe files found under {paths.recipes_dir}.")
        return

    failures = validate_recipe_paths(recipe_paths)

    print(f"Validated {len(recipe_paths)} recipe file(s) under {paths.recipes_dir}.")
    if not failures:
        print("[OK] All recipes passed validation.")
        return

    print(f"[ERROR] {len(failures)} recipe file(s) failed validation.")
    for recipe_path, errors in failures:
        print(f"- {recipe_path.relative_to(paths.data_root)}")
        for error in errors:
            print(f"  - {error}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
