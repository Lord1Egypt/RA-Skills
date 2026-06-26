---
name: orca-lp
description: Full-stack Orca Whirlpool agent — read-only pool analytics (discovery, ranking, 6-month stability, range sizing, Monte Carlo projection, retrospective yield, rebalance planning, exit planning) plus on-chain liquidity management (open, increase, decrease, collect fees, close, swap). Wallet only required for intentional writes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npx tsc:*), Bash(npx tsx:*), WebFetch
model: sonnet
license: MIT
metadata:
  author: orca
  version: '4.0.1'
  operation_mode:
    default: read-only analytics and planning
    writes: use a small dedicated wallet, pinned dependencies, quote preview, address/slippage check, and a confirm flag for each transaction step
    broadcast: confirm flag only
  env_vars:
    KEYPAIR_PATH:
      required: false
      required_for: writes
      type: solana-keypair-file
      sensitive: true
      description: Path to a Solana keypair JSON file. Only set for write operations. Read-only analytics, rebalance planning, and exit planning do not need it.
    SOLANA_RPC_URL:
      required: false
      type: url
      description: Solana RPC endpoint. Defaults to https://api.mainnet-beta.solana.com.
  credentials:
    - name: KEYPAIR_PATH
      type: solana-keypair-file
      required: false
      required_for: intentional write operations only
      sensitive: true
  requires:
    - KEYPAIR_PATH (writes only)
tags:
  - orca
  - whirlpool
  - solana
  - defi
  - clmm
  - analytics
  - liquidity
  - pool-scanning
  - fee-tiers
  - stability
  - atr
  - monte-carlo
  - yield-analysis
  - lp-range
  - beachhouse
  - lp-position
  - open-position
  - close-position
  - rebalance
  - collect-fees
  - swap
  - whirlpools-sdk
  - token-2022
  - concentrated-liquidity
---

# Orca LP

Read-only analysis of Orca Whirlpool pools on Solana, plus on-chain management of concentrated liquidity positions. Generates TypeScript that queries public APIs and (when given a keypair) can submit transactions through `@orca-so/whirlpools-sdk`.

**Default workflow**: run analytics and planning without a wallet. For writes, use a small dedicated wallet, the pinned dependencies from this package, a quote preview, and a `--confirm` run after checking pool/mint addresses, token amounts, and slippage.

**APIs**:
- Orca REST: `https://api.orca.so/v2/solana` — pool discovery, search, stats
- Beachhouse: `https://stats-api.mainnet.orca.so` — 6-month daily TVL/volume timeseries
- Snorkel: `https://pools-api.mainnet.orca.so` — multi-hop swap quotes (read-only)
- Solana RPC: `https://api.mainnet-beta.solana.com` — on-chain reads + tx submission

## Use / Do Not Use

Use when:
- The user is exploring, comparing, or ranking Orca pools.
- The user asks about pool stability, volatility, or range sizing before deciding to LP.
- The user wants to see what a position would have earned historically.
- The user wants to open, increase, decrease, collect fees from, rebalance, or close an LP position on Orca.
- The user wants to swap tokens via Orca pools (single-hop or multi-hop via a bridge).
- The user wants to plan an exit — list positions, quote closures/swaps, and produce separately executable close/swap phases.

Do not use when:
- The task is not Orca-specific.

**Triggers**: `find pools`, `scan pools`, `rank pools`, `compare pools`, `stable pools`, `pool stability`, `pool APR`, `pool fees`, `fee tier`, `fee tier comparison`, `best pool`, `ATR`, `LP range`, `tick range`, `range sizing`, `price range`, `range projection`, `Monte Carlo`, `yield`, `yield analysis`, `retrospective yield`, `consistency`, `price consistency`, `which pool should I LP in`, `is this pool safe`, `add liquidity`, `provide liquidity`, `remove liquidity`, `withdraw LP`, `LP position`, `open position`, `close position`, `increase liquidity`, `decrease liquidity`, `rebalance`, `concentrated liquidity`, `CLMM`, `collect fees`, `collect rewards`, `claim rewards`, `swap`, `quote`, `exit position`, `exit everything`, `sweep to SOL`

## Requirements

| Variable | Required for | Default |
|----------|--------------|---------|
| `KEYPAIR_PATH` | Any on-chain write (open / increase / decrease / collect / close / swap) | — |
| `SOLANA_RPC_URL` | All write ops | `https://api.mainnet-beta.solana.com` |

