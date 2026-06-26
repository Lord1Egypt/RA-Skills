# DEX Yields

Query current DEX yield data for Indigo iAsset trading pairs.

## MCP Tools

### get_dex_yields

Get current DEX yield data for Indigo iAsset pairs across supported decentralized exchanges.

**Parameters:** None

**Returns:** Array of yield objects with APY, TVL, and volume data for each iAsset trading pair.

## Examples

### View all DEX yield opportunities

Get a comprehensive overview of all iAsset trading pair yields across Cardano DEXs.

**Prompt:** "What are the current DEX yields for iAsset pairs?"

**Workflow:**
1. Call `get_dex_yields()` to retrieve yield data for all pairs
2. Group by iAsset and sort by APY
3. Present yields with TVL and volume context

**Sample response:**
```
DEX Yields for iAsset Pairs:

iUSD Pairs:
  iUSD/ADA (Minswap):    12.4% APY — $2.1M TVL
  iUSD/ADA (SundaeSwap):  9.8% APY — $890K TVL

iBTC Pairs:
  iBTC/ADA (Minswap):    15.1% APY — $1.4M TVL
  iBTC/ADA (SundaeSwap): 11.3% APY — $520K TVL

iETH Pairs:
  iETH/ADA (Minswap):    13.7% APY — $980K TVL
```

### Find best yield for a specific iAsset

Compare yield opportunities for a single iAsset across different DEXs.

**Prompt:** "Where can I get the best yield for iUSD?"

**Workflow:**
1. Call `get_dex_yields()` to get all yield data
2. Filter for iUSD pairs only
3. Sort by APY descending and highlight the best option

**Sample response:**
```
Best iUSD Yield Opportunities:
  1. Minswap iUSD/ADA:    12.4% APY ($2.1M TVL)
  2. SundaeSwap iUSD/ADA:  9.8% APY ($890K TVL)

Recommendation: Minswap offers the highest APY with deeper
liquidity. SundaeSwap has lower APY but may have less
impermanent loss risk due to tighter price ranges.
```

### Compare DEX yields vs stability pool APR

Help users decide between providing DEX liquidity and depositing in stability pools.

**Prompt:** "Should I provide liquidity on a DEX or deposit in the stability pool?"

**Workflow:**
1. Call `get_dex_yields()` to get DEX yield data
2. Call `get_apr_rewards()` to get stability pool APR data
3. Compare yields side by side, noting risk differences

**Sample response:**
```
iUSD Yield Comparison:
  Stability Pool: 18.5% APR (single-sided, no IL risk)
  Minswap LP:     12.4% APY (dual-sided, IL risk)
  SundaeSwap LP:   9.8% APY (dual-sided, IL risk)

The stability pool currently offers higher returns with
lower risk (no impermanent loss). DEX LPs earn trading
fees but face impermanent loss if ADA/iUSD price diverges.
```

## Example Prompts

- "What are the current DEX yields for iAsset pairs?"
- "Show me the best yield opportunities for iUSD on DEXs"
- "What is the liquidity mining APY for iBTC pairs?"
- "Compare DEX yields to stability pool returns"
- "Which DEX has the deepest liquidity for iETH?"
