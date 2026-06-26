---
name: github-trending
description: "Fetch top trending GitHub repositories today/this-week/this-month and summarize top 15 with stars, language, description."
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": ["curl", "jq"],
              "bins": ["curl", "jq"],
              "label": "Install curl + jq (brew)",
            },
          ],
      },
  }
---

# GitHub Trending

Fetch and summarize top trending GitHub repos. Uses GitHub search API — no auth required for basic queries (rate-limited at 10 req/min unauthenticated).

## Usage

```bash
# Top 15 repos trending this week (default)
bash scripts/fetch-trending.sh

# Custom time range
bash scripts/fetch-trending.sh "2026-05-15"

# Custom count
bash scripts/fetch-trending.sh "7-days-ago" 10
```

## Output

For each repo: rank, name, description (truncated), language, ⭐ stars, 🍴 forks, link.

## Rate Limits

- Unauthenticated: 10 req/min — enough for occasional use
- Authenticated (set `GH_TOKEN` env): 5000 req/hr
- If hitting limits, increase the `--retry` or use longer date ranges