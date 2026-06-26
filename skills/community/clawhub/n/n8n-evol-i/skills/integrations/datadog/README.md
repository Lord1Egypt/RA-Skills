---
name: integration-datadog
description: Datadog as the audit destination for n8n error handlers — events POST via HTTP Request, region selection, tag conventions for aggregation.
user-invocable: false
---

# Datadog

## Node type

`n8n-nodes-base.httpRequest`. There is no dedicated `n8n-nodes-base.datadog` node — Datadog is HTTP-shaped.

## Credential type

`httpHeaderAuth` with header `DD-API-KEY: <api_key>`. Get the key from Datadog → Organization Settings → API Keys.

For most error-handling use cases the API key alone is sufficient. The Application Key (`DD-APPLICATION-KEY`) is only required for endpoints that read data on your behalf (querying logs, dashboards, etc.) — POSTing events doesn't need it.

Store as `.env.<env>`:

```bash
# .env.<env>
DD_API_KEY=<your-key>
```

Resolve via `{{@env:credentials.datadog.id}}` / `{{@env:credentials.datadog.name}}` after running `manage-credentials` to register the n8n credential. See [`skills/manage-credentials.md`](../../manage-credentials.md).

## Endpoint

Errors as **events** (recommended for human-readable incident streams):
```
POST https://api.datadoghq.com/api/v1/events
```

Errors as **logs** (alternative — better when you want full-text search across high-volume errors):
```
POST https://api.datadoghq.com/api/v2/logs
```

The events endpoint shows up in Datadog's Event Stream and can drive monitor alerts directly. The logs endpoint shows up in Log Explorer and indexes the body for full-text search. Pick events if your error volume is low (incidents, not noise); pick logs if you want every error retained and queryable.

### Region selection

Datadog hosts per region. The endpoint changes accordingly:

| Region | Base URL |
|---|---|
| US1 (default) | `https://api.datadoghq.com` |
| US3 | `https://api.us3.datadoghq.com` |
| US5 | `https://api.us5.datadoghq.com` |
| EU1 | `https://api.datadoghq.eu` |
| AP1 | `https://api.ap1.datadoghq.com` |
| US-Gov | `https://api.ddog-gov.com` |

Make region env-configurable so a single template runs in EU staging + US prod:

```yaml
# n8n-config/<env>.yml
datadog:
  endpoint: "https://api.datadoghq.com"
  apiKeyEnv: "DD_API_KEY"
```

Then `={{ $env.DD_ENDPOINT || 'https://api.datadoghq.com' }}` in the URL field, or use a `{{@env:datadog.endpoint}}` placeholder.

## Worked example: HTTP Request POST event

