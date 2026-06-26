# Order Book

Query the ROB order book and historical redemption orders on Indigo Protocol.

## Tools

### get_order_book

Get open limited redemption positions from the order book.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asset` | `iUSD` \| `iBTC` \| `iETH` \| `iSOL` | No | Filter by iAsset |
| `owners` | `string[]` | No | Filter by owner addresses |

**Returns:** Array of ROB position objects with owner, ADA amount, max price, and fill status.

### get_redemption_orders

Get redemption orders, optionally filtered by timestamp or price range.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `timestamp` | `number` | No | Unix timestamp in milliseconds |
| `in_range` | `boolean` | No | Filter by price range |

**Returns:** Array of redemption order objects with amounts, prices, and timestamps.

## Examples

### View the iUSD ROB order book

See all open ROB positions for iUSD to assess available liquidity.

**Prompt:** "Show me all open ROB positions for iUSD"

**Workflow:**
1. Call `get_order_book({ asset: "iUSD" })` to get all iUSD ROB positions
2. Sort by max price ascending to show cheapest liquidity first
3. Present total ADA available at each price level

**Sample response:**
```
iUSD ROB Order Book (12 positions):
  Max Price 1.00: 5,000 ADA (2 positions)
  Max Price 1.02: 12,300 ADA (4 positions)
  Max Price 1.05: 8,700 ADA (3 positions)
  Max Price 1.10: 15,200 ADA (3 positions)
Total available: 41,200 ADA
```

### Check your own ROB positions

View your active ROB positions to monitor fill status and manage them.

**Prompt:** "Show me my ROB positions"

**Workflow:**
1. Call `get_order_book({ owners: ["addr1qx...abc"] })` to filter by your address
2. Display each position with its current status and fill percentage

**Sample response:**
```
Your ROB Positions:

1. iUSD position — 2,000 ADA at max 1.05
   Status: Partially filled (40%)
   Claimable: 800 iUSD

2. iBTC position — 5,000 ADA at max 42,500
   Status: Open (0% filled)
```

### Review recent redemption history

See recent redemption orders to understand market activity.

**Prompt:** "Show me recent redemption orders"

**Workflow:**
1. Call `get_redemption_orders()` to get recent orders
2. Sort by timestamp descending
3. Present with amounts and prices

**Sample response:**
```
Recent Redemption Orders:
  2 hours ago:  500 iUSD redeemed @ 1.02 — 510 ADA
  5 hours ago:  1,200 iUSD redeemed @ 1.01 — 1,212 ADA
  8 hours ago:  200 iBTC redeemed @ 42,100 — 84,200 ADA
```

## Example Prompts

- "Show me all open ROB positions for iUSD"
- "What's the current ROB order book depth for iBTC?"
- "Show me my ROB positions"
- "List recent redemption orders"
- "How much ADA liquidity is available in the iUSD order book?"
