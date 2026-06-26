---
name: openclaw-config
description: Use when editing openclaw.json, adding or changing config keys, troubleshooting a gateway crash after a config change, validating config before restart, or recovering from an unknown key error. Also use when asked to set tools.sessions, agents, channels, compaction, or any gateway setting.
---

# openclaw-config

Safe protocol for editing `~/.openclaw/openclaw.json`. Wrong key names silently break the gateway — this skill prevents that.

## The Protocol (Always Follow This Order)

### 1. Backup first
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M)
```

### 2. Verify the key exists in source before adding it
Never guess a config key name. Check the source:
```bash
# Replace KEY with the key you're about to add (e.g. "visibility", "agentToAgent")
grep -r "cfg\." ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/dist/*.js \
  | grep -o '"[a-zA-Z.]*KEY[a-zA-Z.]*"' | sort -u | head -10
```

Or check the full path:
```bash
grep -r "tools\.sessions\." ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/dist/*.js \
  | grep -o '"[a-z.]*"' | sort -u
```

If the key doesn't appear in source → **it doesn't exist, don't add it.**

### 3. Edit the config
Use Python to safely read/modify/write (avoids JSON syntax errors):
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
cfg = json.load(sys.stdin)

# Make your change here, e.g.:
# cfg['tools']['sessions']['visibility'] = 'all'

with open('$HOME/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
print('Done')
"
```

### 4. Validate before restarting
```bash
openclaw gateway status 2>&1 | grep -i "unknown\|invalid\|error"
```

Doctor will flag unknown keys. If you see any → restore from backup, don't restart.

### 5. Restart only when clean
```bash
openclaw gateway restart
```

---

## Recovery: If the Gateway Breaks

```bash
# List backups
ls -lt ~/.openclaw/openclaw.json.bak-* | head -5

# Restore most recent
cp ~/.openclaw/openclaw.json.bak-YYYYMMDD-HHMM ~/.openclaw/openclaw.json

# Restart
openclaw gateway restart
```

---

## Common Keys + Correct Names

| What you want | Correct key path | Valid values |
|---|---|---|
| Cross-agent session visibility | `tools.sessions.visibility` | `self` `tree` `agent` `all` |
| Agent-to-agent messaging | `tools.agentToAgent.enabled` | `true` / `false` |
| Compaction trigger threshold | `agents.defaults.compaction.maxHistoryShare` | `0.0`–`1.0` |
| Compaction mode | `agents.defaults.compaction.mode` | `default` `safeguard` |
| Reserve tokens before compaction | `agents.defaults.compaction.reserveTokens` | integer |
| Primary model | `agents.defaults.model.primary` | `provider/model-id` |
| Tool allow/deny | `tools.allow` / `tools.deny` | array of tool names |

---

## What NOT to Do

- ❌ Guessing key names — always verify in source first
- ❌ Direct string editing of the JSON file — use Python to avoid syntax errors
- ❌ Restarting before validating — doctor catches unknown keys
- ❌ Skipping backup — a 5-second backup saves a 10-minute recovery

---

## Why This Matters

A single unknown key in `openclaw.json` makes the gateway refuse to start. There's no warning — it just fails. The backup + source verification + doctor flow takes 30 seconds and prevents complete system outages.

Real example: `tools.sessions.scope` (doesn't exist) vs `tools.sessions.visibility` (correct) — one character difference, gateway down.
