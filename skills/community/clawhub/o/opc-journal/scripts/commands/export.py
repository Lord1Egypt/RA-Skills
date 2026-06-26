"""Journal command: export - actual local file export."""
import glob
import json
import os
from pathlib import Path

from utils.storage import build_customer_dir
from scripts.commands._meta import get_language


def run(customer_id: str, args: dict) -> dict:
    """Export journal entries locally to markdown or json."""
    export_format = args.get("format", "markdown")
    time_range = args.get("time_range", "all")
    output_path = args.get("output_path", "")
    
    lang = get_language(customer_id)
    base = os.path.expanduser(build_customer_dir(customer_id))
    memory_dir = os.path.join(base, "memory")
    
    if not os.path.exists(memory_dir):
        return {
            "status": "error",
            "result": None,
            "message": "No memory directory found",
        }
    
    files = sorted(glob.glob(os.path.join(memory_dir, "*.md")))
    entries = []
    
    for f in files:
        content = Path(f).read_text(encoding="utf-8")
        file_entries = _extract_entries(content, f)
        entries.extend(file_entries)
    
    # Sort by date
    entries.sort(key=lambda x: x.get("date", "00-00-00"))
    
    # Filter by time range if specified
    if time_range != "all" and time_range:
        entries = _filter_by_time_range(entries, time_range)
    
    if not entries:
        return {
            "status": "success",
            "result": {
                "customer_id": customer_id,
                "export_format": export_format,
                "time_range": time_range,
                "entry_count": 0,
                "output_path": "",
                "language": lang,
            },
            "message": "No entries found to export",
        }
    
    # Generate output
    if export_format.lower() == "json":
        exported_content = json.dumps({"customer_id": customer_id, "entries": entries}, indent=2, ensure_ascii=False)
        ext = ".json"
    else:
        exported_content = _format_markdown(customer_id, entries)
        ext = ".md"
    
    # Write to file if output_path not provided, use default
    if not output_path:
        output_path = os.path.join(base, f"export_{customer_id}{ext}")
    else:
        output_path = os.path.expanduser(output_path)
    
    try:
        Path(output_path).write_text(exported_content, encoding="utf-8")
    except Exception as e:
        return {
            "status": "error",
            "result": None,
            "message": f"Failed to write export file: {e}",
        }
    
    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "export_format": export_format,
            "time_range": time_range,
            "entry_count": len(entries),
            "output_path": output_path,
            "language": lang,
        },
        "message": f"Exported {len(entries)} entries to {output_path}",
    }


def _extract_entries(content: str, file_path: str) -> list:
    """Extract individual entries from memory file content."""
    entries = []
    separator = "\n\n---\ntype: entry"
    if separator not in content:
        separator = "---\ntype: entry"
    
    parts = content.split(separator)
    
    for idx, part in enumerate(parts):
        if idx == 0 and not part.strip().startswith("type: entry"):
            if "type: charter" in part:
                continue
            if not part.strip():
                continue
            block = part
        else:
            if idx > 0:
                block = "---\ntype: entry" + part
            else:
                block = part
        
        entry = _parse_entry_block(block, file_path)
        if entry:
            entries.append(entry)
    
    return entries


def _parse_entry_block(block: str, file_path: str) -> dict:
    """Parse a single entry block to extract metadata and body."""
    lines = block.split("\n")
    frontmatter = {}
    in_frontmatter = False
    body_lines = []
    
    for i, line in enumerate(lines):
        if line.strip() == "---" and i == 0:
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            continue
        
        if in_frontmatter:
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip()] = val.strip()
        else:
            body_lines.append(line)
    
    body = "\n".join(body_lines).strip()
    
    if frontmatter.get("type") != "entry":
        return None
    
    return {
        "entry_id": frontmatter.get("entry_id", ""),
        "date": frontmatter.get("date", ""),
        "day": frontmatter.get("day", ""),
        "type": frontmatter.get("type", ""),
        "emotion": frontmatter.get("emotion", ""),
        "language": frontmatter.get("language", ""),
        "file": file_path,
        "body": body,
    }


def _format_markdown(customer_id: str, entries: list) -> str:
    """Format entries as markdown document."""
    lines = [
        f"# Journal Export - {customer_id}",
        "",
        f"Total entries: {len(entries)}",
        "",
        "---",
        "",
    ]
    
    for entry in entries:
        lines.append(f"## Entry {entry.get('entry_id', 'N/A')} - Day {entry.get('day', 'N/A')}")
        lines.append("")
        lines.append(f"- **Date:** {entry.get('date', 'N/A')}")
        lines.append(f"- **Emotion:** {entry.get('emotion', 'N/A') or 'None'}")
        lines.append("")
        lines.append(entry.get("body", ""))
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def _filter_by_time_range(entries: list, time_range: str) -> list:
    """Filter entries by a simple time range expression like '7d', '30d', '1m'."""
    from datetime import datetime, timedelta
    from utils.timezone import now_tz
    
    now = now_tz()
    days = 0
    
    time_range = str(time_range).lower().strip()
    if time_range.endswith("d"):
        try:
            days = int(time_range[:-1])
        except ValueError:
            days = 0
    elif time_range.endswith("m"):
        try:
            days = int(time_range[:-1]) * 30
        except ValueError:
            days = 0
    elif time_range.endswith("w"):
        try:
            days = int(time_range[:-1]) * 7
        except ValueError:
            days = 0
    
    if days <= 0:
        return entries
    
    cutoff = now - timedelta(days=days)
    filtered = []
    
    for entry in entries:
        date_str = entry.get("date", "")
        try:
            entry_date = datetime.strptime(date_str, "%d-%m-%y")
            if entry_date >= cutoff:
                filtered.append(entry)
        except (ValueError, TypeError):
            # If we can't parse the date, include it to be safe
            filtered.append(entry)
    
    return filtered
