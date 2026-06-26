"""Changelog formatting in multiple output styles."""

from typing import List, Dict, Optional
from datetime import datetime
from .config import CHANGE_TYPES, CHANGE_TYPE_EMOJIS, TELEGRAM_EMOJIS


def _group_by_type(entries: List[Dict]) -> Dict[str, List[Dict]]:
    """Group changelog entries by change type."""
    grouped = {}
    for entry in entries:
        change_type = entry.get("change_type", "CHANGED")
        if change_type not in grouped:
            grouped[change_type] = []
        grouped[change_type].append(entry)
    return grouped


def _filter_by_audience(entries: List[Dict], audience: str) -> List[Dict]:
    """Filter entries for a specific audience."""
    return [e for e in entries if e.get("audience") == audience or e.get("audience") is None]


def format_keepachangelog(project: Dict, version: str, entries: List[Dict]) -> str:
    """
    Format changelog in Keep a Changelog style.

    See: https://keepachangelog.com/
    """
    grouped = _group_by_type(entries)

    output = f"# Changelog - {project['name']}\n\n"
    output += f"All notable changes to this project will be documented in this file.\n\n"
    output += f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"

    # Standard order of sections
    section_order = ["ADDED", "CHANGED", "DEPRECATED", "REMOVED", "FIXED", "SECURITY", "PERFORMANCE"]

    for change_type in section_order:
        if change_type not in grouped:
            continue

        type_name = CHANGE_TYPES.get(change_type, change_type)
        output += f"### {type_name}\n\n"

        for entry in grouped[change_type]:
            desc = entry.get("description", "")
            author = entry.get("author", "")
            scope = entry.get("scope", "")

            line = f"- {desc}"
            if scope:
                line += f" ({scope})"
            if author:
                line += f" - {author}"

            output += line + "\n"

        output += "\n"

    return output.rstrip() + "\n"


def format_simple(project: Dict, version: str, entries: List[Dict]) -> str:
    """Format changelog as a simple bullet list."""
    grouped = _group_by_type(entries)

    output = f"{project['name']} - Version {version}\n"
    output += f"Released: {datetime.now().strftime('%Y-%m-%d')}\n\n"

    if not entries:
        output += "No changes.\n"
        return output

    for change_type in sorted(grouped.keys()):
        type_name = CHANGE_TYPES.get(change_type, change_type)
        output += f"{type_name}:\n"

        for entry in grouped[change_type]:
            output += f"  - {entry.get('description', '')}\n"

        output += "\n"

    return output.rstrip() + "\n"


def format_client_email(project: Dict, version: str, entries: List[Dict], client_name: str = "") -> str:
    """
    Format changelog for client-facing email.

    Filters to CLIENT audience entries only, uses friendly tone, no jargon.
    """
    # Filter for client-facing entries
    client_entries = _filter_by_audience(entries, "CLIENT")

    if not client_entries:
        client_entries = entries  # Fallback to all if none marked as client

    grouped = _group_by_type(client_entries)

    salutation = f"Hi {client_name}!" if client_name else "Hi!"

    output = f"{salutation}\n\n"
    output += f"We're excited to announce version {version} of {project['name']}!\n\n"
    output += f"Here's what's new:\n\n"

    # Reorder sections for client friendliness
    client_section_order = ["ADDED", "FIXED", "PERFORMANCE", "CHANGED", "SECURITY", "DEPRECATED", "REMOVED"]

    for change_type in client_section_order:
        if change_type not in grouped:
            continue

        type_name = CHANGE_TYPES.get(change_type, change_type)
        emoji = CHANGE_TYPE_EMOJIS.get(change_type, "")
        output += f"{emoji} {type_name}\n"

        for entry in grouped[change_type]:
            output += f"  • {entry.get('description', '')}\n"

        output += "\n"

    output += f"Thank you for your continued trust in {project['name']}!\n\n"
    output += f"Questions? Feel free to reach out.\n\n"
    output += f"Best regards\n"

    return output


def format_telegram(project: Dict, version: str, entries: List[Dict]) -> str:
    """
    Format changelog for Telegram (compact with emojis).

    Fits in a single message or minimal messages.
    """
    grouped = _group_by_type(entries)

    if not entries:
        return f"{project['name']} v{version}\nNo changes."

    output = f"📦 {project['name']} v{version}\n\n"

    for change_type in sorted(grouped.keys()):
        emoji = TELEGRAM_EMOJIS.get(change_type, "•")
        type_name = CHANGE_TYPES.get(change_type, change_type)
        output += f"{emoji} {type_name}\n"

        for entry in grouped[change_type]:
            desc = entry.get("description", "")
            # Truncate long descriptions
            if len(desc) > 60:
                desc = desc[:57] + "..."
            output += f"  • {desc}\n"

    return output.rstrip()


def format_release_notes(project: Dict, version: str, entries: List[Dict],
                        audience: str = "CLIENT", client_name: str = "") -> str:
    """
    Format release notes based on audience.

    Args:
        audience: "CLIENT", "INTERNAL", or "PUBLIC"
    """
    if audience == "CLIENT":
        return format_client_email(project, version, entries, client_name)
    elif audience == "PUBLIC":
        return format_keepachangelog(project, version, entries)
    elif audience == "INTERNAL":
        return format_keepachangelog(project, version, entries)
    else:
        return format_simple(project, version, entries)


def format_markdown_table(entries: List[Dict]) -> str:
    """Format entries as a markdown table."""
    if not entries:
        return "No entries."

    output = "| Type | Description | Author | Date |\n"
    output += "|------|-------------|--------|------|\n"

    for entry in entries:
        change_type = CHANGE_TYPES.get(entry.get("change_type", ""), "")
        desc = entry.get("description", "")[:50]  # Truncate for table
        author = entry.get("author", "")[:20]
        date = entry.get("created_at", "")[:10]

        output += f"| {change_type} | {desc} | {author} | {date} |\n"

    return output


def format_json_export(project: Dict, version: str, entries: List[Dict]) -> str:
    """Format entries as JSON (returns JSON string)."""
    import json

    export_data = {
        "project": {
            "name": project.get("name"),
            "version": version,
            "client": project.get("client_name"),
            "description": project.get("description"),
        },
        "entries": entries,
        "generated_at": datetime.now().isoformat()
    }

    return json.dumps(export_data, indent=2, default=str)
