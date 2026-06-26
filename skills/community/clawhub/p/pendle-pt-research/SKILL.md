---
name: pendle-pt-research
description: Research Pendle PT (principal token) markets, including unlevered hold-to-par ideas, near-expiry rotations, and looped PT strategies across money markets like Morpho and Euler. Use when evaluating Pendle PT opportunities, comparing natural PT APY versus practical loopability, ranking PTs by time to par / implied APY / liquidity / underlying risk, assessing PT collateral support, or comparing manual-only loops against easier execution paths such as Contango.
---

# Pendle PT Research

Research Pendle PT markets with a decision-first lens.

Author credit: @Moshu

This skill covers:
- **unlevered PT research** — buy PT, hold to par, or rotate near expiry
- **looped PT research** — deposit PT into a money market, borrow against it, buy more PT, and recurse when the spread and risk budget justify it
- **practical execution comparison** — compare raw PT APY against easier execution paths such as manually confirmed Contango-supported routes

Do not optimize only for the highest displayed APY. The job is to sort PT markets into investable buckets that answer questions like:
- which PTs are attractive to buy and hold until par
- which near-expiry PTs may be good for fast rotations
- which PTs are attractive to **loop for leveraged fixed yield**
- which PTs are best on paper but still manual-only
- which slightly lower-yielding PTs may still be better because execution is easier
- which markets have enough liquidity to enter and exit cleanly
- which underlying assets introduce too much risk even if APY looks good

When Peter asks specifically about **manual Contango-supported PT routes**, read `references/manual-contango-comparison.md` before answering.

## Core framework

Always evaluate Pendle PT markets across these dimensions first:

1. **Time to par**
2. **APY / implied yield**
3. **Underlying risk**
4. **Liquidity / market quality**
5. **Loopability / money-market support** when leverage is relevant

Do not rank purely by APY.

A PT with lower APY but cleaner underlying risk and better liquidity can be a better trade than a high-APY PT with ugly exit conditions or fragile collateral.

For looped PT strategies, a market with slightly lower raw PT APY can still be superior if it has:
- strong money-market support
- a borrowable major stable like USDC
- favorable max LTV
- healthy borrow liquidity
- materially lower borrow cost than PT APY

## Three strategy buckets

### 1. Hold-to-par bucket

Use for markets with roughly **1-4 months to expiry** when the yield is attractive and the underlying risk is acceptable.

Focus on:
- annualized PT discount / implied APY
- confidence in the underlying asset / yield source
- enough liquidity for exit if needed
- whether holding to maturity is simpler than actively managing in and out

This bucket is usually best when:
- maturity is not too far away
- the underlying is understandable and reasonably trusted
- liquidity is healthy enough
- the yield is good without needing heroic timing

### 2. Near-par rotation bucket

Use for PTs that will reach par soon but still show unusually attractive APY.

Focus on:
- very short time to maturity
- whether the annualized yield is still meaningfully elevated
- ability to enter and exit repeatedly without getting chewed up by slippage / fees
- whether market depth is good enough for repeated rotations

This bucket is usually best when:
- time to maturity is short
- APY remains unusually high for that short duration
- liquidity is strong
- the market can be treated as a short-duration yield parking spot

### 3. PT looping bucket

Use for PTs that can be deposited into a money market and borrowed against to create **leveraged fixed-yield exposure**.

Focus on:
- raw PT implied APY
- supported money markets such as Morpho, Euler, Aave, Dolomite, or other Pendle integrations
- borrowable assets, especially major stables like USDC
- borrow APR at realistic size
- max LTV and a practical safety buffer below max LTV
- available borrow liquidity
- Pendle Pencosystem `Max Looping APY` when visible
- whether execution is available manually or through automators such as Contango

This bucket is usually best when:
- the PT already has attractive raw yield
- PT collateral support exists on a credible money market
- borrow cost is comfortably below PT APY
- liquidity is deep enough for both PT entry and borrow execution
- the leverage can be run conservatively with a real liquidation buffer

## Ranking workflow

### Step 1: Build the candidate list

Start from Pendle PT markets page:
- https://app.pendle.finance/trade/markets

For each candidate PT market, capture at least:
- market name
- chain
- expiry date
- days to expiry / time to par
- displayed APY or implied yield
- fixed-yield direction (PT)
- underlying asset / protocol / vault
- market liquidity / TVL / depth if visible
- volume if visible
- any incentive / points context if relevant

If needed, also read Pendle docs or market details pages to understand the underlying source of yield.

### Step 1B: Build the loopability map

For PT looping research, inspect the data sources in this order:
1. protocol-verified sources such as Morpho GraphQL or Euler indexer GraphQL
2. Pendle Pencosystem partner data
3. manually confirmed Contango-supported routes when Peter provides them
4. heuristic inference only as a last resort

