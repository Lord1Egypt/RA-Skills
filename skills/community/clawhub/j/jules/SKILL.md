---
name: jules
description: Manage and automate coding tasks with Jules, Google's autonomous AI coding agent CLI. Use when delegating repository tasks, tracking remote sessions, reviewing/applying patches, or using teleport.
metadata:
  openclaw:
    emoji: 🦑
    requires:
      bins: [jules]
---

# Jules CLI

Use this skill to interact with Jules (`jules`), Google's autonomous AI coding agent for cloud-based asynchronous software engineering tasks.

## Quick reference

| Goal | Command |
| --- | --- |
| Launch interactive TUI | `jules` |
| Delegate task (current repo) | `jules new "task description"` |
| Delegate task (specific repo) | `jules new --repo <owner/repo> "task description"` |
| Run parallel attempts | `jules new --parallel <1-5> "task description"` |
| Pipe prompt from stdin | `cat task.md \| jules new` |
| List remote sessions | `jules remote list --session` |
| List connected repos | `jules remote list --repo` |
| Pull patch | `jules remote pull --session <id>` |
| Pull and apply patch | `jules remote pull --session <id> --apply` |
| Clone & apply in one step | `jules teleport <id>` |
| Auth status & lifecycle | `jules login` / `jules logout` |

## Core workflows

### 1. Delegating tasks

Delegate async work without waiting in the terminal:

```bash
# Current repo auto-detected
jules new "Fix flaky unit test in auth_test.go"

# Specific remote repo
jules new --repo org/backend "Upgrade dependency X to v2 and fix breaking changes"

# Generate 3 candidate approaches in parallel
jules new --parallel 3 "Refactor caching layer to use Redis cluster"
```

### 2. Monitoring & inspecting progress

- List active and historical sessions: `jules remote list --session`
- Check connected GitHub/source repos: `jules remote list --repo`
- Launch dashboard TUI: `jules`

### 3. Reviewing & applying changes

- **Apply directly to existing checkout**:
  ```bash
  jules remote pull --session <id> --apply
  ```
- **Inspect patch before applying**:
  ```bash
  jules remote pull --session <id> > patch.diff
  git apply --check patch.diff
  ```
- **Fresh checkout (Teleport)**:
  ```bash
  jules teleport <id>
  ```
  _Teleport behavior_:
  - Inside a matching git repo: applies the patch to current workspace.
  - Outside a repo: clones the repository, checks out the base branch, and applies the session patch automatically.

## References

For detailed subcommands and automation patterns, load [`references/cli-reference.md`](references/cli-reference.md).
