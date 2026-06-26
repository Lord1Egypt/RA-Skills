---
name: google-trends
description: Fetches Google Trends data including daily trending topics, real-time trends, interest by region, related topics, related queries, and autocomplete suggestions. Use when the user asks about trending searches, search popularity, keyword trends, or Google Trends data.
---

# Google Trends

Fetch Google Trends data using the bundled script. No API key required.

## Quick start

Run the script from the skill directory:

```bash
node scripts/trends.mjs <command> [options]
```

## Available commands

| Command | Description |
|---------|-------------|
| `daily-trends` | Get daily trending search topics |
| `realtime-trends` | Get real-time trending topics |
| `autocomplete` | Get autocomplete suggestions for a keyword |
| `explore` | Explore trend data for a keyword |
| `interest-by-region` | Get search interest breakdown by region |
| `related-topics` | Get topics related to a keyword |
| `related-queries` | Get queries related to a keyword |

## Usage examples

**Daily trending topics in the US:**
```bash
node scripts/trends.mjs daily-trends --geo US
```

**Real-time trends (last 4 hours):**
```bash
node scripts/trends.mjs realtime-trends --geo US --hours 4
```

**Autocomplete suggestions:**
```bash
node scripts/trends.mjs autocomplete "artificial intelligence"
```

**Explore a keyword:**
```bash
node scripts/trends.mjs explore "machine learning" --geo US --time "now 7-d"
```

**Interest by region:**
```bash
node scripts/trends.mjs interest-by-region "bitcoin" --geo US --resolution REGION
```

**Related topics:**
```bash
node scripts/trends.mjs related-topics "python programming" --geo US
```

**Related queries:**
```bash
node scripts/trends.mjs related-queries "python programming" --geo US
```

## Options reference

For full option details per command, see [reference.md](reference.md).

## Output

All commands output JSON to stdout. Parse the output to extract relevant data for the user. Present results in a readable format (tables, lists, summaries) based on context.

## Error handling

If Google rate-limits the request, the script retries with exponential backoff (up to 3 retries). If it still fails, inform the user and suggest waiting before retrying.
