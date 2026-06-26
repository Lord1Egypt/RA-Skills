---
name: pattern-queues
description: Producer-consumer queueing semantics — when to choose over locks/rate-limit, sizing guidance, retry/DLQ trade-offs.
user-invocable: false
---

# Queues (producer-consumer pattern)

The harness ships a Redis-Streams-backed queue primitive: a producer XADDs to a stream, one or more consumers poll on a schedule and drain it with bounded concurrency, ack on success, and optionally route poison messages to a DLQ.

## When to use this vs. a lock

| Pattern | Use when | Don't use when |
|---|---|---|
| **Lock** (`add-lock-to-workflow`) | One thing at a time on a shared resource. Latency-bounded by typical work + max-wait. Coordination, not buffering. | The contended workers are doing different work (use queue with one consumer). |
| **Rate-limit** (`add-rate-limit-to-workflow`) | Cap requests-per-window against an external API quota. Drop / fail-fast on excess. | You can't drop — work must eventually be done (use queue). |
| **Queue** (this pattern) | Work needs to be durable, retried on failure, drained by N parallel workers, with DLQ for poison messages. Producer ≠ consumer (or producer wants async confirmation only). | Sub-second end-to-end latency required (schedule polling adds 1s–30s). Cross-region — Upstash Streams aren't replicated synchronously. |

## Producer / consumer semantics

| | Producer (`queue_publish`) | Consumer (`queue_pop` + `queue_ack`) |
|---|---|---|
| Trigger | Caller's existing workflow (after-trigger insertion) | Schedule (default 30s) |
| Idempotent on retry | **No** — each XADD makes a fresh XID | Yes — XAUTOCLAIM/XREADGROUP at-least-once + permit-based acquire |
| Output discriminator | `{message_id, published:true}` or thrown error | `{empty}` / `{at_capacity}` / `{dlq_routed}` / `{message_id, payload, ...}` |
| Backpressure | None — XADD always succeeds (stream uncapped unless `--max-len`) | `q:<stream>:inflight ≤ max_concurrency` semaphore; over-cap rolls back via DECR |

## Read-vs-claim: XAUTOCLAIM-then-XREADGROUP

The Pop primitive runs XAUTOCLAIM **before** XREADGROUP each iteration:

1. **XAUTOCLAIM** — moves messages from any stuck consumer's PEL (Pending Entries List) to ours, but only if they've been idle ≥ `--claim-idle-ms`. This is the "stuck consumer recovery" mechanism. Without it, a crashed consumer's PEL'd messages would be stranded forever.
2. If a message was claimed → process it (it's a redelivery, increment `delivery_count`).
3. **XREADGROUP** — fall through to fresh delivery if no claim happened.

**Why this order, not the reverse**: claiming first prevents starvation of stuck-consumer messages. If we read fresh first, busy consumers would always pick fresh messages and the PEL'd ones would never get retried.

## Permit sidecar — why a separate Redis key

Each successful Pop writes a JSON sidecar at `q:<stream>:permits:<message_id>` containing `{message_id, execution_id, sub_execution_id, workflow_id, workflow_name, stream, group, claimed_at}`, with `EX 86400`. `execution_id` is the **caller's** (consumer workflow's) execution id, passed in via the `caller_execution_id` input on queue_pop — NOT the queue_pop sub-workflow's own `$execution.id`. This matters for error-handler ownership matching: errorTrigger fires with the caller's failed-execution id, so the sidecar must record that one for the filter to match. `sub_execution_id` records the queue_pop sub-workflow's id for diagnostic purposes only. The sidecar is the bridge between "this consumer holds capacity" (`q:<stream>:inflight` integer counter) and "which message did this execution claim" (the sidecar JSON).

