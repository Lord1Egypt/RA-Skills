#!/usr/bin/env python3
"""
IDEA Manager - Structured manager for IDEAS.md

Provides CLI access to read, write, edit, and update entries in IDEAS.md
with validation and drift prevention.
"""

import argparse
import json
import re
import sys
import tempfile
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import shutil


class IdeaManager:
    """Manages structured entries in IDEAS.md"""

    def __init__(self, ideas_path: Path):
        self.ideas_path = ideas_path
        self.ideas_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Core file operations ---

    def read_entries(self) -> List[Dict]:
        """Parse IDEAS.md and return list of entry dicts.

        Creates an empty IDEAS.md template if the file doesn't exist yet.
        """
        if not self.ideas_path.exists():
            self._create_default_file()
            return []

        content = self.ideas_path.read_text()
        entries = []
        current = None
        in_details = False
        detail_lines = []

        for line in content.splitlines(keepends=True):
            # Check for entry header: ## [ID] title
            header_match = re.match(r'^##\s+\[([A-Z0-9-]+)\]\s+(.+)$', line.strip())
            if header_match:
                if current:
                    current['details'] = ''.join(detail_lines).strip()
                    entries.append(current)
                current = {
                    'id': header_match.group(1),
                    'title': header_match.group(2).strip(),
                }
                in_details = True
                detail_lines = []
                continue

            if not current:
                # Content before first entry - skip or preserve?
                continue

            # Metadata lines
            meta_match = re.match(r'^\*\*([A-Za-z\s]+)\*\*:\s+(.+)$', line.strip())
            if meta_match:
                key = meta_match.group(1).strip().lower().replace(' ', '_')
                value = meta_match.group(2).strip()
                if current:
                    current[key] = value
                continue

            # Collect detail lines (everything else until next entry)
            if in_details and not header_match:
                stripped = line.strip()
                if stripped == '---':
                    continue
                if not re.match(r'^\*\*[A-Za-z\s]+\*\*:', stripped):
                    detail_lines.append(line)

        if current:
            current['details'] = ''.join(detail_lines).strip()
            entries.append(current)

        return entries

    def _create_default_file(self) -> None:
        """Create a fresh IDEAS.md with template structure."""
        template = '''# Ideas

Entries are managed with the idea-manager skill.

## Format

Each idea is a markdown section:

```
## [IDEA-001] Short title

**Status**: pending
**Area**: area,domain
**Logged**: 2026-08-22

Details about the idea...

---
```

Use `idea-manager write` to add new entries, `idea-manager edit` to update them,
`idea-manager delete` to remove them, and `idea-manager archive` to prune
completed items.
'''
        self.ideas_path.write_text(template)
        print(f"Created new {self.ideas_path}")

    def _format_entry(self, entry: Dict) -> str:
        """Format a single entry as markdown."""
        lines = []
        lines.append(f"## [{entry['id']}] {entry.get('title', 'Untitled')}")
        lines.append("")

        # Standard fields in preferred order
        field_order = ['logged', 'priority', 'status', 'area', 'source', 'recurrence_count',
                       'first_seen', 'last_seen', 'related_files', 'pattern_key',
                       'tags', 'decision', 'owner']

        for field in field_order:
            if field in entry and entry[field]:
                label = field.replace('_', ' ').title()
                lines.append(f"**{label}**: {entry[field]}")

        # Any remaining fields
        for key, value in entry.items():
            if key not in ['id', 'title', 'details'] + field_order and value:
                label = key.replace('_', ' ').title()
                lines.append(f"**{label}**: {value}")

        lines.append("")

        # Details section
        if entry.get('details'):
            lines.append(entry['details'].strip())
            lines.append("")

        return '\n'.join(lines)

    def write_entries(self, entries: List[Dict]) -> None:
        """Write entries to IDEAS.md atomically."""

        # Sort entries: by recency (Logged date), then by ID
        def sort_key(e):
            logged = e.get('logged', '')
            return (logged, e.get('id', ''))

        sorted_entries = sorted(entries, key=sort_key, reverse=True)

        content_parts = []
        content_parts.append("# IDEAS.md\n")
        content_parts.append("Persistent ideas, proposals, and speculative directions.\n")
        content_parts.append("Entries here are durable but not necessarily active.\n")
        content_parts.append("\n")

        for entry in sorted_entries:
            content_parts.append(self._format_entry(entry))
            content_parts.append("---")
            content_parts.append("")

        content = '\n'.join(content_parts)

        # Atomic write via tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=self.ideas_path.parent) as f:
            f.write(content)
            temp_path = f.name

        try:
            shutil.move(temp_path, self.ideas_path)
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    # --- CLI actions ---

    def action_read(self, args) -> int:
        """Read and display entries."""
        entries = self.read_entries()

        if args.id:
            entries = [e for e in entries if e['id'].lower() == args.id.lower()]
            if not entries:
                print(f"Entry {args.id} not found.", file=sys.stderr)
                return 1

        if args.status:
            entries = [e for e in entries if e.get('status', '').lower() == args.status.lower()]

        if args.area:
            entries = [e for e in entries if args.area.lower() in e.get('area', '').lower()]

        if args.search:
            search_term = args.search.lower()
            entries = [
                e for e in entries
                if search_term in e.get('title', '').lower()
                or search_term in e.get('details', '').lower()
            ]

        if args.json:
            print(json.dumps(entries, indent=2))
        else:
            if not entries:
                print("No entries found.")
            else:
                for entry in entries:
                    print(self._format_entry(entry))

        return 0

    def action_write(self, args) -> int:
        """Add a new entry."""
        entries = self.read_entries()

        # Handle JSON input
        if args.json:
            json_str = args.json
            if json_str.startswith('@'):
                # Read from file
                filepath = Path(json_str[1:])
                try:
                    # Resolve relative paths against the IDEAS.md directory,
                    # then restrict to that directory
                    allowed_dir = self.ideas_path.parent.resolve()
                    if filepath.is_absolute():
                        resolved = filepath.resolve()
                    else:
                        resolved = (allowed_dir / filepath).resolve()
                    if allowed_dir not in resolved.parents:
                        print(f"Error: File outside IDEAS.md directory: {filepath}", file=sys.stderr)
                        return 1
                    with open(resolved, 'r') as f:
                        json_str = f.read()
                except FileNotFoundError:
                    print(f"Error: File not found: {filepath}", file=sys.stderr)
                    return 1
                except Exception as e:
                    print(f"Error reading file: {e}", file=sys.stderr)
                    return 1
            if len(json_str) > 10 * 1024 * 1024:  # 10 MB
                print("Error: JSON input too large (max 10 MB)", file=sys.stderr)
                return 1
            try:
                new_entry = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON - {e}", file=sys.stderr)
                return 1
            if not isinstance(new_entry, dict):
                print("Error: JSON must be an object/dict", file=sys.stderr)
                return 1
        else:
            # Build from CLI args
            if not args.title:
                print("Error: --title is required", file=sys.stderr)
                return 1
            if args.id:
                new_entry = {'id': args.id, 'title': args.title}
            elif args.auto_id:
                new_entry = {'id': self.generate_next_id(entries), 'title': args.title}
            else:
                print("Error: Either --id or --auto-id is required", file=sys.stderr)
                return 1

        # Validate required fields
        if 'id' not in new_entry or 'title' not in new_entry:
            print("Error: JSON input must include both 'id' and 'title' fields", file=sys.stderr)
            return 1

        # Check for duplicate ID
        entry_id = new_entry.get('id')
        if entry_id:
            existing = [e for e in entries if e.get('id', '').lower() == entry_id.lower()]
            if existing:
                print(f"Error: Entry with ID {entry_id} already exists.", file=sys.stderr)
                print("Use --edit to modify existing entries.", file=sys.stderr)
                return 1

        # Set logged date if not provided
        if args.logged:
            new_entry['logged'] = args.logged
        elif 'logged' not in new_entry:
            new_entry['logged'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        if args.priority:
            new_entry['priority'] = args.priority
        if args.status:
            new_entry['status'] = args.status
        if args.area:
            new_entry['area'] = args.area
        if args.source:
            new_entry['source'] = args.source
        if args.recurrence_count:
            new_entry['recurrence_count'] = args.recurrence_count
        if args.first_seen:
            new_entry['first_seen'] = args.first_seen
        if args.last_seen:
            new_entry['last_seen'] = args.last_seen
        if args.related_files:
            new_entry['related_files'] = args.related_files
        if args.pattern_key:
            new_entry['pattern_key'] = args.pattern_key
        if args.tags:
            new_entry['tags'] = args.tags
        if args.decision:
            new_entry['decision'] = args.decision
        if args.owner:
            new_entry['owner'] = args.owner
        if args.details:
            new_entry['details'] = args.details

        entries.append(new_entry)
        self.write_entries(entries)

        print(f"Added entry [{new_entry.get('id')}] {new_entry.get('title')}")
        return 0

    def generate_next_id(self, entries: List[Dict]) -> str:
        """Generate the next IDEA-NNN ID based on existing entries."""
        max_num = 0
        pattern = re.compile(r'^IDEA-(\d+)$')
        for entry in entries:
            match = pattern.match(entry.get('id', ''))
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
        return f'IDEA-{max_num + 1:03d}'

    def action_edit(self, args) -> int:
        """Edit an existing entry."""
        entries = self.read_entries()

        target = None
        for i, e in enumerate(entries):
            if e['id'].lower() == args.id.lower():
                target = (i, e)
                break

        if not target:
            print(f"Entry {args.id} not found.", file=sys.stderr)
            return 1

        idx, entry = target

        # Update fields if provided
        if args.title:
            entry['title'] = args.title
        if args.logged:
            entry['logged'] = args.logged
        if args.priority:
            entry['priority'] = args.priority
        if args.status:
            entry['status'] = args.status
        if args.area:
            entry['area'] = args.area
        if args.source:
            entry['source'] = args.source
        if args.recurrence_count:
            entry['recurrence_count'] = args.recurrence_count
        if args.first_seen:
            entry['first_seen'] = args.first_seen
        if args.last_seen:
            entry['last_seen'] = args.last_seen
        if args.related_files:
            entry['related_files'] = args.related_files
        if args.pattern_key:
            entry['pattern_key'] = args.pattern_key
        if args.tags:
            entry['tags'] = args.tags
        if args.decision:
            entry['decision'] = args.decision
        if args.owner:
            entry['owner'] = args.owner
        if args.details:
            entry['details'] = args.details

        entries[idx] = entry
        self.write_entries(entries)

        print(f"Updated entry [{args.id}]")
        return 0

    def action_delete(self, args) -> int:
        """Delete an entry by ID."""
        entries = self.read_entries()

        target = None
        for i, e in enumerate(entries):
            if e['id'].lower() == args.id.lower():
                target = (i, e)
                break

        if not target:
            print(f"Error: Entry {args.id} not found.", file=sys.stderr)
            return 1

        idx, entry = target
        entries.pop(idx)
        self.write_entries(entries)

        msg = f"Deleted entry [{entry['id']}] {entry['title']}"
        if args.decision:
            msg += f" — {args.decision}"
        print(msg)
        return 0

    def action_archive(self, args) -> int:
        """Archive completed entries, reindex remaining."""
        entries = self.read_entries()

        # --status is restricted to 'completed' only; other values are rejected
        target_status = args.status or 'completed'
        if target_status.lower() != 'completed':
            print(f"Error: --status can only be 'completed' (got '{target_status}').", file=sys.stderr)
            return 1

        to_archive = [e for e in entries if e.get('status', '').lower() == 'completed']

        if not to_archive:
            print(f"No completed entries to archive.", file=sys.stderr)
            return 1

        # Warning / confirmation
        archive_dir = self.ideas_path.parent / 'memory'
        today = datetime.now().strftime('%Y-%m-%d')
        archive_path = archive_dir / f'IDEAS-Archive-{today}.md'
        if not args.force:
            print(f"WARNING: This will archive {len(to_archive)} completed entr{'ies' if len(to_archive) != 1 else 'y'} to:")
            print(f"  {archive_path}")
            print(f"It will remove them from {self.ideas_path} and reindex all remaining entry IDs.")
            print("This operation is irreversible.")
            # In non-interactive mode, require --force
            if not sys.stdin.isatty():
                print("\nError: Non-interactive mode requires --force to archive.", file=sys.stderr)
                return 1
            try:
                response = input("\nType 'yes' to continue: ")
            except (EOFError, KeyboardInterrupt):
                print("\nArchive cancelled.", file=sys.stderr)
                return 1
            if response.strip().lower() != 'yes':
                print("Archive cancelled.")
                return 0

        # Build archive file
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Append to existing archive or create new
        existing = ''
        if archive_path.exists():
            existing = archive_path.read_text()

        archive_content = existing
        if archive_content and not archive_content.endswith('\n'):
            archive_content += '\n'

        for entry in to_archive:
            archive_content += f"\n## [{entry['id']}] {entry.get('title', 'Untitled')}\n\n"
            # Default archive: metadata only to avoid unintended data duplication
            archive_fields = ['logged', 'status', 'area', 'decision']
            if args.archive_details:
                archive_fields.extend([
                    'source', 'recurrence_count', 'first_seen', 'last_seen',
                    'related_files', 'pattern_key', 'tags', 'owner', 'details'
                ])
            for field in archive_fields:
                if entry.get(field):
                    label = field.replace('_', ' ').title()
                    archive_content += f"**{label}**: {entry[field]}\n"
            archive_content += "\n---\n"

        archive_path.write_text(archive_content.lstrip('\n'))
        print(f"Archived {len(to_archive)} entr{'ies' if len(to_archive) != 1 else 'y'} to {archive_path}")

        # Remove archived entries
        remaining = [e for e in entries if e not in to_archive]

        # Reindex: assign new sequential IDs
        id_map = {}
        for i, e in enumerate(remaining, start=1):
            old_id = e['id']
            new_id = f'IDEA-{i:03d}'
            id_map[old_id] = new_id
            e['id'] = new_id

        # Update any references to old IDs in related_files, etc.
        for e in remaining:
            if e.get('related_files'):
                for old_id, new_id in id_map.items():
                    e['related_files'] = e['related_files'].replace(old_id, new_id)

        self.write_entries(remaining)

        print(f"Reindexed {len(remaining)} remaining entr{'ies' if len(remaining) != 1 else 'y'}.")
        if id_map:
            print("ID mapping:")
            for old_id, new_id in id_map.items():
                print(f"  {old_id} -> {new_id}")
        return 0

    def action_status(self, args) -> int:
        """Show status summary."""
        entries = self.read_entries()

        status_counts = {}
        priority_counts = {}
        area_counts = {}

        for e in entries:
            status = e.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

            priority = e.get('priority', 'unknown')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

            area = e.get('area', 'unknown')
            area_counts[area] = area_counts.get(area, 0) + 1

        if args.json:
            # JSON output for programmatic use
            result = {
                'total': len(entries),
                'by_status': dict(sorted(status_counts.items())),
                'by_priority': dict(sorted(priority_counts.items())),
                'by_area': dict(sorted(area_counts.items()))
            }
            print(json.dumps(result, indent=2))
        else:
            # Human-readable output
            print(f"Total entries: {len(entries)}")
            print()
            print("By status:")
            for status, count in sorted(status_counts.items()):
                print(f"  {status}: {count}")
            print()
            print("By priority:")
            for priority, count in sorted(priority_counts.items()):
                print(f"  {priority}: {count}")
            print()
            print("By area:")
            for area, count in sorted(area_counts.items()):
                print(f"  {area}: {count}")

        return 0

    def action_report(self, args) -> int:
        """Generate a report of non-completed items."""
        entries = self.read_entries()

        # Default: exclude completed items
        if args.status:
            report_entries = [
                e for e in entries
                if e.get('status', 'pending').lower() == args.status.lower()
            ]
        else:
            report_entries = [
                e for e in entries
                if e.get('status', 'pending').lower() != 'completed'
            ]

        # Apply sorting
        if args.sort == 'id-asc':
            report_entries.sort(key=lambda e: e.get('id', ''))
        elif args.sort == 'id-desc':
            report_entries.sort(key=lambda e: e.get('id', ''), reverse=True)
        elif args.sort == 'status':
            report_entries.sort(key=lambda e: e.get('status', 'pending'))
        elif args.sort == 'date-asc':
            report_entries.sort(key=lambda e: e.get('logged', '9999-99-99'))
        elif args.sort == 'date-desc':
            report_entries.sort(key=lambda e: e.get('logged', '9999-99-99'), reverse=True)

        if not report_entries:
            if args.json:
                print("[]")
            else:
                print("No entries found.")
            return 0

        if args.json:
            print(json.dumps(report_entries, indent=2))
        else:
            # Markdown table
            print("| ID | Status | Title |")
            print("|---|---|---|")
            for e in report_entries:
                eid = e.get('id', '')
                status = e.get('status', 'pending')
                title = e.get('title', '')
                print(f"| {eid} | {status} | {title} |")
            print()
            total = len(entries)
            completed = len([
                e for e in entries
                if e.get('status', '').lower() == 'completed'
            ])
            print(f"\n**Total: {total} entries | Uncompleted: {len(report_entries)} | Completed: {completed}**")

        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Manage IDEAS.md entries with structure and validation'
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read entries')
    read_parser.add_argument('--id', help='Filter by entry ID')
    read_parser.add_argument('--status', help='Filter by status')
    read_parser.add_argument('--area', help='Filter by area')
    read_parser.add_argument('--search', help='Search keyword/phrase in title and details (case-insensitive)')
    read_parser.add_argument('--json', action='store_true', help='Output as JSON')
    read_parser.set_defaults(func='read')

    # Write command
    write_parser = subparsers.add_parser('write', help='Add new entry')
    write_parser.add_argument('--id', help='Entry ID (e.g. IDEA-001)')
    write_parser.add_argument('--title', help='Entry title')
    write_parser.add_argument('--logged', help='Logged date (ISO format)')
    write_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], help='Priority')
    write_parser.add_argument('--status', choices=['active', 'pending', 'completed', 'superseded', 'blocked'], help='Status')
    write_parser.add_argument('--area', help='Area/domain')
    write_parser.add_argument('--source', help='Source of the idea')
    write_parser.add_argument('--recurrence-count', type=int, help='Recurrence count')
    write_parser.add_argument('--first-seen', help='First seen date')
    write_parser.add_argument('--last-seen', help='Last seen date')
    write_parser.add_argument('--related-files', help='Related files')
    write_parser.add_argument('--pattern-key', help='Pattern key')
    write_parser.add_argument('--tags', help='Tags (comma-separated)')
    write_parser.add_argument('--json', help='JSON string or @file.json containing entry data (overrides individual fields)')
    write_parser.add_argument('--auto-id', action='store_true', help='Auto-generate next IDEA-NNN ID (alternative to --id)')
    write_parser.add_argument('--decision', help='Decision/outcome')
    write_parser.add_argument('--owner', help='Owner')
    write_parser.add_argument('--details', help='Details/description')
    write_parser.set_defaults(func='write')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an entry by ID')
    delete_parser.add_argument('--id', required=True, help='Entry ID to delete')
    delete_parser.add_argument('--decision', help='Reason for deletion')
    delete_parser.set_defaults(func='delete')

    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive completed entries, reindex remaining')
    archive_parser.add_argument('--status', help='Filter by status (default: completed)')
    archive_parser.add_argument('--archive-details', action='store_true', help='Include full entry details in the archive file (default: metadata only)')
    archive_parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation prompt')
    archive_parser.set_defaults(func='archive')

    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit existing entry')
    edit_parser.add_argument('--id', required=True, help='Entry ID to edit')
    edit_parser.add_argument('--title', help='New title')
    edit_parser.add_argument('--logged', help='Logged date')
    edit_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], help='Priority')
    edit_parser.add_argument('--status', choices=['active', 'pending', 'completed', 'superseded', 'blocked'], help='Status')
    edit_parser.add_argument('--area', help='Area/domain')
    edit_parser.add_argument('--source', help='Source')
    edit_parser.add_argument('--recurrence-count', type=int, help='Recurrence count')
    edit_parser.add_argument('--first-seen', help='First seen date')
    edit_parser.add_argument('--last-seen', help='Last seen date')
    edit_parser.add_argument('--related-files', help='Related files')
    edit_parser.add_argument('--pattern-key', help='Pattern key')
    edit_parser.add_argument('--tags', help='Tags')
    edit_parser.add_argument('--decision', help='Decision')
    edit_parser.add_argument('--owner', help='Owner')
    edit_parser.add_argument('--details', help='Details')
    edit_parser.set_defaults(func='edit')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show status summary')
    status_parser.add_argument('--json', action='store_true', help='Output as JSON')
    status_parser.set_defaults(func='status')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate a markdown table of non-completed items')
    report_parser.add_argument('--status', help='Filter by specific status (default: non-completed)')
    report_parser.add_argument('--sort', choices=['id-asc', 'id-desc', 'status', 'date-asc', 'date-desc'], default='id-asc', help='Sort order (default: id-asc)')
    report_parser.add_argument('--json', action='store_true', help='Output as JSON instead of markdown table')
    report_parser.set_defaults(func='report')

    # Global options
    parser.add_argument('--file', help='Path to IDEAS.md file (default: auto-detect)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Use --file flag, CWD/IDEAS.md, or fallback to workspace root
    if args.file:
        ideas_path = Path(args.file)
    elif (Path.cwd() / 'IDEAS.md').exists() or any(f.name == 'IDEAS.md' for f in Path.cwd().glob('*')):
        ideas_path = Path.cwd() / 'IDEAS.md'
    else:
        ideas_path = Path.home() / '.openclaw' / 'workspace' / 'IDEAS.md'

    # Ensure parent directory exists
    ideas_path.parent.mkdir(parents=True, exist_ok=True)

    manager = IdeaManager(ideas_path)

    action_map = {
        'read': manager.action_read,
        'write': manager.action_write,
        'edit': manager.action_edit,
        'delete': manager.action_delete,
        'archive': manager.action_archive,
        'status': manager.action_status,
        'report': manager.action_report,
    }

    try:
        return action_map[args.command](args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