For each loopable candidate PT, capture at least:
- supported money market(s)
- borrowable asset(s)
- current borrow APR when known
- max LTV when known
- available liquidity to borrow when known
- Pendle `Max Looping APY` when shown
- whether the route is `Morpho verified`, `Euler verified`, `Contango manual`, or `heuristic only`

Treat this loopability map as a first-class input, not an afterthought.

### Step 2: Classify the underlying risk

Assign an explicit risk tier.

Suggested tiers:
- **Low** — major stable / major LST / highly recognizable underlying with relatively simple structure
- **Medium** — decent protocol quality but more smart-contract, strategy, bridge, or asset-specific risk
- **High** — fragile, obscure, highly reflexive, leveraged, low-trust, or structurally complex underlying

When rating risk, consider:
- what generates the yield
- whether principal ultimately depends on another protocol / vault / bridge
- smart contract complexity
- asset volatility
- depeg risk
- whether the underlying is easy to explain in one sentence

If the underlying is hard to explain clearly, penalize it.

## Liquidity / market-quality lens

Do not treat all PT APY equally.

Check for:
- total liquidity / TVL
- recent trading volume
- likely slippage for realistic position sizes
- ease of entering and exiting without moving the market too much
- whether the market looks alive or stale

Prefer markets where Peter can move in and out without drama.

Penalize:
- thin liquidity
- stale / low-volume markets
- markets that are only attractive on paper for tiny size

For looped PT research, apply the same discipline to the financing leg:
- borrow liquidity must be deep enough for realistic size
- the money market integration must look maintained and usable
- max LTV is not the operating target; leave a real buffer below it
- a high displayed `Max Looping APY` is not enough if available liquidity is tiny or borrow cost is unstable

## Suggested output format

Use bullet lists on Discord. Avoid markdown tables there.

For each PT market, include:
- market
- chain
- expiry
- time to par
- natural PT APY
- underlying asset / source
- risk tier
- liquidity notes
- who it suits: `hold-to-par`, `near-par rotation`, `pt-looping`, `multiple`, or `avoid`
- short thesis
- key risk / invalidation
- final rank or score

For each loopable PT market, also include:
- money market(s)
- borrowable asset(s)
- borrow APR when known
- max LTV when known
- available borrow liquidity when known
- Pendle `Max Looping APY` if visible
- estimated net loop spread or loop attractiveness
- route status such as `Morpho verified`, `Euler verified`, `Contango manual`, or `heuristic only`
- practical leverage note such as `light`, `moderate`, or `aggressive only`

When comparing practical loop candidates, separate the output into:
- **Best natural PT yield**
- **Best practical PT loops**
- **Best Contango-supported manual set**
- **Best paper APY but manual-only**
- **Avoid / low-conviction markets**

## Scoring guidance

Use a weighted judgment rather than pretending the numbers are exact.

For unlevered PT ranking, a good default weighting:
- 30% time to par fit
- 30% APY attractiveness
- 25% underlying risk quality
- 15% liquidity / exit quality

For PT looping ranking, use a different weighting:
- 25% raw PT APY attractiveness
- 25% borrow spread quality and borrow APR
- 20% max LTV / leverage capacity
- 15% PT liquidity + borrow liquidity
- 15% underlying / protocol / integration risk

Adjust judgment when needed. For example:
- near-expiry rotation candidates may deserve more weight on liquidity
- longer hold-to-par candidates may deserve more weight on underlying risk
- loop candidates deserve heavier penalties for thin borrow liquidity, fragile integrations, or tiny practical size

## Decision heuristics

### Prefer for hold-to-par
- 30-120 days to maturity
- attractive fixed yield
- understandable underlying
- healthy liquidity
- clean thesis with limited babysitting required

### Prefer for near-par rotation
- short duration to maturity
- still elevated APY despite near expiry
- strong liquidity / active market
- easy to recycle capital repeatedly

### Prefer for PT looping
- PT APY comfortably above borrow APR
- support on a credible money market
- borrowable major stable like USDC
- healthy max LTV with room to run conservatively below the cap
- enough PT liquidity and borrow liquidity for realistic size
- visible `Max Looping APY` or a clearly positive manually estimated spread
- operational path that is simple enough to repeat manually or via Contango

### Penalize hard
- high APY driven by shaky or obscure underlying risk
- thin liquidity
- market too small for realistic sizing
- hard-to-explain yield source
- poor exit quality
- thin or unstable borrow liquidity
- loop economics that only work at paper max LTV and fall apart with a sensible safety buffer
- integrations that exist in theory but are hard to access or unsupported operationally

## Use the reference file

For detailed ranking dimensions and a reusable research template, read:
- `references/ranking-framework.md`

## Phase 2 scripts

