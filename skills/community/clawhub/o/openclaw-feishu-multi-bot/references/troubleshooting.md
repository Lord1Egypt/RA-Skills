# Troubleshooting

## Diagnostic Flowchart

```
Bot not responding?
  │
  ├── Is the Feishu app published (not draft)? → Publish it
  │
  ├── Is the gateway running? → openclaw gateway status
  │
  ├── Are there errors in logs? → openclaw logs --channel feishu
  │
  ├── Is the accountId consistent in all 3 places? → Check channels/bindings/agents
  │
  ├── Is the binding type "route"? → Fix to "route"
  │
  └── Is the bot added to the target group? → Add bot as group member
```

## Issue: Gateway Startup Failure

**Symptom**: `openclaw gateway restart` fails or gateway exits immediately.

**Common causes**:

| Cause | Check | Fix |
|-------|-------|-----|
| Invalid binding type | `bindings[].type` is not `"route"` | Change to `"route"` |
| Malformed JSON | Syntax error in openclaw.json | `python3 -c "import json; json.load(open('openclaw.json'))"` |
| Duplicate accountId | Same accountId used for two agents | Rename one of them |
| Missing appSecret | Account entry without appSecret | Add the secret from Feishu console |

## Issue: Bot Not Responding

**Symptom**: Message sent to Feishu bot, no response.

**Diagnostic steps**:

1. **Check app status**: Log in to [open.feishu.cn/app](https://open.feishu.cn/app). Is the app published and online? Draft apps silently drop all messages.

2. **Check credentials**: Verify `appId` and `appSecret` match the Feishu developer console exactly. Watch for leading/trailing spaces in the JSON.

3. **Check gateway logs**:
   ```bash
   openclaw logs --channel feishu
   ```
   Look for connection errors or authentication failures.

4. **Check agent registration**:
   ```bash
   openclaw agents list --bindings
   ```
   Confirm the target agent appears in the list with the correct binding.

5. **Check group membership**: If messaging in a group, confirm the bot has been added to that group as a member.

## Issue: Message Routed to Wrong Agent

**Symptom**: Bot A receives messages meant for Bot B, or vice versa.

**Cause**: accountId mismatch between `channels.feishu.accounts` and `bindings`.

**Fix**:
```bash
# Find all accountId references
grep -n "accountId" ~/.openclaw/openclaw.json

# Find all agent references in accounts
grep -n '"agent"' ~/.openclaw/openclaw.json
```

Verify each accountId maps to the correct agentId in both `channels.feishu.accounts[].agent` and `bindings[].agentId`.

## Issue: Sub-Agent Spawn Permission Error

**Symptom**: `sessions_spawn` fails with "agentId not allowed" or similar.

**Causes and fixes**:

| Cause | Fix |
|-------|-----|
| Agent ID not in `allowAgents` | Add it to orchestrator's `subagents.allowAgents` |
| Agent not in `agents.list` | Add the agent definition |
| `agentToAgent.enabled: true` | Set to `false` and restart gateway (Bug #5813) |
| Stale gateway state | `pkill` gateway process, then `openclaw gateway restart` |

## Issue: agentToAgent Conflicts

**Symptom**: All sub-agents show token usage = 0 and never execute.

**Cause**: `agentToAgent.enabled: true` in openclaw.json conflicts with `sessions_spawn`. Known bug (#5813, 2026-02).

**Fix**:
```json
{
  "tools": {
    "agentToAgent": {
      "enabled": false
    }
  }
}
```

Then full restart:
```bash
pkill -f openclaw
openclaw gateway restart
```

**Rule**: Unless you have a specific need for Agent-to-Agent direct messaging, keep `agentToAgent` disabled.

## Issue: Agent Registers But `openclaw agents list` Only Shows "main"

**Symptom**: You added agents to `agents.list` in openclaw.json, but `openclaw agents list` returns only `["main"]`.

**Cause**: Possible version regression or stale process state.

**Fix**:
1. Kill all gateway processes: `pkill -f openclaw`
2. Verify openclaw.json is saved correctly
3. Restart: `openclaw gateway restart`
4. Check: `openclaw agents list`

If still only "main", check if the JSON structure is correct (agents must be under `agents.list`, not `agents.agents` or other paths).

## Useful Commands

```bash
# Full health check
openclaw doctor

# Auto-fix detected issues
openclaw doctor --fix

# Restart gateway (graceful)
openclaw gateway restart

# Force kill and restart
pkill -f openclaw && sleep 2 && openclaw gateway restart

# Check gateway status
openclaw gateway status

# View Feishu-specific logs
openclaw logs --channel feishu

# List all agents with bindings
openclaw agents list --bindings

# Verify configuration without restarting
openclaw doctor
```

## Prevention Checklist

Before every gateway restart after config changes:

- [ ] JSON syntax valid (`python3 -c "import json; json.load(open('openclaw.json'))"`)
- [ ] Every new agent ID added to `agents.list`
- [ ] Every new agent ID added to orchestrator's `allowAgents`
- [ ] Every new Feishu account has matching binding with `type: "route"`
- [ ] accountId consistent across channels/bindings/agents
- [ ] `agentToAgent.enabled` is `false`
- [ ] All Feishu apps are published (not draft)
