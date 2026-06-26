#!/usr/bin/env python3
"""Nex Changelog - Changelog & Version Notes Generator for client-facing release communication."""

import sys
import argparse
import re
from pathlib import Path
from lib.storage import ChangelogDB
from lib.config import CHANGE_TYPES, AUDIENCE_TYPES, TEMPLATE_STYLES, DATA_DIR
from lib.formatter import (
    format_keepachangelog, format_simple, format_client_email,
    format_telegram, format_release_notes, format_markdown_table, format_json_export
)
from lib.git_parser import (
    generate_entries_from_git, get_latest_tag, parse_conventional_commit,
    categorize_commit, validate_semver, increment_version
)

FOOTER = "[Nex Changelog by Nex AI | nex-ai.be]"


def init_db():
    """Initialize database."""
    return ChangelogDB()


def cmd_add(args):
    """Add a changelog entry."""
    db = init_db()

    # Get or create project
    if args.project:
        project = db.get_project(args.project)
        if not project:
            project_id = db.save_project(args.project)
            project = db.get_project_by_id(project_id)
        else:
            project_id = project['id']
    else:
        print("Error: --project is required")
        sys.exit(1)

    # Parse natural language if provided
    if args.description:
        description = args.description
        change_type = args.type or "CHANGED"
        audience = args.audience or "INTERNAL"

        # Try to infer type from description
        desc_lower = description.lower()
        if desc_lower.startswith("fixed ") or desc_lower.startswith("fix "):
            change_type = "FIXED"
            audience = "CLIENT"
        elif desc_lower.startswith("added ") or desc_lower.startswith("add "):
            change_type = "ADDED"
            audience = "CLIENT"
        elif desc_lower.startswith("removed ") or desc_lower.startswith("remove "):
            change_type = "REMOVED"
        elif "security" in desc_lower:
            change_type = "SECURITY"
            audience = "CLIENT"
        elif "deprecated" in desc_lower:
            change_type = "DEPRECATED"
        elif "performance" in desc_lower or "faster" in desc_lower or "improved" in desc_lower:
            change_type = "PERFORMANCE"
            audience = "CLIENT"

    else:
        print("Error: description is required")
        sys.exit(1)

    # Save entry
    entry_id = db.save_entry(
        project_id=project_id,
        version=args.version,
        change_type=change_type,
        description=description,
        audience=audience,
        details=args.details,
        author=args.author,
        commit_hash=args.commit_hash,
        breaking=args.breaking
    )

    print(f"Added entry #{entry_id} to {project['name']}")
    if args.version:
        print(f"  Version: {args.version}")
    print(f"  Type: {change_type}")
    print(f"  Description: {description}")
    print(f"  Audience: {audience}")
    print(f"\n{FOOTER}")


def cmd_git(args):
    """Import changelog entries from git commits."""
    db = init_db()

    if not args.repo:
        print("Error: repo path is required")
        sys.exit(1)

    repo_path = args.repo
    if not Path(repo_path).is_dir():
        print(f"Error: {repo_path} is not a directory")
        sys.exit(1)

    # Get or create project
    project_name = args.project or Path(repo_path).name
    project = db.get_project(project_name)
    if not project:
        project_id = db.save_project(
            project_name,
            repo_path=repo_path,
            description=args.description
        )
        project = db.get_project_by_id(project_id)
    else:
        project_id = project['id']

    # Get entries from git
    try:
        entries = generate_entries_from_git(repo_path, since_tag=args.since)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not entries:
        print(f"No commits found in {repo_path}")
        print(f"\n{FOOTER}")
        return

    # Save entries
    count = 0
    for entry in entries:
        db.save_entry(
            project_id=project_id,
            version=args.version,
            change_type=entry['change_type'],
            description=entry['description'],
            audience=entry.get('audience'),
            details=entry.get('details'),
            author=entry.get('author'),
            commit_hash=entry.get('commit_hash'),
            breaking=entry.get('breaking', False)
        )
        count += 1

    print(f"Imported {count} entries from {repo_path} to {project['name']}")
    if args.version:
        print(f"  Version: {args.version}")
    if args.since:
        print(f"  Since: {args.since}")
    print(f"\n{FOOTER}")


