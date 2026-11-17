#!/usr/bin/env python3
"""Plan or apply Notion push/pull/sync for the compact travel mirror."""

from __future__ import annotations

import argparse
from typing import Any

from build_records_from_places import merge_markdown_records
from notion_common import (
    append_conflict,
    append_sync_log,
    content_hash,
    content_hash_with_detail,
    load_ledger,
    load_records,
    notion_dir,
    notion_env,
    notion_properties_for_record,
    notion_record_from_page,
    notion_request,
    notion_sync_hash_from_page,
    resolve_db,
    save_ledger,
    save_records,
    validate_records,
)
from travel_model import filter_records, normalize_city_name, save_generated_indexes


def query_notion_pages(token: str, data_source_id: str, version: str, limit: int | None = None) -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    start_cursor: str | None = None
    while True:
        body: dict[str, Any] = {"page_size": min(limit or 100, 100)}
        if start_cursor:
            body["start_cursor"] = start_cursor
        result = notion_request("POST", f"/data_sources/{data_source_id}/query", token, version, body)
        pages.extend(result.get("results", []))
        if limit and len(pages) >= limit:
            return pages[:limit]
        if not result.get("has_more"):
            return pages
        start_cursor = result.get("next_cursor")


def available_notion_properties(token: str, data_source_id: str, version: str) -> set[str]:
    data_source = notion_request("GET", f"/data_sources/{data_source_id}", token, version)
    return set((data_source.get("properties") or {}).keys())


