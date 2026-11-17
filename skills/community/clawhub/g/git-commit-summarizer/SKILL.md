---
name: git-commit-summarizer
description: Generate structured summaries of recent git commit activity. Use when the user asks for a commit summary, changelog draft, standup notes from git, or to understand what changed in a repo over a time range. Supports filtering by author, date range, and output format.
metadata:
  openclaw:
    emoji: "📝"
---

# Git Commit Summarizer

Generate structured summaries of recent git commits in a repository.

## When to use

- User asks "what did I commit this week?"
- Drafting a changelog or release notes
- Preparing daily standup notes from git activity
- Reviewing what changed in a time range

## Prerequisites

- Git repository present in the working directory
- `git` CLI available

## Usage

Run the summarizer script:

```bash
bash scripts/summarize.sh [OPTIONS]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--since <date>` | Start date (e.g. `7 days ago`, `2026-01-01`) | `7 days ago` |
| `--until <date>` | End date | now |
| `--author <name>` | Filter by author (regex) | all |
| `--format <text|json>` | Output format | `text` |
| `--repo <path>` | Repository path | cwd |

### Examples

```bash
# Summary of last 7 days
bash scripts/summarize.sh

# Last 24 hours, current author only
bash scripts/summarize.sh --since "24 hours ago" --author "$(git config user.name)"

# JSON output for last 30 days
bash scripts/summarize.sh --since "30 days ago" --format json

# Specific repo
bash scripts/summarize.sh --repo /path/to/repo --since "2026-08-01"
```

## Output

### Text format

```
## Commit Summary: 2026-08-23 → 2026-08-30
Total commits: 12

### By type
- feat: 5
- fix: 4
- docs: 2
- chore: 1

### Recent commits
- abc1234 feat: add user authentication
- def5678 fix: resolve login redirect bug
...
```

### JSON format

```json
{
  "since": "2026-08-23",
  "until": "2026-08-30",
  "totalCommits": 12,
  "byType": { "feat": 5, "fix": 4, "docs": 2, "chore": 1 },
  "commits": [
    { "hash": "abc1234", "author": "Jane", "date": "2026-08-30", "message": "feat: add user authentication", "type": "feat" }
  ]
}
```
