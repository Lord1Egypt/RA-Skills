---
name: git-quick
description: Show a quick summary of the current git repo — branch, status, recent commits, and contributor stats.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - git
    emoji: "\U0001F500"
---

# git-quick

A lightweight skill that displays a quick summary of the current git repository.

## What it does

- Shows current branch and tracking status
- Lists modified/staged/untracked files
- Displays the 5 most recent commits
- Shows top contributors by commit count

## Usage

Run the script directly:

```bash
bash git-quick.sh
```

Or use the shorthand:

```bash
bash git-quick.sh --short    # Only show branch + status
bash git-quick.sh --commits  # Only show recent commits
bash git-quick.sh --stats    # Only show contributor stats
```

## Example Output

```
=== Git Quick Summary ===
Branch: main (up to date with origin/main)

--- Status ---
M  src/app.ts
A  src/utils.ts
?? config.local.json

--- Recent Commits ---
a1b2c3d feat: add user auth module          (2 hours ago)
e4f5g6h fix: resolve login redirect loop    (5 hours ago)
i7j8k9l docs: update API reference          (1 day ago)

--- Top Contributors ---
  alice  42 commits
  bob    28 commits
  carol  15 commits
```