def page_records(pages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    records: list[dict[str, Any]] = []
    sync_hash_by_id: dict[str, str] = {}
    for page in pages:
        record = notion_record_from_page(page)
        records.append(record)
        sync_hash_by_id[record["id"]] = notion_sync_hash_from_page(page)
    return records, sync_hash_by_id


def plan_push(records: list[dict[str, Any]], ledger: dict[str, dict[str, Any]], sync_dir) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for record in records:
        entry = ledger.get(record["id"], {})
        local_hash = content_hash_with_detail(sync_dir, record)
        page_id = record.get("notion_page_id") or entry.get("notion_page_id")
        if not page_id:
            actions.append({"action": "create_page", "id": record["id"], "record": record, "local_hash": local_hash})
        elif local_hash != entry.get("local_hash"):
            actions.append({"action": "update_page", "id": record["id"], "page_id": page_id, "record": record, "local_hash": local_hash})
    return actions


def apply_push(actions: list[dict[str, Any]], ledger: dict[str, dict[str, Any]], token: str, data_source_id: str, version: str) -> None:
    from notion_common import now_iso

    timestamp = now_iso()
    available_properties = available_notion_properties(token, data_source_id, version)
    for action in actions:
        record = action["record"]
        properties = notion_properties_for_record(record, available_properties, sync_hash=action["local_hash"])
        if action["action"] == "create_page":
            page = notion_request("POST", "/pages", token, version, {"parent": {"data_source_id": data_source_id}, "properties": properties})
            record["notion_page_id"] = page.get("id")
            page_id = page.get("id")
        else:
            page_id = action["page_id"]
            notion_request("PATCH", f"/pages/{page_id}", token, version, {"properties": properties})
        ledger[record["id"]] = {
            "id": record["id"],
            "notion_page_id": page_id,
            "local_hash": action["local_hash"],
            "notion_hash": action["local_hash"],
            "last_synced_at": timestamp,
            "last_direction": "push",
        }


def plan_pull(notion_records: list[dict[str, Any]], local_records: list[dict[str, Any]], ledger: dict[str, dict[str, Any]], sync_dir) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    local_by_id = {record["id"]: record for record in local_records}
    actions: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for notion_record in notion_records:
        record_id = notion_record["id"]
        notion_hash = content_hash(notion_record)
        local = local_by_id.get(record_id)
        entry = ledger.get(record_id, {})
        if not local:
            actions.append({"action": "create_local", "id": record_id, "record": notion_record, "notion_hash": notion_hash})
            continue
        local_hash = content_hash_with_detail(sync_dir, local)
        local_changed = bool(entry and local_hash != entry.get("local_hash"))
        notion_changed = bool(entry and notion_hash != entry.get("notion_hash"))
        if local_changed and notion_changed:
            conflicts.append({
                "id": record_id,
                "reason": "local and Notion changed since last sync",
                "local_changed": True,
                "notion_changed": True,
                "notion_page_id": notion_record.get("notion_page_id"),
            })
        elif notion_changed or not entry:
            actions.append({"action": "update_local", "id": record_id, "record": notion_record, "notion_hash": notion_hash})
    return actions, conflicts


def apply_pull(actions: list[dict[str, Any]], records: list[dict[str, Any]], ledger: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    from notion_common import now_iso

    timestamp = now_iso()
    by_id = {record["id"]: record for record in records}
    for action in actions:
        record = action["record"]
        by_id[record["id"]] = record
        ledger[record["id"]] = {
            "id": record["id"],
            "notion_page_id": record.get("notion_page_id"),
            "local_hash": action["notion_hash"],
            "notion_hash": action["notion_hash"],
            "last_synced_at": timestamp,
            "last_direction": "pull",
        }
    return list(by_id.values())


def apply_strict_push_guard(actions: list[dict[str, Any]], remote_by_id: dict[str, dict[str, Any]], remote_sync_hash_by_id: dict[str, str], ledger: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    allowed: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for action in actions:
        if action["action"] != "update_page":
            allowed.append(action)
            continue

        record_id = action["id"]
        entry = ledger.get(record_id, {})
        remote = remote_by_id.get(record_id)
        if not entry or not entry.get("notion_hash"):
            conflicts.append({
                "id": record_id,
                "reason": "strict push cannot verify previous Notion baseline",
                "local_changed": True,
                "notion_changed": None,
                "notion_page_id": action.get("page_id"),
            })
            continue
        if not remote:
            conflicts.append({
                "id": record_id,
                "reason": "strict push could not find the Notion page in the current query",
                "local_changed": True,
                "notion_changed": None,
                "notion_page_id": action.get("page_id"),
            })
            continue

        remote_hash = content_hash(remote)
        remote_sync_hash = remote_sync_hash_by_id.get(record_id)
        remote_changed = remote_hash != entry.get("notion_hash")
        sync_hash_mismatch = bool(remote_sync_hash and remote_sync_hash != entry.get("notion_hash"))
        if remote_changed or sync_hash_mismatch:
            conflicts.append({
                "id": record_id,
                "reason": "Notion changed since last sync; strict push blocked local overwrite",
                "local_changed": True,
                "notion_changed": True,
                "notion_page_id": remote.get("notion_page_id"),
            })
            continue
        allowed.append(action)
    return allowed, conflicts


def print_actions(title: str, actions: list[dict[str, Any]]) -> None:
    print(title)
    if not actions:
        print("- no changes")
        return
    for action in actions:
        detail = action.get("page_id") or action["record"].get("name")
        print(f"- {action['action']}: {action['id']} ({detail})")


def print_conflicts(conflicts: list[dict[str, Any]]) -> None:
    for conflict in conflicts:
        print(f"- conflict: {conflict['id']} ({conflict['reason']})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("direction", choices=("push", "pull", "sync"), nargs="?", default="sync")
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--apply", action="store_true", help="Apply changes. Without this flag, only print a dry-run plan.")
    parser.add_argument("--limit", type=int, default=None, help="Limit Notion pages queried during pull/sync/strict.")
    parser.add_argument("--no-auto-records", action="store_true", help="Do not refresh _records.jsonl from Markdown entries before push/sync.")
    parser.add_argument("--strict", action="store_true", help="Block push updates when the Notion page changed since the last ledger hash.")
    parser.add_argument("--filter-city", default=None, help="Only plan/apply records for one city.")
    parser.add_argument("--filter-tag", action="append", default=[], help="Only plan/apply records matching a tag. Repeatable.")
    args = parser.parse_args()

    db = resolve_db(args.db)
    sync_dir = notion_dir(db)
    filter_city = normalize_city_name(args.filter_city)
    filter_tags = [tag for tag in args.filter_tag if tag]
    log_entry: dict[str, Any] = {
        "direction": args.direction,
        "apply": args.apply,
        "strict": args.strict,
        "filter_city": filter_city,
        "filter_tags": filter_tags,
        "record_count": 0,
        "pull_actions": 0,
        "push_actions": 0,
        "conflicts": 0,
        "errors": [],
    }

    records = load_records(sync_dir)
    if args.direction in {"push", "sync"} and not args.no_auto_records:
        records, markdown_stats = merge_markdown_records(db, records)
        log_entry["markdown_mirror"] = markdown_stats
        if any(markdown_stats[key] for key in ("added", "updated")):
            print(
                "Markdown mirror: "
                f"{markdown_stats['added']} add, {markdown_stats['updated']} update, "
                f"{markdown_stats['unchanged']} unchanged."
            )

    errors = validate_records(records, sync_dir)
    if errors:
        print("Cannot sync until local records are valid:")
        for error in errors:
            print(f"- {error}")
        log_entry["errors"] = errors
        append_sync_log(sync_dir, log_entry)
        return 1

    ledger = load_ledger(sync_dir)
    token, data_source_id, version = notion_env()
    target_records = filter_records(records, filter_city, filter_tags)
    log_entry["record_count"] = len(target_records)

    notion_records: list[dict[str, Any]] = []
    sync_hash_by_id: dict[str, str] = {}
    needs_notion_query = args.direction in {"pull", "sync"} or args.strict
    if needs_notion_query:
        if not token or not data_source_id:
            message = "Notion query requires NOTION_TOKEN and NOTION_TRAVEL_DATA_SOURCE_ID."
            print(message)
            log_entry["errors"] = [message]
            append_sync_log(sync_dir, log_entry)
            if args.direction == "pull" or args.strict:
                return 1
        else:
            pages = query_notion_pages(token, data_source_id, version, args.limit)
            notion_records, sync_hash_by_id = page_records(pages)

    conflicts: list[dict[str, Any]] = []
    pull_actions: list[dict[str, Any]] = []
    push_actions: list[dict[str, Any]] = []

    if args.direction in {"pull", "sync"} and notion_records:
        target_notion_records = filter_records(notion_records, filter_city, filter_tags)
        pull_actions, pull_conflicts = plan_pull(target_notion_records, records, ledger, sync_dir)
        conflicts.extend(pull_conflicts)
        print_actions("Pull plan:", pull_actions)
        print_conflicts(pull_conflicts)
        if args.apply:
            records = apply_pull(pull_actions, records, ledger)
            target_records = filter_records(records, filter_city, filter_tags)
            for conflict in pull_conflicts:
                append_conflict(sync_dir, conflict)

    if args.direction in {"push", "sync"}:
        push_actions = plan_push(target_records, ledger, sync_dir)
        if args.strict:
            remote_by_id = {record["id"]: record for record in notion_records}
            push_actions, strict_conflicts = apply_strict_push_guard(push_actions, remote_by_id, sync_hash_by_id, ledger)
            conflicts.extend(strict_conflicts)
            print_conflicts(strict_conflicts)
            if args.apply:
                for conflict in strict_conflicts:
                    append_conflict(sync_dir, conflict)
        print_actions("Push plan:", push_actions)
        if args.apply:
            if not token or not data_source_id:
                message = "Push requires NOTION_TOKEN and NOTION_TRAVEL_DATA_SOURCE_ID."
                print(message)
                log_entry["errors"] = [message]
                append_sync_log(sync_dir, log_entry)
                return 1
            apply_push(push_actions, ledger, token, data_source_id, version)

    log_entry["pull_actions"] = len(pull_actions)
    log_entry["push_actions"] = len(push_actions)
    log_entry["conflicts"] = len(conflicts)

    if args.apply:
        save_records(sync_dir, records)
        save_ledger(sync_dir, ledger)
        save_generated_indexes(db)
        print("Applied changes.")
    else:
        print("Dry-run only. Re-run with --apply to write changes.")

    append_sync_log(sync_dir, log_entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
