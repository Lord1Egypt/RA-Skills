#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy

from contract import WEEKLY_DEAL_SOURCE_TYPES, WEEKLY_DEAL_STORE_STATUSES
from deals import (
    deal_store_by_id,
    ensure_stores_config_shape,
    load_raw_stores_config,
    normalize_deal_store,
    render_store,
    replace_deal_store,
    save_stores_config,
    load_stores_config,
    slugify,
    validate_stores_config,
)
from paths import KitchenCompassPaths, resolve_data_root


SOURCE_HELP = "One of: " + ", ".join(WEEKLY_DEAL_SOURCE_TYPES)
STATUS_HELP = "One of: " + ", ".join(WEEKLY_DEAL_STORE_STATUSES)



def _report(args: argparse.Namespace, summary: str, payload: dict) -> None:
    if args.silent:
        return
    if args.quiet:
        print(summary)
        return
    print(json.dumps(payload, indent=2))


def build_store_payload(args: argparse.Namespace, existing: dict | None = None) -> dict:
    base = deepcopy(existing or {})
    label = args.label if args.label is not None else base.get("label", "")
    retailer = args.retailer if args.retailer is not None else base.get("retailer", "")
    store_id = args.store_id or base.get("id") or slugify(label)
    source = deepcopy(base.get("source") or {})
    if args.source_type is not None:
        source["type"] = args.source_type
    if args.source_url is not None:
        source["url"] = args.source_url
    if args.source_label is not None:
        source["label"] = args.source_label
    if args.source_notes is not None:
        source["notes"] = args.source_notes
    if args.last_verified_at is not None:
        source["last_verified_at"] = args.last_verified_at
    retrieval_recipe = deepcopy(base.get("retrieval_recipe") or {})
    if args.retrieval_start_url is not None:
        retrieval_recipe["starting_url"] = args.retrieval_start_url
    if args.retrieval_fallback_url is not None:
        retrieval_recipe["fallback_url"] = args.retrieval_fallback_url
    if args.store_selector_hint is not None:
        retrieval_recipe["store_selector_hint"] = args.store_selector_hint
    if args.retrieval_step is not None:
        retrieval_recipe["steps"] = args.retrieval_step
    if args.known_friction is not None:
        retrieval_recipe["known_friction"] = args.known_friction
    if args.last_success_url is not None:
        retrieval_recipe["last_successful_url"] = args.last_success_url
    if args.last_success_at is not None:
        retrieval_recipe["last_successful_at"] = args.last_success_at
    if args.retrieval_notes is not None:
        retrieval_recipe["notes"] = args.retrieval_notes
    payload = {
        **base,
        "id": store_id,
        "label": label,
        "retailer": retailer,
        "store_code": args.store_code if args.store_code is not None else base.get("store_code", ""),
        "location_notes": args.location_notes if args.location_notes is not None else base.get("location_notes", ""),
        "status": args.status if args.status is not None else base.get("status", "active"),
        "manual_setup_required": base.get("manual_setup_required", True),
        "source": source,
        "retrieval_recipe": retrieval_recipe,
        "notes": args.notes if args.notes is not None else base.get("notes", ""),
    }
    if args.manual_setup_required is not None:
        payload["manual_setup_required"] = args.manual_setup_required
    return normalize_deal_store(payload)



def set_default_store(config: dict, store_id: str, enabled: bool) -> dict:
    normalized = ensure_stores_config_shape(config)
    weekly = deepcopy(normalized["weekly_deal_brief"])
    defaults = [value for value in weekly.get("default_store_ids", []) if value != store_id]
    if enabled:
        defaults.append(store_id)
        normalized["preferred_stores"] = list(dict.fromkeys(normalized.get("preferred_stores", []) + [store_id]))
    weekly["default_store_ids"] = defaults
    normalized["weekly_deal_brief"] = weekly
    return ensure_stores_config_shape(normalized)



