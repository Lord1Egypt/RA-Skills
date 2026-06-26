---
name: github-rising-stars
description: Discover fast-growing GitHub repositories before they appear on the official Trending page. Use when users ask to find emerging/rising GitHub projects, spot early-stage repos gaining momentum, identify hidden gems not yet on Trending, or discover the hottest new repos in the last 1-7 days. Triggers on phrases like "find rising GitHub repos", "GitHub trending before trending", "fast growing repos", "GitHub黑马项目", "增速快的GitHub项目", "还没上trending的项目", "发现早期项目".
---

# GitHub Rising Stars

Discovers fast-growing GitHub repositories that haven't made the official Trending page yet, by querying the GitHub Search API across multiple dimensions and ranking by **stars per day**.

## Quick Start

Run the bundled script directly:

```bash
python3 scripts/find_rising.py
```

Default: repos created in the last 3 days, min 20 stars, top 15 results.

## Script Options

```
python3 scripts/find_rising.py [options]

--days N        Look-back window in days (default: 3, range: 1-7)
--min-stars N   Minimum star count threshold (default: 20)
--top N         Number of results to return (default: 15)
--lang LANG     Filter by programming language (e.g. Python, TypeScript, Go)
--json          Output machine-readable JSON
```

### Examples

```bash
# Find Python repos rising fast in the last 5 days
python3 scripts/find_rising.py --days 5 --lang Python

# Find top 20 repos with at least 50 stars
python3 scripts/find_rising.py --min-stars 50 --top 20

# JSON output for further processing
python3 scripts/find_rising.py --json
```

## How It Works

1. **Multi-query search** — runs 3 GitHub API queries with overlapping time/star ranges to maximize coverage
2. **Deduplication** — merges results by repo ID
3. **Spam filtering** — removes known low-quality signals (crypto bots, game hacks, follower farms, etc.)
4. **Rate calculation** — computes `stars / age_in_days` for each repo
5. **Ranked output** — sorts by rate descending, shows top N

## Interpreting Results

- **Rate > 200/day**: Viral — likely hits Trending within 24h
- **Rate 50–200/day**: Fast-rising — worth watching
- **Rate < 50/day**: Early signal — may accelerate

Repos with **no description** or **no language** tag may be spam or private mirrors — apply extra scrutiny.

## Agent Workflow

When a user asks to find rising repos:

1. Run `python3 scripts/find_rising.py` with appropriate flags
2. Present results in a clean table, grouped by theme/category if patterns emerge
3. Highlight repos worth deeper investigation (high rate + meaningful description + known author)
4. Optionally open top repos in browser for quick review

## Limitations

- GitHub Search API is unauthenticated by default — rate limit: 10 requests/min. Add a `Authorization: token <PAT>` header in the script for higher limits.
- Results reflect repos *created* recently; established repos that suddenly spike are not captured (use `pushed` filter variant for that).
- Stars can be artificially inflated; cross-reference with Hacker News / Reddit for validation.
