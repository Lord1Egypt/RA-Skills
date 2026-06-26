# TVL & Protocol Stats

Query total value locked and protocol-wide statistics for the Indigo Protocol.

## MCP Tools

### get_tvl

Get the total value locked (TVL) in Indigo Protocol across all pools and CDPs.

**Parameters:** None

**Returns:** TVL data including total value locked in ADA and USD.

### get_protocol_stats

Get protocol-wide statistics and metrics including number of CDPs, total minted iAssets, and pool utilization.

**Parameters:** None

**Returns:** Protocol statistics object with aggregate metrics across all Indigo components.

## Examples

### Get total TVL from DefiLlama

Retrieve the current total value locked in Indigo Protocol, sourced from DefiLlama aggregated data.

**Prompt:** "What is the current TVL of Indigo Protocol?"

**Workflow:**
1. Call `get_tvl` to retrieve the latest TVL figure
2. The response includes TVL in both ADA and USD denominations
3. Data is sourced from DefiLlama, which aggregates on-chain pool balances

**Sample response:**
```
Indigo Protocol TVL: $42.5M (106.2M ADA)
```

### Protocol stats breakdown (CDP TVL, SP TVL, staking TVL)

Break down the total TVL into its component parts: CDP collateral, stability pool deposits, and staked INDY.

**Prompt:** "Give me a breakdown of Indigo's TVL by component"

**Workflow:**
1. Call `get_protocol_stats` to get detailed metrics
2. Parse the response to extract CDP collateral totals, stability pool deposit totals, and staking totals
3. Present each category with its ADA/USD value

**Sample response:**
```
Indigo Protocol Stats Breakdown:
- CDP Collateral:     $28.1M (70.2M ADA)
- Stability Pools:    $11.3M (28.2M ADA)
- Staked INDY:        $3.1M  (7.8M ADA)
- Total TVL:          $42.5M (106.2M ADA)
- Active CDPs:        4,231
- Total iAssets minted: 5
```

### Historical TVL trend analysis

Analyze how Indigo's TVL has changed over time by comparing current data with known historical figures.

**Prompt:** "How has Indigo's TVL trended recently?"

**Workflow:**
1. Call `get_tvl` to get the current TVL snapshot
2. Call `get_protocol_stats` to get supporting metrics like active CDP count and pool utilization
3. Compare current figures against previously known data points to identify trends
4. Summarize growth or decline in a clear narrative

**Sample response:**
```
Current TVL: $42.5M
Active CDPs: 4,231
Pool Utilization: 78%

TVL is primarily driven by CDP collateral (66%) followed by
stability pool deposits (27%) and INDY staking (7%).
```

### Comparison with other Cardano protocols

Put Indigo's TVL in context by comparing it against other Cardano DeFi protocols using DefiLlama data.

**Prompt:** "How does Indigo's TVL compare to other Cardano protocols?"

**Workflow:**
1. Call `get_tvl` to get Indigo's current TVL
2. Reference DefiLlama's Cardano chain rankings for context
3. Present Indigo's position relative to other top Cardano DeFi protocols

**Sample response:**
```
Indigo Protocol TVL: $42.5M
Cardano DeFi Ranking: #3

Indigo is the leading synthetic assets protocol on Cardano.
Its TVL places it among the top Cardano DeFi protocols alongside
Minswap, SundaeSwap, and Liqwid Finance.
```

## Example Prompts

- "What is the current TVL of Indigo Protocol?"
- "Show me the overall Indigo protocol stats"
- "How much value is locked in Indigo?"
- "Break down Indigo's TVL by category"
- "How does Indigo compare to other Cardano DeFi protocols?"
- "What percentage of TVL comes from CDPs vs stability pools?"