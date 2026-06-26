# Asset Prices

Query prices and details for Indigo Protocol iAssets: iUSD, iBTC, iETH, and iSOL.

## MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_assets` | Get all iAssets with prices and interest data | None |
| `get_asset` | Get details for a specific iAsset | `asset` (iUSD, iBTC, iETH, iSOL) |
| `get_asset_price` | Get the current price for a specific iAsset | `asset` (iUSD, iBTC, iETH, iSOL) |

## Examples

### Get all iAsset prices at once

Use `get_assets` to retrieve a full list of all iAssets with their current prices and interest data. This returns iUSD, iBTC, iETH, and iSOL in a single call, which is useful for building dashboards or comparing assets.

```
User: "What are the current prices for all Indigo iAssets?"
Tool: get_assets
Response: Returns each iAsset with its current oracle price, interest rate, and metadata.
```

### Query a single iAsset price

Use `get_asset_price` with the `asset` parameter to get the current price for one specific iAsset. Valid values are `iUSD`, `iBTC`, `iETH`, and `iSOL`.

```
User: "What is the current price of iUSD?"
Tool: get_asset_price { asset: "iUSD" }
Response: Returns the current iUSD price (expected to be close to $1.00).
```

```
User: "How much is iBTC worth right now?"
Tool: get_asset_price { asset: "iBTC" }
Response: Returns the current iBTC price tracking Bitcoin's market price.
```

### Get detailed iAsset information

Use `get_asset` with the `asset` parameter to get comprehensive details including price, interest rate, and protocol metadata for a single iAsset.

```
User: "Show me full details for iETH"
Tool: get_asset { asset: "iETH" }
Response: Returns iETH price, interest data, and asset configuration details.
```

```
User: "What's the interest rate on iSOL?"
Tool: get_asset { asset: "iSOL" }
Response: Returns iSOL details including its current interest rate and oracle price.
```

### Price formatting and display

When displaying iAsset prices to users:
- **iUSD** tracks USD, so display as `$X.XX` (e.g., `$1.00`)
- **iBTC** tracks Bitcoin, so display as `$XX,XXX.XX` (e.g., `$67,432.15`)
- **iETH** tracks Ethereum, so display as `$X,XXX.XX` (e.g., `$3,521.80`)
- **iSOL** tracks Solana, so display as `$XXX.XX` (e.g., `$142.35`)

All prices are denominated in USD.

### Oracle source and update frequency

iAsset prices are sourced from Indigo Protocol's on-chain oracle system (Charli3). The oracle aggregates price feeds from multiple sources to ensure accuracy. Prices update at regular intervals determined by the oracle configuration, typically every few minutes. Use `get_asset` to see the latest oracle-reported price for any iAsset.
