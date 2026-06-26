---
name: bootstrap-env
description: Stand up an n8n environment from scratch and/or top up its placeholder workflow IDs.
user-invocable: false
---

# bootstrap-env

## When

- **Fresh env** — first time setting up `dev` / `staging` / `prod` / a colleague's instance.
- **Top-up env** — `<env>.yml` exists, but new `workflows.<key>` rows have placeholder IDs that need real n8n IDs minted.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/bootstrap_env.py --env <name> [--instance <url>] [--api-key <key>] [--postfix " [DEV]"] [--display-name "Development"] [--dry-run]
```

If `--instance` / `--api-key` omitted on the CLI, the helper falls back to env vars (`N8N_API_KEY`) or prompts.

## Side effects

Three idempotent stages:

1. **YAML / secret creation (if absent).** Writes `<workspace>/n8n-config/<env>.yml` and `<workspace>/n8n-config/.env.<env>` (mode 0600). Skipped if YAML already exists.
2. **Live validation.** `GET /api/v1/workflows?limit=1` against the env's instance. Rolls back any stage-1 writes on failure and exits 1.
3. **Placeholder workflow minting.** For every `workflows.<key>` whose `id` is empty / null / starts with `your-` / equals `placeholder`, POSTs an empty workflow to n8n and writes the returned ID back into the YAML.

`--dry-run` prints what would be done without writing or POSTing.

## Tearing down an env

Manually delete `<workspace>/n8n-config/<env>.yml` and `<workspace>/n8n-config/.env.<env>`. There is no teardown helper.

## See also

- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `POST /workflows` minimum-body shape via Context7 before relying on training-data recall.
