# Audit Log Hook - Tool Call Audit

## Purpose

Record all tool calls via `before_tool_call` and `after_tool_call` hooks for:
- Security auditing
- Debugging issues
- Usage statistics
- Error tracking

## Implementation

Register hooks in a plugin:

```javascript
// Audit log file path
const AUDIT_LOG = path.join(process.env.OPENCLAW_STATE_DIR || '~/.openclaw', 'audit.log');

api.registerHook("before_tool_call", async ({ event, ctx }) => {
  const entry = {
    ts: new Date().toISOString(),
    event: "before_tool_call",
    tool: event.tool.name,
    params: JSON.stringify(event.tool.params).slice(0, 500),
    session: ctx.sessionKey,
    user: ctx.session?.senderId || 'unknown'
  };
  console.log("[AUDIT]", JSON.stringify(entry));
  return {};
});

api.registerHook("after_tool_call", async ({ event, ctx }) => {
  const entry = {
    ts: new Date().toISOString(),
    event: "after_tool_call",
    tool: event.tool.name,
    result: String(event.result).slice(0, 200),
    error: event.error?.message || null,
    duration: event.durationMs,
    session: ctx.sessionKey
  };
  console.log("[AUDIT]", JSON.stringify(entry));
  return {};
});
```

## Log Format

```json
{"ts":"2026-04-01T23:00:00.000Z","event":"before_tool_call","tool":"exec","params":"{\"command\":\"ls -la\"}","session":"agent:main:feishu:direct:ou_xxx","user":"ou_xxx"}
{"ts":"2026-04-01T23:00:00.050Z","event":"after_tool_call","tool":"exec","result":"total 8\ndrwxr-xr-x  12 dc  staff   384 Apr  1 23:00","error":null,"duration":50,"session":"agent:main:feishu:direct:ou_xxx"}
```

## Sensitive Data Handling

Auto-redact sensitive fields:

```javascript
function redactSensitive(obj) {
  const sensitive = ['apiKey', 'token', 'password', 'secret'];
  for (const key of Object.keys(obj)) {
    if (sensitive.some(s => key.toLowerCase().includes(s))) {
      obj[key] = '[REDACTED]';
    }
  }
  return obj;
}
```

## Statistics Analysis

Periodically analyze audit.log:

```bash
# Count tool usage
grep "before_tool_call" audit.log | jq -r .tool | sort | uniq -c | sort -rn

# Count errors
grep "after_tool_call" audit.log | jq -r '.error' | grep -v null | wc -l

# Count sessions
grep "before_tool_call" audit.log | jq -r .session | sort -u | wc -l
```
