# Trackability Assessment Framework

## Overview

Not all Polymarket markets can be automatically tracked for resolution. This framework defines how to assess whether a market's resolution data source can be monitored programmatically.

## Trackability Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **Full** | JSON API + quantitative metric | Auto-monitor with `monitor.py` |
| **Partial** | HTML scrape needed | Monitor via script + WebFetch |
| **Manual** | Data accessible but not machine-readable | Suggest manual check schedule |
| **None** | Subjective, private, or vague criteria | Reject with explanation |

## Assessment Checklist

Evaluate these four dimensions to determine trackability:

### 1. Data Source Accessibility

- **Is the URL public?** Must be accessible without authentication.
- **Does it require JavaScript rendering?** If yes, WebFetch may work but direct HTTP fetch won't.
- **Is the data behind a paywall?** Paywalled sources are Manual or None.
- **Does the URL return a stable, parseable response?** Check for bot detection, CAPTCHAs, or rate limiting.

### 2. Metric Objectivity

- **Is the metric quantitative?** Score, ranking, price, count → Trackable.
- **Is the metric categorical?** Yes/No, binary outcome from official source → Trackable.
- **Is the metric subjective?** "At discretion of", "sole judgment" → Not trackable.

### 3. Data Format

- **JSON API** → Full trackability (best case)
- **HTML table** → Partial trackability (parse with scrape_source.py)
- **HTML embedded JSON** (Next.js `__NEXT_DATA__`) → Partial trackability
- **PDF/image/video** → Manual only
- **Dynamic JS-rendered** (no static data in source) → Requires WebFetch

### 4. Update Frequency

- **Real-time / frequent updates** (leaderboards, prices) → Good for monitoring
- **Infrequent updates** (quarterly reports) → Longer intervals
- **One-time event** (election result, announcement) → Single check at event time

## Non-Trackable Market Indicators

Scan the market description for these keywords that signal non-trackability:

### Red-flag keywords (auto-reject)
- "discretion"
- "sole judgment"
- "opinion"
- "decides"
- "may determine"
- "at the discretion of"
- "UMA oracle"
- "subjective"

### Yellow-flag keywords (manual review needed)
- "at the time of"
- "based on reporting"
- "according to sources"
- "media reports"

## Handling Non-Trackable Markets

When a market is assessed as non-trackable:

1. **Explain why** — clearly state which criteria failed
2. **Suggest manual monitoring** — recommend a check schedule based on resolution date:
   - > 30 days: Weekly manual check
   - 7-30 days: Every 2-3 days
   - < 7 days: Daily
   - < 24 hours: Every few hours
3. **Identify what can be tracked** — even if the resolution source isn't scrapable, related data (market prices, news) may still be monitorable
4. **Stop the workflow** — do not proceed to Steps 4-6

## Common Resolution Source Patterns

### Chatbot Arena / LMArena
- **Type:** HTML table (leaderboard)
- **Trackability:** Full (HTML scraping works)
- **URL patterns:** `lmarena.ai/*`, `arena.ai/*`
- **Metric:** Arena Score (Elo rating)
- **Script:** `scrape_source.py --type arena_leaderboard`

### Government / Official Statistics
- **Type:** Usually PDF or HTML
- **Trackability:** Partial to Manual
- **Metric:** Various numeric indicators

### Sports / Election Results
- **Type:** Various APIs and HTML
- **Trackability:** Depends on source
- **Metric:** Scores, vote counts, standings

### Cryptocurrency Prices
- **Type:** JSON APIs widely available
- **Trackability:** Full
- **Metric:** Price in USD/USDT

### Corporate Announcements
- **Type:** Press releases, SEC filings
- **Trackability:** Manual (event-driven, not periodic)
- **Metric:** Binary (announced or not)
