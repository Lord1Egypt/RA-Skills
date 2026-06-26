#!/usr/bin/env python3
"""
Generate MEMORY.md, memory/ directory, HEARTBEAT.md, and AGENTS.md.

Usage:
    python3 generate-memory.py --name "Pepper" --emoji "🌶️" --creature "Executive assistant" --workspace /path/to/workspace
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.templates import render_template


def generate_memory(context):
    """Generate MEMORY.md content."""
    return render_template("MEMORY.md.hbs", context)


def generate_heartbeat(context):
    """Generate HEARTBEAT.md content."""
    return render_template("HEARTBEAT.md.hbs", context)


def generate_agents(context):
    """Generate AGENTS.md content."""
    return render_template("AGENTS.md.hbs", context)


def create_daily_note(workspace, name, emoji, today):
    """Create the first daily memory note."""
    memory_dir = Path(workspace) / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    note_path = memory_dir / f"{today}.md"
    content = f"# {today} — {name} {emoji}\n\n- Persona created via AI Persona Engine.\n"
    note_path.write_text(content, encoding="utf-8")
    return str(note_path)


def write_file(path, content):
    """Write content to file, creating parent dirs."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate memory infrastructure")
    parser.add_argument("--input", "-i", help="JSON config file")
    parser.add_argument("--workspace", "-w", help="Workspace directory", required=True)
    parser.add_argument("--name", help="Agent name")
    parser.add_argument("--emoji", help="Agent emoji")
    parser.add_argument("--creature", help="Agent description")
    parser.add_argument("--user-name", help="User's name")
    parser.add_argument("--daily-notes", action="store_true", default=True)
    parser.add_argument("--no-daily-notes", action="store_false", dest="daily_notes")
    parser.add_argument("--long-term", action="store_true", default=True)
    parser.add_argument("--no-long-term", action="store_false", dest="long_term")
    parser.add_argument("--heartbeat-maintenance", action="store_true", default=True)
    parser.add_argument("--no-heartbeat-maintenance", action="store_false", dest="heartbeat_maintenance")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            context = json.load(f)
    elif args.name:
        context = {}
    elif not sys.stdin.isatty():
        try:
            context = json.load(sys.stdin)
        except json.JSONDecodeError:
            context = {}
    else:
        context = {}

    if args.name:
        context["name"] = args.name
    if args.emoji:
        context["emoji"] = args.emoji
    if args.creature:
        context["creature"] = args.creature
    if args.user_name:
        context["userName"] = args.user_name

    context.setdefault("name", "Agent")
    context.setdefault("emoji", "")
    context.setdefault("creature", "AI assistant")

    today = date.today().isoformat()
    context["createdDate"] = today
    context["dailyNotes"] = args.daily_notes
    context["longTermCuration"] = args.long_term
    context["heartbeatMaintenance"] = args.heartbeat_maintenance

    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    # Generate MEMORY.md
    memory_content = generate_memory(context)
    write_file(workspace / "MEMORY.md", memory_content)
    print(f"Generated: {workspace / 'MEMORY.md'}", file=sys.stderr)

    # Generate HEARTBEAT.md
    heartbeat_content = generate_heartbeat(context)
    write_file(workspace / "HEARTBEAT.md", heartbeat_content)
    print(f"Generated: {workspace / 'HEARTBEAT.md'}", file=sys.stderr)

    # Generate AGENTS.md
    agents_context = dict(context)
    agents_context.setdefault("platformNotes", [])
    agents_content = generate_agents(agents_context)
    write_file(workspace / "AGENTS.md", agents_content)
    print(f"Generated: {workspace / 'AGENTS.md'}", file=sys.stderr)

    # Create memory directory and first daily note
    note_path = create_daily_note(workspace, context["name"], context["emoji"], today)
    print(f"Generated: {note_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
