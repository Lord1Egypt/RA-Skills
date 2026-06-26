---
name: paradex-risk-guardian
description: >
  Real-time risk monitoring, margin analysis, and protective alerts for Paradex
  trading accounts and vaults. Synthesizes account summary, positions, market data,
  and funding rates into actionable risk metrics — liquidation distance, portfolio
  concentration, margin utilization, exposure heatmaps, and daily P&L attribution.
  Use this skill whenever the user asks about their risk on Paradex, margin health,
  liquidation levels, portfolio exposure, drawdown, how much they can lose, position
  sizing, or when they say things like "am I safe", "check my risk", "how close am I
  to liquidation", "what's my exposure", "should I be worried", "risk report", or
  any question about the safety of their Paradex positions or vault positions.
  Also trigger for any request to monitor or set alerts on Paradex account health.
---

# Paradex Risk Guardian

Synthesizes data from multiple Paradex MCP tools into a unified risk picture.
Answers the question: "Am I safe?" with specific numbers and actionable recommendations.

## Available MCP Tools (data sources)

| Tool | Risk data it provides |
|---|---|
| `paradex_vault_account_summary` | Margin usage, total equity, maintenance margin, available balance |
| `paradex_vault_positions` | Open positions, unrealized PnL, entry prices, sizes |
| `paradex_vault_balance` | Cash available for new positions |
| `paradex_market_summaries` | Current prices, 24h changes, funding rates, volatility context |
| `paradex_markets` | Position limits, margin params, price bands width |
| `paradex_bbo` | Current prices for mark-to-market |
| `paradex_funding_data` | Funding cost/income over time |
| `paradex_orderbook` | Liquidity available for exit |

## Risk Assessment Framework

### 1. Account Health Check

Pull `paradex_vault_account_summary` and compute:

- **Margin utilization**: used_margin / total_equity × 100%
  - <50%: Healthy (green)
  - 50-75%: Caution (yellow)
  - 75-90%: Warning (orange)
  - >90%: Danger — liquidation risk (red)

- **Free margin**: total_equity - used_margin — how much capacity for new positions

- **Liquidation buffer**: estimate distance to liquidation as a percentage price move
  - For each position: how much can the market move against you before maintenance margin is breached?
  - Report the tightest (most dangerous) position

### 2. Position Analysis

Pull `paradex_vault_positions` and analyze:

**Concentration risk:**
- Calculate notional value of each position
- Compute percentage of total exposure per market
- Flag if any single position is >40% of total exposure
- Flag if top 2 positions are >70% of total exposure

**Directional bias:**
- Sum net delta across all positions
- Report as: "Net long $X notional" or "Net short $X notional"
- Compare net exposure to account equity for effective leverage

**Unrealized P&L:**
- Total unrealized P&L across all positions
- Unrealized P&L as percentage of equity
- Identify worst-performing position (biggest drag)
- Identify best-performing position

### 3. Funding Cost Analysis

For each open position, estimate funding cost:

1. Get current funding rate from `paradex_market_summaries`
2. Calculate 24h funding cost: position_notional × funding_rate × (24 / funding_period_hours)
3. Annualize: daily_cost × 365
4. Sum across all positions for total portfolio funding cost/income

**Report:**
- Total daily funding cost/income
- Per-position funding breakdown
- Flag positions where funding is >0.1% daily (costly to hold)

### 4. Liquidity Risk

For each position, check exit liquidity via `paradex_orderbook`:

- Can the full position be exited within 1% slippage?
- What percentage of the position could be exited at current depth?
- Flag illiquid positions where orderbook depth < 50% of position size within 2%

### 5. Stress Testing (Scenario Analysis)

Run simple what-if scenarios:

**Price shock scenarios:**
- -5% across all markets: estimate portfolio P&L impact
- -10% across all markets: estimate P&L + check if margin call triggered
- -20% across all markets: extreme scenario

**Calculation for each scenario:**
For each position: `position_size × price_change × direction_multiplier`
Sum to get portfolio impact, subtract from equity, check against maintenance margin.

**Correlation stress:**
If user holds multiple crypto positions, note that crypto assets are highly correlated.
A -10% BTC move often means -12 to -20% in alts. Apply asset-specific beta adjustments:
- BTC: 1.0x
- ETH: ~1.2x
- Alts: ~1.5-2.0x

### 6. Daily P&L Attribution

Break down the day's P&L into components:

- **Trading P&L**: unrealized P&L changes from position mark-to-market
- **Funding P&L**: funding payments received or paid
- **Fee P&L**: trading fees incurred (if data available)
- **Net P&L**: sum of above

## Risk Score

Compute an overall risk score (1-10) based on:

| Factor | Weight | Score 1 (Low Risk) | Score 10 (High Risk) |
|---|---|---|---|
| Margin utilization | 30% | <30% | >90% |
| Position concentration | 20% | No position >25% | Single position >60% |
| Effective leverage | 20% | <2x | >10x |
| Funding cost (daily) | 15% | Net positive | >0.2% of equity |
| Liquidity risk | 15% | All positions liquid | Major positions illiquid |

**Weighted sum → Risk Score 1-10**

## Output Format

### Quick Risk Check
```
## Risk Check — [Account/Vault]

🟢/🟡/🟠/🔴 **Risk Score: X/10**

| Metric | Value | Status |
|---|---|---|
| Margin Used | X% | 🟢/🟡/🟠/🔴 |
| Free Margin | $X | — |
| Net Exposure | $X (Xx leverage) | 🟢/🟡/🟠/🔴 |
| Largest Position | MARKET (X% of exposure) | 🟢/🟡 |
| Unrealized P&L | $X (X% of equity) | — |
| Daily Funding Cost | $X | — |
| Tightest Liquidation | MARKET @ $X (X% away) | 🟢/🟡/🟠/🔴 |

### Recommendations
- [specific, actionable items if risk is elevated]
```

### Full Risk Report
```
## Full Risk Report — [Account/Vault]

### Account Overview
[equity, margin, free capital]

### Position Breakdown
[table of all positions with notional, direction, P&L, liquidation distance]

### Concentration Analysis
[exposure distribution chart/table]

### Funding Analysis
[per-position funding costs, net daily cost]

### Stress Test Results
[scenario table: -5%, -10%, -20% impact]

### Liquidity Assessment
[exit capacity per position]

### Recommendations
[prioritized list of risk-reducing actions]
```

## Safety Principles

- When risk score is ≥7, lead the response with the risk warning before any other analysis
- Never suggest increasing position size when margin utilization is >60%
- Always note that liquidation estimates are approximate — actual liquidation depends on
  mark price which can differ from last traded price
- Stress test results assume instantaneous price moves — real liquidations can cascade
- This is risk analysis, not financial advice
- Recommend the user verify critical numbers on the Paradex UI before acting

See [margin-model.md](references/margin-model.md) for detailed Paradex margin formulas and risk scoring methodology.
