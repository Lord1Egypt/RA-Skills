---
name: hotapi
description: Integrate HotAPI image, video, and audio generation into an application. Use for endpoint selection, asynchronous task handling, idempotent submissions, webhooks, errors, credits, and result persistence.
metadata:
  product: "HotAPI"
  version: "1.0"
---

# HotAPI integration

Inspect the target repository before choosing a framework, HTTP client, file layout, or test strategy. Preserve its existing architecture and local instructions.

## Sources of truth

- Exact endpoints and schemas: [OpenAPI 3.1](https://api.hotapi.ai/docs/json)
- Integration guidance: [HotAPI developer docs](https://hotapi.ai/en/docs/getting-started)
- Consolidated agent context: [llms-full.txt](https://hotapi.ai/llms-full.txt)
- Live read-only alternative: `https://hotapi.ai/mcp`

OpenAPI wins when prose and a request schema disagree. Do not infer fields or supported values from memory.

## Integration rules

1. Keep `HOTAPI_KEY` in trusted server-side code. Never expose it to browser code, logs, tests, commits, or an agent transcript.
2. Prefer the typed per-model endpoint for a fixed capability. Use `POST /v1/tasks` only when the model is chosen at runtime.
3. Generate one stable `Idempotency-Key` per business action and reuse it for submission retries.
4. Persist the returned task `id` before waiting. Stop on `succeeded`, `failed`, or `cancelled`; use a bounded poll loop or a signature-verified webhook.
5. Check HTTP status before treating a body as success. Preserve `error.type`, `error.code`, `error.param`, and `request_id`.
6. Copy result assets into application-owned storage before `expires_at` when the product needs durable files.
7. Mock HotAPI in automated tests. Never spend credits from CI.

## Acceptance check

Report the endpoint and model selected, files changed, secret configuration, terminal-state handling, timeout and retry behavior, output persistence, tests run, and one exact manual smoke test.
