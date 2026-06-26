---
name: git-tool
description: Useful Git commands for repository management. Use when user needs to manage git repositories, create branches, view history, stash changes, or automate git workflows.
---

# Git Tool

Useful Git commands for repository management.

## Quick Start

```bash
# Initialize repo
python scripts/git.py init

# View status
python scripts/git.py status
```

## Usage

```bash
python scripts/git.py COMMAND [OPTIONS]

Commands:
  init          Initialize repository
  status        Show working tree status
  branch        List branches
  commit        Create commit
  log           View commit history
  stash         Stash changes
  diff          Show changes
```

## Examples

```bash
# Initialize
python scripts/git.py init

# Status
python scripts/git.py status

# View log
python scripts/git.py log --oneline

# Create branch
python scripts/git.py branch new-feature

# Stash changes
python scripts/git.py stash save "work in progress"

# Commit
python scripts/git.py commit -m "Update files"
```

## Features

- Repository initialization
- Branch management
- Commit creation
- History viewing
- Stash operations
- Diff viewing
