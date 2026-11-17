#!/usr/bin/env python3
"""Look up a state or DC property-tax appeal routing profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "references" / "us-jurisdictions.json"


def load_registry() -> dict[str, Any]:
    with REGISTRY.open(encoding="utf-8") as stream:
        return json.load(stream)


def resolve_state(value: str, profiles: dict[str, Any]) -> str | None:
    normalized = " ".join(value.strip().lower().replace(".", "").split())
    if normalized.upper() in profiles:
        return normalized.upper()
    aliases = {
        "district of columbia": "DC",
        "washington dc": "DC",
        "washington d c": "DC",
    }
    if normalized in aliases:
        return aliases[normalized]
    for code, profile in profiles.items():
        if normalized == profile["name"].lower():
            return code
    return None


def human_output(code: str, profile: dict[str, Any], policy: dict[str, Any]) -> str:
    sequence = " -> ".join(profile["common_sequence"])
    terms = ", ".join(profile["common_form_terms"])
    return "\n".join(
        [
            f"Jurisdiction: {profile['name']} ({code})",
            f"Typical administration: {profile['administration']}",
            f"Route family: {profile['route_family']}",
            f"Typical sequence: {sequence}",
            f"Common form/search terms: {terms}",
            f"Official starting point: {profile['official_starting_url']}",
            f"Official-source query: {profile['official_search_query']}",
            "",
            f"Required verification: {policy['required_verification']}",
            f"Deadline policy: {policy['deadline_policy']}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", help="Two-letter code or full state name, including DC.")
    parser.add_argument("--json", action="store_true", help="Print the selected profile as JSON.")
    parser.add_argument("--list", action="store_true", help="List all supported jurisdictions.")
    args = parser.parse_args()

    registry = load_registry()
    profiles = registry["jurisdictions"]
    if args.list:
        for code, profile in profiles.items():
            print(f"{code}\t{profile['name']}\t{profile['route_family']}")
        return 0
    if not args.state:
        parser.error("--state is required unless --list is used")

    code = resolve_state(args.state, profiles)
    if not code:
        print(f"Unknown US state or district: {args.state}", file=sys.stderr)
        return 2
    profile = profiles[code]
    if args.json:
        print(json.dumps({"code": code, **profile}, indent=2, sort_keys=True))
    else:
        print(human_output(code, profile, registry["policy"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
