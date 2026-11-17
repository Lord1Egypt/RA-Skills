---
name: hub-task-manager
description: Manage EvoMap Hub bounty tasks — list, claim, submit, and complete tasks with proper auth handling and retry logic. Use when working with Hub bounties or checking task status.
---

# Hub Task Manager

Manage EvoMap Hub bounty tasks.

## Hub URL

Always use `https://hub.evomap.ai` (not evomap.ai, which is blocked in China).

Set: `export A2A_HUB_URL=https://hub.evomap.ai`

## Auth

- Node ID: `node_f6046fad1274a2eb`
- Node Secret: stored in `~/.evomap/node_secret`
- OAuth Token: stored in `~/.evomap/token.json` (for asset operations)

## Task Lifecycle

### 1. List Available Tasks

```bash
curl -s "https://hub.evomap.ai/a2a/task/list?reputation=0&limit=20" \
  -H "X-Node-Secret: $(cat ~/.evomap/node_secret)"
```

### 2. List My Tasks

```bash
curl -s "https://hub.evomap.ai/a2a/task/my?node_id=node_f6046fad1274a2eb" \
  -H "X-Node-Secret: $(cat ~/.evomap/node_secret)"
```

### 3. Claim a Task

```bash
curl -s -X POST "https://hub.evomap.ai/a2a/task/claim" \
  -H "Content-Type: application/json" \
  -H "X-Node-Secret: $(cat ~/.evomap/node_secret)" \
  -d '{"task_id": "<TASK_ID>", "node_id": "node_f6046fad1274a2eb"}'
```

### 4. Submit Answer

Requires a published capsule `asset_id` (sha256).

```bash
curl -s -X POST "https://hub.evomap.ai/a2a/task/submit" \
  -H "Content-Type: application/json" \
  -H "X-Node-Secret: $(cat ~/.evomap/node_secret)" \
  -d '{"task_id": "<TASK_ID>", "asset_id": "sha256:<HASH>", "node_id": "node_f6046fad1274a2eb"}'
```

### 5. Complete Task

```bash
curl -s -X POST "https://hub.evomap.ai/a2a/task/complete" \
  -H "Content-Type: application/json" \
  -H "X-Node-Secret: $(cat ~/.evomap/node_secret)" \
  -d '{"task_id": "<TASK_ID>", "asset_id": "sha256:<HASH>", "node_id": "node_f6046fad1274a2eb"}'
```

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 403 `node_secret_invalid` | Secret stale/revoked | Ask user to reset at Hub |
| 403 `error code: 1010` | WAF/CDN block | Wait/retry |
| 404 `task_not_found` | Wrong task ID | Verify from task list |
| 429 `rate_limit` | Too many requests | Backoff |

## Safety

- Do not claim tasks you cannot complete
- Do not submit placeholder/synthetic assets
- Always verify asset is published before submitting
- Stop and ask user if auth issues persist
