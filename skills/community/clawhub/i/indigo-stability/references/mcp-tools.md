# Stability Pool MCP Tools Reference

Detailed reference for all stability pool MCP tools in the Indigo Protocol.

## Read Operations

### get_stability_pools

List all stability pools with their total deposits, earned rewards, and iAsset type.

**Parameters:** None

**Returns:** Array of stability pool objects:
- `asset` — iAsset type (iUSD, iBTC, iETH, iSOL)
- `totalDeposited` — Total iAssets deposited across all accounts
- `totalRewards` — Total ADA rewards earned from liquidations
- `accountCount` — Number of active accounts

---

### get_stability_pool_accounts

List all accounts in a specific stability pool.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | Pool iAsset type |

**Returns:** Array of account objects with deposit amounts, rewards, and pending requests.

---

### get_sp_account_by_owner

Look up stability pool accounts by owner address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owners` | `string[]` | Yes | Array of owner bech32 addresses |

**Returns:** Array of account objects matching the owner addresses.

## Write Operations

All write operations return `{ tx: string }` — unsigned CBOR transaction hex for client-side signing.

### create_sp_account

Create a new stability pool account with an initial iAsset deposit.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset to deposit |
| `amount` | `string` | Yes | Amount in smallest unit |

---

### adjust_sp_account

Adjust deposit in an existing account. Positive = deposit more, negative = withdraw.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | Pool iAsset |
| `amount` | `string` | Yes | Adjustment amount (positive = deposit, negative = withdraw) |
| `accountTxHash` | `string` | Yes | Account UTxO transaction hash |
| `accountOutputIndex` | `number` | Yes | Account UTxO output index |

---

### close_sp_account

Close a stability pool account, withdrawing all deposits and claiming rewards.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `accountTxHash` | `string` | Yes | Account UTxO transaction hash |
| `accountOutputIndex` | `number` | Yes | Account UTxO output index |

---

### process_sp_request

Process a pending stability pool request (deposit or withdrawal).

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `requestTxHash` | `string` | Yes | Request UTxO transaction hash |
| `requestOutputIndex` | `number` | Yes | Request UTxO output index |

---

### annul_sp_request

Cancel a pending stability pool request before it is processed.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `requestTxHash` | `string` | Yes | Request UTxO transaction hash |
| `requestOutputIndex` | `number` | Yes | Request UTxO output index |
