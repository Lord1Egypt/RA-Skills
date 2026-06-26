---
name: Market Breadth Analyzer
version: 1.0.2
description: "Measure US equity market breadth using advance/decline lines, percentage of stocks above moving averages, and new highs/lows via the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/market-breadth-analyzer
---

# Market Breadth Analyzer

Assess internal market health and regime using breadth indicators from the
Finskills API: advance/decline data, percentage of stocks above key moving
averages, new highs vs. new lows, and short volume. Identify divergences
between index price action and underlying breadth — the most reliable early
warning system for market tops and bottoms.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks "is this rally broad-based or narrow?"
- Wants to assess whether the market is healthy or deteriorating
- Asks about advance/decline ratio, new highs/lows, or breadth divergence
- Wants to understand if it's a good environment to be fully invested
- Asks "are we in a bull or bear market internally?"

---

## Data Retrieval — Finskills API Calls

### 1. Market Breadth Indicators
```
GET https://finskills.net/v1/free/market/breadth
```
Extract:
- `advancers`: number of stocks advancing
- `decliners`: number of stocks declining
- `unchanged`: number of stocks flat
- `new52wHigh`: stocks hitting 52-week highs
- `new52wLow`: stocks hitting 52-week lows
- `pctAbove200MA`: % of S&P 500 stocks trading above 200-day MA
- `pctAbove50MA`: % of S&P 500 stocks trading above 50-day MA
- `advanceVolume`: volume in advancing stocks
- `declineVolume`: volume in declining stocks

### 2. Market Summary (Index Price Context)
```
GET https://finskills.net/v1/market/summary
```
Extract: S&P 500 and Nasdaq current level, daily change, YTD performance

### 3. Short Volume (Market Stress Signal)
```
GET https://finskills.net/v1/free/market/short-volume-top
```
Extract: list of most heavily shorted stocks today (ratio of short vol to total vol)

---

## Analysis Workflow

### Step 1 — Advance/Decline Analysis

**Advance/Decline Ratio (ADR):**
```
ADR = advancers / decliners
```

| ADR | Signal |
|-----|--------|
| > 3.0 | Strong breadth — broad rally |
| 1.5–3.0 | Good breadth — healthy market |
| 0.75–1.5 | Mixed breadth — selective market |
| 0.25–0.75 | Weak breadth — narrow or declining market |
| < 0.25 | Very weak breadth — broad selloff |

**Volume-Weighted A/D:**
```
Volume A/D = advanceVolume / declineVolume
```
If Volume ADR > ADR: Distribution (smart money selling into rally) — bearish signal  
If Volume ADR < ADR: Accumulation (buying on pullbacks) — bullish signal

**Net New Highs/Lows:**
```
Net New Highs = new52wHigh - new52wLow
```
- Positive and growing: Strong bull market confirmation
- Negative while index is rising: Breadth divergence ⚠️ (early warning signal)
- Accelerating lows: Risk-off, potential broad decline

### Step 2 — Moving Average Participation

Classify market health by % of stocks above key moving averages:

**% Stocks Above 200-Day MA:**

| Level | Market Health |
|-------|--------------|
| > 70% | Bull market — broad participation |
| 50–70% | Moderate — mixed conditions |
| 30–50% | Weakening — selective market |
| < 30% | Bear market conditions |

**% Stocks Above 50-Day MA:**
- Leading indicator (shorter-term): signals shifts 2–4 weeks before 200MA
- When 50MA% drops below 40% while 200MA% still > 60%: caution flag ⚠️

### Step 3 — Breadth Divergence Detection

**Bullish Divergence** (oversold bounce setup):
- Index near 52-week lows
- But % stocks above 200MA is rising
- ADR improving
→ Signal: Internal strength building before price recovers

**Bearish Divergence** (distribution signal):
- Index near 52-week highs
- But % stocks above 200MA is falling
- New highs count shrinking (fewer stocks making highs)
- Net new lows expanding
→ Signal: Market becoming a narrow rally — top risk elevated

**Participation Narrowing:**
Calculate the ratio:
```
Narrowness Index = (leaders outperforming SPY with > 5% weight) / total S&P 500 constituents
```
If < 10 stocks are driving most of the index return, flag as "narrow rally" with high reversal risk.

### Step 4 — Short Volume Stress Signals

Top heavily-shorted stocks signal areas of market stress:
- If heavily shorted stocks are in key sectors: sector under significant bearish pressure
- High short ratio on recent IPOs or hyper-growth names: speculative froth reducing
- Short squeeze potential: stocks with high short ratio + positive news catalyst = snapback risk

### Step 5 — Overall Market Health Score

Score each dimension and compute composite:

| Dimension | Score (1–5) |
|-----------|------------|
| ADR (daily) | 5=very strong, 1=very weak |
| NetNewHighs | 5=expanding, 1=contracting |
| % > 200MA | 5= > 70%, 1= < 30% |
| % > 50MA | 5= > 65%, 1= < 35% |
| Vol. A/D Confirm | 5=confirmed, 3=neutral, 1=diverging |

**Market Health Score** = avg of 5 dimensions (scale 1–5)
- 4–5: Healthy bull market — stay invested
- 3–4: Moderate — selective stock picking
- 2–3: Weakening — raise cash, reduce risk
- 1–2: Unhealthy — defensive positioning

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║    MARKET BREADTH REPORT  —  {DATE}                 ║
╚══════════════════════════════════════════════════════╝

📊 MARKET INDEXES
  S&P 500:  {level}  {change}%  YTD: {ytd}%
  Nasdaq:   {level}  {change}%  YTD: {ytd}%
  Russell:  {level}  {change}%  YTD: {ytd}%

🩺 MARKET HEALTH SCORE: {X}/5  →  {HEALTHY / MODERATE / WEAKENING / UNHEALTHY}

📈 BREADTH DASHBOARD
  Advancers / Decliners:  {adv} / {dec}  (ADR: {ratio} — {Strong/Weak/Mixed})
  Volume Split:           {adv_vol}B advancing / {dec_vol}B declining
  Volume A/D Ratio:       {ratio} [{Accumulation/Distribution}]

  New 52-Week Highs:  {n}
  New 52-Week Lows:   {n}
  Net New Highs:      {+/-n}  [{Expanding/Contracting}]

  % Stocks > 200-Day MA: {%}  [{Bull/Moderate/Bear} zone]
  % Stocks > 50-Day MA:  {%}

🔍 DIVERGENCE CHECK
  Price vs. Breadth: {No divergence / BULLISH divergence / BEARISH divergence ⚠️}
  Detail: {Brief explanation of any divergence}
  Narrowing Rally Check: {Broad / Narrowing ⚠️}

📊 SHORT INTEREST SIGNALS
  Top Heavily Shorted Stocks Today:
    {TICKER}: {short_ratio}% short volume
    {TICKER}: {short_ratio}% short volume
  Signal: {Normal / Elevated stress in {sector}}

🎯 MARKET HEALTH ASSESSMENT
  Overall Verdict: {Healthy Bull / Mixed / Weakening / Risk-Off}

  Implication for Investors:
    ✅ {What to do if healthy}  OR
    ⚠️ {What to watch / reduce if weakening}

  Key indicator to monitor: {The metric most likely to confirm direction}
```

---

## Limitations

- Breadth indicators work best over 5–20 day windows; single-day readings can be noisy.
- % above MA data depends on the data provider's stock universe (may cover S&P 500 constituents only).
- Short volume data from the prior trading day (T+1 reporting lag for official FINRA data).
