# jp-supplier-due-diligence — request examples

Set `JPVERIFY_API_KEY` (create one at https://www.jpverify.com/signup?ref=jp-supplier-due-diligence). Without a key the API answers HTTP 402 with the x402 price; see https://api.jpverify.com/docs/x402 for x402 SDK code.

## `POST /v1/jp/companies/resolve` — $0.25

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    json={"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/suppliers/resolve` — $0.10

```bash
curl -X POST https://api.jpverify.com/v1/jp/suppliers/resolve \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "株式会社ABC", "registration_number": "T1013301046627", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/suppliers/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    json={"name": "株式会社ABC", "registration_number": "T1013301046627", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/check-issuer` — $0.05

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoices/check-issuer \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/check-issuer",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    json={"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/regulated-entities/verify` — $0.03

```bash
curl -X POST https://api.jpverify.com/v1/jp/regulated-entities/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"corporate_number": "1234567890123", "categories": ["funds_transfer_business"], "response_language": "en"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/regulated-entities/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    json={"corporate_number": "1234567890123", "categories": ["funds_transfer_business"], "response_language": "en"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `GET /v1/jp/filings` — $0.01

```bash
curl -G https://api.jpverify.com/v1/jp/filings \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  --data-urlencode 'edinet_code=E00000' \
  --data-urlencode 'limit=20' \
  --data-urlencode 'response_language=en'
```

```python
import os, requests

response = requests.get(
    "https://api.jpverify.com/v1/jp/filings",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    params={"edinet_code": "E00000", "limit": 20, "response_language": "en"},
    timeout=60,
)
print(response.status_code, response.json())
```
