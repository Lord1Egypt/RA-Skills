#!/usr/bin/env python3
"""Figma REST API CLI tool for reading design files, components, and exporting assets."""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from collections import Counter

TOKEN = os.environ.get("FIGMA_TOKEN", "")
BASE = "https://api.figma.com/v1"


def _get(path: str) -> dict:
    """Make authenticated GET request to Figma API."""
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def extract_file_key(url_or_key: str) -> str:
    """Extract file_key from a Figma URL or return as-is if already a key."""
    m = re.search(r"figma\.com/(?:design|file)/([a-zA-Z0-9]+)", url_or_key)
    return m.group(1) if m else url_or_key


def cmd_pages(args):
    """List pages in a file."""
    fk = extract_file_key(args.file_key)
    d = _get(f"files/{fk}?depth=1")
    print(f"File: {d.get('name')} (role: {d.get('role', '?')})")
    print(f"Last modified: {d.get('lastModified')}")
    pages = d.get("document", {}).get("children", [])
    print(f"\nPages ({len(pages)}):")
    for p in pages:
        print(f"  [{p['id']}] {p['name']}")


def cmd_tree(args):
    """Show frame tree of a node."""
    fk = extract_file_key(args.file_key)
    node_id = args.node
    depth = args.depth or 3
    d = _get(f"files/{fk}/nodes?ids={node_id}&depth={depth}")
    nodes = d.get("nodes", {})
    for nid, ndata in nodes.items():
        doc = ndata.get("document", {})
        _print_tree(doc, 0, args.max_children or 20)


def _print_tree(node: dict, indent: int, max_children: int):
    t = node.get("type", "")
    n = node.get("name", "")
    nc = len(node.get("children", []))
    extra = ""
    if t == "TEXT":
        chars = node.get("characters", "")
        if chars:
            extra = f' "{chars[:80]}"'
    elif t == "INSTANCE":
        comp = node.get("componentId", "")
        if comp:
            extra = f" (componentId: {comp})"
    suffix = f" [{nc} children]" if nc > 0 else ""
    print("  " * indent + f"[{t}] {n}{extra}{suffix}")
    children = node.get("children", [])
    for i, c in enumerate(children[:max_children]):
        _print_tree(c, indent + 1, max_children)
    if len(children) > max_children:
        print("  " * (indent + 1) + f"... +{len(children) - max_children} more")


def cmd_components(args):
    """List published components."""
    fk = extract_file_key(args.file_key)
    d = _get(f"files/{fk}/components")
    comps = d.get("meta", {}).get("components", [])
    print(f"Published components: {len(comps)}")
    if args.group:
        frames = Counter(c.get("containing_frame", {}).get("name", "?") for c in comps)
        print("\nBy containing frame:")
        for f, cnt in frames.most_common(args.limit or 30):
            print(f"  {f}: {cnt}")
    else:
        for c in comps[: args.limit or 50]:
            frame = c.get("containing_frame", {}).get("name", "?")
            print(f"  - {c.get('name', '?')} | frame: {frame} | id: {c.get('node_id', '?')}")
        if len(comps) > (args.limit or 50):
            print(f"  ... +{len(comps) - (args.limit or 50)} more (use --limit to show more)")


def cmd_component_sets(args):
    """List component sets."""
    fk = extract_file_key(args.file_key)
    d = _get(f"files/{fk}/component_sets")
    sets = d.get("meta", {}).get("component_sets", [])
    print(f"Component sets: {len(sets)}")
    for s in sets[: args.limit or 50]:
        print(f"  - {s.get('name', '?')} | id: {s.get('node_id', '?')}")


def cmd_styles(args):
    """List styles."""
    fk = extract_file_key(args.file_key)
    d = _get(f"files/{fk}/styles")
    styles = d.get("meta", {}).get("styles", [])
    print(f"Styles: {len(styles)}")
    types = Counter(s.get("style_type") for s in styles)
    if types:
        print("\nBy type:")
        for t, c in types.most_common():
            print(f"  {t}: {c}")
    for s in styles[: args.limit or 30]:
        print(f"  - [{s.get('style_type')}] {s.get('name')}")


def cmd_export(args):
    """Export nodes as images."""
    fk = extract_file_key(args.file_key)
    nodes = args.nodes
    fmt = args.format or "png"
    scale = args.scale or 2
    d = _get(f"images/{fk}?ids={nodes}&format={fmt}&scale={scale}")
    images = d.get("images", {})
    if d.get("err"):
        print(f"Error: {d['err']}", file=sys.stderr)
        return
    for nid, url in images.items():
        if url:
            out = args.output or f"/tmp/figma_{nid.replace(':', '_')}.{fmt}"
            urllib.request.urlretrieve(url, out)
            print(f"Saved: {out}")
        else:
            print(f"No image for node {nid}")


def cmd_node(args):
    """Get detailed node JSON."""
    fk = extract_file_key(args.file_key)
    depth = args.depth or 4
    d = _get(f"files/{fk}/nodes?ids={args.node}&depth={depth}")
    nodes = d.get("nodes", {})
    for nid, ndata in nodes.items():
        doc = ndata.get("document", {})
        print(json.dumps(doc, indent=2, ensure_ascii=False)[:args.max_chars or 10000])


def cmd_me(args):
    """Show current user info."""
    d = _get("me")
    print(json.dumps(d, indent=2))


def main():
    if not TOKEN:
        print("Error: FIGMA_TOKEN not set. Export it or add to ~/.openclaw/.env", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Figma REST API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("pages", help="List file pages")
    p.add_argument("file_key")
    p.set_defaults(func=cmd_pages)

    p = sub.add_parser("tree", help="Show frame tree")
    p.add_argument("file_key")
    p.add_argument("--node", required=True)
    p.add_argument("--depth", type=int, default=3)
    p.add_argument("--max-children", type=int, default=20)
    p.set_defaults(func=cmd_tree)

    p = sub.add_parser("components", help="List published components")
    p.add_argument("file_key")
    p.add_argument("--group", action="store_true", help="Group by containing frame")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_components)

    p = sub.add_parser("component-sets", help="List component sets")
    p.add_argument("file_key")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_component_sets)

    p = sub.add_parser("styles", help="List styles")
    p.add_argument("file_key")
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_styles)

    p = sub.add_parser("export", help="Export nodes as images")
    p.add_argument("file_key")
    p.add_argument("--nodes", required=True, help="Comma-separated node IDs")
    p.add_argument("--format", choices=["png", "svg", "jpg", "pdf"], default="png")
    p.add_argument("--scale", type=float, default=2)
    p.add_argument("--output", help="Output file path")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("node", help="Get node JSON")
    p.add_argument("file_key")
    p.add_argument("--node", required=True)
    p.add_argument("--depth", type=int, default=4)
    p.add_argument("--max-chars", type=int, default=10000)
    p.set_defaults(func=cmd_node)

    p = sub.add_parser("me", help="Show current user")
    p.set_defaults(func=cmd_me)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
