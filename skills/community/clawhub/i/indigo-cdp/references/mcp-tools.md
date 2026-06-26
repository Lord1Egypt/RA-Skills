# CDP MCP Tools Reference

Detailed reference for all CDP-related MCP tools in the Indigo Protocol.

## Write Operations

All write operations return an unsigned transaction (CBOR hex) for client-side signing and submission.

### open_cdp

Open a new Collateralized Debt Position.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset to mint |
| `collateralAmount` | `string` | Yes | ADA collateral in lovelace (1 ADA = 1,000,000 lovelace) |

**Returns:** `{ tx: string }` — unsigned CBOR transaction hex

---

### deposit_cdp

Deposit additional ADA collateral into an existing CDP.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `collateralAmount` | `string` | Yes | Additional ADA in lovelace |

**Returns:** `{ tx: string }`

---

### withdraw_cdp

Withdraw excess collateral from a CDP. Ratio must stay above minimum.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `collateralAmount` | `string` | Yes | ADA to withdraw in lovelace |

**Returns:** `{ tx: string }`

---

### close_cdp

Close a CDP, burning all remaining debt and returning collateral.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

**Returns:** `{ tx: string }`

---

### mint_cdp

Mint iAssets against CDP collateral, increasing debt.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to mint (smallest unit) |

**Returns:** `{ tx: string }`

---

### burn_cdp

Burn iAssets to reduce CDP debt.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to burn (smallest unit) |

**Returns:** `{ tx: string }`

---

### liquidate_cdp

Liquidate an undercollateralized CDP. Caller pays debt, receives collateral + bonus.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | Liquidator Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

**Returns:** `{ tx: string }`

---

### redeem_cdp

Redeem iAssets against a CDP at oracle price.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to redeem |

**Returns:** `{ tx: string }`

---

### freeze_cdp

Freeze a CDP to prevent further operations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

**Returns:** `{ tx: string }`

---

### merge_cdps

Merge multiple CDPs of the same iAsset into one.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpRefs` | `array` | Yes | Array of `{ txHash: string, outputIndex: number }` |

**Returns:** `{ tx: string }`

---

### leverage_cdp

Open a leveraged CDP via ROB mechanism.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | Target iAsset |
| `collateralAmount` | `string` | Yes | Initial ADA collateral in lovelace |
| `leverageMultiplier` | `number` | Yes | Leverage multiplier |

**Returns:** `{ tx: string }`

## Read Operations

### get_all_cdps

List all CDPs in the protocol.

**Parameters:** None

**Returns:** `CDP[]` — array of CDP objects

---

### get_cdps_by_owner

List CDPs filtered by owner address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `owners` | `string[]` | Yes | Array of owner bech32 addresses |

**Returns:** `CDP[]`

---

### get_cdps_by_address

List CDPs by UTxO address.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | CDP UTxO address |

**Returns:** `CDP[]`

---

### analyze_cdp_health

Analyze CDP health, liquidation risk, and collateral ratio.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

**Returns:** Health analysis with ratio, liquidation price, risk level, and recommended actions.
