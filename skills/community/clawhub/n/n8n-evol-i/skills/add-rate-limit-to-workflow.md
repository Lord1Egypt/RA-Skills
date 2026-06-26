---
name: add-rate-limit-to-workflow
description: Insert a Redis-backed fixed-window rate-limit gate at the head of a workflow's main flow.
user-invocable: false
---

# add-rate-limit-to-workflow

## When

A workflow needs to throttle requests per scope (per user, per tenant, per route) so that bursts above a chosen `limit` per `windowSeconds` are denied (or stopped, or surfaced as errors).

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_rate_limit_to_workflow.py \
  --workflow-key <wf> \
  --limit <int> \
  --window-seconds <int> \
  [--scope-expression "={{ 'api-' + $json.userId }}"] \
  [--on-denied {passthrough|stop|error}]   # default: passthrough
```

## Side effects

Edits `<workspace>/n8n-workflows-template/<wf>.template.json`:

- Inserts an `Execute Workflow` node calling `rate_limit_check` right after the trigger.
- Inserts an `If` node testing `={{ $json.allowed === true }}`.
- Wires the **allowed** branch (`main[0]`) to whatever the trigger originally connected to.
- Wires the **denied** branch (`main[1]`) per `--on-denied`:
  - `passthrough` (default) → a `Set` node returning `{ allowed: false, scope, count, limit }`. Workflow exits cleanly with that payload. **HTTP-level signal:** if the workflow has a `respondToWebhook` node downstream of the gate, the caller receives a 200 with that JSON body. Without one, the caller sees an empty 200.
  - `stop` → a `stopAndError` node. Workflow halts with an error message including scope/count/limit. **HTTP-level signal:** webhook callers see HTTP 500 with `{"message":"Error in workflow"}`. The denial is observable at the HTTP layer.
  - `error` → same `stopAndError` node, paired with `register-workflow-to-error-handler.md` so an error workflow picks up the failure. **HTTP-level signal:** same as `stop` (HTTP 500). Caller-side observability is identical; the difference is server-side routing of the error to a handler.

> **Caller observability note:** with `passthrough`, distinguishing a rate-limit denial from a normal success requires inspecting the response body (`allowed === false`). With `stop`/`error`, distinguish denial from any other workflow error by inspecting `/api/v1/executions` — both produce HTTP 500 with the same error envelope.
- Recalculates downstream node positions (660 px right shift to make room for the rate-limit + If nodes).

Refuses if `rate_limit_check.template.json` isn't yet in the workspace — run `create-lock --include-rate-limit` first.

## Redis namespace

The rate-limit primitive writes its counter under the `n8n-ratelimit-<scope>-<bucket>` Redis key. The bucket is `Math.floor(Date.now() / (windowSeconds * 1000))` so it auto-rolls every window.

## Worked example

You have an API-fronting workflow keyed `api_v1_handler` and want to cap any single user at 100 requests per minute, returning a passthrough payload to the caller when they exceed:

```bash
# 1. one-time: ship the rate-limit primitive into the workspace
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/create_lock.py --include-rate-limit

# 2. wire the gate
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_rate_limit_to_workflow.py \
  --workflow-key api_v1_handler \
  --scope-expression "={{ 'api-v1-' + \$json.userId }}" \
  --limit 100 \
  --window-seconds 60 \
  --on-denied passthrough
```

Result on the wire:

- `Webhook` → `Rate Limit` → `Rate Limit Allowed?` (If)
- If `allowed === true` → original downstream nodes (your handler logic).
- Else → `Rate Limit Denied` (Set) outputs `{ allowed: false, scope: "api-v1-<userId>", count: <count>, limit: 100 }` and the workflow returns that payload to the caller.

The bucket key is `n8n-ratelimit-api-v1-<userId>-<bucket>` where `<bucket>` rotates every 60 s. EXPIRE only fires on the first INCR per bucket so within-window calls don't reset TTL.

## Caveats

- **Fixed-window boundary burst.** A user can hit `limit=100` near the end of one window and `limit=100` again at the start of the next — up to `2 × limit` across the boundary. Token-bucket is deferred. If you need strict ceiling-per-rolling-window, you'll need an external solution.
- **Per-scope keys.** Choose `--scope-expression` carefully: a scope of `={{ 'global' }}` rate-limits all callers together; `={{ 'api-v1-' + $json.userId }}` rate-limits per user. Bad scopes either over- or under-throttle. Always use the canonical `={{ ... }}` form — bare `=<expr>` is auto-wrapped with a deprecation warning (the helper saves you from the literal-string trap, but write the canonical form anyway).
- **Redis required.** The rate-limit primitive uses `this.helpers.redis.call('INCR', ...)`. The Redis credential must be reachable from your n8n instance.

## Pattern

See `skills/patterns/locking.md` for the full picture of the three coordination primitives (fail-fast lock, wait-on-lock, rate-limit) and `skills/integrations/redis/lock-pattern.md` for the underlying Redis recipes.
