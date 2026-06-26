# Analysis Framework

## Module Overview

The analysis process has four interconnected modules:

```
A1 (Information Sourcing) → A2 (Reasoning & Prediction)
                                    ↓
B1 (Market Assessment)    → C1 (Comments Validation) → B2 (Trade Idea & Execution)
```

## A1: Information Sourcing

### Source Priority (highest to lowest reliability)

1. **Official data** - Government statistics, corporate filings, official announcements
2. **Authoritative media** - Reuters, AP, Bloomberg, BBC, established newspapers
3. **Domain experts** - Named analysts, researchers with verifiable track records
4. **Prediction aggregators** - Metaculus, PredictIt, other forecasting platforms
5. **Social/opinion** - Twitter/X, Reddit, forums (use only as sentiment signal)

### Source Evaluation Checklist

- Is the source primary (direct observation) or secondary (reporting on others)?
- Does the source have incentive to bias the information?
- When was the information published? Is it still current?
- Can the claim be corroborated by an independent source?

### Search Strategy

For each market question, construct 2-3 targeted web searches:
1. Direct factual query about the event/outcome
2. Expert analysis or forecast for the topic
3. Recent news or developments that could shift probability

Record every source URL and extract the key data point from each.

## A2: Reasoning & Prediction

### Semi-Structured Probability Estimation

Probability estimation uses an "evidence-based structured adjustment" method: establish a baseline first, then explicitly record the direction, strength, and adjustment magnitude for each piece of evidence, forming an auditable reasoning chain.

#### Step 1: Establish Base Probability

| Situation | Base Source |
|-----------|------------|
| Historical frequency data available | Use historical frequency (e.g., "similar events occurred 12% of the time over the past 10 years") |
| No historical data but authoritative forecasts exist | Use the median of authoritative forecasts |
| Neither available | Use current market price as starting point (but mark "market price as prior") |

For longshot markets (Yes < 20%): **mandatory use of historical base rate** — do not use market price as prior.

#### Step 2: Evidence Registry

For each piece of evidence collected, fill in the following table (this table must be displayed in the report):

| # | Evidence Summary | Source | Direction | Strength | Adjustment | Updated Prob |
|---|------------------|--------|-----------|----------|------------|--------------|
| 0 | Base probability | {source} | — | — | — | {base}% |
| 1 | {evidence_1} | {URL} | ↑/↓ | Strong/Med/Weak | ±X% | {new}% |
| 2 | {evidence_2} | {URL} | ↑/↓ | Strong/Med/Weak | ±X% | {new}% |
| ... | ... | ... | ... | ... | ... | ... |
| N | **Final estimate** | — | — | — | — | **{final}%** |

#### Strength-to-Adjustment Mapping

| Strength | Adjustment Range | Typical Sources |
|----------|------------------|-----------------|
| Strong | ±10-20% | Official data, established facts, authoritative forecasts |
| Medium | ±5-10% | Mainstream media reports, expert analysis, statistical models |
| Weak | ±1-5% | Social sentiment, single sources, indirect evidence |

#### Step 3: Assign Confidence

- **High**: Multiple strong pieces of evidence point in the same direction, no contradictory signals in the evidence registry
- **Medium**: Moderate evidence supports the estimate, but 1-2 contradictory pieces or information gaps exist
- **Low**: Conflicting signals, limited information, or heavy reliance on assumptions

#### Step 4: Cross-Checks

After completing the estimate, perform two checks:
1. **Anchoring check**: Is the gap between the final estimate and market price reasonable? If the gap > 25%, re-examine whether the evidence chain is strong enough to support it.
2. **Reversal check**: If you flip the direction, could the same evidence support the opposite conclusion? If yes, lower the confidence level.

### Common Reasoning Pitfalls to Avoid

- **Anchoring**: Don't over-weight the current market price as truth
- **Recency bias**: Don't over-weight the latest headline
- **Narrative fallacy**: Don't construct compelling stories from sparse data
- **Base rate neglect**: Always start from historical frequency when available

### Longshot Bias

#### The Phenomenon
In prediction markets, low-probability events (Yes < 20%) are systematically overpriced. Causes:
- Retail traders are drawn to high payoff ratios (5:1, 10:1) for psychological excitement
- Narrative-driven: dramatic events (regime change, war outbreak) naturally attract attention and capital
- Psychological resistance to shorting (buying No) — the illusion of "win small, lose big"

