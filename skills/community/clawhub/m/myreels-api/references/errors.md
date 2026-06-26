# Error Handling

### Task Submission Status Codes

| Status | Meaning |
|--------|------|
| 200 | Task created successfully |
| 400 | Empty body, invalid field format, or missing required parameters |
| 401 | Missing Authorization header, or invalid / expired token |
| 402 | Insufficient points |
| 403 | Model requires extra permission or subscription |
| 404 | `modelName` not found |
| 500 | Server-side processing error |
| 507 | Insufficient storage |

### Task Query Status Codes

| Status | Meaning |
|--------|------|
| 200 | Query succeeded |
| 400 | Invalid task ID format or invalid request |
| 401 | Missing Authorization header, or invalid / expired token |
| 404 | Task not found, or not accessible for the current user |
| 429 | Query rate too high |
| 500 | Server-side processing error |

### Task List Query Status Codes

| Status | Meaning |
|--------|------|
| 200 | Query succeeded |
| 400 | Invalid `page`, `limit`, or `status` value |
| 401 | Missing Authorization header, or invalid / expired token |
| 500 | Server-side processing error |

### Task Status Enum

Public task status values:

- `pending`
- `processing`
- `completed`
- `failed`
- `cancelled`
- `warning`

### Response Evaluation Order

- If the upstream response includes `code`, Worker uses it as the final HTTP status.
- Otherwise Worker falls back to the upstream HTTP status.
- Check the final HTTP status first.
- If the HTTP status is `2xx`, then inspect the response body `status`.
- `status === "ok"` means success.
- `status === "failed"` means failure.

Example:

```json
{ "status": "failed", "message": "Missing required header: Authorization" }
```

### Error Handling Example

```typescript
const res = await fetch(`https://api.myreels.ai/generation/${modelName}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${ACCESS_TOKEN}`,
  },
  body: JSON.stringify(userInput),
});

const data = await res.json();
if (res.status === 401) throw new Error('Invalid AccessToken');
if (res.status === 402) throw new Error('Insufficient points');
if (res.status === 403) throw new Error('Subscription or permission required');
if (!res.ok || data.status !== 'ok') throw new Error(data.message || 'Task submission failed');
```

### Rate Limit Guidance

- query endpoint limit: 60 requests per minute
- image generation / image editing polling: 10 seconds
- video generation polling: 30 seconds to 1 minute
- if you receive `429`, back off and retry later

### Cost Display Guidance

- use `estimatedCost` as the final user-facing points value

### Public Path Scope

Public paths:

- `POST /generation/:modelName`
- `GET /generation/tasks`
- `GET /query/task/:taskID`
- `GET|POST /api/v1/*`

Other paths may return:

```json
{ "status": "failed", "message": "Path not allowed" }
```
