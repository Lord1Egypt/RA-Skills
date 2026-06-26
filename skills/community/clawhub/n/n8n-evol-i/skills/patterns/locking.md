---
name: pattern-locking
description: Distributed coordination via Redis sub-workflows — atomic INCR lock + GET-poll wait + fixed-window rate-limit. Safety model, scope expressions, when NOT to use.
user-invocable: false
---

# Pattern: locking + rate-limit

A workflow that mutates a shared resource (a Sharepoint Excel file, a database row, an external CMS, …) needs a mutex to prevent two concurrent runs from clobbering each other. A workflow that fronts an API needs rate-limiting to keep one caller from exhausting shared quota. The harness ships four primitives that compose into three operations:

| Mode | Primitive | Caller payload | Returns |
|---|---|---|---|
| Lock — wait-with-retry (default) | `lock_acquisition` | `{ scope, ttl_seconds, execution_id, wait_till_lock_released: true, max_wait_seconds }` | `{ acquired, count, scope, lock_id, key }` |
| Lock — fail-fast | `lock_acquisition` | `{ scope, ttl_seconds, execution_id, wait_till_lock_released: false, max_wait_seconds }` | `{ acquired, count, scope, lock_id, key }` OR Stop and Error |
| Rate limit | `rate_limit_check` | `{ scope, limit, windowSeconds }` | `{ allowed, scope, count, limit }` |

`lock_release` is the partner to `lock_acquisition` (always called once per acquire) and verifies caller ownership before releasing. `error_handler_lock_cleanup` actively iterates `<env>.yml.lockScopes`, GETs each scope's `:meta` sidecar, and DELs only the entries owned by the failed execution. Scopes not registered in `lockScopes` (typically dynamic ones) fall back to Redis-side TTL self-heal.

For node-graph diagrams + the Redis key namespace, see [`skills/integrations/redis/lock-pattern.md`](../integrations/redis/lock-pattern.md).

## Architectural rationale

The shipped pattern is **Redis-native atomic INCR + EXPIRE**. INCR is a single server-side atomic op that returns the post-increment count: the first caller gets 1, concurrent callers get 2, 3, … Whoever sees `count === 1` holds the lock. EXPIRE applied at the same time gives Redis-enforced TTL.

Wait-mode polls with **GET (read-only)** instead of re-INCR — because re-INCR would re-EXTEND the EXPIRE TTL on every poll, breaking the holder's TTL backstop. When GET returns null (lock released or expired), the waiter re-INCRs to attempt acquire.

This is materially better than a token-fencing pattern:
- Race-on-acquire is **prevented** at acquire time, not detected at release time.
- TTL is enforced **server-side** by Redis, not client-side by every reader.
- The counter is a plain integer; identity (owner, workflow, execution) lives in a separate `:meta` sidecar so the hot-path INCR stays cheap and the verification path can read JSON without contending on it.

## Safety model

**INCR is atomic.** Redis serializes increments. Two concurrent callers get distinct post-increment values; only one sees `count === 1` and holds the lock. There is no race-on-acquire window.

**Wasted INCRs on re-race are harmless.** If 5 waiters all see GET=null and all simultaneously re-INCR, only the first gets `count === 1` (holds); the others see counts 2–5 and re-enter wait. The inflated counter is cleared when the holder DELs on release.

**Release verifies ownership.** `lock_release` GETs the `:meta` sidecar, parses the stored `lock_id`, and DELs the counter + meta pair only when the caller-supplied `lock_id` matches. Mismatch raises StopAndError with a `LOGIC ERROR:` prefix that names the actual holder (workflow, execution, locked_at). Absent meta is treated as idempotent success (already released or expired). This catches caller bugs — wrong scope passed to release, or one workflow trying to release another's lock.

## When NOT to use this

The atomic-INCR pattern eliminates the race-on-acquire that the earlier token-fencing model could only detect. The remaining caveats are different:

- **Single-instance Redis assumed.** Multi-region / multi-master Redis topologies have eventual-consistency behaviors that can re-introduce races. Use a stronger primitive for cross-region coordination.
- **Holder must release.** A workflow that crashes between acquire and release leaves the lock held until `ttl_seconds` expires. For long-running workflows, set `--ttl-seconds` larger than your worst-case critical-section runtime.
- **No fairness.** Waiters are not queued in arrival order. Whichever waiter wins the next re-INCR race after the holder releases gets the lock. Could be unfair under heavy contention.
- **Wait-mode polls Redis.** Default `max_wait_seconds=86400` (24h) with 1-second poll interval = up to 86400 GETs to Redis per stuck waiter. Redis handles it without sweat, but it's worth knowing if you're cost-conscious or want to bound traffic.

For use cases the INCR pattern still doesn't fit (sub-millisecond contention, queued fairness, multi-region), consider Postgres advisory locks via `n8n-nodes-base.postgres` — they're transaction-scoped and integrate with your application DB if you have one.

## TTL semantics

`ttl_seconds` defaults to `86400` (24h). Set on Redis at acquire-time via the INCR node's `expire: true, ttl: <n>` parameter — **Redis-enforced**. A crashed holder's lock auto-expires after `ttl_seconds`; the next caller's INCR sees the key absent and starts fresh.

