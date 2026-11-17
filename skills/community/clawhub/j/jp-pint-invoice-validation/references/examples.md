# jp-pint-invoice-validation — request examples

Set `JPVERIFY_API_KEY` (create one at https://www.jpverify.com/signup?ref=jp-pint-invoice-validation). Without a key the API answers HTTP 402 with the x402 price; see https://api.jpverify.com/docs/x402 for x402 SDK code.

## `POST /v1/jp/invoices/validate-pint` — $0.02

```bash
# invoice.xml: your JP PINT 1.1.3 UBL Invoice
jq -n --rawfile xml invoice.xml '{xml: $xml, registry_enhance: true}' |
  curl -X POST https://api.jpverify.com/v1/jp/invoices/validate-pint \
    -H "Authorization: Bearer $JPVERIFY_API_KEY" \
    -H "X-JPVerify-Client: jp-pint-invoice-validation/1.3.5" \
    -H "Content-Type: application/json" \
    --data-binary @-
```

```python
import os, pathlib, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoices/validate-pint",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-pint-invoice-validation/1.3.5"},
    json={"xml": pathlib.Path("invoice.xml").read_text(encoding="utf-8"), "registry_enhance": True},
    timeout=60,
)
print(response.status_code, response.json())
```
