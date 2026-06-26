# Pay — Error Codes & Recovery

## Critical rule

NEVER blind-retry a payment. Double-pay is unrecoverable. Read the
error code, understand the cause, then decide.

## Error table

| Error | Meaning | Recovery |
|-------|---------|----------|
| `INSUFFICIENT_BALANCE` | Wallet or tab is empty | `pay fund` -> present link to operator -> wait for funding -> retry |
| `BELOW_MINIMUM` | Direct < $1 or tab open < $5 | Increase amount. For sub-$1 payments, use tab settlement via x402. |
| `TAB_DEPLETED` | Tab balance is zero | `pay tab topup <id> <amount>` (with operator confirmation) then retry |
| `NONCE_REUSED` | Duplicate payment nonce | CLI auto-handles on retry. If manual, generate new nonce. |
| `RATE_LIMITED` | Too many requests per window | Wait `retry_after` seconds, then retry. Do not loop. |
| `INVALID_ADDRESS` | Malformed recipient address | Check the 0x address. Must be 42 characters, valid hex. |
| `SELF_PAYMENT` | Sending to yourself | Not allowed. Use a different recipient. |
| `TAB_NOT_FOUND` | Tab ID doesn't exist | Check `pay tab list` for valid IDs. |
| `UNAUTHORIZED` | Auth failure or wrong wallet | CLI may need re-init. Check `pay address` matches expected wallet. |
| `PROVIDER_ONLY` | Non-provider tried to charge tab | Only the tab's provider can charge it. |
| `MANDATE_VIOLATION` | AP2 mandate bounds exceeded | Payment exceeds mandate constraints (amount, expiry, issuer). Renegotiate mandate. |

## Patterns

### Insufficient balance flow

```
1. Payment fails with INSUFFICIENT_BALANCE
2. Run `pay fund` -> get link
3. Present link to operator for approval before sharing
4. Poll briefly (1-2 minutes, short intervals)
5. If funded -> confirm with operator, then retry payment
6. If not funded -> report to operator, move on
7. Fund link expires in 1 hour
```

### Tab depleted during use

```
1. Charge fails with TAB_DEPLETED
2. Inform operator, suggest: pay tab topup <id> <amount>
3. If topup fails (insufficient balance) -> funding flow above
4. Retry the charge after confirmation
```

### Rate limited

```
1. Request returns RATE_LIMITED with retry_after header
2. Wait exactly retry_after seconds (do not add buffer)
3. Retry once
4. If still limited -> report to operator
```

### Unknown errors

If the CLI returns an error not in this table:
1. Report the raw error to the operator
2. Do not attempt recovery
3. Do not retry
