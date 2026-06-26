# Manual Contango PT Comparison Framework

Use this reference when Peter wants to compare **manually confirmed Contango-supported PT routes** against broader Pendle PT opportunities.

Important:
- Treat this list as **manual / user-confirmed**, not auto-discovered from a verified live Contango API.
- Mark it clearly as manual in outputs.
- Use it when execution convenience matters more than having a fully automated Contango catalog.

## Current manual Contango PT set

As manually confirmed in research discussion, the current Contango-focused PT family includes:
- PT USDe
- PT sUSDE
- PT cUSD
- PT stcUSD
- PT reUSD

Known quote routes may include combinations such as:
- USDC
- USDT
- USDe

Do not assume every PT/quote combination exists unless manually confirmed.

## Comparison dimensions

For each manual Contango PT candidate, compare across two separate layers.

### 1. Natural PT yield layer
This is the **unlooped PT yield** from Pendle itself.

Capture:
- PT name / family
- exact maturity
- underlying accounting asset
- implied APY / PT discount
- days to expiry
- Pendle liquidity
- broad risk notes

This answers:
- "How attractive is this PT even without looping?"

### 2. Practical looping layer
This is the **execution-adjusted** comparison.

Capture:
- Contango supported? `manual yes` / `unknown` / `no`
- quote assets available
- manual-only loop or easier execution via Contango
- known money-market support (Morpho / Euler / other)
- borrow asset cleanliness (`USDC` > `USDT` > `USDe` / more exotic quote)
- operational complexity

This answers:
- "How practical is it to actually run this loop?"

## Output format

When comparing manual Contango PTs vs broader PT markets, use sections like:

### Best natural PT APY
Raw Pendle opportunities regardless of Contango support.

### Best practical Contango-supported loops
Manual Contango set with execution convenience weighted heavily.

### Best manual-only loops
High-APY PTs that may beat Contango names on paper but require manual Morpho-style looping.

## Recommended table columns

Use bullet lists on Discord instead of markdown tables.

For each item, include:
- PT family / exact market
- natural PT APY
- days to expiry
- liquidity
- loop support status:
  - `Contango manual`
  - `Morpho verified`
  - `Euler verified`
  - `manual-only`
- execution ease:
  - `easy`
  - `moderate`
  - `manual`
- practical take

## Interpretation guidance

Use this framing explicitly:
- A PT with higher raw APY but **no Contango support** can still be the best paper trade.
- A PT with slightly lower raw APY but **manual Contango support** can still be the better practical trade.
- Separate **natural PT APY rank** from **practical executable rank**.

## Current qualitative framing

### Likely strongest raw-yield / manual-loop names
Examples from current Pendle + Morpho research:
- PT apxUSD
- PT apyUSD
- PT reUSDe
- sometimes short-duration names like PT msY

These may win on raw PT APY or manual loop economics, but they currently lack confirmed Contango support in the working manual set.

### Likely strongest practical Contango names
Manual Contango set to prioritize when execution convenience matters:
- PT USDe
- PT sUSDE
- PT cUSD
- PT stcUSD
- PT reUSD

These may not always be top raw APY, but they deserve extra weight because Contango likely makes execution materially easier.

## Reporting language to use

Prefer wording like:
- `Best natural PT yield`
- `Best practical Contango-supported loops`
- `Best paper APY but manual-only`

Avoid implying that the Contango manual set is exhaustive or auto-verified.
