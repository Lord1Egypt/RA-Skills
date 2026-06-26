---
name: integration-redis-queue
description: Redis Streams + atomic-INCR semaphore implementation reference — node graphs, `q:*` key namespace, why HTTP Request + Upstash REST instead of redis@1.
user-invocable: false
---

# Redis Streams (queue pattern)

The harness ships four queue primitives backed by **HTTP Request against the Upstash Redis REST API**, NOT the dedicated `n8n-nodes-base.redis@1` node. Redis@1 exposes `delete | get | incr | info | keys | llen | pop | push | publish | set` only — no XADD / XREADGROUP / XACK / XAUTOCLAIM / XPENDING. Streams ops require a different transport.

## Credential

`redis_rest` credential type — `httpHeaderAuth` with header `Authorization: Bearer <UPSTASH_REDIS_REST_TOKEN>`. Mint via [`manage-credentials.md`](../../manage-credentials.md) Path A from `.env.<env>`'s `UPSTASH_REDIS_REST_TOKEN`. The four queue primitives reference it via `{{@env:credentials.redis_rest.{id,name}}}` placeholders.

The existing `credentials.redis` (TCP redis@1) is left untouched — the lock + rate-limit primitives keep using it.

## Shipped primitives

| Primitive | Trigger | Output |
|---|---|---|
| `queue_publish` | `executeWorkflowTrigger` (passthrough; expects `{stream, payload, max_len?, approximate?}` in `$json`) | `{stream, message_id, published:true}` or thrown error |
| `queue_pop` | `executeWorkflowTrigger` (inputs: `stream, group, consumer, max_concurrency, max_retries, dlq_enabled, batch_size, claim_idle_ms`) | `{empty:true}` / `{at_capacity:true}` / `{dlq_routed:true}` / `{message_id, payload, ..., permit_held:true}` |
| `queue_ack` | `executeWorkflowTrigger` (inputs: `stream, group, message_id, success`) | `{acked:true, idempotent:bool, xacked:bool, success:bool, inflight_count_after}` |
| `error_handler_queue_cleanup` | `errorTrigger` | `{cleaned:bool, cleaned_count, streams:[]}` |

Every Code-node body inside these primitives starts with `// @n8n-evol-I:primitive` to bypass `validate.py`'s pure-function discipline. **Do not copy that marker into user Code nodes** — it silently disables validation.

## `q:*` key namespace

| Key | Shape | Set by | Cleared by | TTL |
|---|---|---|---|---|
| `q:<stream>:inflight` | integer counter | `queue_pop` INCR Inflight | `queue_ack` DECR Inflight (on success), `queue_pop` DECR Rollback (on over-capacity), `error_handler_queue_cleanup` DECR Inflight (on failed-exec match) | **none** — operational state, must equal permit count |
| `q:<stream>:permits:<message_id>` | JSON sidecar `{message_id, execution_id, sub_execution_id, workflow_id, workflow_name, stream, group, claimed_at}`. `execution_id` is the **caller** (consumer) execution; `sub_execution_id` is the queue_pop sub-workflow execution (diagnostic only). | `queue_pop` SET Permit Sidecar (with `EX 86400`) | `queue_ack` DEL Permit Sidecar, `error_handler_queue_cleanup` DEL Owned Permit | **EX 86400** (24h backstop) |
| `<stream>` (the Stream itself) | Redis Stream | `queue_publish` XADD | `queue_ack` XACK + retention via XADD MAXLEN | controlled by `--max-len` |
| `<stream>-dlq` | Redis Stream | `queue_pop` XADD to DLQ (when enabled + delivery_count > max_retries) | manual operator action (XRANGE / XDEL) | none — DLQ is forensic |

`q:*` colon-separated namespace deliberately distinct from the lock primitive's `n8n-lock-*` and rate-limit's `n8n-ratelimit-*` (hyphen-separated). KEYS scans of either prefix never overlap.

## Why HTTP Request + Upstash REST (not redis@1)