These scripts now exist for the reusable workflow:
- `scripts/scan-markets.py` — pull and normalize Pendle PT markets across supported chains
- `scripts/rank-markets.py` — score and bucket markets into hold-to-par vs near-par rotation, with asset-family and stable-subtype filters
- `scripts/report-markets.py` — print a compact research report
- `scripts/generate-brief.py` — generate a markdown research brief

## PT loop scanner extension

Use these scripts inside this skill:
- `scripts/scan-pencosystem.py` — fetch the live Pendle Pencosystem partner directory
- `scripts/scan-morpho-pt-markets.py` — verify live Morpho PT-collateral markets, loan assets, borrow APY, utilization, and LLTV via GraphQL
- `scripts/scan-euler-pt-markets.py` — verify Euler PT token coverage and Euler vault matches for the target PT set via the Euler indexer GraphQL
- `scripts/scan-contango-pt-markets.py` — verify exact PT route support from Contango's public Pendle external integration config
- `scripts/merge-loop-data.py` — combine ranked PT markets with live Pencosystem partner data and protocol-verified market support when available
- `scripts/rank-looped-markets.py` — score PT looping candidates using PT APY, borrow economics, leverage capacity, liquidity, and execution practicality
- `scripts/report-looped-markets.py` — print a compact loop-focused report with money markets, borrow assets, and leverage notes

Suggested outputs:
- `data/pencosystem.latest.json`
- `data/loop-venues.latest.json`
- `data/loop-ranked.latest.json`

Typical flow:

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py
python3 report-markets.py --top 10
```

PT looping flow:

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py --stable-only --chains ethereum base arbitrum --min-days 7 --max-days 120 --min-liquidity 1000000
python3 scan-pencosystem.py
python3 scan-morpho-pt-markets.py --stable-only --min-apy 0.08
python3 scan-euler-pt-markets.py --stable-only --min-apy 0.08
python3 scan-contango-pt-markets.py --stable-only --min-apy 0.08
python3 merge-loop-data.py --stable-only --min-apy 0.08
python3 rank-looped-markets.py
python3 report-looped-markets.py --top 10
```

Filtered example for a more practical first pass:

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py --chains ethereum base arbitrum --min-days 7 --max-days 120 --min-liquidity 1000000
python3 report-markets.py --top 10
```

Stable-only example (good default for Peter's likely next strategy work):

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py --stable-only --chains ethereum base arbitrum --min-days 7 --max-days 120 --min-liquidity 1000000
python3 report-markets.py --top 10
```

Stable-subtype example:

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py --stable-only --stable-subtype stable-major stable-synthetic stable-rwa --chains ethereum base arbitrum --min-days 7 --max-days 120 --min-liquidity 1000000
python3 report-markets.py --top 10
python3 generate-brief.py --top 8
```

Outputs are written to:
- `data/markets.latest.json`
- `data/ranked.latest.json`
- `data/risk-overrides.json`

## Current implementation notes

- The Phase 2/3 scripts use live market data from Pendle's backend endpoint and currently scan supported chains in paginated batches.
- Risk scoring now supports explicit protocol / underlying overrides via `data/risk-overrides.json`.
- Manual exclusions / score nudges / bucket overrides now live in `data/market-notes.json`.
- Asset-family filtering now supports `stable`, `eth-beta`, `btc-beta`, and `other`, plus a first-class `--stable-only` mode.
- Stable sub-buckets now support `stable-major`, `stable-synthetic`, `stable-rwa`, and `stable-other` through `data/stable-subtype-overrides.json` and `--stable-subtype`.
- Ranking now also emits lightweight allocation suggestions (`tiny`, `small`, `medium`) as a first sizing heuristic.
- The risk model is still intentionally heuristic, not authoritative credit analysis.
- Protocol / underlying risk labels should be treated as a starting point for research review, not a final truth source.
- Use the filters (`--chains`, `--min-days`, `--max-days`, `--min-liquidity`, `--risk`, `--asset-family`, `--stable-only`) to narrow the field into practical buckets before reading the report.
- Use the scripts to narrow the field quickly, then manually inspect the highest-ranked candidates before deploying capital.
- PT looping research must explicitly check Pendle's per-market **Pencosystem** integrations rather than assuming every high-APY PT is loopable.
- Treat `Max Looping APY` and venue metadata from the Pencosystem as decision inputs, but still sanity-check borrow liquidity and route usability.
- Contango support should be surfaced when present because it materially changes operational simplicity, but Contango availability is not a substitute for good loop economics.

## Peter-specific preferences

- Bias toward opportunities that are practical to enter and exit, not just theoretically high-yield
- Separate **hold-to-par** ideas from **near-par rotation** ideas
- Prefer strong underlying quality and usable liquidity over APR-chasing
- Keep the output decision-oriented so it directly informs whether to deploy capital