Analytics and planning playbooks do not need a wallet. `KEYPAIR_PATH` points to a keypair that can sign transactions, so use a small dedicated wallet for write operations. Reserve **≥ 0.02 SOL** in the wallet for rent + priority fees before any write operation. See [Reserve math](#reserve-math).

### Write Workflow

For every write playbook:

- Start with a quote or simulation. Print pool address, token mints, position mint, token amounts, slippage bounds, rent/fee estimate, and the planned transaction steps.
- Use the dependency versions pinned by this skill and check the generated TypeScript before running it with `KEYPAIR_PATH`.
- Run the execution command only with the confirm flag documented by that example.
- For rebalance or exit flows, generate the plan first and execute close/drain, swap, and open steps separately.
- If the wallet contains more than the intended working amount, switch to a smaller dedicated wallet before running writes.

## Intent Router (first step)

| User intent | Playbook | First action |
|---|---|---|
| "Find / scan / rank pools" | [Quick Ranking](#quick-ranking) | `GET /pools?orderBy=tvlUsdc` |
| "Compare fee tiers for X/Y" | [Fee Tier Comparison](#fee-tier-comparison) | `GET /pools/search?query=X/Y` |
| "Is this pool stable?" / "Which pools are safest?" | [Stability Analysis](#stability-analysis) | 6mo Beachhouse TVL + volume |
| "What range should I use?" | [Range Sizing](#range-sizing) | ATR(14d) on 6mo A/B price |
| "Where could the price go?" / "Simulate the range" | [Monte Carlo Projection](#monte-carlo-projection) | GBM sim from realized vol |
| "What would I earn?" / "How much would $X have made?" | [Retrospective Yield](#retrospective-yield) | Stable periods × feeRate × volume |
| "Should I LP in X/Y?" (broad) | Start with [Quick Ranking](#quick-ranking), escalate | See [Escalation rules](#escalation--reporting-rules) |
| "Swap X for Y" / "Get a quote" | [Swap (single-pool)](#swap-single-pool) or [Swap (multi-hop)](#swap-multi-hop) | Quote → preview → execute |
| "Open an LP position on X/Y" | [Open Position](#open-position) | Compute ticks, build quote, send |
| "Open with only one token (usually SOL)" | [Open from Single Token](#open-from-single-token) | Detect SOL side, probe LP, exact-output swap, then open |
| "Add to my position" | [Increase Liquidity](#increase-liquidity) | Refresh pool, re-quote, send |
| "Take out some liquidity" | [Decrease Liquidity](#decrease-liquidity) | Partial-liquidity quote, send |
| "Collect fees" / "Claim rewards" | [Collect Fees + Rewards](#collect-fees--rewards) | Sync + collect in one tx |
| "Close my position" | [Close Position](#close-position) | Collect → drain → close (burns NFT) |
| "My position is out of range" | [Rebalance](#rebalance) | Plan close + reopen; execute phases separately |
| "Show my positions" | [Fetch Positions](#fetch-positions) | Scan both SPL programs for position NFTs |
| "Exit everything and convert to SOL" | [Exit Planning](#exit-planning) | Plan close/swap phases; execute separately |

---

## Playbooks

Each playbook is standalone. Chain them as the user's question deepens — don't pre-run everything. Read-only playbooks (analytics + planning) need no wallet. Write playbooks (Swap, Open / Increase / Decrease / Collect / Close) require `KEYPAIR_PATH` and follow the [Write Workflow](#write-workflow).

### Quick Ranking

- **Purpose**: First-pass filter on TVL / APR / Vol/TVL / priceDelta. Never the final answer — always ask before escalating to Beachhouse.
- **Endpoint**: `GET /pools?orderBy=tvlUsdc&orderDirection=desc&limit=<n>` or `/pools/search?query=<pair>`
- **Inputs**: pair or criteria (min TVL, min APR), limit
- **Output columns**: address, tokenA/B symbols, TVL, APR(7d), APR(30d), Vol/TVL, priceDelta(7d), feeRate
- **Compute**:
  - `APR(7d) = Number(stats["7d"].yieldOverTvl) / 7 * 365 * 100`
  - `APR(30d) = Number(stats["30d"].yieldOverTvl) / 30 * 365 * 100`
  - `Vol/TVL(24h) = Number(stats["24h"].volume) / Number(tvlUsdc)`
- **Flags to surface even at first pass**: priceDelta(7d) below -20% (IL trap), Vol/TVL(24h) < 0.05 (stagnant pool)
- **Gotchas**: numeric fields are strings — cast with `Number()` before math (see Gotcha #1). `priceDelta` is not volatility (see Gotcha #5).
- **Refs**: [Pool Response Key Fields](#pool-response-key-fields), [Pool Stats](#pool-stats-available-on-every-pool), [examples/scan-pools.md](examples/scan-pools.md)

### Fee Tier Comparison

- **Purpose**: The same pair often has multiple fee tiers (e.g. SOL/USDC at 1 / 4 / 30 / 100 bps). Compare yield vs stability across them.
- **Endpoint**: `GET /pools/search?query=<pair>`
- **Inputs**: pair symbol or mint-pair
- **Output**: fee tier, tickSpacing, TVL, volume(24h/7d), APR(7d), Vol/TVL — sorted by the metric the user cares about
- **Gotchas**: higher fee tiers usually have lower TVL but higher APR per dollar. Surface both — don't pick by APR alone. Thin fee-tier pools (< $10k TVL) will give bad quotes.
- **Refs**: [examples/compare-fee-tiers.md](examples/compare-fee-tiers.md)

### Stability Analysis

- **Purpose**: Distinguish stable pools from trap APRs. High APR with falling TVL is a warning, not a buy.
- **Endpoints**:
  - `GET /api/pools/{address}/tvl?time_from=<6mo-ago>&time_to=<now>&type=1D`
  - `GET /api/pools/{address}/volume?time_from=<6mo-ago>&time_to=<now>&type=1D`
- **Inputs**: pool address, 6-month window (`now - 180*86400` to `now`)
- **Compute**:
  - Realized volatility: `stddev(ln(price[i]/price[i-1]))` where `price = Number(volumeQuote) / Number(volumeBase)`
  - ATR(14d): `mean(|price[i] - price[i-1]|)` over last 14 daily A/B prices
  - Max drawdown over 6 months
  - TVL coefficient of variation
- **Red flags (can disqualify)**:
  - **TVL bleeding**: 30d-avg TVL < 70% of 6mo-mean TVL. LPs leaving is a stronger signal than TVL CV alone.
  - **Yield decay**: 30d APR < 70% of 6mo retrospective APR on stable periods.
  - **Unknown/suspect tokens**: Token-2022 mints with `permanentDelegate`, `mintCloseAuthority`, or no entry in Orca's token list. Do not proceed without explicit user acknowledgement.
- **Gotchas**: use A/B ratio `volumeQuote/volumeBase`, not `volumeBaseUsd/volumeBase` (see Gotcha #2 and [Two Different "Prices"](#two-different-prices-from-volume-data)). Beachhouse blocks default Python urllib UA (see Gotcha #3). Response is double-nested (see Gotcha #4).
- **Refs**: [Beachhouse API Reference](#beachhouse-api-reference), [examples/stability-rankings.md](examples/stability-rankings.md)

### Range Sizing

- **Purpose**: Recommend tick ranges (tight / medium / wide) for a user-chosen pool, backtested against 6-month history.
- **Inputs**: pool address, risk preference (optional)
- **Compute**:
  - ATR(14d) → three range widths
  - Historical containment %: what fraction of last 6mo would each range have held
  - Implied rebalance frequency from range exits
- **Output**: three ranges (tight/med/wide) with containment% + rebalance frequency
- **Gotchas**: containment % is a historical backtest, not a forward estimate — use Monte Carlo for forward-looking simulation.
- **Refs**: [examples/lp-range-analysis.md](examples/lp-range-analysis.md), [examples/price-range-history.md](examples/price-range-history.md)

### Monte Carlo Projection

- **Purpose**: Forward-looking simulation of price paths for a chosen range. Noisy — use Retrospective Yield for grounded earnings numbers.
- **Inputs**: pool address, range widths, horizon (7/14/30/90 days)
- **Method**: GBM from Beachhouse-derived realized volatility (A/B log returns, NOT priceDelta). Simulate ≥ 5000 paths.
- **Output**:
  - Price-path percentiles: p5 / p25 / p50 / p75 / p95
  - Expected in-range days for each range width
  - Confidence bands
- **Reporting rules (critical)**:
  - **Never quote a single number as expectation.** Always give at least [p25, p50, p75]. Percentile framing makes error bars visible.
  - **Always caveat in the same sentence**: "GBM with constant σ — underestimates tail risk and assumes no regime change." Don't bury it in a footnote.
  - **Never combine MC with fee projection.** MC projects price paths. LP-vs-HODL fee attribution under concentrated liquidity is high-variance and prone to math errors. Use Retrospective Yield for the grounded earnings number.
- **Refs**: [examples/range-projection.md](examples/range-projection.md)

### Retrospective Yield

- **Purpose**: What a deposit at a given range would have actually earned during stable periods in the last 6 months. The grounded baseline.
- **Inputs**: pool address, range width, deposit size (USD)
- **Method**:
  - Identify stable periods (days within ±2% / ±5% around a moving mean)
  - Daily fees: `Number(totalVolumeUsd) × (feeRate / 10000 / 100)`
  - Attribute to the user's position by range share
  - Annualize from the retrospective window — NOT project forward
- **Output**: realized daily fees, annualized rate on stable periods, stable-period fraction of the 6mo window
- **Reporting rules**:
  - Always caveat: "recent fee data, past performance does not predict future."
  - Quote both the stable-period APR and the blended 6mo APR — LPs should understand both.
- **Gotchas**: concentrated-liquidity fee share scales with range width (see Gotcha #7) — don't use the full-range approximation `deposit/TVL × pool_fees`.
- **Refs**: [examples/yield-projection.md](examples/yield-projection.md)

### Swap (single-pool) {#swap-single-pool}

- **Purpose**: Single-pool swap via SDK. Fastest path when a direct pool exists.
- **Inputs**: pool address, input mint, input amount (base units), slippage
- **Output**: tx signature + estimated amounts
- **CU**: 300,000
- **Gotchas**: SDK handles wSOL wrap/unwrap when the pool involves native SOL. `pool.refreshData()` before quoting to avoid stale state.
- **Refs**: [Setup](#setup), [Transaction Send Pattern](#transaction-send-pattern), [examples/swap.md](examples/swap.md), [examples/quote.md](examples/quote.md)

```typescript
const pool = await client.getPool(poolAddress);
await pool.refreshData(); // freshen cached state before quoting

const quote = await swapQuoteByInputToken(
  pool,
  inputMint,                         // e.g. SOL mint
  new BN(amountInBaseUnits),
  Percentage.fromFraction(1, 100),   // 1% slippage
  ORCA_WHIRLPOOL_PROGRAM_ID,
  ctx.fetcher,
);
console.log(`Quote: ${quote.estimatedAmountIn} → ${quote.estimatedAmountOut}`);

const tx = await pool.swap(quote);
const sig = await sendWithRetry(tx, connection);
```

### Swap (multi-hop via bridge token) {#swap-multi-hop}

- **Purpose**: Chain two swaps when no direct pool exists (e.g. TOKEN ↔ SOL where only TOKEN/USDC and SOL/USDC exist).
- **Inputs**: leg 1 pool, leg 2 pool, input mint, input amount, slippage
- **Discovery**: Snorkel's `GET /swap-quote` returns multi-hop splits in `data.swap.split[][]` — use it to pick pools, then execute each leg via the SDK.
- **Rate limit**: Snorkel 429s on repeated calls. Space iterated calls ≥ 200–500ms or use `swapQuoteByInputToken` from the SDK for single-pool quotes.
- **Gotchas**: Verify each leg's price impact independently. Low-TVL warning applies to both legs. Leg 2 depends on leg 1 landing — always await confirmation before quoting leg 2.
- **Refs**: [Canonical bridge pools](#canonical-bridge-pools), [Snorkel API Reference](#snorkel-api-reference)

```typescript
// Leg 1: TOKEN → USDC
const leg1Pool = await client.getPool(tokenUsdcPool);
await leg1Pool.refreshData();
const leg1Quote = await swapQuoteByInputToken(
  leg1Pool, tokenMint, new BN(tokenAmount),
  Percentage.fromFraction(1, 100), ORCA_WHIRLPOOL_PROGRAM_ID, ctx.fetcher,
);
await sendWithRetry(await leg1Pool.swap(leg1Quote), connection);

// Leg 2: USDC → SOL (after leg 1 lands)
const leg2Pool = await client.getPool(solUsdcPool);
await leg2Pool.refreshData();
const usdcReceived = leg1Quote.estimatedAmountOut;
const leg2Quote = await swapQuoteByInputToken(
  leg2Pool, USDC_MINT, usdcReceived,
  Percentage.fromFraction(1, 100), ORCA_WHIRLPOOL_PROGRAM_ID, ctx.fetcher,
);
await sendWithRetry(await leg2Pool.swap(leg2Quote), connection);
```

### Open Position

- **Purpose**: Open a new concentrated position centered on the current price (or a custom range).
- **Inputs**: pool address, deposit amount (token A human units), rangePct (e.g. `0.05` for ±5%), slippage
- **Output**: position mint + tx signature
- **CU**: 600,000 (position + metadata)
- **Compute**:
  - Current price from `data.sqrtPrice` via `PriceMath.sqrtPriceX64ToPrice`
  - `tickLower/tickUpper` from rangePct
  - Align ticks to pool's `tickSpacing`
  - Build quote via `increaseLiquidityQuoteByInputTokenUsingPriceDeviation`
- **Gotchas**:
  - **`tokenMaxA/B` vs `tokenEstA/B`.** The wallet must hold `tokenMaxA` AND `tokenMaxB` (slippage-buffered), not `tokenEst*` — because the on-chain instruction pulls up to the Max if the price has moved. Buffer is asymmetric when range isn't centered on current price: at 1% deviation with a ±10% offset range, `tokenMaxA` can exceed `tokenEstA` by 10–15%.
  - If sizing a deposit from a tight balance, check `tokenMaxA/B` against your available balance, not `Est`. When in doubt, scale input by ~90% of balance.
- **Refs**: [examples/open-position.md](examples/open-position.md), [CLMM Concepts](#clmm-concepts), [Range strategies](#range-strategies)

```typescript
const pool = await client.getPool(poolAddress);
await pool.refreshData();
const data = pool.getData();
const decA = pool.getTokenAInfo().decimals;
const decB = pool.getTokenBInfo().decimals;

const price = PriceMath.sqrtPriceX64ToPrice(data.sqrtPrice, decA, decB);
const rangePct = 0.05; // ±5%
const ts = data.tickSpacing;
const rawLower = PriceMath.priceToTickIndex(new Decimal(price.toNumber() * (1 - rangePct)), decA, decB);
const rawUpper = PriceMath.priceToTickIndex(new Decimal(price.toNumber() * (1 + rangePct)), decA, decB);
const tickLower = Math.floor(rawLower / ts) * ts;
const tickUpper = Math.ceil(rawUpper / ts) * ts;

const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
  ctx.fetcher, data.tokenMintA, data.tokenMintB,
);

// PriceDeviation returns matched tokenMaxA/B + minSqrtPrice/maxSqrtPrice bounds.
// Pass the quote directly to openPositionWithMetadata — no manual sqrt fields.
const quote = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
  data.tokenMintA,                    // input token
  new Decimal(depositAmount),
  tickLower, tickUpper,
  Percentage.fromFraction(1, 100),
  pool, tokenExtCtx,
);

const { positionMint, tx } = await pool.openPositionWithMetadata(tickLower, tickUpper, quote);
const sig = await sendWithRetry(tx, connection);
console.log(`Position opened: ${positionMint.toBase58()} — tx ${sig}`);
```

Save `positionMint` for future operations.

### Open Position from Single Token (swap-half-first) {#open-from-single-token}

- **Purpose**: Start with only one token (usually SOL), probe the LP pool for the exact opposite-side amount, use an exact-output swap to acquire it, then open with the other token as input.
- **Inputs**: `pool`, `decA`, `decB`, `tickLower`, `tickUpper`, `tokenExtCtx` (computed as in [Open Position](#open-position))
- **Flow**:
  1. Detect which side SOL is on (tokenA in SOL/USDC, tokenB in JUP/SOL)
  2. Reserve gas + rent, split the rest half-to-A / half-to-B
  3. Probe: quote `increaseLiquidity` with half SOL → learn `tokenMax` on the other side
  4. Exact-output swap via `swapQuoteByOutputToken` to get exactly `needOther`
  5. Re-quote with the OTHER token as input (use `0.90×` multiplier to absorb price drift)
  6. Open position
- **Gotchas**:
  - Use `swapQuoteByOutputToken` — `swapQuoteByInputToken` would require knowing the SOL → other rate ahead of time.
  - The `0.90×` multiplier in step 5 absorbs (a) price drift between swap and open, and (b) keeps the final quote's `tokenMax` under the received balance on skewed ranges. If you tighten it (e.g. `0.95`), the open-position tx will bounce on insufficient balance.
  - **Token-2022 with transfer fees**: if `otherMint` is Token-2022 with a transfer-fee extension, the wallet receives less than `swapQuote.estimatedAmountOut`. The `0.90×` absorbs it in practice; if the transfer fee > 5%, tighten the probe size instead.
  - Budget check: `solNeededForSwap + solForLPSide + ~20M lamports rent ≤ walletBalance`. `otherAmountThreshold` (slippage-bounded max) is tighter than `estimatedAmountIn` for exact-output swaps — use it.
- **Fallback**: If the LP pool doesn't support the needed swap direction (rare), swap via a bridge pool (`TOKEN/USDC` from `/pools/search`) and chain two swaps.
- **Refs**: [examples/open-position.md](examples/open-position.md)

```typescript
import { swapQuoteByOutputToken } from "@orca-so/whirlpools-sdk";

const SOL_MINT = new PublicKey("So11111111111111111111111111111111111111112");

// 1. Detect which side SOL is on
const data = pool.getData();
const solIsA = data.tokenMintA.equals(SOL_MINT);
const solMint    = solIsA ? data.tokenMintA : data.tokenMintB;
const otherMint  = solIsA ? data.tokenMintB : data.tokenMintA;
const decSol     = solIsA ? decA : decB;
const decOther   = solIsA ? decB : decA;

// 2. Reserve gas + rent, split the rest half-to-A / half-to-B
const solBalance = await connection.getBalance(wallet.publicKey);
const solForDeposit = solBalance - 25_000_000;   // leave 0.025 SOL for rent + fees
const halfSolHuman = new Decimal(solForDeposit).div(10 ** decSol).div(2);

// 3. Probe: what does the LP quote want on the other side if we put half our SOL in?
const probe = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
  solMint, halfSolHuman,
  tickLower, tickUpper,
  Percentage.fromFraction(1, 100),
  pool, tokenExtCtx,
);
// Wallet must hold tokenMax (not tokenEst) — pick the Max on the non-SOL side.
const needOther = solIsA ? probe.tokenMaxB : probe.tokenMaxA;

// 4. Exact-output swap: get exactly `needOther` of the other token
const swapQuote = await swapQuoteByOutputToken(
  pool, otherMint, needOther,
  Percentage.fromFraction(1, 100),
  ORCA_WHIRLPOOL_PROGRAM_ID, ctx.fetcher,
);

// Budget check
const solNeededForSwap = swapQuote.otherAmountThreshold.toNumber();
const solForLPSide = (solIsA ? probe.tokenMaxA : probe.tokenMaxB).toNumber();
if (solNeededForSwap + solForLPSide + 20_000_000 > solBalance) {
  throw new Error(`Not enough SOL: need ${(solNeededForSwap + solForLPSide) / 1e9} + ~0.02 for rent`);
}

await sendWithRetry(await pool.swap(swapQuote), connection, 300_000);

// 5. Re-quote using the OTHER token as input — with 0.90× buffer
await pool.refreshData();
const receivedOther = DecimalUtil.fromBN(swapQuote.estimatedAmountOut, decOther);
const finalQuote = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
  otherMint, receivedOther.mul(0.90),
  tickLower, tickUpper,
  Percentage.fromFraction(1, 100),
  pool, tokenExtCtx,
);

const { positionMint, tx } = await pool.openPositionWithMetadata(tickLower, tickUpper, finalQuote);
await sendWithRetry(tx, connection, 600_000);
```

### Increase Liquidity

- **Purpose**: Add more liquidity to an existing position at the current price.
- **Inputs**: positionMint, additionalAmount (token A human units), slippage
- **CU**: 400,000
- **Gotchas**: Always `pool.refreshData()` before quoting — position math is sqrt-price-sensitive.
- **Refs**: [examples/manage-position.md](examples/manage-position.md)

```typescript
const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey;
const position = await client.getPosition(posPda);
const pool = await client.getPool(position.getData().whirlpool);
await pool.refreshData();

const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
  ctx.fetcher, pool.getData().tokenMintA, pool.getData().tokenMintB,
);

const quote = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
  pool.getData().tokenMintA,
  new Decimal(additionalAmount),
  position.getData().tickLowerIndex,
  position.getData().tickUpperIndex,
  Percentage.fromFraction(1, 100),
  pool, tokenExtCtx,
);

await sendWithRetry(await position.increaseLiquidity(quote), connection);
```

### Decrease Liquidity

- **Purpose**: Remove a fraction of liquidity from an existing position (without closing).
- **Inputs**: positionMint, fraction (e.g. `0.50` for 50%), slippage
- **CU**: 400,000
- **Gotchas**: Always `pool.refreshData()` before quoting.
- **Refs**: [examples/manage-position.md](examples/manage-position.md)

```typescript
const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey;
const position = await client.getPosition(posPda);
const pool = await client.getPool(position.getData().whirlpool);
await pool.refreshData();

const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
  ctx.fetcher, pool.getData().tokenMintA, pool.getData().tokenMintB,
);

const liquidity = position.getData().liquidity;
const amountToRemove = liquidity.muln(50).divn(100); // 50%

const quote = decreaseLiquidityQuoteByLiquidityWithParams({
  liquidity: amountToRemove,
  tickLowerIndex: position.getData().tickLowerIndex,
  tickUpperIndex: position.getData().tickUpperIndex,
  slippageTolerance: Percentage.fromFraction(1, 100),
  sqrtPrice: pool.getData().sqrtPrice,
  tickCurrentIndex: pool.getData().tickCurrentIndex,
  tokenExtensionCtx: tokenExtCtx,
});

await sendWithRetry(await position.decreaseLiquidity(quote), connection);
```

### Collect Fees + Rewards

- **Purpose**: Collect accumulated trading fees and reward emissions from an open position.
- **Inputs**: positionMint
- **CU**: 200,000 per tx
- **Notes**: `collectFees(true)` syncs fee accounting and collects in one tx. `collectRewards` returns `TransactionBuilder[]` — iterate.
- **Refs**: [examples/collect-fees.md](examples/collect-fees.md)

```typescript
const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey;
const position = await client.getPosition(posPda);

// collectFees(true) syncs fee accounting and collects in one tx
await sendWithRetry(await position.collectFees(true), connection);

// collectRewards returns TransactionBuilder[] — iterate
const rewardTxs = await position.collectRewards(undefined, true);
for (const rtx of rewardTxs) await sendWithRetry(rtx, connection);
```

### Close Position

- **Purpose**: Collect remaining fees/rewards, drain all liquidity, close the position NFT, refund rent.
- **Inputs**: positionMint
- **Flow**: Collect fees + rewards → drain liquidity (if non-zero) → close (burns NFT, refunds rent)
- **CU**: 500,000 for standard close; 800,000 if bundling V2 instructions
- **Token-2022**: High-level `pool.closePosition(...)` handles V2 paths automatically. For raw Anchor control, see [Raw Anchor Fallback](#raw-anchor-fallback).
- **Refs**: [examples/manage-position.md](examples/manage-position.md), [examples/close-position-anchor.md](examples/close-position-anchor.md)

```typescript
const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey;
const position = await client.getPosition(posPda);
const pool = await client.getPool(position.getData().whirlpool);
await pool.refreshData();

// 1. Collect fees and rewards
await sendWithRetry(await position.collectFees(true), connection);
for (const rtx of await position.collectRewards(undefined, true)) await sendWithRetry(rtx, connection);

// 2. Drain liquidity to zero
if (!position.getData().liquidity.isZero()) {
  const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
    ctx.fetcher, pool.getData().tokenMintA, pool.getData().tokenMintB,
  );
  const drainQuote = decreaseLiquidityQuoteByLiquidityWithParams({
    liquidity: position.getData().liquidity,
    tickLowerIndex: position.getData().tickLowerIndex,
    tickUpperIndex: position.getData().tickUpperIndex,
    slippageTolerance: Percentage.fromFraction(1, 100),
    sqrtPrice: pool.getData().sqrtPrice,
    tickCurrentIndex: pool.getData().tickCurrentIndex,
    tokenExtensionCtx: tokenExtCtx,
  });
  await sendWithRetry(await position.decreaseLiquidity(drainQuote), connection);
}

// 3. Close (burns NFT, refunds rent)
const closeTxs = await pool.closePosition(posPda, Percentage.fromFraction(1, 100));
for (const tx of closeTxs) await sendWithRetry(tx, connection);
```

### Rebalance

- **Purpose**: Decide whether an out-of-range position should be moved, and size the replacement range from current pool data.
- **Flow**: Use [Range Sizing](#range-sizing) to choose the new ticks, then use [Close Position](#close-position) and [Open Position](#open-position) as separate operations if the user decides to move.
- **Tradeoff**: Rebalance cycles cost ~$0.02–0.10 in priority fees each. Don't rebalance on a fixed cadence — only when the position is meaningfully out of range.
- **Refs**: [examples/lp-range-analysis.md](examples/lp-range-analysis.md), [examples/manage-position.md](examples/manage-position.md), [examples/open-position.md](examples/open-position.md)

### Fetch Positions

- **Purpose**: List all open Orca positions owned by the wallet.
- **Inputs**: wallet public key (implicit from `wallet.publicKey`)
- **Method**:
  1. Scan both SPL programs (classic + Token-2022) — position NFTs can be minted under either.
  2. Filter NFTs: `decimals === 0 && amount === "1"`.
  3. `PDAUtil.getPosition` works for both (PDA seeds use only the mint).
- **Gotcha**: Non-Orca NFTs will throw on `client.getPosition` — catch and skip.
- **Refs**: [examples/manage-position.md](examples/manage-position.md)

```typescript
import { TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID } from "@solana/spl-token";

// Scan both token programs — position NFTs can be minted under either
const [classic, t2022] = await Promise.all([
  connection.getParsedTokenAccountsByOwner(wallet.publicKey, { programId: TOKEN_PROGRAM_ID }),
  connection.getParsedTokenAccountsByOwner(wallet.publicKey, { programId: TOKEN_2022_PROGRAM_ID }),
]);

const nftMints = [...classic.value, ...t2022.value]
  .map(a => a.account.data.parsed.info)
  .filter(i => i.tokenAmount.decimals === 0 && i.tokenAmount.amount === "1")
  .map(i => new PublicKey(i.mint));

// PDAUtil.getPosition works for both classic and Token-2022 positions —
// the PDA seeds use the mint only, not the token program.
for (const mint of nftMints) {
  const pda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, mint).publicKey;
  try {
    const position = await client.getPosition(pda);
    // ... it's ours
  } catch {
    // not an Orca position; skip
  }
}
```

### Exit Planning

- **Purpose**: Produce an exit plan without signing transactions: positions to close, remaining tokens to swap to SOL, dust to skip, ATA rent refunds, and estimated fees.
- **Flow**:
  1. [Fetch Positions](#fetch-positions). For each: estimate collect fees/rewards → drain → close.
  2. List remaining non-zero fungible token balances on both SPL programs.
  3. Print the full plan: positions to close, tokens to swap, pool/mint addresses, slippage assumptions, skipped dust, ATA closures, and gas estimate.
  4. For each token → SOL: quote first. **Skip dust**: if `estimatedAmountOut` (in SOL via current price) < ~0.0005 SOL, swap costs more than it returns.
  5. The plan command does not send transactions. Execute with separate close-position and swap runs after checking each quote.
  6. Close empty ATAs only as a separately reviewed write (`createCloseAccountInstruction(ata, wallet, wallet, [], tokenProgram)` refunds ~0.002 SOL each).
  7. If wSOL ATA remains, closing it unwraps to native SOL; treat this as a separate reviewed write.
- **Reserves**: ≥ 0.01 SOL at start — even closing operations need gas upfront.
- **Refs**: [examples/manage-position.md](examples/manage-position.md)

---

## Escalation & Reporting Rules

**Escalation — save cycles:**
- Start every broad question with Quick Ranking before pulling Beachhouse
- Ask before escalating to 6-month analysis — don't run it on 30 pools when the user cares about 3
- Retrospective Yield > Monte Carlo for grounded earnings numbers
- When the user asks "so what should I do?", synthesize across data already gathered — don't re-run analyses

**Reporting — never skip:**
- Never present a raw APR table as a recommendation
- Never quote 7d-annualized APR as an expected return
- Never quote Monte Carlo percentiles as predictions
- Flag IL traps in Quick Ranking (e.g. priceDelta(7d) < -20%) even at first pass
- Flag TVL bleeding and yield decay as red flags during Stability Analysis
- For memecoin pairs with high APR: always warn about IL before recommending

**Summary recommendations** (when the user asks "so what should I do?"):
- State expected IL exposure (from realized vol and max drawdown)
- State rebalance frequency expectation (from ATR vs chosen range)
- State retrospective earnings at the chosen range
- Close with an honest trade-off

---

## Dependencies

Use these package versions for the TypeScript examples. The SDK's API has changed shape across versions, and different releases may not export the functions used below (e.g. `WhirlpoolContext.from` signature changed; `…UsingPriceDeviation` only exists in `@orca-so/whirlpools-sdk@>=0.18`; `@orca-so/whirlpools-sdk@0.20` requires `@coral-xyz/anchor@~0.32.1`).

Pinned versions:

| Package | Version |
|---|---|
| `@solana/web3.js` | `1.98.4` |
| `@coral-xyz/anchor` | `0.32.1` |
| `bn.js` | `5.2.3` |
| `decimal.js` | `10.6.0` |
| `@orca-so/whirlpools-sdk` | `0.20.0` |
| `@orca-so/common-sdk` | `0.7.0` |
| `@solana/spl-token` | `0.4.14` |

Sanity-check scripts before sending any tx: `npx tsc --noEmit your-script.ts` catches wrong API signatures and missing exports for free.

**Whirlpool program ID**: `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc` (same on mainnet + devnet).

---

## Setup

Every write operation starts with this block:

```typescript
import { Connection, Keypair, PublicKey, ComputeBudgetProgram } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import BN from "bn.js";
import { Decimal } from "decimal.js";
import {
  WhirlpoolContext, buildWhirlpoolClient, buildDefaultAccountFetcher,
  ORCA_WHIRLPOOL_PROGRAM_ID, PDAUtil, PriceMath, TokenExtensionUtil,
  swapQuoteByInputToken,
  increaseLiquidityQuoteByInputTokenUsingPriceDeviation,
  decreaseLiquidityQuoteByLiquidityWithParams,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import * as fs from "fs";

const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm"); // require --confirm to broadcast

const connection = new Connection(process.env.SOLANA_RPC_URL!, "confirmed");
const keypair = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"))));
const wallet = new Wallet(keypair);

const fetcher = buildDefaultAccountFetcher(connection);
const ctx = WhirlpoolContext.from(connection, wallet, fetcher);
const client = buildWhirlpoolClient(ctx);
```

### Reserve math

Keep **≥ 0.02 SOL** in the wallet for rent + fees when opening or rebalancing positions (`openPositionWithMetadata` costs ~0.015 SOL rent before it's reclaimed on close; ATA creation is ~0.002 SOL each). Any write operation also needs SOL upfront even if rent is refunded after — refunds arrive when the tx lands.

---

## Transaction Send Pattern

Every write operation uses this wrapper. It adapts the priority fee to current network load, retries on blockhash expiry, and verifies landing via signature status (because `confirmTransaction` can throw while the tx still lands):

```typescript
import type { TransactionBuilder } from "@orca-so/common-sdk";

async function recommendedPriorityFee(conn: Connection): Promise<number> {
  // p75 of recent prioritization fees; floor at 10k microLamports
  const recent = await conn.getRecentPrioritizationFees();
  if (recent.length === 0) return 10_000;
  const fees = recent.map(x => x.prioritizationFee).sort((a, b) => a - b);
  const p75 = fees[Math.floor(fees.length * 0.75)];
  return Math.max(10_000, p75);
}

async function sendWithRetry(
  txBuilder: TransactionBuilder,
  conn: Connection,
  computeUnits = 400_000,
): Promise<string> {
  const microLamports = await recommendedPriorityFee(conn);
  txBuilder.prependInstruction({
    instructions: [
      ComputeBudgetProgram.setComputeUnitLimit({ units: computeUnits }),
      ComputeBudgetProgram.setComputeUnitPrice({ microLamports }),
    ],
    cleanupInstructions: [],
    signers: [],
  });

  for (let attempt = 1; attempt <= 3; attempt++) {
    let sig: string;
    try {
      sig = await txBuilder.buildAndExecute();
    } catch (e: any) {
      if (attempt < 3 && /Blockhash|expired|BlockheightExceeded/i.test(e.message)) continue;
      throw e;
    }
    for (let i = 0; i < 30; i++) {
      const status = (await conn.getSignatureStatus(sig)).value;
      if (status?.err) throw new Error(`Tx ${sig} failed: ${JSON.stringify(status.err)}`);
      if (status?.confirmationStatus === "confirmed" || status?.confirmationStatus === "finalized") return sig;
      await new Promise(r => setTimeout(r, 1000));
    }
    throw new Error(`Tx ${sig} did not confirm within 30s`);
  }
  throw new Error("unreachable");
}
```

### Compute unit sizing per operation

| Operation | CU |
|-----------|-----|
| Swap (single-pool) | 300,000 |
| Open position (with metadata) | 600,000 |
| Increase / decrease liquidity | 400,000 |
| Collect fees | 200,000 |
| Close position (drain + close) | 500,000 |
| Multi-instruction bundle (V2 close) | 800,000 |

### Address Lookup Tables (ALTs)

Multi-hop swaps with 3+ pools can exceed the 1232-byte legacy transaction limit. Pool detail responses include `addressLookupTable` — fetch each ALT with `connection.getAddressLookupTable(key)`, then compile the tx as V0:

```typescript
import { TransactionMessage, VersionedTransaction } from "@solana/web3.js";

const alt = (await connection.getAddressLookupTable(altKey)).value!;
const { blockhash } = await connection.getLatestBlockhash();
const msg = new TransactionMessage({
  payerKey: wallet.publicKey,
  recentBlockhash: blockhash,
  instructions,
}).compileToV0Message([alt]);                  // single arg: ALT array
const tx = new VersionedTransaction(msg);
tx.sign([keypair]);
await connection.sendTransaction(tx);
```

---

## CLMM Concepts

- **Tick**: discrete price unit. `price = 1.0001^tick` (before decimal adjustment).
- **Tick spacing**: the program only allows ticks at multiples of `tickSpacing`. Each pool has its own.
- **In-range**: a position earns fees only while `tickLowerIndex <= currentTick < tickUpperIndex`. Out-of-range positions earn nothing and sit entirely in one token.
- **Position NFT**: each position is a unique mint (NFT). Losing it means losing access.

### Tick spacing by fee tier

| Fee rate | Fee % | Tick spacing | Typical use |
|----------|-------|-------------|-------------|
| 1 | 0.0001% | 1 | Stablecoin pairs |
| 100 | 0.01% | 1 | Tight stablecoin |
| 400 | 0.04% | 4 | Major pairs (SOL/USDC) |
| 3000 | 0.30% | 64 | Standard pairs |
| 10000 | 1.00% | 128 | Volatile / exotic pairs |

### Range strategies

| Strategy | Width | Best for | Rebalance |
|----------|-------|----------|-----------|
| Tight | ±2% | Stablecoin pairs | Rarely |
| Medium | ±5% | Correlated (SOL/JitoSOL) | Weekly |
| Wide | ±10% | Volatile (SOL/USDC) | Bi-weekly |
| Full range | `-443636 → 443636` | Set-and-forget | Never |

Tick conversion uses the SDK: `PriceMath.priceToTickIndex(price, decA, decB)` and `PriceMath.tickIndexToPrice(tick, decA, decB)`. Align ticks: `Math.floor(raw / tickSpacing) * tickSpacing` for lower, `Math.ceil(...)` for upper.

### Canonical bridge pools

For multi-hop routes and dust swaps, these are the deepest pools for common bridge pairs:

| Pair | Fee | Pool |
|------|-----|------|
| SOL/USDC | 0.04% | `Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE` |
| USDC/USDT | 0.01% | `4fuUiYxTQ6QCrdSq9ouBYcTM7bqSwYTSyLueGZLTy4T4` |
| SOL/JitoSOL | 0.01% | `Hp53XEtt4S8SvPCXarsLSdGfZBuUr5mMmZmX2DRNXQKp` |
| SOL/USDT | 0.02% | `FwewVm8u6tFPGewAyHmWAqad9hmF7mvqxK4mJ7iNqqGC` |
| cbBTC/WBTC | 0.01% | `4v8ufj8Hj7UvFgtofQJAtzUud5xomwZfEqfCTHZ4wM72` |
| PYUSD/USDC | 0.01% | `9tXiuRRw7kbejLhZXtxDxYs2REe43uH2e7k1kocgdM9B` |
| USDG/USDC | 0.01% | `9RqDTfwCx2SgxsvKpspQHc38HUo3B6hRd3oR9JR966Ps` |

For other pairs, discover via `/pools/search?query=TOKEN/USDC`.

---

## Token-2022 Pools

Pools where at least one side (or the position NFT) uses the Token-2022 program need V2 instructions. The high-level SDK methods (`pool.swap`, `position.collectFees`, `pool.closePosition`, etc.) handle this internally — use them and it just works. Drop to raw instructions only if bundling custom flows.

Detect a mint's program:
```typescript
const prog = (await connection.getAccountInfo(mint))!.owner;
// equals TOKEN_PROGRAM_ID or TOKEN_2022_PROGRAM_ID
```

V1 → V2 instruction map (raw-Anchor flows only):

| V1 | V2 (mixed / Token-2022) |
|----|-------------------------|
| `collectFees` | `collectFeesV2` |
| `collectReward` | `collectRewardV2` |
| `increaseLiquidity` | `increaseLiquidityV2` |
| `decreaseLiquidity` | `decreaseLiquidityV2` |
| `swap` | `swapV2` |

V2 instructions take `tokenProgramA`, `tokenProgramB`, `tokenMintA`, `tokenMintB`, and `memoProgram` (`MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr`) accounts. ATA creation: pass the correct program per mint — `createAssociatedTokenAccountIdempotentInstruction(payer, ata, owner, mint, tokenProgram)`.

---

## Raw Anchor Fallback

The high-level helpers cover nearly everything. Drop to raw Anchor when:

- Installed SDK version is missing a method from the dependency table above
- You need to bundle multiple SDK operations into one transaction
- You're debugging a specific on-chain error and need instruction-level control

Fetch accounts and build instructions directly:

```typescript
const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint).publicKey;
const position = await (ctx.program.account as any).position.fetch(posPda);
const pool = await (ctx.program.account as any).whirlpool.fetch(position.whirlpool);

const tokenProgA = (await connection.getAccountInfo(pool.tokenMintA))!.owner;
const tokenProgB = (await connection.getAccountInfo(pool.tokenMintB))!.owner;

// `whirlpool` (relations:[position]) and `memoProgram` (address-constrained)
// are auto-resolved by Anchor's typed builder — omit them from .accounts().
const ix = await ctx.program.methods
  .collectFeesV2(null)
  .accounts({
    positionAuthority: wallet.publicKey,
    position: posPda,
    positionTokenAccount,
    tokenMintA: pool.tokenMintA, tokenMintB: pool.tokenMintB,
    tokenOwnerAccountA, tokenOwnerAccountB,
    tokenVaultA: pool.tokenVaultA, tokenVaultB: pool.tokenVaultB,
    tokenProgramA: tokenProgA, tokenProgramB: tokenProgB,
  })
  .remainingAccounts([])
  .instruction();
```

Decode a program error code from the IDL:
```typescript
import idl from "@orca-so/whirlpools-sdk/dist/artifacts/whirlpool.json" with { type: "json" };
const err = idl.errors.find((e: any) => e.code === parseInt("17b5", 16));
// { code: 6069, name: "PriceSlippageOutOfBounds", msg: "Price outside slippage bounds" }
```

See [examples/close-position-anchor.md](examples/close-position-anchor.md) for a complete multi-instruction close using raw Anchor + V2.

---

## Gotchas

Read before writing code. These bite agents who don't.

### 1. All numeric fields are strings

Both REST and Beachhouse return numeric values as JSON strings. Cast with `Number()` (TypeScript) or `float()` (Python) before math or comparisons.

- REST: `Number(pool.tvlUsdc)`, `Number(stats["7d"].yieldOverTvl)` — `feeRate` is already a number, but most others are strings.
- Beachhouse: `Number(point.tvl)`, `Number(point.baseAmount)`, `Number(point.volumeBase)`, `Number(point.volumeQuote)`, `Number(point.totalVolumeUsd)` — **every timeseries field is a string**.
- Common failure: `tvls.filter((x) => typeof x === "number")` silently drops EVERY row because they're all strings. Cast first, then filter.

### 2. A/B pool price ≠ USD price of base

For LP range analysis, use the pool ratio `volumeQuote / volumeBase` (B per A), not `volumeBaseUsd / volumeBase` (which is base-token USD price). Identical for USDC-quoted pools; divergent for LST pairs (SOL/JitoSOL), BTC pairs (cbBTC/WBTC), etc. See [Two Different "Prices"](#two-different-prices-from-volume-data).

### 3. Beachhouse blocks default Python urllib User-Agent

Cloudflare returns 403 for the default urllib UA. Set a browser-like header:

```python
import urllib.request
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = json.loads(urllib.request.urlopen(req).read())
```

`curl` and Node `fetch` work without extra headers.

### 4. Beachhouse response is double-nested

`response.data.data[]` — outer `data` wraps the payload; inner `data` is the timeseries array. REST is single-nested: `response.data[]` or `response.data.<field>`.

### 5. `priceDelta` is NOT volatility

It's the net price change over the period. A choppy week ending flat shows `priceDelta ≈ 0` despite high realized volatility. For actual volatility, use log returns on the A/B price from Beachhouse: `stddev(ln(price[i]/price[i-1]))`.

### 6. Cross-asset USD conversion: divide, don't multiply

Pool price `P = quote / base`. For a pair like SOL/whETH where A=SOL, B=whETH, `P ≈ 0.037` means "0.037 whETH per SOL". If you know `SOL_USD`, then `whETH_USD = SOL_USD / P`, NOT `SOL_USD * P`. Multiplying gives ~$3 for whETH instead of ~$2,275. Bites anyone doing HODL comparisons or USD-denominated MC projections on non-USDC pools.

### 7. Concentrated liquidity fee share scales with range width

A narrower position earns proportionally more fees per in-range day. Rough approximation: `relative_fee_share ∝ 1 / width`. Do NOT model concentrated LP fees as `deposit/TVL × pool_fees` — that's the full-range approximation and severely underestimates tight-range earnings (and overestimates if you assume a tight range earns the same as full-range). Calibrate against a baseline width (e.g. ±20% ≈ pool average) and scale from there.

### 8. This skill deliberately does not project LP yield

Retrospective Yield reports actual historical fee earnings during stable periods. Full LP-vs-HODL Monte Carlo with fee attribution requires deep CLMM math (liquidity-from-deposit inversion, active-liquidity attribution, concentration scaling) and is high-variance even when done correctly. If you build one, verify against a known baseline (e.g. the retrospective yield on a stablecoin pair) before reporting numbers.

---

## Orca REST API Reference

Base: `https://api.orca.so/v2/solana`

### Endpoints

| Path | Purpose | Response shape |
|------|---------|----------------|
| `GET /pools` | List pools. Params: `orderBy=tvlUsdc\|volume24hUsdc`, `orderDirection=asc\|desc`, `limit` | `{ data: [...pools] }` |
| `GET /pools/search?query=<pair-or-addr>` | Search by pair or address | `{ data: [...pools] }` |
| `GET /pools/{address}` | Single pool detail | `{ data: {...pool} }` |
| `GET /protocol` | Protocol-wide stats (flat, no `data` wrapper) | `{ volume24hUsdc, fees24hUsdc, tvl }` |
| `GET /tokens/search?query=<symbol>` | Token lookup | `{ data: [...tokens] }` |

### Pool Response Key Fields

```
address           - Pool address (string)
feeRate           - Fee in basis points × 100 (e.g. 300 = 0.03%)
price             - Current price as string
tvlUsdc           - TVL in USD as string
tickSpacing       - 1 (stables), 4 (majors), 64 (standard), 128 (volatile)
tokenA / tokenB   - { symbol, name, decimals, address }
tokenBalanceA/B   - Raw integer token balance (÷ 10^decimals)
```

### Pool Stats (available on every pool)

Each pool has `stats.24h`, `stats.7d`, `stats.30d`:

```
volume             - Total volume in USD (string)
fees               - Total fees generated (string)
rewards            - Total reward emissions in USD (string)
yieldOverTvl       - Fee yield as fraction of TVL (e.g. 0.0019 = 0.19%)
volumeDelta        - Volume change vs previous period (24h and 7d only)
feesDelta          - Fees change rate (24h and 7d only)
tvlDelta           - TVL change rate (24h and 7d only)
priceDelta         - Price change rate (24h and 7d only)
yieldOverTvlDelta  - Yield change rate (24h and 7d only)
```

---

## Beachhouse API Reference

Base: `https://stats-api.mainnet.orca.so`

Daily timeseries for up to 6 months. Coverage: top 50 pools by TVL. Use for realized volatility (VWAP log returns), ATR, historical range analysis, and retrospective yield.

### Endpoints

**`GET /api/pools/{address}/tvl?time_from=<unix>&time_to=<unix>&type=1D`**

```json
{ "data": { "data": [
  { "tvl": "1234567.89", "baseAmount": "500.5", "quoteAmount": "75000.0", "unixTime": 1700000000 }
] } }
```

**`GET /api/pools/{address}/volume?time_from=<unix>&time_to=<unix>&type=1D`**

```json
{ "data": { "data": [
  { "totalVolumeUsd": "500000.0", "volumeBase": "3000.0", "volumeQuote": "450000.0",
    "volumeBaseUsd": "250000.0", "volumeQuoteUsd": "250000.0", "unixTime": 1700000000 }
] } }
```

**Resolutions**: `1H`, `1D`, `1W`, `1M`, `1Y`. `baseAmount` and `quoteAmount` are human-readable (already decimal-adjusted). 6-month window: `time_from = now - 180 * 86400`, `time_to = now`.

### Two Different "Prices" From Volume Data

| Formula | Meaning | Use when |
|---------|---------|----------|
| `Number(volumeQuote) / Number(volumeBase)` | **A/B pool ratio** — token B per token A (actual trade execution ratio) | Pool-internal price for in-range analysis, ATR of the pair, realized vol of the actual LP position. **Correct for all pools**, especially LST pairs (SOL/JitoSOL) and BTC wrapped pairs (cbBTC/WBTC). |
| `Number(volumeBaseUsd) / Number(volumeBase)` | **USD price of the base token** | USD-denominated price context (e.g. "what was SOL worth each day"). For USDC-quoted pools these are identical; for LST/BTC pairs they diverge — USD price reflects the dollar value, not the pool ratio. |

For LP range sizing and in-range checking, **always use `volumeQuote / volumeBase`**. For "what was the price in USD" context, use `volumeBaseUsd / volumeBase`.

---

## Snorkel API Reference

Base: `https://pools-api.mainnet.orca.so`

Read-only multi-hop swap quoting. Returns route splits across pools so you can pick the deepest path before executing each leg via the SDK.

**`GET /swap-quote?from=<mint>&to=<mint>&amount=<base-units>&slippageBps=<bps>&amountIsInput=true`**

Required params: `from` (input mint), `to` (output mint), `amount` (base units), `slippageBps`, `amountIsInput` (`true` for exact-input, `false` for exact-output). Snorkel returns `400 missing field "from"` if you use `inputMint`/`outputMint` — those are SDK names, not API names.

Response shape:

```
{ data: {
    request: { from, to, amount, amountIsInput, ... },
    swap:    { inputAmount, outputAmount, split: [ [ ...hops ] ] },
    num_measured, optimal_amount_deviation, price_impact
}, meta }
```

`split` is an array of routes; each route is an array of hops (pools chained sequentially). For single-route swaps, `split.length === 1`; for split routes (Snorkel sharded the input across pools), `split.length > 1`.

Rate limit: 429s on hot loops. Space iterated calls ≥ 200–500 ms. For single-pool quotes, `swapQuoteByInputToken` from the SDK avoids the API entirely.

---

## Key Formulas

| Formula | Expression |
|---------|------------|
| Fee % | `feeRate / 10000` (e.g. 400 → 0.04%) |
| APR (7d) | `Number(stats["7d"].yieldOverTvl) / 7 * 365 * 100` |
| APR (30d) | `Number(stats["30d"].yieldOverTvl) / 30 * 365 * 100` |
| A/B pool price | `Number(volumeQuote) / Number(volumeBase)` |
| USD price of base | `Number(volumeBaseUsd) / Number(volumeBase)` |
| Realized volatility | `stddev(ln(price[i]/price[i-1]))` (A/B price for LP; USD price for market context) |
| ATR (14d) | `mean(|price[i] - price[i-1]|)` over last 14 daily A/B prices |
| Daily fees (pool) | `Number(totalVolumeUsd) × (feeRate / 10000 / 100)` |
| Vol/TVL (24h) | `Number(stats["24h"].volume) / Number(tvlUsdc)` — higher = more active |
| Daily earning (full-range approx) | `deposit × Number(stats["7d"].yieldOverTvl) / 7` |

---

## Common Token Mints

Token program is classic SPL (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`, shown as `cls`) unless marked `T22` (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`). For any mint not in this table, resolve dynamically with `(await connection.getAccountInfo(mint))!.owner`.

| Symbol | Decimals | Prog | Mint |
|--------|----------|------|------|
| SOL (wSOL) | 9 | cls | `So11111111111111111111111111111111111111112` |
| USDC | 6 | cls | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | 6 | cls | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| ORCA | 6 | cls | `orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE` |
| BONK | 5 | cls | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` |
| JitoSOL | 9 | cls | `J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn` |
| JupSOL | 9 | cls | `jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v` |
| INF | 9 | cls | `5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm` |
| JUP | 6 | cls | `JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN` |
| JLP | 6 | cls | `27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4` |
| whETH | 8 | cls | `7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs` |
| cbBTC | 8 | cls | `cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij` |
| WBTC | 8 | cls | `3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh` |
| xBTC | 8 | cls | `CtzPWv73Sn1dMGVU3ZtLv9yWSyUAanBni19YWDaznnkn` |
| ZEC | 8 | cls | `A7bdiYdS5GjqGFtxf17ppRHtDKPkkRqbKtR27dxvQXaS` |
| PYUSD | 6 | **T22** | `2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo` |
| USDG | 6 | **T22** | `2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH` |
| CASH | 6 | **T22** | `CASHx9KJUStyftLFWGvEVf59SGeG9sh5FfcnZMVPCASH` |
| PUMP | 6 | **T22** | `pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn` |
| syrupUSDC | 6 | cls | `AvZZF1YaZDziPY2RCK4oJrRVrbN3mTD9NL24hPeaZeUj` |
| hyUSD | 6 | cls | `5YMkXAYccHSGnHn9nob9xEvv6Pvka9DZWH7nTbotTu9E` |
| USX | 6 | cls | `6FrrzDk5mQARGc1TDYoyVnSyRdds1t4PbtohCD6p3tgG` |
| eUSX | 6 | cls | `3ThdFZQKM6kRyVGLG48kaPg5TRMhYMKY1iCRa9xop1WC` |
| ONyc | 9 | cls | `5Y8NV33Vv7WbnLfq3zBcKSdYPrk7g2KoiQoe7M2tcxp5` |
| EURC | 6 | cls | `HzwqbKZw8HxMN6bF2yFZNrht3c2iXXzpKcFu7uBEDKtr` |
| TRUMP | 6 | cls | `6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN` |

> Orca pools use the wSOL mint (`So111…112`) to represent SOL. Native SOL is the chain's native asset, not an SPL token — the SDK handles wrap/unwrap automatically.

---

## Examples

| File | Description |
|------|-------------|
| [scan-pools.md](examples/scan-pools.md) | Scan and rank top Orca pools by TVL |
| [pool-detail.md](examples/pool-detail.md) | Full breakdown of a single pool |
| [compare-fee-tiers.md](examples/compare-fee-tiers.md) | Compare fee tiers for a trading pair |
| [pair-discovery.md](examples/pair-discovery.md) | Find all pools for a specific token |
| [stability-rankings.md](examples/stability-rankings.md) | Rank pools by 6-month Beachhouse stability score |
| [lp-range-analysis.md](examples/lp-range-analysis.md) | ATR-based LP range sizing from Beachhouse VWAP |
| [range-projection.md](examples/range-projection.md) | Monte Carlo using Beachhouse realized volatility |
| [price-range-history.md](examples/price-range-history.md) | Historical price bands and containment |
| [yield-projection.md](examples/yield-projection.md) | Retrospective yield from Beachhouse volume and TVL |
| [monitor-pool.md](examples/monitor-pool.md) | Real-time pool monitoring with price/TVL deltas |
| [open-position.md](examples/open-position.md) | Open a medium-range SOL/USDC position |
| [manage-position.md](examples/manage-position.md) | Increase, decrease, close |
| [collect-fees.md](examples/collect-fees.md) | Collect fees and rewards |
| [close-position-anchor.md](examples/close-position-anchor.md) | Raw-Anchor close (Token-2022 safe) |
| [quote.md](examples/quote.md) | Read-only swap quote via Snorkel |
| [swap.md](examples/swap.md) | SDK-native swap |

---

## Fresh Context

Treat referenced Orca docs, live API responses, and the pinned SDK's type definitions as the source of truth over this file. If the live response or SDK signatures diverge from examples here, follow live and surface the mismatch to the user. Re-fetch `/pools/{address}` or Beachhouse data per request — don't cache across unrelated queries. Re-fetch pool state with `pool.refreshData()` before any quote — never reuse cached `sqrtPrice` across unrelated operations.
