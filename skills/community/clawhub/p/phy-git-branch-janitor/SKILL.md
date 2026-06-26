---
name: Git Branch Janitor
description: Git branch cleanup assistant. Audits all local and remote branches, categorizes them as safe-to-delete (merged), stale-unmerged (old + no open PR), or active. Detects branches that exist locally but not on remote (orphaned), finds branches with no commits ahead of main, and optionally cross-references GitHub/GitLab PRs to confirm merge status. Outputs a prioritized delete plan with one copy-paste cleanup command. Zero external API required for local audit; optional GitHub CLI for PR status. Triggers on "clean up branches", "stale branches", "branch cleanup", "delete old branches", "git branch audit", "/git-branch-janitor".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - git
    - branches
    - cleanup
    - maintenance
    - github
    - developer-tools
    - workflow
---

# Git Branch Janitor

Audit every branch in your repo — local and remote — and produce a prioritized cleanup plan. Find branches that are already merged, branches that have gone stale with no activity, and branches that never made it to the remote. Get one copy-paste command to clean them all up safely.

**Works on any Git repo. Optional GitHub CLI for PR cross-reference. Zero config.**

---

## Trigger Phrases

- "clean up branches", "branch cleanup", "delete old branches"
- "stale branches", "orphaned branches", "branch audit"
- "git housekeeping", "which branches can I delete"
- "/git-branch-janitor"

---

## Step 1: Fetch Latest State

```bash
# Sync remote branch state (prune deleted remote branches from local tracking)
git fetch --all --prune

# Show current branch (to avoid deleting it)
git branch --show-current
```

> **Important:** Never delete the current branch, `main`, `master`, `develop`, or `release/*` — these are protected.

---

## Step 2: Inventory All Branches

Run all three simultaneously to build a complete picture:

```bash
# Local branches
git branch --format='%(refname:short)' | sort

# Remote branches
git branch -r --format='%(refname:short)' | sed 's/origin\///' | sort

# All branches with last commit metadata
git for-each-ref --sort=committerdate \
  --format='%(refname:short)|%(committerdate:relative)|%(committerdate:iso)|%(authorname)|%(subject)' \
  refs/heads refs/remotes/origin \
  | grep -v "HEAD$" \
  | sort -t'|' -k3
```

Parse each branch's:
- **Last commit date** → age bucket (< 7 days, 7-30 days, 30-90 days, > 90 days)
- **Author** → who owns this branch
- **Subject** → last commit message (hint about what the branch was for)

---

## Step 3: Classify Each Branch

### Class 1: SAFE-TO-DELETE (Merged)

Branches that are fully merged into the default branch:

```bash
# Branches merged into main (replace 'main' with your default branch)
DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's/refs\/remotes\/origin\///' || echo "main")

# Local merged branches
git branch --merged "$DEFAULT" | grep -v "^\*" | grep -vE "^\s*(main|master|develop|release/)" | sed 's/^  //'

# Remote merged branches
git branch -r --merged "origin/$DEFAULT" | grep -v "HEAD" | grep -vE "(main|master|develop|release/)" | sed 's/origin\///' | sed 's/^  //'
```

**Rule:** If a branch has been fully merged into the default branch, it's safe to delete.

### Class 2: STALE-UNMERGED (Review Required)

Branches NOT merged but with no recent activity:

```bash
# Branches NOT merged into main, older than 30 days
git for-each-ref \
  --format='%(refname:short)|%(committerdate:iso)|%(committerdate:relative)' \
  refs/heads \
  | while IFS='|' read -r branch date reldate; do
      # Skip protected branches
      echo "$branch" | grep -qE "^(main|master|develop|release/)" && continue
      # Check if merged
      git merge-base --is-ancestor "$branch" "$DEFAULT" 2>/dev/null && continue
      # Check age > 30 days
      DAYS=$(( ($(date +%s) - $(date -d "$date" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M:%S %z" "$date" "+%s" 2>/dev/null)) / 86400 ))
      [ "$DAYS" -gt 30 ] && echo "$branch|${DAYS}d old|$reldate"
  done
```

**Rule:** These need human review — was this branch abandoned? Did it become a draft PR?

### Class 3: ORPHANED (Local only, never pushed)

Branches that exist locally but have no remote tracking branch:

```bash
git branch -vv | grep ": gone]" | awk '{print $1}'
# These had a remote, but remote was deleted (PR merged via GitHub UI)

git branch -vv | grep -v "\[origin" | grep -v "^\*" | awk '{print $1}'
# These were never pushed at all
```

### Class 4: AHEAD-ONLY (Unpushed work)

Branches that have commits not on remote — **don't delete these**:

```bash
# Check which branches have commits ahead of remote
git branch -vv | grep "ahead"
```

---

## Step 4: Cross-Reference PRs (Optional — requires `gh` CLI)

If `gh` is available, enhance stale-unmerged branches with PR status:

```bash
# Check if a branch has an open or merged PR
for branch in $STALE_BRANCHES; do
  PR=$(gh pr list --head "$branch" --state all --json number,state,title --jq '.[0]' 2>/dev/null)
  if [ -n "$PR" ]; then
    STATE=$(echo "$PR" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['state'])")
    TITLE=$(echo "$PR" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['title'][:50])")
    NUMBER=$(echo "$PR" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['number'])")
    echo "$branch → PR #$NUMBER ($STATE): $TITLE"
  else
    echo "$branch → No PR found"
  fi
done
```

