# Assets MCP Tools Reference

Detailed reference for all iAsset and token price MCP tools.

## get_assets

Get all Indigo iAssets with their current prices, interest rates, and metadata.

**Parameters:** None

**Returns:** Array of iAsset objects:
- `name` — iAsset name (iUSD, iBTC, iETH, iSOL)
- `price` — Current oracle price in USD
- `interestRate` — Current interest rate
- `totalMinted` — Total amount minted across all CDPs
- `minCollateralRatio` — Minimum collateral ratio for this iAsset

---

## get_asset

Get detailed information for a specific iAsset.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset name |

**Returns:** Single iAsset object with price, interest data, total minted, and collateral parameters.

---

## get_asset_price

Get the current oracle price for a specific iAsset.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset name |

**Returns:** `{ asset: string, price: number }` — current price in USD.

---

## get_ada_price

Get the current ADA price in USD.

**Parameters:** None

**Returns:** `{ price: number }` — ADA/USD price from oracle.

---

## get_indy_price

Get the current INDY token price in both ADA and USD.

**Parameters:** None

**Returns:** `{ priceAda: number, priceUsd: number }` — INDY price in ADA and USD.
