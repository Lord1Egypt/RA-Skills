#!/usr/bin/env python3
"""
Git Tool - Useful Git commands wrapper
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_git(args, capture=True):
    """Run git command."""
    cmd = ['git'] + args
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True)
        if result.returncode == 0:
            if capture:
                print(result.stdout)
            return 0
        else:
            print(f"Error: {result.stderr}")
            return result.returncode
    except FileNotFoundError:
        print("Error: git not found. Install git first.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def git_init(path='.'):
    """Initialize repository."""
    return run_git(['init', path])


def git_status():
    """Show status."""
    return run_git(['status'])


def git_branch(list_only=False, name=None):
    """Manage branches."""
    if list_only:
        return run_git(['branch'])
    elif name:
        return run_git(['branch', name])
    else:
        print("Usage: --list or --name BRANCH_NAME")
        return 1


def git_log(limit=10, oneline=False):
    """View commit history."""
    args = ['log']
    if oneline:
        args.append('--oneline')
    args.append(f'-n{limit}')
    return run_git(args)


def git_diff(file=None):
    """Show changes."""
    args = ['diff']
    if file:
        args.append(file)
    return run_git(args)


def git_stash(save_message=None, pop=False, list_stash=False):
    """Stash changes."""
    if list_stash:
        return run_git(['stash', 'list'])
    elif save_message:
        return run_git(['stash', 'save', save_message])
    elif pop:
        return run_git(['stash', 'pop'])
    else:
        print("Usage: --save 'message' or --pop or --list")
        return 1


def git_commit(message):
    """Create commit."""
    return run_git(['commit', '-m', message])


def git_add(files=None):
    """Stage files."""
    args = ['add']
    if files:
        args.extend(files)
    else:
        args.append('.')
    return run_git(args)


def git_push(remote='origin', branch='main'):
    """Push to remote."""
    return run_git(['push', remote, branch])


def git_pull(remote='origin', branch='main'):
    """Pull from remote."""
    return run_git(['pull', remote, branch])


def main():
    parser = argparse.ArgumentParser(description='Git Tool')
    parser.add_argument('command', help='Git command')
    
    # Options
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--files', nargs='*', help='Files to add/commit')
    parser.add_argument('--remote', default='origin', help='Remote name')
    parser.add_argument('--branch', default='main', help='Branch name')
    parser.add_argument('--limit', type=int, default=10, help='Log limit')
    parser.add_argument('--oneline', action='store_true', help='One line log')
    
    args = parser.parse_args()
    
    cmd = args.command
    
    if cmd == 'init':
        return git_init()
    elif cmd == 'status':
        return git_status()
    elif cmd == 'branch':
        return git_branch(list_only=True)
    elif cmd == 'log':
        return git_log(args.limit, args.oneline)
    elif cmd == 'diff':
        return git_diff()
    elif cmd == 'stash':
        return git_stash(save_message=args.message)
    elif cmd == 'stash-list':
        return git_stash(list_stash=True)
    elif cmd == 'stash-pop':
        return git_stash(pop=True)
    elif cmd == 'add':
        return git_add(args.files)
    elif cmd == 'commit':
        if not args.message:
            print("Error: --message required for commit")
            return 1
        git_add(args.files)
        return git_commit(args.message)
    elif cmd == 'push':
        return git_push(args.remote, args.branch)
    elif cmd == 'pull':
        return git_pull(args.remote, args.branch)
    else:
        print(f"Unknown command: {cmd}")
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
