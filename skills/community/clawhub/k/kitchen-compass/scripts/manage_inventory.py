#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy

from contract import INVENTORY_KINDS, INVENTORY_LOCATIONS, INVENTORY_PRIORITIES
from inventory import (
    append_inventory_transaction,
    build_transaction,
    ensure_unique_item_id,
    format_quantity,
    inventory_item_by_id,
    load_inventory_state,
    normalize_inventory_item,
    quantity_dict,
    replace_inventory_item,
    save_inventory_state,
    slugify,
    subtract_quantity,
)
from paths import KitchenCompassPaths, resolve_data_root



def _report(args: argparse.Namespace, summary: str, payload: dict[str, object]) -> None:
    if args.silent:
        return
    if args.quiet:
        print(summary)
        return
    print(json.dumps(payload, indent=2))


def render_item(item: dict[str, object]) -> str:
    rules = item.get("match_rules", {})
    planning = item.get("planning", {})
    lines = [
        f"- {item['label']} [{item['id']}]",
        f"  location={item['location']} | kind={item['kind']} | quantity={format_quantity(item['quantity'])} | priority={planning.get('priority', 'normal')}",
        f"  recipe_slugs={', '.join(rules.get('recipe_slugs', [])) or '-'}",
        f"  search_terms={', '.join(rules.get('search_terms', [])) or '-'}",
        f"  core_proteins={', '.join(rules.get('core_proteins', [])) or '-'}",
    ]
    if item.get("notes"):
        lines.append(f"  notes={item['notes']}")
    return "\n".join(lines)



def add_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--item-id", help="Stable item id. Defaults to <location>-<label> slug.")
    parser.add_argument("--label")
    parser.add_argument("--location", choices=list(INVENTORY_LOCATIONS), default="freezer")
    parser.add_argument("--kind", choices=list(INVENTORY_KINDS), default="other")
    parser.add_argument("--amount", type=float)
    parser.add_argument("--unit", default="each")
    parser.add_argument("--notes", default="")
    parser.add_argument("--priority", choices=list(INVENTORY_PRIORITIES), default="normal")
    parser.add_argument("--match-recipe", action="append", default=None, help="Repeatable explicit recipe slug matcher.")
    parser.add_argument("--match-term", action="append", default=None, help="Repeatable free-text matcher against recipe title/slug/ingredients.")
    parser.add_argument("--match-core", action="append", default=None, help="Repeatable core protein lane like beef or chicken.")



def build_item_from_args(args: argparse.Namespace) -> dict[str, object]:
    if not args.label:
        raise SystemExit("--label is required")
    if args.amount is None:
        raise SystemExit("--amount is required")
    item_id = slugify(args.item_id or f"{args.location}-{args.label}")
    rules = {}
    if args.match_recipe is not None:
        rules["recipe_slugs"] = args.match_recipe
    if args.match_term is not None:
        rules["search_terms"] = args.match_term
    if args.match_core is not None:
        rules["core_proteins"] = args.match_core
    return normalize_inventory_item(
        {
            "id": item_id,
            "label": args.label,
            "location": args.location,
            "kind": args.kind,
            "quantity": quantity_dict(args.amount, args.unit),
            "match_rules": rules,
            "planning": {"priority": args.priority},
            "notes": args.notes,
        }
    )



