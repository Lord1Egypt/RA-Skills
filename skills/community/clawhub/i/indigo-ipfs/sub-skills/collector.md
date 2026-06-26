# Collector

Query collector UTXOs for fee distribution in the Indigo Protocol.

## Tools

### get_collector_utxos

Get collector UTXOs that hold accumulated protocol fees. These UTXOs can be queried to inspect fee distribution state.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `length` | number | No | Maximum number of UTXOs to return |

## Examples

### Check accumulated protocol fees

View all collector UTXOs to see how much in protocol fees has accumulated and is available for distribution.

**Prompt:** "How much in protocol fees has accumulated in the collector?"

**Workflow:**

1. Call `get_collector_utxos` with no parameters to retrieve all UTXOs:
   ```
   get_collector_utxos({})
   ```
2. Sum up the ADA values and any native token amounts across all returned UTXOs.
3. Present the total accumulated fees broken down by asset.

**Sample response:**

```
Collector Fee Summary
─────────────────────
Total UTXOs: 8

Accumulated fees:
  ADA:   12,450.32
  iUSD:  3,210.00
  iBTC:  0.045
  iETH:  1.82
  INDY:  580.00

These fees are available for distribution to protocol participants.
```

### Paginated collector query

Retrieve a limited number of collector UTXOs to inspect the most recent fee accumulations without fetching the entire set.

**Prompt:** "Show me the first 5 collector UTXOs"

**Workflow:**

1. Call `get_collector_utxos` with a length limit:
   ```
   get_collector_utxos({ "length": 5 })
   ```
2. Format each UTXO showing its transaction hash, index, and asset values.

**Sample response:**

```
Collector UTXOs (showing 5)
───────────────────────────
#1  tx: a1b2c3...d4e5  index: 0
    ADA: 1,500.00 | iUSD: 420.50

#2  tx: f6g7h8...i9j0  index: 1
    ADA: 2,100.00 | iBTC: 0.012

#3  tx: k1l2m3...n4o5  index: 0
    ADA: 980.00

#4  tx: p6q7r8...s9t0  index: 2
    ADA: 3,200.00 | iETH: 0.65

#5  tx: u1v2w3...x4y5  index: 0
    ADA: 1,870.00 | INDY: 145.00
```

### Monitor fee distribution readiness

Check collector UTXOs to determine if enough fees have accumulated to warrant triggering a distribution.

**Prompt:** "Are there enough fees in the collector to distribute?"

**Workflow:**

1. Call `get_collector_utxos` to retrieve all UTXOs:
   ```
   get_collector_utxos({})
   ```
2. Calculate total ADA value across all UTXOs.
3. Compare against a reasonable distribution threshold (e.g., 10,000 ADA).
4. Report whether distribution is recommended.

**Sample response:**

```
Fee Distribution Status
───────────────────────
Total collected: 12,450.32 ADA + native tokens
UTXO count: 8
Threshold: 10,000 ADA

✓ Sufficient fees accumulated for distribution.
  Consider triggering a collector distribution to
  allocate fees to INDY stakers and stability providers.
```

## Example Prompts

- "Show me the collector UTXOs"
- "How much in fees has the protocol collected?"
- "List the first 10 collector UTXOs"
- "Is there enough in the collector for a distribution?"
