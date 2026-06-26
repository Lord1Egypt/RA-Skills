# Stability Pool Concepts

Key concepts for understanding Stability Pools on the Indigo Protocol.

## What are Stability Pools?

Stability pools are a core mechanism of the Indigo Protocol that serve two purposes:

1. **Liquidation buffer** — iAssets deposited into stability pools are used to liquidate undercollateralized CDPs
2. **Reward earning** — depositors earn ADA from liquidation gains and INDY token incentives

Each iAsset (iUSD, iBTC, iETH, iSOL) has its own stability pool.

## How Stability Pools Work

1. Users deposit iAssets into the pool (e.g., deposit iUSD into the iUSD stability pool)
2. When a CDP is liquidated, the pool's iAssets are burned to cover the CDP's debt
3. In return, the pool receives the liquidated CDP's ADA collateral (at a discount)
4. The ADA gains are distributed proportionally to all depositors

## Account Lifecycle

1. **Create** — `create_sp_account` deposits iAssets and creates an account
2. **Adjust** — `adjust_sp_account` increases or decreases the deposit
3. **Close** — `close_sp_account` withdraws everything and claims rewards

## Pending Requests

Deposit adjustments and withdrawals go through a **two-step process**:

1. User submits a request (adjust or close) → creates a **pending request**
2. The request must be **processed** (`process_sp_request`) in a subsequent transaction
3. Alternatively, the request can be **cancelled** (`annul_sp_request`) before processing

This two-step mechanism exists for on-chain safety, ensuring that pool state is consistent during liquidation epochs.

## Rewards

Stability pool depositors earn two types of rewards:

| Reward Type | Source | Description |
|-------------|--------|-------------|
| ADA gains | Liquidations | When CDPs are liquidated, depositors receive the excess collateral |
| INDY rewards | Protocol incentives | INDY governance tokens distributed to stability pool participants |

Rewards accumulate over time and are claimed when the account is closed.

## Decimal Precision

| iAsset | Decimals | 1 unit example |
|--------|----------|----------------|
| iUSD | 6 | 1 iUSD = 1,000,000 |
| iBTC | 8 | 1 iBTC = 100,000,000 |
| iETH | 18 | 1 iETH = 1,000,000,000,000,000,000 |
| iSOL | 9 | 1 iSOL = 1,000,000,000 |

All amounts in MCP tool calls use the smallest unit (no decimal points).
