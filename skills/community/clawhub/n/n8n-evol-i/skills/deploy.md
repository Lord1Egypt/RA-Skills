---
description: Hydrate, PUT to n8n, and (default) activate one workflow on one env.
---

# deploy

## When

Roll one workflow to one env.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy.py --env <env> --workflow-key <key> [--no-activate] [--rehydrate] [--debug]
```

## Side effects

1. Calls `hydrate.py` first (composes; produces `<workspace>/n8n-build/<env>/<key>.generated.json`) if missing or `--rehydrate`.
2. Reads the generated JSON, drops disallowed PUT fields (active, tags, id, versionId), PUTs to `<base>/api/v1/workflows/<id>`.
3. By default, activates via `POST /workflows/<id>/activate`. `--no-activate` skips this.
4. With `--debug`, dumps redacted pre/post artifacts to `~/.cache/n8n-evol-I/debug/<pid>/deploy-<n>.json` (mode 0600).

## Pattern

See `skills/patterns/validate-deploy.md` for the canonical 5-step loop.

## n8n Cloud sub-workflow caveat

n8n Cloud surfaces an extra constraint that self-hosted instances don't enforce uniformly: a parent workflow that calls another workflow via `Execute Workflow` cannot be activated until **every referenced sub-workflow is itself active (n8n's "published" state)**. If you call `deploy.py` (or `deploy_all.py`) on the parent before its sub-workflows are activated, n8n Cloud rejects the activate POST with:

```
400 {"message":"Cannot publish workflow: Node \"X\" references workflow Y (\"...\") which is not published. Please publish all referenced sub-workflows first."}
```

Note: there is **no separate `/publish` endpoint** in n8n's public REST API. `POST /api/v1/workflows/{id}/activate` IS the publish action — n8n renamed the UI verb from "Activate" to "Publish" but the API path stayed the same. The harness's `activate.py` already calls the right endpoint; the issue is purely activation ordering.

**Workarounds:**

1. **Use `deploy_all.py` with proper tier ordering.** Put leaf sub-workflows (no Execute Workflow callers, or whose callers are leaves) in earlier tiers. The harness's default order — `Tier 0a: leaves` → `Tier 0b: handlers` → `Tier 1` and onward — does this correctly. If a leaf's own activation fails for a different reason (e.g. invalid credential ref), `deploy_all.py` will warn-and-continue by default, but the parent's activate will then 400. Look at the leaf failure first.
2. **Activate manually via UI** if a single workflow needs to be unblocked out-of-band — then re-run `deploy.py` on the parent.
3. **Self-hosted instances** generally don't enforce this; the caveat is Cloud-specific.

`deploy.py` exits with code 2 (distinct from PUT failure code 1) when only activation failed. `deploy_all.py` treats exit=2 as warn-and-continue by default — pass `--strict-activate` to escalate it to a tier-stop.

## See also

- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `PUT /workflows/{id}` accepted-fields list and `/activate` response shape via Context7 before assuming training-data recall is current.
