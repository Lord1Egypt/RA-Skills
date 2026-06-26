# Redemption Queue

Query the aggregated redemption queue for Indigo Protocol iAssets.

## Tools

### get_redemption_queue

Get the aggregated redemption queue for a specific iAsset, sorted by max price ascending.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asset` | `iUSD` \| `iBTC` \| `iETH` \| `iSOL` | Yes | The iAsset to query |

**Returns:** Aggregated queue data with total ADA queued at each price level, sorted ascending.

## Examples

### View the iUSD redemption queue

See how much ADA is queued for iUSD redemptions at each price level.

**Prompt:** "Show me the iUSD redemption queue"

**Workflow:**
1. Call `get_redemption_queue({ asset: "iUSD" })` to get the aggregated queue
2. Present price levels with total ADA queued at each level
3. Calculate the total ADA in the queue

**Sample response:**
```
iUSD Redemption Queue:
  Price ≤ 1.00:  15,200 ADA queued
  Price ≤ 1.02:  28,500 ADA queued
  Price ≤ 1.05:  41,200 ADA queued
  Price ≤ 1.10:  56,400 ADA queued
Total queued: 56,400 ADA across 12 positions
```

### Compare redemption pressure across iAssets

Identify which iAsset has the most or least redemption demand.

**Prompt:** "Which iAsset has the most redemption pressure?"

**Workflow:**
1. Call `get_redemption_queue({ asset: "iUSD" })` for iUSD
2. Call `get_redemption_queue({ asset: "iBTC" })` for iBTC
3. Call `get_redemption_queue({ asset: "iETH" })` for iETH
4. Call `get_redemption_queue({ asset: "iSOL" })` for iSOL
5. Compare total ADA queued across all assets

**Sample response:**
```
Redemption Queue Comparison:
  iUSD: 56,400 ADA queued (12 positions)
  iBTC: 84,200 ADA queued (8 positions)
  iETH: 23,100 ADA queued (5 positions)
  iSOL: 11,800 ADA queued (3 positions)

iBTC has the highest redemption pressure at 84,200 ADA.
```

### Assess fill probability for an ROB position

Use the queue data to estimate how quickly an ROB position might be filled.

**Prompt:** "If I open a ROB at max price 1.05, how much demand is there?"

**Workflow:**
1. Call `get_redemption_queue({ asset: "iUSD" })` to see queue depth
2. Look at positions at or below the 1.05 price level
3. Estimate fill probability based on queued ADA vs your position size

**Sample response:**
```
iUSD queue at max price 1.05:
  Total queued: 41,200 ADA (your position would be 9th in line)
  Recent fill rate: ~5,000 ADA/day
  Estimated time to fill: ~8 days

Lower max price = earlier position in queue but slower fills.
```

## Example Prompts

- "Show me the iUSD redemption queue"
- "Which iAsset has the most redemption pressure?"
- "What's the queue depth for iBTC?"
- "How much ADA is in the iETH redemption queue?"