Tune per workflow:
- A 5-minute payment workflow → `--ttl-seconds 600` (10 min, generous buffer).
- A long batch job that may run for 6 hours → `--ttl-seconds 32400` (9h, also generous).

The TTL is NOT a wait timeout. It bounds how long an orphaned lock blocks the scope after a crash. The wait timeout is `--max-wait-seconds`.

## `max_wait_seconds` semantics

`max_wait_seconds` defaults to `86400` (24h) — effectively unbounded for typical use. The waiter polls every 1 second (hardcoded in the primitive) until either the lock is acquired or `max_wait_seconds` has elapsed since the original acquire attempt.

Override per-workflow with `--max-wait-seconds <n>` if you need fail-fast-ish semantics for time-sensitive callers (webhooks, user-facing API endpoints):

```bash
# Webhook handler — give up after 30 seconds, let upstream retry / queue.
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_lock_to_workflow.py \
  --workflow-key webhook_handler \
  --scope-expression "='user-' + $json.userId" \
  --max-wait-seconds 30
```

Lower bounds catch "lock is genuinely contended" without dragging out user-facing latency. The default `86400` is the conservative choice — assume callers want to wait unless they explicitly say otherwise.

## Wait mode

Default behavior (`wait_till_lock_released: true`): if the lock is held, the n8n Wait node fires for 1 second, then the flow GETs the lock key. If still present, loop back to Wait. If absent, re-INCR. If `max_wait_seconds` elapsed at any point, Stop and Error with a timeout message.

`--fail-fast` flips `wait_till_lock_released: false`: the primitive immediately Stop-and-Errors with a descriptive message including the current count.

The Wait node duration is hardcoded to 1 second. Edit the primitive in your workspace if you need a different cadence (most contention is sub-second; 1s is the right default).

## Scope expression

Each primitive invocation passes a `scope` field that becomes the Redis key suffix (`n8n-lock-<scope>`, with a paired `n8n-lock-<scope>:meta` sidecar). Choose carefully:

- `={{ $execution.id }}` — "one execution at a time" semantics. Useful for self-throttling.
- `={{ 'excel-' + $json.fileId }}` — per-resource locking (one Excel file at a time).
- `=api-v1-{{ $json.userId }}` — per-caller rate-limiting.
- `={{ 'global' }}` — single global lock or rate-limit across all callers.

Anything that produces a stable, per-protected-thing string works.

## Rate-limit semantics

`rate_limit_check` is **fixed-window INCR** (different from the lock pattern even though both use INCR):

- Bucket key: `n8n-ratelimit-<scope>-<floor(now_ms / (windowSeconds * 1000))>`.
- INCR returns the new count; EXPIRE is set on every INCR.
- `allowed = count <= limit`.

The boundary burst caveat: a caller can hit `limit` near the end of one window and `limit` again at the start of the next, so the worst-case observed throughput is `2 × limit` across the boundary. Token-bucket would smooth this but is deferred — fixed-window INCR is usually sufficient for "throttle obvious abuse" rather than "enforce a strict ceiling".

## Wiring it in

| Goal | Skill |
|---|---|
| Install the lock pair (copy + register in env YAMLs) | [`create-lock.md`](../create-lock.md) — use `--include-error-handler` and/or `--include-rate-limit` as needed. |
| Copy a single primitive without registration | [`copy-primitive.md`](../copy-primitive.md) |
| Wrap a workflow in lock acquire / release (default wait mode) | [`add-lock-to-workflow.md`](../add-lock-to-workflow.md) |
| Wrap a workflow in lock acquire / release with fail-fast | [`add-lock-to-workflow.md`](../add-lock-to-workflow.md) — pass `--fail-fast` |
| Tune the lock TTL | [`add-lock-to-workflow.md`](../add-lock-to-workflow.md) — pass `--ttl-seconds` |
| Tune the wait timeout | [`add-lock-to-workflow.md`](../add-lock-to-workflow.md) — pass `--max-wait-seconds` |
| Add error-handler cleanup hook (active per-scope cleanup; falls back to Redis TTL for unregistered scopes) | [`add-lock-to-workflow.md`](../add-lock-to-workflow.md) — pass `--lock-on-error` (requires `--include-error-handler` at create-lock time) |
| Gate a workflow with a rate-limit | [`add-rate-limit-to-workflow.md`](../add-rate-limit-to-workflow.md) — requires `--include-rate-limit` at create-lock time |

## Caveats

- **Real Redis required.** All four primitives use `n8n-nodes-base.redis` — a Redis credential must be reachable from your n8n instance. See [`skills/integrations/redis/lock-pattern.md`](../integrations/redis/lock-pattern.md).
- **Single-instance Redis assumed.** Multi-region coordination is out of scope.
- **No automatic primitive migration.** Workspaces with old (pre-INCR) primitives are not auto-updated. Use `create_lock.py --force-overwrite` (or `copy_primitive.py --force-overwrite`) to opt in.
