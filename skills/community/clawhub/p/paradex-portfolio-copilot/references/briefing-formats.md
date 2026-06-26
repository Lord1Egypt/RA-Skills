# Briefing Format Templates

Detailed output templates for each of the 6 briefing types defined in the Portfolio Copilot skill.
Each template includes placeholder variables (in `{curly_braces}`) and a realistic example.

---

## 1. Quick Status Template

**Trigger phrases:** "How am I doing?", "Quick update", "Status"

### Template

```
Your Paradex account has ${equity} equity with {position_count} open position(s).
Unrealized P&L: {unrealized_pnl_sign}${unrealized_pnl_abs} ({unrealized_pnl_pct}%).
Largest position: {largest_market} at ${largest_notional} notional.
Margin used: {margin_pct}% — {margin_status}.
```

### Placeholder Reference

| Variable | Source | Example |
|---|---|---|
| `{equity}` | `vault_account_summary.equity` | `24,512` |
| `{position_count}` | `len(vault_positions)` | `3` |
| `{unrealized_pnl_sign}` | `+` or `-` | `+` |
| `{unrealized_pnl_abs}` | `sum(positions.unrealized_pnl)` | `1,287` |
| `{unrealized_pnl_pct}` | `unrealized_pnl / equity × 100` | `5.25` |
| `{largest_market}` | position with max notional | `BTC-USD-PERP` |
| `{largest_notional}` | max position notional | `15,200` |
| `{margin_pct}` | `used_margin / equity × 100` | `42` |
| `{margin_status}` | threshold label | `healthy` |

**Margin status thresholds:** <50% = "healthy", 50-75% = "getting snug", 75-90% = "tight", >90% = "dangerously tight"

### Example Output

```
Your Paradex account has $24,512 equity with 3 open positions.
Unrealized P&L: +$1,287 (+5.25%).
Largest position: BTC-USD-PERP at $15,200 notional.
Margin used: 42% — healthy.
```

---

## 2. Position Breakdown Template

**Trigger phrases:** "What are my positions?", "Show positions", "Position details"

Two formats depending on position count.

### Prose Format (1-3 positions)

```
You have {position_count} open position(s):

**{market_1}** — {direction_1} {size_1} {base_1} (${notional_1} notional)
Entry: ${entry_1} | Mark: ${mark_1} | P&L: {pnl_sign_1}${pnl_1} ({pnl_pct_1}%)
Funding: {funding_status_1}

**{market_2}** — {direction_2} {size_2} {base_2} (${notional_2} notional)
Entry: ${entry_2} | Mark: ${mark_2} | P&L: {pnl_sign_2}${pnl_2} ({pnl_pct_2}%)
Funding: {funding_status_2}
```

### Example (Prose, 2 positions)

```
You have 2 open positions:

**BTC-USD-PERP** — Long 0.15 BTC ($9,825 notional)
Entry: $64,200 | Mark: $65,500 | P&L: +$195 (+1.98%)
Funding: paying ~$2.40/day

**ETH-USD-PERP** — Short 2.5 ETH ($8,750 notional)
Entry: $3,580 | Mark: $3,500 | P&L: +$200 (+2.29%)
Funding: receiving ~$1.80/day
```

### Table Format (4+ positions)

```
You have {position_count} open positions (${total_notional} total notional):

| Market | Direction | Size | Notional | Entry | Mark | P&L | P&L % |
|---|---|---|---|---|---|---|---|
| {market_1} | {dir_1} | {size_1} | ${notional_1} | ${entry_1} | ${mark_1} | {pnl_sign_1}${pnl_1} | {pnl_pct_1}% |
| {market_2} | {dir_2} | {size_2} | ${notional_2} | ${entry_2} | ${mark_2} | {pnl_sign_2}${pnl_2} | {pnl_pct_2}% |
| ... | ... | ... | ... | ... | ... | ... | ... |
| **Total** | | | **${total_notional}** | | | **{total_pnl_sign}${total_pnl}** | **{total_pnl_pct}%** |

Net exposure: {net_direction} ${net_notional} | Effective leverage: {leverage}x
```

