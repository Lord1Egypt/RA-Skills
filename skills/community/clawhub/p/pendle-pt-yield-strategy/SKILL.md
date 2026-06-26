---
name: pendle-pt-yield-strategy
description: Pendle PT fixed-yield strategy for market scanning, ranking, position tracking, maturity monitoring, and execution planning. Prefer managed wallet execution through Privy or a similar policy-controlled wallet backend, and otherwise fall back to manual user-executed transactions. Use when the user wants to research Pendle PT opportunities, choose stable-ish PT markets, monitor active PT positions, or prepare Pendle PT deposit, redeem, withdraw, and rollover actions with explicit confirmation and clear wallet-path disclosures.
---

# Pendle PT Yield Strategy

Pendle PT strategy skill for fixed-yield workflows built around Principal Tokens.

This publishable package is intentionally scoped to:
- **analysis / monitoring**
- **execution planning**
- **managed-wallet-oriented operation guidance**
- **manual execution fallback**

It does **not** bundle raw secret-key signing code.
It does **not** bundle direct transaction-submission helpers that read local
wallet secrets.

---

## Wallet philosophy

Default to the safest practical wallet path.

Priority order:
1. **Managed wallet with policy controls** — preferred
2. **Manual user-executed transaction flow** — fallback
3. **Do not default to raw secret-key runtime signing in this public package**

This public package is designed to avoid normalizing secret key export or
runtime secret-key injection as the standard path.

---

## Preferred wallet path: Privy or another managed wallet layer

The preferred execution model for this skill is a managed wallet system with
policy controls, spend limits, and explicit operator setup.

Use a managed wallet provider such as **Privy** when available.
That is the preferred deployment pattern for agentic execution.

Why this is preferred:
- avoids normalizing raw secret key export as the default
- supports policy-based controls and safer operational boundaries
- is a better fit for production agent workflows
- maps better to the security posture expected for agentic onchain systems

### Current behavior of this package

This package helps the agent:
- scan and rank markets
- plan deposits, redeems, exits, and rollovers
- track positions in local JSON state
- monitor maturities and prepare the next action
- clearly state the expected managed-wallet or manual-execution path

Actual transaction submission should happen through:
- a managed wallet backend such as Privy, orchestrated by the host environment
- or a manual user-executed wallet flow

If the host environment already has the `privy` skill installed, prefer using
that wallet layer for transaction execution and use this skill for Pendle
market/position logic plus execution planning.

---

## Supported execution modes

### Mode 1 — Managed wallet execution via Privy or equivalent
**Preferred.**

Use this when the runtime has:
- a managed agent wallet system
- policy controls / spending limits
- server-side transaction execution with guardrails

In this mode, this skill should:
1. scan / rank the market
2. preview the intended Pendle action
3. ask for explicit confirmation
4. route execution through the managed wallet backend
5. update `data/positions.json`

When `privy` skill is available, prefer that integration path.

### Mode 2 — Manual user-executed transaction flow
**Fallback.**

Use this when no managed wallet is configured.

In this mode, this skill should:
1. scan / rank the market
2. preview amount, APY, maturity, and slippage
3. prepare the next action or transaction plan
4. ask the user to submit via their wallet
5. record the position after execution is confirmed

---

## Required disclosures before execution

Before execution or execution planning, the agent must make these points clear:

1. **This action may lead to a real onchain transaction.**
2. **The wallet path being used must be stated clearly**:
   - managed wallet backend
   - manual external wallet execution
3. **Gas costs and slippage apply.**
4. **PT yield is fixed only if held to maturity.**
5. **Underlying asset risk still matters.**
6. **Early exit may realize less than maturity value.**

Never blur the line between planning and execution.

---

## Safety and confirmation rules

### Hard rule
Do not present a transaction as already executed unless the host environment or
user confirms it actually happened.

### Confirmation standard
Require a clear confirmation such as:
- `Confirm Pendle deposit`
- `Confirm Pendle redeem`
- `Confirm Pendle withdraw`
- `Confirm Pendle rollover`

The confirmation should come **after** the user has seen:
- market / position name
- chain
- amount in / amount out estimate
- slippage or price impact estimate
- maturity date
- notable risks
- wallet path that will be used

### Hard stops
Do not proceed with execution planning as if it were executable if:
- the quote / route API fails
- liquidity is too thin for the intended size
- slippage exceeds threshold
- the wallet path is unclear
- the user has not clearly authorized the next step

---

## What this skill can do

### Analysis and monitoring
- scan active Pendle PT markets
- rank stable-ish PT markets by APY, liquidity, risk, and maturity fit
- compare hold-to-par vs near-par rotation ideas
- track positions in `data/positions.json`
- monitor maturities and identify rollover candidates
- generate status reports and manual action plans

### Execution planning
- preview USDC → PT routes
- prepare PT deposit plans
- prepare PT redemption or PT → USDC exit plans
- prepare rollover flows after maturity
- record and monitor positions after externally confirmed execution

This package is **managed-wallet oriented** and **manual-execution compatible**.
It does not ship secret-key runtime signing code.

---

## Strategy overview

The core loop is: **scan → select → preview → confirm → execute externally or via managed wallet → track → monitor → roll**.

1. Scan active Pendle PT markets
2. Filter for stable-ish underlyings and acceptable maturity windows
3. Rank candidates by APY, liquidity, risk, and execution practicality
4. Preview the intended route and surface trade details
5. State the wallet path that would be used
6. Ask for explicit confirmation before the next step
7. Execute via managed wallet backend or manual external wallet flow
8. Update `data/positions.json`
9. Monitor for maturity or near-maturity and repeat

