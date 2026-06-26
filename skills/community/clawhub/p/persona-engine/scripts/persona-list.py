#!/usr/bin/env python3
"""
List all personas across workspaces.
Scans ~/.openclaw/workspace-* directories for persona configurations.

Usage:
    python3 persona-list.py
    python3 persona-list.py --json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def scan_workspaces(base_dir=None):
    """Scan all workspace directories for persona information."""
    if base_dir is None:
        base_dir = Path.home() / ".openclaw"

    base = Path(base_dir)
    if not base.exists():
        return []

    personas = []

    # Scan workspace-* directories
    for ws_dir in sorted(base.glob("workspace*")):
        if not ws_dir.is_dir():
            continue

        persona = _scan_single_workspace(ws_dir, base)
        if persona:
            personas.append(persona)

    return personas


def _scan_single_workspace(ws_dir, base):
    """Extract persona info from a single workspace directory."""
    info = {
        "workspace": str(ws_dir),
        "workspaceName": ws_dir.name,
        "name": "",
        "emoji": "",
        "archetype": "",
        "lastModified": "",
    }

    # Try to read from openclaw.json in parent or alongside
    config_candidates = [
        base / "openclaw.json",
        ws_dir / "openclaw.json",
        ws_dir.parent / "openclaw.json",
    ]

    for config_path in config_candidates:
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                persona = config.get("persona", {})
                if persona.get("name"):
                    info["name"] = persona.get("name", "")
                    info["emoji"] = persona.get("emoji", "")
                    info["archetype"] = persona.get("personality", {}).get("archetype", "")
                    break
            except (json.JSONDecodeError, OSError):
                continue

    # Fallback: try reading from IDENTITY.md or SOUL.md
    if not info["name"]:
        identity_path = ws_dir / "IDENTITY.md"
        if identity_path.exists():
            import re
            content = identity_path.read_text(encoding="utf-8")
            m = re.search(r"\*\*Name:\*\*\s*(.+)", content)
            if m:
                info["name"] = m.group(1).strip()
            m = re.search(r"\*\*Emoji:\*\*\s*(.+)", content)
            if m:
                info["emoji"] = m.group(1).strip()

    # Get last modified time from most recently modified .md file
    md_files = list(ws_dir.glob("*.md"))
    if md_files:
        latest = max(md_files, key=lambda f: f.stat().st_mtime)
        info["lastModified"] = datetime.fromtimestamp(latest.stat().st_mtime).isoformat()

    # Only return if we found something useful
    if info["name"] or any((ws_dir / f).exists() for f in ["SOUL.md", "IDENTITY.md"]):
        return info

    return None


def format_table(personas):
    """Format personas as a terminal table."""
    if not personas:
        return "No personas found."

    # Headers
    headers = ["Workspace", "Name", "Emoji", "Archetype", "Last Modified"]
    rows = []
    for p in personas:
        last_mod = p.get("lastModified", "")
        if last_mod:
            try:
                dt = datetime.fromisoformat(last_mod)
                last_mod = dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass
        rows.append([
            p["workspaceName"],
            p.get("name", "—"),
            p.get("emoji", ""),
            p.get("archetype", "—"),
            last_mod or "—",
        ])

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    # Format
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header_line = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"
    lines = [sep, header_line, sep]
    for row in rows:
        line = "|" + "|".join(f" {cell:<{widths[i]}} " for i, cell in enumerate(row)) + "|"
        lines.append(line)
    lines.append(sep)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List all personas across workspaces")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--base-dir", help="Base directory to scan (default: ~/.openclaw)")
    args = parser.parse_args()

    personas = scan_workspaces(args.base_dir)

    if args.json:
        print(json.dumps(personas, indent=2))
    else:
        print(f"\n🧬 Personas found: {len(personas)}\n")
        print(format_table(personas))


if __name__ == "__main__":
    main()
