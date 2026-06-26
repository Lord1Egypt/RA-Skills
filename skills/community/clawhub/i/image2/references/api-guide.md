# image2 API Guide

## Endpoint

- Method: `POST`
- Path: `/api/v1/user_task/asyncCreateWithCost`
- Query Method: `GET`
- Query Path: `/api/v1/user_task/get/passAuth/{id}`
- Recommended base URL: `https://kexiangai.com`
- Full URL example: `https://kexiangai.com/api/v1/user_task/asyncCreateWithCost`
- Query URL example: `https://kexiangai.com/api/v1/user_task/get/passAuth/13170`

## Headers

- `Content-Type: application/json` (required)
- `x-api-key: <YOUR_X_API_KEY>` (required)

## Request Body

```json
{
  "cost_type": 1,
  "business_url": "gpt-image2/img",
  "user_input": {
    "modelName": "GPT-Image-2",
    "modelType": "text2img",
    "prompt": "为图片中的产品生成一个海报,4K",
    "size": "3:4",
    "urls": [
      "https://example.com/reference.png"
    ]
  }
}
```

## Field Constraints

- `cost_type`: fixed `1`
- `business_url`: fixed `gpt-image2/img`
- `user_input.modelName`: recommended `GPT-Image-2`
- `user_input.modelType`: `text2img` or `img2img`
- `user_input.prompt`: required, non-empty string
- `user_input.size`: required, one of:
  - `auto`, `1:1`, `3:2`, `2:3`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `9:21`, `1:3`, `3:1`, `2:1`, `1:2`
- `user_input.urls`:
  - required when `modelType=img2img`
  - optional/empty when `modelType=text2img`
  - at most 8 URLs

## Response (Creation Success)

Typical response includes:

- `id`: task id
- `task_status`: typically `pending`
- `cost`: billing cost string
- `user_input`: echoed payload

Example:

```json
{
  "id": 13170,
  "task_status": "pending",
  "cost": "0.2",
  "user_input": {
    "modelName": "GPT-Image-2",
    "modelType": "img2img",
    "prompt": "为图片中的产品生成一个海报,4K",
    "size": "3:4",
    "urls": [
      "https://example.com/reference.png"
    ]
  }
}
```

## Query Task Result

Request example:

```bash
curl --location 'https://kexiangai.com/api/v1/user_task/get/passAuth/13170' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>'
```

Typical query response includes:

- `id`: task id
- `task_status`: `pending` / `running` / `success` / `failed` (provider-dependent)
- `service_output`: final output or failure reason

Result extraction priority:

1. `service_output.imgUrls` (array)
2. `service_output.imgUrl` (single URL)
3. If failed, `service_output.failReason`

Polling recommendation:

- interval: 5-10 seconds
- stop when status is terminal (`success`, `failed`, `error`, `canceled`)
- set max attempts to avoid infinite loop

## Notes

- This API creates an async task. It may return `pending` immediately.
- After task creation, call the query endpoint until terminal status is returned.
- Keep dedup logic in client/skill side to avoid duplicated cost.
- Never print full `x-api-key` in logs or user-visible output.