Inside an n8n error handler, fed by the `Build Context` Code node from [`patterns/error-handling.md`](../../patterns/error-handling.md):

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "POST",
    "url": "={{ ($env.DD_ENDPOINT || 'https://api.datadoghq.com') + '/api/v1/events' }}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        { "name": "Accept", "value": "application/json" },
        { "name": "Content-Type", "value": "application/json" }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify({ title: 'n8n workflow failed: ' + $json.workflow_name, text: '%%%\\n**Workflow:** ' + $json.workflow_name + '\\n**Last node:** ' + $json.last_node + '\\n**Execution:** [' + $json.execution_id + '](' + ($json.execution_url || '') + ')\\n\\n**Error:**\\n```\\n' + $json.message + '\\n```\\n%%%', tags: ['workflow:' + $json.workflow_name, 'workflow_id:' + $json.workflow_id, 'execution:' + $json.execution_id, 'env:' + ($env.N8N_ENV || 'unknown'), 'last_node:' + $json.last_node, 'alert_type:error'], priority: 'normal', alert_type: 'error', source_type_name: 'n8n', aggregation_key: 'n8n-workflow-' + $json.workflow_id }) }}",
    "options": { "response": { "response": { "neverError": true } } }
  },
  "credentials": {
    "httpHeaderAuth": {
      "id": "{{@env:credentials.datadog.id}}",
      "name": "{{@env:credentials.datadog.name}}"
    }
  }
}
```

Two things worth knowing:

- **`%%%` markers wrap markdown.** Datadog's events API treats text between `%%%` lines as markdown; outside, plain text. Without the markers, the code block won't render.
- **`response.neverError: true`** prevents a Datadog 5xx from breaking the handler. Same reasoning as Sentry — log destinations must not crash the handler.

## Event body shape

```json
{
  "title": "<one-line summary>",
  "text": "%%%\n<markdown body>\n%%%",
  "tags": [
    "workflow:<name>",
    "workflow_id:<id>",
    "execution:<id>",
    "env:<dev|staging|prod>",
    "last_node:<name>",
    "alert_type:error"
  ],
  "priority": "normal",
  "alert_type": "error",
  "source_type_name": "n8n",
  "aggregation_key": "n8n-workflow-<workflow_id>"
}
```

| Field | Why |
|---|---|
| `title` | Shows in event stream + alerts. Keep short, lead with the workflow name. |
| `text` | The detail. Use `%%%`-wrapped markdown so code blocks + links render. |
| `tags` | Datadog tags are `key:value` strings (note the colon, not `key=value`). |
| `priority` | `normal` or `low`. Errors are normal. |
| `alert_type` | `error`, `warning`, `info`, `success`, `user_update`. Drives icon + color. |
| `source_type_name` | Free-form source identifier. Use `"n8n"` so monitor filters can target n8n events. |
| `aggregation_key` | Events with the same key cluster in the stream. Use the workflow id so all errors from the same workflow group together; switch to execution id if you want per-execution clustering instead. |

## Tag conventions

Datadog tags are powerful but quirky:

- **Use `key:value`, not `key=value`** — the colon is the separator.
- **Lowercase keys.** Datadog is case-insensitive on tag keys but normalizes to lowercase; using lowercase explicitly avoids surprises in dashboard queries.
- **Don't put PII in tags.** Tags are indexed and persist; emails, user names, etc. should go in the `text` field instead.

The standard tags from [`patterns/error-handling.md`](../../patterns/error-handling.md):

| Tag | Source expression |
|---|---|
| `workflow:` | `={{ $workflow.name }}` |
| `workflow_id:` | `={{ $workflow.id }}` |
| `execution:` | `={{ $workflow.errorData?.execution?.id || $execution.id }}` |
| `env:` | `{{@env:name}}` |
| `last_node:` | `={{ $workflow.errorData?.lastNodeExecuted }}` |

Add business-relevant tags (`scope:`, `user_id:`, `tenant_id:`) for triage filtering.

## Logs endpoint alternative

If you'd rather ship to Datadog Logs (full-text search, longer retention):

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "POST",
    "url": "={{ ($env.DD_ENDPOINT || 'https://api.datadoghq.com') + '/api/v2/logs' }}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify([{ ddsource: 'n8n', ddtags: 'workflow:' + $json.workflow_name + ',env:' + ($env.N8N_ENV || 'unknown') + ',workflow_id:' + $json.workflow_id, hostname: 'n8n', service: 'n8n-workflow', message: $json.message, status: 'error', workflow_id: $json.workflow_id, workflow_name: $json.workflow_name, execution_id: $json.execution_id, last_node: $json.last_node, execution_url: $json.execution_url }]) }}"
  },
  "credentials": {
    "httpHeaderAuth": {
      "id": "{{@env:credentials.datadog.id}}",
      "name": "{{@env:credentials.datadog.name}}"
    }
  }
}
```

Note: `ddtags` is a single comma-separated string, NOT an array (logs API quirk). The body is an array of log entries (single-element array for one entry).

## See also

- [`patterns/error-handling.md`](../../patterns/error-handling.md) — three-step paradigm + worked handler example.
- [`manage-credentials.md`](../../manage-credentials.md) — registering the DD-API-KEY credential.
