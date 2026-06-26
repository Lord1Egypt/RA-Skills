---
description: Run unit tests over JS used in n8n Code nodes and/or Python used in cloud functions.
---

# test

## When

Before deploys. After edits that touch `n8n-functions/` or `cloud-functions/`.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/test_functions.py --target {n8n|cloud|all} [--filter <name>]
```

## Side effects

- Discovers tests under `<workspace>/n8n-functions-tests/*.test.js` (runs each via `node --test`, or via `npm test` if a `package.json` is present).
- Discovers tests under `<workspace>/cloud-functions-tests/test_*.py` (runs `pytest`).
- With `--target all`, runs both.
- Prints a per-target summary.
- Returns 0 only on all-green; non-zero otherwise.

## Reshape

Test directory paths can be overridden via `<workspace>/n8n-config/common.yml`:

```yaml
workspace_layout:
  n8n_functions_tests_dir: tests/n8n
  cloud_functions_tests_dir: tests/cloud
```