`n8n-nodes-base.redis@1` predates Redis 5+ Streams (XADD et al). Verified via `mcp__n8n-mcp__search_nodes`: the operation discriminator enum is `delete | get | incr | info | keys | llen | pop | push | publish | set`. None of XADD / XACK / XREADGROUP / XAUTOCLAIM / XPENDING.

Upstash REST is the cleanest fit: `POST <UPSTASH_REDIS_REST_URL>/` with a JSON command-array body and `Authorization: Bearer <token>`. The response shape is `{result: <result>}` on success or `{error: <msg>}` on failure. Uniform across all command types.

We deliberately route the **semaphore** ops (INCR / DECR / GET / SET / DEL) through the same REST endpoint instead of mixing TCP redis@1 + HTTP. Mixing two access paths would (a) require two distinct credentials per env, (b) split atomicity reasoning across two transports, (c) risk cross-transport consistency drift if the credentials ever pointed at different instances. Single transport, single credential, single mental model.

## `queue_publish` node graph (4 nodes)

```
Execute Workflow Trigger (passthrough)
       │
       ▼
Build Publish Context (Code: validates stream, JSON.stringifies payload,
                       constructs ['XADD', stream, [MAXLEN ~ <n>]?, '*',
                                   'payload', payload, 'enqueued_at', ISO])
       │
       ▼
XADD Message (HTTP POST to Upstash REST with the cmd-array body)
       │
       ▼
Build Publish Output (Code: returns {stream, message_id: $json.result,
                       published: true}; throws on $json.error)
```

## `queue_pop` node graph (23 nodes)

Reading top-to-bottom-then-by-branch:

```
Execute Workflow Trigger (workflowInputs: stream, group, consumer, max_concurrency,
                          max_retries, dlq_enabled, batch_size, claim_idle_ms)
       │
       ▼
Build Pop Context (Code: defaults group=<stream>-cg, consumer=<stream>-c-<execId>,
                   inflight_key=q:<stream>:inflight, dlq_stream=<stream>-dlq,
                   captures workflow id/name/exec id for the permit sidecar)
       │
       ▼
XGROUP CREATE (idempotent; start-id=0 so cold-start groups drain backlog
               instead of silently skipping pre-existing messages;
               MKSTREAM; neverError=true to swallow BUSYGROUP)
       │
       ▼
XAUTOCLAIM Stale (claim PEL'd messages idle ≥ claim_idle_ms; COUNT=batch_size)
       │
       ▼
Parse Claim Result (Code: extract first message from raw[1][0] if any)
       │
       ▼
Has Claimed?
   ├── true  → Merge Message ◄──────────────────────────────┐
   └── false → XREADGROUP Fresh (>; COUNT=batch_size) → Parse Read Result ─┘
                                                                 │
       ┌─────────────────────────────────────────────────────────┘
       ▼
Merge Message (Code: decode flat [k,v,...] fields → {payload, enqueued_at};
               delivery_count is set later from XPENDING)
       │
       ▼
Has Message?
   ├── false → Empty Output (terminate: {empty:true})
   └── true  → XPENDING Lookup (HTTP: XPENDING <stream> <group> IDLE 0 <id> <id> 1
                                returns [[id, consumer, idle_ms, delivery_count]])
                       │
                       ▼
                 Check DLQ Threshold (Code: parses delivery_count from XPENDING result;
                                      should_dlq = dlq_enabled && delivery_count > max_retries)
                       │
                       ▼
                 Should DLQ?
                   ├── true  → XADD to DLQ (HTTP) → XACK Off Main (HTTP) → DLQ-Routed Output
                   └── false → INCR Inflight (HTTP)
                                       │
                                       ▼
                                 Capacity Gate (Code: over_capacity = post-INCR count > max_concurrency)
                                       │
                                       ▼
                                 Over Capacity?
                                   ├── true  → DECR Rollback (HTTP) → At-Capacity Output
                                   └── false → SET Permit Sidecar (HTTP, EX 86400) → Build Success Output
```

