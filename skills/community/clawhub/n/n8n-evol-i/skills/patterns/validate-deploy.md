---
name: pattern-validate-deploy
description: The canonical 5-step validate-before-deploy loop — REST-only.
user-invocable: false
---

# Pattern: validate-deploy

Before declaring a workflow shipped, run this loop. Both forms below produce the same result; pick by ergonomics.

## The 5 steps

| # | Step | What it catches |
|---|---|---|
| 1 | **hydrate** (`hydrate.py`) | Missing referenced files, residual placeholders, malformed JSON. |
| 2 | **validate** (`validate.py --source built`) | Top-level shape violations, missing `name`/`type`/`parameters` on nodes. |
| 3 | **deploy** (`deploy.py`) | Per-env auth, n8n-side schema rejections (e.g. missing required parameter), credential-name mismatch on activate. |
| 4 | **run** (`run.py --expect-status success`) | Runtime errors that only surface during execution: bad expressions, missing data, sub-workflow not published. |
| 5 | **wait_for_execution** (built into `run.py`) | Polls `/executions/<id>` until terminal — so you don't accept a "running" status as success. |

`run.py` does steps 4+5 atomically.

## Composite (one-liner)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy_run_assert.py --env <env> --workflow-key <key> [--payload <json>] [--timeout 30]
```

This subprocesses `validate.py → deploy.py → run.py` and exits with the first failing stage's exit code, printing `FAIL: stage=<n> exit=<code>` on stderr.

## Unit chain (finer control)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/hydrate.py --env <env> --workflow-key <key>
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/validate.py --env <env> --workflow-key <key> --source built
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy.py --env <env> --workflow-key <key>
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/run.py --env <env> --workflow-key <key> --expect-status success --timeout 30
```

Use the unit chain when you need to interleave other commands (e.g. activate sub-workflows manually) or when you want to keep a workflow inactive after deploy.

## Polling, not accepting "running"

`run.py` deliberately does not return on `running` status — it polls until the execution is `finished: true` and reports the actual terminal status. This catches workflows that hang in mid-execution.
