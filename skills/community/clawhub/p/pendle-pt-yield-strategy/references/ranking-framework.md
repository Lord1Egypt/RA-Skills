# Pendle PT Ranking Framework

Use this as the detailed rubric when comparing PT markets.

## Required fields per market

Capture these fields whenever possible:

- market name
- chain
- underlying asset / protocol
- expiry date
- days to expiry
- PT APY / implied fixed yield
- liquidity / TVL
- volume
- incentives / points context if relevant
- notable constraints (caps, withdrawal friction, bridge dependency, unusual mechanics)

## Scoring dimensions

### 1. Time to par

Questions:
- How many days remain until maturity?
- Is that duration a good fit for a hold-to-par trade?
- Is it short enough to be attractive for a rotation strategy?

Suggested buckets:
- **0-30 days** — strongest rotation candidates
- **30-120 days** — strongest hold-to-par candidates
- **120+ days** — needs better APY and cleaner underlying to justify duration

### 2. APY attractiveness

Questions:
- Is the displayed PT APY competitive versus other PTs of similar duration?
- Is the yield still attractive after considering friction and execution quality?
- Is the APY likely driven by real discount / carry, or does it look distorted by poor liquidity?

### 3. Underlying risk

Questions:
- What asset / protocol is ultimately backing the PT?
- Is the source of return easy to explain?
- Are there additional smart contract, strategy, leverage, or bridge layers?
- Is there meaningful depeg or solvency risk?

Suggested qualitative labels:
- **Low risk**
- **Medium risk**
- **High risk**

### 4. Liquidity / exit quality

Questions:
- Is there enough market depth for practical trade sizes?
- Does the market show enough recent activity?
- Would repeated entry / exit likely incur meaningful slippage?
- Is this only investable at tiny size?

Suggested qualitative labels:
- **Strong liquidity**
- **Usable liquidity**
- **Thin liquidity**

## Recommended report layout

For each market:

- **Market:**
- **Chain:**
- **Underlying:**
- **Expiry / days to par:**
- **Natural PT APY:**
- **Risk:**
- **Liquidity:**
- **Loop support:** Morpho verified / Euler verified / Contango manual / heuristic only / none
- **Execution ease:** easy / moderate / manual
- **Best fit:** hold-to-par / near-par rotation / practical loop / paper-only loop / avoid
- **Why it matters:**
- **Key risk:**
- **Verdict:**

## Final ranking buckets

Always end with these sections:

### Best natural PT yield

Include the strongest raw PT opportunities regardless of Contango support.

### Best hold-to-par ideas

Include the markets that combine:
- good 1-4 month duration fit
- attractive APY
- acceptable underlying risk
- enough liquidity

### Best near-par rotation ideas

Include the markets that combine:
- short time to maturity
- still-strong annualized APY
- strong enough liquidity to rotate

### Best practical PT loops

Include PTs where execution is realistically attractive once loop support and route quality are considered.

### Best Contango-supported manual set

Use this when the user specifically wants the manually confirmed Contango set weighted for execution convenience.

### Best paper APY but manual-only

Use this for PTs that may have stronger raw PT APY or manual loop economics, but lack easier Contango execution.

### Avoid / low-conviction

Include markets that fail on:
- underlying quality
- liquidity
- excessive complexity
- duration mismatch

## Useful comparisons

When the data supports it, compare:
- same underlying across different expiries
- similar duration across different underlying assets
- high-APY but thin-liquidity markets versus lower-APY but cleaner markets

## Important principle

The final answer should help the user decide where to put money, not just identify the highest APY row on Pendle.
