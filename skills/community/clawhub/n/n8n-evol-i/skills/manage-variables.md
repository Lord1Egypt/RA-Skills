---
name: manage-variables
description: Lifecycle for n8n Variables (instance-wide key-value pairs read at expression runtime as `$vars.*`). Companion to manage-credentials.
user-invocable: false
---

# manage-variables

## When

Any time a workflow expression needs a runtime value that **is not a credential**:

- A non-secret string the workflow should resolve at execution time (a base URL, a Redis stream prefix, a feature-flag toggle).
- A secret that the deployment cannot reach via `$env.*` because env access is blocked (n8n Cloud's default sandbox mode, or self-hosted with `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`).

If the value belongs in an n8n credential — anything with auth shape (API key, OAuth token, basic-auth header, certificate) — use [`manage-credentials.md`](manage-credentials.md) instead. Variables and credentials are sibling concepts that solve different problems; do not conflate them.

## Variables vs credentials vs `$env` vs harness env-YAML

Four distinct mechanisms. Pick by what the value is and where it must resolve.

| Mechanism | Value lives in | Resolved at | Read in templates as | Use for |
|---|---|---|---|---|
| **Credential** | n8n DB (encrypted) | Workflow execution (n8n injects per-node) | `credentials.<type>.{id,name}` block on the node | Auth material (API keys, OAuth tokens, DB passwords, header tokens) |
| **n8n Variable** | n8n DB (plaintext, instance-scoped) | Workflow execution (expression engine) | `={{ $vars.NAME }}` | Runtime non-secret values, OR secrets when `$env` is blocked |
| **`$env` (host env-var)** | OS env-var passed to the n8n process | Workflow execution (expression engine) | `={{ $env.NAME }}` | Runtime values on self-hosted instances with env access enabled |
| **Harness env-YAML** | `<workspace>/n8n-config/<env>.yml` | Hydrate time (before deploy — value baked into JSON) | `{{@env:dotted.path}}` | Deploy-time config that's the same across every execution (workflow IDs, display names, credential IDs) |

The big practical split between `$env` and `$vars`: `$env` is the cleanest expression-side mechanism, but **n8n Cloud blocks it by default** and self-hosted instances often lock it down via `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`. When blocked, every reference throws `ExpressionError: access to env vars denied`. Variables are the supported fallback.

## Policy (load-bearing)

1. **The agent NEVER collects variable values from the user directly in the chat.** Secret values flow through `<workspace>/n8n-config/.env.<env>` exactly like credentials — the helper loads them via subprocess; the agent's context never sees them.
2. **The agent NEVER reads `.env*` files itself.** Same discipline as `manage-credentials`.
3. **Variables are not version-controlled.** Unlike credentials (which get an `id`+`name` row in `<env>.yml`), n8n variables have no YAML representation. The helper warns about this on every mutation. This is by design: variables can be changed in the n8n UI without breaking deployed workflows, and the source of truth is the live n8n instance.
4. **Prefer `$env` where it works.** Variables exist because `$env` is sometimes unavailable, not because they're better. On self-hosted instances with env access enabled, `$env` is the simpler path — no instance-side resource to mint, no extra REST round-trip on activate.

## Lifecycle

```bash
# List (optionally filter by name)
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_variables.py list \
  --env <env> [--name <variable-name>]

# Create
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_variables.py create \
  --env <env> --name <variable-name> --value "<value>"

# Update (requires --id from list)
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_variables.py update \
  --env <env> --id <var-id> --name <variable-name> --value "<value>"

# Delete (dry by default; needs --force to actually delete)
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_variables.py delete \
  --env <env> --id <var-id> [--force]
```

`--name` is the n8n variable's **name** (called `key` in the n8n REST API; the helper translates at the HTTP boundary). The CLI deliberately uses `--name` because `--key` already means a YAML config slot elsewhere in the harness (`credentials.<key>`, `workflows.<key>`).

## When `$env` is blocked (the n8n Cloud case)

Symptom: a deployed workflow throws `ExpressionError: access to env vars denied` at the first node that evaluates `={{ $env.* }}`.

Confirm: try `={{ Object.keys($env) }}` in a Code node — if you get the same error rather than an array, env access is blocked.

Resolution paths, in preference order:

1. **Self-host with env enabled.** Set `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` on the n8n process and restart. Cleanest fix if you control the deployment.
2. **Replace the `$env.*` reference with `$vars.*`** in the affected templates (the workflow-level change) AND mint the variable via `manage_variables.py create` (the n8n-instance-level change). The harness's primitives stay `$env`-first; per-deployment overrides live in the user's workspace.
3. **Bake the value at hydrate time** via `{{@env:...}}` reading from `<env>.yml`. Only works for deploy-time-stable values — every workflow execution reads the value frozen at deploy time, not at execution time.

Do not switch the shipped primitives from `$env` to `$vars` to work around (2) — that would force every operator onto the variable-creation step even on instances where `$env` works. Variables are an opt-in deployment-specific fallback, not the default.

## Idempotence

`manage_variables.py` does NOT diff before mutating: `create` always POSTs, `update` always PUTs. n8n returns an error on duplicate `key` for create. Use `list --name` first if you need to detect-before-mutate.

(This differs from `manage_credentials.py`, which diffs n8n vs YAML and no-ops on a match. The asymmetry exists because variables have no YAML representation to diff against.)

## See also

- [`skills/manage-credentials.md`](manage-credentials.md) — sibling: credential lifecycle (Path A / Path B), the auth-material companion to this skill.
- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `GET /variables` filter parameters and response shape via Context7 before relying on training-data recall.
- [`skills/integrations/redis/queue-pattern.md`](integrations/redis/queue-pattern.md) — concrete example: the queue primitives use `$env.UPSTASH_REDIS_REST_URL` by default; on `$env`-blocked instances, the operator mints `UPSTASH_REDIS_REST_URL` as a variable instead.
