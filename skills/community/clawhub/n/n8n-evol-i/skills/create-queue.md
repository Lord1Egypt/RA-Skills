---
name: create-queue
description: First-time setup for the producer-consumer queue primitive (Redis Streams + atomic-INCR semaphore). Copies queue_publish + queue_pop + queue_ack into the workspace and registers them.
user-invocable: false
---

# create-queue

## When

When locking is too coarse: the work shouldn't serialise — it should be queued, drained by N concurrent consumers, retried on failure, and optionally routed to a dead-letter stream after `max_retries`.

Use `create-lock` for **coordination** (one-at-a-time access to a shared resource). Use `create-queue` for **buffer-and-cap semantics** (durable backlog + bounded concurrency + retry/DLQ).

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/create_queue.py \
  [--include-error-handler] \
  [--with-sample-test] \
  [--force-overwrite]
```

## Side effects

- Copies these primitives from `${CLAUDE_PLUGIN_ROOT}/primitives/workflows/` into `<workspace>/n8n-workflows-template/`:
  - `queue_publish.template.json` (always)
  - `queue_pop.template.json` (always)
  - `queue_ack.template.json` (always)
  - `error_handler_queue_cleanup.template.json` (with `--include-error-handler`)
- Registers each in every configured env's YAML (delegates to `create_workflow.py --no-template`). This mints placeholder workflow IDs that callers reference via `{{@env:workflows.queue_publish.id}}` etc.
- Adds them to `deployment_order.yml` under "Tier 0a: leaves" so they deploy before any caller workflow that depends on them.

## What you're actually deploying

Three sub-workflows + an optional error-handler. All Redis Streams operations route through the **HTTP Request node against Upstash REST** — `n8n-nodes-base.redis@1` exposes no Streams ops, so XADD / XREADGROUP / XACK / XAUTOCLAIM all run as command-array POSTs to `UPSTASH_REDIS_REST_URL`.

- `queue_publish` (4 nodes) — XADDs a message to the stream, optional `MAXLEN ~ <n>` trimming, returns `{message_id, stream, published:true}`.
- `queue_pop` (23 nodes) — XAUTOCLAIM-then-XREADGROUP, DLQ check (when enabled), atomic `q:<stream>:inflight` semaphore (INCR + over-cap rollback), per-message permit sidecar at `q:<stream>:permits:<id>`. Returns one of `{empty:true}`, `{at_capacity:true}`, `{dlq_routed:true}`, or the message with `permit_held:true`.
- `queue_ack` (12 nodes) — releases a permit. On `success:true`, XACKs off the main stream + DECR inflight + DEL permit. On `success:false`, leaves the message in the PEL (XAUTOCLAIM redelivers after `claim_idle_ms`) but still DECR inflight + DEL permit so a fresh consumer can grab it. Idempotent on absent permit.
- `error_handler_queue_cleanup` (11 nodes) — iterates `<env>.yml.queueScopes`, KEYS `q:<stream>:permits:*`, GETs each sidecar, DECRs inflight + DELs permit only when `sidecar.execution_id` matches the failed run.

For node-graph diagrams + the `q:*` key namespace, see [`skills/integrations/redis/queue-pattern.md`](integrations/redis/queue-pattern.md). For semantics + when to use over locks, see [`skills/patterns/queues.md`](patterns/queues.md).

## Prerequisites

The queue primitives need **two** things provisioned in n8n before deploy:

### 1. Credential — `credentials.redis_rest`

An `httpHeaderAuth`-typed credential carrying `Authorization: Bearer <UPSTASH_REDIS_REST_TOKEN>`, registered in every env YAML. The existing `credentials.redis` (TCP redis@1) is left untouched and continues to back the lock + rate-limit primitives.

Mint it via [`manage-credentials.md`](manage-credentials.md) Path A, sourcing the token from `.env.<env>` (`UPSTASH_REDIS_REST_TOKEN`).

### 2. Runtime URL — `UPSTASH_REDIS_REST_URL`

Every queue primitive's HTTP Request URL field references **`={{ $env.UPSTASH_REDIS_REST_URL }}`**. On self-hosted instances with env access enabled, set the env var on the n8n process and you're done.

**If your deployment blocks `$env`** (n8n Cloud's default sandbox mode, or self-hosted with `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`), you'll see `ExpressionError: access to env vars denied` at the first HTTP node. See [`manage-variables.md`](manage-variables.md) for the resolution paths (self-host with env enabled, or replace `$env.*` with `$vars.*` per-deployment and mint the variable). The shipped primitives stay `$env`-first; per-deployment overrides live in your workspace, not in the harness.

## `queueScopes` env config

For active error-handler cleanup to work, every static stream name used by your consumers must be registered in `<env>.yml.queueScopes`. `add-queue-publish-to-workflow` and `add-queue-consumer-to-workflow` auto-append static literal streams (`={{ "foo" }}`-form) here on each invocation; dynamic streams (`={{ "stream-" + $json.x }}`) require manual maintenance.

```yaml
# n8n-config/dev.yml
queueScopes:
  - orders
  - notifications
  - test-stream
```

## Flag details

- **`--include-error-handler`** — also copy `error_handler_queue_cleanup`. Required if you'll add `--cleanup-on-error` to any consumer via `add-queue-consumer-to-workflow`.
- **`--with-sample-test`** — also copy a paired producer + consumer that exercise the full primitive (happy path, transient-retry path, poison → DLQ path) against a stream named `test-stream`. The producer is a webhook (`POST /webhook/queue-sample-producer`) that publishes 5 tagged messages; the consumer is schedule-polled (every 10s) and acks based on per-tag simulation logic. Registers both at `Tier 1` (callers) so `deploy_all.py` rolls them out after the primitives. Use this for first-time end-to-end validation, then archive when no longer needed.
- **`--force-overwrite`** — overwrite existing workspace copies of the primitives instead of skipping them.

## Next steps

- [`add-queue-publish-to-workflow.md`](add-queue-publish-to-workflow.md) — wrap a workflow with a producer-side XADD call.
- [`add-queue-consumer-to-workflow.md`](add-queue-consumer-to-workflow.md) — turn a workflow into a polling queue consumer.
