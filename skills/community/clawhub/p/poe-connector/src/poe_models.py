#!/usr/bin/env python3
"""Poe Connector — List, search, and inspect available Poe models."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from poe_utils import get_client, handle_api_error
import openai


def fetch_models() -> list[dict]:
    """Fetch all available models from the Poe API."""
    client = get_client()
    try:
        response = client.models.list()
    except openai.APIError as e:
        handle_api_error(e)
        sys.exit(1)

    models = []
    for m in response.data:
        entry = {"id": m.id, "created": m.created, "owned_by": m.owned_by}
        if hasattr(m, "object"):
            entry["object"] = m.object
        models.append(entry)
    return models


def list_models(as_json: bool = False) -> None:
    """Print all available models."""
    models = fetch_models()
    if as_json:
        print(json.dumps(models, indent=2))
        return

    print(f"Available Poe models ({len(models)} total):\n")
    for m in sorted(models, key=lambda x: x["id"].lower()):
        owner = m.get("owned_by", "")
        owner_str = f"  (by {owner})" if owner else ""
        print(f"  {m['id']}{owner_str}")
    print(f"\nTotal: {len(models)} models")


def search_models(query: str, as_json: bool = False) -> None:
    """Search models by keyword (case-insensitive)."""
    models = fetch_models()
    query_lower = query.lower()
    matches = [
        m for m in models
        if query_lower in m["id"].lower() or query_lower in (m.get("owned_by") or "").lower()
    ]

    if as_json:
        print(json.dumps(matches, indent=2))
        return

    if not matches:
        print(f'No models matching "{query}".')
        return

    print(f'Models matching "{query}" ({len(matches)} found):\n')
    for m in sorted(matches, key=lambda x: x["id"].lower()):
        owner = m.get("owned_by", "")
        owner_str = f"  (by {owner})" if owner else ""
        print(f"  {m['id']}{owner_str}")


def model_info(model_id: str) -> None:
    """Show detailed info for a specific model."""
    models = fetch_models()
    match = next((m for m in models if m["id"].lower() == model_id.lower()), None)

    if not match:
        close = [m for m in models if model_id.lower() in m["id"].lower()]
        print(f'Model "{model_id}" not found.', file=sys.stderr)
        if close:
            print(f"\nDid you mean one of these?", file=sys.stderr)
            for m in close[:10]:
                print(f"  {m['id']}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(match, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="List, search, and inspect Poe models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --list\n"
            "  %(prog)s --list --json\n"
            '  %(prog)s --search "claude"\n'
            '  %(prog)s --info "Claude-Sonnet-4"\n'
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", "-l", action="store_true", help="List all available models")
    group.add_argument("--search", "-s", metavar="QUERY", help="Search models by keyword")
    group.add_argument("--info", "-i", metavar="MODEL", help="Show detailed info for a model")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        list_models(as_json=args.json)
    elif args.search:
        search_models(args.search, as_json=args.json)
    elif args.info:
        model_info(args.info)


if __name__ == "__main__":
    main()
