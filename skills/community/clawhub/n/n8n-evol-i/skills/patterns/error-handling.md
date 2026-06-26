---
name: pattern-error-handling
description: Three-step paradigm for n8n error handling — capture (Error Trigger), log (Sentry/Datadog/Slack), process (locks, DB invalidation, compensating workflows).
user-invocable: false
---

# Pattern: error handling

A workflow error in n8n isn't just "something went wrong" — it's an event that needs to flow through three steps:

1. **Capture** — n8n catches the error and routes it to a dedicated error-handler workflow.
2. **Log** — the handler ships the error to your audit/observability platform (Sentry, Datadog, Slack, …).
3. **Process** — the handler does *something about it*: release stale locks, invalidate pending DB rows, notify the originating user, trigger a compensating workflow.

Skipping any step leaves you blind, deafened, or with a corrupt state. The harness wires step 1 for you (`register_error_handler.py`); steps 2 and 3 are your error-handler's body. This doc covers the paradigm; the integration skills give you the concrete API surfaces.

## Step 1: Capture

n8n supports per-workflow error handlers via `settings.errorWorkflow`. When the source workflow errors, n8n routes the failed-execution data to the handler workflow (which uses `n8n-nodes-base.errorTrigger` as its entry).

Use `register-workflow-to-error-handler.md`:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/register_error_handler.py --workflow-key <wf> --handler-key <handler>
```

This sets `settings.errorWorkflow = "{{@env:workflows.<handler>.id}}"` (literal placeholder, no `=` prefix — n8n expects a literal id).

It also writes to `<workspace>/n8n-config/common.yml.error_source_to_handler[<wf>] = <handler>` so `run.py` knows about the pairing for indirect dispatch.

The error data arrives at the handler's Error Trigger as `$json.errorData` with this shape:

```js
{
  execution: { id, url, retryOf },
  workflow: { id, name },
  trigger: { ... },         // node that originally fired
  lastNodeExecuted: "<name>",
  source: { ... },          // the failing node's metadata
  // n8n version-dependent fields...
}
```

The exact shape varies between n8n versions. Add a Set node downstream during testing to inspect `$workflow.errorData` and confirm field paths before relying on them in production.

### Indirect dispatch (testing handlers)

Error Trigger workflows have no Webhook entry — you can't fire them directly. To run / verify a handler, fire the **paired source** workflow (which is supposed to error and route to the handler). `run.py` does this automatically when the requested key is a known handler:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/run.py --env dev --workflow-key error_handler_lock_cleanup
# → reverse-looks-up the source key from common.yml.error_source_to_handler
# → fires that source's webhook (expecting it to error)
# → polls the handler's executions for the routed error
```

## Step 2: Log

Pick a destination based on what you need to *do* with the audit trail:

| Platform | Best for | Skill |
|---|---|---|
| **Sentry** | Stack-trace tracking, exception grouping, regression detection. Use when you want "is this error new or recurring?" answered automatically. | [`integrations/sentry/README.md`](../integrations/sentry/README.md) |
| **Datadog** | Metrics + events in one pane. Use when error rates need to feed dashboards / alerts alongside infra metrics. | [`integrations/datadog/README.md`](../integrations/datadog/README.md) |
| **Slack** | Real-time human notification. Use when on-call humans need to *see* the error within seconds, not pull it from a dashboard. | [`integrations/slack/README.md`](../integrations/slack/README.md) |

These aren't mutually exclusive — a typical handler sends to all three: Sentry (durable, searchable), Datadog (metrics), Slack (loud).

All three are HTTP-shaped (Sentry and Datadog use `n8n-nodes-base.httpRequest` since they have no dedicated n8n node; Slack uses `n8n-nodes-base.slack`). Each integration skill shows the exact node config + tag/field conventions to maximize usefulness.

### Tag conventions (apply to all log destinations)

Always include these fields/tags so cross-platform correlation works:

| Tag | Source expression | Why |
|---|---|---|
| `workflow_id` | `={{ $workflow.id }}` | Pivot from Sentry to n8n UI. |
| `workflow_name` | `={{ $workflow.name }}` | Human-readable in dashboards. |
| `execution_id` | `={{ $workflow.errorData?.execution?.id || $execution.id }}` | Direct link to the failing run. |
| `env` | `{{@env:name}}` | Filter by dev/staging/prod. |
| `last_node` | `={{ $workflow.errorData?.lastNodeExecuted }}` | Where it actually broke. |

Add business-relevant tags too (`scope`, `user_id`, `tenant_id`, ...) — they make incident triage 10× faster.

## Step 3: Process

What does "doing something about it" mean? Some recipes:

### Release stale Redis locks

If the source workflow held a lock when it errored, the lock keys (`n8n-lock-<scope>` + `n8n-lock-<scope>:meta`) sit in Redis until TTL or the next contention. The harness's `error_handler_lock_cleanup.template.json` is the shipped primitive that handles this: it iterates `<env>.yml.lockScopes`, GETs each scope's `:meta` sidecar, and DELs the lock+meta pair only when the stored `execution_id` matches the failed execution. Wire it in by passing `--lock-on-error` to `add-lock-to-workflow.md`, or by setting `settings.errorWorkflow` on your workflow to `error_handler_lock_cleanup` directly.

