---
name: google-trending
description: "Fetch and display the top trending Google searches in the last 24 hours for any country. Use when the user asks for Google trending topics, trending searches, what people are googling, or top searches today."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "python3",
              "kind": "system",
              "bins": ["python3"],
              "label": "Python 3 (stdlib only, no pip required)",
            },
          ],
      },
  }
---

# Google Trending

Fetch the top trending Google searches in the last 24 hours via the Google Trends daily RSS feed. No API key required.

## Usage

```bash
# Top 20 trending searches in the US (default)
python3 scripts/fetch-google-trending.py

# Specific country (ISO 3166-1 alpha-2 code)
python3 scripts/fetch-google-trending.py FR
python3 scripts/fetch-google-trending.py GB
python3 scripts/fetch-google-trending.py JP

# Custom result count
python3 scripts/fetch-google-trending.py US 10
```

## Arguments

| Position | Default | Description                          |
|----------|---------|--------------------------------------|
| 1        | `US`    | Country code (ISO 3166-1 alpha-2)   |
| 2        | `20`    | Number of trending topics to show    |

## Output

For each trending topic: rank, search term, approximate search volume, publication time, up to 2 related news headlines with source, and a link to the Google Trends page.

## Data source

- **Feed**: `https://trends.google.com/trending/rss?geo={GEO}`
- **Update cadence**: refreshed every few hours by Google
- **No auth required**: uses only public RSS endpoints and Python stdlib (`urllib`, `xml.etree`)

## Workflow for the AI agent

1. Run `python3 scripts/fetch-google-trending.py [GEO] [COUNT]`
2. Parse and present the results to the user
3. If the user asks about a specific trending topic, you can search for more context using WebSearch

## Guardrails

- Data comes directly from Google Trends RSS — do not fabricate traffic numbers or topics.
- The feed reflects Google's own editorial/algorithmic choices; surface that to the user if asked why a topic appears.
- If the fetch fails (network error, rate limit), report it clearly and suggest retrying.
