---
name: integration-redis
description: Redis-backed coordination primitives — atomic-INCR lock with GET-poll wait loop, rate-limit, key namespace.
user-invocable: false
---

# Redis (lock + rate-limit pattern)

The harness ships four primitives backed by the dedicated `n8n-nodes-base.redis` node (NOT `this.helpers.redis.call(...)` from a Code node — that API is only exposed inside custom-node `INodeType.execute()` methods, not in user Code-node sandboxes).

## Credential

`redis` credential type. See [`skills/manage-credentials.md`](../../manage-credentials.md). The four primitives all reference it via `{{@env:credentials.redis.{id,name}}}` placeholders.

## Shipped primitives

| Primitive | Trigger | Output |
|---|---|---|
| `lock_acquisition` | `executeWorkflowTrigger` (inputs: `scope, ttl_seconds, execution_id, wait_till_lock_released, max_wait_seconds, lock_id, workflow_id, workflow_name`) | `{ acquired, count, scope, lock_id, key, meta_key, workflow_id, workflow_name, execution_id, locked_at }` |
| `lock_release` | `executeWorkflowTrigger` (inputs: `scope, lock_id`) | `{ released: true, idempotent: bool, scope, lock_id }` — or StopAndError on ownership mismatch |
| `error_handler_lock_cleanup` | `errorTrigger` | `{ cleaned: bool, cleaned_count, scopes }` — actively iterates `<env>.yml.lockScopes`, GETs each `:meta`, DELs only the failed-execution-owned ones |
| `rate_limit_check` | `executeWorkflowTrigger` (inputs: `scope, limit, windowSeconds`) | `{ allowed, scope, count, limit }` |

Every Code-node body inside these primitives starts with `// @n8n-evol-I:primitive` to bypass `validate.py`'s pure-function discipline. **Do not copy that marker into user Code nodes** — it silently disables validation.

## Lock storage: counter + identity sidecar

Two Redis keys per held lock:
- `n8n-lock-<scope>` — plain integer counter (set via INCR, expires via EXPIRE). Atomic acquire: whoever sees `count === 1` after the INCR holds the lock.
- `n8n-lock-<scope>:meta` — JSON sidecar written by `Set Lock Meta` immediately after the count===1 branch. Contains `{lock_id, workflow_id, workflow_name, execution_id, locked_at}`. Same TTL as the counter so they expire together.

The sidecar exists so:
- **Release can verify ownership** — the release primitive GETs the meta, parses, compares the caller-supplied `lock_id` to the stored one, and DELs both keys only on match. Mismatch → StopAndError with a `LOGIC ERROR:` prefix that names the actual holder. This catches bugs where workflow A tries to release a lock workflow B is holding.
- **Active error-handler cleanup** — `error_handler_lock_cleanup` iterates `<env>.yml.lockScopes`, GETs each meta, finds the entries whose `execution_id` matches the failed execution, and DELs only those. The TTL backstop still applies for unregistered (typically dynamic) scopes.

The bare `n8n-lock-` namespace prevents collisions with any unrelated Redis traffic on the same instance.

## `lock_acquisition` node graph (15 nodes)

```
Execute Workflow Trigger
       │
       ▼
Build Lock Context (Code: scope, ttl, executionId, key, meta_key, lock_id, workflow_id,
                          workflow_name, locked_at, deadline_ms = now + max_wait_seconds*1000)
       │
       ▼
INCR Acquire Attempt (Redis INCR + EXPIRE)  ◄────────────────────────────┐
       │                                                                  │
       ▼                                                                  │
Evaluate Acquired (Code: count = $json[ctx.key]; acquired = count === 1)  │
       │                                                                  │
       ▼                                                                  │
Acquired? (If $json.acquired === true)                                    │
   ├── true  → Set Lock Meta (Redis SET <meta_key> = JSON identity sidecar, EXPIRE = ttl)
   │              │                                                       │
   │              ▼                                                        │
   │          Build Acquire Output (Code: { acquired:true, count, scope, lock_id,
   │                                        key, meta_key, workflow_id, workflow_name,
   │                                        execution_id, locked_at })
   └── false → Should Wait? (If wait_till_lock_released === true)         │
                  ├── false → Fail Fast — Lock Held (Stop and Error)      │
                  └── true  → Wait Before Poll (n8n Wait, 1 second)       │
                               │                                          │
                               ▼                                          │
                              GET Lock (Redis GET, propertyName=LOCK_VALUE)
                               │                                          │
                               ▼                                          │
                              Check Wait State (Code: returns state ∈     │
                                {timeout, retry-incr, keep-waiting})      │
                               │                                          │
                               ▼                                          │
                              Timeout? (If state === 'timeout')           │
                               ├── true  → Wait Timeout — Stop (Stop and Error)
                               └── false → Retry INCR? (If state === 'retry-incr')
                                              ├── true  ───────────────── ┘
                                              └── false → loops back to Wait Before Poll
```

