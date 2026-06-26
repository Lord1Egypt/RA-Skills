# Output Template

Use this template for the backtest report.

---

## Report Header

```markdown
# Polymarket Recommendation Backtest

**Report Time:** {YYYY-MM-DD HH:MM:SS} (UTC)
**Data Range:** {earliest_recommendation_date} — {today}
**Recommendations:** {total} | Settled: {settled} | Open: {open} | Unmatched: {unmatched}

> {1-2 sentence summary of overall performance}
```

## Performance Overview

```markdown
---

## Performance Overview

| Metric | Value |
|--------|-------|
| Total Invested | ${total_invested} |
| Current Value | ${total_current_value} |
| **Total P&L** | **${total_pnl} ({total_pnl_pct}%)** |
| Realized P&L | ${realized_pnl} (settled positions) |
| Unrealized P&L | ${unrealized_pnl} (open positions) |
| Win Rate | {win_rate}% ({wins}/{settled}) |
| Best Position | {best_market} (+${best_pnl}, +{best_pnl_pct}%) |
| Worst Position | {worst_market} (${worst_pnl}, {worst_pnl_pct}%) |
| Avg Edge (AI est.) | {avg_edge}% |
| Avg Actual Return | {avg_return}% |
```

## Position Details

```markdown
---

## Position Details

| # | Date | Market | Link | Dir | Entry | Current | Position | P&L | P&L% | Days | Status |
|---|------|--------|------|-----|-------|---------|----------|-----|------|------|--------|
| 1 | {date} | {market_name_truncated} | [link](https://polymarket.com/event/{slug}) | {Buy Yes/No} | {entry}% | {current}% | ${position} | ${pnl} | {pnl_pct}% | {days} | {open/won/lost} |
| ... | | | | | | | | | | |

**Notes:**
- Entry and Current prices shown as percentages (e.g., 29.0% = $0.29 per share)
- P&L = (current_price - entry_price) × shares; shares = position / entry_price
- Positive P&L in green prefix (+), negative in red prefix (-)
- Settled positions show exit price as 100% (won) or 0% (lost)
```

## Category Analysis

```markdown
---

## Category Analysis

| Category | Count | Invested | P&L | P&L% |
|----------|-------|----------|-----|------|
| Crypto | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Geopolitics | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Sports | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Tech | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Politics | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Science | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Other | {n} | ${invested} | ${pnl} | {pnl_pct}% |

{1-2 sentences interpreting which categories performed best/worst}
```

## Direction Analysis

```markdown
---

## Direction Analysis

| Direction | Count | Invested | P&L | P&L% |
|-----------|-------|----------|-----|------|
| Buy Yes | {n} | ${invested} | ${pnl} | {pnl_pct}% |
| Buy No | {n} | ${invested} | ${pnl} | {pnl_pct}% |

{1-2 sentences on Buy Yes vs Buy No performance, with reference to longshot bias theory}
```

## Edge Calibration

```markdown
---

## Edge Calibration

| # | Market | AI Edge | Actual Return | Deviation | Rating |
|---|--------|---------|---------------|-----------|--------|
| 1 | {market} | +{edge}% | {actual_return}% | {deviation}% | {accurate/overestimated/underestimated} |
| ... | | | | | |

**Average AI Edge:** {avg_edge}%
**Average Actual Return:** {avg_return}%
**Edge Conversion Rate:** {avg_return / avg_edge × 100}%

{2-3 sentences analyzing calibration: is the AI systematically over- or under-estimating edge? Any pattern by category or direction?}
```

## Strategy Reflection

```markdown
---

## Strategy Reflection

### Top Performers
{Analyze the 2-3 best performing recommendations: what made the AI estimate accurate? What information was key?}

### Worst Performers
{Analyze the 2-3 worst performing recommendations: what went wrong? Missing information? Overconfidence? Market moved on new info?}

### Category Insights
{Which categories does the AI predict well? Where does it struggle? Recommendations for category focus.}

### Buy Yes vs Buy No — Longshot Bias Validation
{Does the data confirm the longshot bias theory? Do Buy No positions on low-Yes markets outperform? Should we increase Buy No allocation?}

### Position Sizing Review
{Compare Kelly-sized positions (later entries) vs flat-sized (earlier entries). Did Kelly improve risk-adjusted returns? Any over-concentration issues?}

### Improvement Recommendations
1. {Concrete, actionable suggestion #1}
2. {Concrete, actionable suggestion #2}
3. {Concrete, actionable suggestion #3}
4. {Concrete, actionable suggestion #4 — optional}
5. {Concrete, actionable suggestion #5 — optional}
```

## Report Footer

```markdown
---

## Metadata

| Field | Value |
|-------|-------|
| Methodology | Compare entry prices from recommendation history vs current market prices / settlement outcomes |
| Analyst | Claude AI |
| Report Version | 1.0 |
| Price Source | Polymarket CLOB Midpoint API + Gamma API |
| History File | ~/polymarket-reports/recommendation-history.md |

**Disclaimer:** This is a retrospective analysis of AI-generated recommendations. Past performance does not indicate future results. Prediction markets involve risk of total loss.

---
*Report generated at {YYYY-MM-DD HH:MM:SS} UTC*
```

## Formatting Rules

1. All probabilities displayed as percentages (e.g., 35%, not 0.35)
2. All dollar amounts with $ prefix and comma separators (e.g., $5,000)
3. P&L values use + prefix for positive, no prefix for negative
4. Percentages to 1 decimal place (e.g., +12.5%, -3.2%)
5. Dollar amounts to 2 decimal places (e.g., $1,234.56)
6. All timestamps in UTC timezone, format: YYYY-MM-DD HH:MM:SS
7. Table rows sorted by date ascending (chronological order, earliest first) in Position Details
8. Categories with 0 entries omitted from Category Analysis table
9. Unmatched positions listed separately with explanation

## File Saving Convention

Save path: `~/polymarket-reports/backtest-{YYYY-MM-DD}-{HHMMSS}.md`

Filename example: `backtest-2026-02-25-120000.md`
