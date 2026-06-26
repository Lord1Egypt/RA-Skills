# Skill: Catalyst Edge

**Purpose:** High-conviction stock opportunities + JB's retirement portfolio tracker.

**Trigger:** Weekly (Sunday 10 AM CDT via cron) or on demand.

---

## Part 1 — Stock Scanning

### What It Looks For

| Pattern | Description | Conviction |
|---------|-------------|------------|
| Earnings Surprise | Beat estimates, raised guidance | 🟡-🟢 |
| Catalyst Event | FDA approval, contract win, merger | 🟡-🟠 |
| Technical Breakout | Volume surge, breakout above resistance | 🟡 |
| Insider Buying | Executives buying heavily | 🟡 |
| Sector Rotation | Money flowing into our themes | 🟢 |

### Target Themes
- Healthcare/RCM tech
- AI/automation
- Dividend payers
- Growth with value

### Quality Criteria
- Score ≥75 = alert JB immediately (Discord DM)
- Score 60-75 = include in weekly summary
- Score <60 = skip
- Always include source + date

### Output Format
```
🎯 CATALYST EDGE — [Date]

[Stock] — [Ticker]
Catalyst: [What it is]
Conviction: [🔵🟡🟢🟠]
Score: [0-100]
Thesis: [1-sentence why]

Watch List:
1. [Stock] - [reason]
2. [Stock] - [reason]
```

---

## Part 2 — Quarterly Financial Review (Every 3 Months)

**Trigger:** January, April, July, October — first Sunday of the month at 10 AM CDT.

### Steps
1. **Read the current state:**
   - `/workspace/skills/catalyst-edge/FIRE_MODEL.md` — current numbers
   - `/workspace/skills/catalyst-edge/PORTFOLIO_ANALYSIS.md` — portfolio
   - `/workspace/memory/life-archive.md` — personal context

2. **Post to Discord `#retirement-edge`:**
   ```
   📊 QUARTERLY FINANCIAL REVIEW — [Month Year]
   
   Net Worth: $XX,XXX (vs $XX,XXX last quarter — +/- $X,XXX)
   This Quarter: [what changed — new savings, paid down debt, market movement]
   
   FIRE Progress: [X years to FI / age XX target]
   Next Quarter Goals:
   • [Action 1]
   • [Action 2]
   
   Action Items Due:
   • [Stale items from FIRE_MODEL.md priority list]
   ```

3. **Update the files:**
   - Note any account changes in PORTFOLIO_ANALYSIS.md
   - Flag any action items that are overdue
   - Log the quarter's net worth in a table at the bottom of FIRE_MODEL.md

4. **Alert JB if:**
   - A major milestone was hit (e.g., hit $100K, mortgage paid off early)
   - An action item is 60+ days overdue
   - Net worth dropped >15% (market downturn check)

### Quality Standards
- Keep it to 10 lines or less in Discord
- Full details go in the .md files
- Numbers over opinions always

---

---

## Part 3 — FIRE Pipeline (Weekly)

**Trigger:** Runs alongside the weekly stock scan (Sunday 10 AM CDT).

### What It Does
1. Reads RSI results from `/workspace/skills/catalyst-edge/stock_scanner/last_scan.json`
2. Applies FIRE model thresholds from `/workspace/skills/catalyst-edge/fire_config.json`
3. Calculates signals: STRONG BUY / BUY / HOLD / WEAK / AVOID / TAKE PROFIT
4. Posts a formatted signal report to Discord `#retirement-edge`

### FIRE Signal Logic
| RSI Range | Signal | Action |
|-----------|--------|--------|
| ≤ 30 (core) / ≤ 35 (income) | 🟢 STRONG BUY | FI deployment window |
| 30-40 | 🟢 BUY | Accumulation candidate |
| 40-60 | 🟡 HOLD | No action |
| 60-70 | 🟠 WEAK | Partial profit taking |
| ≥ 70 (core) / ≥ 75 (income) | 🔴 TAKE PROFIT / AVOID | Book gains; not an entry |

### Core Principle
VT/VTI/QYLD at RSI ~29-30 simultaneously = **historically rare cluster bottom**. When 2+ core holdings hit RSI < 30 → FI deployment signal. This has happened <5 times in the past 5 years.

### Run the Pipeline
```bash
cd /workspace/skills/catalyst-edge/stock_scanner
python3 scan_once.py  # runs fresh scan
python3 ../fire_pipeline.py  # applies FIRE logic + posts to Discord
```

### Files
- `/workspace/skills/catalyst-edge/SKILL.md` (this)
- `/workspace/skills/catalyst-edge/FIRE_MODEL.md` — current numbers
- `/workspace/skills/catalyst-edge/PORTFOLIO_ANALYSIS.md` — portfolio details
- `/workspace/skills/catalyst-edge/HISTORICAL_PICKS.md` — past picks + performance
- `/workspace/skills/catalyst-edge/fire_config.json` — FIRE threshold config
- `/workspace/skills/catalyst-edge/fire_pipeline.py` — signal engine
- `/workspace/skills/catalyst-edge/stock_scanner/last_scan.json` — latest scan results
