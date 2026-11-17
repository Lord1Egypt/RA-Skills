# jp-invoice-number-check — request examples

Set `JPVERIFY_API_KEY` (create one at https://www.jpverify.com/signup?ref=jp-invoice-number-check). Without a key the API answers HTTP 402 with the x402 price; see https://api.jpverify.com/docs/x402 for x402 SDK code.

## `POST /v1/jp/invoice-registrations/verify` — $0.01

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoice-registrations/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-invoice-number-check/1.3.5"},
    json={"registration_number": "T1013301046627", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/check-issuer` — $0.05

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoices/check-issuer \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/check-issuer",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-invoice-number-check/1.3.5"},
    json={"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoice-registrations/verify-batch` — $0.008 per item

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify-batch \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_numbers": ["T1013301046627"], "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoice-registrations/verify-batch",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-invoice-number-check/1.3.5"},
    json={"registration_numbers": ["T1013301046627"], "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/check-issuer-batch` — $0.04 per item

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoices/check-issuer-batch \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"registration_number": "T1013301046627", "supplier_name": "宏達株式会社", "invoice_date": "2026-10-31"}], "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/check-issuer-batch",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-invoice-number-check/1.3.5"},
    json={"items": [{"registration_number": "T1013301046627", "supplier_name": "宏達株式会社", "invoice_date": "2026-10-31"}], "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```
