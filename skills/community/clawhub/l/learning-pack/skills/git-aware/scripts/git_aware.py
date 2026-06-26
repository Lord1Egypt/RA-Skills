#!/usr/bin/env python3
"""Git-aware operations with smart commits."""

import subprocess
import sys
from pathlib import Path

def git(*args):
    """Run git command and return output."""
    result = subprocess.run(['git'] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Git error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()

def status():
    """Show git status with context."""
    branch = git('rev-parse', '--abbrev-ref', 'HEAD')
    print(f"📦 Branch: {branch}")
    
    # Check uncommitted changes
    changes = git('status', '--porcelain')
    if changes:
        print(f"📝 Uncommitted changes:\n{changes}")
    else:
        print("✅ Working tree clean")
    
    # Check remote status
    remote = git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}', stderr=subprocess.DEVNULL)
    if remote:
        ahead_behind = git('rev-list', '--left-right', '--count', f'{remote}...HEAD')
        print(f"🌐 Remote: {ahead_behind}")

def commit(message, commit_type='feat'):
    """Auto-commit with smart message."""
    # Stage all changes
    git('add', '-A')
    
    # Generate commit message
    full_message = f"{commit_type}: {message}"
    
    # Commit
    git('commit', '-m', full_message)
    print(f"✅ Committed: {full_message}")

def create_branch(task_id):
    """Create feature branch from task ID."""
    branch_name = f"feature/{task_id}"
    git('checkout', '-b', branch_name)
    print(f"🌿 Created branch: {branch_name}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: git_aware.py <command> [args]")
        print("Commands: status, commit, branch create")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'status':
        status()
    elif cmd == 'commit':
        msg = sys.argv[2] if len(sys.argv) > 2 else "Update"
        commit_type = 'feat'
        if '--type' in sys.argv:
            idx = sys.argv.index('--type')
            commit_type = sys.argv[idx + 1]
            msg = sys.argv[idx + 2] if idx + 2 < len(sys.argv) else msg
        commit(msg, commit_type)
    elif cmd == 'branch' and len(sys.argv) > 2:
        if sys.argv[2] == 'create':
            create_branch(sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
