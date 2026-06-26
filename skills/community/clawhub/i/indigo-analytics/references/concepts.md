# Analytics Concepts

Key concepts for understanding Indigo Protocol analytics and metrics.

## Total Value Locked (TVL)

TVL measures the total amount of assets deposited in the Indigo Protocol. It includes:

| Component | Description |
|-----------|-------------|
| CDP Collateral | ADA locked as collateral in CDPs |
| Stability Pools | iAssets deposited in stability pools |
| Staked INDY | INDY tokens locked in staking positions |

TVL data is sourced from DefiLlama, which aggregates on-chain data.

## APR vs APY

- **APR (Annual Percentage Rate)** — simple interest rate without compounding
- **APY (Annual Percentage Yield)** — effective rate including compounding

Stability pool and staking rewards are quoted in APR. DEX yields are typically quoted in APY since LP rewards can be compounded.

## Pool Types

### Stability Pools
Each iAsset has a dedicated stability pool. Depositors earn:
- ADA from liquidation gains (when CDPs are liquidated)
- INDY incentive rewards

### DEX Liquidity Pools
iAsset trading pairs on Cardano DEXs (Minswap, SundaeSwap, etc.). LPs earn:
- Trading fees from swaps
- Liquidity mining rewards (if applicable)
- Risk: impermanent loss if prices diverge

### INDY Staking
Single-asset staking of INDY tokens. Stakers earn:
- Protocol fees in ADA
- Governance voting power

## Protocol Statistics

Key metrics tracked by `get_protocol_stats`:

- **Active CDPs** — number of open collateralized positions
- **Total minted iAssets** — count of distinct iAsset types with active CDPs
- **Pool utilization** — percentage of available pool capacity in use
- **Collateral distribution** — breakdown of ADA across CDP types

## Data Sources

| Metric | Source |
|--------|--------|
| TVL | DefiLlama (aggregated on-chain data) |
| APR/APY | Indigo Protocol indexer |
| DEX Yields | DEX APIs (Minswap, SundaeSwap, etc.) |
| Protocol Stats | Indigo on-chain data |
