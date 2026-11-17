# jpverify — request examples

Set `JPVERIFY_API_KEY` (create one at https://www.jpverify.com/signup?ref=jpverify). Without a key the API answers HTTP 402 with the x402 price; see https://api.jpverify.com/docs/x402 for x402 SDK code.

## `POST /v1/jp/companies/resolve` — $0.25

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoice-registrations/verify` — $0.01

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoice-registrations/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"registration_number": "T1013301046627", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/check-issuer` — $0.05

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoices/check-issuer \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/check-issuer",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"registration_number": "T1013301046627", "supplier_name": "株式会社ABC", "address": "東京都千代田区千代田1-1", "invoice_date": "2026-11-01", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoice-registrations/verify-batch` — $0.008 per item

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify-batch \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_numbers": ["T1013301046627"], "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoice-registrations/verify-batch",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"registration_numbers": ["T1013301046627"], "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/check-issuer-batch` — $0.04 per item

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoices/check-issuer-batch \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"registration_number": "T1013301046627", "supplier_name": "宏達株式会社", "invoice_date": "2026-10-31"}], "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/check-issuer-batch",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"items": [{"registration_number": "T1013301046627", "supplier_name": "宏達株式会社", "invoice_date": "2026-10-31"}], "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/companies/verify` — $0.01

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "トヨタ自動車株式会社", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"name": "トヨタ自動車株式会社", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/companies/report` — $0.10

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/report \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "株式会社ABC", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/report",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"name": "株式会社ABC", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/companies/verify-batch` — $0.008 per item

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/verify-batch \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"corporate_number": "1180301018771"}], "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/verify-batch",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"items": [{"corporate_number": "1180301018771"}], "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/suppliers/resolve` — $0.10

```bash
curl -X POST https://api.jpverify.com/v1/jp/suppliers/resolve \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "株式会社ABC", "registration_number": "T1013301046627", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/suppliers/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"name": "株式会社ABC", "registration_number": "T1013301046627", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/regulated-entities/verify` — $0.03

```bash
curl -X POST https://api.jpverify.com/v1/jp/regulated-entities/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"corporate_number": "1234567890123", "categories": ["funds_transfer_business"], "response_language": "en"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/regulated-entities/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"corporate_number": "1234567890123", "categories": ["funds_transfer_business"], "response_language": "en"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `GET /v1/jp/filings` — $0.01

```bash
curl -G https://api.jpverify.com/v1/jp/filings \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  --data-urlencode 'edinet_code=E00000' \
  --data-urlencode 'limit=20' \
  --data-urlencode 'response_language=en'
```

```python
import os, requests

response = requests.get(
    "https://api.jpverify.com/v1/jp/filings",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    params={"edinet_code": "E00000", "limit": 20, "response_language": "en"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/normalize` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/normalize \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/normalize",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/parse` — $0.002

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/parse \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "response_language": "ja"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/parse",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "response_language": "ja"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/postal-codes/lookup` — $0.001

```bash
curl -X POST https://api.jpverify.com/v1/jp/postal-codes/lookup \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"postal_code": "100-0001", "max_results": 10}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/postal-codes/lookup",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"postal_code": "100-0001", "max_results": 10},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/geocode` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/geocode \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "max_candidates": 3}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/geocode",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "max_candidates": 3},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/validate` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/validate \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "required_level": 8, "strict": false}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/validate",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "required_level": 8, "strict": False},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/invoices/validate-pint` — $0.02

```bash
# invoice.xml: your JP PINT 1.1.3 UBL Invoice
jq -n --rawfile xml invoice.xml '{xml: $xml, registry_enhance: true}' |
  curl -X POST https://api.jpverify.com/v1/jp/invoices/validate-pint \
    -H "Authorization: Bearer $JPVERIFY_API_KEY" \
    -H "X-JPVerify-Client: jpverify/1.3.5" \
    -H "Content-Type: application/json" \
    --data-binary @-
```

```python
import os, pathlib, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/validate-pint",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"xml": pathlib.Path("invoice.xml").read_text(encoding="utf-8"), "registry_enhance": True},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/batch-jobs` — per item (x402 only)

x402 only (not available with an API key). Choose your own capability token (32+ characters) and a unique `Idempotency-Key` per job.

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/batch-jobs \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Authorization: Bearer REPLACE_WITH_YOUR_OWN_RANDOM_TOKEN_32_CHARS_OR_MORE" \
  -H "Idempotency-Key: my-batch-job-0001" \
  -H "Content-Type: application/json" \
  -d '{"operation": "invoice_registration_verify", "items": [{"registration_number": "T1013301046627"}, {"registration_number": "T1180301018771"}], "response_language": "en"}'
```
