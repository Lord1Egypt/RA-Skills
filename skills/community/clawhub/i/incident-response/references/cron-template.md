# Cron Job Template for Incident Monitoring

## When to Use

Set a monitoring cron after every incident. Run until user says "good enough" — minimum 7 days for minor incidents, 30 days for recurring/systemic ones.

## Schedule Guidelines

| Severity | Frequency | Example |
|----------|-----------|---------|
| High (repeated, systemic) | Every 6h | Binding loss, gateway crash pattern |
| Medium (single incident, complex) | Every 24h | Config key disappearance |
| Low (one-off, simple) | Every 48h | Session routing issue |

## Cron Job Prompt Template

```
You are doing a [NAME] integrity check for the [SYSTEM] system.

## What to Check
1. [Specific command/check]: expected = [BASELINE_VALUE]
2. [Guard check]: verify [GUARD] is still in [FILE]
3. [Git log]: ssh [HOST] "cd ~/.openclaw && git log --since='25 hours ago' --oneline"

## Decision Tree
- If [METRIC] == [BASELINE]: report OK
- If [METRIC] < [BASELINE]:
  a. Run 5 Whys: find what's missing, check git log for who, check session logs for which tool call
  b. Restore: [RESTORE_COMMAND]
  c. Check if guard failed: [GUARD_CHECK]
  d. If guard failed, strengthen it: [HOW_TO_STRENGTHEN]
  e. Commit prevention update to git

## Auto-escalate Rule
If same fix is needed 3+ days in a row: upgrade prevention measure from SOUL.md rule → config-validate.sh hard guard.

## Report Format
Send to sessions_send(sessionKey='<your-session-key>'):
'[Daily CHECK_NAME] [SYSTEM]: [METRIC]/[BASELINE] | Guard: OK/MISSING | Changes: [git summary] | Status: OK/FIXED([what])'

If issue found and fixed, include: what was missing, who caused it, what was restored, what prevention was updated.
```

## Real Example (Titan Binding Integrity Check)

Cron job ID: `b8c86094-4b14-42bc-8d59-23f78598bb5b`

- Schedule: every 24h
- Baseline: 12 bindings
- Guard: `BLOCKED: binding count` in `config-validate.sh`
- Restore: git show last good state → python3 restore script → config-validate.sh --merge
- Report: Signal/Telegram/Discord channel (configure your session key)

## Stopping Monitoring

Only stop when:
1. User explicitly says "stop monitoring" or "it's good enough"
2. OR: N consecutive clean checks with no incidents (N = 7 for minor, 30 for systemic)

Never self-terminate monitoring. The cron job should report its own run count and ask user for confirmation when approaching the suggested stop date.
