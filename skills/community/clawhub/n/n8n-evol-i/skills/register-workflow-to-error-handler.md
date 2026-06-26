---
name: register-workflow-to-error-handler
description: Wire a workflow's settings.errorWorkflow to point at an existing error handler.
user-invocable: false
---

# register-workflow-to-error-handler

## When

A workflow needs `settings.errorWorkflow` to route on-error to an existing Error Trigger workflow.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/register_error_handler.py --workflow-key <wf> --handler-key <handler>
```

## Side effects

- Edits `<workspace>/n8n-workflows-template/<wf>.template.json` so its `settings.errorWorkflow` becomes the literal placeholder `"{{@env:workflows.<handler>.id}}"` (no `=` prefix — n8n expects a literal id).
- Updates `<workspace>/n8n-config/common.yml.error_source_to_handler[<wf>] = <handler>` so `run.py` knows about the source/handler pairing for indirect dispatch.

Aborts if `<handler-key>` is not registered in any env's YAML.

## Pattern

For Error Trigger workflows that have no Webhook entry, see `skills/patterns/error-handling.md` and the indirect-dispatch behavior in `run.md`.

## See also

- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `settings.errorWorkflow` field shape (literal id, no `=` prefix) via Context7 before assuming training-data recall is current.
