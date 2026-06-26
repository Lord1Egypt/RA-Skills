#!/usr/bin/env python3
"""
Fleet view: show a table of all agents across all machines/workspaces.
Aggregates persona data from all workspace directories.

Usage:
    python3 persona-fleet.py
    python3 persona-fleet.py --json
    python3 persona-fleet.py --base-dir ~/.openclaw
"""

import argparse
import json
import os
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib.machinery import SourceFileLoader

persona_list = SourceFileLoader(
    "persona_list", str(Path(__file__).resolve().parent / "persona-list.py")
).load_module()


def get_machine_info():
    """Get current machine identifier."""
    return {
        "hostname": platform.node() or "unknown",
        "platform": platform.system(),
        "user": os.getenv("USER", os.getenv("USERNAME", "unknown")),
    }


def build_fleet_view(base_dir=None):
    """Build fleet view with machine context."""
    machine = get_machine_info()
    personas = persona_list.scan_workspaces(base_dir)

    fleet = []
    for p in personas:
        entry = {
            "machine": machine["hostname"],
            "user": machine["user"],
            **p,
        }
        fleet.append(entry)

    return fleet, machine


def format_fleet_table(fleet, machine):
    """Format fleet as a rich terminal table."""
    if not fleet:
        return "No agents found in fleet."

    headers = ["Machine", "Workspace", "Name", "Emoji", "Archetype", "Status"]
    rows = []
    for agent in fleet:
        rows.append([
            agent.get("machine", "—"),
            agent.get("workspaceName", "—"),
            agent.get("name", "—"),
            agent.get("emoji", ""),
            agent.get("archetype", "—"),
            "active" if agent.get("lastModified") else "inactive",
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
    parser = argparse.ArgumentParser(description="Fleet view of all agents")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--base-dir", help="Base directory to scan")
    args = parser.parse_args()

    fleet, machine = build_fleet_view(args.base_dir)

    if args.json:
        print(json.dumps({"machine": machine, "agents": fleet}, indent=2))
    else:
        print(f"\n🚀 Agent Fleet — {machine['hostname']} ({machine['user']}@{machine['platform']})\n")
        print(format_fleet_table(fleet, machine))
        print(f"\nTotal agents: {len(fleet)}")


if __name__ == "__main__":
    main()
