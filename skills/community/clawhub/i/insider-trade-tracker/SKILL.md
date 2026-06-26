---
name: Insider Trade Tracker
version: 1.0.2
description: "Track and interpret SEC Form 4 insider buying and selling activity across US-listed equities using the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/insider-trade-tracker
---

# Insider Trade Tracker

Monitor SEC-reported insider buying and selling activity using the Finskills API
SEC endpoints. Surfaces unusual insider transactions, cluster buying signals,
and corporate officer behavior — one of the most reliable alternative data
signals for identifying high-conviction investment opportunities.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks "is management buying their own stock?"
- Wants to check recent insider transactions for a specific company
- Asks for unusual insider buying or selling activity across the market
- Wants to understand what Form 4 filings mean
- Uses insider activity as part of their investment screening process

---

## Background — Insider Trading Signals

Corporate insiders (officers, directors, 10%+ shareholders) must file Form 4 with
the SEC within 2 business days of any transaction. Key signal principles:

**Insider Buying Signals:**
- Cluster buying (3+ insiders buying within 30 days): High conviction ⭐⭐⭐
- CEO/CFO buying (most informed executives): Strongest signal ⭐⭐⭐
- Open-market purchase (not options exercise): More meaningful ⭐⭐
- New director buying shortly after joining: Board confidence signal ⭐⭐
- Buying at or near multi-year lows: Turnaround signal ⭐⭐⭐

**Insider Selling Signals (interpret carefully):**
- Insiders sell for many reasons (diversification, tax planning, personal needs)
- Cluster selling by multiple insiders simultaneously: Warning signal ⚠️
- CEO/CFO selling > 50% of holdings: Significant concern 🚨
- Selling before known negative catalyst: Potential information advantage (SEC investigates) 🚨
- Pre-planned 10b5-1 sales: Less meaningful (scheduled in advance)

---

## Data Retrieval — Finskills API Calls

### 1. Symbol-Specific Insider Trades
```
GET https://finskills.net/v1/free/sec/insider-trades/{SYMBOL}
```
Extract:
- `filerName`: insider's name
- `filerTitle`: role (CEO, CFO, Director, 10% owner, etc.)
- `transactionType`: Purchase (P) or Sale (S) or gift (G) or option exercise (A)
- `transactionDate`: date of transaction
- `shares`: number of shares transacted
- `pricePerShare`: transaction price
- `totalValue`: total dollar value of transaction
- `sharesOwnedAfter`: total shares owned after transaction
- `filingDate`: date filed with SEC

### 2. SEC EDGAR Filings (for context)
```
GET https://finskills.net/v1/free/sec/filings/{CIK}
```
(If the company's CIK number is known)  
Extract: recent 8-K, 10-Q, 10-K filings to provide context for insider timing

---

## Analysis Workflow

### Step 1 — Transaction Filtering

Filter the insider trade feed:
1. **Remove option exercises** (transactionType = 'A'): These are pre-planned, not discretionary
2. **Remove gifts** (transactionType = 'G'): Non-economic, planning-related
3. **Focus on Open-Market Purchases ('P') and Sales ('S')**: True economic decisions

### Step 2 — Insider Hierarchy Weighting

Assign signal weight by filer title:

| Role | Signal Weight |
|------|--------------|
| CEO | ⭐⭐⭐ Highest |
| CFO | ⭐⭐⭐ Highest |
| President / COO | ⭐⭐⭐ High |
| Director (Board) | ⭐⭐ Medium |
| VP / Other Officer | ⭐⭐ Medium |
| 10% Shareholder | ⭐ Lower (may have strategic not informational motivation) |

### Step 3 — Cluster Signal Detection

**Cluster Buy Signal** (high conviction):
- ≥ 3 distinct insiders purchasing within a 30-day window
- At least one C-suite (CEO/CFO) included
- Total purchase value > $500K combined
→ **Flag: CLUSTER BUY ⭐⭐⭐**

**Cluster Sell Signal** (caution):
- ≥ 3 distinct insiders selling within a 30-day window (excluding 10b5-1)
- Combined shares represent > 20% of their aggregate holdings
→ **Flag: CLUSTER SELL ⚠️**

**Size Signal:**
- Purchase > $1M by a single insider: High conviction
- Purchase > $5M: Exceptional conviction

### Step 4 — Transaction Context Analysis

Compare transaction price to current stock price:
```
Unrealized Gain/Loss % = (current_price - transaction_price) / transaction_price × 100
```

If CEO bought at $X and stock is still near $X: Insider is "underwater" → management's money at risk too (alignment signal).

If CEO bought and stock has already risen 30%: Signal may be partly priced in, but confirms thesis.

### Step 5 — Trend Summary

Compute rolling 90-day stats:
- Count of buy transactions vs. sell transactions
- Net buy/sell dollar value
- Number of unique insiders transacting

**Net Insider Sentiment Score:**
```
Score = (buy_transactions × buy_value) / max(sell_transactions × sell_value, 1)
```
- Score > 2.0: Net buying pressure — bullish insider signal
- Score 0.5–2.0: Balanced / neutral
- Score < 0.5: Net selling — caution

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║    INSIDER TRADE REPORT — {TICKER}  ({DATE})        ║
╚══════════════════════════════════════════════════════╝

📌 INSIDER SENTIMENT (Last 90 Days)
  Net Sentiment:   {BULLISH / NEUTRAL / CAUTIOUS}
  Buy Transactions:  {n}  ($${total_value}M)
  Sell Transactions: {n}  ($${total_value}M)
  Unique Insiders:   {n} buyers / {n} sellers

{CLUSTER BUY SIGNAL ⭐⭐⭐}  OR  {CLUSTER SELL WARNING ⚠️}  if triggered

📋 RECENT TRANSACTIONS (Last 90 Days, open-market only)
  Date        Insider                Title    Type     Shares    Price    Value
  2025-04-05  John Smith             CEO      BOUGHT   50,000    $42.10   $2.1M
  2025-03-28  Jane Doe               CFO      BOUGHT   15,000    $39.80   $597K
  2025-03-10  Robert Johnson         Director BOUGHT    8,000    $41.20   $330K
  2025-02-15  Alice Chen             VP Ops   SOLD     12,000    $44.50   $534K
  ...

  [Only showing open-market purchases and sales, excluding option exercises and gifts]

📊 SIGNAL ANALYSIS
  Key Buy Signal:   {Date}: {Name} (CEO/CFO) purchased ${amount}M at ${price}
                    → {Interpretation / context — near 52-week low? Vs. current price?}

  Ownership Context: After purchase, CEO holds {shares} shares (${value} at current price)
                    → {high/medium/low} skin-in-the-game vs. annual compensation

  Price Action Since:  Stock is {+/-}% from average insider purchase price

⚠️ CAVEATS
  • {Any pre-planned 10b5-1 sales noted in filings}
  • {Any concurrent SEC investigation or litigation}
  • {Acquisition-related transactions to exclude}

📈 OVERALL VERDICT
  Insider Signal: {STRONG BUY / MILD BUY / NEUTRAL / MILD CAUTION / CAUTION}
  Confidence:     {High / Medium / Low}
  Rationale:      {2 sentence summary of why}
```

---

## Limitations

- Form 4 filings can be delayed up to 2 business days; very recent transactions may not appear.
- Insider selling is inherently ambiguous — always consider alongside valuation and fundamentals.
- This skill does not identify illegal insider trading; all transactions shown are SEC-reported.
- CIK numbers must be obtained from SEC EDGAR for company-specific filing lookups.
