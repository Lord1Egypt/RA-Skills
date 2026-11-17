# HTTP contracts

Base URL:

```text
https://mongol.open-idea.net/api/v1
```

Every endpoint path must end with `/`. Do not follow redirects for POST requests.

Authenticate with:

```http
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
```

JSON requests also use `Content-Type: application/json`.

## Endpoints

| Method and path | Request | Success result |
|---|---|---|
| `POST /translation/` | JSON `from`, `to`, `content` | `data.tgtText` |
| `POST /chat/completions/` | JSON chat payload | `choices[0].message.content` |
| `POST /ocr/` | JSON image Base64 | `data.text` |
| `POST /audio/` | multipart audio | `data.text` |
| `POST /audio/async/` | multipart audio | 202 + job identifier |
| `GET /audio/async/{jobId}/` | none | 202 processing or 200 + `data.text` |
| `POST /tts/` | JSON TTS payload | binary audio |
| `POST /tts/async/` | JSON TTS payload | 202 + job identifier |
| `GET /tts/async/{jobId}/` | none | 202 processing or 200 + `audioBase64` |
| `POST /word/translation/` | multipart document | `data.text` |
| `POST /pdf/translation/` | multipart document | `data.text` |

Asynchronous endpoints may use either `jobId` or `job_id`, and may report `done` or `completed`. Treat 422 or `failed` as terminal.

## Billing metadata

Read both headers and JSON because asynchronous billing can appear in the completed job body.

Headers:

```text
X-Mengguyu-Billing-Charged
X-Mengguyu-Billing-Balance
X-Mengguyu-Billing-Currency
```

Common JSON keys:

```text
billingCharged
billingBalance
billingCurrency
```

When charged amount and balance are available, emit:

```text
本次扣费: {charged} {currency}, 余额: {balance} {currency}
```

Do not invent missing billing values.

## HTTP handling

- 2xx: process the documented result.
- 3xx: fail; do not redirect a POST.
- 4xx: fail without blind retry.
- 429: bounded retry is allowed when the server has not accepted a job.
- 5xx: bounded retry is allowed.
- ambiguous POST transport error: fail without retry.
- GET polling transport error: bounded retry.

Never print a full error body. Return a sanitized message or HTTP status and request identifier.
