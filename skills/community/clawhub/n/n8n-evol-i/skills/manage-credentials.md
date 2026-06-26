---
name: manage-credentials
description: Single source of truth for credential lifecycle (Path A — agent-mediated create from .env; Path B — link to existing n8n credential).
user-invocable: false
---

# manage-credentials

## When

Any time a workflow needs an n8n credential — whether the user wants the agent to mint it from secrets in `.env.<env>` (Path A) or to use a credential they already created in the n8n UI (Path B).

## Policy (load-bearing)

1. **The agent NEVER collects API keys, OAuth secrets, or any credential material from the user directly in the chat.** The agent MUST instruct the user to write secrets into `<workspace>/n8n-config/.env.<env>` following `<workspace>/n8n-config/.env.example`.
2. **The agent NEVER reads `.env*` files itself.** Reading `.env.<env>` is exclusively a subprocess concern: when the agent invokes this helper, the helper loads the env via `helpers/config.py:load_env()` for the duration of the subprocess. The agent's context never sees secret values.
3. **The agent figures out which credentials are needed** by consulting n8n documentation (Context7 or web search) for the specific node `type`s it intends to use — not from a hardcoded per-service playbook in the harness. Once the agent knows the n8n credential `type` (e.g. `microsoftOAuth2Api`, `gmailOAuth2`, `redis`, `openAiApi`) and which secret-env-var names that type expects, fall into one of the two paths below.

## Path A (agent-mediated creation — preferred when secrets are available in `.env.<env>`)

1. Agent appends the required secret env-var names to `<workspace>/n8n-config/.env.example` (as documentation only; values stay empty) and tells the user to copy them into `<workspace>/n8n-config/.env.<env>` with real values.
2. Agent runs:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_credentials.py create \
  --env <env> --key <yaml-key> \
  --type <n8n-credential-type> --name "<display name>" \
  --env-vars KEY1,KEY2,...
```

3. The helper loads `.env.<env>` via `config.py:load_env()`, builds the credential `data` payload, POSTs to `<base>/api/v1/credentials`, captures the returned `id` + `name`, and writes them into `<workspace>/n8n-config/<env>.yml` under `credentials.<key>: { id, name, type }`.

`--dry-run` previews the body (with values redacted) without POSTing.

## Path B (user-mediated creation in n8n UI — preferred when OAuth flow needs UI interaction)

1. User creates the credential themselves in the n8n UI.
2. Agent runs:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/manage_credentials.py list-link \
  --env <env> --key <yaml-key> \
  --type <n8n-credential-type> [--from-name "<existing display name>"]
```

3. The helper GETs `<base>/api/v1/credentials`, filters by `type` (and `name` if `--from-name`), prints matches, picks the unique one (or fails if multiple match without `--from-name`), and writes `id`+`name`+`type` into `<workspace>/n8n-config/<env>.yml` under `credentials.<key>`.

## Idempotence

Re-running with the same `--key` against an already-populated YAML row is a no-op when the n8n side matches. The helper diffs n8n vs YAML and only writes on change.

## See also

- `skills/patterns/credential-refs.md` — YAML shape + placeholder syntax (reference pattern).
- [`skills/manage-variables.md`](manage-variables.md) — sibling skill for **n8n Variables** (non-credential runtime values, or secret fallback when `$env` is blocked). Variables ≠ credentials; do not conflate.
- `skills/integrations/<service>/...md` — per-service `type` strings + service-specific gotchas.
- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `GET /credentials` filter parameters and response shape via Context7 before relying on training-data recall.
