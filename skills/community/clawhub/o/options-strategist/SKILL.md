---
name: Options Strategist
version: 1.0.2
description: "Analyze options chains, compute implied volatility rank, and select optimal multi-leg strategies based on market conditions via the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/options-strategist
---

# Options Strategist

Analyze options chains, construct multi-leg strategies, calculate Greek risk
metrics, and generate structured trade recommendations using real-time options
data from the Finskills API. Combines quantitative options theory with live
market data to evaluate opportunity and manage risk.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks which options strategy is best for a given outlook
- Wants to analyze a specific options contract or expiration
- Asks about Greeks (Delta, Gamma, Theta, Vega) for a position
- Wants to build a covered call, protective put, spread, straddle, or iron condor
- Asks about implied volatility, volatility skew, or IV rank
- Wants to calculate break-even points or max profit/loss for a trade

---

## Required Information

Resolve before starting:
1. **Underlying ticker** — e.g., `SPY`, `AAPL`
2. **Directional outlook** — Bullish / Bearish / Neutral / Volatile / Non-volatile
3. **Time horizon** — Days to target expiration (e.g., 30, 45, 60 DTE)
4. **Risk tolerance** — Defined-risk vs. undefined-risk strategies preferred
5. **Account level** — Options approval level (Level 1–4) if known

---

## Data Retrieval — Finskills API Calls

### 1. Real-Time Quote
```
GET https://finskills.net/v1/stocks/quote/{SYMBOL}
```
Extract: `price` (current underlying price), `volume`, `changePercent`

### 2. Options Chain
```
GET https://finskills.net/v1/stocks/options/{SYMBOL}
```
Extract from each contract:
- `strike`, `expiration`, `type` (call/put)
- `bid`, `ask`, `mid` (use mid for pricing)
- `impliedVolatility` (as decimal, multiply by 100 for %)
- `delta`, `gamma`, `theta`, `vega` (Greeks)
- `openInterest`, `volume`
- `inTheMoney` flag

