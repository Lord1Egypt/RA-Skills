#!/usr/bin/env python3
"""
KB Framework CLI - Command Discovery und Execution

Usage:
    python3 -m kb <command> [args]
    cd ~/projects/kb-framework && python3 -m kb <command> [args]
    
Commands:
    sync      Sync ChromaDB with SQLite
    audit     Run full KB audit
    ghost     Find orphaned entries
    warmup    Preload ChromaDB model
    llm       LLM-Integration (Essenzen, Reports, Watcher, Scheduler)
    backup    Backup KB data (library-only or full)

Architecture:
    kb/
    ├── base/           # Core components
    │   ├── config.py   # KBConfig singleton
    │   ├── logger.py   # KBLogger singleton
    │   ├── db.py       # KBConnection context manager
    │   └── command.py  # BaseCommand abstract class
    ├── commands/        # Command implementations
    │   ├── sync.py     # SyncCommand
    │   ├── audit.py    # AuditCommand
    │   ├── ghost.py    # GhostCommand
    │   ├── warmup.py   # WarmupCommand
    │   └── llm.py      # LLMCommand
    └── __main__.py     # CLI entrypoint
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
KB_DIR = Path(__file__).resolve().parent  # This is kb/ directory
PARENT_DIR = KB_DIR.parent  # This is kb-framework/ directory

# Ensure our packages are on the path
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

# Setup paths for KB installation — delegate to paths.py
try:
    from kb.framework.paths import get_default_base_path
    _default_path = str(get_default_base_path())
except Exception:
    _default_path = str(Path.home() / ".openclaw" / "kb")
KB_BASE_PATH = os.getenv("KB_BASE_PATH", _default_path)
os.environ.setdefault("KB_BASE_PATH", KB_BASE_PATH)


def setup_environment():
    """Setup environment variables and paths."""
    # Ensure KB directories exist
    for subdir in ['knowledge.db', 'chroma_db']:
        path = Path(KB_BASE_PATH) / subdir
        if not path.exists() and subdir != 'knowledge.db':  # DB might not exist yet
            pass  # Let individual commands handle directory creation


def create_parser() -> argparse.ArgumentParser:
    """Build argument parser with all commands."""
    parser = argparse.ArgumentParser(
        prog='kb',
        description='KB Framework - Knowledge Base Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kb sync --stats          Show sync statistics
  kb sync --dry-run        Preview sync without changes  
  kb audit -v              Run audit with verbose output
  kb ghost --scan-dirs ~/docs,~/notes
  kb warmup                Preload embedding model
  kb llm status            LLM-Status anzeigen
  kb llm generate essence "ML Basics"
  kb llm generate report daily
  kb llm watch status
  kb llm scheduler list
  kb llm list essences
  kb llm config

Environment Variables:
  KB_BASE_PATH       Base directory for KB (default: ~/.openclaw/kb)
  KB_DB_PATH         SQLite database path
  KB_CHROMA_PATH     ChromaDB persistence path
  KB_LIBRARY_PATH    Document library path
  KB_WORKSPACE_PATH  Workspace path
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.1.0'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress informational output'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command', 
        help='Commands',
        title='Commands'
    )
    
    return parser, subparsers


def register_command_arguments(parser, cmd_cls):
    """Register a command's arguments with the subparser."""
    subparser = parser.add_parser(
        cmd_cls.name,
        help=cmd_cls.help,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    cmd = cmd_cls()
    cmd.add_arguments(subparser)
    return cmd


def main() -> int:
    """Main entrypoint."""
    # Setup logging first
    import logging
    from kb.base.logger import KBLogger
    
    # Parse known args first to check for debug
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument('--debug', action='store_true')
    pre_parser.add_argument('--quiet', '-q', action='store_true')
    pre_args, _ = pre_parser.parse_known_args()
    
    # Setup logging
    log_level = logging.DEBUG if pre_args.debug else logging.INFO
    if pre_args.quiet:
        log_level = logging.WARNING
    
    KBLogger.setup_logging(level=log_level)
    
    # Build full parser
    parser, subparsers = create_parser()
    
    # Import and register commands
    from kb.commands import get_commands, _ensure_commands_loaded
    
    _ensure_commands_loaded()
    commands = get_commands()
    
    # Register each command
    command_instances = {}
    for name, cmd_cls in sorted(commands.items()):
        cmd = register_command_arguments(subparsers, cmd_cls)
        command_instances[name] = cmd
    
    # Parse all arguments
    args = parser.parse_args()
    
    # Show help if no command specified
    if not args.command:
        parser.print_help()
        print("\nCommands:")
        for name, cmd_cls in sorted(commands.items()):
            print(f"  {name:12} {cmd_cls.help}")
        return 0
    
    # Execute command
    cmd = command_instances.get(args.command)
    if not cmd:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1
    
    return cmd.run(args)


if __name__ == '__main__':
    sys.exit(main())