---

## Parameters and defaults

### Commitment tiers

| Parameter             | Short commitment | Long commitment |
|-----------------------|------------------|-----------------|
| `max_days_to_maturity`| 15               | 100             |
| `min_days_to_maturity`| 1                | 15              |
| `min_apy_threshold`   | 5%               | 10%             |

Default to **long commitment** unless the user explicitly requests short-term
parking or specifies a different preference.

### Market filters

| Parameter               | Default                          | Description |
|--------------------------|----------------------------------|-------------|
| `chains`                 | `ethereum,arbitrum,base`         | Chains to scan |
| `asset_types`            | `stable-major,stable-synthetic,stable-rwa` | Stable subtypes to include |
| `include_non_usd`        | `false`                          | Include EUR / SGD stablecoin PTs |
| `min_liquidity_usd`      | `1000000`                        | Minimum market TVL |
| `max_slippage_pct`       | `2.0`                            | Max acceptable slippage |
| `min_volume_24h_usd`     | `50000`                          | Minimum 24h volume |

---

## Commands

### `scan`
Use the bundled scanning and ranking scripts to find candidates.

Suggested flow:

```bash
cd scripts
python3 scan-markets.py --active-only
python3 rank-markets.py \
  --stable-only \
  --stable-subtype stable-major stable-synthetic stable-rwa \
  --chains ethereum base arbitrum \
  --min-days 1 \
  --max-days 100 \
  --min-liquidity 1000000
python3 report-markets.py --top 20
```

### `deposit`
1. validate the market
2. preview route, APY, maturity, and slippage
3. state which wallet path would be used
4. ask for explicit confirmation
5. if using a managed wallet backend, route execution there
6. otherwise prepare a manual transaction plan and ask the user to sign
7. record the position after execution is confirmed

### `redeem`
1. check if the PT is matured or otherwise ready to exit
2. preview redeem / exit route
3. state which wallet path would be used
4. ask for explicit confirmation
5. if using a managed wallet backend, route execution there
6. otherwise prepare a manual transaction plan and ask the user to sign
7. update `data/positions.json` after execution is confirmed

### `withdraw`
1. preview PT → USDC early exit
2. warn that early exit may realize less than maturity value
3. state which wallet path would be used
4. ask for explicit confirmation
5. prepare or route the exit flow accordingly

### `status`
Read `data/positions.json` and summarize active positions, expected value,
maturity schedule, and aggregate expected yield.

### `monitor`
Use for periodic checks.
Flag matured and soon-to-mature positions, then prepare the next action:
- hold
- redeem
- redeem then roll
- manual review

### `rollover`
1. identify the existing position near maturity
2. scan for the next best candidate
3. preview the combined exit + next entry plan
4. state which wallet path would be used
5. ask for explicit confirmation
6. route to managed wallet backend or prepare a manual step-by-step flow

---

## Files in this skill

| File | Purpose |
|------|---------|
| `SKILL.md` | Strategy instructions and safety rules |
| `data/positions.json` | Active and historical position tracking |
| `data/strategy-config.json` | Saved parameter overrides |
| `scripts/check-slippage.py` | Preview market slippage |
| `scripts/monitor-positions.py` | Check tracked positions for maturity / alerts |
| `scripts/report-status.py` | Generate human-readable position reports |
| `scripts/scan-markets.py` | Scan Pendle PT markets |
| `scripts/rank-markets.py` | Rank PT markets by fit |
| `scripts/report-markets.py` | Render ranked market summaries |
| `references/eligible-underlyings.md` | Stable-ish asset guidance |
| `references/chain-addresses.md` | Chain and token reference data |

---

## Position tracking schema

All positions are stored in `data/positions.json` as a JSON array.

```json
[
  {
    "id": "pos_001",
    "status": "active | redeemed | withdrawn_early | rolling",
    "chain": "ethereum",
    "chain_id": 1,
    "market_address": "0x...",
    "market_name": "PT-sUSDe 25JUN2026",
    "pt_address": "0x...",
    "underlying_asset": "sUSDe",
    "underlying_address": "0x...",
    "deposit_token": "USDC",
    "deposit_amount_usd": 10000.00,
    "deposit_amount_raw": "10000000000",
    "pt_amount_received": "10234000000000000000000",
    "effective_apy_at_entry": 0.112,
    "entry_date": "2026-04-03T14:30:00Z",
    "entry_tx_hash": "0x...",
    "maturity_date": "2026-06-25T00:00:00Z",
    "days_to_maturity_at_entry": 83,
    "expected_value_at_maturity_usd": 10254.00,
    "redemption_date": null,
    "redemption_tx_hash": null,
    "realized_yield_usd": null,
    "withdrawal_date": null,
    "withdrawal_tx_hash": null,
    "realized_pnl_usd": null,
    "rollover_history": [],
    "notes": ""
  }
]
```

---

## Relationship to pendle-pt-research

This skill overlaps with `pendle-pt-research` but is designed to stand on its
own. If both are installed, use the research skill for broader discovery and
this skill for execution-oriented filtering, tracking, and rollover planning.

---

## Portability notes

This package is intentionally portable because it avoids bundling direct secret-
backed signer code. Host environments can:
- route execution through a managed wallet provider such as Privy
- use manual external signing
- adapt host-specific execution tooling outside this package while keeping the
  market and position logic here