def cmd_release(args):
    """Create a release for a project."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    if not args.version:
        print("Error: --version is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    project_id = project['id']

    # Create release
    release_id = db.create_release(
        project_id=project_id,
        version=args.version,
        summary=args.summary,
        client_notes=args.client_notes,
        internal_notes=args.internal_notes
    )

    print(f"Created release #{release_id}: {project['name']} v{args.version}")
    if args.summary:
        print(f"  Summary: {args.summary}")
    print(f"\n{FOOTER}")


def cmd_show(args):
    """Show changelog for a project or version."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    project_id = project['id']

    # Get entries
    entries = db.list_entries(
        project_id=project_id,
        version=args.version,
        change_type=args.type,
        audience=args.audience
    )

    if not entries:
        print(f"No entries found for {project['name']}")
        print(f"\n{FOOTER}")
        return

    # Format output
    version = args.version or "All Versions"
    if args.format == "keepachangelog":
        output = format_keepachangelog(project, version, entries)
    elif args.format == "simple":
        output = format_simple(project, version, entries)
    elif args.format == "table":
        output = format_markdown_table(entries)
    elif args.format == "json":
        output = format_json_export(project, version, entries)
    else:
        output = format_keepachangelog(project, version, entries)

    print(output)
    print(f"\n{FOOTER}")


def cmd_list(args):
    """List changelog entries."""
    db = init_db()

    project = None
    if args.project:
        project = db.get_project(args.project)
        if not project:
            print(f"Error: Project '{args.project}' not found")
            sys.exit(1)

    entries = db.list_entries(
        project_id=project['id'] if project else None,
        version=args.version,
        change_type=args.type,
        audience=args.audience
    )

    if not entries:
        print("No entries found")
        print(f"\n{FOOTER}")
        return

    print(f"Found {len(entries)} entries:\n")
    for entry in entries:
        proj = db.get_project_by_id(entry['project_id'])
        print(f"• [{entry['change_type']}] {entry['description']}")
        print(f"  Project: {proj['name']}")
        if entry['version']:
            print(f"  Version: {entry['version']}")
        if entry['audience']:
            print(f"  Audience: {entry['audience']}")
        if entry['author']:
            print(f"  Author: {entry['author']}")
        print()

    print(f"{FOOTER}")