### Example (Table, 5 positions)

```
You have 5 open positions ($62,350 total notional):

| Market | Direction | Size | Notional | Entry | Mark | P&L | P&L % |
|---|---|---|---|---|---|---|---|
| BTC-USD-PERP | Long | 0.25 BTC | $16,375 | $64,100 | $65,500 | +$350 | +2.18% |
| ETH-USD-PERP | Long | 4.0 ETH | $14,000 | $3,420 | $3,500 | +$320 | +2.34% |
| SOL-USD-PERP | Short | 80 SOL | $12,560 | $160.50 | $157.00 | +$280 | +2.18% |
| DOGE-USD-PERP | Long | 50,000 DOGE | $10,250 | $0.198 | $0.205 | +$350 | +3.54% |
| ARB-USD-PERP | Long | 5,000 ARB | $9,165 | $1.78 | $1.833 | +$265 | +2.98% |
| **Total** | | | **$62,350** | | | **+$1,565** | **+2.51%** |

Net exposure: Long $27,530 | Effective leverage: 2.5x
```

---

## 3. Daily Recap Template

**Trigger phrases:** "What happened today?", "Daily recap", "End of day summary"

### Template

```
## Daily Recap — {date}

### Account Snapshot
- Equity: ${equity} ({equity_change_sign}${equity_change} today)
- Margin used: {margin_pct}%
- Free margin: ${free_margin}

### Position Changes Today
{position_changes_section}

### P&L Breakdown
| Source | Amount |
|---|---|
| Trading P&L (unrealized moves) | {trading_pnl_sign}${trading_pnl} |
| Funding payments | {funding_pnl_sign}${funding_pnl} |
| **Net P&L today** | **{net_pnl_sign}${net_pnl}** |

Top contributor: {top_contributor_market} ({top_pnl_sign}${top_pnl})
Worst performer: {worst_market} ({worst_pnl_sign}${worst_pnl})

### Funding Costs
| Market | Rate (8h) | Daily Cost | Direction |
|---|---|---|---|
| {market_1} | {rate_1}% | ${funding_cost_1} | {paying_receiving_1} |
| ... | ... | ... | ... |
| **Total** | | **${total_funding}** | |

### Market Context
{market_context_lines}
```

### Example Output

```
## Daily Recap — 2026-03-31

### Account Snapshot
- Equity: $24,512 (+$487 today)
- Margin used: 42%
- Free margin: $14,217

### Position Changes Today
- Opened Long 0.15 BTC-USD-PERP at $64,200
- Increased SOL-USD-PERP short by 20 SOL at $158.30
- No positions closed

### P&L Breakdown
| Source | Amount |
|---|---|
| Trading P&L (unrealized moves) | +$512 |
| Funding payments | -$25 |
| **Net P&L today** | **+$487** |

Top contributor: ETH-USD-PERP (+$320)
Worst performer: ARB-USD-PERP (-$45)

### Funding Costs
| Market | Rate (8h) | Daily Cost | Direction |
|---|---|---|---|
| BTC-USD-PERP | 0.0100% | $4.91 | Paying |
| ETH-USD-PERP | 0.0085% | $3.57 | Paying |
| SOL-USD-PERP | -0.0120% | $4.51 | Receiving |
| **Total** | | **$3.97 net paid** | |

### Market Context
- BTC +2.3% ($64,050 -> $65,500) — broad risk-on move
- ETH +1.8% ($3,438 -> $3,500) — following BTC
- SOL -1.5% ($159.40 -> $157.00) — underperforming amid alt rotation
```

---

## 4. Morning Briefing Template

**Trigger phrases:** "Morning briefing", "Give me a briefing", "Start of day"

### Template

