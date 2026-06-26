# nano-banana2 API Guide

## Endpoint

- URL: https://agent.mathmind.cn/minimalist/api/imgEditNB2
- Method: POST
- Headers:
  - Content-Type: application/json
  - x-api-key: required

## Request Body

- prompt: string, required
- urls: string[], optional, default []
- aspectRatio: string, optional, default auto
- imageSize: string, optional, default 1K

### aspectRatio Allowed Values

- auto
- 1:1
- 16:9
- 9:16
- 4:3
- 3:4
- 3:2
- 2:3
- 5:4
- 4:5
- 21:9

### imageSize Allowed Values

- 1K
- 2K
- 4K

## cURL Example

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/imgEditNB2' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--data '{
  "urls": [],
  "prompt": "一只猫咪在玩耍",
  "aspectRatio": "auto",
  "imageSize": "1K"
}'
```

## Common Error Hints

- 401/403: invalid or missing x-api-key
- 429: rate limited, retry later
- 5xx: service unavailable, retry with same payload
