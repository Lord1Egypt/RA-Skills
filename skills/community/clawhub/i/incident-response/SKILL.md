---
name: incident-response
version: 1.0.0
description: Structured incident response for OpenClaw system failures. Use when a user reports something broken, missing, changed, or misbehaving — config loss, agent routing failures, binding changes, gateway crashes, missing settings, or any system regression. Follows a strict 7-phase loop: Triage → Evidence → 5 Whys → Restore → Prevent → Monitor → Document. Triggers on: "investigate", "why did X stop working", "something changed", "bindings lost", "gateway down", "gateway crashed", "setting disappeared", "something disappeared", "fix this", "who changed X", "root cause", "audit", "misconfigured", "agent not responding".
owner_agent: any agent with exec access to the affected system
---

# Incident Response

Seven phases, in order. Never skip. Never assume — follow the evidence.

**Outputs produced by this skill:**
- Root cause statement (5 Whys chain with evidence citations)
- Restore confirmation (what was restored, verified working)
- Prevention commit (git commit hash of guard/rule added)
- Monitoring cron (job ID + schedule)
- Learning entry (appended to `~/.openclaw/learnings/rules.md`)

## Phase 0: Triage (2 min)

**Check current state FIRST before investigating history.**

```bash
# Is it actually broken right now?
openclaw status
ssh "<remote-host>" "launchctl list | grep openclaw"
# Test with correct protocol (check source: HTTP vs HTTPS?)
```

If currently working → report "recovered, investigating cause." If still broken → proceed.

## Phase 1: Evidence Collection

Gather hard evidence from four sources:

### 1a. Config backups timeline
```bash
# See binding/setting counts over time
ssh "<remote-host>" "python3 << 'EOF'
import json, glob, os
for f in sorted(glob.glob('~/.openclaw/config-backups/openclaw-*.json'), key=os.path.getmtime):
    d = json.load(open(f))
    import datetime
    dt = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
    # Customize: bindings, agents, channels, etc.
    count = len(d.get('bindings', []))
    ids = [b.get('agentId') for b in d.get('bindings', [])]
    print(f'{dt} [{count}] {ids}')
EOF"
```

### 1b. Git audit trail
```bash
ssh "<remote-host>" "cd ~/.openclaw && git log --oneline -20"
ssh "<remote-host>" "cd ~/.openclaw && git diff <commit-a> <commit-b> -- openclaw.json | grep '^[+-]' | grep -v '^---\|^+++'"
```

### 1c. Session logs (who did what)
```bash
# Find sessions that touched the broken config key
ssh "<remote-host>" "rg -rl 'keyword' ~/.openclaw/agents/*/sessions/*.jsonl | head -5"

# Extract tool calls from a session
ssh "<remote-host>" "python3 << 'EOF'
import json
for line in open('SESSION.jsonl'):
    obj = json.loads(line)
    if obj.get('type') != 'message': continue
    for block in obj.get('message',{}).get('content',[]):
        if block.get('type') == 'toolCall' and block.get('name') in ['Write','Edit','gateway','exec']:
            print(obj['timestamp'], block['name'], str(block.get('input',''))[:200])
EOF"
```

### 1d. Config backup diff (find the exact moment of change)
```bash
# Compare before/after a suspicious backup
python3 -c "
import json
a = json.load(open('backup-before.json'))
b = json.load(open('backup-after.json'))
# Compare specific field
print('Before:', a.get('bindings'))
print('After:', b.get('bindings'))
"
```

**Stop and document:** Who changed what, when, which session, which tool call.

## Phase 2: 5 Whys Analysis

Write each "why" as a statement of fact backed by evidence from Phase 1.

```
Why 1: [Symptom] — e.g. "Bindings dropped from 17 to 1"
  Evidence: backup timestamp + count

Why 2: [Immediate cause] — e.g. "A full config replacement was written at 09:38 PST"
  Evidence: backup mtime + content diff

Why 3: [Mechanism] — e.g. "the agent wrote a new config from scratch, not from current config"
  Evidence: session log tool call + content

Why 4: [System gap] — e.g. "config-validate.sh --merge had no guard against binding count drops"
  Evidence: script inspection showing no such check

Why 5: [Root cause] — e.g. "No automated detection existed between when the config was written and the next user report"
  Evidence: no monitoring cron, no git at the time
```

**Rule:** Every "why" must cite a specific file, log entry, timestamp, or command output. No assumptions.

## Phase 3: Restore

Restore to last known-good state using backup timeline from Phase 1.

```bash
# Restore specific fields (always merge, never replace)
PATCH=$(python3 -c "
import json
good = json.load(open('/path/to/good-backup.json'))
patch = {'bindings': good['bindings']}  # customize field
print(json.dumps(patch))
")
echo "$PATCH" | ssh "<remote-host>" "~/.openclaw/scripts/config-validate.sh --merge"

# Restart gateway
ssh "<remote-host>" "launchctl stop ai.openclaw.gateway && sleep 2 && launchctl start ai.openclaw.gateway"
ssh "<remote-host>" "launchctl list | grep ai.openclaw.gateway"  # verify exit code 0
```

**Verify restore:** Check that the restored value matches the good backup. Re-run the user's original failing action.

## Phase 4: Prevention

Add guards proportional to the severity and recurrence risk. See `references/prevention-patterns.md` for full patterns. Quick reference:

**For config fields that must not decrease:**
Add guard to `config-validate.sh --merge` (see references for template)

**For agent behavior rules:**
Add to `~/.openclaw/agents/<id>/agent/SOUL.md` as a Hard Rule (HR-NNN)

**For recurring mistakes:**
Add to `~/.openclaw/learnings/rules.md` with category and date

**For schema validation gaps:**
Update `config-validate.sh` valid_keys list after verifying against DeepWiki

Always commit prevention changes to git:
```bash
ssh "<remote-host>" "cd ~/.openclaw && git add -A && git commit -m 'prevention: <what was added> after <incident>'"
```

## Phase 5: Monitor

Set a recurring cron job that runs until user confirms "good enough" (minimum 7 days, 30 days for recurring incidents).

```
Cron job structure:
- Schedule: every 24h (or every N hours for high-severity)
- Task: check specific metric → compare to baseline → if degraded: restore + 5-why → report
- Report channel: sessions_send to your preferred channel (Signal, Telegram, Discord)
- Auto-escalate: if same fix needed 3+ days in a row → upgrade prevention measure
- Termination: user explicitly says "stop monitoring" or N days without incident
```

See `references/cron-template.md` for the full cron job prompt template.

## Phase 6: Document

Write to `~/.openclaw/learnings/rules.md` if a Hard Rule should be added:
- Category: HR (Hard Rule, recurring) or SR (Soft Rule, first offense)
- Include: what triggered, what the rule is, date learned, why it matters

Update `MEMORY.md` with incident summary if it's systemic.

---

## Configuration

No persistent configuration required. Adapt the following to your environment:

| Variable | Description | Example |
|----------|-------------|---------|
| Remote host | SSH target for remote investigations | `<remote-host>` → your Titan/server hostname |
| Config backup path | Where OpenClaw stores automatic config backups | `~/.openclaw/config-backups/` |
| Session key | Your messaging session key for cron reports | `agent:main-signal:signal:<your-number>` |
| Learnings path | Where rules are persisted | `~/.openclaw/learnings/rules.md` |

See `references/cron-template.md` for full cron report configuration.


---

## Quick Diagnosis Checklists

See `references/checklists.md` for:
- Gateway crash checklist
- Binding loss checklist
- Config key disappeared checklist
- Agent routing wrong checklist
- Vector search not finding content checklist
