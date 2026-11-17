#!/usr/bin/env python3
"""Check or migrate optional Notion Travel Entries schema."""

from __future__ import annotations

import argparse

from notion_common import (
    OPTIONAL_NOTION_PROPERTIES,
    OPTIONAL_PROPERTY_CREATE_SCHEMA,
    check_notion_properties,
    notion_env,
    notion_request,
    resolve_db,
)


def property_type_errors(properties: dict, expected: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for name, expected_type in expected.items():
        actual = properties.get(name)
        if not actual:
            continue
        actual_type = actual.get("type")
        if actual_type != expected_type:
            errors.append(f"{name}: expected {expected_type}, got {actual_type}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "migrate"), help="Check schema or add missing optional columns.")
    parser.add_argument("--db", default=None, help="Path to travel-db. Loaded for consistent env resolution.")
    parser.add_argument("--apply", action="store_true", help="Apply migration. Without this flag, migrate is a dry-run.")
    args = parser.parse_args()

    resolve_db(args.db)
    token, data_source_id, version = notion_env()
    if not token or not data_source_id:
        print("Schema check requires NOTION_TOKEN and NOTION_TRAVEL_DATA_SOURCE_ID in local env.")
        return 1

    data_source = notion_request("GET", f"/data_sources/{data_source_id}", token, version)
    properties = data_source.get("properties", {})
    required_errors = check_notion_properties(properties)
    type_errors = property_type_errors(properties, OPTIONAL_NOTION_PROPERTIES)
    missing_optional = [name for name in OPTIONAL_NOTION_PROPERTIES if name not in properties]

    if required_errors:
        print("Required Notion properties need manual attention:")
        for error in required_errors:
            print(f"- {error}")
    if type_errors:
        print("Optional Notion properties with incompatible types:")
        for error in type_errors:
            print(f"- {error}")

    if not missing_optional:
        print("Optional Notion schema is complete.")
        return 0 if not required_errors and not type_errors else 1

    print("Missing optional Notion columns:")
    for name in missing_optional:
        print(f"- {name} ({OPTIONAL_NOTION_PROPERTIES[name]})")

    if args.action == "check":
        return 0 if not required_errors and not type_errors else 1

    if not args.apply:
        print("Dry-run only. Re-run with migrate --apply to add missing optional columns.")
        return 0 if not required_errors and not type_errors else 1

    payload = {"properties": {name: OPTIONAL_PROPERTY_CREATE_SCHEMA[name] for name in missing_optional}}
    notion_request("PATCH", f"/data_sources/{data_source_id}", token, version, payload)
    print(f"Added {len(missing_optional)} optional Notion column(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
