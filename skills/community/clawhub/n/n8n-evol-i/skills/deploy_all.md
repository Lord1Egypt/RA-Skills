---
description: Roll out an entire env in tier order.
---

# deploy_all

## When

Bulk deploy or initial deployment for an env.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/deploy_all.py --env <env> [--keep-active] [--continue-on-failure]
```

## Side effects

- Reads `<workspace>/n8n-config/deployment_order.yml`, walks tiers in alphabetical order (callees before callers).
- Calls `deploy.py --env <env> --workflow-key <k>` for each.
- With `--env dev` and without `--keep-active`, deactivates all after deploy (safety against test fires accidentally hitting real systems).
- Returns non-zero exit if any workflow failed (unless `--continue-on-failure`).
