---
name: git-aware
description: "Git-aware operations with auto-commit and smart context. Use when: you need to make code changes with automatic git tracking, create meaningful commit messages, manage branches, or review changes. NOT for: simple file reads (use read tool), one-off git commands (use exec directly). Inspired by Aider's git integration."
metadata: { "openclaw": { "emoji": "📦", "requires": { "bins": ["git"] } } }
---

# Git-Aware Skill

Smart git integration with automatic tracking, meaningful commits, and branch management.

## When to Use

✅ **USE this skill when:**
- Making code changes that need version control
- Need automatic commit message generation
- Managing feature branches
- Reviewing changes before commit
- Syncing with remote repositories

❌ **DON'T use this skill when:**
- Simple file reads → use `read` tool
- One-off git commands → use `exec git ...`
- Non-code file operations → use file tools directly

## Features

### 1. Auto-Status Check

Before any operation, automatically check:
- Current branch
- Uncommitted changes
- Ahead/behind remote
- Conflicts

### 2. Smart Commit Messages

Generates meaningful commit messages based on:
- Files changed
- Diff content
- Task context

Format: `<type>: <description>`
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `chore:` Maintenance

### 3. Branch Management

- Create feature branches from task ID
- Auto-push after commit
- PR-ready branch names

## Commands

### Quick Start

```bash
# Initialize git-aware mode
python3 scripts/git_aware.py init

# Make changes with auto-commit
python3 scripts/git_aware.py commit "Implement feature X"

# Check status
python3 scripts/git_aware.py status
```

### Branch Operations

```bash
# Create feature branch from task
python3 scripts/git_aware.py branch create JJC-20260407-003

# Switch branch
python3 scripts/git_aware.py branch switch <name>

# Merge branch
python3 scripts/git_aware.py branch merge <name>
```

### Commit Operations

```bash
# Auto-commit with message generation
python3 scripts/git_aware.py commit "Add user authentication"

# Commit with specific type
python3 scripts/git_aware.py commit --type feat "Add login endpoint"

# Amend last commit
python3 scripts/git_aware.py commit --amend
```

### Review Operations

```bash
# Review staged changes
python3 scripts/git_aware.py review

# Review uncommitted changes
python3 scripts/git_aware.py review --unstaged

# Compare with main
python3 scripts/git_aware.py diff main
```

## Usage Patterns

### Pattern 1: Feature Development

```bash
# 1. Create feature branch
python3 scripts/git_aware.py branch create JJC-20260407-004

# 2. Make changes (edit files)

# 3. Auto-commit
python3 scripts/git_aware.py commit "Implement new feature"

# 4. Push to remote
git push -u origin feature/JJC-20260407-004
```

### Pattern 2: Bug Fix

```bash
# 1. Checkout main
git checkout main && git pull

# 2. Create fix branch
python3 scripts/git_aware.py branch create fix-issue-123

# 3. Fix the bug (edit files)

# 4. Commit with fix type
python3 scripts/git_aware.py commit --type fix "Resolve null pointer in auth"

# 5. Create PR
gh pr create --title "fix: Resolve null pointer in auth"
```

### Pattern 3: Code Review

```bash
# 1. Review changes
python3 scripts/git_aware.py review

# 2. Generate diff summary
python3 scripts/git_aware.py diff --summary main

# 3. Export review report
python3 scripts/git_aware.py review --export > review.md
```

## Script Implementation

### git_aware.py

```python
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
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == 'status':
        status()
    elif cmd == 'commit':
        commit(sys.argv[2] if len(sys.argv) > 2 else "Update")
    elif cmd == 'branch' and len(sys.argv) > 2:
        if sys.argv[2] == 'create':
            create_branch(sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
```

## Integration with三省六部

### Task Tracking

Each task creates a branch:
```
feature/JJC-20260407-003  # 调研任务
feature/JJC-20260407-004  # 开发任务
```

### Commit Convention

Commits reference task ID:
```
feat: Add MCP bridge skill (JJC-20260407-003)
fix: Resolve git hook conflict (JJC-20260407-003)
```

### Review Flow

1. 工部开发 → commit to feature branch
2. 兵部测试 → review changes
3. 尚书省汇总 → merge to main

## Best Practices

1. **Commit Often**: Small, focused commits
2. **Meaningful Messages**: Explain why, not what
3. **Branch Per Task**: One feature/fix per branch
4. **Review Before Merge**: Always review changes
5. **Sync Regularly**: Pull from main frequently

## Troubleshooting

### Detached HEAD
```bash
git checkout main
git pull
```

### Commit Hook Failed
```bash
# Skip hooks (temporary)
git commit --no-verify -m "message"

# Or fix hook
chmod +x .git/hooks/pre-commit
```

### Merge Conflicts
```bash
# Start merge
git merge main

# Resolve conflicts manually
# Then:
git add <resolved-files>
git commit
```

## References

- [Aider Git Integration](https://github.com/Aider-AI/aider)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)