def cmd_unreleased(args):
    """Show unreleased entries for a project."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    entries = db.get_unreleased_entries(project['id'])

    if not entries:
        print(f"No unreleased entries for {project['name']}")
        print(f"\n{FOOTER}")
        return

    print(f"Unreleased entries for {project['name']} ({len(entries)} total):\n")
    for entry in entries:
        print(f"• [{entry['change_type']}] {entry['description']}")
        if entry['audience']:
            print(f"  Audience: {entry['audience']}")
        if entry['author']:
            print(f"  Author: {entry['author']}")
        print()

    print(f"{FOOTER}")


def cmd_email(args):
    """Generate a client-facing email for a release."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    if not args.version:
        print("Error: --version is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    entries = db.list_entries(project_id=project['id'], version=args.version)

    if not entries:
        print(f"No entries for {project['name']} v{args.version}")
        print(f"\n{FOOTER}")
        return

    client_name = args.client or project.get('client_name', '')
    output = format_client_email(project, args.version, entries, client_name)

    print(output)
    print(f"\n{FOOTER}")


def cmd_telegram(args):
    """Generate a Telegram message for a release."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    if not args.version:
        print("Error: --version is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    entries = db.list_entries(project_id=project['id'], version=args.version)

    if not entries:
        print(f"No entries for {project['name']} v{args.version}")
        print(f"\n{FOOTER}")
        return

    output = format_telegram(project, args.version, entries)

    print(output)
    print(f"\n{FOOTER}")


def cmd_project(args):
    """Manage projects."""
    db = init_db()

    if args.action == "add":
        if not args.name:
            print("Error: --name is required")
            sys.exit(1)

        project_id = db.save_project(
            args.name,
            repo_path=args.repo_path,
            client_name=args.client_name,
            client_email=args.client_email,
            description=args.description
        )

        print(f"Created/updated project: {args.name} (ID: {project_id})")
        print(f"\n{FOOTER}")

    elif args.action == "list":
        projects = db.list_projects()

        if not projects:
            print("No projects found")
            print(f"\n{FOOTER}")
            return

        print(f"Projects ({len(projects)} total):\n")
        for proj in projects:
            print(f"• {proj['name']}")
            if proj['description']:
                print(f"  Description: {proj['description']}")
            if proj['client_name']:
                print(f"  Client: {proj['client_name']}")
            if proj['current_version']:
                print(f"  Current version: {proj['current_version']}")
            print()

        print(f"{FOOTER}")

    elif args.action == "show":
        if not args.name:
            print("Error: --name is required")
            sys.exit(1)

        project = db.get_project(args.name)
        if not project:
            print(f"Error: Project '{args.name}' not found")
            sys.exit(1)

        print(f"{project['name']}")
        print(f"  ID: {project['id']}")
        if project['description']:
            print(f"  Description: {project['description']}")
        if project['repo_path']:
            print(f"  Repository: {project['repo_path']}")
        if project['client_name']:
            print(f"  Client: {project['client_name']}")
        if project['client_email']:
            print(f"  Client Email: {project['client_email']}")
        if project['current_version']:
            print(f"  Current Version: {project['current_version']}")
        print(f"  Created: {project['created_at']}")
        print(f"\n{FOOTER}")


def cmd_export(args):
    """Export full changelog as markdown."""
    db = init_db()

    if not args.project:
        print("Error: --project is required")
        sys.exit(1)

    project = db.get_project(args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found")
        sys.exit(1)

    output = db.export_changelog(project['id'])

    if args.output:
        output_file = Path(args.output)
        output_file.write_text(output)
        print(f"Exported to {output_file}")
    else:
        print(output)

    print(f"\n{FOOTER}")


def cmd_search(args):
    """Search changelog entries."""
    db = init_db()

    if not args.query:
        print("Error: --query is required")
        sys.exit(1)

    project = None
    if args.project:
        project = db.get_project(args.project)
        if not project:
            print(f"Error: Project '{args.project}' not found")
            sys.exit(1)

    results = db.search_entries(args.query, project['id'] if project else None)

    if not results:
        print(f"No entries found matching '{args.query}'")
        print(f"\n{FOOTER}")
        return

    print(f"Found {len(results)} entries matching '{args.query}':\n")
    for entry in results:
        proj = db.get_project_by_id(entry['project_id'])
        print(f"• [{entry['change_type']}] {entry['description']}")
        print(f"  Project: {proj['name']}")
        if entry['version']:
            print(f"  Version: {entry['version']}")
        print()

    print(f"{FOOTER}")


def cmd_stats(args):
    """Show statistics."""
    db = init_db()

    projects = db.list_projects()
    if not projects:
        print("No projects found")
        print(f"\n{FOOTER}")
        return

    print("Statistics\n")

    total_entries = 0
    total_releases = 0

    for proj in projects:
        entries = db.list_entries(project_id=proj['id'])
        releases = db.list_releases(project_id=proj['id'])

        total_entries += len(entries)
        total_releases += len(releases)

        print(f"{proj['name']}")
        print(f"  Entries: {len(entries)}")
        print(f"  Releases: {len(releases)}")
        if proj['current_version']:
            print(f"  Latest version: {proj['current_version']}")
        print()

    print(f"Total: {total_entries} entries, {total_releases} releases")
    print(f"\n{FOOTER}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Nex Changelog - Changelog & Version Notes Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  nex-changelog add --project "Ribbens Airco Website" --type added --description "Contact form with email notification" --audience client
  nex-changelog git /path/to/repo --project "My App"
  nex-changelog release --project "My App" --version 1.3.0 --summary "Bug fixes and improvements"
  nex-changelog email --project "My App" --version 1.3.0
  nex-changelog show --project "My App" --format keepachangelog
  nex-changelog project add --name "New Project" --client "Client Name" --description "Project description"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a changelog entry')
    add_parser.add_argument('--project', required=True, help='Project name')
    add_parser.add_argument('--type', choices=CHANGE_TYPES.keys(), help='Change type')
    add_parser.add_argument('--description', required=True, help='Entry description')
    add_parser.add_argument('--audience', choices=AUDIENCE_TYPES.keys(), help='Target audience')
    add_parser.add_argument('--details', help='Additional details')
    add_parser.add_argument('--author', help='Author name')
    add_parser.add_argument('--commit-hash', help='Git commit hash')
    add_parser.add_argument('--breaking', action='store_true', help='Mark as breaking change')
    add_parser.add_argument('--version', help='Version number')
    add_parser.set_defaults(func=cmd_add)

    # Git command
    git_parser = subparsers.add_parser('git', help='Import from git repository')
    git_parser.add_argument('repo', help='Repository path')
    git_parser.add_argument('--project', help='Project name (defaults to repo name)')
    git_parser.add_argument('--since', help='Import commits since tag (e.g., v1.2.0)')
    git_parser.add_argument('--version', help='Assign version to imported entries')
    git_parser.add_argument('--description', help='Project description')
    git_parser.set_defaults(func=cmd_git)

    # Release command
    release_parser = subparsers.add_parser('release', help='Create a release')
    release_parser.add_argument('--project', required=True, help='Project name')
    release_parser.add_argument('--version', required=True, help='Version number')
    release_parser.add_argument('--summary', help='Release summary')
    release_parser.add_argument('--client-notes', help='Notes for client')
    release_parser.add_argument('--internal-notes', help='Internal notes')
    release_parser.set_defaults(func=cmd_release)

    # Show command
    show_parser = subparsers.add_parser('show', help='Show changelog')
    show_parser.add_argument('--project', required=True, help='Project name')
    show_parser.add_argument('--version', help='Filter by version')
    show_parser.add_argument('--type', help='Filter by change type')
    show_parser.add_argument('--audience', help='Filter by audience')
    show_parser.add_argument('--format', choices=['keepachangelog', 'simple', 'table', 'json'],
                            default='keepachangelog', help='Output format')
    show_parser.set_defaults(func=cmd_show)

    # List command
    list_parser = subparsers.add_parser('list', help='List entries')
    list_parser.add_argument('--project', help='Filter by project')
    list_parser.add_argument('--version', help='Filter by version')
    list_parser.add_argument('--type', help='Filter by change type')
    list_parser.add_argument('--audience', help='Filter by audience')
    list_parser.set_defaults(func=cmd_list)

    # Unreleased command
    unreleased_parser = subparsers.add_parser('unreleased', help='Show unreleased entries')
    unreleased_parser.add_argument('--project', required=True, help='Project name')
    unreleased_parser.set_defaults(func=cmd_unreleased)

    # Email command
    email_parser = subparsers.add_parser('email', help='Generate client email')
    email_parser.add_argument('--project', required=True, help='Project name')
    email_parser.add_argument('--version', required=True, help='Version number')
    email_parser.add_argument('--client', help='Client name (overrides project default)')
    email_parser.set_defaults(func=cmd_email)

    # Telegram command
    telegram_parser = subparsers.add_parser('telegram', help='Generate Telegram message')
    telegram_parser.add_argument('--project', required=True, help='Project name')
    telegram_parser.add_argument('--version', required=True, help='Version number')
    telegram_parser.set_defaults(func=cmd_telegram)

    # Project command
    project_parser = subparsers.add_parser('project', help='Manage projects')
    project_parser.add_argument('action', choices=['add', 'list', 'show'], help='Action')
    project_parser.add_argument('--name', help='Project name')
    project_parser.add_argument('--repo-path', help='Repository path')
    project_parser.add_argument('--client-name', help='Client name')
    project_parser.add_argument('--client-email', help='Client email')
    project_parser.add_argument('--description', help='Project description')
    project_parser.set_defaults(func=cmd_project)

    # Export command
    export_parser = subparsers.add_parser('export', help='Export changelog')
    export_parser.add_argument('--project', required=True, help='Project name')
    export_parser.add_argument('--output', help='Output file path')
    export_parser.set_defaults(func=cmd_export)

    # Search command
    search_parser = subparsers.add_parser('search', help='Search entries')
    search_parser.add_argument('--query', required=True, help='Search query')
    search_parser.add_argument('--project', help='Filter by project')
    search_parser.set_defaults(func=cmd_search)

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
