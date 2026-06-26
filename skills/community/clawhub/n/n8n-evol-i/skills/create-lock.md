---
name: create-lock
description: First-time setup for distributed locking + rate-limit — copy the coordination primitives into the workspace AND register them in env YAMLs.
user-invocable: false
---

# create-lock

## When

First time the user wants distributed-locking or rate-limiting semantics in their workflows.

This skill is the **bundled** entry point: it copies the lock pair (lock_acquisition + lock_release) by default, plus optional opt-ins for the error-handler stub and rate-limit primitive, AND registers each in every configured env's YAML so callers can reference them by ID. For copying just one primitive without registration, see [`copy-primitive.md`](copy-primitive.md).

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/create_lock.py \
  [--include-error-handler] \
  [--include-rate-limit] \
  [--force-overwrite]
```

## Side effects

- Copies these primitives from `${CLAUDE_PLUGIN_ROOT}/primitives/workflows/` into `<workspace>/n8n-workflows-template/`:
  - `lock_acquisition.template.json` (always)
  - `lock_release.template.json` (always)
  - `error_handler_lock_cleanup.template.json` (with `--include-error-handler`)
  - `rate_limit_check.template.json` (with `--include-rate-limit`)
- Registers each in every configured env's YAML (delegates to `create_workflow.py --no-template`). This mints placeholder workflow IDs that callers reference via `{{@env:workflows.lock_acquisition.id}}` etc.
- Adds them to `deployment_order.yml` under "Tier 0a: leaves" so they deploy before any caller workflow that depends on them.

After this skill, the user owns the primitives in their workspace. The harness's seed copies in `${CLAUDE_PLUGIN_ROOT}/primitives/workflows/` are never written to.

## What you're actually deploying

The four primitives are sub-workflows that wrap the dedicated `n8n-nodes-base.redis` node:

- `lock_acquisition` uses Redis-native atomic INCR + EXPIRE for acquire, with a GET-poll wait loop for retry-on-contention. After a successful acquire it writes a JSON identity sidecar at `n8n-lock-<scope>:meta` (lock_id, workflow_id, workflow_name, execution_id, locked_at) for ownership-checked release. 15 nodes total.
- `lock_release` GETs the meta sidecar, parses, verifies the caller's `lock_id` matches, then DELs both `n8n-lock-<scope>` (counter) and `n8n-lock-<scope>:meta` (identity). Mismatch → StopAndError with `LOGIC ERROR` prefix. Absent meta → idempotent success.
- `error_handler_lock_cleanup` actively iterates `<env>.yml.lockScopes`, GETs each scope's `:meta`, and DELs only the entries owned by the failed execution (matched by `execution_id`). Empty/missing `lockScopes` → graceful no-op with a config-gap log entry.
- `rate_limit_check` is a fixed-window INCR counter at `n8n-ratelimit-<scope>-<bucket>`, 4 nodes.

### `lockScopes` env config

For active error-handler cleanup to work, every static lock scope used in your workflows must be registered in `<env>.yml.lockScopes`. `add_lock_to_workflow.py` auto-appends static literal scopes (`={{ "foo" }}`-form) here on each invocation; dynamic scopes (`={{ "lock-" + $json.x }}`) require manual maintenance. Example:

```yaml
# n8n-config/dev.yml
lockScopes:
  - excel-sharepoint-write
  - cms-row-update
  - global
```

`doctor.py` will WARN with verdict `lock-scopes-unregistered` when a deployed workflow's Lock Acquire scope is missing from this list.

For node-graph diagrams + the Redis key namespace, see [`skills/integrations/redis/lock-pattern.md`](integrations/redis/lock-pattern.md). For the safety model (atomic INCR prevents race-on-acquire) and when this pattern is NOT safe enough (multi-region Redis, fairness-required), see [`skills/patterns/locking.md`](patterns/locking.md).

| Primitive | Used by |
|---|---|
| `lock_acquisition` + `lock_release` | `add-lock-to-workflow.md` (the standard wrap-a-workflow flow) |
| `error_handler_lock_cleanup` | `add-lock-to-workflow.md --lock-on-error` (active cleanup; iterates `<env>.yml.lockScopes`) |
| `rate_limit_check` | `add-rate-limit-to-workflow.md` |

## Flag details

- **`--include-error-handler`** — also copy `error_handler_lock_cleanup`. Required if you'll add `--lock-on-error` to any workflow via `add-lock-to-workflow`.
- **`--include-rate-limit`** — also copy `rate_limit_check`. Required before `add-rate-limit-to-workflow` will run.
- **`--force-overwrite`** — overwrite existing workspace copies of the primitives instead of skipping them. Default off (preserves idempotence). Without the flag, an already-present primitive triggers:
  ```
  WARNING: <key>.template.json already exists — re-run with --force-overwrite
  to update to the real Redis implementation.
  ```
  Use this when upgrading from an earlier harness version that shipped placeholder Set-node primitives — it pulls the current real-Redis bodies in.

## Next steps

- [`add-lock-to-workflow.md`](add-lock-to-workflow.md) to wrap a workflow's flow in lock acquire / release.
- [`add-rate-limit-to-workflow.md`](add-rate-limit-to-workflow.md) to gate a workflow with a rate-limit (requires `--include-rate-limit` here).

## When to use copy-primitive instead

Use [`copy-primitive.md`](copy-primitive.md) instead of this skill when:
- You only want one primitive, not the bundled lock pair.
- You don't need env-YAML registration (e.g., experimenting in a fresh workspace before bootstrap-env).
- You want to force-update one primitive without touching the others.

`create-lock` is "everything for locking, ready to deploy". `copy-primitive` is "drop one file in".
