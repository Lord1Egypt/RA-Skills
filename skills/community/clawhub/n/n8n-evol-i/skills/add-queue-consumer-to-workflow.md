---
name: add-queue-consumer-to-workflow
description: Turn a workflow into a polling queue consumer — schedule trigger → Queue Pop → If has-message → main flow → Queue Ack.
user-invocable: false
---

# add-queue-consumer-to-workflow

## When

You have a producer (`add-queue-publish-to-workflow`) feeding a stream, and you need a consumer to drain it with bounded concurrency + ack-on-success + optional DLQ.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_queue_consumer_to_workflow.py \
  --workflow-key <wf> \
  --stream-expression "={{ 'orders' }}" \
  [--group-expression "={{ 'orders-cg' }}"] \
  [--consumer-expression "={{ 'orders-c-' + \$execution.id }}"] \
  [--max-concurrency 1] \
  [--max-retries 3] \
  [--dlq-enabled] \
  [--batch-size 1] \
  [--claim-idle-ms 60000] \
  [--schedule-interval 30s] \
  [--ack-on-success-expression "={{ true }}"] \
  [--cleanup-on-error] \
  [--remove-existing-trigger]
```

## What it does to your template

```
Schedule Trigger ──► Queue Pop ──► Has Message? ──true──► <your existing main flow> ──► Queue Ack
                                       └──false──► (terminate iteration — empty / at-capacity / dlq-routed)