**With PR context:**
- `MERGED` PR → definitely safe to delete
- `CLOSED` PR → was abandoned, confirm with user before deleting
- `OPEN` PR → active work in progress — **never delete**
- No PR → was this work captured elsewhere? Ask user.

---

## Step 5: Generate Cleanup Commands

Produce three batches of commands:

### Batch 1: Auto-Safe Deletes

```bash
# Delete merged local branches
git branch -d feat/add-login feat/fix-typo chore/update-deps

# Delete merged remote branches
git push origin --delete feat/add-login feat/fix-typo chore/update-deps
```

### Batch 2: Gone-Remote Cleanup (Orphaned)

```bash
# These had remotes that were already deleted (usually by GitHub after PR merge)
git branch -d fix/header-bug refactor/auth-service
```

### Batch 3: Stale-Unmerged (Review First)

```bash
# ⚠️ Review these before running — they were never merged
# Branch: wip/new-feature (last commit: 47 days ago, no PR found)
# git branch -D wip/new-feature  # -D forces delete of unmerged branch
# git push origin --delete wip/new-feature
```

---

## Output Report

Always produce this report structure:

```markdown
## Git Branch Janitor Report
Repo: [repo name] | Default branch: main | $(date)

### Summary
| Category | Local | Remote |
|----------|-------|--------|
| 🟢 Safe-to-delete (merged) | 8 | 6 |
| 🟠 Stale unmerged (>30 days, no open PR) | 3 | 2 |
| 🔵 Orphaned (remote gone) | 4 | — |
| ⚠️ Ahead-only (unpushed work) | 2 | — |
| ✅ Active (recent commits) | 5 | 7 |

---

### 🟢 Safe to Delete — Already Merged

| Branch | Last Commit | Author | Merged Via |
|--------|-------------|--------|-----------|
| feat/add-login | 12 days ago | alice | PR #142 (merged) |
| fix/header-bug | 23 days ago | bob | PR #138 (merged) |
| chore/bump-deps | 31 days ago | alice | Direct merge |

**One command to clean all:**
```bash
# Local
git branch -d feat/add-login fix/header-bug chore/bump-deps

# Remote
git push origin --delete feat/add-login fix/header-bug chore/bump-deps
```

---

### 🔵 Orphaned — Remote Already Deleted

These branches exist locally but their remote was deleted (e.g., GitHub merged the PR):

| Branch | Last Commit | Author |
|--------|-------------|--------|
| feat/dark-mode | 8 days ago | carol |
| fix/mobile-nav | 15 days ago | alice |

```bash
git branch -d feat/dark-mode fix/mobile-nav
```

---

### 🟠 Stale Unmerged — Review Before Deleting

| Branch | Age | Author | PR Status |
|--------|-----|--------|----------|
| wip/new-dashboard | 47 days | bob | No PR found |
| experiment/redis-cache | 62 days | carol | PR #120 (closed, abandoned) |

**⚠️ These were never merged. Confirm with owner before deleting:**
```bash
# Only run after confirming work is captured or abandoned:
git branch -D wip/new-dashboard
git push origin --delete wip/new-dashboard
```

---

### ⚠️ Skipped — Has Unpushed Work

| Branch | Commits Ahead | Last Commit |
|--------|--------------|-------------|
| feat/user-settings | 7 commits | 2 days ago |
| fix/payment-flow | 2 commits | yesterday |

**Not deleted — these have unpushed commits. Push or open a PR first.**

---

### Cleanup Summary

After running the safe commands above, you'll free:
- **15 local branches** removed
- **8 remote branches** removed
- Estimated `git fetch` speed improvement: ~30% (fewer refs to sync)
```

---

## Age Thresholds (Configurable)

By default, branches are flagged as "stale" after:

| Category | Default Threshold |
|----------|------------------|
| Stale (review recommended) | > 30 days since last commit |
| Very stale (safe to flag) | > 90 days since last commit |
| Ancient (definitely dead) | > 6 months |

User can override: "show branches older than 2 weeks" or "flag anything over 60 days."

---

## Protected Branches (Never Delete)

The following patterns are always excluded from cleanup suggestions:

```
main, master, develop, staging, production
release/*, hotfix/*, v*.*.*
HEAD
```

---

## Quick Mode

When user just wants a fast count:

```
Quick Branch Audit:
🟢 12 merged (safe to delete)
🔵 5 orphaned (remote gone)
🟠 3 stale unmerged (>30d, no open PR)
⚠️ 2 with unpushed commits (skip)

Safe to clean: 17 branches
Run /git-branch-janitor --full for delete commands
```

---

## Why Not Just `git branch -d`?

`git branch -d` only deletes branches merged into the current HEAD — it misses:

- Branches merged on GitHub/GitLab via squash or rebase (not a standard merge commit)
- Remote tracking refs left behind after the remote branch was deleted
- Branches with PRs that were closed without merging
- Branches that diverged from main and were superseded by a re-implementation

This skill handles all four cases.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
