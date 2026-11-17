---
name: git-state-checker
description: Reports git repository status including modified files, untracked files, recent commits, and stash list. Use when checking repo state before solidify, after evolution cycles, or when diagnosing git issues.
---

# Git State Checker

Quick git repository health report.

## Usage

```bash
node skills/git-state-checker/index.js
```

## What It Reports

- Modified, staged, and untracked files
- Recent commit history (default 5)
- Stash list with overflow warning if >10 entries

## Why It Exists

Evolver cycles create stash entries on failure. This skill helps monitor stash buildup and working directory state before solidify operations.
