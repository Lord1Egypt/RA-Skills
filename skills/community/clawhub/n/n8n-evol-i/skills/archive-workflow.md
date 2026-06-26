---
name: archive-workflow
description: Archive a deployed workflow on its env's n8n instance via POST /api/v1/workflows/{id}/archive.
user-invocable: false
---

# archive-workflow

## When

A deployed workflow should be retired but not deleted — archive it. Archived workflows are hidden from the active list, are deactivated, and reject all updates (`PUT` returns `400 {"message":"Cannot update an archived workflow."}`) until unarchived. Use [`unarchive-workflow.md`](unarchive-workflow.md) to restore.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/archive.py \
  --env <env> \
  --workflow-key <wf>
```

## Side effects

- Resolves `<wf>` to its workflow id via `<workspace>/n8n-config/<env>.yml.workflows.<wf>.id`.
- Calls `POST /api/v1/workflows/<id>/archive` against the env's n8n instance.
- Idempotent: archiving an already-archived workflow returns `200`.

The workflow id mapping in env YAML is unchanged — the workflow still exists and can be unarchived in place. Only the live n8n instance state flips.

## Notes

- The `/archive` endpoint was added to n8n's public REST API in 2026-Q1. Older n8n versions (pre-Q1-2026) reject the call with `404`. Verify your instance version before scripting against it.
- Archive supersedes `deactivate` for the "permanently retire" intent. Use `deactivate-single-workflow-in-env.md` instead if you only want to pause triggers temporarily.

## See also

- [`unarchive-workflow.md`](unarchive-workflow.md) — restore an archived workflow.
- [`deactivate-single-workflow-in-env.md`](deactivate-single-workflow-in-env.md) — pause triggers without archiving.
