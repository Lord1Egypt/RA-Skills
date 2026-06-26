# Polymarket-Brain Workflow — Correct Implementation

**Version:** 1.3 (User-specified workflow)
**Date:** 2026-03-18

---

## Core Workflow (5 Steps)

### Step 1: Fetch CNBC News
**Skill:** `cnbc-geopolitics-fetcher`
- Runs first, always
- Fetches latest CNBC geopolitics/macro articles
- Posts articles to Discord (one-by-one, complete messages)
- Tracks sent URLs in `references/sent_urls.txt` to avoid duplicates
- **Output:** Articles stored in memory files (`memory/YYYY-MM-DD-cnbc-geopolitics.md`)

**No News Handling:**
- If all URLs already in history → Output: "No new articles to post (all already sent before)"
- **Stop workflow** → Don't run analysts on stale data

---

### Step 2: Classify News Type
**Decision Logic:**

| News Content | Classification | Router |
|--------------|----------------|--------|
| Military strikes, troop movements, infrastructure attacks, chokepoint disruptions | **Geopolitics** | → `geopolitics-expert` |
| Fed decisions, inflation data, employment reports, Treasury yields, currency markets | **Macroeconomics/Fed** | → `the-fed-agent` |
| Mixed (war + markets, oil + Fed, Iran + Treasury) | **Both** | → Run both skills |

**Classification Keywords:**

**Geopolitics:**
- iran, israel, russia, ukraine, china, middle east
- war, conflict, strike, missile, drone, military
- hormuz, strait, oil, crude, energy, barrel
- sanctions, tariff, invasion, regime

**Macroeconomics/Fed:**
- fed, powell, rate, interest, inflation, cpi
- treasury, yield, bond, dollar, forex, currency
- employment, payroll, unemployment, pmi, sentiment
- recession, nber, gdp, economic

---

### Step 3: Run Analyst Skill(s)

#### If Geopolitics → `geopolitics-expert`
**Input:** Article URL(s) from Step 1

**Output:** 5-section analysis:
1. Conclusion (conflict assessment)
2. Economic/Commodity Impact (oil, gas, supply chains)
3. Commodity Trading Odds (long/short positions)
4. War Duration Categorization (short% vs forever%)
5. Termination Scenarios (ranked by probability)

**Frameworks Applied:**
- Strategic Gravity (forever war indicators)
- Five Pathways (conflict termination)
- Hormuz Siege (chokepoint weaponization)
- IRGCistan (post-theocratic dynamics)

#### If Macroeconomics/Fed → `the-fed-agent`
**Input:** Article URL(s) from Step 1

**Output:** 4-section professional Fed analysis:
1. **Conclusion** — Policy stance, key decision metrics, policy bind
2. **Economic/Commodity Impact** — Rate decision, inflation, growth, oil, employment, expectations
3. **Commodity Trading Odds** — USD, EUR/USD, GBP/USD, gold, oil, Treasury recommendations
4. **What's Next Can Be Happened?** — Ranked scenarios by likelihood (Hold+Pivot, Stagflation, Recession, Inflation Breakout)

---

### Step 4: Combined Analysis → `polymarket-analyst`
**Input:** Results from Step 3 (geopolitics-expert OR the-fed-agent OR both)

**CRITICAL:** Polymarket-analyst does **NOT** fetch news randomly. It uses the combined analyst output to:
1. Extract key topics from analyst results (e.g., "Iran regime fall", "Fed rate cut", "Oil $100+")
2. Fetch active Polymarket markets matching those **specific topics**
3. Filter for balanced odds (30-70% probability = trading opportunities)
4. Format as individual messages with all fields

**This is topic-driven, not random fetching.**

---

### Step 5: Discord Output (One-by-One Format)

**Message Sequence:**
1. **Header** — Date, classification, analyst(s) used
2. **Classification Details** — Which articles routed to which analyst
3. **Analyst Summary** — Combined outputs from geopolitics-expert + the-fed-agent
4. **Market 1/N** — Complete message with all fields + link
5. **Market 2/N** — Complete message with all fields + link
6. **Market 3/N** — Complete message with all fields + link
7. **Market 4/N** — Complete message with all fields + link
8. **Market 5/N** — Complete message with all fields + link
9. **Trading Summary** — Recommendations table + key risks

**Format Rules:**
- **One-by-one delivery** — Each market is a separate complete message (not chopped)
- **Market:** Full market title with clickable URL
- **Resolution Date:** Date + time from now (~X months)
- **Market Odds:** Real-time Polymarket odds (Yes %)
- **Expert Probability:** Derived from analyst output (geopolitics-expert or the-fed-agent)
- **Recommendation:** Emoji + verdict + rationale anchored to framework

**Emoji Legend:**
- ✅ Strong conviction (market vs. expert gap >20%)
- ⚠️ Fair/Lean (market vs. expert gap 10-20%)
- ⚖️ Fair Value (market vs. expert gap <10%)

---

## Dynamic Analyst Header

The header dynamically shows based on classification:

| Classification | Header Display |
|---------------|----------------|
| **Geopolitics only** | "Analyst: geopolitics-expert" |
| **Macroeconomics only** | "Analyst: the-fed-agent" |
| **Mixed** | "Analysts: geopolitics-expert + the-fed-agent" |

---

## File Structure

```
skills/polymarket-brain/
├── SKILL.md                    # This documentation
├── scripts/
│   ├── run_polymarket_brain.py # Main orchestrator script (needs path fix)
│   └── send_discord_summary.py # Discord delivery
└── references/
    ├── config.md               # Shared configuration (webhook, API keys)
    └── workflow.md             # This file (correct workflow logic)
```

---

## Dependencies

| Skill | Role | Required |
|-------|------|----------|
| `cnbc-geopolitics-fetcher` | News source + Discord delivery | ✅ Yes (Step 1) |
| `geopolitics-expert` | Conflict analysis | ⚠️ Conditional (geopolitics news) |
| `the-fed-agent` | Macro/Fed analysis | ⚠️ Conditional (macro news) |
| `polymarket-analyst` | Topic-driven market matching | ✅ Yes (Step 4) |

---

## Critical Notes (Don't Forget)

1. **polymarket-analyst is NOT random** — It uses analyst topics from Step 3, not random news fetching
2. **Classification drives routing** — Geopolitics → geopolitics-expert, Macro → the-fed-agent, Mixed → both
3. **No news = stop workflow** — Don't run analysts on stale/already-sent data
4. **One-by-one Discord delivery** — Each market is a complete separate message, not chopped or batched
5. **Expert probability comes from analysts** — Not from Polymarket API, from geopolitics-expert or the-fed-agent output

---

## Example Flow

**Article:** "Treasury yields edge lower as investors weigh rising oil price, Iran attacks and looming Fed decision"

1. **Fetch:** cnbc-geopolitics-fetcher gets article
2. **Classify:** MIXED (Iran war = geopolitics + Treasury/Fed = macro)
3. **Route:** Run BOTH geopolitics-expert + the-fed-agent
4. **Combine:** Merge both analyst outputs
5. **Match:** polymarket-analyst finds markets on "Iran regime", "Fed rate", "Oil price"
6. **Deliver:** One-by-one Discord messages with expert probabilities from both analysts