**`delivery_count` source.** Read from Redis directly via `XPENDING <stream> <group> IDLE 0 <id> <id> 1` — Redis tracks the count per PEL entry, so we read the authoritative value rather than infer it. The detailed-form response is `[[id, consumer, idle_ms, delivery_count]]`; we parse `[0][3]`. The XPENDING node fires only when `Has Message? === true`, so the cost is one extra HTTP round-trip per delivered message — paid only when there's actual work to gate on. If XPENDING returns `[]` (rare race: message XACK'd between Merge and the lookup), we default to `delivery_count = 1`.

## `queue_ack` node graph (12 nodes)

```
Execute Workflow Trigger (inputs: stream, group, message_id, success)
       │
       ▼
Build Ack Context (Code: inflight_key, permit_key, validates inputs)
       │
       ▼
GET Permit Sidecar (HTTP)
       │
       ▼
Verify Permit (Code: permit_exists = result !== null)
       │
       ▼
Permit Exists?
   ├── false → Idempotent Output ({acked:true, idempotent:true, reason:'permit absent'})
   └── true  → Should XACK?
                  ├── true (success=true)  → XACK Main (HTTP) ──┐
                  └── false (success=false) → Skip XACK Marker ─┤
                                                                ▼
                                                         DECR Inflight (HTTP)
                                                                │
                                                                ▼
                                                         DEL Permit Sidecar (HTTP)
                                                                │
                                                                ▼
                                                         Build Ack Output
                                                         ({acked:true, xacked, success,
                                                           inflight_count_after})
```

The `success: false` path leaves the message in the PEL — XAUTOCLAIM will redeliver after `claim_idle_ms`. This is the "soft NACK" path. The hard XACK case (`success: true`) removes the message from the stream.

## `error_handler_queue_cleanup` node graph (11 nodes)

```
Error Trigger
       │
       ▼
Prepare Stream List (Code: read <env>.yml.queueScopes via {{@env:queueScopes}};
                     fan out one item per registered stream with permits_glob,
                     inflight_key, failed_execution_id)
       │
       ▼
Has Streams?
   ├── false → Log Cleanup (no-op: {cleaned:false, reason:'no queueScopes'})
   └── true  → KEYS Permits (HTTP, q:<stream>:permits:*)
                       │
                       ▼
                 Fan Out Permit Keys (Code: flatten KEYS results, propagate stream context)
                       │
                       ▼
                 GET Permit Body (HTTP, per permit key)
                       │
                       ▼
                 Filter Owned Permits (Code: parse JSON; keep entries where
                                       parsed.execution_id === failed_execution_id)
                       │
                       ▼
                 Owned?
                   ├── true  → DECR Inflight (HTTP) → DEL Owned Permit (HTTP) → Log Cleanup
                   └── false → Log Cleanup (no-op)
```

The handler does **not** XACK. The failed run's work was incomplete; we leave the message in the PEL and let the next XAUTOCLAIM cycle redeliver it (subject to `claim_idle_ms`). This is the more conservative choice — XACK'ing here would silently lose work.

`KEYS` is used (not SCAN) because permits-per-failed-exec is small. For larger fan-outs, swap KEYS → SCAN.

## TTL discipline

- `q:<stream>:inflight` — **no TTL.** The counter must match the count of held permits at all times. A TTL that fired mid-flight would let new consumers exceed `max_concurrency`. Maintained by the {INCR, DECR} pair across `queue_pop` (acquire + over-cap rollback), `queue_ack` (ack), and `error_handler_queue_cleanup` (failed-run release).
- `q:<stream>:permits:<id>` — **EX 86400 (24h).** Defensive backstop only. Normal lifecycle DELs in seconds. 24h is long enough that no normal slow consumer ever expires; short enough to cap permanent leak from a totally broken cluster (no acks, no error handler firing).

## See also

- [`skills/patterns/queues.md`](../../patterns/queues.md) — semantic reference + when to use over locks/rate-limit.
- [`skills/integrations/redis/lock-pattern.md`](lock-pattern.md) — sibling lock primitive (TCP redis@1 + INCR pattern).
- [`skills/manage-credentials.md`](../../manage-credentials.md) — minting the `redis_rest` httpHeaderAuth credential from `.env.<env>`.
- [`skills/create-queue.md`](../../create-queue.md) — workspace install.
