# NanoGPT Usage & Balance APIs

Source: https://docs.nano-gpt.com/api-reference/endpoint/subscription-usage.md
Source: https://docs.nano-gpt.com/api-reference/endpoint/check-balance.md

## Subscription Usage — GET /api/subscription/v1/usage
Auth: `Authorization: Bearer <key>` or `x-api-key: <key>`

```json
{
  "active": true,
  "limits": { "daily": 5000, "monthly": 60000 },
  "enforceDailyLimit": true,
  "daily": {
    "used": 5,
    "remaining": 4995,
    "percentUsed": 0.001,
    "resetAt": 1738540800000
  },
  "monthly": {
    "used": 45,
    "remaining": 59955,
    "percentUsed": 0.00075,
    "resetAt": 1739404800000
  },
  "period": { "currentPeriodEnd": "2025-02-13T23:59:59.000Z" },
  "state": "active",
  "graceUntil": null
}
```

Key fields:
- `active` — account active status
- `daily/monthly.used` — units consumed (NOT tokens — represents completed operations)
- `daily/monthly.remaining` — remaining allowance
- `daily/monthly.resetAt` — Unix ms epoch when window resets
- `state` — `active | grace | inactive`
- `graceUntil` — ISO timestamp when grace access ends

## Check Balance — POST /api/check-balance
Auth: `x-api-key: <key>` (header-based)

```json
{
  "usd_balance": "129.46956147",
  "nano_balance": "26.71801147",
  "nanoDepositAddress": "nano_1gx385..."
}
```

## OpenClaw usage tracking hooks needed
From the SDK provider hooks, these are the relevant ones:
- `resolveUsageAuth` — Custom usage credential parsing
- `fetchUsageSnapshot` — Custom usage endpoint

NanoGPT uses:
- `Authorization: Bearer <key>` for usage endpoint
- Response maps to OpenClaw's usage snapshot format
