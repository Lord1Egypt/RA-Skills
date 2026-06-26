---
name: unarchive-workflow
description: Restore a previously-archived workflow via POST /api/v1/workflows/{id}/unarchive so it accepts updates again.
user-invocable: false
---

# unarchive-workflow

## When

A workflow was previously archived via [`archive-workflow.md`](archive-workflow.md) and now needs to be edited or redeployed. Without unarchiving first, every `PUT /workflows/{id}` rejects with `400 {"message":"Cannot update an archived workflow."}` — including the PUT that `deploy.py` issues.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/unarchive.py \
  --env <env> \
  --workflow-key <wf>
```

## Side effects

- Resolves `<wf>` to its workflow id via `<workspace>/n8n-config/<env>.yml.workflows.<wf>.id`.
- Calls `POST /api/v1/workflows/<id>/unarchive` against the env's n8n instance.
- After unarchive, the workflow is in deactivated state — run `activate-single-workflow-in-env.md` (or pass through `deploy.py`) to re-enable triggers.

## Typical sequence

```bash
# Restore an archived workflow and bring it back online:
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/unarchive.py --env prod --workflow-key foo
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy.py --env prod --workflow-key foo
```

`deploy.py` re-PUTs the latest hydrated template and (by default) activates — so unarchive + deploy is the round-trip from archived back to live.

## See also

- [`archive-workflow.md`](archive-workflow.md) — archive a deployed workflow.
- [`deploy.md`](deploy.md) — redeploy after unarchiving.
