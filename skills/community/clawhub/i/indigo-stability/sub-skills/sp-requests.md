# Stability Pool Requests

Process and manage pending stability pool requests. Deposit and withdrawal adjustments create pending requests that must be processed (or annulled) in a subsequent transaction.

All operations return an unsigned transaction (CBOR hex) for client-side signing.

## Tools

### process_sp_request

Process a pending stability pool request (deposit adjustment or withdrawal). This is a protocol maintenance operation that finalizes a previously submitted adjust request.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset of the stability pool |
| `accountTxHash` | `string` | Yes | Transaction hash of the account UTxO with the pending request |
| `accountOutputIndex` | `number` | Yes | Output index of the account UTxO |

#### Examples

**Process a pending deposit request:**

```
User: "Process my pending iUSD stability pool deposit"
→ First call get_sp_account_by_owner to find the account and confirm a
  pending request exists.
→ Call process_sp_request({
    address: "addr1qx...abc",
    asset: "iUSD",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. Upon signing and submitting, the deposit
  adjustment is finalized in the stability pool.
```

**Process a pending withdrawal:**

```
User: "I submitted a withdrawal from the iBTC pool — can you process it?"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Verify the iBTC account has a pending withdrawal request.
→ Call process_sp_request({
    address: "addr1qx...abc",
    asset: "iBTC",
    accountTxHash: "def456...ghi",
    accountOutputIndex: 1
  })
→ Returns unsigned tx CBOR. The withdrawal is completed once signed
  and submitted.
```

**Process requests for multiple accounts:**

```
User: "Process all my pending stability pool requests"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Identify all accounts with pending requests.
→ For each account with a pending request, call process_sp_request
  with the appropriate asset and account UTxO details.
→ Each call returns a separate unsigned tx CBOR for signing.
```

---

### annul_sp_request

Cancel a pending stability pool request before it is processed. Use this when a user changes their mind about a deposit or withdrawal.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `accountTxHash` | `string` | Yes | Transaction hash of the account UTxO with the pending request |
| `accountOutputIndex` | `number` | Yes | Output index of the account UTxO |

#### Examples

**Cancel a pending deposit request:**

```
User: "Cancel my pending stability pool deposit"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Find the account with a pending deposit request.
→ Call annul_sp_request({
    address: "addr1qx...abc",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. Upon signing, the pending deposit is
  cancelled and the account reverts to its previous state.
```

**Cancel a withdrawal you no longer want:**

```
User: "I changed my mind — cancel my iUSD withdrawal from the stability pool"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Confirm the iUSD account has a pending withdrawal.
→ Call annul_sp_request({
    address: "addr1qx...abc",
    accountTxHash: "abc123...def",
    accountOutputIndex: 0
  })
→ Returns unsigned tx CBOR. The withdrawal request is cancelled.
```

**Handle error: no pending request to cancel:**

```
User: "Cancel my pending request on the iBTC stability pool"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ Check if the iBTC account has a pending request.
→ If no pending request exists, inform the user:
  "Your iBTC stability pool account has no pending requests to cancel."
→ No transaction is needed.
```

**Handle error: account not found:**

```
User: "Cancel my stability pool request"
→ Call get_sp_account_by_owner({ owners: ["addr1qx...abc"] })
→ If no accounts are returned, inform the user:
  "No stability pool accounts found for your address."
→ No transaction is needed.
```