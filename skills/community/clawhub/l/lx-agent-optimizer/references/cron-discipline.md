# Cron Discipline

## The Golden Rule
> If the cron prompt needs > 200 tokens to explain, convert it to a script.

## Script-first pattern

### Structure
```
skills/my-skill/
├── SKILL.md
└── scripts/
    └── my_job.py    ← all logic here
```

### Cron payload (short)
```json
{
  "message": "Run script via nodes.run:\n[\"/usr/bin/python3\", \"/path/to/scripts/my_job.py\"]\n\nIf output: send to user.\nIf no output: end silently.",
  "timeoutSeconds": 60,
  "model": "qwen-plus"
}
```

## Script design rules

### Silent on success
```python
# Good: no output when nothing to report
if not new_events:
    exit(0)

# Good: output only when something happened
print(f"⚽ AC Milan won 3-2")
```

### Validate data sources first
Before embedding any URL in a cron job:
```bash
curl -s "https://api.example.com/data" | head -5
# Confirm: returns real data, not HTML shell, not 403
```

### State file for idempotency
```python
# Track what was last sent to avoid duplicates
state_path = "/tmp/my_job_state.json"
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
last_sent = state.get("last_id", "")

if new_id == last_sent:
    exit(0)  # already sent this

# ... send ...
json.dump({"last_id": new_id}, open(state_path, "w"))
```

## Pre-ship checklist
- [ ] Logic is in `.py` script, not in prompt
- [ ] Script tested locally: `python3 script.py`
- [ ] Silent on no-op (exit 0, no output)
- [ ] Output < 300 chars for routine cases
- [ ] Model: cheapest tier that works
- [ ] Timeout: 60s for simple, 120s for web fetch, never > 180s
- [ ] File writes in main session, not work agent
- [ ] Data source validated with curl

## Common timeout guide
| Task | Timeout |
|------|---------|
| Local script (no network) | 30s |
| Single API call | 60s |
| Web fetch + parse | 120s |
| Multi-step with LLM reasoning | 120s |
| Never | > 180s |

## Delivery rules
- `NO_REPLY` / no output = no message sent ✅
- Alert only on: new data, errors, anomalies
- Never send "everything is fine" messages
- Success = silence

## Cron error classification

When a cron shows `consecutiveErrors > 0`, **do not assume the root cause immediately**. Classify first:

| Type | Typical signal | Meaning | Default action |
|------|----------------|---------|----------------|
| **Delivery failure** | `Message failed`, `sendMessage failed`, `not-delivered`, `deliveryStatus = unknown` | The job logic may have succeeded, but message delivery failed | Verify current channel health with a **live probe** before fallback alerts or remediation |
| **Task failure** | script exception, parse failure, bad prompt/tool call, non-zero exit | The workflow itself broke | Alert user briefly if user-facing job; fix logic/script path |
| **Node failure** | `Nodes failed`, remote host unavailable, permission/runtime error on node | The remote machine or node bridge failed | Alert user only if task matters now; retry later or repair node path |

**Rule:** delivery failure ≠ task failure. A report may already exist even when the final send step failed.

## Channel health check pattern

For "is channel X alive?" cron tasks, always use a **real-time probe**, never stale log scanning:

```
# ✅ Correct pattern
Attempt to send silent message to channel
  → success: exit silently
  → failure: remediate (e.g., reconnect VPN) + notify via fallback channel

# ❌ Wrong pattern
Scan cron job lastError / deliveryStatus history
  → if found → alert
  (Problem: old errors look like current failures)
```

**Why it matters:** Historical cron errors may be days old. A channel that failed yesterday might be healthy now. Real-time probe catches the ground truth.

**Heartbeat add-on rule:** if heartbeat notices Telegram-related cron errors, treat that as an anomaly hint only. Before sending DingTalk fallback or triggering recovery, run a live Telegram probe first whenever the environment allows it.

## Reminder disable: what to check

When the user asks to remove or disable a reminder/feature:
1. Check `cron list` for matching job names
2. **Also** check `HEARTBEAT.md` — some features live there, not in cron jobs
3. Confirm both sides are cleaned up before responding "done"

## Heartbeat cron-scan rule

Heartbeat is allowed to scan cron state for anomalies, but should follow this sequence:
1. Spot jobs with `consecutiveErrors > 0`
2. Classify them as **delivery / task / node**
3. Only escalate the ones that matter now
4. For channel-related delivery failures, **verify with a live probe before saying the channel is down**
5. Report only the current actionable conclusion, not a dump of historical run noise
