#!/usr/bin/env python3
"""
Git Workflow - Main Entry Point
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_suggest_commit(args):
    """Generate commit message suggestion"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from commit_generator import CommitGenerator

    generator = CommitGenerator(args.root)
    result = generator.generate(args.type)

    if 'error' in result:
        print(f"❌ {result['error']}")
        return

    print("\n📝 Suggested commit message:")
    print(f"{'='*60}")
    print(result['full_message'])
    print()
    print(f"Type: {result['type']}")
    print(f"Files: {len(result['files'])}")


def run_pr_description(args):
    """Generate PR description"""
    # Get branch diff summary
    result = subprocess.run(
        ['git', 'log', f'{args.base}..{args.head}', '--oneline'],
        capture_output=True,
        text=True,
        cwd=args.root
    )

    commits = result.stdout.strip().split('\n') if result.stdout else []

    # Get changed files
    result = subprocess.run(
        ['git', 'diff', f'{args.base}...{args.head}', '--name-status'],
        capture_output=True,
        text=True,
        cwd=args.root
    )

    files = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                files.append(parts[1])

    # Generate PR description
    print("\n📝 PR Description")
    print(f"{'='*60}")
    print()
    print("## Summary")
    print("<!-- Describe your changes -->")
    print()
    print("## Changes")
    for commit in commits[:10]:
        if commit:
            print(f"- {commit}")
    if len(commits) > 10:
        print(f"- ... and {len(commits) - 10} more commits")
    print()
    print("## Files Changed")
    for f in files[:20]:
        print(f"- `{f}`")
    if len(files) > 20:
        print(f"- ... and {len(files) - 20} more files")
    print()
    print("## Testing")
    print("- [ ] Unit tests pass")
    print("- [ ] Integration tests pass")
    print("- [ ] Manual testing completed")
    print()
    print("## Related Issues")
    print("Closes #<!-- issue number -->")


def run_branch_strategy(args):
    """Show branch strategy suggestions"""
    # Get current branch
    result = subprocess.run(
        ['git', 'branch', '--show-current'],
        capture_output=True,
        text=True,
        cwd=args.root
    )
    current_branch = result.stdout.strip()

    # Check if behind main
    result = subprocess.run(
        ['git', 'rev-list', '--count', f'HEAD..origin/{args.base}'],
        capture_output=True,
        text=True,
        cwd=args.root
    )
    behind_count = int(result.stdout.strip() or 0)

    print("\n🌿 Branch Strategy")
    print(f"{'='*60}")
    print(f"Current branch: {current_branch}")
    print(f"Base branch: {args.base}")
    print()
    print("Recommended workflow:")
    print("1. Keep feature branch up to date:")
    print(f"   git fetch origin")
    print(f"   git rebase origin/{args.base}")
    print()
    print("2. Before creating PR:")
    print("   git rebase -i origin/main  # Squash if needed")
    print()
    print("3. Merge strategy:")
    print(f"   git checkout {args.base}")
    print(f"   git merge --no-ff {current_branch}")

    if behind_count > 0:
        print()
        print(f"⚠️  Warning: Branch is {behind_count} commits behind {args.base}")


def run_check_branches(args):
    """Check and clean branches"""
    # Get all branches
    result = subprocess.run(
        ['git', 'branch', '-a'],
        capture_output=True,
        text=True,
        cwd=args.root
    )

    branches = [b.strip().strip('* ') for b in result.stdout.strip().split('\n') if b.strip()]

    # Get default branch
    result = subprocess.run(
        ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'],
        capture_output=True,
        text=True,
        cwd=args.root
    )
    default_branch = result.stdout.strip().split('/')[-1] if result.stdout else 'main'

    print("\n🧹 Branch Check")
    print(f"{'='*60}")
    print(f"Total branches: {len(branches)}")
    print(f"Default branch: {default_branch}")
    print()
    print("Local branches:")
    for b in branches:
        if not b.startswith('remotes/'):
            print(f"  - {b}")


def main():
    parser = argparse.ArgumentParser(
        description='Git Workflow Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py suggest-commit
  python3 main.py pr-description --base main --head feature-branch
  python3 main.py branch-strategy
  python3 main.py check-branches
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # suggest-commit command
    commit_parser = subparsers.add_parser('suggest-commit', help='Suggest commit message')
    commit_parser.add_argument('--root', '-r', default='.', help='Project root')
    commit_parser.add_argument('--type', '-t', choices=['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'],
                              help='Commit type')
    commit_parser.set_defaults(func=run_suggest_commit)

    # pr-description command
    pr_parser = subparsers.add_parser('pr-description', help='Generate PR description')
    pr_parser.add_argument('--root', '-r', default='.', help='Project root')
    pr_parser.add_argument('--base', default='main', help='Base branch')
    pr_parser.add_argument('--head', default='HEAD', help='Head branch')
    pr_parser.set_defaults(func=run_pr_description)

    # branch-strategy command
    strategy_parser = subparsers.add_parser('branch-strategy', help='Show branch strategy')
    strategy_parser.add_argument('--root', '-r', default='.', help='Project root')
    strategy_parser.add_argument('--base', default='main', help='Base branch')
    strategy_parser.set_defaults(func=run_branch_strategy)

    # check-branches command
    check_parser = subparsers.add_parser('check-branches', help='Check branches')
    check_parser.add_argument('--root', '-r', default='.', help='Project root')
    check_parser.set_defaults(func=run_check_branches)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
