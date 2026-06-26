# APR Rewards

Query APR reward rates for Indigo Protocol pools and staking positions.

## MCP Tools

### get_apr_rewards

Get APR reward rates across all Indigo pools.

**Parameters:** None

**Returns:** Array of pool reward objects with APR percentages for each pool type.

### get_apr_by_key

Get the APR reward rate for a specific pool identified by key.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | string | Yes | Pool key identifier |

**Returns:** APR reward data for the specified pool.

## Examples

### Compare APR across all pools

View reward rates for every Indigo pool to find the best yield opportunity.

**Prompt:** "What are the current APR rewards for all Indigo pools?"

**Workflow:**
1. Call `get_apr_rewards()` to retrieve all pool APR data
2. Sort pools by APR percentage descending
3. Present a ranked table of pools with their reward rates

**Sample response:**
```
Indigo Pool APR Rewards:
  iUSD Stability Pool:  18.5% APR — $11.3M TVL
  iBTC Stability Pool:  14.2% APR — $4.1M TVL
  iETH Stability Pool:  12.8% APR — $2.9M TVL
  iSOL Stability Pool:  22.1% APR — $1.2M TVL
  INDY Staking:         9.4% APR — $3.1M TVL
```

### Check APR for a specific pool

Look up the reward rate for a particular pool by its key.

**Prompt:** "What's the APR for the iUSD stability pool?"

**Workflow:**
1. Call `get_apr_by_key({ key: "iUSD-stability" })` to get the specific pool data
2. Present the APR with context about pool size and rewards

**Sample response:**
```
iUSD Stability Pool:
  APR: 18.5%
  TVL: $11.3M
  Daily rewards: ~$5,726
  Source: Liquidation gains + INDY incentives
```

### Find the highest-yielding pool

Identify which Indigo pool currently offers the best returns.

**Prompt:** "Which Indigo pool has the highest APR?"

**Workflow:**
1. Call `get_apr_rewards()` to get all pool data
2. Sort by APR descending and identify the top pool
3. Compare against other pools for context

**Sample response:**
```
Highest APR: iSOL Stability Pool at 22.1%

Note: Higher APR pools often have lower TVL. The iSOL pool
has $1.2M TVL vs $11.3M for iUSD. Smaller pools can offer
higher APR but may have more variable returns.
```

## Example Prompts

- "What are the current APR rewards for Indigo pools?"
- "Show me the APR for the iUSD stability pool"
- "Which Indigo pool has the highest APR?"
- "Compare stability pool yields across all iAssets"
- "What rewards would I earn staking 10,000 INDY?"
