# Staking Management

Open, adjust, and close INDY staking positions on Indigo Protocol.

## MCP Tools

### open_staking_position

Open a new INDY staking position by locking INDY tokens. Staked INDY earns ADA rewards from protocol fees and grants governance voting power proportional to the staked amount.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `amount` | number | Yes | Amount of INDY to stake |

**Returns:** Transaction CBOR to be signed and submitted.

**Example — Stake 1000 INDY:**

```
User: "Open a new staking position with 1000 INDY"

Tool call: open_staking_position({ amount: 1000 })

Response:
{
  "tx": "84a400...",
  "positionAddress": "addr1q...",
  "stakedAmount": 1000,
  "fee": "0.25 ADA"
}
```

**Example — Start staking with a small amount:**

```
User: "I want to start staking, just 50 INDY to test"

Tool call: open_staking_position({ amount: 50 })

Response:
{
  "tx": "84a400...",
  "positionAddress": "addr1q...",
  "stakedAmount": 50,
  "fee": "0.22 ADA"
}
```

### adjust_staking_position

Adjust an existing staking position by setting a new staked INDY amount. Use a higher amount to add more INDY or a lower amount to partially unstake.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Staking position UTxO address |
| `amount` | number | Yes | New total staked INDY amount |

**Returns:** Transaction CBOR to be signed and submitted.

**Example — Add more INDY to a position (increase from 1000 to 2000):**

```
User: "Add 1000 more INDY to my staking position"

Step 1 — get_staking_positions_by_owner({ owner: "stake1u8a..." })
         => position at addr1q... with 1000 INDY staked

Step 2 — adjust_staking_position({ address: "addr1q...", amount: 2000 })

Response:
{
  "tx": "84a400...",
  "positionAddress": "addr1q...",
  "previousAmount": 1000,
  "newAmount": 2000,
  "fee": "0.28 ADA"
}
```

**Example — Partially unstake (reduce from 2000 to 500):**

```
User: "Remove 1500 INDY from my staking position"

Step 1 — get_staking_positions_by_owner({ owner: "stake1u8a..." })
         => position at addr1q... with 2000 INDY staked

Step 2 — adjust_staking_position({ address: "addr1q...", amount: 500 })

Response:
{
  "tx": "84a400...",
  "positionAddress": "addr1q...",
  "previousAmount": 2000,
  "newAmount": 500,
  "fee": "0.28 ADA"
}
```

### close_staking_position

Close an existing staking position and withdraw all staked INDY plus any accrued ADA rewards.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Staking position UTxO address |

**Returns:** Transaction CBOR to be signed and submitted.

**Example — Close position and unstake all:**

```
User: "Close my staking position and withdraw everything"

Step 1 — get_staking_positions_by_owner({ owner: "stake1u8a..." })
         => position at addr1q... with 2000 INDY staked, 15.3 ADA rewards

Step 2 — close_staking_position({ address: "addr1q..." })

Response:
{
  "tx": "84a400...",
  "positionAddress": "addr1q...",
  "withdrawnIndy": 2000,
  "claimedRewards": 15.3,
  "fee": "0.30 ADA"
}
```

## Transaction Fees

All staking transactions require a Cardano transaction fee paid in ADA. Typical fees:

| Operation | Typical Fee |
|-----------|-------------|
| Open position | ~0.20-0.30 ADA |
| Adjust position | ~0.25-0.35 ADA |
| Close position | ~0.25-0.35 ADA |

Fees vary based on transaction size and current network parameters. The returned transaction CBOR includes the calculated fee before signing.

## Common Prompts

- "Open a new staking position with 1000 INDY"
- "Stake 500 INDY"
- "Add 1000 more INDY to my staking position"
- "Increase my staking position to 5000 INDY"
- "Remove 500 INDY from my staking position"
- "Reduce my stake to 200 INDY"
- "Close my staking position and withdraw everything"
- "Unstake all my INDY"