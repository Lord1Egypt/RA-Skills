---
name: pr-auto-merger
description: "Autonomous PR merge agent. Scans repos for approved + CI-passing PRs and merges them automatically. Supports dry-run mode, squash/merge options, and min-approval thresholds. Ideal for teams wanting hands-off PR cleanup."
version: "1.0.0"
slug: pr-auto-merger
tags: ["github", "pr", "auto-merge", "ci-cd", "automation", "devops"]
---

# PR Auto-Merge Agent

Autonomous pull request merge tool. Scans GitHub repos for PRs that are approved, CI-passing, and mergeable — then merges them automatically (or reports in dry-run mode).

## What It Does

- Finds all open PRs that are: not drafts + mergeable + CI passing + approved
- Merges them via `--squash` (default) or `--admin --merge`
- Supports `--dry-run` mode to preview what WOULD be merged without making changes
- Configurable minimum approval count
- Pure Python stdlib + `gh` — zero external dependencies

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Python 3.6+
- Token must have `repo` scope to merge

## Quick Start

```bash
# Preview what would be merged (default — safe)
python3 scripts/auto_merge.py owner/repo

# Actually merge
python3 scripts/auto_merge.py owner/repo --no-dry-run

# Require 2 approvals minimum, squash merge
python3 scripts/auto_merge.py owner/repo --min-approvals 2 --squash

# Scan multiple repos
python3 scripts/auto_merge.py owner/repo1 && python3 scripts/auto_merge.py owner/repo2
```

## Usage as Claude Code Skill

```
/pr-auto-merger owner/repo --dry-run
```

The agent will:
1. Fetch all open PRs from the repo via `gh pr list --json`
2. Filter to approved + CI-passing + mergeable PRs
3. Report in dry-run mode (default), or merge with `--no-dry-run`

## Merge Criteria

A PR is merged only when ALL of these are true:
- Not a draft (`isDraft: false`)
- Mergeable (`mergeable: true`)
- All required status checks passing (`statusCheckRollup conclusion: SUCCESS`)
- Review decision is `APPROVED`
- Has at least `--min-approvals` approvals (default: 1)

## Output Format

```
Scanning owner/repo for mergeable PRs...
[DRY-RUN] Found 3 PR(s) ready to merge:
  #123 — Fix auth middleware (https://github.com/owner/repo/pull/123)
  #456 — Add caching layer (https://github.com/owner/repo/pull/456)
  #789 — Update dependencies (https://github.com/owner/repo/pull/789)

Re-run with --no-dry-run to actually merge.
```

## GitHub Actions Integration

Drop this into a nightly cron job:

```yaml
name: Nightly PR Merge
on:
  schedule:
    - cron: '0 6 * * *'
jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          pip install gh
          gh auth status
          python3 scripts/auto_merge.py owner/repo --no-dry-run --min-approvals 2
```

## Cron Agent Configuration

For OpenClaw scheduling, configure as:

```json
{
  "task": "python3 /path/to/scripts/auto_merge.py owner/repo --no-dry-run",
  "schedule": "0 8 * * 1-5",
  "notify_on": ["failure", "merged"]
}
```

## Architecture

- `scripts/auto_merge.py` — Pure Python 3 (stdlib only)
- Uses `gh pr list --json` for data fetching
- Uses `gh pr merge` for actual merging
- No pip packages, no external APIs
- Portable: Linux, macOS, Windows (Python + gh)

## License

MIT