Node-by-node:

- **Build Lock Context**: pure JS. Computes `key = n8n-lock-<scope>`, `meta_key = <key>:meta`, `lock_id = caller-supplied || crypto.randomUUID() || executionId`, `deadline_ms = Date.now() + max_wait_seconds * 1000`, plus the workflow-identity fields (`workflow_id`, `workflow_name`, `locked_at`) used by the `:meta` sidecar. Output is referenced via `$('Build Lock Context').first().json` from every loop iteration — n8n's `$()` returns the most recent execution of a node, which is stable across loop revisits.
- **INCR Acquire Attempt**: Redis INCR with `expire: true, ttl: $json.ttl`. INCR is atomic server-side; only one concurrent caller sees the post-increment count of 1. EXPIRE is re-applied on every INCR (a property of the n8n Redis node) — not a problem for the holder (their TTL gets refreshed each time someone else races and fails) and bounded by max_wait_seconds for waiters.
- **Evaluate Acquired**: pure JS. Reads `$json[ctx.key]` (the INCR result) and computes `acquired = count === 1`.
- **Acquired?**: standard If. Success branch flows into `Set Lock Meta`; failure branch flows into `Should Wait?`.
- **Set Lock Meta**: Redis SET on `<meta_key>` with the JSON identity sidecar (`{lock_id, workflow_id, workflow_name, execution_id, locked_at}`) and EXPIRE = `ttl` so the meta expires alongside the counter. Only runs on the count===1 branch — waiters never write meta.
- **Build Acquire Output**: pure JS. Surfaces the full identity payload (lock_id, workflow_id, workflow_name, execution_id, locked_at, key, meta_key, count, scope, acquired:true) to the calling workflow so it can pass `lock_id` to `lock_release` and observe the rest in logs.
- **Should Wait?**: routes between fail-fast (Stop and Error) and wait-loop based on the original `wait_till_lock_released` input.
- **Wait Before Poll**: n8n Wait node, `amount: 1, unit: seconds`. Releases the worker between polls (not pinned).
- **GET Lock**: Redis GET with `propertyName: LOCK_VALUE`. Read-only — does NOT touch the EXPIRE. Returns null if the key has expired or been DEL'd.
- **Check Wait State**: pure JS. Reads `$json.LOCK_VALUE` and `Build Lock Context`'s `deadline_ms`. Returns one of three states:
  - `timeout` if `now > deadline_ms`
  - `retry-incr` if `LOCK_VALUE` is null/empty (lock released — try INCR again)
  - `keep-waiting` if `LOCK_VALUE` is present and not yet timed out
- **Timeout?** + **Retry INCR?**: two sequential If nodes routing on the state field.

### Why GET, not INCR, in the wait loop

Re-INCR'ing inside the wait loop would re-EXTEND the EXPIRE TTL on every poll attempt (the n8n Redis node always re-applies EXPIRE on INCR), defeating the holder's TTL backstop. GET is read-only and doesn't touch the TTL — so the holder's TTL counts down independently of how many waiters are polling.

### Wasted INCRs on re-race

If 5 waiters all see GET=null and all simultaneously re-INCR:
- Caller A: post-increment value 1 → acquired
- Callers B/C/D/E: values 2–5 → re-enter wait

