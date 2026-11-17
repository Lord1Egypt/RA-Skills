---
name: mapleflow
description: Call MapleFlow for AI chat, image generation, masked image erase, speech, transcription, embeddings, translation, weather, currency, and face comparison using one API key and credit balance.
metadata:
  openclaw:
    requires:
      env:
        - MAPLEFLOW_API_KEY
      bins:
        - curl
    primaryEnv: MAPLEFLOW_API_KEY
---

# MapleFlow API

Base URL: `https://api.mapleflow.io`. Pass `X-API-Key: $MAPLEFLOW_API_KEY`
on authenticated requests. Keep the key out of messages and logs.

## Discover current models and schemas

Use `GET /v1/models` for public chat model names. Read
`GET /openapi.json` for supported request fields and model enums, including
provider overrides. Both discovery endpoints are public. Interactive docs:
`https://api.mapleflow.io/docs`.

Use model names exactly as returned. Hosted model availability differs from
provider announcements; never invent a model ID or substitute a provider.

## AI chat

POST `/ai/chat` with `messages`, optional `model`, and positive integer
`max_tokens`. Messages contain `role` and string `content`.

```bash
curl --fail-with-body https://api.mapleflow.io/ai/chat \
  -H "X-API-Key: $MAPLEFLOW_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Reply with OK"}],"model":"gpt-4o-mini","max_tokens":128}'
```

Response: `{"success":true,"data":{"model":"gpt-4o-mini","response":"OK"}}`.
Chat credits depend on tokens and the selected serving route. An estimate is
reserved before inference; unused credits are refunded after gateway cost
settlement. Minimum 0.01 credit; reduce `max_tokens` if the balance is insufficient.

OpenAI-compatible clients can use base URL `https://api.mapleflow.io/v1`,
API key `MAPLEFLOW_API_KEY`, and POST `/v1/chat/completions`. This endpoint
returns OpenAI-format JSON and accepts `max_tokens` or `max_completion_tokens`.
Streaming is not supported. The default chat model is `llama-3.2-1b` on
`/ai/chat` and `llama-3.1-8b` on `/v1/chat/completions`.

## Other endpoints

| Endpoint | Method | Request | Credits |
|---|---|---|---|
| `/ai/images` | POST | JSON `{prompt, model:"flux-schnell", num_steps:4}` | 5 |
| `/ai/speech` | POST | JSON `{text, model:"melotts"}` | 2 |
| `/ai/transcribe` | POST | Multipart `audio` file, optional `model:"whisper"` | 2 |
| `/ai/embeddings` | POST | JSON `{text:string\|string[], model:"bge-base-en"}` | 1 |
| `/images/erase` | POST | JSON or multipart `image`, `mask`, optional `prompt` | 3 |
| `/translate` | POST | JSON `{text, from:"auto", to:"es"}` | 1 per 300 characters |
| `/weather` | GET | `?location=Toronto` or `?lat=43.65&lon=-79.38` | 1 |
| `/currency` | GET | `?from=USD&to=EUR&amount=1` | 1 |
| `/verify/face` | POST | See OpenAPI for image fields | 2 |

`/images/erase` uses `sd-1.5-inpainting` for masked editing: white mask pixels
are replaced, black pixels are kept. Return data is a base64 PNG. Image generation,
speech, and transcription responses use the formats documented in OpenAPI.

```bash
curl --fail-with-body https://api.mapleflow.io/ai/transcribe \
  -H "X-API-Key: $MAPLEFLOW_API_KEY" -F 'audio=@recording.wav'
```

`/images/bg-remove` and other disabled models return `MODEL_DISABLED`; do not
advertise them as available. Check the account with authenticated `GET /account`
and recent calls with `GET /account/usage?limit=20`.

## MCP access

Remote HTTP MCP: `https://api.mapleflow.io/mcp`. Use JSON-RPC `initialize`,
`tools/list`, and `tools/call`; tool calls require the API key header.
The npm stdio server is `npx -y @mapleflow/mcp-server`, configured with
`MAPLEFLOW_API_KEY`. It reads the live OpenAPI spec when it starts.

## Errors and purchasing

Inspect HTTP status and the machine-readable `code`, including
`INVALID_MODEL`, `MODEL_DISABLED`, `INSUFFICIENT_CREDITS`, and `RATE_LIMITED`.
Retry transient failures with backoff; do not repeatedly retry invalid input.
Paid credits never expire. Read public `GET /billing/packages` for packages.
Only create a checkout when the user requests a purchase; never purchase credits
automatically to recover a failed call.
