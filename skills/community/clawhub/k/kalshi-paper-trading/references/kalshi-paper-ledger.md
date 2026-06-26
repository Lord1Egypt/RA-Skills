# Kalshi Paper Ledger Proposal

## Why

The generic paper trader is a poor fit for Kalshi contracts.

Main mismatches:

- Kalshi quotes are naturally cent-denominated, while the generic ledger assumes dollar prices.
- Kalshi positions are binary contracts with bounded settlement values of `0` or `100` cents.
- Open risk is contract premium and event exposure, not token-style stop-distance risk.
- Missing live marks should not silently collapse open Kalshi positions to zero contribution.

This proposal defines a small Kalshi-native paper ledger and CLI.

## Goals

- Store Kalshi executions in native units without ambiguity.
- Keep realized and unrealized PnL mathematically correct.
- Support reconciliation against finalized markets.
- Support paper-only scouting and execution workflows used by Kalshi-focused skills.
- Make it hard to mix cents and dollars incorrectly.

## Non-Goals

- Live Kalshi order placement.
- General multi-venue abstraction.
- Token-style stop and TP automation in the first version.

## Core Decision

Store Kalshi execution prices as integer cents in the ledger.

Rules:

- `price_cents` is always an integer in `[0, 100]`
- reporting may derive `price_dollars = price_cents / 100`
- settlement is stored as:
  - `100` cents for the winning side
  - `0` cents for the losing side

This keeps storage aligned with Kalshi-native semantics and avoids the bug class where raw cents are mixed with dollar settlement values.

## Data Model

### Accounts

One row per paper account.

Suggested fields:

- `id`
- `name`
- `base_currency`
- `starting_balance_usd`
- `created_at`

### Executions

Append-only execution log.

Suggested fields:

- `id`
- `account_id`
- `market_ticker`
- `event_ticker`
- `series_ticker`
- `contract_side`
  - `YES`
  - `NO`
- `action`
  - `BUY`
  - `SELL`
- `contracts`
- `price_cents`
- `fee_usd`
- `source`
  - `manual`
  - `kalshi-openapi`
  - `reconcile`
- `note`
- `meta_json`
- `created_at`

### Market Marks

Latest known market state for valuation and reconciliation.

Suggested fields:

- `market_ticker`
- `status`
  - `open`
  - `closed`
  - `finalized`
- `close_time_utc`
- `settlement_side`
  - `YES`
  - `NO`
  - `NULL` when not finalized
- `yes_bid_cents`
- `yes_ask_cents`
- `last_yes_trade_cents`
- `mark_method`
  - `mid`
  - `bid`
  - `last_trade`
  - `settlement`
  - `unknown`
- `mark_cents`
- `raw_json`
- `updated_at`

## Position Model

An open position is grouped by:

- `account_id`
- `market_ticker`
- `contract_side`

Do not reuse `LONG` and `SHORT` plus `mint`.
For Kalshi, the natural exposure is:

- buy YES contracts
- buy NO contracts

That keeps settlement and valuation simple.

## Accounting Rules

### Cost Basis

For a `BUY`:

- cash decreases by `contracts * price_cents / 100 + fee_usd`

For a `SELL`:

- cash increases by `contracts * price_cents / 100 - fee_usd`

### Realized PnL

Use average-cost matching in v1.

For a closed portion:

- `realized_pnl_usd = contracts_closed * (exit_cents - avg_entry_cents) / 100 - allocated_open_fees - close_fee`

This formula is the same for YES and NO positions when the position is keyed by `contract_side`.

### Settlement

If market finalizes:

- winning `contract_side` settles at `100`
- losing `contract_side` settles at `0`

Settlement can be recorded as a synthetic `SELL` execution with source `reconcile`, or as a separate settlement event. For MVP, a synthetic sell is simpler.

### Mark-to-Market

Preferred valuation order:

1. midpoint of `yes_bid_cents` and `yes_ask_cents`
2. conservative bid-side exit value
3. last trade
4. cost basis with stale warning

For YES positions:

- mark from YES-side market fields

For NO positions:

- derive NO mark as `100 - yes_mark_cents` when direct NO mark is unavailable

