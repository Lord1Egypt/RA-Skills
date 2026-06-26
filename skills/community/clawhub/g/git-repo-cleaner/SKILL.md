---
name: git-repo-cleaner
description: Audit and clean up Git repositories. Find stale/merged branches, large files in history, orphaned tags, repo bloat, and generate cleanup scripts. Use when asked to clean up a git repo, find stale branches, detect large files in git history, audit repo health, find merged branches to delete, reduce repo size, or perform git maintenance. Triggers on "clean up repo", "stale branches", "large files in git", "repo bloat", "merged branches", "git cleanup", "repo maintenance", "git audit".
---

# Git Repo Cleaner

Audit Git repositories for bloat, stale branches, and maintenance issues. Generate safe cleanup scripts.

## Quick Audit

```bash
python3 scripts/audit_repo.py /path/to/repo
```

## Specific Checks

```bash
# Stale branches only
python3 scripts/audit_repo.py /path/to/repo --check branches

# Large files in history
python3 scripts/audit_repo.py /path/to/repo --check large-files

# Full audit
python3 scripts/audit_repo.py /path/to/repo --check all
```

## Output Formats

```bash
python3 scripts/audit_repo.py /path/to/repo --format text|json|markdown
```

## Checks Performed

### 1. Stale Branches
- Branches not updated in >30 days (configurable with `--stale-days`)
- Branches already merged into main/master
- Branches with no unique commits
- Remote tracking branches with deleted remotes

### 2. Large Files
- Files >1MB in current tree (configurable with `--min-size`)
- Large blobs in git history (top 20)
- Binary files that shouldn't be tracked

### 3. Repo Stats
- Total repo size (.git directory)
- Pack file stats
- Object count and size
- Unreachable objects

### 4. Maintenance
- Missing .gitignore patterns (node_modules, __pycache__, .env, etc.)
- Unoptimized packfiles
- Stale reflog entries

## Cleanup Script Generation

Use `--fix` to generate (not execute) cleanup scripts:

```bash
python3 scripts/audit_repo.py /path/to/repo --fix
# Outputs cleanup.sh with safe delete commands
```

The generated script uses `git branch -d` (safe delete, refuses if not merged) by default.
Use `--force-delete` to generate `git branch -D` commands instead.

## Workflow

1. Run audit on repo
2. Review findings
3. Generate cleanup script if needed
4. Review script before executing
5. Execute cleanup