def command_show(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    state = load_inventory_state(paths)
    items = state.get("items", [])
    if args.available_only:
        items = [item for item in items if float(item.get("quantity", {}).get("amount", 0) or 0) > 0]
    if args.json:
        print(json.dumps({**state, "items": items}, indent=2))
        return
    if not items:
        print("No inventory items saved yet.")
        return
    for item in items:
        print(render_item(item))



def command_add(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    state = load_inventory_state(paths)
    item = build_item_from_args(args)
    ensure_unique_item_id(state, item["id"])
    next_state = replace_inventory_item(state, item)
    save_inventory_state(paths, next_state)
    append_inventory_transaction(paths, build_transaction("add", item, notes=args.notes))
    _report(args, f"added inventory item: {item['id']}", item)



def command_set(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    state = load_inventory_state(paths)
    item = inventory_item_by_id(state, args.item)
    if not item:
        raise SystemExit(f"Unknown inventory item: {args.item}")

    updated = deepcopy(item)
    if args.label:
        updated["label"] = args.label
    if args.location:
        updated["location"] = args.location
    if args.kind:
        updated["kind"] = args.kind
    if args.amount is not None:
        updated["quantity"]["amount"] = round(float(args.amount), 3)
    if args.unit:
        updated["quantity"]["unit"] = args.unit
    if args.notes is not None:
        updated["notes"] = args.notes
    if args.priority:
        updated.setdefault("planning", {})["priority"] = args.priority
    if args.match_recipe is not None:
        updated.setdefault("match_rules", {})["recipe_slugs"] = args.match_recipe
    if args.match_term is not None:
        updated.setdefault("match_rules", {})["search_terms"] = args.match_term
    if args.match_core is not None:
        updated.setdefault("match_rules", {})["core_proteins"] = args.match_core

    updated = normalize_inventory_item(updated)
    next_state = replace_inventory_item(state, updated)
    save_inventory_state(paths, next_state)
    append_inventory_transaction(paths, build_transaction("set", updated, before=item, notes=args.notes or ""))
    _report(args, f"updated inventory item: {updated['id']}", updated)



def command_use(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    if not args.confirmed:
        raise SystemExit("Refusing to subtract inventory without --confirmed. Inventory changes must be explicit and user-confirmed.")

    state = load_inventory_state(paths)
    item = inventory_item_by_id(state, args.item)
    if not item:
        raise SystemExit(f"Unknown inventory item: {args.item}")

    updated = deepcopy(item)
    updated["quantity"] = subtract_quantity(item["quantity"], args.amount, args.unit or item["quantity"].get("unit", "each"))
    updated = normalize_inventory_item(updated)
    next_state = replace_inventory_item(state, updated)
    save_inventory_state(paths, next_state)
    append_inventory_transaction(
        paths,
        build_transaction(
            "confirmed-use",
            updated,
            before=item,
            notes=args.notes or "",
            metadata={
                "confirmed": True,
                "used_quantity": quantity_dict(args.amount, args.unit or item["quantity"].get("unit", "each")),
            },
        ),
    )
    _report(args, f"used inventory item: {updated['id']}", updated)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage portable Kitchen Compass inventory state.")
    parser.add_argument(
        "--data-root",
        help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--quiet", action="store_true", help="Suppress the verbose JSON dump; print a one-line confirmation instead.")
    parser.add_argument("--silent", action="store_true", help="Suppress all stdout output from mutation commands.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="Show saved inventory items.")
    show_parser.add_argument("--json", action="store_true")
    show_parser.add_argument("--available-only", action="store_true", help="Hide depleted items with zero quantity.")

    add_parser = subparsers.add_parser("add", help="Add a new inventory item.")
    add_args(add_parser)

    set_parser = subparsers.add_parser("set", help="Set the current saved state for an existing inventory item.")
    set_parser.add_argument("--item", required=True, help="Inventory item id.")
    set_parser.add_argument("--label")
    set_parser.add_argument("--location", choices=list(INVENTORY_LOCATIONS))
    set_parser.add_argument("--kind", choices=list(INVENTORY_KINDS))
    set_parser.add_argument("--amount", type=float)
    set_parser.add_argument("--unit")
    set_parser.add_argument("--notes")
    set_parser.add_argument("--priority", choices=list(INVENTORY_PRIORITIES))
    set_parser.add_argument("--match-recipe", action="append", default=None)
    set_parser.add_argument("--match-term", action="append", default=None)
    set_parser.add_argument("--match-core", action="append", default=None)

    use_parser = subparsers.add_parser("use", help="Subtract confirmed inventory usage from an existing item.")
    use_parser.add_argument("--item", required=True, help="Inventory item id.")
    use_parser.add_argument("--amount", required=True, type=float)
    use_parser.add_argument("--unit", help="Defaults to the item's saved unit.")
    use_parser.add_argument("--confirmed", action="store_true", help="Required guard rail for usage subtraction.")
    use_parser.add_argument("--notes", default="")

    return parser



def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))

    try:
        if args.command == "show":
            command_show(args, paths)
        elif args.command == "add":
            command_add(args, paths)
        elif args.command == "set":
            command_set(args, paths)
        elif args.command == "use":
            command_use(args, paths)
        else:
            raise SystemExit(f"Unknown command: {args.command}")
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
