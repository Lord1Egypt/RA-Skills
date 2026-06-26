---
name: github-agent-trends
description: Generate GitHub agent-trending project reports as formatted markdown leaderboards. Fetches agent/LLM-agent/multi-agent related repos by daily, weekly, or monthly activity window and sorts by stars. Use when the user asks for GitHub agent trends, AI agent leaderboard, coding agents, or popular agent frameworks on GitHub.
---

# GitHub Agent Trends

Generate a formatted leaderboard of **agent-related** open-source projects on GitHub (keywords + topics such as `ai-agent`, `multi-agent`, `agent framework`), and paste the script output into chat.

## Usage

From the **repository root**:

```bash
python3 scripts/skills/github-agent-trends/scripts/fetch_trends.py --period weekly --limit 20
```

With a token (recommended for rate limits):

```bash
export GITHUB_TOKEN=ghp_...
python3 scripts/skills/github-agent-trends/scripts/fetch_trends.py --period weekly --limit 20
```

## Parameters

- `--period`: `daily` | `weekly` | `monthly` (default: `weekly`)
- `--limit`: Number of repos after dedupe/sort (default: 20)
- `--token`: GitHub PAT (or set `GITHUB_TOKEN`)
- `--json`: Raw JSON instead of markdown

## How It Works

1. Queries GitHub **Search repositories** API with agent-focused **keywords** (e.g. `ai-agent`, `multi-agent`, `agent framework`) and **topics** (e.g. `ai-agent`, `multi-agent`, `langchain`, `autogen`), filtered by `pushed` within the period and minimum stars.
2. Deduplicates by `full_name`, sorts by `stargazers_count`, takes top N.
3. Prints a markdown leaderboard (Chinese title: **GitHub Agent 趋势榜**).

## Notes

- Results reflect **search relevance + stars**, not the official GitHub “Trending” page (which has no public API).
- Unauthenticated: ~10 requests/minute to Search API; with `GITHUB_TOKEN`: higher quotas (follow GitHub docs).
- **Stdlib only** — no pip dependencies.

## Customization

Edit `SEARCH_KEYWORDS` and `SEARCH_TOPICS` in `scripts/fetch_trends.py` to widen or narrow the agent theme (e.g. add `crewai`, `browser-use`).
