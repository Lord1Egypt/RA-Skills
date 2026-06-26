---
name: integration-sentry
description: Sentry as the audit destination for n8n error handlers — envelope POST via HTTP Request, DSN auth, tag conventions for grouping.
user-invocable: false
---

# Sentry

## Node type

`n8n-nodes-base.httpRequest`. There is no dedicated `n8n-nodes-base.sentry` node — Sentry is HTTP-shaped end-to-end.

## Credential type

Two ways to authenticate to Sentry's ingest endpoint:

1. **Embedded DSN auth (recommended for the envelope endpoint)** — the DSN string contains both the project ID and the public key. No credential needed; the DSN goes in the URL.
2. **`httpHeaderAuth` with a Bearer token** — for the legacy `/store/` endpoint or for Sentry's REST management API. Get a token from Sentry → Settings → Account → API → Auth Tokens.

The envelope endpoint with DSN-in-URL is the simpler, current-recommended path. Treat the DSN as a secret and store it in `.env.<env>`:

```bash
# .env.<env>
SENTRY_DSN=https://<public_key>@o<org_id>.ingest.sentry.io/<project_id>
```

Resolve via `{{@env:sentry.dsn}}` (after wiring `sentry.dsn: "${SENTRY_DSN}"` in your env YAML). See [`skills/manage-credentials.md`](../../manage-credentials.md) for the env-secret pattern.

## Endpoint

**Current (envelope):**
```
POST https://o<org_id>.ingest.sentry.io/api/<project_id>/envelope/
```

The envelope endpoint accepts events wrapped in a multi-line newline-delimited envelope structure. For the simpler "send one event" case, the envelope body is three lines: header, item-header, item-payload.

**Legacy (deprecated, still works):**
```
POST https://sentry.io/api/<project_id>/store/
Header: X-Sentry-Auth: Sentry sentry_version=7, sentry_key=<public_key>, sentry_client=n8n/1.0
Body: <event JSON>
```

The legacy `/store/` endpoint is documented as deprecated by Sentry but is widely used in custom integrations and will keep working for the foreseeable future. If your Sentry environment supports the envelope endpoint, prefer it.

## Worked example: HTTP Request node sending an envelope

This is the node body inside an n8n error handler, fed by the `Build Context` Code node from [`patterns/error-handling.md`](../../patterns/error-handling.md). The DSN can be baked into the URL via expression — DSN-in-URL skips the X-Sentry-Auth header entirely.

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "POST",
    "url": "={{ 'https://o' + $env.SENTRY_ORG_ID + '.ingest.sentry.io/api/' + $env.SENTRY_PROJECT_ID + '/envelope/' }}",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        { "name": "Content-Type", "value": "application/x-sentry-envelope" },
        { "name": "X-Sentry-Auth", "value": "={{ 'Sentry sentry_version=7, sentry_key=' + $env.SENTRY_PUBLIC_KEY + ', sentry_client=n8n/1.0' }}" }
      ]
    },
    "sendBody": true,
    "contentType": "raw",
    "rawContentType": "application/x-sentry-envelope",
    "body": "={{ JSON.stringify({ event_id: $json.execution_id.replace(/-/g,''), sent_at: $json.timestamp, dsn: $env.SENTRY_DSN }) + '\\n' + JSON.stringify({ type: 'event', content_type: 'application/json' }) + '\\n' + JSON.stringify({ event_id: $json.execution_id.replace(/-/g,''), timestamp: Math.floor(new Date($json.timestamp).getTime() / 1000), platform: 'javascript', logger: 'n8n', level: 'error', logentry: { message: $json.message }, exception: { values: [{ type: 'WorkflowError', value: $json.message, stacktrace: { frames: [{ function: $json.last_node, module: $json.workflow_name, in_app: true }] } }] }, tags: { workflow_id: $json.workflow_id, workflow_name: $json.workflow_name, execution_id: $json.execution_id, env: $env.N8N_ENV, last_node: $json.last_node }, extra: { execution_url: $json.execution_url } }) }}",
    "options": { "response": { "response": { "neverError": true } } }
  }
}
```

The body is the three-line envelope: envelope header (with DSN), item header (declaring the event type), then the event JSON payload.

For most cases the simpler legacy `/store/` POST is more readable:

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "POST",
    "url": "={{ 'https://sentry.io/api/' + $env.SENTRY_PROJECT_ID + '/store/' }}",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        { "name": "Content-Type", "value": "application/json" },
        { "name": "X-Sentry-Auth", "value": "={{ 'Sentry sentry_version=7, sentry_key=' + $env.SENTRY_PUBLIC_KEY + ', sentry_client=n8n/1.0' }}" }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify({ event_id: $json.execution_id.replace(/-/g,''), timestamp: Math.floor(new Date($json.timestamp).getTime() / 1000), platform: 'javascript', logger: 'n8n', level: 'error', logentry: { message: $json.message }, exception: { values: [{ type: 'WorkflowError', value: $json.message }] }, tags: { workflow_id: $json.workflow_id, workflow_name: $json.workflow_name, execution_id: $json.execution_id, env: $env.N8N_ENV, last_node: $json.last_node }, extra: { execution_url: $json.execution_url } }) }}",
    "options": { "response": { "response": { "neverError": true } } }
  }
}
```

`response.neverError: true` is critical: a Sentry-side rate limit or 5xx must NOT break the error handler. Log silently and continue.

## Event JSON shape (legacy /store/ form)

```json
{
  "event_id": "<32-char hex>",
  "timestamp": <unix-seconds>,
  "platform": "javascript",
  "logger": "n8n",
  "level": "error",
  "logentry": { "message": "<human-readable>" },
  "exception": {
    "values": [
      {
        "type": "WorkflowError",
        "value": "<error message>",
        "stacktrace": {
          "frames": [
            { "function": "<last_node_name>", "module": "<workflow_name>", "in_app": true }
          ]
        }
      }
    ]
  },
  "tags": {
    "workflow_id": "...",
    "workflow_name": "...",
    "execution_id": "...",
    "env": "...",
    "last_node": "..."
  },
  "extra": {
    "execution_url": "..."
  }
}
```

## Tag conventions

Sentry's grouping algorithm is driven by the `exception.values[].type` and the top frame's `function` + `module`. To make grouping behave well:

- Set `exception.values[0].type` to a stable string like `"WorkflowError"` (not the dynamic error message).
- Put the failing node name in the top frame's `function`. This makes "all errors at the Foo node" cluster together regardless of message.
- Put `workflow_name` in the top frame's `module`. Sentry will then cluster per workflow as the next layer.

Always include the standard tags from [`patterns/error-handling.md`](../../patterns/error-handling.md):

| Tag | Source expression |
|---|---|
| `workflow_id` | `={{ $workflow.id }}` |
| `workflow_name` | `={{ $workflow.name }}` |
| `execution_id` | `={{ $workflow.errorData?.execution?.id || $execution.id }}` |
| `env` | `{{@env:name}}` |
| `last_node` | `={{ $workflow.errorData?.lastNodeExecuted }}` |

Add business-relevant tags (`scope`, `user_id`, `tenant_id`) so Sentry filtering reflects what your on-call actually needs.

## See also

- [`patterns/error-handling.md`](../../patterns/error-handling.md) — three-step paradigm + worked handler example.
- [`manage-credentials.md`](../../manage-credentials.md) — DSN as env-secret.