Three keys-of-truth:
- `q:<stream>:inflight` — integer count of active consumers. **No TTL** (it's operational state; a TTL that fired mid-flight would let new consumers exceed `max_concurrency`).
- `q:<stream>:permits:<id>` — JSON identity sidecar. **EX 86400** (24h disaster backstop). Normal lifecycle DELs in seconds.
- The Stream itself — Redis-managed; messages stay in the PEL until XACK.

Invariant: `inflight == count(permit sidecars for the stream)`. Maintained by the {INCR, DECR} pair across `queue_pop` + `queue_ack` + `error_handler_queue_cleanup`.

The sidecar lets the error handler know which permits to release on a failed execution: it iterates `<env>.yml.queueScopes`, KEYS the permits glob, GETs each, and only DECR/DEL when `parsed.execution_id == failed_execution_id`. This avoids cleaning up permits held by other in-flight runs.

## Retry / DLQ semantics

The consumer wrap inserts a `Queue Ack` at the terminal of your main flow. Its `success` argument decides what happens to the message:

- `success: true` → XACK (remove from PEL) + DECR inflight + DEL permit. Done.
- `success: false` → **No XACK** + DECR inflight + DEL permit. Message stays in the PEL; XAUTOCLAIM will redeliver it after `claim_idle_ms`.

Override via `--ack-on-success-expression`. Common patterns:

```
# "Don't ack on transient API errors — let the next consumer retry."
--ack-on-success-expression "={{ \$json.transient_failure !== true }}"

# "Always ack — never retry. Trust the caller to have caught all errors."
--ack-on-success-expression "={{ true }}"

# "Conditional based on response code from an HTTP call earlier."
--ack-on-success-expression "={{ \$json.status === 200 || \$json.status === 422 }}"
```

When `--dlq-enabled` is set and `delivery_count > max_retries`, the next Pop iteration routes the message to `<stream>-dlq` instead of delivering it to your main flow. This protects against poison pills that would otherwise loop forever in the PEL. `delivery_count` is read from Redis via `XPENDING ... IDLE 0 <id> <id> 1` — authoritative, not inferred — so `max_retries=N` means "retry up to N times, route to DLQ on the (N+1)th delivery."

## Race losers and inflight semantics

INCR returns the post-increment count. With `max_concurrency=1`, two consumers racing INCR will see counts 1 and 2:
- 1 → proceeds, processes the message.
- 2 → trips the over-cap gate, runs DECR rollback, exits with `at_capacity:true`.

The race loser's poll iteration is wasted, but no message is lost — the message stays in the PEL because the loser never wrote a permit (so the next iteration via XAUTOCLAIM will pick it back up).

## Boundary cases

- **Stream doesn't exist yet** → first Pop's XGROUP CREATE with `MKSTREAM` creates an empty stream + group. Subsequent XGROUP CREATE attempts return BUSYGROUP, swallowed via `options.response.response.neverError = true` on the HTTP node.
- **All workers crash mid-flight** → permits' 24h EX backstop expires; `q:<stream>:inflight` is at +N from the crash. The error handler (if wired) cleans up the matching execution's permits, but DOES NOT touch other-execution permits. After 24h, EXPIRE'd permits leave the inflight counter inflated. Operators should monitor `q:<stream>:inflight` with an alert on "stuck > N for > Xh".
- **Producer retries** → produces duplicate XIDs. Consumers must tolerate duplicates (idempotent processing) or dedupe at the application layer. The primitive does not enforce exactly-once.

## When NOT to use this primitive

- **Cross-region** — Upstash Streams aren't synchronously replicated. Build a different transport (Kinesis, NATS JetStream).
- **Sub-second end-to-end latency** — schedule polling minimum is 1s; default is 30s. For tighter latency, run a long-lived process outside n8n.
- **FIFO + priority** — Streams are FIFO within the stream but have no priority levels. Multiple streams + a priority-aware dispatcher would be needed.
- **Fairness across producers** — there's no per-producer quota. A noisy producer can flood the stream and starve out others.

## See also

- [`skills/integrations/redis/queue-pattern.md`](../integrations/redis/queue-pattern.md) — node-graph diagrams + `q:*` key namespace.
- [`skills/patterns/locking.md`](locking.md) — coordination pattern for "one at a time" semantics.
- [`skills/create-queue.md`](../create-queue.md) — workspace install.
- [`skills/add-queue-publish-to-workflow.md`](../add-queue-publish-to-workflow.md) — producer wrap.
- [`skills/add-queue-consumer-to-workflow.md`](../add-queue-consumer-to-workflow.md) — consumer wrap.
