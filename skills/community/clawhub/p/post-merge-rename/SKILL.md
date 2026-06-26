---
name: post-merge-rename
description: Post-merge branch renaming. Appends --merged-YYYY-MM-DD to preserve history.
license: MIT
interface: [cli, skill]
metadata:
  display-name: "Post-Merge Branch Naming"
  version: "1.3.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - branch-rename
    - history-preservation
  requires:
    bins: [git, bash]
  openclaw:
    requires:
      bins: [git, bash]
    emoji: "🏷️"
compatibility: Requires git, bash.
---

# post-merge-rename

Scans for merged branches that haven't been renamed and appends `--merged-YYYY-MM-DD` to preserve history. We never delete branches. We rename them.

## When to Use This Skill

**Use post-merge-rename for:**
- After merging PRs, to rename the source branch
- Cleaning up branches that were merged but not renamed
- Runs automatically as step 10 of `wip-release`

### Do NOT Use For

- Unmerged branches
- Branches you're currently working on

## API Reference

### CLI

```bash
bash scripts/post-merge-rename.sh              # scan + rename all merged branches
bash scripts/post-merge-rename.sh --dry-run     # preview only
bash scripts/post-merge-rename.sh <branch>      # rename specific branch
```

## What It Does

1. Lists all local branches merged into main
2. Skips branches already renamed (containing `--merged-`)
3. Finds the merge date from git history
4. Renames: `feature-branch` -> `feature-branch--merged-2026-03-09`
5. Pushes the renamed branch to origin
6. Deletes the old branch name from origin
