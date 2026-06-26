# Stability Pool Management

Create, adjust, and close stability pool accounts.

All management operations return an unsigned transaction (CBOR hex) for client-side signing.

## Tools

### create_sp_account

Create a new stability pool account by depositing iAssets.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset to deposit |
| `amount` | `string` | Yes | Amount of iAsset to deposit (in smallest unit) |

#### Examples

**Create an iUSD stability pool account:**

```
User: "I want to deposit 1000 iUSD into the stability pool"
→ Call create_sp_account({
    address: "addr1qx...abc",
    asset: "iUSD",
    amount: "1000000000"
  })
→ Returns unsigned tx CBOR. User signs and submits to create the account.
  Note: 1 iUSD = 1,000,000 smallest units (6 decimals).
```

**Create an iBTC stability pool account:**

```
User: "Open a stability pool position with 0.5 iBTC"
→ Call create_sp_account({
    address: "addr1qx...abc",
    asset: "iBTC",
    amount: "50000000"
  })
→ Returns unsigned tx CBOR for signing.
  Note: iBTC uses 8 decimal places.
```

**Create an iETH stability pool account:**

```
User: "Deposit 2 iETH into the stability pool"
→ Call create_sp_account({
    address: "addr1qx...abc",
    asset: "iETH",
    amount: "2000000000000000000"
  })
→ Returns unsigned tx CBOR for signing.
  Note: iETH uses 18 decimal places.
```

---

### adjust_sp_account

Increase or decrease the deposit in an existing stability pool account. Positive amounts deposit more iAssets; negative amounts withdraw.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset of the stability pool |
| `amount` | `string` | Yes | Amount to adjust (positive = deposit, negative = withdraw) |
| `accountTxHash` | `string` | Yes | Transaction hash of the account UTxO |
| `accountOutputIndex` | `number` | Yes | Output index of the account UTxO |

#### Examples

**Deposit more iUSD into an existing account:**

```
User: "Add 500 more iUSD to my stability pool position"
→ First call get_sp_account_by_owner to find the account UTxO.
→ Call adjust_sp_account({
    address: "addr1qx...abc",
    asset: "iUSD",
    amount: "500000000",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. Creates a pending deposit request.
```

**Withdraw iAssets from a stability pool account:**

```
User: "Withdraw 200 iUSD from my stability pool"
→ First call get_sp_account_by_owner to find the account UTxO.
→ Call adjust_sp_account({
    address: "addr1qx...abc",
    asset: "iUSD",
    amount: "-200000000",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. Creates a pending withdrawal request.
  Note: Withdrawals use a negative amount.
```

**Partial withdrawal from an iBTC pool:**

```
User: "Take out 0.1 iBTC from my stability pool position"
→ First call get_sp_account_by_owner to find the account UTxO.
→ Call adjust_sp_account({
    address: "addr1qx...abc",
    asset: "iBTC",
    amount: "-10000000",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR for signing.
```

---

### close_sp_account

Close a stability pool account entirely, withdrawing all deposited iAssets and earned rewards (ADA from liquidation gains and INDY staking rewards).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `accountTxHash` | `string` | Yes | Transaction hash of the account UTxO |
| `accountOutputIndex` | `number` | Yes | Output index of the account UTxO |

#### Examples

**Close an account and claim all rewards:**

```
User: "Close my iUSD stability pool account"
→ First call get_sp_account_by_owner to find the account UTxO.
→ Call close_sp_account({
    address: "addr1qx...abc",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. Upon signing and submitting:
  - All deposited iAssets are returned
  - Earned ADA from liquidation gains is claimed
  - Accumulated INDY rewards are claimed
```

**Close account after checking balance first:**

```
User: "How much do I have in the stability pool? Then close it."
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Present the deposit amount and accumulated rewards.
→ Call close_sp_account({
    address: "addr1qx...abc",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR for signing.
```

**Close one of multiple accounts:**

```
User: "Close my iBTC stability pool position but keep my iUSD one"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Identify the iBTC account UTxO from the results.
→ Call close_sp_account({
    address: "addr1qx...abc",
    accountTxHash: "def456...ghi",
    accountOutputIndex: 1
  })
→ Returns unsigned tx CBOR. Only the iBTC account is closed.
```