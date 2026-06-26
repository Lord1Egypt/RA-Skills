#!/usr/bin/env python3
"""
Repo JSON Generator - Git Repository to Structured JSON Converter

Fetches code from Git repositories and generates structured JSON instructions
for accurate code updates via AI agents and automation tools.

## Features
- Cross-platform temp directory support (Windows/macOS/Linux)
- Circuit breaker mechanism for resilient operations
- Streaming/chunked output for large repositories
- Automatic cleanup of temporary files
- Sensitive information protection (tokens, credentials)

All directories are automatically removed after script completion.

Usage:
    python3 generator.py sync --repo URL --commit COMMIT [options]
    python3 generator.py info --repo URL [--commit COMMIT] [options]
    
Note:
    App ID is automatically extracted from repository URL if not provided.
    Example: https://github.com/xiaoanso/app-9wublrxntfr5.git -> app-9wublrxntfr5
"""

import argparse
import json
import os
import sys
import tempfile

# Import modular components
from git.repository import RepoJSONGenerator
from processors.instruction_gen import InstructionGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI commands"""
    parser = argparse.ArgumentParser(
        prog='generator.py',
        description='Repo JSON Generator - Convert Git repository code to structured JSON instructions for AI agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage:
  python3 scripts/generator.py sync --repo URL --branch BRANCH [--commit COMMIT] [options]
  python3 scripts/generator.py info --repo URL --branch BRANCH [--commit COMMIT] [options]
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # sync command
    sync_parser = subparsers.add_parser(
        'sync',
        help='Generate JSON instructions for code synchronization'
    )
    sync_parser.add_argument('--repo', required=True, help='Git repository URL')
    sync_parser.add_argument('--branch', required=True, help='Branch name (required)')
    sync_parser.add_argument('--commit', help='Specific commit hash (defaults to latest on branch)')
    sync_parser.add_argument('--filter', help='Include only files matching patterns (e.g., "*.py,*.js")')
    sync_parser.add_argument('--exclude', help='Exclude files matching patterns (e.g., "*.md,test/*")')
    sync_parser.add_argument('--max-files', type=int, default=50, help='Maximum number of files to process (default: 50)')
    sync_parser.add_argument('--output', help='Save output to file')
    sync_parser.add_argument('--no-instructions', action='store_true', help='Output pure JSON without formatted instructions')
    sync_parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    # info command
    info_parser = subparsers.add_parser(
        'info',
        help='Get commit information and changed files with contents'
    )
    info_parser.add_argument('--repo', required=True, help='Git repository URL')
    info_parser.add_argument('--branch', required=True, help='Branch name (required)')
    info_parser.add_argument('--commit', help='Specific commit hash (defaults to latest on branch)')
    info_parser.add_argument('--filter', help='Include only files matching patterns (e.g., "*.ts,*.tsx")')
    info_parser.add_argument('--exclude', help='Exclude files matching patterns (e.g., "*.md,docs/*")')
    info_parser.add_argument('--output', help='Save output to file')
    info_parser.add_argument('--no-instructions', action='store_true', help='Save pure JSON to file')
    info_parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    return parser


def cmd_sync(args, generator: RepoJSONGenerator):
    """Handle sync command"""
    try:
        branch = args.branch
        
        # If commit not specified, get latest commit
        commit = args.commit
        if not commit:
            print(f"   ℹ️  No commit specified, using latest from branch '{branch}'")
            # Clone to get latest commit
            with tempfile.TemporaryDirectory(prefix='github-sync-latest-') as temp_dir:
                generator.clone_repo(args.repo, temp_dir, branch=branch)
                # Get HEAD commit
                import subprocess
                result = subprocess.run(
                    ['git', '-C', temp_dir, 'rev-parse', 'HEAD'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    commit = result.stdout.strip()
                else:
                    raise Exception("Failed to get latest commit")
        
        print(f"   📦 Repository: {args.repo}")
        print(f"   📌 Commit: {commit[:8]}")
        print(f"   🌿 Branch: {branch}")
        if args.filter:
            print(f"   ✅ Filter: {args.filter}")
        if args.exclude:
            print(f"   ⛔ Exclude: {args.exclude}")
        print()
        
        # Get full changes
        result = generator.get_commit_full_changes(
            repo_url=args.repo,
            commit=commit,
            branch=branch,
            file_filter=args.filter,
            exclude_filter=args.exclude,
            command_type='sync'
        )
        
        # Display summary
        summary = result.get('summary', {})
        print(f"📊 Summary:")
        print(f"  Files Changed: {summary.get('files_changed', 0)}")
        print(f"  Total Files: {summary.get('total_files', 0)}")
        print()
        
        print(f"📁 Changed Files ({summary.get('files_changed', 0)}):")
        for file_info in summary.get('files', []):
            print(f"  📝 {file_info['path']} ({file_info.get('size', 0)} chars)")
        
        # Output result
        instruction_gen = InstructionGenerator()
        instruction_gen.output_result(result, args.output, args.no_instructions)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def cmd_info(args, generator: RepoJSONGenerator):
    """Handle info command"""
    try:
        branch = args.branch
        
        # If commit not specified, get latest commit
        commit = args.commit
        if not commit:
            print(f"   ℹ️  No commit specified, using latest from branch '{branch}'")
            # Clone to get latest commit
            with tempfile.TemporaryDirectory(prefix='github-info-latest-') as temp_dir:
                generator.clone_repo(args.repo, temp_dir, branch=branch)
                # Get HEAD commit
                import subprocess
                result = subprocess.run(
                    ['git', '-C', temp_dir, 'rev-parse', 'HEAD'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    commit = result.stdout.strip()
                else:
                    raise Exception("Failed to get latest commit")
        
        print(f"   📦 Repository: {args.repo}")
        print(f"   📌 Commit: {commit[:8]}")
        print(f"   🌿 Branch: {branch}")
        if args.filter:
            print(f"   ✅ Filter: {args.filter}")
        if args.exclude:
            print(f"   ⛔ Exclude: {args.exclude}")
        print()
        
        # Get diff info (statistics only, not full content)
        result = generator.get_commit_diff_info(
            repo_url=args.repo,
            commit=commit,
            branch=branch,
            file_filter=args.filter,
            exclude_filter=args.exclude
        )
        
        # Display summary
        summary = result.get('summary', {})
        print(f"📊 Summary:")
        print(f"  Files Changed: {summary.get('files_changed', 0)}")
        print(f"  Total Additions: +{summary.get('total_additions', 0)}")
        print(f"  Total Deletions: -{summary.get('total_deletions', 0)}")
        print()
        
        print(f"📁 Changed Files ({summary.get('files_changed', 0)}):")
        for file_info in summary.get('files', []):
            status_icon = "🆕" if file_info['status'] == 'added' else "📝"
            status_label = "Added" if file_info['status'] == 'added' else "Modified"
            additions = file_info.get('additions', 0)
            deletions = file_info.get('deletions', 0)
            print(f"  {status_icon} {status_label}: {file_info['path']} (+{additions}/-{deletions})")
        
        # Save to file if requested
        if args.output:
            instruction_gen = InstructionGenerator()
            instruction_gen.output_result(result, args.output, args.no_instructions)
            print(f"\n💾 Output saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize generator with token from environment
    token = os.environ.get('GITHUB_TOKEN')
    generator = RepoJSONGenerator(token=token, verbose=args.verbose)
    
    # Route to appropriate command handler
    if args.command == 'sync':
        cmd_sync(args, generator)
    elif args.command == 'info':
        cmd_info(args, generator)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
