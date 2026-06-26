# Permission Guard

Requests temporary permission for sensitive operations from a human approver.

## Tools

- **`pvm_request`** — Request a permission grant
- **`pvm_status`** — Check active grants for an agent
- **`pvm_revoke`** — Revoke a grant early
- **`pvm_log`** — View the audit log

## Usage

### Request a grant

```
pvm_request scope="delete:/Users/soup/flume/data/backups" reason="cleaning old backups" duration=5
```

### Check active grants

```
pvm_status agent_id="coder"
```

### Revoke a grant

```
pvm_revoke grant_id="grant_abc123"
```

### View audit log

```
pvm_log --agent coder --limit 20
```

## Configuration

Set `PVM_CONFIG` env var or pass `--config /path/to/config.yaml`.

Requires `config.yaml` with:
- `vault.db_path` — SQLite database path
- `vault.default_ttl_minutes` — Default grant TTL (default: 30)
- `channels.*` — At least one enabled notification channel

## How it works

1. Agent calls `pvm request` with scope and reason
2. PVM notifies all configured approvers (iMessage, Email, Discord, Telegram, Slack)
3. Approver approves via any channel
4. Grant is created in SQLite with TTL
5. Agent's `safe-*` wrappers check vault and execute if grant active

## Error codes

- `0` — Success / grant found / operation allowed
- `1` — Grant not found / denied / revoked / expired
- `2` — Configuration or usage error
