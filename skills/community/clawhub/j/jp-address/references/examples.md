# jp-address — request examples

Set `JPVERIFY_API_KEY` (create one at https://www.jpverify.com/signup?ref=jp-address). Without a key the API answers HTTP 402 with the x402 price; see https://api.jpverify.com/docs/x402 for x402 SDK code.

## `POST /v1/jp/addresses/normalize` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/normalize \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/normalize",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/validate` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/validate \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "required_level": 8, "strict": false}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/validate",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "required_level": 8, "strict": False},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/parse` — $0.002

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/parse \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "response_language": "ja"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/parse",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "response_language": "ja"},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/addresses/geocode` — $0.005

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/geocode \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都千代田区千代田1丁目1番1号", "max_candidates": 3}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/geocode",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"address": "東京都千代田区千代田1丁目1番1号", "max_candidates": 3},
    timeout=60,
)
print(response.status_code, response.json())
```

## `POST /v1/jp/postal-codes/lookup` — $0.001

```bash
curl -X POST https://api.jpverify.com/v1/jp/postal-codes/lookup \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"postal_code": "100-0001", "max_results": 10}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/postal-codes/lookup",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"postal_code": "100-0001", "max_results": 10},
    timeout=60,
)
print(response.status_code, response.json())
```
