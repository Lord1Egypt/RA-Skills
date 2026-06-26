---
name: deploy-run-assert
description: One-shot validate → deploy → run --expect-status success.
user-invocable: false
---

# deploy-run-assert

## When

Verify a workflow end-to-end in a single call after authoring or modifying it.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy_run_assert.py --env <env> --workflow-key <key> [--payload '{"x":1}'] [--timeout 30] [--no-activate]
```

## Side effects

Orchestrates four subprocesses in sequence:

1. `hydrate.py`
2. `validate.py --source built`
3. `deploy.py`
4. `run.py --expect-status success`

On any step's non-zero exit, the composite exits with that step's code and prints `FAIL: stage=<n> exit=<code>` on stderr so the failure point is immediately legible.

The single-purpose helpers (`validate.py`, `deploy.py`, `run.py`) remain available for callers that want finer control. Both forms are documented in `skills/patterns/validate-deploy.md`.
