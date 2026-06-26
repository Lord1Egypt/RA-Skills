# Skillpay.me API Reference

## Overview

This skill integrates with skillpay.me for pay-per-use monetization.

## Configuration

- **API Key**: Set via `SKILLPAY_API_KEY` environment variable
- **Skill ID**: Set via `SKILLPAY_SKILL_ID` environment variable
- **Price**: 0.001 USDT per request
- **API Endpoint**: `https://skillpay.me`

## API Usage

### Create Charge

```python
POST https://skillpay.me/api/v1/billing/charge

Headers:
  Content-Type: application/json
  X-API-Key: <your-api-key>

Body:
{
  "user_id": "user_123",
  "skill_id": "your-skill-id",
  "amount": 0.001
}
```

### Response

```json
{
  "success": true,
  "transaction_id": "tx_20240305010203",
  "amount": "0.001",
  "currency": "USDT",
  "status": "completed",
  "timestamp": "2024-03-05T01:02:03Z"
}
```

## Integration in Code

The payment is automatically processed in `scripts/process_record.py`:

```python
from scripts.process_record import process_medical_record
import os

# Set environment variables
os.environ["SKILLPAY_API_KEY"] = "your-api-key"
os.environ["SKILLPAY_SKILL_ID"] = "your-skill-id"

result = process_medical_record(
    input_text="患者信息...",
    user_id="user_123"
)

if result['success']:
    print("Payment processed, balance:", result['balance'])
    print("Structured record:", result['structured_record'])
else:
    print("Error:", result['error'])
    if 'paymentUrl' in result:
        print("Payment URL:", result['paymentUrl'])
```

## Pricing

| Service | Price | Currency |
|---------|-------|----------|
| Medical Record Structuring | 0.001 | USDT |

## Notes

- Payment must be completed before processing
- Failed payments return error without processing the record
- Transaction IDs are logged for reconciliation