```
## Morning Briefing — {date}

### Account Overview
- Equity: ${equity}
- Free margin: ${free_margin} ({free_margin_pct}% available)
- Margin used: {margin_pct}% — {margin_status}
- Effective leverage: {leverage}x

### Position Summary
| Market | Dir | Size | Notional | Overnight P&L | Total P&L |
|---|---|---|---|---|---|
| {market_1} | {dir_1} | {size_1} | ${notional_1} | {overnight_pnl_sign_1}${overnight_pnl_1} | {total_pnl_sign_1}${total_pnl_1} |
| ... | ... | ... | ... | ... | ... |

### Overnight Funding
- Total funding paid/received overnight: {funding_sign}${overnight_funding}
- Biggest funding cost: {market_x} at ${funding_x}/day
- Net daily funding rate: {funding_sign}${daily_funding}/day

### Market Context (Overnight Moves)
| Market | Close | Current | Change |
|---|---|---|---|
| {market_1} | ${close_1} | ${current_1} | {change_1}% |
| ... | ... | ... | ... |

### Risk Flags
{risk_flags_section}

### Outlook
{outlook_section}
```

### Example Output

```
## Morning Briefing — 2026-04-01

### Account Overview
- Equity: $24,512
- Free margin: $14,217 (58% available)
- Margin used: 42% — healthy
- Effective leverage: 2.5x

### Position Summary
| Market | Dir | Size | Notional | Overnight P&L | Total P&L |
|---|---|---|---|---|---|
| BTC-USD-PERP | Long | 0.25 BTC | $16,375 | +$163 | +$350 |
| ETH-USD-PERP | Long | 4.0 ETH | $14,000 | +$96 | +$320 |
| SOL-USD-PERP | Short | 80 SOL | $12,560 | +$72 | +$280 |

### Overnight Funding
- Total funding paid overnight: -$8.12 (2 funding intervals)
- Biggest funding cost: BTC-USD-PERP at $4.91/day
- Net daily funding rate: -$3.97/day

### Market Context (Overnight Moves)
| Market | Close | Current | Change |
|---|---|---|---|
| BTC-USD-PERP | $64,900 | $65,500 | +0.92% |
| ETH-USD-PERP | $3,476 | $3,500 | +0.69% |
| SOL-USD-PERP | $157.90 | $157.00 | -0.57% |

### Risk Flags
- No immediate concerns. All positions within normal ranges.
- ETH-USD-PERP is now 34% of total exposure — not critical, but worth noting.

### Outlook
- BTC consolidating near $65,500 resistance. A break above $66,000 could accelerate your long.
- SOL weakness benefits your short — watch $154 as next support level.
- Funding rates are moderate across the board; no urgency to adjust.
```

---

## 5. P&L Analysis Template

**Trigger phrases:** "How much have I made?", "P&L", "What's my profit?"

Three sub-formats depending on what the user asks.

### Total P&L Format

```
### Portfolio P&L Summary

**Unrealized P&L (open positions):** {total_pnl_sign}${total_unrealized_pnl} ({total_pnl_pct}% of equity)

| Market | Direction | Unrealized P&L | % of Entry |
|---|---|---|---|
| {market_1} | {dir_1} | {pnl_sign_1}${pnl_1} | {entry_pct_1}% |
| ... | ... | ... | ... |
| **Total** | | **{total_sign}${total_pnl}** | |

Best performer: {best_market} ({best_sign}${best_pnl})
Worst performer: {worst_market} ({worst_sign}${worst_pnl})

Note: Realized P&L from closed trades is not available via current data tools.
Check the Paradex UI for complete trade history.
```

### Example (Total P&L)

```
### Portfolio P&L Summary

**Unrealized P&L (open positions):** +$1,565 (+6.39% of equity)

| Market | Direction | Unrealized P&L | % of Entry |
|---|---|---|---|
| BTC-USD-PERP | Long | +$350 | +2.18% |
| ETH-USD-PERP | Long | +$320 | +2.34% |
| SOL-USD-PERP | Short | +$280 | +2.18% |
| DOGE-USD-PERP | Long | +$350 | +3.54% |
| ARB-USD-PERP | Long | +$265 | +2.98% |
| **Total** | | **+$1,565** | |

Best performer: DOGE-USD-PERP (+$350, +3.54%)
Worst performer: ARB-USD-PERP (+$265, +2.98%) — still positive, all positions in profit.

Note: Realized P&L from closed trades is not available via current data tools.
Check the Paradex UI for complete trade history.
```

### Per-Position P&L Format

