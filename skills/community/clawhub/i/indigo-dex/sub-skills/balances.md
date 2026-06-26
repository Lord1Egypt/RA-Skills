# Wallet Balances

Query wallet token balances on Cardano via the Blockfrost API.

## MCP Tools

### get_blockfrost_balances

Retrieve all token balances for a given wallet address using Blockfrost.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Cardano wallet address (bech32 format) |

**Returns:** Array of token balance objects with policy ID, asset name, and quantity for each token held.

## Examples

### Check wallet balances

View all tokens held by a specific wallet address.

**Prompt:** "What are the token balances for addr1qx...abc?"

**Workflow:**
1. Call `get_blockfrost_balances({ address: "addr1qx...abc" })`
2. Parse the token list, matching policy IDs to known token names
3. Present balances grouped by category

**Sample response:**
```
Wallet Balances for addr1qx...abc:

Native:
  ADA: 12,450.32

iAssets:
  iUSD: 2,340.00
  iBTC: 0.15
  iETH: 1.82

Tokens:
  INDY: 5,200.00
  MIN: 890.00

Total assets: 8 tokens
```

### Check specific iAsset holdings

Find out how much of a specific iAsset a wallet holds.

**Prompt:** "Check how much iUSD this address holds"

**Workflow:**
1. Call `get_blockfrost_balances({ address: "addr1qx...abc" })`
2. Filter for iUSD by matching its policy ID
3. Present the balance with USD value context

**Sample response:**
```
iUSD Balance for addr1qx...abc:
  Amount: 2,340.00 iUSD
  Value: ~$2,340 (1 iUSD ≈ $1.00)
```

### Portfolio overview before trading

Check wallet balances to plan a swap or CDP operation.

**Prompt:** "Show me all assets held by this wallet so I can plan a swap"

**Workflow:**
1. Call `get_blockfrost_balances({ address: "addr1qx...abc" })`
2. Present all holdings with current values
3. Highlight tradeable assets on SteelSwap

**Sample response:**
```
Wallet Portfolio for addr1qx...abc:

  ADA:  12,450.32 (~$5,602)
  iUSD: 2,340.00  (~$2,340)
  iBTC: 0.15      (~$6,300)
  INDY: 5,200.00  (~$1,560)

Tradeable on SteelSwap: ADA, iUSD, iBTC, INDY
Total estimated value: ~$15,802
```

## Example Prompts

- "What are the token balances for addr1q...?"
- "Show me all assets held by this wallet"
- "Check how much iUSD this address holds"
- "Does this wallet hold any INDY tokens?"