The wasted INCRs leave the Redis counter at 5 instead of 1. **Harmless** — `count === 1` is the ownership check (only A holds), and when A eventually DELs on release, the inflated counter goes with the key. The next acquire INCRs from scratch.

## `lock_release` node graph (8 nodes)

```
Execute Workflow Trigger (inputs: scope, lock_id)
       │
       ▼
Build Release Context (Code: scope, key = n8n-lock-<scope>, meta_key = <key>:meta, provided_lock_id)
       │
       ▼
GET Lock Meta (Redis GET, propertyName = LOCK_META, key = <meta_key>)
       │
       ▼
Parse + Verify Ownership (Code: parse JSON; is_match = parsedLock.lock_id === provided_lock_id;
                                also surfaces stored workflow_id / workflow_name / execution_id / locked_at)
       │
       ▼
Match? (If $json.is_match === true)
   ├── true (held + ours)  → DEL Lock Counter (Redis DEL key)
   │                                │
   │                                ▼
   │                         DEL Lock Meta (Redis DEL meta_key)
   │                                │
   │                                ▼
   │                         Build Result (Code: { released:true, idempotent:false, scope, lock_id })
   │
   └── false (held + not ours) → Ownership Mismatch — Stop (Stop and Error: 'LOGIC ERROR: ...')
```

Output on success: `{ released: true, idempotent: bool, scope, lock_id }`. `idempotent:true` is the absent-meta case — the meta key already expired or was DEL'd by an earlier release. `idempotent:false` is the live release path (the caller's lock_id matched, both keys were DEL'd).

