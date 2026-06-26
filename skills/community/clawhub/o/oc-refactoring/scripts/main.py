#!/usr/bin/env python3
"""
Refactoring - Main Entry Point

Commands:
  rename              - Rename symbols
  suggest             - Get refactoring suggestions
  undo                - Undo last refactoring
  list-backups        - List available backups
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_rename(args):
    """Run rename command"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from rename import PythonRenameEngine

    engine = PythonRenameEngine(args.root)
    plan = engine.preview_rename(args.old_name, args.new_name, args.type)

    print(f"\n🔍 Rename Plan: {args.old_name} → {args.new_name}")
    print(f"{'='*60}")
    print(f"Found {plan.total_changes} occurrence(s) in {len(plan.affected_files)} file(s)")
    print()

    # Group by file
    by_file = {}
    for occ in plan.occurrences:
        if occ.file not in by_file:
            by_file[occ.file] = []
        by_file[occ.file].append(occ)

    for file_path, occurrences in by_file.items():
        print(f"📄 {file_path}")
        for occ in occurrences:
            print(f"   Line {occ.line}:{occ.column} ({occ.context})")
            print(f"   - {occ.original_line.strip()[:60]}")
        print()

    if args.dry_run:
        print("\n⏸️  Dry run mode - no changes made")
        print("   Remove --dry-run to execute")
    else:
        print("\n⚡ Executing rename...")
        result = engine.execute_rename(plan, create_backup=not args.no_backup)

        if result['success']:
            print(f"✅ Success! Made {result['changes']} change(s)")
            print(f"   Modified {len(result['files_modified'])} file(s)")
            if result.get('backup_id'):
                print(f"   Backup: {result['backup_id']}")
        else:
            print(f"❌ Error: {result['message']}")
            sys.exit(1)


def run_suggest(args):
    """Run suggest command"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from suggest import SuggestionEngine

    engine = SuggestionEngine(args.root)
    suggestions = engine.analyze(args.path or args.root)

    print(f"\n🔍 Refactoring Suggestions")
    print(f"{'='*60}")
    print(f"Analyzed: {args.path or args.root}")
    print(f"Found {len(suggestions)} suggestion(s)")
    print()

    for suggestion in suggestions:
        severity_emoji = "🔴" if suggestion['severity'] == 'error' else ("⚠️" if suggestion['severity'] == 'warning' else "ℹ️")
        print(f"{severity_emoji}  {suggestion['type']}: {suggestion['message']}")
        print(f"   📍 {suggestion['location']}")
        if suggestion.get('suggestion'):
            print(f"   💡 {suggestion['suggestion']}")
        print()


def run_undo(args):
    """Undo last refactoring"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from rename import PythonRenameEngine

    engine = PythonRenameEngine(args.root)

    if args.backup_id:
        result = engine.undo(args.backup_id)
    else:
        # List backups first
        backups = engine.list_backups()
        if not backups:
            print("❌ No backups found")
            sys.exit(1)

        print("📦 Available backups:")
        for i, backup in enumerate(backups[:5], 1):
            print(f"   {i}. {backup['id']} ({backup['files']} files)")

        if args.list:
            return

        # Undo most recent
        result = engine.undo()

    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {result['message']}")
        sys.exit(1)


def run_list_backups(args):
    """List available backups"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from rename import PythonRenameEngine

    engine = PythonRenameEngine(args.root)
    backups = engine.list_backups()

    if not backups:
        print("📦 No backups found")
        return

    print("📦 Available backups:")
    print(f"{'='*60}")
    for backup in backups:
        print(f"\n   ID: {backup['id']}")
        print(f"   Time: {backup['timestamp']}")
        print(f"   Files: {backup['files']}")


def main():
    parser = argparse.ArgumentParser(
        description='Refactoring - Automated code transformations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Rename a function
  python3 main.py rename -o "old_func" -n "new_func" src/

  # Preview rename
  python3 main.py rename -o "old_func" -n "new_func" src/ --dry-run

  # Get refactoring suggestions
  python3 main.py suggest src/

  # Undo last refactoring
  python3 main.py undo

  # List backups
  python3 main.py list-backups
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # rename command
    rename_parser = subparsers.add_parser('rename', help='Rename symbols')
    rename_parser.add_argument('root', nargs='?', default='.', help='Project root')
    rename_parser.add_argument('--old-name', '-o', required=True, help='Old symbol name')
    rename_parser.add_argument('--new-name', '-n', required=True, help='New symbol name')
    rename_parser.add_argument('--type', '-t', choices=['function', 'class', 'variable', 'method'],
                               help='Symbol type')
    rename_parser.add_argument('--dry-run', '-d', action='store_true', help='Preview only')
    rename_parser.add_argument('--no-backup', action='store_true', help='Skip backup')
    rename_parser.set_defaults(func=run_rename)

    # suggest command
    suggest_parser = subparsers.add_parser('suggest', help='Get refactoring suggestions')
    suggest_parser.add_argument('path', nargs='?', help='Path to analyze')
    suggest_parser.add_argument('--root', '-r', default='.', help='Project root')
    suggest_parser.set_defaults(func=run_suggest)

    # undo command
    undo_parser = subparsers.add_parser('undo', help='Undo refactoring')
    undo_parser.add_argument('root', nargs='?', default='.', help='Project root')
    undo_parser.add_argument('--backup-id', '-b', help='Specific backup ID')
    undo_parser.add_argument('--list', '-l', action='store_true', help='List backups only')
    undo_parser.set_defaults(func=run_undo)

    # list-backups command
    list_parser = subparsers.add_parser('list-backups', help='List available backups')
    list_parser.add_argument('root', nargs='?', default='.', help='Project root')
    list_parser.set_defaults(func=run_list_backups)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