#### Rules of Thumb
- Market price < 15%: true probability is typically 30-50% lower than market price (e.g., market 15% → true ~8-10%)
- Market price 15-25%: true probability is typically 15-30% lower than market price
- Market price 25-40%: smaller bias, requires case-by-case analysis
- Market price > 50%: longshot bias does not apply (favorite bias may exist instead)

#### "No Scan" Strategy
In each analysis cycle, specifically select 3-5 high-liquidity markets with Yes < 20% and systematically evaluate the No-side edge:
1. Estimate probability independently using external evidence — ignore market price
2. Apply extra skepticism to narrative-driven dramatic events — ask: "What is the base rate?"
3. Sanity check: if you use the market price as prior, how strong would evidence need to be to justify it? Usually the answer is "far stronger than what exists"

#### Advantages of Buying No
- High win rate (profitable 80%+ of the time)
- Small per-trade profit but high certainty — suitable for steady accumulation
- Typically better liquidity (No-side depth > Yes-side)

## B1: Market Assessment

### Edge Calculation

```
Edge = AI_estimated_probability - Market_implied_probability
```

- `Market_implied_probability` = outcome price from Polymarket (e.g., 0.35 = 35%)
- Positive edge on "Yes" → buy Yes tokens
- Negative edge on "Yes" (positive edge on "No") → buy No tokens

### Edge Thresholds

| Edge (absolute) | Signal Strength | Action |
|------------------|-----------------|--------|
| > 20% | Strong | High-priority recommendation |
| 10-20% | Moderate | Standard recommendation |
| 5-10% | Weak | Mention but note low confidence |
| < 5% | Noise | Skip, insufficient edge |

### Four-Dimensional Market Scoring

Rate each market 1-5 on:

1. **Information Flow**: How much information asymmetry exists? Can web-accessible data give an edge over the crowd?
2. **Resolution Clarity**: How clearly defined are the resolution criteria? Is there ambiguity risk?
3. **Liquidity**: How deep is the order book? Can positions be entered and exited without excessive slippage?
4. **Volatility**: How much has the price moved recently? High volatility = more opportunity but also more risk.

## C1: Comments Validation

### Purpose

Serves as an independent verification layer for probability estimates. Web search (A1) provides macro-level information, while comments provide micro-level perspectives from actual position holders — they often possess more specialized domain knowledge and better understand the nuances of resolution rules.

### Comment Signal Classification

| Signal | Weight | Notes |
|--------|--------|-------|
| Cites verifiable news sources | High | Can directly update probability after click-through verification |
| Quantitative models/data | Medium-High | Verify logic is sound before incorporating |
| Resolution rule discussions | Medium | Reveals resolution ambiguity risks |
| Sentiment/narrative | Low | Use only as sentiment signal, does not change probability |
| Claims of insider information | Low | Ignore unless corroborated by other sources |

### Adjustment Magnitude

- Substantive overlooked evidence discovered: ±5-15%
- Resolution rule ambiguity discovered: downgrade confidence from High to Medium, or Medium to Low
- No new information found: no adjustment (this is the most common outcome)

### Caveats

- Comments contain noise and bias — position holders naturally tend to argue in favor of their own direction
- Do not raise probability simply because "most comments are bullish"
- Focus on **argument quality** rather than **quantity or direction**

## B2: Trade Idea & Execution

### Position Sizing: Quarter-Kelly Criterion

Full Kelly:
  f* = (p - c) / (1 - c)

Quarter Kelly (recommended):
  f_q = f* / 4
  position = min(f_q × bankroll, 0.10 × order_book_depth_at_2%_slippage)

Reference bankroll: $10,000 (adjust to user's stated bankroll if provided).

Edge cases:
- f* ≤ 0: no edge — do not bet
- f* > 1.0: cap display at 100%, still apply quarter Kelly
- Liquidity cap < $50: warn very thin liquidity

### Monthly Return Estimation

  expected_return = (p - c) / c
  monthly_return = (1 + expected_return) ^ (30 / d) - 1

Duration handling:
- d < 7 days: floor at 7, flag "illustrative only"
- d > 365 days: compute normally, note long capital lock-up
- No end_date: default 90 days, mark "(assumed)"

### Order Placement Strategy

- **Limit orders preferred**: Place limit orders at or slightly better than current market
- **Avoid market orders**: Slippage on thin books can be significant
- For "Yes" bets: place limit buy at or just above best bid
- For "No" bets: place limit buy on No token at or just above best bid

### Risk Disclosure

Always note:
- Prediction markets carry risk of total loss
- Resolution criteria may be interpreted unexpectedly
- Liquidity can disappear, making exit difficult
- Past market accuracy does not guarantee future accuracy
