# Leveraged CDP

Open leveraged CDP positions using Redemption Order Book (ROB).

## Tools

### leverage_cdp

Open a leveraged CDP position. Uses ROB mechanism to amplify exposure to an iAsset with a single transaction.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | Target iAsset |
| `collateralAmount` | `string` | Yes | Initial ADA collateral in lovelace |
| `leverageMultiplier` | `number` | Yes | Leverage multiplier (e.g. 2 for 2x) |

## Examples

### Open a 2x leveraged iUSD position

Use leverage to amplify exposure to iUSD with a single transaction instead of manually looping mint-sell-deposit.

**Prompt:** "Open a 2x leveraged CDP for iUSD with 5000 ADA"

**Workflow:**
1. Call `leverage_cdp({ address: "addr1qx...abc", asset: "iUSD", collateralAmount: "5000000000", leverageMultiplier: 2 })`
2. The protocol uses ROB to: open CDP → mint iUSD → sell for ADA → deposit back as collateral → repeat
3. Returns unsigned transaction for signing

**Sample response:**
```
Leveraged CDP ready.
Initial collateral: 5,000 ADA
Effective exposure: ~10,000 ADA worth of iUSD
Leverage: 2x
Collateral ratio: ~200%
Transaction ready for signing.
```

### Open a conservative leveraged position

Use a lower multiplier for reduced risk while still amplifying returns.

**Prompt:** "Open a 1.5x leveraged iBTC position with 10,000 ADA"

**Workflow:**
1. Call `leverage_cdp({ address: "addr1qx...abc", asset: "iBTC", collateralAmount: "10000000000", leverageMultiplier: 1.5 })`
2. Returns unsigned transaction — lower leverage means higher collateral ratio and less liquidation risk

**Sample response:**
```
Leveraged CDP ready.
Initial collateral: 10,000 ADA
Effective exposure: ~15,000 ADA worth of iBTC
Leverage: 1.5x
Collateral ratio: ~267%
Transaction ready for signing.
```

### Understand leverage risks

Check what leverage multiplier is safe given current market conditions.

**Prompt:** "What leverage can I safely use for iETH?"

**Workflow:**
1. Call `get_asset_price({ asset: "iETH" })` to get current price and volatility context
2. Call `get_protocol_params()` to check minimum collateral ratios for iETH
3. Calculate safe leverage based on min ratio: safe_multiplier = min_ratio / (min_ratio - 100%)
4. Present recommendation with risk levels

**Sample response:**
```
iETH Leverage Analysis:
  Min collateral ratio: 150%
  Max theoretical leverage: 3x
  Recommended safe leverage: 2x (200% ratio)
  Conservative: 1.5x (267% ratio)

Higher leverage = higher liquidation risk.
At 3x, a 17% ADA price drop triggers liquidation.
```

## Example Prompts

- "Open a leveraged CDP for iUSD"
- "What's the maximum leverage I can use?"
- "Create a 2x leveraged iBTC position"
- "How risky is 3x leverage on iETH?"
