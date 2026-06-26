#!/usr/bin/env python3
"""
Long-Term Memory Manager
Consolidates daily memories, manages MEMORY.md, and archives old content.
"""

import argparse
import json
import os
import re
import shutil
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# Default paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
ARCHIVE_DIR = WORKSPACE / ".memory-archive"


def ensure_directories():
    """Ensure memory directories exist."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def get_daily_files(days: Optional[int] = None, older_than: Optional[int] = None) -> list:
    """Get daily memory files based on criteria."""
    files = []

    if not MEMORY_DIR.exists():
        return files

    now = datetime.now()

    for file_path in sorted(MEMORY_DIR.glob("*.md")):
        try:
            file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")

            if days is not None:
                cutoff = now - timedelta(days=days)
                if file_date >= cutoff:
                    files.append(file_path)
            elif older_than is not None:
                cutoff = now - timedelta(days=older_than)
                if file_date < cutoff:
                    files.append(file_path)
            else:
                files.append(file_path)
        except ValueError:
            continue

    return files


def read_memory_md() -> dict:
    """Parse MEMORY.md into sections."""
    if not MEMORY_FILE.exists():
        return {"sections": {}, "raw": ""}

    content = MEMORY_FILE.read_text(encoding="utf-8")
    sections = {}

    # Split by headers
    current_section = "header"
    current_content = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Don't forget the last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return {"sections": sections, "raw": content}


def write_memory_md(sections: dict, preserve_order: bool = True):
    """Write sections back to MEMORY.md."""
    # Define preferred section order
    preferred_order = [
        "User Profile",
        "Key Decisions",
        "Important Facts",
        "Lessons Learned",
        "Active Projects",
        "Recurring Context",
        "Notes",
    ]

    lines = ["# MEMORY.md - Long-Term Memory\n"]

    written = set()

    # Write in preferred order
    for section in preferred_order:
        if section in sections and sections[section]:
            lines.append(f"## {section}\n")
            lines.append(sections[section])
            lines.append("\n")
            written.add(section)

    # Write remaining sections
    for section, content in sections.items():
        if section not in written and content and section != "header":
            lines.append(f"## {section}\n")
            lines.append(content)
            lines.append("\n")

    MEMORY_FILE.write_text("\n".join(lines), encoding="utf-8")


def extract_facts_from_file(file_path: Path) -> list:
    """Extract key facts from a daily memory file."""
    facts = []
    content = file_path.read_text(encoding="utf-8")

    # Look for decision markers
    decision_patterns = [
        r'(?:决策|决定|Decision):\s*(.+)',
        r'(?:选择|Choose)\s+(.+)',
        r'(?:确定|确认|Confirmed)\s+(.+)',
    ]

    for pattern in decision_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        facts.extend([{"type": "decision", "content": m.strip(), "source": file_path.name} for m in matches])

    # Look for preference markers
    preference_patterns = [
        r'(?:偏好|喜欢|prefer)\s+(.+)',
        r'(?:不喜欢|avoid)\s+(.+)',
        r'(?:习惯|usually)\s+(.+)',
    ]

    for pattern in preference_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        facts.extend([{"type": "preference", "content": m.strip(), "source": file_path.name} for m in matches])

    # Look for important markers
    important_patterns = [
        r'(?:重要|important|key):\s*(.+)',
        r'(?:记住|remember|note):\s*(.+)',
        r'(?:账号|account|credential):\s*(.+)',
    ]

    for pattern in important_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        facts.extend([{"type": "fact", "content": m.strip(), "source": file_path.name} for m in matches])

    return facts


def consolidate(days: int = 7, auto_archive: bool = False) -> dict:
    """Consolidate recent daily memories into MEMORY.md."""
    ensure_directories()

    files = get_daily_files(days=days)
    if not files:
        return {"status": "no_files", "message": f"No daily files found in last {days} days"}

    # Extract facts from all files
    all_facts = []
    for file_path in files:
        all_facts.extend(extract_facts_from_file(file_path))

    # Group by type
    decisions = [f for f in all_facts if f["type"] == "decision"]
    preferences = [f for f in all_facts if f["type"] == "preference"]
    facts = [f for f in all_facts if f["type"] == "fact"]

    # Read current MEMORY.md
    memory = read_memory_md()

    # Update sections
    if decisions:
        decision_section = memory["sections"].get("Key Decisions", "")
        for d in decisions:
            date_prefix = d["source"].replace(".md", "")
            entry = f"- [{date_prefix}] {d['content']}\n"
            if entry not in decision_section:
                decision_section += entry
        memory["sections"]["Key Decisions"] = decision_section

    if preferences:
        profile_section = memory["sections"].get("User Profile", "")
        for p in preferences:
            entry = f"- {p['content']}\n"
            if entry not in profile_section:
                profile_section += entry
        memory["sections"]["User Profile"] = profile_section

    if facts:
        facts_section = memory["sections"].get("Important Facts", "")
        for f in facts:
            entry = f"- {f['content']}\n"
            if entry not in facts_section:
                facts_section += entry
        memory["sections"]["Important Facts"] = facts_section

    # Write back
    write_memory_md(memory["sections"])

    result = {
        "status": "success",
        "files_processed": len(files),
        "facts_extracted": len(all_facts),
        "decisions": len(decisions),
        "preferences": len(preferences),
        "facts": len(facts),
    }

    # Auto archive if requested
    if auto_archive:
        archive_result = archive(older_than=days)
        result["archived"] = archive_result

    return result


def archive(older_than: int = 30, consolidate_first: bool = False) -> dict:
    """Archive old daily memory files."""
    ensure_directories()

    files = get_daily_files(older_than=older_than)
    if not files:
        return {"status": "no_files", "message": f"No files older than {older_than} days"}

    # Group files by month
    by_month = {}
    for file_path in files:
        try:
            file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")
            month_key = file_date.strftime("%Y-%m")
            if month_key not in by_month:
                by_month[month_key] = []
            by_month[month_key].append(file_path)
        except ValueError:
            continue

    archived_count = 0

    for month_key, month_files in by_month.items():
        # Create archive directory for this month
        month_archive = ARCHIVE_DIR / month_key
        month_archive.mkdir(parents=True, exist_ok=True)
        raw_dir = month_archive / "raw"
        raw_dir.mkdir(exist_ok=True)

        # Optionally consolidate
        if consolidate_first:
            consolidated_content = []
            for file_path in month_files:
                content = file_path.read_text(encoding="utf-8")
                consolidated_content.append(f"### {file_path.stem}\n\n{content}\n")

            consolidated_file = month_archive / "consolidated.md"
            consolidated_file.write_text("\n".join(consolidated_content), encoding="utf-8")

        # Move files to archive
        for file_path in month_files:
            dest = raw_dir / file_path.name
            shutil.move(str(file_path), str(dest))
            archived_count += 1

    return {
        "status": "success",
        "files_archived": archived_count,
        "months": list(by_month.keys()),
    }


def search(query: str, include_archive: bool = False, context_lines: int = 3) -> list:
    """Search through memory files."""
    results = []

    # Search daily files
    for file_path in get_daily_files():
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = "\n".join(lines[start:end])

                results.append({
                    "date": file_path.stem,
                    "file": str(file_path.relative_to(WORKSPACE)),
                    "line": i + 1,
                    "context": context,
                    "match": line,
                })

    # Search MEMORY.md
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding="utf-8")
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = "\n".join(lines[start:end])

                results.append({
                    "date": "MEMORY.md",
                    "file": "MEMORY.md",
                    "line": i + 1,
                    "context": context,
                    "match": line,
                })

    # Search archive if requested
    if include_archive:
        for archive_month in ARCHIVE_DIR.iterdir():
            if archive_month.is_dir():
                raw_dir = archive_month / "raw"
                if raw_dir.exists():
                    for file_path in raw_dir.glob("*.md"):
                        content = file_path.read_text(encoding="utf-8")
                        lines = content.split("\n")

                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                start = max(0, i - context_lines)
                                end = min(len(lines), i + context_lines + 1)
                                context = "\n".join(lines[start:end])

                                results.append({
                                    "date": file_path.stem,
                                    "file": str(file_path.relative_to(WORKSPACE)),
                                    "line": i + 1,
                                    "context": context,
                                    "match": line,
                                    "archived": True,
                                })

    return results


def health_check() -> dict:
    """Check memory system health."""
    ensure_directories()

    metrics = {
        "daily_files": len(list(MEMORY_DIR.glob("*.md"))),
        "memory_md_exists": MEMORY_FILE.exists(),
        "memory_md_size": 0,
        "archive_exists": ARCHIVE_DIR.exists(),
        "archive_months": 0,
        "last_consolidation": None,
    }

    if MEMORY_FILE.exists():
        metrics["memory_md_size"] = MEMORY_FILE.stat().st_size

    if ARCHIVE_DIR.exists():
        metrics["archive_months"] = len(list(ARCHIVE_DIR.iterdir()))

    # Determine status
    status = "healthy"
    issues = []

    if metrics["daily_files"] > 60:
        status = "warning"
        issues.append(f"Too many daily files ({metrics['daily_files']})")

    if metrics["memory_md_size"] > 100 * 1024:
        status = "warning"
        issues.append(f"MEMORY.md too large ({metrics['memory_md_size'] / 1024:.1f}KB)")

    if not metrics["memory_md_exists"]:
        status = "critical"
        issues.append("MEMORY.md does not exist")

    return {
        "status": status,
        "metrics": metrics,
        "issues": issues if issues else None,
    }


def generate_summary(output_file: Optional[str] = None) -> str:
    """Generate a summary of memory state."""
    ensure_directories()

    lines = [
        f"# Memory Summary: {datetime.now().strftime('%Y-%m-%d')}",
        "",
    ]

    # Health
    health = health_check()
    lines.append(f"## Health Status: {health['status']}")
    lines.append("")

    if health["issues"]:
        lines.append("### Issues")
        for issue in health["issues"]:
            lines.append(f"- {issue}")
        lines.append("")

    # Statistics
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- Daily files: {health['metrics']['daily_files']}")
    lines.append(f"- MEMORY.md size: {health['metrics']['memory_md_size'] / 1024:.1f}KB")
    lines.append(f"- Archive months: {health['metrics']['archive_months']}")
    lines.append("")

    # MEMORY.md sections
    memory = read_memory_md()
    if memory["sections"]:
        lines.append("## MEMORY.md Sections")
        lines.append("")
        for section, content in memory["sections"].items():
            if content:
                lines.append(f"### {section}")
                lines.append(f"Lines: {len(content.splitlines())}")
                lines.append("")

    summary = "\n".join(lines)

    if output_file:
        Path(output_file).write_text(summary, encoding="utf-8")
        print(f"Summary written to {output_file}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Long-Term Memory Manager")
    parser.add_argument("--consolidate", action="store_true", help="Consolidate daily memories")
    parser.add_argument("--archive", action="store_true", help="Archive old memories")
    parser.add_argument("--extract-facts", action="store_true", help="Extract key facts")
    parser.add_argument("--search", metavar="QUERY", help="Search memories")
    parser.add_argument("--summary", action="store_true", help="Generate memory summary")
    parser.add_argument("--health", action="store_true", help="Check memory health")

    parser.add_argument("--days", type=int, default=7, help="Days to process (default: 7)")
    parser.add_argument("--older-than", type=int, default=30, help="Archive threshold (default: 30)")
    parser.add_argument("--auto-archive", action="store_true", help="Auto-archive after consolidation")
    parser.add_argument("--consolidate-first", action="store_true", help="Consolidate before archiving")
    parser.add_argument("--include-archive", action="store_true", help="Include archived memories in search")
    parser.add_argument("--context", type=int, default=3, help="Context lines for search")
    parser.add_argument("--output", help="Output file")

    args = parser.parse_args()

    if args.consolidate:
        result = consolidate(days=args.days, auto_archive=args.auto_archive)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.archive:
        result = archive(older_than=args.older_than, consolidate_first=args.consolidate_first)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.extract_facts:
        files = get_daily_files(days=args.days)
        all_facts = []
        for file_path in files:
            all_facts.extend(extract_facts_from_file(file_path))
        print(json.dumps(all_facts, indent=2, ensure_ascii=False))

    elif args.search:
        results = search(args.search, include_archive=args.include_archive, context_lines=args.context)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.summary:
        summary = generate_summary(output_file=args.output)
        if not args.output:
            print(summary)

    elif args.health:
        result = health_check()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