### 3. Historical Price (for IV Rank / Realized Vol)
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=1y&interval=1d
```
Extract closing prices; compute:
- **HV20**: 20-day historical volatility (annualized standard deviation of daily returns × √252)
- **HV60**: 60-day historical volatility
- **Price range**: 52-week high/low for support/resistance context

---

## Analysis Workflow

### Step 1 — Market Context

From the quote data, note:
- Current price vs. 52-week range (where in range?)
- Recent price momentum (up/down trend)
- Sector/market context (risk-on/off environment)

### Step 2 — Volatility Analysis

Using the options chain and historical data:

**Implied Volatility Metrics:**
- **ATM IV**: Use implied volatility of the nearest-to-ATM straddle
- **IV Rank** (approximation): (Current ATM IV − 52w Low IV) / (52w High IV − 52w Low IV) × 100
  - IV Rank > 50: Elevated IV → consider selling premium
  - IV Rank < 30: Low IV → consider buying premium

**Volatility Skew:** Compare put IV vs. call IV at equidistant strikes
- Positive skew (puts more expensive): Market pricing downside protection
- Flat skew: Balanced two-directional uncertainty

**HV vs. IV Comparison:**
- IV > HV by > 20%: Premium selling opportunity (high vega)
- IV < HV: Premium buying may be cheap

### Step 3 — Strategy Selection Matrix

Based on outlook and volatility environment:

| Outlook | IV Environment | Recommended Strategy |
|---------|----------------|---------------------|
| Bullish | Low IV | Long Call, Bull Call Spread |
| Bullish | High IV | Cash-Secured Put (sell put), Bull Put Spread |
| Bearish | Low IV | Long Put, Bear Put Spread |
| Bearish | High IV | Bear Call Spread, Covered Call |
| Neutral (non-volatile) | High IV | Iron Condor, Short Strangle, Short Straddle |
| Neutral (volatile) | Low IV | Long Straddle, Long Strangle |
| Mildly Bullish | High IV | Covered Call, Bull Put Spread |
| Hedge existing long | Any | Protective Put, Collar |

Always prefer **defined-risk** strategies unless user explicitly requests undefined risk.

### Step 4 — Strike and Expiration Selection

**Expiration guidelines:**
- Income strategies (iron condor, credit spreads): 30–45 DTE (optimal theta decay)
- Directional strategies (debit spreads): 45–90 DTE (time buffer)
- Long options (earnings plays, catalysts): 1–2 weeks past the event

**Strike selection guidelines:**
- **Delta guide**: Long calls/puts: 0.30–0.50 delta for balanced risk/reward
- **Credit spreads**: Sell at 0.25–0.35 delta (≈ 70–75% probability of profit)
- **Iron condor wings**: 0.15–0.20 delta for outer strikes
- **ATM for straddles/strangles**: Use the nearest strike(s) to current price

### Step 5 — Strategy Metrics Calculation

For the recommended strategy (manual calculation using API data):

**For Debit Spreads (e.g., Bull Call Spread):**
```
Max Profit  = (Width of spread − Net debit) × 100
Max Loss    = Net debit × 100
Break-Even  = Long strike + Net debit paid
ROI at max  = Max Profit / Max Loss × 100%
```

**For Credit Spreads (e.g., Bull Put Spread):**
```
Max Profit  = Net credit received × 100
Max Loss    = (Width of spread − Net credit) × 100
Break-Even  = Short strike − Net credit received
Probability of Profit ≈ 1 − short put delta (as %)
```

**For Iron Condors:**
```
Max Profit  = Total net credit × 100
Max Loss    = (Width of widest wing − Total credit) × 100
Lower B/E   = Short put strike − Total credit
Upper B/E   = Short call strike + Total credit
```

**Greeks for the position:**
- Position Delta: Net sum of (leg delta × lots × sign)
- Position Theta: Net sum of (leg theta × lots × sign) — daily P&L from time decay
- Position Vega: Net sum — how much P&L changes per 1% IV move

### Step 6 — Risk Management Rules

Always state:
1. **Max loss cap**: Risk no more than 2–5% of portfolio per trade
2. **Exit at 50% max profit** (for credit strategies): Lock in profit, reinvest theta
3. **Exit at 2× max credit** (stop-loss): Close if spread doubles in value against you
4. **Adjust or roll if**: Underlying breaches short strike by more than 1 strike width
5. **Earnings blackout**: Close or roll before earnings if not intentionally an earnings play

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║     OPTIONS STRATEGY REPORT — {TICKER} ({DATE})     ║
╚══════════════════════════════════════════════════════╝

📌 UNDERLYING
  {Ticker}: ${price}  Change: {%}  Outlook: {Bullish/Bearish/Neutral}

📊 VOLATILITY ENVIRONMENT
  ATM IV:        {%}    IV Rank: {0–100} → {Low/Elevated/High}
  HV20:          {%}    HV60: {%}
  IV vs HV:      {premium/discount}
  Skew:          {Positive/Flat/Negative} — {one-line interpretation}
  Recommendation: {Sell premium / Buy premium}

🎯 RECOMMENDED STRATEGY: {STRATEGY NAME}

  Structure:
    Leg 1: {BUY/SELL} {qty} {TICKER} {Strike} {Exp} {CALL/PUT}  @ ${price}
    Leg 2: {BUY/SELL} {qty} {TICKER} {Strike} {Exp} {CALL/PUT}  @ ${price}
    [Additional legs if applicable]

  Net {Debit/Credit}: ${amount} per contract

  📐 Key Metrics:
    Max Profit:   ${amount} ({%} ROI)
    Max Loss:     ${amount}
    Break-Even:   ${price} [{direction} from current]
    Prob of Profit: {%}
    Days to Exp:  {DTE} days

  📉 Position Greeks (per contract):
    Delta: {value}  Gamma: {value}  Theta: {value}/day  Vega: {value}

  💼 Risk Management:
    ✓ Profit target: Close at 50% max profit (${amount} credit remaining)
    ✓ Stop-loss: Close if debit/spread reaches ${amount} (2× initial credit)
    ✓ Time exit: Close or roll at 21 DTE to avoid gamma risk

📋 ALTERNATIVE STRATEGIES CONSIDERED
  {Alternative 1}: {brief rationale for/against}
  {Alternative 2}: {brief rationale for/against}

⚠️ KEY RISKS
  • {Risk 1 — e.g., earnings announcement within DTE, sudden vol crush}
  • {Risk 2 — e.g., gap risk if undefined risk}
```

---

## Limitations

- Options chain data reflects last available bid/ask; actual fills may differ.
- IV Rank is approximated from available chain data, not full 52-week option history.
- Greeks calculations assume no dividends or early assignment unless noted.
- This is not personalized financial advice; consult a licensed advisor before trading options.