def command_show(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    config = load_stores_config(paths)
    if args.json:
        print(json.dumps(config, indent=2))
        return
    weekly = config.get("weekly_deal_brief", {})
    schedule = weekly.get("scan_schedule") or {}
    print(f"Weekly deal brief enabled: {str(weekly.get('enabled', False)).lower()}")
    print(f"Default deal stores: {', '.join(weekly.get('default_store_ids', [])) or '-'}")
    if any(schedule.values()):
        print(f"Scan schedule: {schedule.get('day_of_week') or '-'} @ {schedule.get('time_local') or '-'} ({schedule.get('timezone') or '-'})")
    stores = weekly.get("stores", [])
    if not stores:
        print("No weekly deal stores saved yet.")
        return
    for store in stores:
        print(render_store(store))



def command_validate(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    config = load_raw_stores_config(paths)
    errors = validate_stores_config(config)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
    if args.json:
        print(json.dumps(config, indent=2))
        return
    print("stores.json is valid for optional weekly deal brief use.")



def command_enable(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    config = load_stores_config(paths)
    config["weekly_deal_brief"]["enabled"] = args.enabled
    errors = validate_stores_config(config)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
    save_stores_config(paths, config)
    _report(args, f"weekly deal brief enabled={args.enabled}", config["weekly_deal_brief"])



def command_set_scan_schedule(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    config = load_stores_config(paths)
    weekly = deepcopy(config.get("weekly_deal_brief") or {})
    if args.clear:
        weekly["scan_schedule"] = {"day_of_week": "", "time_local": "", "timezone": ""}
    else:
        if not (args.day_of_week and args.time_local and args.timezone):
            raise SystemExit("set-scan-schedule requires --day-of-week, --time-local, and --timezone unless --clear is used")
        weekly["scan_schedule"] = {
            "day_of_week": args.day_of_week,
            "time_local": args.time_local,
            "timezone": args.timezone,
        }
    config["weekly_deal_brief"] = weekly
    errors = validate_stores_config(config)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
    save_stores_config(paths, config)
    _report(args, "scan schedule updated", config["weekly_deal_brief"].get("scan_schedule", {}))



def command_add_store(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    if not args.label:
        raise SystemExit("--label is required")
    if not args.retailer:
        raise SystemExit("--retailer is required")
    config = load_stores_config(paths)
    store = build_store_payload(args)
    if deal_store_by_id(config, store["id"]):
        raise SystemExit(f"Deal store already exists: {store['id']}")
    updated = replace_deal_store(config, store)
    if args.default:
        updated = set_default_store(updated, store["id"], True)
        updated["weekly_deal_brief"]["enabled"] = True
    errors = validate_stores_config(updated)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
    save_stores_config(paths, updated)
    _report(args, f"added deal store: {store['id']}", store)



def command_set_store(args: argparse.Namespace, paths: KitchenCompassPaths) -> None:
    config = load_stores_config(paths)
    existing = deal_store_by_id(config, args.store)
    if not existing:
        raise SystemExit(f"Unknown deal store: {args.store}")
    updated_store = build_store_payload(args, existing=existing)
    if updated_store["id"] != existing["id"] and deal_store_by_id(config, updated_store["id"]):
        raise SystemExit(f"Deal store already exists: {updated_store['id']}")

    updated = deepcopy(config)
    weekly = deepcopy(updated.get("weekly_deal_brief") or {})
    weekly["stores"] = [
        store for store in weekly.get("stores", [])
        if store.get("id") != existing["id"]
    ]
    weekly["default_store_ids"] = [
        updated_store["id"] if store_id == existing["id"] else store_id
        for store_id in weekly.get("default_store_ids", [])
    ]
    updated["preferred_stores"] = [
        updated_store["id"] if store_id == existing["id"] else store_id
        for store_id in updated.get("preferred_stores", [])
    ]
    updated["weekly_deal_brief"] = weekly
    updated = replace_deal_store(updated, updated_store)
    if args.default is not None:
        updated = set_default_store(updated, updated_store["id"], args.default)
    errors = validate_stores_config(updated)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {e}" for e in errors))
    save_stores_config(paths, updated)
    _report(args, f"updated deal store: {updated_store['id']}", updated_store)



def add_store_args(parser: argparse.ArgumentParser, *, include_default_flag: bool = True) -> None:
    parser.add_argument("--store-id", help="Stable store id. Defaults to a slug of --label.")
    parser.add_argument("--label", required=False)
    parser.add_argument("--retailer", required=False, help="Retailer slug or name, for example giant or shoprite.")
    parser.add_argument("--store-code")
    parser.add_argument("--location-notes")
    parser.add_argument("--status", choices=list(WEEKLY_DEAL_STORE_STATUSES), help=STATUS_HELP)
    parser.add_argument("--manual-setup-required", dest="manual_setup_required", action="store_true")
    parser.add_argument("--no-manual-setup-required", dest="manual_setup_required", action="store_false")
    parser.add_argument("--source-type", choices=list(WEEKLY_DEAL_SOURCE_TYPES), help=SOURCE_HELP)
    parser.add_argument("--source-url")
    parser.add_argument("--source-label")
    parser.add_argument("--source-notes")
    parser.add_argument("--last-verified-at")
    parser.add_argument("--retrieval-start-url", help="Best known URL to start from next week for this store.")
    parser.add_argument("--retrieval-fallback-url", help="Fallback source URL if the primary flow breaks.")
    parser.add_argument("--store-selector-hint", help="Store-specific hint such as a store code, rsid, or selection note.")
    parser.add_argument("--retrieval-step", action="append", default=None, help="Repeatable step describing how to reach the right ad next week.")
    parser.add_argument("--known-friction", action="append", default=None, help="Repeatable note for issues like JS, cookies, Cloudflare, coupon gating, or mirror fallback.")
    parser.add_argument("--last-success-url", help="Last successful deep link or resolved flyer URL.")
    parser.add_argument("--last-success-at", help="Timestamp or note for the last successful retrieval.")
    parser.add_argument("--retrieval-notes", help="Freeform notes about how this store's retrieval flow works.")
    parser.add_argument("--notes")
    if include_default_flag:
        parser.add_argument("--default", action="store_true", help="Also save this store as a default weekly deal brief store and enable the feature.")
    parser.set_defaults(manual_setup_required=None)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage optional manual weekly deal brief store/source setup for Kitchen Compass.")
    parser.add_argument(
        "--data-root",
        help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--quiet", action="store_true", help="Suppress the verbose JSON dump; print a one-line confirmation instead.")
    parser.add_argument("--silent", action="store_true", help="Suppress all stdout output from mutation commands.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="Show saved weekly deal brief store/source setup.")
    show_parser.add_argument("--json", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="Validate household/stores.json for optional weekly deal brief use.")
    validate_parser.add_argument("--json", action="store_true")

    enable_parser = subparsers.add_parser("enable", help="Enable or disable the optional weekly deal brief feature flag.")
    enable_parser.add_argument("--enabled", action="store_true", help="Turn weekly deal brief support on.")
    enable_parser.add_argument("--disabled", dest="enabled", action="store_false", help="Turn weekly deal brief support off.")
    enable_parser.set_defaults(enabled=True)

    schedule_parser = subparsers.add_parser("set-scan-schedule", help="Set or clear the preferred weekly deal scan schedule.")
    schedule_parser.add_argument("--day-of-week", choices=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    schedule_parser.add_argument("--time-local", help="HH:MM 24-hour local time, for example 12:00")
    schedule_parser.add_argument("--timezone", help="IANA timezone, for example America/New_York")
    schedule_parser.add_argument("--clear", action="store_true", help="Clear the saved weekly scan schedule.")

    add_parser = subparsers.add_parser("add-store", help="Add a manual weekly deal brief store/source definition.")
    add_store_args(add_parser)

    set_parser = subparsers.add_parser("set-store", help="Update an existing weekly deal brief store/source definition.")
    set_parser.add_argument("--store", required=True, help="Existing store id.")
    add_store_args(set_parser, include_default_flag=False)
    default_group = set_parser.add_mutually_exclusive_group()
    default_group.add_argument("--default", dest="default", action="store_true", help="Add this store to weekly_deal_brief.default_store_ids.")
    default_group.add_argument("--not-default", dest="default", action="store_false", help="Remove this store from weekly_deal_brief.default_store_ids.")
    set_parser.set_defaults(default=None)

    return parser



def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))

    if args.command == "show":
        command_show(args, paths)
    elif args.command == "validate":
        command_validate(args, paths)
    elif args.command == "enable":
        command_enable(args, paths)
    elif args.command == "set-scan-schedule":
        command_set_scan_schedule(args, paths)
    elif args.command == "add-store":
        command_add_store(args, paths)
    elif args.command == "set-store":
        command_set_store(args, paths)
    else:
        raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
