# DEX MCP Tools Reference

Detailed reference for all DEX integration MCP tools.

## get_steelswap_tokens

List all tokens available for swapping on SteelSwap.

**Parameters:** None

**Returns:** Array of token objects:
- `name` — Full token name
- `ticker` — Token ticker symbol
- `policyId` — Cardano policy ID
- `decimals` — Number of decimal places

---

## get_steelswap_estimate

Get a swap estimate for a token pair on SteelSwap.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `from` | `string` | Yes | Source token ticker or policy ID |
| `to` | `string` | Yes | Destination token ticker or policy ID |
| `amount` | `number` | Yes | Amount of source token to swap |

**Returns:** Swap estimate object:
- `outputAmount` — Expected amount of destination token
- `priceImpact` — Price impact as percentage
- `route` — Routing path used for the swap
- `exchangeRate` — Effective exchange rate

---

## get_iris_liquidity_pools

Fetch current liquidity pool data from Iris DEX.

**Parameters:** None

**Returns:** Array of pool objects:
- `pair` — Token pair (e.g., "ADA/iUSD")
- `tvl` — Total value locked in USD
- `volume24h` — 24-hour trading volume
- `feeTier` — Pool fee percentage
- `tokenA` / `tokenB` — Token details for each side

---

## get_blockfrost_balances

Get all token balances for a wallet address via Blockfrost.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | Cardano wallet address (bech32) |

**Returns:** Array of balance objects:
- `policyId` — Token policy ID (empty string for ADA)
- `assetName` — On-chain asset name (hex)
- `quantity` — Token amount in smallest unit
