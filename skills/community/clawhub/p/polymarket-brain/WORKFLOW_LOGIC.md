# Polymarket Brain — Workflow Logic v1.2

## Overview

This skill orchestrates a complete geopolitical → macroeconomic → Polymarket trading analysis workflow.

---

## Workflow Steps

### Step 1: Fetch CNBC News
- **Skill:** `cnbc-geopolitics-fetcher`
- **Action:** Fetches 5 latest CNBC geopolitics articles
- **Discord:** ✅ Sends raw article data (title, URL, market impact, hard facts) one-by-one
- **History:** Skips duplicates (checks `sent_urls.txt`)
- **No News:** Sends notification "No new articles found" and stops

---

### Step 2: Classify News
- **Logic:** Keyword matching on title + content
- **Categories:**
  - **Geopolitics:** iran, israel, war, strike, missile, hormuz, oil, regime
  - **Macroeconomics:** fed, rate, dollar, forex, inflation, employment
  - **Both:** Mixed keywords from both categories
- **Output:** Classification count for routing to analysts

---

### Step 3: Run Analyst Skills
- **Geopolitics articles** → Run `geopolitics-expert`
  - Output: Conflict duration, scenarios, pathways
- **Macro articles** → Run `the-fed-agent`
  - Output: Fed policy, inflation transmission, treasury impact
- **Mixed articles** → Run BOTH analysts
- **Discord Header:** Dynamic based on classification
  - "Analyst: geopolitics-expert"
  - "Analyst: the-fed-agent"
  - "Analysts: geopolitics-expert + the-fed-agent"

---

### Step 4: Polymarket Analyst
- **Skill:** `polymarket-analyst`
- **Action:** Fetches 10 Polymarket markets (30-70% odds)
- **Filter:** Balanced markets (not extreme odds)
- **Output:** Market title, odds, resolution date, URL

---

### Step 5: Discord Delivery (One-by-One)
- **Format:** Each market as separate complete message
- **Content:**
  - Market title
  - Resolution date
  - Market odds
  - Expert probability (derived from analyst)
  - Recommendation (✅ Strong / ⚠️ Fair / ⚖️ Fair Value)
  - Clickable link
- **Summary:** Trading recommendations table

---

## No News Handling

If Step 1 finds no new articles:
1. **Stop workflow** — Don't run analysts on stale data
2. **Send ONE notification:** "No new CNBC articles found"
3. **Exit cleanly** — Don't send empty tables

---

## Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Modular** | Each skill is independent, composable |
| **Complete** | Each skill delivers to Discord end-to-end |
| **One-by-One** | No chopped messages — complete delivery |
| **Dynamic** | Analyst header based on classification |
| **Graceful** | Clear notification when no news found |

---

## Version History

- **v1.2** (2026-03-17): One-by-one delivery + dynamic analyst header
- **v1.1**: Classification + analyst routing
- **v1.0**: Initial workflow orchestration

---

## Files

- `scripts/run_polymarket_brain.py` — Main orchestrator
- `../cnbc-geopolitics-fetcher/scripts/fetch_cnbc_geopolitics.py` — News fetcher
- `../geopolitics-expert/scripts/run_geopolitics_expert.py` — Geopolitics analyst
- `../the-fed-agent/scripts/run_the_fed_agent.py` — Macro analyst
- `../polymarket-analyst/scripts/poll_polymarket_markets.py` — Market fetcher

---

**Author:** @rafimchmd  
**License:** MIT
