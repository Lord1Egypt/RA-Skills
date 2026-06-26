# Iris Liquidity Pools

Retrieve liquidity pool data from the Iris DEX on Cardano, including pool composition, TVL, and fee information.

## MCP Tools

### get_iris_liquidity_pools

Fetch current liquidity pool data from Iris.

**Parameters:** None

**Returns:** Array of liquidity pool objects with token pairs, total value locked, volume, and fee tier information.

## Examples

### View all Iris liquidity pools

Get a comprehensive list of all available liquidity pools on Iris.

**Prompt:** "Show me all Iris liquidity pools"

**Workflow:**
1. Call `get_iris_liquidity_pools()` to retrieve all pool data
2. Sort by TVL descending
3. Present pools with key metrics

**Sample response:**
```
Iris Liquidity Pools (18 pools):

  ADA/iUSD:   $2.1M TVL — 0.3% fee — $142K 24h volume
  ADA/iBTC:   $1.4M TVL — 0.3% fee — $89K 24h volume
  ADA/iETH:   $980K TVL — 0.3% fee — $67K 24h volume
  ADA/INDY:   $620K TVL — 0.3% fee — $41K 24h volume
  ADA/iSOL:   $340K TVL — 0.3% fee — $22K 24h volume
  ...and 13 more
```

### Find pools for a specific iAsset

Filter pools to see liquidity available for a particular iAsset.

**Prompt:** "List the available liquidity pools for iUSD on Iris"

**Workflow:**
1. Call `get_iris_liquidity_pools()` to get all pools
2. Filter for pools containing iUSD
3. Present with TVL and volume

**Sample response:**
```
iUSD Pools on Iris:
  ADA/iUSD:  $2.1M TVL — $142K 24h volume — 0.3% fee
  iUSD/USDC: $890K TVL — $56K 24h volume — 0.05% fee

Total iUSD liquidity: $2.99M across 2 pools
```

### Compare pool sizes

Identify which pools have the deepest liquidity for optimal trading.

**Prompt:** "What are the largest pools on Iris by TVL?"

**Workflow:**
1. Call `get_iris_liquidity_pools()` to get all pool data
2. Sort by TVL descending
3. Present top pools with percentage of total TVL

**Sample response:**
```
Top Iris Pools by TVL:
  1. ADA/iUSD:  $2.1M (28% of total)
  2. ADA/iBTC:  $1.4M (19% of total)
  3. ADA/iETH:  $980K (13% of total)
  4. ADA/INDY:  $620K (8% of total)
  5. ADA/iSOL:  $340K (5% of total)

Total Iris TVL: $7.4M across 18 pools
```

## Example Prompts

- "Show me all Iris liquidity pools"
- "What are the largest pools on Iris by TVL?"
- "List the available liquidity pools for iUSD on Iris"
- "What's the 24h volume on the ADA/iBTC pool?"
