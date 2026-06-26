---
name: github-trending-scraper
description: >
  Scrape GitHub Trending repos into structured JSON. Use when the user asks about
  GitHub trending, hottest repos, trending repositories, what's popular on GitHub today,
  or needs GitHub trending data for cards/visualizations. Supports language filters
  (python, rust, go, etc.) and time ranges (daily, weekly, monthly).
---

# GitHub Trending Scraper

Scrapes `https://github.com/trending` and outputs structured JSON.

## Quick Start

```bash
# All languages, today, top 25
python3 scripts/github_trending.py

# Python repos, this week, top 10
python3 scripts/github_trending.py --language python --since weekly --top 10

# Save to file
python3 scripts/github_trending.py -o /tmp/github-trending.json
```

## Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--language` | `-l` | all | Filter by language (python, rust, go, javascript, etc.) |
| `--since` | `-s` | daily | Time range: `daily`, `weekly`, `monthly` |
| `--top` | `-n` | 25 | Number of repos to return |
| `--output` | `-o` | stdout | Output file path |
| `--compact` | | | Minified JSON output |

## Output Schema

```json
{
  "source": "github-trending",
  "scraped_at": "ISO-8601",
  "language": "all|python|rust|...",
  "since": "daily|weekly|monthly",
  "count": 25,
  "repos": [
    {
      "rank": 1,
      "owner": "warpdotdev",
      "name": "warp",
      "full_name": "warpdotdev/warp",
      "url": "https://github.com/warpdotdev/warp",
      "description": "Warp is an agentic development environment...",
      "language": "Rust",
      "stars": 46667,
      "forks": 2917,
      "stars_period": 12822,
      "stars_period_label": "today"
    }
  ]
}
```

## Integration with Trending Cards

Pipe output into the existing trending card generator:

```bash
python3 scripts/github_trending.py -o /tmp/github-trending.json
python3 ~/.openclaw/workspace/scripts/trending-card-gen.py \
  --input /tmp/github-trending.json \
  --output /tmp/trending-card.html \
  --platform github --theme white --size hd
```

## Notes

- No API key required; scrapes the public GitHub Trending page
- Rate limit: reasonable use only; avoid rapid repeated calls
- Some repos (e.g. `sponsors/username`) may show 0 stars/forks due to GitHub page structure
