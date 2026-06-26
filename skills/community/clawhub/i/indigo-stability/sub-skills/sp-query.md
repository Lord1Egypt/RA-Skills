# Stability Pool Queries

Query stability pool state, accounts, and balances.

## Tools

### get_stability_pools

List all stability pools with their snapshot state (snapshotP, snapshotD, snapshotS), epoch, and scale values.

**Parameters:** None

#### Examples

**List all stability pools with TVL:**

```
User: "Show me all stability pools"
→ Call get_stability_pools()
→ Returns pool state for each iAsset (iUSD, iBTC, iETH, iSOL) including
  snapshot values and epoch/scale data.
```

**Query pool state for a specific iAsset:**

```
User: "What's the current state of the iUSD stability pool?"
→ Call get_stability_pools()
→ Filter response for iUSD pool and present snapshot values, epoch, and scale.
```

**Compare pools across iAssets:**

```
User: "Compare the iUSD and iBTC stability pools"
→ Call get_stability_pools()
→ Present both pools side-by-side with their deposit totals and snapshot data.
```

---

### get_stability_pool_accounts

List all accounts in a stability pool, optionally filtered by iAsset.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | No | Filter accounts by iAsset |

#### Examples

**List all iUSD stability pool accounts:**

```
User: "Show all accounts in the iUSD stability pool"
→ Call get_stability_pool_accounts({ asset: "iUSD" })
→ Returns all accounts with deposit amounts and pending rewards.
```

**List all accounts across all pools:**

```
User: "Show me every stability pool account"
→ Call get_stability_pool_accounts()
→ Returns all accounts across all iAsset pools.
```

**Find top depositors in the iBTC pool:**

```
User: "Who are the largest depositors in the iBTC stability pool?"
→ Call get_stability_pool_accounts({ asset: "iBTC" })
→ Sort results by deposit amount descending and present the top accounts.
```

---

### get_sp_account_by_owner

Look up stability pool accounts by owner address or payment key hash. Returns deposit amount, rewards, and pending requests.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owners` | `string[]` | Yes | Array of payment key hashes or bech32 addresses |

#### Examples

**Check a single owner's stability pool positions:**

```
User: "Show my stability pool accounts"
→ Call get_sp_account_by_owner({
    owners: ["addr1qx...abc"]
  })
→ Returns all SP accounts owned by that address, including deposits,
  earned rewards, and any pending requests.
```

**Look up multiple owners at once:**

```
User: "Check stability pool accounts for these two addresses"
→ Call get_sp_account_by_owner({
    owners: [
      "addr1qx...abc",
      "addr1qy...def"
    ]
  })
→ Returns accounts for both owners in a single call.
```

**Check if an address has any SP positions:**

```
User: "Does addr1qx...abc have any stability pool deposits?"
→ Call get_sp_account_by_owner({
    owners: ["addr1qx...abc"]
  })
→ If empty, the address has no stability pool accounts.
  If populated, show deposit amounts per iAsset pool.
```
