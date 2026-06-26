# Redemption MCP Tools Reference

Detailed reference for all redemption and ROB MCP tools.

## Read Operations

### get_order_book

Get open ROB positions from the order book.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | No | Filter by iAsset |
| `owners` | `string[]` | No | Filter by owner addresses |

**Returns:** Array of ROB position objects with owner, ADA deposited, max price, fill status, and UTxO reference.

---

### get_redemption_orders

Get historical redemption orders.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `timestamp` | `number` | No | Unix timestamp (ms) — filter orders after this time |
| `in_range` | `boolean` | No | Filter by price range |

**Returns:** Array of redemption order objects with iAsset, amount, price, ADA received, and timestamp.

---

### get_redemption_queue

Get the aggregated redemption queue for a specific iAsset, sorted by max price ascending.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset to query |

**Returns:** Aggregated queue data with ADA totals at each price level.

## Write Operations

All write operations return `{ tx: string }` — unsigned CBOR transaction hex.

### open_rob

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | Target iAsset |
| `lovelacesAmount` | `string` | Yes | ADA in lovelace |
| `maxPrice` | `string` | Yes | Max price as on-chain integer |

---

### cancel_rob

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User bech32 address |
| `robTxHash` | `string` | Yes | ROB UTxO tx hash |
| `robOutputIndex` | `number` | Yes | ROB UTxO output index |

---

### adjust_rob

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User bech32 address |
| `robTxHash` | `string` | Yes | ROB UTxO tx hash |
| `robOutputIndex` | `number` | Yes | ROB UTxO output index |
| `lovelacesAdjustAmount` | `string` | Yes | Adjustment (positive = add, negative = remove) |
| `newMaxPrice` | `string` | No | Updated max price |

---

### claim_rob

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User bech32 address |
| `robTxHash` | `string` | Yes | ROB UTxO tx hash |
| `robOutputIndex` | `number` | Yes | ROB UTxO output index |

---

### redeem_rob

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User bech32 address |
| `redemptionRobs` | `array` | Yes | Array of `{ txHash, outputIndex, iAssetAmount }` |
| `priceOracleTxHash` | `string` | Yes | Price oracle UTxO tx hash |
| `priceOracleOutputIndex` | `number` | Yes | Price oracle output index |
| `iassetTxHash` | `string` | Yes | iAsset UTxO tx hash |
| `iassetOutputIndex` | `number` | Yes | iAsset UTxO output index |
