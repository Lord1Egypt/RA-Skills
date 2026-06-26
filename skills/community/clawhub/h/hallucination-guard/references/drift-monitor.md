# Drift Detection Monitor

## Purpose

Detect when an autonomous agent enters a hallucination loop — claiming to do work without physical execution.

## When to Deploy

- Coding agents running >15 minutes
- Research agents producing reports autonomously
- Any `sessions_spawn` task with `mode: "session"` that runs extended

## Monitoring Method

Periodically check the agent's session history:

```
sessions_history:
  sessionKey: "{agent_session_key}"
  includeTools: true
  limit: 20
```

## Detection Signals

### Signal 1: Claim/Tool Ratio

Count messages containing action claims vs actual tool calls in the last 20 messages.

- **Healthy**: tool_calls ≥ 0.5 × claims (agent uses tools for at least half its claims)
- **Warning**: tool_calls < 0.3 × claims
- **Critical**: tool_calls < 0.1 × claims (agent claiming much, doing little)

Action claims to count: "created", "modified", "committed", "pushed", "deployed", "ran tests", "fixed", "updated".

### Signal 2: Zero-Error Streak

In real work, agents encounter errors, retries, and unexpected states.

- **Healthy**: Errors/retries appear naturally in tool outputs
- **Warning**: 8+ consecutive steps with zero errors
- **Critical**: 15+ steps all "successful" (very likely fabricating)

### Signal 3: Phantom References

Agent mentions files, branches, or artifacts that do not exist.

Quick check:
```bash
# Extract file paths from agent's last N messages
# Verify each exists
ls -la {each_referenced_path}
git branch -a | grep {each_referenced_branch}
```

Any miss = critical alert.

### Signal 4: Output Stagnation

Agent produces verbose text but file system shows no changes.

```bash
# Check workspace modification time
find {workspace} -mmin -5 -type f | wc -l
```

If agent claims active work but 0 files modified in 5 minutes → alert.

## Response Protocol

| Alert Level | Action |
|-------------|--------|
| Warning (1 signal) | Log it, continue monitoring |
| Elevated (2 signals) | Steer agent: "Verify your last 3 claims with tool output" |
| Critical (3+ signals OR phantom ref) | Kill agent, run L2 cross-model audit on outputs |

### Steering Command

```
subagents:
  action: steer
  target: "{agent_label}"
  message: "VERIFICATION CHECKPOINT: Before continuing, use exec/read tools to confirm your last 3 claimed actions actually happened. Show the tool output."
```

If agent responds with claims but still no tool calls after steering → kill and audit.

## Monitoring Frequency

| Task Duration | Check Interval |
|---------------|----------------|
| 15-30 min | Once at end |
| 30-60 min | Every 15 min |
| >60 min | Every 10 min |

## Cost

- `sessions_history` call: free (internal)
- `subagents steer`: free (internal)
- Only costs money if audit triggers (L2 spawn)
