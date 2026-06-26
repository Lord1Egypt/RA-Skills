# SkillPay API Contract (P0 Assumptions)

## Charge Endpoint

- Method: `POST`
- Path: `/billing/charge`
- Full URL: from `SKILLPAY_CHARGE_ENDPOINT`

Request body:

```json
{
  "user_id": "user_001",
  "amount": "0.10",
  "currency": "USDT",
  "item": "ecommerce-ad-copy-generator",
  "metadata": {
    "product_name": "CloudBoost 智能投放器",
    "target_audience": "跨境电商运营团队"
  },
  "trace_id": "uuid"
}
```

## Expected Success Response

```json
{
  "success": true,
  "transaction_id": "tx_123"
}
```

## Insufficient Balance Response (Examples)

HTTP `402` or JSON contains balance-insufficient semantic fields.

```json
{
  "success": false,
  "code": "INSUFFICIENT_BALANCE",
  "payment_url": "https://skillpay.me/pay?user_id=user_001"
}
```

## Error Mapping Rules

- `402` or body text with `insufficient/balance/not_enough/low_balance` => `INSUFFICIENT_BALANCE`
- Other non-2xx => `BILLING_ERROR`
- Network exceptions => `BILLING_ERROR` with network context

## Payment URL Fallback

Priority:
1. `payment_url` / `pay_url` from charge response
2. `SKILLPAY_PAYMENT_URL_TEMPLATE` (supports `{user_id}`)
3. `SKILLPAY_TOPUP_BASE_URL` + `?user_id=<id>`

## Security Notes

- Never hardcode API keys.
- Keep `SKILLPAY_API_KEY` in environment variables.
- Do not print secret tokens into logs.
