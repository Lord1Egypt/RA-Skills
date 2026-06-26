---
name: code-sync
description: >-
  Use this skill to batch-sync all git repos across machines — pushing uncommitted
  changes at end of day or pulling latest at start of day. Invoke when the user
  wants to sync all repos (not just one), mentions 「下班同步」「上班更新」
  「code-sync」, or describes end-of-day push / morning pull across ~/code.
  Triggers on: "sync all my repos", "end of day sync", "morning update",
  "push all dirty repos", "pull all projects", 「同步代码」「下班同步」「上班更新」.
  Do NOT trigger for: single-repo git operations, committing specific files
  (use git-workflow), general git push/pull questions, or workspace template updates.
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["git"]}}}
---

# Code Sync

Batch sync all git repos under a base directory — push (end-of-day) or pull (start-of-day).
Default base directory: `~/code`. Configurable via `~/.config/nini-skill/code-sync/config.md`.

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| git | cli | Yes | `brew install git` or [git-scm.com](https://git-scm.com/) |
| git-workflow | skill | Yes | Included in `npx skills add niracler/skill` — **must** be invoked via `Skill` tool for all commits |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## First-Time Setup

On first use, check for config at `~/.config/nini-skill/code-sync/config.md`.
If not found, ask the user:

1. "Where do you keep your git repos?" (default: `~/code`)
2. "What's the directory structure?" — explain the expected pattern:
   `<base-dir>/*/` for top-level repos and `<base-dir>/*/repos/*/` for monorepo sub-repos
3. Save to `~/.config/nini-skill/code-sync/config.md`:

```yaml
base_dir: ~/code
```

## Mode Selection

| User says | Mode |
|-----------|------|
| 「下班同步」or "push" | Push |
| 「上班更新」or "pull" | Pull |
| 「同步代码」「code-sync」 | Ask user |

## Workflow (shared by both modes)

1. **Scan** → 2. **Categorize** → 3. **Batch action** (auto, no confirmation) → 4. **Handle exceptions** (interactive) → 5. **Summary**

If all repos are up-to-date, report that and stop.

### Scan

```bash
bash scripts/scan.sh                          # Push: local data only (default ~/code)
bash scripts/scan.sh --fetch                  # Pull: fetch remote first (10s timeout/repo)
bash scripts/scan.sh --base-dir /path/to/dir  # Custom base directory
```

Output: JSON array with fields `path`, `name`, `branch`, `remote`, `remote_url`, `dirty_count`, `has_upstream`, `ahead`, `behind`, and `fetch_error` (only on `--fetch` failure).

### Categorize

**Push mode:**

| Category | Condition | Action |
|----------|-----------|--------|
| up-to-date | `dirty_count == 0 && ahead == 0` | Report |
| needs-push | `dirty_count == 0 && ahead > 0` | Auto `git push` |
| dirty | `dirty_count > 0` | Interactive |
| no-upstream | `has_upstream == false` | Ask user |

**Pull mode:**

| Category | Condition | Action |
|----------|-----------|--------|
| up-to-date | `dirty_count == 0 && behind == 0` | Report |
| needs-pull | `dirty_count == 0 && behind > 0` | Auto `git pull --ff-only` |
| dirty+behind | `dirty_count > 0 && behind > 0` | Interactive |
| fetch-error | `fetch_error == true` | Report, skip |

### Exception Handling

| Situation | Steps |
|-----------|-------|
| **Dirty repo** (push) | `git diff --stat` + `git status` → describe to user → ask: **commit**, **stash**, or **skip**. If commit, **MUST invoke `git-workflow` skill via `Skill` tool** — never run `git commit` directly. |
| **No upstream** (push) | Report → ask: **set upstream and push** (`git push -u origin <branch>`), or **skip** |
| **ff-only fails** (pull) | `git log --oneline HEAD..@{u}` + `@{u}..HEAD` → explain divergence → suggest: **rebase**, **merge**, or **skip** |
| **Dirty + behind** (pull) | Report both issues → ask: **stash and pull** (stash, pull --ff-only, pop), or **skip** |

### Summary

Group repos by outcome after all operations complete:

```text
## {Push|Pull} Summary

{Pushed|Updated} (N):
  - repo-name (branch, N commits)
Already up-to-date (N):
  - repo-a, repo-b, ...
Resolved (N):
  - repo-c: action taken
Skipped (N):
  - repo-d: reason
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `scan.sh` finds 0 repos | Check `~/code/*/` has git repos |
| `fetch_error` | Check network, SSH keys |
| ff-only fails | Rebase or merge manually |
| Push rejected | Pull first, then push |
