# CDP Liquidation & Recovery

Handle CDP liquidation, redemption, freezing, and merging.

## Tools

### liquidate_cdp

Liquidate an undercollateralized CDP. Caller receives liquidation bonus.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | Liquidator Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

### redeem_cdp

Redeem iAssets against a CDP at oracle price.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to redeem |

### freeze_cdp

Freeze a CDP to prevent further operations.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

### merge_cdps

Merge multiple CDPs of the same iAsset type into a single position.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpRefs` | `array` | Yes | Array of CDP UTxO references (txHash + outputIndex) |

## Examples

### Liquidate an undercollateralized CDP

Liquidate a CDP that has fallen below the minimum collateral ratio to earn the liquidation bonus.

**Prompt:** "Liquidate CDP abc123...def"

**Workflow:**
1. Call `analyze_cdp_health({ cdpTxHash: "abc123...def", cdpOutputIndex: 0 })` to confirm it is liquidatable
2. Call `liquidate_cdp({ address: "addr1qx...liq", cdpTxHash: "abc123...def", cdpOutputIndex: 0 })`
3. Returns unsigned transaction — liquidator provides iAssets to cover debt, receives collateral + bonus

**Sample response:**
```
Liquidation ready.
CDP: abc123...def
Debt covered: 1,000 iUSD
Collateral received: 2,500 ADA (includes 10% bonus)
Transaction ready for signing.
```

### Merge multiple CDPs

Combine several CDPs of the same iAsset type into one for easier management.

**Prompt:** "Merge my three iUSD CDPs into one"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to list all iUSD CDPs
2. Call `merge_cdps({ address: "addr1qx...abc", cdpRefs: [{ txHash: "aaa...", outputIndex: 0 }, { txHash: "bbb...", outputIndex: 0 }, { txHash: "ccc...", outputIndex: 0 }] })`
3. Returns unsigned transaction — merges collateral and debt into a single CDP

**Sample response:**
```
Merge ready.
Merging 3 iUSD CDPs:
  CDP #42: 2,000 ADA / 500 iUSD
  CDP #78: 3,000 ADA / 800 iUSD
  CDP #91: 1,500 ADA / 300 iUSD
Result: 6,500 ADA / 1,600 iUSD (ratio: 203%)
```

### Freeze a CDP

Freeze a CDP to temporarily prevent any operations on it.

**Prompt:** "Freeze my iBTC CDP"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find the iBTC CDP
2. Call `freeze_cdp({ address: "addr1qx...abc", cdpTxHash: "abc123...def", cdpOutputIndex: 0 })`
3. Returns unsigned transaction — once submitted, the CDP cannot be modified until unfrozen

**Sample response:**
```
Freeze ready.
CDP: abc123...def (iBTC)
Status will change to: Frozen
No further operations will be possible until unfrozen.
```

## Example Prompts

- "Find liquidatable CDPs for iUSD"
- "Liquidate the most undercollateralized CDP"
- "Merge all my iUSD CDPs"
- "Freeze my CDP to protect it"
- "Redeem 500 iUSD against a CDP"
