---
name: security-audit
description: Security logging, periodic auditing, and config security review for OpenClaw agents. Use when: (1) logging potentially risky operations (rm -rf, curl | bash, sensitive file writes, external network requests), (2) user asks for an activity audit or wants to review recent agent actions, (3) user asks to audit the current OpenClaw configuration for security risks, (4) setting up periodic security checks or notifications.
---

# Security Audit Skill

Lightweight, observer-only security layer for OpenClaw. Logs agent actions, audits activity history, and reviews OpenClaw config for risks. **Does not block or interrupt any operations.**

## Quick Start

Three things this skill does:

1. **Log risky actions** → call `./scripts/log_event.sh` after notable operations
2. **Audit activity history** → run `./scripts/run_audit.sh` on request
3. **Audit OpenClaw config** → run `./scripts/audit_config.sh` on request

## Core Behaviors

### Logging Risky Actions (Observer Mode)

This skill is **purely observational** — it never blocks or delays any operation. After completing a risky action, log it:

```bash
./scripts/log_event.sh <level> <category> "<summary>" "<detail>" <action>
```

**When to log:**

| Level | When |
|-------|------|
| CRITICAL | Remote code execution (curl\|bash), credential/key file reads, persistence writes (cron, authorized_keys, launchd), privilege escalation |
| WARN | Bulk file deletion, sensitive file reads, external requests with dynamic URLs, shell env modification |
| INFO | Normal workspace operations, standard dev tooling — skip unless building an audit trail |

**Categories**: `exec` | `file_write` | `network` | `credential` | `persistence`

**Actions**: `allowed` | `flagged`

Note: `blocked_soft` is removed — this skill does not block. If something was risky but the user explicitly requested it, use `allowed`. Otherwise `flagged`.

**Example:**
```bash
./scripts/log_event.sh WARN exec "bulk delete outside workspace" "rm -rf /tmp/build" flagged
./scripts/log_event.sh CRITICAL credential "SSH key read" "cat ~/.ssh/id_rsa" allowed
```

### Running Activity Audits

When user asks for a security audit or activity review:

```bash
./scripts/run_audit.sh 7   # last 7 days (default)
./scripts/run_audit.sh 30  # last 30 days
```

Read the output, then:
- Highlight CRITICAL entries and explain what happened
- Note any suspicious patterns (same WARN repeating, unexpected credential access)
- If `notify_on_audit_complete: true` in config → send via `message` tool to configured channel

### Auditing OpenClaw Config

When user asks "is my OpenClaw config secure?" or similar:

```bash
./scripts/audit_config.sh          # standard audit
./scripts/audit_config.sh --deep   # also probe live Gateway
./scripts/audit_config.sh --fix    # audit + apply safe fixes
```

This script delegates to `openclaw security audit` (the native CLI tool), which checks gateway auth, tool permissions, network exposure, file permissions, and other config foot-guns. Read the output and present findings to the user with context and recommendations.

## Notification Setup

Users can enable proactive notifications by creating `logs/security-audit-config.json`:

```json
{
  "notify_channel": "dingtalk",
  "notify_on": ["CRITICAL", "WARN"],
  "notify_on_audit_complete": true
}
```

Supported channels: whatever OpenClaw has configured (dingtalk, telegram, discord, etc.).  
Default if file missing: log-only, no notifications.

When `notify_on` is set and you log a matching event, send a brief message via the `message` tool after logging.

## Reference Files

- **[dangerous-patterns.md](references/dangerous-patterns.md)** — Comprehensive list of risky exec, file, and network patterns with examples
- **[audit-guide.md](references/audit-guide.md)** — Log format, risk classification, notification config, report format
- **[config-risks.md](references/config-risks.md)** — OpenClaw config fields and their security implications

## First-Time Setup

1. `logs/security-audit.log` is created automatically on first event
2. Offer to help create `logs/security-audit-config.json` for notifications
3. Suggest adding a cron job via the `cron` skill for periodic audits (user sets interval)
4. For config audit: no setup needed — runs on demand

## What This Skill Does NOT Do

- Block or delay any operation
- Intercept other skills at runtime
- Monitor the OpenClaw process itself
- Replace proper OS-level access controls or sandboxing
