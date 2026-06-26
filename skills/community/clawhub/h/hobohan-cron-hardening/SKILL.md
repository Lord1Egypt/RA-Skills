---
name: cron-hardening
version: 1.0.0
description: "Guidelines for reliable OpenClaw cron jobs: model pinning, absolute paths, timeouts, delivery config, and error recovery."
allowed-tools: [cron]
---

# Cron Hardening

Reliable cron config learned through repeated failures. Follow these rules for every new cron.

## 1. PIN the model

**Every cron that delivers to the user** must explicitly set a fast model. The global default can get stuck on model resolution (MiniMax cold-start especially).

```json
"model": "deepseek/deepseek-v4-flash"
```

Time-sensitive crons that need pinning:
- Expense check-ins (10am, 1:30pm, 10pm)
- Expense sync (9:30am)
- News briefings (7:30am, 3pm, 10pm)
- Investment check-in (Sat 10am) and sync (Sat 11am)
- Transport check-in (9am)

Non-time-sensitive crons (dashboard, backup, security audit) can use default model — delay is harmless.

## 2. Absolute paths only

Cron agentTurn payloads run in an isolated context. They cannot `cd` to the workspace first. Every command MUST use absolute paths.

**WRONG:**
```
cd /workspace && python3 scripts/sync.py
```

**RIGHT:**
```
/usr/bin/python3 /home/hobopi/.openclaw/workspace/scripts/sync-ledger-to-sheet.py
```

Preflight checks reject `cd && python3` chains.

## 3. Timeouts

| Cron type | Timeout | Reason |
|-----------|---------|--------|
| Expense check-in | 300s (600s for 10pm) | May wait for Hobo reply |
| News briefing | 600s | Web search + curation takes time |
| Expense sync | 60s | Quick script, just needs to run |
| Investment sync | 600s | Reads all ledger files |
| Dashboard gen | 180s | Runs 3 scripts in sequence |
| Token tracker | 300s | Heavy usage data parsing |
| Transport check-in | 600s | Previous-day ask, may wait |
| Backup | 300s | tar + gzip |
| Security audit | 600s | Full healthcheck |

## 4. Delivery config

For crons that deliver to Telegram, use explicit delivery:

```json
"delivery": {
  "mode": "announce",
  "channel": "telegram",
  "to": "telegram:37134287"
}
```

`mode: "none"` for crons that don't need to notify the user (dashboard updates, token tracking).

## 5. Failure recovery

- Check `lastRunStatus` and `consecutiveErrors` on cron status
- `lastDiagnostics` shows the error phase: `model-call-started` = model resolution timeout
- Common fixes: pin model, bump timeout, check absolute paths
- After fixing, next scheduled run uses new config (no manual trigger needed)

## 6. maxConcurrentRuns

Set `cron.maxConcurrentRuns` in `openclaw.json` when multiple crons fire simultaneously:

```json
"cron": { "maxConcurrentRuns": 2 }
```

Prevents Sunday 5am clash (security audit + hourly dashboard + expense check-in).

## 7. Failure alerts

```json
"failureAlert": {
  "after": 2,
  "mode": "announce",
  "channel": "telegram",
  "to": "telegram:37134287"
}
```

Notifies Hobo after 2 consecutive failures. Default enabled.
