# CDP Health Analysis

Monitor CDP health and liquidation risk.

## Tools

### analyze_cdp_health

Analyze a CDP's collateral ratio, liquidation price, and overall health status. Returns risk level and recommended actions.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

**Returns:** Health analysis with collateral ratio, liquidation price, risk level (healthy/warning/danger), and suggested actions.

### get_all_cdps

List all CDPs in the protocol.

**Parameters:** None

**Returns:** Array of all CDP objects with owner, collateral, minted amount, and ratio.

### get_cdps_by_owner

List CDPs by owner address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owners` | `string[]` | Yes | Array of owner addresses |

### get_cdps_by_address

List CDPs by specific UTxO address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | CDP UTxO address |

## Examples

### Check CDP health before a market move

Analyze your CDP's health ratio to see how close you are to liquidation.

**Prompt:** "How healthy is my iUSD CDP?"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find user's CDPs
2. Call `analyze_cdp_health({ cdpTxHash: "abc123...def", cdpOutputIndex: 0 })` on the iUSD CDP
3. Present the health status, collateral ratio, and liquidation price

**Sample response:**
```
CDP #42 Health Analysis
Status: Healthy
Collateral Ratio: 285%
Min Required: 150%
Liquidation Price: $0.2105 ADA/USD
Current ADA Price: $0.4500
Buffer: 53% above liquidation
```

### Monitor all CDPs for a wallet

View all CDPs owned by a wallet to get a portfolio-level health overview.

**Prompt:** "Show me all my CDPs and their health"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to list all CDPs
2. For each CDP, call `analyze_cdp_health` to get detailed health data
3. Present a summary table

**Sample response:**
```
Your CDPs:
  CDP #42 (iUSD): 285% ratio — Healthy
  CDP #78 (iBTC): 162% ratio — Warning
  CDP #91 (iETH): 310% ratio — Healthy

Action needed: CDP #78 is approaching minimum ratio (150%).
Consider depositing more collateral.
```

### Check protocol-wide CDP stats

Review all CDPs across the protocol to gauge overall collateralization.

**Prompt:** "How many CDPs exist on Indigo?"

**Workflow:**
1. Call `get_all_cdps()` to retrieve every CDP
2. Aggregate totals by iAsset type
3. Calculate average collateral ratios per asset

**Sample response:**
```
Protocol CDPs: 4,231 total
  iUSD: 2,890 CDPs — avg ratio 245%
  iBTC: 612 CDPs — avg ratio 198%
  iETH: 489 CDPs — avg ratio 267%
  iSOL: 240 CDPs — avg ratio 223%
```

## Example Prompts

- "Analyze the health of my CDP"
- "Is my CDP at risk of liquidation?"
- "Show me all CDPs for my wallet"
- "What is the average collateral ratio across all iUSD CDPs?"