```

- If the workflow already has a `scheduleTrigger`, it's reused — no duplicate trigger inserted.
- If it has a different trigger (webhook, etc.), the helper refuses unless `--remove-existing-trigger` is passed (which drops the old trigger).
- If it has no trigger at all, a `scheduleTrigger@1.3` is installed at the front configured to fire every `--schedule-interval`.
- Existing main-flow nodes are shifted right by 660 px to make room for Pop + If + Ack.

Refuses if the queue primitives aren't yet in the workspace — run [`create-queue.md`](create-queue.md) first.

## Output discriminator

`Queue Pop` returns one of four shapes; the inserted `Has Message?` If gate routes on them:

- `{ empty: true }` — the stream had no claimable + no fresh messages. Iteration ends.
- `{ at_capacity: true, inflight_count, max_concurrency }` — INCR pushed inflight over `--max-concurrency`; the over-cap consumer rolled back via DECR. Iteration ends. Message stays in the PEL; XAUTOCLAIM will redeliver it after `claim_idle_ms`.
- `{ dlq_routed: true, original_message_id, dlq_stream }` — only if `--dlq-enabled` and the message's inferred `delivery_count` exceeded `--max-retries`. Iteration ends.
- otherwise `{ message_id, payload, enqueued_at, claimed, delivery_count, permit_held: true, inflight_count }` — your main flow runs.

The terminal `Queue Ack` always pulls `stream` / `group` / `message_id` from `={{ $('Queue Pop').first().json.* }}` — it doesn't matter what intermediate nodes did to `$json`.

## Flag reference

### `--stream-expression`

Same shape as the producer-side: canonical `={{ "name" }}` for static, `={{ "prefix-" + $json.id }}` for dynamic. Static literals are auto-appended to `<env>.yml.queueScopes` so the error handler can find them.

### `--group-expression` / `--consumer-expression`

Stream consumer-group name and consumer ID. Defaults: group = `<stream>-cg` (literal stream name), consumer = `={{ $workflow.name + '-' + $execution.id }}` (per-execution unique). The XGROUP CREATE in the primitive is idempotent (`MKSTREAM` + `BUSYGROUP` ignored).

### `--max-concurrency <int>`

Default 1. The cap on `q:<stream>:inflight` — set to N for "at most N consumers concurrently processing". After INCR, if the post-increment value exceeds N, the consumer DECRs (rollback) and exits with `at_capacity:true`.

### `--max-retries <int>`

Default 3. Compared against the message's inferred `delivery_count`. When `--dlq-enabled` and `delivery_count > max_retries`, the message is XADDed to `<stream>-dlq` and XACKed off the main stream.

The current implementation infers `delivery_count` heuristically: fresh delivery (XREADGROUP) = 1; redelivered (XAUTOCLAIM) = 2. Operators who need precise counting can extend the primitive with an explicit per-message counter key (`q:<stream>:deliveries:<id>`). This is documented in the queue-pattern reference.

### `--dlq-enabled` / `--no-dlq-enabled`

Default off. When enabled, messages exceeding `max_retries` are routed to `<stream>-dlq` (a separate Redis Stream) for forensic review. DLQ reads are operator-driven (XRANGE / manual workflow); the primitive doesn't auto-drain it.

### `--batch-size <int>`

Default 1. `COUNT` argument passed to XAUTOCLAIM + XREADGROUP. The current Pop primitive returns the **first** message in the batch (further messages are claimed but ignored — they'll be redelivered next iteration). Increasing this is a tuning knob; in v1 prefer 1 unless you're profiling.

### `--claim-idle-ms <int>`

Default 60000ms (60s). Minimum age before XAUTOCLAIM steals a PEL'd message from a stuck consumer. Should be ≫ typical processing time — otherwise normal-running consumers will have messages stolen mid-flight.

### `--schedule-interval <expr>`

Default `30s`. Format: `<n><unit>` where unit is `s`/`m`/`h`/`d`/`w`. Bare integer = minutes. Encoded as `parameters.rule.interval[0] = {field, <unit>Interval: n}` on the inserted Schedule Trigger.

### `--ack-on-success-expression "<n8n-expression>"`

Default `={{ true }}` — XACK every message after the main flow completes without throwing. Use a custom expression to conditionally NACK transient failures (the message stays in the PEL for redelivery):

```
--ack-on-success-expression "={{ \$json.transient_failure !== true }}"
```

When the main flow sets `transient_failure: true` on its last item, Queue Ack receives `success:false`, leaves the message in the PEL, and DECRs inflight + DELs the permit so a fresh consumer can grab it on next claim.

### `--cleanup-on-error`

Default off. Wires `settings.errorWorkflow` to `error_handler_queue_cleanup` (delegates to `register-workflow-to-error-handler.md`). On any uncaught exception in the consumer, the handler iterates `<env>.yml.queueScopes`, GETs every permit sidecar, and DECRs inflight + DELs only the permits owned by the failed execution.

Requires `create-queue --include-error-handler` to have been run.

### `--remove-existing-trigger`

Default off. Required when the target workflow has a non-schedule trigger that should be replaced. Without this flag the helper refuses to silently drop your trigger.

## Tuning quick reference

| Goal | Knob |
|---|---|
| One-at-a-time processing across all consumers | `--max-concurrency 1` |
| Multiple parallel workers | `--max-concurrency N` (rule of thumb: 5–20 for I/O-bound, 1–4 for CPU-bound) |
| Fast retry of transient errors | `--ack-on-success-expression` returning false; relies on `--claim-idle-ms` |
| Poison-pill containment | `--dlq-enabled --max-retries 3` (redelivers 3 times then DLQs) |
| Drain-as-fast-as-possible | `--schedule-interval 30s` (the practical minimum) — for sub-30s polling, run multiple consumer workflows |

## Caveats

- **Schedule polling minimum is 1 second** (n8n schedule trigger limit). For lower latency, prefer multiple consumer workflows or a dedicated stream-tailing service.
- **`delivery_count` heuristic** as documented above. Conservative `--max-retries` recommended.
- **`--max-concurrency` race losers** lose a poll iteration. With a 30s schedule, contention bursts cost ≤30s of latency for the loser. Document in your runbook.

See [`skills/patterns/queues.md`](patterns/queues.md) for the full semantic reference and [`skills/integrations/redis/queue-pattern.md`](integrations/redis/queue-pattern.md) for the node-graph diagrams.
