# Architecture

## Overview

PVM (Permission Vending Machine) is a local approval system for AI agent operations. It gates sensitive commands behind human-approved, time-limited grants persisted in SQLite.

```
Agent                  PVM Core              Channels           Human
  |                       |                     |                 |
  |-- request(scope) --->|                     |                 |
  |                      |-- notify all ------>|                 |
  |                      |<-- results ---------|<-- notification |
  |                      |                     |                 |
  |<-- token ------------|                     |                 |
  |                      |<--------- approve --|<----------------
  |                      |                     |                 |
  |                      | create_grant()      |                 |
  |                      | log_audit(GRANTED)  |                 |
  |<-- GRANTED ---------|                     |                 |
  |                      |                     |                 |
  | safe-rm /path        |                     |                 |
  |-- check_grant() --->|                     |                 |
  |<-- True ------------|                     |                 |
  |                      | log_audit(SUCCESS)  |                 |
  |-- exec rm /path --> |                     |                 |
```

## Components

### `pvm.vault.Vault`

SQLite-backed store for grants and audit entries.

- **Grants table**: `grant_id`, `agent_id`, `scope`, `scope_type`, `reason`, `issued_at`, `expires_at`, `revoked`, `approved_by`
- **Audit table**: `entry_id`, `timestamp`, `entry_type`, `agent_id`, `scope`, `decision`, `details`, `grant_id`

Key methods:
- `create_grant()` — issue a new grant, log APPROVAL
- `check_grant(agent_id, scope)` — exact match check
- `check_grant_glob(agent_id, scope, scope_type)` — path prefix or exact match
- `revoke_grant(grant_id)` — mark revoked, log REVOKED
- `get_active_grants(agent_id)` — list valid grants
- `log_audit()` — append to audit trail

### `pvm.notifier.Notifier`

Multicast dispatcher. Loads `config.yaml`, instantiates enabled channels, sends to all in parallel. Failures on one channel don't block others.

### Channels

| Channel | Protocol | API |
|---------|----------|-----|
| Sendblue | HTTPS POST | `api.sendblue.co/api/send-sms` |
| Email | SMTP/SMTPS | Python `smtplib` |
| Discord | Webhook | `discord.com/api/webhooks/...` |
| Telegram | Bot API | `api.telegram.org/bot{token}/sendMessage` |
| Slack | Webhook | `hooks.slack.com/services/...` |

### `pvm.approval.PollingPoller`

Polls vault for grant creation within a timeout window. Calls `on_approve` / `on_deny` callbacks on resolution.

### `pvm.approval.CallbackHandler`

Handles incoming webhook callbacks (Discord interactions, custom HTTP endpoints). Verifies signatures, creates grants or logs denials.

### Wrappers (`safe-rm`, `safe-git-push`, `safe-trash`)

Shell scripts that:
1. Parse arguments to determine scope
2. Call Python inline to check vault
3. If no grant: print denial + request instructions, exit 1
4. If granted: log SUCCESS to audit, exec the real command

## Data Flow

```
PermissionRequest.create()
    ↓
Notifier.notify_approvers()  →  Channel.send() × N
    ↓
ApprovalPoller.wait_for_decision()
    ↓
Vault.create_grant()  ←  CallbackHandler.handle_approval()
    ↓
Vault.check_grant()  ←  safe-* wrappers
    ↓
real command execution + Vault.log_audit(SUCCESS)
```

## Thread Safety

`Vault` uses `threading.local()` for connection-per-thread. Concurrent reads and writes from multiple agents are safe.
