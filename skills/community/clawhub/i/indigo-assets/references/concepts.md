# Asset Concepts

Key concepts for understanding iAssets and token pricing on the Indigo Protocol.

## iAssets

iAssets are synthetic assets on Cardano that track real-world asset prices. They are minted through CDPs on the Indigo Protocol.

| iAsset | Tracks | Description |
|--------|--------|-------------|
| iUSD | US Dollar | Synthetic stablecoin pegged to USD |
| iBTC | Bitcoin | Synthetic Bitcoin exposure on Cardano |
| iETH | Ethereum | Synthetic Ethereum exposure on Cardano |
| iSOL | Solana | Synthetic Solana exposure on Cardano |

## Price Oracles

iAsset prices are determined by on-chain oracles that feed real-world price data to the Indigo smart contracts. Oracle prices are used for:

- CDP collateral ratio calculations
- Liquidation threshold checks
- Redemption valuations
- Interest rate adjustments

## ADA Price

The ADA price is the base currency price used throughout the Indigo Protocol. Since all collateral is denominated in ADA, the ADA/USD price is critical for:

- Determining CDP health (collateral value in USD)
- Calculating TVL in USD terms
- Pricing INDY tokens

## INDY Token

INDY is the governance and utility token of the Indigo Protocol:

- **Governance** — staked INDY grants voting power
- **Staking rewards** — stakers earn protocol fees in ADA
- **Price** — quoted in both ADA (native pair) and USD (derived)

## Interest Rates

Each iAsset has an associated interest rate that affects:

- Cost of maintaining open CDPs (interest accrues on minted debt)
- Stability pool reward distribution
- Protocol revenue generation
