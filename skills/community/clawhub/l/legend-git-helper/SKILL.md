---
name: git-helper
description: "Git workflow automation for commits, pushes, rebases, status checks, and branch operations. Use when working with git repositories for: (1) Checking status, (2) Staging files, (3) Creating commits with conventional messages, (4) Pushing/pulling, (5) Rebasing/merging, (6) Viewing logs/diffs, or (7) Managing branches."
---

# Git Helper

Handles all git operations through safe, consistent workflows.

## Core Workflows

### Status Check
Before any git operation, run `git status` to understand repository state.

### Staging
- `git add <file>` - Stage specific files
- `git add -A` - Stage all changes
- `git add -p` - Interactive staging (review hunks)

### Committing
Use Conventional Commits format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Scope:** Optional, usually the component or area affected

**Description:** Imperative present tense ("add feature" not "added feature")

### Push/Pull
- `git push` - Push to remote (default: current branch)
- `git pull --rebase` - Fetch and rebase (preferred default)
- `git pull` - Fetch and merge (when merge history needed)

### Rebasing
- `git rebase -i HEAD~N` - Interactive rebase last N commits
- Always confirm branch state before rebasing
- Never rebase shared/public branches without explicit permission

### Log/Diff
- `git log --oneline -N` - View last N commits
- `git diff` - Unstaged changes
- `git diff --staged` - Staged changes
- `git diff HEAD~N` - Changes over last N commits

## Safety Rules

1. **Never force push** without explicit user permission
2. **Always check status** before any operation
3. **Confirm destructive actions** (rebase, reset, hard, force push)
4. **Stay within workspace boundaries** - respect user's file access rules
5. **Pull before push** when working with shared branches

## When to Read references/workflows.md

Load this reference file when:
- User needs detailed Conventional Commits specification
- Complex rebase/merge scenarios require guidance
- Branch strategy consultation needed
- Conflict resolution guidance required