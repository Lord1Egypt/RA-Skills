# CDP Concepts

Key concepts for understanding Collateralized Debt Positions on the Indigo Protocol.

## What is a CDP?

A Collateralized Debt Position (CDP) is a smart contract that holds ADA as collateral and allows users to mint synthetic assets (iAssets) against it. The minted iAssets represent debt that must be repaid to reclaim the collateral.

## Collateral Ratio

The collateral ratio is the value of ADA collateral divided by the value of minted iAssets:

```
Collateral Ratio = (Collateral ADA × ADA Price) / (Minted iAssets × iAsset Price) × 100%
```

Each iAsset has a **minimum collateral ratio** (typically 150%). If the ratio falls below this threshold, the CDP becomes eligible for liquidation.

## iAssets

Indigo supports four synthetic assets:

| iAsset | Tracks | Decimals |
|--------|--------|----------|
| iUSD | US Dollar | 6 |
| iBTC | Bitcoin | 8 |
| iETH | Ethereum | 18 |
| iSOL | Solana | 9 |

iAssets are minted by opening a CDP and can be traded on Cardano DEXs (SteelSwap, Minswap, etc.) or used in stability pools.

## Health Status Levels

| Status | Meaning | Action |
|--------|---------|--------|
| Healthy | Ratio well above minimum | No action needed |
| Warning | Ratio approaching minimum (within 20%) | Consider depositing more collateral or burning debt |
| Danger | Ratio at or below minimum | Immediate action required — deposit, burn, or face liquidation |

## Liquidation

When a CDP's collateral ratio falls below the minimum:

1. **Anyone** can call `liquidate_cdp` on the undercollateralized CDP
2. The liquidator provides iAssets to cover the CDP's debt
3. The liquidator receives the CDP's collateral **plus a liquidation bonus** (typically 10%)
4. The original CDP owner loses their collateral

## Redemption

Redemption allows iAsset holders to exchange iAssets for ADA collateral at the oracle price, regardless of market price. This helps maintain the iAsset peg.

## Freezing

Freezing a CDP prevents all operations (minting, burning, depositing, withdrawing) until it is unfrozen. This is used as a protective mechanism.

## Merging

CDP owners can merge multiple CDPs of the **same iAsset type** into a single CDP. This combines the collateral and debt of all merged CDPs, simplifying management.

## Leverage

Leveraged CDPs use the ROB (Redemption Order Book) mechanism to amplify exposure:

1. Deposit ADA collateral
2. Mint iAssets against the collateral
3. Sell iAssets for more ADA via DEX
4. Deposit the new ADA as additional collateral
5. Repeat until desired leverage is reached

The `leverage_cdp` tool automates this loop in a single transaction.

## Transaction Signing

All write operations return an **unsigned transaction** in CBOR hex format. The user must:

1. Sign the transaction with their Cardano wallet
2. Submit the signed transaction to the Cardano network
3. Wait for confirmation (typically 1-2 blocks, ~20-40 seconds)
