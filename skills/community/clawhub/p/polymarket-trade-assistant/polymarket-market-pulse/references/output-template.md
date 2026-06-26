# Output Template

Use this template for the final Market Pulse report.

---

## Report Header

```markdown
# Polymarket Market Pulse

**Report Generated:** {YYYY-MM-DD HH:MM:SS} (UTC)
**Market Data Fetched:** {YYYY-MM-DD HH:MM:SS} (UTC)

> {1-2 sentence executive summary of today's top opportunities}
```

## Per-Market Section (repeat for each of top 3 markets)

```markdown
---

## {rank}. {market_question}

**Link:** {market_url}
**Current Implied Probability:** {outcome} @ {price}% | Spread: {spread}
**Market Data Time:** {YYYY-MM-DD HH:MM:SS} (UTC)

### Probability Assessment

| | Market Says | AI Estimate | Edge |
|---|---|---|---|
| {outcome_1} | {market_prob_1}% | {ai_prob_1}% | {edge_1} |
| {outcome_2} | {market_prob_2}% | {ai_prob_2}% | {edge_2} |

<!-- Multi-outcome markets: list only the 1-2 analyzed outcomes. Add an "Others (combined)" row if needed to show the remaining probability mass. -->

### Evidence Chain

| # | Evidence Summary | Source | Direction | Strength | Adjustment | Probability |
|---|------------------|--------|-----------|----------|------------|-------------|
| 0 | Base rate | {source} | — | — | — | {base}% |
| 1 | {evidence_1} | [{src}]({url}) | {↑/↓} | {Strong/Med/Weak} | {±X%} | {X}% |
| ... | ... | ... | ... | ... | ... | ... |
| N | **Final estimate** | — | — | — | — | **{final}%** |

**Confidence:** {High/Medium/Low}
**Assessment Time:** {YYYY-MM-DD HH:MM:SS} (UTC)
**Est. Monthly Return:** {monthly_return}% ({d}d to resolution{" (assumed)" if no end_date})

### Four-Dimensional Analysis

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Information Flow | {score}/5 | {1-2 sentence assessment} |
| Resolution Clarity | {score}/5 | {1-2 sentence assessment} |
| Liquidity | {score}/5 | {1-2 sentence assessment — include total book depth and spread} |
| Volatility | {score}/5 | {1-2 sentence assessment — include 24h and 7d price changes} |

### Resolution Rules

**Basic Condition:** {1-2 sentence summary of the basic resolution condition}
**Quantitative Threshold:** {If applicable, list explicitly: metric name, threshold value, data source}
**Additional Context:** {If post-creation rule clarifications exist, quote verbatim. If none, mark "None"}
**Rules Retrieved:** {YYYY-MM-DD HH:MM} (UTC)

> ⚠️ Probability estimates have fully accounted for the above quantitative thresholds.

### Reasoning

{2-4 sentences explaining the key evidence and logic behind the probability estimate}

### Position Recommendation

| Item | Value |
|------|-------|
| Direction | Buy {outcome} @ limit {price} |
| Full Kelly | {f*}% of bankroll |
| Quarter Kelly | {f_q}% of bankroll |
| Kelly Amount | {f_q}% → ${kelly_amount} (on ${bankroll} bankroll) |
| Liquidity Cap | {liq_pct}% → ${liq_cap} (10% of ${depth} at 2% slippage) |
| **Recommended Size** | **{position_pct}% of bankroll** (${position} on ${bankroll}) |
| Max Executable | ${max} within {slippage}% slippage |
| Order Strategy | {limit / split / market} |
| Est. Monthly Return | {monthly_return}% ({d}d holding) |

### Sources

| # | Source | Retrieved (UTC) | Key Takeaway |
|---|--------|-----------------|--------------|
| 1 | [{source_title}]({url}) | {YYYY-MM-DD HH:MM} | {key_takeaway} |
| 2 | [{source_title}]({url}) | {YYYY-MM-DD HH:MM} | {key_takeaway} |
| 3 | [{source_title}]({url}) | {YYYY-MM-DD HH:MM} | {key_takeaway} |

### Comments Validation

**Scope:** Most recent {N} comments (retrieved {YYYY-MM-DD HH:MM} UTC)

| Finding Type | Details |
|--------------|---------|
| News Sources | {News links cited in comments not covered in Step 3 + key content; if none, mark "No new sources"} |
| Quantitative Analysis | {Valuable data or models from comments; if none, mark "None"} |
| Opposing Views | {Summary of main arguments opposing AI assessment; if none, mark "None"} |
| Resolution Disputes | {Key discussion points about resolution rules; if none, mark "None"} |

**Validation Conclusion:** {Maintain original / Adjust up to XX% / Adjust down to XX%} (Reason: {1 sentence})
```

## Report Footer

```markdown
---

## Metadata

| Field | Value |
|-------|-------|
| Methodology | Evidence-based structured probability estimation vs. market-implied odds |
| Analyst | Claude AI |
| Report Version | 2.0 |
| Market Data Source | Polymarket Gamma API |
| Order Book Source | Polymarket CLOB API |

**Disclaimer:** This is informational analysis, not financial advice. Prediction markets involve risk of total loss.

---
*Report generated at {YYYY-MM-DD HH:MM:SS} UTC*
```

## Formatting Rules

1. All probabilities displayed as percentages (e.g., 35%, not 0.35)
2. All dollar amounts with $ prefix and comma separators (e.g., $5,000)
3. Edge values as signed percentages with direction (e.g., +15% edge on Yes)
4. Include at least 3 sources per market
5. Links must be clickable (full URLs)
6. Market links use format: `https://polymarket.com/event/{event_slug}` (must use event-level slug, not market slug)
7. **All timestamps in UTC timezone, format: YYYY-MM-DD HH:MM:SS**
8. **Each source must include retrieval timestamp**
9. **AI assessment must include judgment timestamp**
10. Kelly fractions: 1 decimal place (e.g., 12.5%)
11. Monthly return: 1 decimal place (e.g., 8.3%)
12. Holding period assumed → append "(assumed)" after day count

## File Saving Convention

Save path: `~/polymarket-reports/market-pulse-{YYYY-MM-DD}-{HHMMSS}.md`

Filename example: `market-pulse-2026-02-23-134500.md`
