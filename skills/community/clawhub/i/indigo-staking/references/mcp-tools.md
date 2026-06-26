# Staking MCP Tools Reference

Detailed reference for all INDY staking MCP tools in the Indigo Protocol.

## Read Operations

### get_staking_info

Get general INDY staking information including total staked, reward rate, and parameters.

**Parameters:** None

**Returns:** Staking info object with total staked INDY, current reward rate, and protocol parameters.

---

### get_staking_positions

Get all active staking positions across the protocol.

**Parameters:** None

**Returns:** Array of staking position objects with owner, staked amount, rewards, and start date.

---

### get_staking_positions_by_owner

Get staking positions filtered by owner address.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owners` | `string[]` | Yes | Array of owner bech32 addresses |

**Returns:** Array of staking positions matching the owner addresses.

---

### get_staking_position_by_address

Get a specific staking position by its UTxO address.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | Staking position UTxO address |

**Returns:** Single staking position object.

## Write Operations

All write operations return `{ tx: string }` — unsigned CBOR transaction hex.

### open_staking_position

Open a new INDY staking position by locking INDY tokens.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `amount` | `string` | Yes | Amount of INDY to stake (smallest unit) |

---

### adjust_staking_position

Adjust an existing staking position — add or remove staked INDY.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `stakingTxHash` | `string` | Yes | Staking position UTxO transaction hash |
| `stakingOutputIndex` | `number` | Yes | Staking position UTxO output index |
| `amount` | `string` | Yes | New staked INDY amount (smallest unit) |

---

### close_staking_position

Close a staking position, withdrawing all staked INDY and accrued rewards.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `stakingTxHash` | `string` | Yes | Staking position UTxO transaction hash |
| `stakingOutputIndex` | `number` | Yes | Staking position UTxO output index |

---

### distribute_staking_rewards

Distribute pending staking rewards to position holders. Can be called by anyone.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | Caller Cardano bech32 address |
