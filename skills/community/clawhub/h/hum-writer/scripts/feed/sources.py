#!/usr/bin/env python3
"""
sources.py — Manage feed sources (X profiles, YouTube, websites).

Usage:
    python3 sources.py list [--type x_profile|youtube|website]
    python3 sources.py add x <handle> [category]
    python3 sources.py add youtube <url> [name]
    python3 sources.py add website <name> <url>
    python3 sources.py remove <handle_or_name_or_url>
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config

SOURCE_TYPES = ("x_feed", "x_profile", "youtube", "website")


def load_sources(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        # Handle legacy format
        if "feed_sources" not in data:
            return {"feed_sources": []}
        # Ensure prefer_longform defaults to False for feed types
        for entry in data["feed_sources"]:
            if entry.get("type") == "x_feed":
                entry.setdefault("prefer_longform", False)
        return data
    return {"feed_sources": []}


def save_sources(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved -> {path}")


def get_by_type(sources: dict, source_type: str) -> list:
    return [s for s in sources["feed_sources"] if s["type"] == source_type]


def update_last_crawled(sources: dict, source_type: str, identifier: str, timestamp: str | None = None):
    """Update last_crawled for a specific source. identifier is handle or url."""
    ts = timestamp or datetime.utcnow().isoformat() + "Z"
    for s in sources["feed_sources"]:
        if s["type"] != source_type:
            continue
        if source_type == "x_profile" and s.get("handle", "").lower() == identifier.lower():
            s["last_crawled"] = ts
        elif source_type == "youtube" and s.get("url", "").lower() == identifier.lower():
            s["last_crawled"] = ts
        elif source_type == "x_feed":
            s["last_crawled"] = ts


def cmd_list(sources: dict, filter_type: str | None = None):
    types_to_show = [filter_type] if filter_type else list(SOURCE_TYPES)

    for st in types_to_show:
        items = get_by_type(sources, st)
        if not items:
            continue
        label = st.replace("_", " ").title()
        print(f"=== {label} ({len(items)}) ===")
        for s in items:
            crawled = f" [crawled: {s['last_crawled']}]" if s.get("last_crawled") else " [never crawled]"
            if st == "x_feed":
                pa = " [prefer_longform]" if s.get("prefer_longform") else ""
                print(f"  {s.get('description', 'X home feed')}{pa}{crawled}")
            elif st == "x_profile":
                cat = f" [{s['category']}]" if s.get("category") else ""
                desc = f" -- {s['description']}" if s.get("description") else ""
                print(f"  @{s['handle']}{cat}{desc}{crawled}")
            elif st == "youtube":
                print(f"  {s.get('name', '?')} -- {s['url']}{crawled}")
            elif st == "website":
                print(f"  {s['name']} -- {s['url']}")
        print()


def cmd_add(sources: dict, args) -> bool:
    if args.source_type == "x":
        handle = args.value.lstrip("@")
        if not re.match(r'^[A-Za-z0-9_]{1,15}$', handle):
            print(f"Error: invalid handle/URL: '{args.value}'", file=sys.stderr)
            return False
        existing = get_by_type(sources, "x_profile")
        if any(s["handle"].lower() == handle.lower() for s in existing):
            print(f"@{handle} already exists.")
            return False
        entry = {
            "type": "x_profile",
            "handle": handle,
            "category": " ".join(args.extra) if args.extra else "",
            "description": "",
            "last_crawled": None,
        }
        sources["feed_sources"].append(entry)
        print(f"Added x_profile: @{handle}")
        return True

    elif args.source_type == "youtube":
        url = args.value
        is_yt_url = "youtube.com" in url or "youtu.be" in url
        is_handle = url.startswith("@")
        if not (is_yt_url or is_handle):
            print(f"Error: invalid handle/URL: '{url}'", file=sys.stderr)
            return False
        existing = get_by_type(sources, "youtube")
        if any(s["url"].lower() == url.lower() for s in existing):
            print(f"{url} already exists.")
            return False
        name = " ".join(args.extra) if args.extra else url.split("@")[-1] if "@" in url else url
        entry = {
            "type": "youtube",
            "name": name,
            "url": url,
            "description": "",
            "last_crawled": None,
        }
        sources["feed_sources"].append(entry)
        print(f"Added youtube: {name}")
        return True

    elif args.source_type == "website":
        name = args.value
        if not args.extra:
            print("Usage: add website <name> <url>")
            return False
        url = args.extra[0]
        existing = get_by_type(sources, "website")
        if any(s["name"].lower() == name.lower() for s in existing):
            print(f"{name} already exists.")
            return False
        entry = {
            "type": "website",
            "name": name,
            "url": url,
            "last_crawled": None,
        }
        sources["feed_sources"].append(entry)
        print(f"Added website: {name}")
        return True

    else:
        print(f"Unknown source type: {args.source_type}")
        return False


def cmd_remove(sources: dict, target: str) -> bool:
    target_lower = target.lower().lstrip("@").rstrip("/")

    for i, s in enumerate(sources["feed_sources"]):
        match = False
        if s["type"] == "x_profile" and s.get("handle", "").lower() == target_lower:
            match = True
        elif s["type"] == "youtube" and (
            s.get("name", "").lower() == target_lower or s.get("url", "").lower() == target_lower
        ):
            match = True
        elif s["type"] == "website" and s.get("name", "").lower() == target_lower:
            match = True

        if match:
            removed = sources["feed_sources"].pop(i)
            label = removed.get("handle") or removed.get("name") or removed.get("url")
            print(f"Removed {removed['type']}: {label}")
            return True

    print(f"Not found: {target}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Manage hum feed sources")
    sub = parser.add_subparsers(dest="command")

    list_p = sub.add_parser("list", help="List all sources")
    list_p.add_argument("--type", choices=SOURCE_TYPES, default=None, help="Filter by type")

    add_p = sub.add_parser("add", help="Add a source")
    add_p.add_argument("source_type", choices=["x", "youtube", "website"])
    add_p.add_argument("value", help="Handle, URL, or name")
    add_p.add_argument("extra", nargs="*", help="Category (x), name (youtube), or URL (website)")

    rm_p = sub.add_parser("remove", help="Remove a source")
    rm_p.add_argument("target", help="Handle, name, or URL to remove")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cfg = load_config()
    sources_file = cfg["sources_file"]
    sources = load_sources(sources_file)

    if args.command == "list":
        cmd_list(sources, args.type)
    elif args.command == "add":
        if cmd_add(sources, args):
            save_sources(sources_file, sources)
    elif args.command == "remove":
        if cmd_remove(sources, args.target):
            save_sources(sources_file, sources)


if __name__ == "__main__":
    main()