Output on mismatch: StopAndError with a `LOGIC ERROR:` prefix that names the actual holder (workflow, execution, locked_at). The wrapper flow (`add_lock_to_workflow.py`) is structured so only the holder reaches release in normal operation — the ownership check is the defensive backstop that catches caller bugs (wrong scope passed, two workflows sharing a `lock_id` they shouldn't).

## `rate_limit_check` node graph (4 nodes)

```
Execute Workflow Trigger
       │
       ▼
Build Bucket Key (Code: scope/limit/windowSeconds + key = n8n-ratelimit-<scope>-<bucket>)
       │
       ▼
Redis INCR (operation=incr, key=$json.key, expire=true, ttl=$json.windowSeconds)
       │
       ▼
Build Result (Code: count = $json[prev.key]; allowed = count <= prev.limit)
       │
       ▼ output: { allowed, scope, count, limit }
```

Bucket key: `n8n-ratelimit-<scope>-<floor(now_ms / (windowSeconds * 1000))>`. The bucket integer rotates each window, so old buckets garbage-collect via their own EXPIRE TTL.

Boundary-burst caveat: a caller can hit `limit` near the end of one window and `limit` again at the start of the next, so observed throughput can reach `2 × limit` across the edge. Token-bucket would smooth this but is deferred.

## `error_handler_lock_cleanup` (active per-scope cleanup, 9 nodes)

```
Error Trigger
       │
       ▼
Prepare Scope List (Code: read <env>.yml.lockScopes via {{@env:lockScopes}};
                    fan out one item per registered scope with key + meta_key + failed_execution_id;
                    if list is empty, terminate with cleanup_terminal:true and a config-gap log entry)
       │
       ▼
Has Scopes? (If $json.cleanup_terminal !== true)
   ├── false (no scopes) → terminates with the no-op log entry
   └── true              → GET Scope Meta (Redis GET, propertyName = LOCK_META, key = <meta_key>) — runs per-scope
                                │
                                ▼
                          Filter Owned Scopes (Code: parse each meta JSON; keep only items where
                                                parsedLock.execution_id === failed_execution_id)
                                │
                                ▼
                          Owned? (If $json.should_release === true)
                            ├── true  → DEL Owned Counter (Redis DEL key)
                            │                │
                            │                ▼
                            │           DEL Owned Meta (Redis DEL meta_key)
                            │                │
                            │                ▼
                            │           Log Cleanup (Code: { cleaned, cleaned_count, scopes })
                            └── false → terminates without DEL
```

Real Redis ops. The handler iterates every scope registered in `<env>.yml.lockScopes`, GETs the `:meta` sidecar, and DELs the lock+meta pair only for the entries whose stored `execution_id` matches the failed execution. Locks owned by other executions are left intact; locks for scopes not registered in `lockScopes` (typically dynamic ones whose key shape isn't known at config time) fall back to Redis-side TTL self-heal.

Output: `{ cleaned: bool, cleaned_count, scopes: [...] }`. Empty `lockScopes` → graceful no-op with a `reason` field that surfaces the configuration gap to the operator log.

See [`skills/create-lock.md`](../../create-lock.md) § "lockScopes env config" for how scopes get into the registry (`add_lock_to_workflow.py` auto-appends static scopes; dynamic scopes need manual entries).

## Key namespace

| Key shape | Operation | Set by | Cleared by |
|---|---|---|---|
| `n8n-lock-<scope>` (e.g. `n8n-lock-excel-fileId-123`) | Plain integer counter | `lock_acquisition.INCR Acquire Attempt` (INCR + EXPIRE) | `lock_release.DEL Lock Counter` (on ownership match), `error_handler_lock_cleanup.DEL Owned Counter` (on crash, owned scope), OR Redis EXPIRE after `ttl_seconds` |
| `n8n-lock-<scope>:meta` | JSON sidecar — `{lock_id, workflow_id, workflow_name, execution_id, locked_at}` | `lock_acquisition.Set Lock Meta` (SET + EXPIRE, same TTL as counter) | `lock_release.DEL Lock Meta` (on ownership match), `error_handler_lock_cleanup.DEL Owned Meta` (on crash, owned scope), OR Redis EXPIRE alongside the counter |
| `n8n-ratelimit-<scope>-<bucket>` | Rate-limit counter | `rate_limit_check.Redis INCR` (INCR + EXPIRE) | EXPIRE after `windowSeconds` |

`<bucket>` for rate-limit is `floor(Date.now() / (windowSeconds * 1000))` — an integer that increments once per window.

## TTL discipline

- **Lock TTL** defaults to `86400` (24h). Set on Redis at acquire-time via INCR's `expire: true, ttl: <n>` parameter. **Server-enforced.** A crashed holder's lock auto-expires after `ttl_seconds`.
- **`max_wait_seconds`** also defaults to `86400` (24h). Different concept: this is the wait-loop's deadline (how long a waiter polls before giving up). Override per-workflow for time-sensitive callers (webhooks → 30s).
- **Rate-limit TTL** equals `windowSeconds`, applied via the Redis INCR node's `expire: true, ttl: ...` parameters. Server-enforced.

## Why `this.helpers.redis` is NOT used

n8n Code nodes run inside a V8 isolate that exposes only `$json`, `$input`, `$()`, `$node`, `$execution`, `$workflow`, `$now`, `$today`. The `this.helpers.*` API surface (httpRequest, redis, etc.) is the **node-developer SDK** — accessible only from `INodeType.execute()` in custom-node code, NOT from the user-facing Code-node sandbox. n8n's docs hedge this: "Some methods and variables aren't available in the Code node. These aren't in the documentation."

So all Redis I/O in the harness primitives goes through the dedicated `n8n-nodes-base.redis` node. The Code nodes only do pure JS work (key construction, count comparison, deadline arithmetic, state-routing decisions).

## See also

- [`skills/patterns/locking.md`](../../patterns/locking.md) — atomic-INCR safety model, when this pattern is + isn't safe.
- [`skills/manage-credentials.md`](../../manage-credentials.md) — Redis credential setup.
- [`skills/create-lock.md`](../../create-lock.md) — installing the lock pair into a workspace.
- [`skills/copy-primitive.md`](../../copy-primitive.md) — copy any single primitive without bundled registration.
- [`skills/add-lock-to-workflow.md`](../../add-lock-to-workflow.md) — wrap an existing workflow with acquire/release.
- [`skills/add-rate-limit-to-workflow.md`](../../add-rate-limit-to-workflow.md) — gate a workflow with rate-limit.
