---
name: git-guardian
description: >
  Track all agent work in git and show diffs before applying changes. Use when:
  (1) creating or modifying scripts, configs, skills, or any workspace files,
  (2) user wants transparency into what the agent changed,
  (3) enforcing a "show before apply" workflow for agent modifications.
  Triggers on: file creation, editing, config changes, script building,
  or when user says "show me what you changed." Ensures all agent work
  is committed, diffable, and reviewable before taking effect.
---

# Git Guardian

Enforce git-tracked, diff-first workflow for all agent file operations.

## Core Rules

1. **All work lives in git.** Every file the agent creates or modifies must be in a git repo.
2. **Branch before changing.** Create a feature branch before making changes. Never commit directly to main.
3. **Diff before applying.** After making changes, show the user a `git diff` before finalizing. Wait for approval.
4. **Commit with context.** Every commit gets a clear message explaining what changed and why.
5. **Push and link.** Push the branch and provide a link (or inline diff) so the user can review.

## Workflow

### For new files or modifications:

```
1. git checkout -b <descriptive-branch-name>
2. Make the changes (create/edit files)
3. git diff                              # Show the user what changed
4. Wait for user approval (👍 or explicit "go ahead")
5. git add -A && git commit -m "<clear message>"
6. git push origin <branch-name>
7. Show the user: branch name, commit hash, diff summary
```

### For quick single-file changes:

```
1. Make the edit
2. Show inline diff (before/after) in chat
3. On approval: commit + push on current branch
```

### Diff display format:

When showing diffs in chat, use fenced code blocks with `diff` syntax highlighting:

~~~
```diff
- old line
+ new line
```
~~~

For large diffs (>50 lines), summarize the key changes in bullet points first, then offer the full diff on request.

## When to use branches vs inline diffs

- **Branch + PR:** Multi-file changes, new features, config modifications, anything touching behavior
- **Inline diff:** Single-line fixes, typo corrections, minor tweaks — still commit, just skip the branch ceremony

## What NOT to track

- Ephemeral files: `/tmp/`, session state, working buffers
- Secrets: Never commit API keys, tokens, or credentials
- Large binaries: Artifacts, media files (reference them, don't commit them)

## Integration

This skill works alongside existing git workflows. It doesn't replace PR review processes — it adds transparency to the agent's own work so the user always knows what changed and can verify it.

## Script: git-guardian.sh

Use `scripts/git-guardian.sh` for common operations:

```bash
# Start tracked work
scripts/git-guardian.sh start "description of work"
# → Creates branch, logs start time

# Show what changed
scripts/git-guardian.sh diff
# → Pretty-prints staged + unstaged changes

# Commit with message
scripts/git-guardian.sh commit "what changed and why"
# → Stages all, commits, shows summary

# Wrap up and push
scripts/git-guardian.sh finish
# → Pushes branch, shows commit log, provides review link
```
