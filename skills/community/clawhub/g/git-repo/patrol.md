# Repo Patrol

Batch traverse and inspect Git repositories managed by ghq, invoking commit-splitter as needed to organize commits.

## When to Use

- Check git status of multiple repositories at once
- Clean up uncommitted/unpushed changes after work
- Clean up repositories with accumulated stashes
- "repo patrol", "ghq inspect", "check all repos", etc.

## Quick Start

```
/git-repo patrol github.com                  # Inspect all under github.com
/git-repo patrol ~/ghq/github.com/me         # Inspect specific path
/git-repo patrol --discover ~/projects        # Scan directory outside ghq (Discovery Mode)
```

## Instructions

### Step 1: Find Target Repositories

When user specifies a hostname or path, find all git repositories under that path.

```bash
# Search by ghq hostname
find ~/ghq/<host> -name ".git" -type d -o -name ".git" -type f | \
  sed 's|/\.git$||' | sort

# Or filter with ghq list
ghq list | grep <host>
```

**Note**: If `.git` is a file, it may be a worktree. Mark such paths separately.

### Step 2: Collect Status for Each Repository

Collect the following information in parallel for each repository (including fetch):

```bash
# 0. Remote fetch (run first for accurate ahead/behind)
git -C <repo> fetch --all --quiet 2>/dev/null

# 1. Branch info
git -C <repo> branch --show-current
git -C <repo> rev-parse --abbrev-ref @{upstream} 2>/dev/null

# 2. Working directory status
git -C <repo> status --porcelain

# 3. Stash list
git -C <repo> stash list

# 4. Unpushed commits
git -C <repo> log --oneline @{upstream}..HEAD 2>/dev/null
```

**Note**: Fetch is included in per-repository parallel work, so a separate fetch step is unnecessary.

### Step 3: Classify and Summarize Status

Classify collected information into the following categories and output as a table:

| Status | Icon | Meaning |
|--------|------|---------|
| Clean | - | No changes |
| Dirty | M | Modified/deleted/added files exist |
| Stash | S | Stash entries exist |
| Unpushed | U | Commits not pushed to remote |
| No remote | R | Upstream not configured |

```
## Repository Status Summary

| Repository | Branch | Status | Details |
|------------|--------|--------|---------|
| web-app | ci | M U | 3 modified, 12 unpushed |
| mobile-app | develop | U | 3 unpushed |
| admin-panel | main | S U | 2 stash, 4 unpushed |
| backend-api | main | - | clean |
```

### Step 4: Process by Status (user selection)

Ask user via AskUserQuestion how to handle Dirty/Stash/Unpushed repositories.

#### Dirty Repositories

```json
{
  "question": "<repo> has uncommitted changes. How should we handle them?",
  "options": [
    {"label": "Invoke commit-splitter", "description": "Analyze changes and suggest commit splitting"},
    {"label": "Skip", "description": "Handle this repository later"},
    {"label": "git stash", "description": "Temporarily save changes"},
    {"label": "git checkout .", "description": "Discard changes (caution!)"}
  ]
}
```

#### Stash Repositories

```json
{
  "question": "<repo> has N stash entries. How should we handle them?",
  "options": [
    {"label": "stash pop + commit-splitter", "description": "Apply latest stash then analyze commits"},
    {"label": "View stash list", "description": "Only view stash list"},
    {"label": "Skip", "description": "Keep stashes"}
  ]
}
```

#### Unpushed Repositories

```json
{
  "question": "<repo> has N unpushed commits (branch: <branch>). How should we handle them?",
  "options": [
    {"label": "push", "description": "Push to remote"},
    {"label": "Review only", "description": "Only view commit list"},
    {"label": "Skip", "description": "Handle later"}
  ]
}
```

### Step 5: commit-splitter Integration

When invoking commit-splitter, pass the repository path:

```
/commit-splitter <repo-path>
```

Receive commit-splitter results and confirm with user whether to execute commits.

### Step 6: Completion

Output final summary after all repositories are processed and finish.

## Processing Order Guide

For repositories with multiple overlapping statuses (e.g., Dirty + Stash + Unpushed), process in this order:

1. **Stash first**: stash pop → transitions to dirty state
2. **Handle Dirty**: commit-splitter → create commits
3. **Check Unpushed**: Decide whether to push including new commits

## Parallel Processing Guide

- **Step 2 (fetch + status collection)**: All repositories in parallel (independent)
- **Step 4 (processing)**: Sequential per repository (user interaction required)

## Notes

- Destructive commands like `git checkout .` must only be run after user confirmation
- Warn when orphan branches (branches without commits) are found
- Mark `.git` files separately (distinguish submodules/worktrees)
- Warn separately when large-scale deletions (10+ files staged deletion) are found
- Immediately notify user on stash pop conflicts

## Discovery Mode (scan directories outside ghq)

Discover Git repositories outside ghq and classify migration targets.

### Usage

```
/git-repo patrol --discover ~/projects ~/archive ~/src-backup
```

### Collected Information

In addition to standard patrol information:

- **origin URL**: Remote address ("no-origin" if none)
- **Host classification**: github.com, bitbucket.org, IP-based, non-standard
- **ghq duplicate check**: Verify with `ghq list | grep <repo-name>`
- **Migration classification**:
  - `migrate`: Standard remote, not in ghq
  - `duplicate`: Already exists in ghq (HEAD comparison needed)
  - `skip`: Non-standard remote (ssh://custom/... etc.)
  - `local`: Local-only repository without origin

### Output Format

```
## Discovery Results

| Path | origin | Host | Status | ghq dup | Classification |
|------|--------|------|--------|---------|----------------|
| ~/projects/infra | github.com/org/infra | github.com | M(5) | - | migrate |
| ~/projects/legacy | ssh://custom/root/source/legacy | non-standard | M(3) | - | skip |
| ~/src-backup/my-project | - | no-origin | - | - | local |
```

### Follow-up Actions

Proceed with `/git-repo migrate` Batch Migration based on Discovery results.
