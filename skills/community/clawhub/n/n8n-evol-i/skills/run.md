---
description: Fire a webhook-triggered workflow and assert terminal status.
---

# run

## When

Verify a deployed workflow actually runs.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/run.py --env <env> --workflow-key <key> [--payload '{"x":1}'] [--expect-status success|error] [--timeout 30]
```

## Side effects

1. Detects the workflow's webhook node, POSTs to `<base>/webhook/<path>` (and `<base>/webhook-test/<path>` fallback).
2. Polls `/api/v1/executions` for a record started after the POST.
3. Polls `/executions/<id>?includeData=true` until terminal.
4. Asserts status matches `--expect-status` if given. Returns non-zero on mismatch / timeout.

## Indirect dispatch (Error Trigger handlers)

When the agent asks to run a workflow that's listed as a *handler* in `n8n-config/common.yml.error_source_to_handler`, `run.py` reverse-looks-up the paired source key, fires the source instead, and polls the handler's executions. This is needed because Error Trigger workflows have no Webhook entry to fire directly.

The mapping is configured in `<workspace>/n8n-config/common.yml`:

```yaml
error_source_to_handler:
  some_source_workflow: some_handler_workflow
```

`register-workflow-to-error-handler.md` writes to this map automatically.

## See also

- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `GET /executions` and `/executions/{id}` shapes via Context7 before relying on training-data recall (status enum, `includeData`, pagination).
