# Scoring Rules

Use these rules to keep sentiment judgments disciplined.

## 1. First Pass Labels

Each item should get one impact label:

- `bullish_for_gold`
- `bearish_for_gold`
- `mixed_or_unclear`
- `background_only`

If the article does not clearly affect gold, use `background_only`.

## 2. Driver Mapping

### Usually bullish for gold

- lower expected policy rates
- falling real yields
- weaker USD
- softer growth or labor data that raises easing expectations
- rising geopolitical stress with clear safe-haven demand
- strong central bank buying
- strong ETF inflows

### Usually bearish for gold

- higher-for-longer rate expectations
- rising real yields
- stronger USD
- resilient growth that reduces easing odds
- ETF outflows
- falling risk perception after a prior fear spike

### Often mixed

- inflation surprise
  - bullish if it boosts safe-haven demand and hurts real growth
  - bearish if it lifts yields and USD more than it helps hedging demand
- geopolitical headlines
  - bullish only if markets actually move toward safety
- physical demand headlines
  - often secondary unless broad or persistent

## 3. Confidence Weighting

Weight each item by:

- source quality
- recency
- directness of the gold linkage
- whether the item is original reporting or repetition
- whether market-sensitive drivers align

Suggested qualitative weighting:

- `high`: official release, Fed statement, top-tier original reporting, major ETF or central bank flow update
- `medium`: credible commentary with a clear macro link
- `low`: repeated headlines, weak explainers, low-signal commentary

## 4. Aggregation Logic

Do not count headlines. Count distinct drivers.

Example:

- 7 articles saying "gold rises as investors await Fed" are mostly one driver, not 7 bullish signals.

When the following drivers align, conviction can increase:

- rates
- real yields
- USD
- risk sentiment

When these drivers conflict, default toward `观望` unless one driver clearly dominates.

## 5. Final Conclusion Thresholds

### `看涨`

Use only when:

- at least two meaningful bullish drivers align
- no stronger bearish macro driver is dominating
- recent news flow is directionally consistent

### `看跌`

Use only when:

- at least two meaningful bearish drivers align
- no stronger bullish safe-haven or easing driver is dominating
- recent news flow is directionally consistent

### `观望`

Use when:

- drivers conflict
- evidence is sparse
- market is waiting for a major catalyst
- headlines are noisy but not decisive

## 6. Required Caveats

Always note at least one invalidation risk, such as:

- upcoming CPI / payrolls / Fed decision
- sudden geopolitical escalation or de-escalation
- sharp moves in USD or real yields
- positioning squeeze despite mixed fundamentals
