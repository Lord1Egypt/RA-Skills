# Staking Queries

Query INDY staking information and browse staking positions on Indigo Protocol.

## MCP Tools

### get_staking_info

Get the global staking manager state including total staked INDY, reward parameters, and staking configuration.

**Parameters:** None

**Returns:** Staking info object with total staked INDY, reward rates, and configuration parameters.

**Example:**

```
User: "What is the current INDY staking info?"

Tool call: get_staking_info()

Response:
{
  "totalStaked": 12500000,
  "rewardRate": 0.05,
  "minStake": 1,
  "stakingManagerAddress": "addr1..."
}
```

### get_staking_positions

List all active INDY staking positions across the protocol.

**Parameters:** None

**Returns:** Array of staking position objects with owner, staked amount, and reward data.

**Example:**

```
User: "Show me all active staking positions"

Tool call: get_staking_positions()

Response:
[
  {
    "address": "addr1q...",
    "owner": "stake1u...",
    "stakedIndy": 5000,
    "accruedRewards": 12.5
  },
  {
    "address": "addr1q...",
    "owner": "stake1u...",
    "stakedIndy": 10000,
    "accruedRewards": 25.0
  }
]
```

### get_staking_positions_by_owner

Get all staking positions owned by a specific address. Use this to check a user's staked INDY and accrued rewards.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `owner` | string | Yes | Owner stake key hash or address |

**Returns:** Array of staking positions for the specified owner.

**Example:**

```
User: "What are my staking positions?"

Tool call: get_staking_positions_by_owner({ owner: "stake1u8a..." })

Response:
[
  {
    "address": "addr1q...",
    "owner": "stake1u8a...",
    "stakedIndy": 3000,
    "accruedRewards": 7.5
  }
]
```

### get_staking_position_by_address

Get a specific staking position by its on-chain UTxO address. Returns full position details including staked amount, owner, and pending rewards.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Staking position UTxO address |

**Returns:** Staking position details for the specified address.

**Example:**

```
User: "Look up the staking position at addr1q9x..."

Tool call: get_staking_position_by_address({ address: "addr1q9x..." })

Response:
{
  "address": "addr1q9x...",
  "owner": "stake1u8a...",
  "stakedIndy": 3000,
  "accruedRewards": 7.5,
  "createdAt": "2025-01-15T10:30:00Z"
}
```

## Calculating Position Value

To estimate the total value of a staking position (staked INDY + accrued ADA rewards):

1. Call `get_staking_positions_by_owner` to retrieve positions
2. Use `get_indy_price` (from indigo-assets) to get the current INDY price
3. Multiply staked amount by INDY price and add accrued ADA rewards

```
User: "How much are my staking positions worth?"

Step 1 — get_staking_positions_by_owner({ owner: "stake1u8a..." })
Step 2 — get_indy_price()  =>  { "price": 0.85 }
Step 3 — Position value = (3000 INDY * $0.85) + 7.5 ADA rewards
```

## Common Prompts

- "What is the current INDY staking info?"
- "How much total INDY is staked?"
- "Show me all active staking positions"
- "What are my staking positions?"
- "Look up the staking position at addr1q..."
- "How much are my staking positions worth?"
- "What rewards have I earned from staking?"