For scopes that are dynamic (e.g. `={{ "lock-" + $json.id }}`) and therefore not in `lockScopes`, the TTL backstop applies: the orphan lock expires after `ttl_seconds` and the next acquire starts cleanly.

See [`patterns/locking.md`](locking.md) for the safety model and [`integrations/redis/lock-pattern.md`](../integrations/redis/lock-pattern.md) for the full node graph and key namespace.

### Invalidate "pending" DB rows

A workflow that wrote a "pending" row before failing leaves orphan state. In your error handler:

1. Identify the pending row(s) — typically by execution-id or a correlation token your source workflow stored.
2. UPDATE the row to `status = 'failed'` with the failure reason copied from `$workflow.errorData.message`.
3. Use `n8n-nodes-base.postgres` (or `n8n-nodes-base.mysql`, etc.) with an UPDATE operation.

This unblocks UI listings ("show me my failed jobs"), avoids stuck-pending bugs, and gives you a queryable failure history.

### Notify the originating user

If the source workflow was triggered by a webhook on behalf of a user, write the failure to whatever user-visible status surface you have: a "jobs" table in your app DB, an `In-App Notification` row, an outbound email via `n8n-nodes-base.gmail`, etc.

### Trigger a compensating workflow

Some failures need an active rollback (e.g., a partial Stripe charge needs a `refund`). Use `n8n-nodes-base.executeWorkflow` to fire your compensation sub-workflow, passing the original payload + the failure reason.

This is where the harness's "leaves first" deployment-tier convention pays off: compensating workflows are leaves (they don't compose), so they deploy independently of the source workflow.

## Worked example: full error handler

A handler that does all three log destinations + lock release. Node graph:

```
Error Trigger
   │
   ▼
Build Context (Code: extract execution_id, workflow_id, last_node, message)
   │
   ▼
   ├──► Slack: Post (alerts channel — :rotating_light: + execution URL)
   │
   ├──► HTTP Request: Sentry envelope POST
   │
   ├──► HTTP Request: Datadog event POST
   │
   └──► (Optional) Process step — Execute Workflow → error_handler_lock_cleanup
                                  OR Postgres UPDATE → mark row failed
```

Each "log" branch runs in parallel from the Build Context node (n8n auto-parallelizes when one node has multiple `main[0]` outputs). The "process" step runs in parallel too — the error has been captured + logged before any state cleanup runs, so even if cleanup fails, the audit trail is durable.

### Build Context Code-node body

```javascript
// @n8n-evol-I:primitive — exempt from pure-function discipline
const ed = $workflow.errorData || {};
const execution = ed.execution || {};
const workflow = ed.workflow || {};
return [{
  json: {
    execution_id: execution.id || $execution.id,
    execution_url: execution.url || null,
    workflow_id: workflow.id || $workflow.id,
    workflow_name: workflow.name || $workflow.name,
    last_node: ed.lastNodeExecuted || null,
    message: ed.message || (ed.error && ed.error.message) || 'unknown error',
    timestamp: new Date().toISOString(),
  },
}];
```

The `// @n8n-evol-I:primitive` marker is appropriate here — this is harness-pattern code, not user business logic. (If you're building this handler inside a user workspace and not as a shipped primitive, omit the marker and follow the standard Code-node discipline: extract to `n8n-functions/js/buildErrorContext.js` with a paired test.)

### Why parallel branches

A sequential `Slack → Sentry → Datadog → Cleanup` chain breaks on the first node that fails. Parallel branches mean Sentry can fail without preventing the Datadog event or the lock cleanup. This is *intentional*: error handlers must be maximally tolerant of their own failures.

If you absolutely need a strict order (e.g., "Sentry must record before Slack notifies the user"), chain those two specifically and leave the rest parallel.

## Why no shipped error-handler primitive?

Users mix log destinations differently — some only Slack, some all three, some Discord/PagerDuty/custom. A shipped `error_handler_default.template.json` would lock in opinions about audit-platform choice and message format. The pattern doc + the three integration skills give you everything to compose your own.

The shipped `error_handler_lock_cleanup.template.json` (active per-scope cleanup over `lockScopes`) is a *building block* for the "process" step, not the whole error handler — your handler should compose it (or your own variant) alongside log/notify branches.

## Cross-references

- [`integrations/sentry/README.md`](../integrations/sentry/README.md) — Sentry envelope POST + tagging.
- [`integrations/datadog/README.md`](../integrations/datadog/README.md) — Datadog events POST + region selection.
- [`integrations/slack/README.md`](../integrations/slack/README.md) — Slack error notification with Block Kit + thread_ts.
- [`patterns/locking.md`](locking.md) — lock cleanup as a "process" step.
- [`integrations/redis/lock-pattern.md`](../integrations/redis/lock-pattern.md) — active-cleanup upgrade path.
- [`register-workflow-to-error-handler.md`](../register-workflow-to-error-handler.md) — the helper that wires step 1.
