---
name: keyword-research
description: "Multi-source keyword intelligence and autocomplete research. Fetches real-time suggestions from Google, YouTube, Amazon, and DuckDuckGo — no API key required. Use when: (1) doing SEO or content keyword research, (2) finding what users search for on a topic, (3) competitor or niche research, (4) expanding a seed keyword into hundreds of related terms, (5) building keyword lists for ads or content. Triggers on: keyword research, what do people search for, autocomplete, keyword ideas, SEO keywords, search suggestions, keyword list."
---

# Keyword Intelligence

Multi-source autocomplete fetcher — no API keys needed. Pulls real-time suggestions from Google, YouTube, Amazon, and DuckDuckGo.

## Quick Usage

```bash
# All sources, default language (de)
python3 scripts/fetch_suggestions.py "keyword"

# Specific sources
python3 scripts/fetch_suggestions.py "keyword" --sources google,youtube

# English / US region
python3 scripts/fetch_suggestions.py "keyword" --lang en --region us

# Expand mode: fetch suggestions of suggestions (10x more keywords)
python3 scripts/fetch_suggestions.py "keyword" --sources google --expand

# JSON output (for piping or further processing)
python3 scripts/fetch_suggestions.py "keyword" --json
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--sources` | `all` | `all` or comma-separated: `google`, `youtube`, `amazon`, `ddg` |
| `--lang` | `de` | Language code: `de`, `en`, `tr`, `fr`, `es`, ... |
| `--region` | `de` | Region: `de`, `us`, `tr`, `gb`, ... |
| `--expand` | off | Fetches 2nd-level suggestions from Google (base keywords → ~10x results) |
| `--json` | off | Outputs JSON instead of formatted text |

## Sources

- **Google** — Broadest coverage, best for general web search intent
- **YouTube** — Video content ideas, tutorials, how-to queries
- **Amazon** — Product/buying intent keywords (works best for product niches)
- **DuckDuckGo** — Privacy-focused users, tech/dev audience

## Workflow

1. Start with a seed keyword and `--sources all`
2. Identify which source is most relevant for the use case
3. Use `--expand` on the most promising source for deeper research
4. Export with `--json` to process or display the results

## Notes

- No rate limits enforced, but add delays for large batch jobs (the script adds 0.2s between expand calls)
- Amazon suggestions may be empty for non-product keywords — expected behavior
- YouTube returns fewer results for niche/regional keywords
- `--expand` only works on Google (most reliable for 2nd-level fetching)
