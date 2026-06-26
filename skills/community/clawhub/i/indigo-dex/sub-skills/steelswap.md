# SteelSwap

Query available tokens and get swap estimates through the SteelSwap DEX aggregator on Cardano.

## MCP Tools

### get_steelswap_tokens

List all tokens available for swapping on SteelSwap.

**Parameters:** None

**Returns:** Array of token objects with name, ticker, policy ID, and decimals.

### get_steelswap_estimate

Get a swap estimate for a given token pair, including expected output, price impact, and routing information.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | string | Yes | Source token ticker or policy ID |
| `to` | string | Yes | Destination token ticker or policy ID |
| `amount` | number | Yes | Amount of the source token to swap |

**Returns:** Swap estimate with expected output amount, price impact, and route details.

## Examples

### Get a swap estimate for ADA to iUSD

Check how much iUSD you would receive for a given amount of ADA.

**Prompt:** "Get a swap estimate for 500 ADA to iUSD"

**Workflow:**
1. Call `get_steelswap_estimate({ from: "ADA", to: "iUSD", amount: 500 })`
2. Parse the response for output amount, price impact, and route
3. Present the estimate with effective exchange rate

**Sample response:**
```
Swap Estimate: 500 ADA → iUSD
  Expected output: 223.45 iUSD
  Exchange rate: 1 ADA = 0.4469 iUSD
  Price impact: 0.12%
  Route: ADA → iUSD (direct)
```

### Check price impact for a large swap

Evaluate whether a large trade would cause significant slippage.

**Prompt:** "What is the price impact of swapping 50,000 ADA to iETH?"

**Workflow:**
1. Call `get_steelswap_estimate({ from: "ADA", to: "iETH", amount: 50000 })`
2. Highlight the price impact percentage
3. Compare with a smaller trade if impact is high

**Sample response:**
```
Swap Estimate: 50,000 ADA → iETH
  Expected output: 6.842 iETH
  Exchange rate: 1 ADA = 0.0001368 iETH
  Price impact: 2.45%
  Route: ADA → iETH (via ADA/iETH pool)

Warning: Price impact above 1%. Consider splitting
into smaller trades to reduce slippage.
```

### Browse available tokens

See what tokens are available for trading on SteelSwap.

**Prompt:** "What tokens can I swap on SteelSwap?"

**Workflow:**
1. Call `get_steelswap_tokens()` to list all available tokens
2. Group by category (native, iAssets, other Cardano tokens)
3. Present with ticker and name

**Sample response:**
```
Available Tokens on SteelSwap (42 tokens):

Native:
  ADA — Cardano

iAssets:
  iUSD — Indigo USD
  iBTC — Indigo BTC
  iETH — Indigo ETH
  iSOL — Indigo SOL

Other:
  INDY — Indigo Protocol
  MIN — Minswap
  SUNDAE — SundaeSwap
  ...and 33 more
```

## Example Prompts

- "What tokens can I swap on SteelSwap?"
- "Get a swap estimate for 500 ADA to iUSD"
- "How much iBTC would I get for 1000 ADA on SteelSwap?"
- "What is the price impact of swapping 10000 ADA to iETH?"