### Equity

Expose all of these separately:

- `cash_usd`
- `realized_pnl_usd`
- `unrealized_pnl_usd`
- `open_cost_basis_usd`
- `open_mark_value_usd`
- `max_loss_remaining_usd`
- `equity_usd`

`equity_usd` should be:

- `cash_usd + open_mark_value_usd`

This is clearer than treating missing marks as zero without explanation.

## Risk Model

Remove token-style `--max-risk-pct` from Kalshi paper flows.

Use Kalshi-native controls instead:

- `max_cost_usd_per_trade`
- `max_contracts_per_trade`
- `max_open_premium_usd`
- `max_market_exposure_usd`
- `max_event_exposure_usd`
- `max_series_exposure_usd`
- `min_cash_reserve_usd`

These are easier to reason about than stop-based risk for binary contracts.

## CLI Surface

Suggested MVP commands:

- `init`
- `status`
- `buy`
- `sell`
- `mark`
- `reconcile`
- `review`

### `init`

Example:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts init \
  --account kalshi \
  --starting-balance-usd 1000
```

### `buy`

Example:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts buy \
  --account kalshi \
  --market KXBTC-26MAR1317-B69750 \
  --event KXBTC-26MAR1317 \
  --series KXBTC \
  --side YES \
  --contracts 15 \
  --price-cents 84
```

### `sell`

Example:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts sell \
  --account kalshi \
  --market KXBTC-26MAR1317-B69750 \
  --side YES \
  --contracts 15 \
  --price-cents 91
```

### `mark`

Writes current market state and derived mark:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts mark \
  --market KXBTC-26MAR1317-B69750 \
  --yes-bid-cents 84 \
  --yes-ask-cents 86 \
  --status open
```

### `reconcile`

Reads market status from Kalshi OpenAPI and settles finalized positions.

Example:

```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts reconcile \
  --account kalshi \
  --market KXBTC-26MAR1317-B69750 \
  --status finalized \
  --winning-side YES
```

### `status`

Should show:

- account summary
- cash
- realized and unrealized PnL
- open positions with cost basis, mark, stale-mark flag, and expiry
- per-event exposure rollup

## Integration

Kalshi-focused scouting skills should stop calling the generic paper trader for Kalshi.

Instead:

- discovery still uses Kalshi OpenAPI read scripts
- paper execution calls the Kalshi-specific paper CLI
- all price values passed to the new CLI should be raw Kalshi cents or `*_dollars` normalized once at the adapter boundary

Preferred adapter rule:

- if the API response exposes `*_dollars`, convert to integer cents once before writing to the ledger
- otherwise use raw Kalshi cent fields directly

The new ledger should reject:

- negative `price_cents`
- `price_cents > 100`
- non-integer cent values

## Migration Plan

### Phase 1

- Add the new Kalshi-specific ledger and CLI.
- Leave generic paper trading unchanged for token strategies.
- Update Kalshi workflow instructions to use the new CLI for paper operations.

### Phase 2

- Add mark refresh and reconciliation helpers around Kalshi OpenAPI.
- Add tests covering settlement, stale marks, and YES and NO valuation.

### Phase 3

- Migrate or archive old Kalshi rows from the generic paper ledger.
- Add a one-time validation script to detect impossible price values like `84` dollars for binary contracts.

## Validation Rules

Hard validation in the new CLI:

- `contracts > 0`
- `price_cents` integer in `[0, 100]`
- settlement side required for finalized markets
- cannot sell more contracts than currently open for the same `market_ticker + contract_side`

Soft warnings:

- missing live mark
- stale market mark
- mark outside bid and ask
- open exposure concentrated in one event or series

## Open Questions

- Whether v1 should support both average-cost and FIFO accounting
- Whether to persist raw OpenAPI snapshots in the ledger or only in external reports
- Whether `SELL` should be allowed before expiry for partial profit-taking in MVP, or only settlement plus full close

## Recommendation

Build a dedicated Kalshi paper ledger rather than extending the generic paper trader again.

That gives us:

- correct units
- correct settlement math
- clearer exposure controls
- less cross-venue complexity
- better failure modes for missing Kalshi marks
