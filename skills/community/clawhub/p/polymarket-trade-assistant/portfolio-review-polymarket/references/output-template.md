# Output Template

Use this template for the Portfolio Review report.

---

## Report Header

```markdown
# Polymarket Portfolio Review

**Report Generated:** {YYYY-MM-DD HH:MM:SS} (UTC)
**Portfolio Mode:** {wallet / paper}
**Username:** {username or "N/A"}
**Wallet Address:** {address or "Paper portfolio from recommendation-history.md"}

> {1-2 sentence executive summary: overall portfolio health, top action item}
```

## Portfolio Overview

```markdown
---

## Portfolio Overview

| Metric | Value |
|--------|-------|
| Total Positions | {n} |
| Total Invested | ${total_invested} |
| Current Value | ${total_current_value} |
| **Total P&L** | **${total_pnl} ({total_pnl_pct}%)** |
| Best Position | {market} ({pnl_pct}%) |
| Worst Position | {market} ({pnl_pct}%) |
| Capital Efficiency | {avg_daily_er}% daily ER (weighted) |
```

## Position Ranking by Daily Expected Return

```markdown
---

## Position Ranking (by Daily Expected Return)

| Rank | Market | Dir | p_now | c_now | Edge | Daily ER | Days Left | Verdict |
|------|--------|-----|-------|-------|------|----------|-----------|---------|
| 1 | {market_truncated} | {Buy Yes/No} | {p_now}% | {c_now}% | {edge}% | {daily_er}% | {days} | {HOLD/SELL/ROTATE} |
| 2 | ... | | | | | | | |
| ... | | | | | | | | |

**Legend:** Daily ER > 0.50% = Excellent | 0.10-0.50% = Good | 0.02-0.10% = Marginal | < 0.02% = Inefficient | Negative = Sell
```

## Per-Position Analysis (repeat for each position)

```markdown
---

## {rank}. {market_question}

**Link:** https://polymarket.com/event/{event_slug}
**Direction:** {Buy Yes/No} | **Entry:** {entry_price}% | **Current:** {current_price}%
**Position:** ${position_usd} ({shares} shares) | **P&L:** ${pnl} ({pnl_pct}%)
**End Date:** {end_date} ({days_remaining} days remaining)
**Aggregated From:** {n} recommendation(s)

### Updated Probability Assessment

| | Market Price | AI Estimate (Updated) | Edge |
|---|---|---|---|
| Yes | {market_yes}% | {ai_yes}% | {edge_yes} |
| No | {market_no}% | {ai_no}% | {edge_no} |

**Confidence:** {High/Medium/Low}

### EV Analysis

| Metric | Value |
|--------|-------|
| p_now (your side) | {p_now}% |
| c_now (current price) | {c_now}% |
| Edge | {edge}% |
| Daily Expected Return | {daily_er}% |
| Full Kelly (f*) | {f_star}% |
| Quarter Kelly (f_q) | {f_q}% |
| Rating | {Excellent/Good/Marginal/Inefficient/Negative} |

### Event-Level Thinking

{2-4 paragraphs of analysis:}

**Latest Developments:**
{What has changed since the position was opened? New information, events, announcements.}

**Thesis Status:**
{Is the original thesis still intact? Any new risks or catalysts?}

**Catalyst Watch:**
{Upcoming events that could move this market: dates, decisions, data releases.}

### Verdict: {HOLD / SELL / ROTATE}

**Rationale:** {1-2 sentences explaining the decision}
{If ROTATE: "Rotate to: {replacement_market} — daily_er improvement: {old}% → {new}%"}
{If SELL: "Reason: {edge_reversed / thesis_broken / over_concentrated / capital_inefficient}"}

### Sources

| # | Source | Retrieved (UTC) | Key Finding |
|---|--------|-----------------|-------------|
| 1 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
| 2 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
| 3 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
```

## Portfolio-Level Analysis

```markdown
---

## Portfolio-Level Analysis

### Concentration Check

| Theme | Positions | Total Invested | % of Portfolio | Status |
|-------|-----------|----------------|----------------|--------|
| {theme} | {n} | ${amount} | {pct}% | {OK / WARNING: >40%} |
| ... | | | | |

### Capital Efficiency

| Metric | Value |
|--------|-------|
| Weighted Avg Daily ER | {daily_er}% |
| Capital Utilization | {utilized}% of bankroll |
| Positions with Daily ER < 0.02% | {n} (${amount} locked) |
| Estimated Portfolio Monthly Return | {monthly_return}% |

### Kelly Check

| Metric | Value |
|--------|-------|
| Total f_q Sum | {total_fq}% |
| Status | {OK: ≤100% / WARNING: over-Kelly} |
| Largest Single Position | {market} at {pct}% of bankroll |

### Action Summary

| # | Action | Market | Reason |
|---|--------|--------|--------|
| 1 | {HOLD/SELL/ROTATE} | {market} | {reason} |
| 2 | ... | | |
| ... | | | |

**Priority Actions:**
1. {Most urgent action with specific details}
2. {Second priority}
3. {Third priority}
```

## Report Footer

```markdown
---

## Metadata

| Field | Value |
|-------|-------|
| Methodology | EV-maximizing daily return framework with Bayesian probability updates |
| Analyst | Claude AI |
| Report Version | 1.0 |
| Price Source | Polymarket CLOB Midpoint API + Gamma API |
| Framework | See references/review-framework.md |

**Disclaimer:** This is informational analysis, not financial advice. Prediction markets involve risk of total loss. Past performance does not indicate future results.

---
*Report generated at {YYYY-MM-DD HH:MM:SS} UTC*
```

## Formatting Rules

1. All probabilities displayed as percentages (e.g., 35%, not 0.35)
2. All dollar amounts with $ prefix and comma separators (e.g., $5,000)
3. Edge values as signed percentages (e.g., +15.0%, -3.2%)
4. Daily ER to 2 decimal places (e.g., 0.15%)
5. P&L values use + prefix for positive, no prefix for negative
6. Market links use format: `https://polymarket.com/event/{event_slug}`
7. All timestamps in UTC timezone, format: YYYY-MM-DD HH:MM:SS
8. Each source must include retrieval timestamp
9. Positions sorted by daily expected return (highest first) in ranking table
10. Per-position sections ordered by daily expected return (highest first)
11. Truncate market questions to 60 characters in ranking table

## File Saving Convention

Save path: `~/polymarket-reports/portfolio-review-report-{YYYY-MM-DD}-{HHMMSS}.md`

Filename example: `portfolio-review-report-2026-02-27-030000.md`
