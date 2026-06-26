---
name: poly-resolution-tracking
version: 1.0.2
description: Track Polymarket markets by monitoring their resolution data sources. Fetches event data, parses resolution criteria, assesses trackability, scrapes the resolution source for current state, and runs continuous terminal monitoring with color-coded alerts for score changes, leader changes, and market/data misalignment. Use when the user wants to track a specific Polymarket market's resolution, monitor resolution data sources, or set up alerts for market resolution changes.
metadata: {"openclaw": {"emoji": "🎯", "requires": {"bins": ["python3"]}}}
---

# Polymarket Resolution Tracker

Monitor a specific Polymarket market by tracking its resolution data source. Detect changes in the underlying data that could affect market resolution, compare with market prices, and alert on significant developments.

## Workflow

Execute the following 6 steps in order. Do not skip steps.

### Step 1: Ask User & Fetch Event

Ask the user which market they want to track. Accept a Polymarket URL or event slug.

Run the event fetcher to get market data:

```bash
python scripts/fetch_event.py <slug_or_url>
```

The script accepts either a full URL (`https://polymarket.com/event/...`) or just the slug. It returns JSON with event metadata and all sub-markets including prices, outcomes, and descriptions.

Present to the user:
- Event title and URL
- Number of sub-markets and top candidates by price
- Resolution date and time remaining
- Key excerpt from the description (resolution criteria)

### Step 2: Parse Resolution Criteria

Read the event description and extract:

1. **Resolution source URL** — the specific data source that determines the outcome
2. **Metric** — what is being measured (score, ranking, price, vote count, etc.)
3. **Resolution date/time** — when the check happens
4. **Conditions** — any special rules (tiebreakers, fallbacks, alphabetical ordering)
5. **Candidates** — list of possible outcomes from the sub-market questions

Present the extracted criteria clearly to the user for confirmation.

### Step 3: Assess Trackability

Evaluate whether the resolution data source can be automatically monitored. Use the framework in [references/trackability-framework.md](references/trackability-framework.md).

Check these four dimensions:

1. **Data source accessibility** — Is the URL public? Does it require JS rendering?
2. **Metric objectivity** — Is the metric quantitative/objective, or subjective?
3. **Data format** — JSON API, HTML table, PDF, video?
4. **Update frequency** — How often does the source data change?

Assign a trackability level:

| Level | Criteria | Action |
|-------|----------|--------|
| **Full** | JSON API + quantitative metric | Auto-monitor |
| **Partial** | HTML scrape needed | Monitor via script + WebFetch |
| **Manual** | Data accessible but not scrapable | Suggest manual schedule |
| **None** | Subjective/private/vague | Reject with explanation |

**Scan for non-trackable keywords** in the description: "discretion", "sole judgment", "opinion", "decides", "may determine", "subjective".

**If NOT trackable (Manual or None):**
- Explain specifically why automatic tracking is not possible
- For Manual: suggest a check schedule based on time to resolution
- For None: explain the subjective criteria and suggest monitoring market prices instead
- **Stop here** — do not proceed to Steps 4-6

**If trackable (Full or Partial):** proceed to Step 4.

### Step 4: Scrape Resolution Data

Fetch the current state of the resolution data source.

For known source types, use the scraper script:

```bash
python scripts/scrape_source.py --url <resolution_url> [--type arena_leaderboard|generic|auto]
```

The script auto-detects source type from the URL. Supported types:
- **arena_leaderboard**: Chatbot Arena / LMArena leaderboards (HTML table parsing)
- **generic**: Any HTML page with tables (extracts all tables)

If the script fails (JS-rendered content, bot detection), use **WebFetch** as fallback to get the rendered page content, then manually extract the relevant data.

Map the scraped data entries to market candidates:
- Match by organization/entity name
- For each candidate, record: rank, score/metric value, confidence interval (if available)
- Identify the current leader and gap to second place

### Step 5: Generate Snapshot & Compare

Present the initial state using the template from [references/output-template.md](references/output-template.md):

1. **Resolution data table** — ranked candidates with scores
2. **Market prices table** — candidates with current market probabilities
3. **Alignment analysis** — does the data leader match the market leader?
4. **Risk assessment:**
   - Leader gap (how close is the race?)
   - CI overlap (do confidence intervals overlap?)
   - Time to resolution
   - Market conviction (how certain is the market?)

Recommend a monitoring interval based on time to resolution:

| Time to Resolution | Recommended Interval |
|---|---|
| > 7 days | 360 min (6h) |
| 2-7 days | 120 min (2h) |
| 1-2 days | 60 min (1h) |
| < 24 hours | 30 min |
| < 6 hours | 15 min |

### Step 6: Start Monitoring Service

Ask the user if they want to start continuous monitoring. If yes, run:

```bash
python scripts/monitor.py --slug <slug> --interval <minutes>
```

The monitor runs in the foreground and continuously displays status updates:

- **Color-coded alerts** in the terminal:
  - `CRITICAL` (red): Leader changed — resolution outcome would flip
  - `WARNING` (yellow): Gap narrowed, CI overlap, significant score change
  - `ALERT` (magenta): Market price vs data misalignment
  - `INFO` (dim): No change, minor updates
- **State persistence**: Each cycle saves state to `~/polymarket-tracking/`
- **Delta comparison**: Compares current vs previous state each cycle
- **Graceful shutdown**: Ctrl-C saves final state and exits cleanly

Optional flags:
- `--once` — Run a single snapshot cycle and exit (no continuous loop)
- `--alert-log <file>` — Also write alerts as JSON lines to a log file
- `--state-dir <path>` — Custom state directory (default: `~/polymarket-tracking/`)

Reports and state files are saved to `~/polymarket-tracking/`.

## Troubleshooting

- **Script can't parse the resolution source page**: The page likely uses JS rendering. Use WebFetch to get the rendered content and manually extract data.
- **Market prices don't match candidate names**: Check the sub-market question format. The candidate name extraction handles "Will X have the best..." patterns. For unusual formats, manually specify the mapping.
- **No events found for slug**: Verify the slug matches exactly. Try searching via `https://gamma-api.polymarket.com/events?slug=<slug>` directly.
- **Monitor shows "No change" every cycle**: This is expected when the resolution data source hasn't updated. Consider increasing the interval to reduce unnecessary API calls.

## Reference Files

- [references/polymarket-api.md](references/polymarket-api.md) — Polymarket API endpoint documentation
- [references/trackability-framework.md](references/trackability-framework.md) — Trackability assessment criteria and non-trackable market handling
- [references/output-template.md](references/output-template.md) — Report templates and alert format specifications
