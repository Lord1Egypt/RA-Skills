#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from paths import KitchenCompassPaths, resolve_data_root, skill_root, write_atomic

SAMPLE_ROOT = skill_root() / "assets" / "sample-household"
RECIPE_TEMPLATE = skill_root() / "assets" / "recipe-template.md"
INVENTORY_STUB = '{\n  "version": 1,\n  "updated_at": null,\n  "items": []\n}\n'


def write_file(target: Path, content: str, force: bool) -> str:
    if target.exists() and not force:
        return "skipped"
    write_atomic(target, content)
    return "wrote"


def copy_sample_tree(target_root: Path, force: bool) -> list[str]:
    if not SAMPLE_ROOT.exists():
        raise SystemExit(f"Missing skill sample tree: {SAMPLE_ROOT}")

    actions: list[str] = []
    for source in sorted(SAMPLE_ROOT.rglob("*")):
        relative = source.relative_to(SAMPLE_ROOT)
        target = target_root / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        status = write_file(target, source.read_text(), force)
        actions.append(f"{status}: {target}")
    return actions


def bootstrap(data_root: Path, force: bool) -> list[str]:
    paths = KitchenCompassPaths.from_root(data_root)
    paths.ensure_runtime_dirs()

    actions = copy_sample_tree(paths.data_root, force)
    template_target = paths.recipes_dir / "_recipe-template.md"
    actions.append(f"{write_file(template_target, RECIPE_TEMPLATE.read_text(), force)}: {template_target}")

    if not paths.history_file.exists() or force:
        actions.append(f"{write_file(paths.history_file, '', force)}: {paths.history_file}")
    if not paths.inventory_items_file.exists() or force:
        actions.append(f"{write_file(paths.inventory_items_file, INVENTORY_STUB, force)}: {paths.inventory_items_file}")
    if not paths.inventory_transactions_file.exists() or force:
        actions.append(f"{write_file(paths.inventory_transactions_file, '', force)}: {paths.inventory_transactions_file}")

    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a portable Kitchen Compass household data tree from the skill assets.")
    parser.add_argument("--data-root", help="Target user-data directory. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing sample files if they already exist.")
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = resolve_data_root(args.data_root, verbose=args.verbose)
    actions = bootstrap(data_root, force=args.force)
    print(f"Initialized Kitchen Compass data root: {data_root}")
    for action in actions:
        print(f"- {action}")


if __name__ == "__main__":
    main()