```
### P&L Detail — {market}

- Direction: {direction}
- Size: {size} {base} (${notional} notional)
- Entry price: ${entry_price}
- Current mark: ${mark_price}
- Price change: {price_change_sign}{price_change_pct}%
- Unrealized P&L: {pnl_sign}${unrealized_pnl}
- Estimated funding cost to date: {funding_sign}${est_funding_cost}
- Net P&L (after funding): {net_sign}${net_pnl}
```

### Example (Per-Position)

```
### P&L Detail — BTC-USD-PERP

- Direction: Long
- Size: 0.25 BTC ($16,375 notional)
- Entry price: $64,100
- Current mark: $65,500
- Price change: +2.18%
- Unrealized P&L: +$350
- Estimated funding cost to date: -$18.40 (held ~3.75 days)
- Net P&L (after funding): +$331.60
```

### Time-Period P&L Format

```
### Estimated P&L — Last {period}

Based on current positions and market price changes over the period:

| Market | Direction | Price Change | Est. P&L Impact |
|---|---|---|---|
| {market_1} | {dir_1} | {change_1}% | {impact_sign_1}${impact_1} |
| ... | ... | ... | ... |
| **Subtotal (price moves)** | | | **{subtotal_sign}${subtotal}** |
| Estimated funding | | | {funding_sign}${funding_est} |
| **Estimated net P&L** | | | **{net_sign}${net_pnl}** |

Caveat: This estimate assumes positions were held for the full period
at current sizes. Actual results may differ if positions were opened,
closed, or resized during this window.
```

### Example (Time-Period, Last 7 Days)

```
### Estimated P&L — Last 7 Days

Based on current positions and market price changes over the period:

| Market | Direction | Price Change | Est. P&L Impact |
|---|---|---|---|
| BTC-USD-PERP | Long | +4.2% | +$688 |
| ETH-USD-PERP | Long | +3.8% | +$532 |
| SOL-USD-PERP | Short | -2.1% | +$264 |
| **Subtotal (price moves)** | | | **+$1,484** |
| Estimated funding (7d) | | | -$27.79 |
| **Estimated net P&L** | | | **+$1,456** |

Caveat: This estimate assumes positions were held for the full period
at current sizes. Actual results may differ if positions were opened,
closed, or resized during this window.
```

---

## 6. Balance & Cash Template

**Trigger phrases:** "How much do I have?", "Balance", "Cash available", "Can I withdraw?"

### Template

```
### Account Balance

| Component | Amount |
|---|---|
| Total equity | ${total_equity} |
| Locked (margin in use) | ${locked} |
| Available (free to trade/withdraw) | ${available} |

**Capital deployment:** {deployed_pct}% deployed, {idle_pct}% idle

{transfer_section_if_requested}
```

### Deployment Ratio Context

| Ratio | Interpretation |
|---|---|
| <30% deployed | Very conservative — significant idle capital |
| 30-60% deployed | Moderate usage — room for new positions |
| 60-80% deployed | Active — limited room for new positions |
| >80% deployed | Fully loaded — consider freeing margin before adding |

### Example Output (Balance Only)

```
### Account Balance

| Component | Amount |
|---|---|
| Total equity | $24,512 |
| Locked (margin in use) | $10,295 |
| Available (free to trade/withdraw) | $14,217 |

**Capital deployment:** 42% deployed, 58% idle
You have plenty of room for additional positions or withdrawals.
```

### Example Output (With Transfer History)

```
### Account Balance

| Component | Amount |
|---|---|
| Total equity | $24,512 |
| Locked (margin in use) | $10,295 |
| Available (free to trade/withdraw) | $14,217 |

**Capital deployment:** 42% deployed, 58% idle

### Recent Transfers
| Date | Type | Amount | Status |
|---|---|---|---|
| 2026-03-28 | Deposit | +$5,000 | Completed |
| 2026-03-15 | Deposit | +$10,000 | Completed |
| 2026-03-01 | Withdrawal | -$2,000 | Completed |

**Net deposits:** $13,000
**Current equity vs. deposits:** $24,512 / $13,000 = +88.6% total return on deposited capital
```
