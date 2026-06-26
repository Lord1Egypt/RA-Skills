---
name: integration-webhooks
description: Webhook node patterns — paths, response modes, test vs production URLs.
user-invocable: false
---

# Webhooks

## Node types

- `n8n-nodes-base.webhook` — incoming webhook trigger.
- `n8n-nodes-base.respondToWebhook` — explicit response (when not using `responseMode: lastNode`).

## Path conventions

Webhook paths are env-agnostic but share a base URL per env. Use a stable, descriptive path:

```json
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "httpMethod": "POST",
    "path": "report/daily",
    "responseMode": "lastNode"
  }
}
```

n8n exposes the webhook at `<instance>/webhook/<path>` (production) and `<instance>/webhook-test/<path>` (test mode in the UI). `run.py` tries production first, then falls back to test.

## Response modes

- `responseMode: lastNode` — n8n returns the last node's output as the response. Simplest case.
- `responseMode: responseNode` — terminate flow with `respondToWebhook` to control status/headers/body explicitly.

## Authentication

- **None** — public webhook. Fine for triggers from trusted sources (or with HMAC-verifying middleware in the workflow).
- **Header Auth** — n8n verifies a header against a credential. Credential type: `httpHeaderAuth`.
- **Basic Auth** — credential type: `httpBasicAuth`.

For credential setup, see [`skills/manage-credentials.md`](../../manage-credentials.md).

## webhookId placeholder

n8n's webhook node has a `webhookId` field that contains a UUID identifying the public webhook URL. Use `{{@uuid:webhook-public}}` so each env gets its own (the path is shared but the public webhook URL varies).
