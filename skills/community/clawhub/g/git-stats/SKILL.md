---
name: git-stats
description: Analyze git repository statistics including contributor rankings, lines of code by language, commit frequency by day/hour, monthly activity trends, and file type breakdowns. Use when asked to analyze a repo, show git stats, get contributor info, count lines of code, or visualize commit activity patterns.
---

# Git Stats

Analyze any local git repository for contributor rankings, LOC by language, commit activity patterns, and monthly trends.

## Quick Start

```bash
# Analyze current repo
python3 scripts/git_stats.py

# Analyze a specific repo
python3 scripts/git_stats.py /path/to/repo

# JSON output for further processing
python3 scripts/git_stats.py --json

# Filter by date range
python3 scripts/git_stats.py --since 2025-01-01 --until 2025-12-31

# Specific branch
python3 scripts/git_stats.py --branch main

# Skip LOC counting for faster results
python3 scripts/git_stats.py --no-loc
```

## Output Sections

- **Top Contributors** — ranked by commit count with email
- **Lines of Code** — total files/lines, broken down by extension
- **File Types** — file count by extension
- **Activity by Day** — which days of the week get the most commits
- **Activity by Hour** — peak coding hours
- **Monthly Trend** — commit volume over the last 12 months (configurable with `--months`)

## Options

| Flag | Description |
|------|-------------|
| `--branch` | Analyze a specific branch |
| `--since` | Only include commits after this date |
| `--until` | Only include commits before this date |
| `--months N` | Monthly trend window (default: 12) |
| `--json` | Output as JSON for programmatic use |
| `--no-loc` | Skip line counting (much faster on large repos) |

## Dependencies

- `git` CLI (must be on PATH)
- Python 3.8+ (stdlib only, no pip packages needed)
