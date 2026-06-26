# OpenClaw Config Security Reference

This document describes OpenClaw config fields with security implications. Used by `audit_config.sh` and the agent when interpreting config audit results.

---

## High-Risk Fields

### `gateway.remote.url` / `gateway.bind`
- **Risk**: If `bind` uses `0.0.0.0` without auth, the gateway is exposed to all network interfaces
- **Good**: `127.0.0.1` (localhost only) or Tailscale IP
- **Flag if**: `0.0.0.0` with no auth token configured

### `gateway.token` / `auth.token`
- **Risk**: Weak or missing token allows unauthenticated access to the gateway
- **Good**: Long random string (32+ chars)
- **Flag if**: empty, missing, or short (<16 chars)

### `plugins.entries.*.config.publicUrl`
- **Risk**: If a plugin exposes a public URL, it's reachable from the internet
- **Good**: Behind Tailscale, behind auth, or explicitly intended
- **Flag if**: public URL set but no mention of auth

### `acp.allowedAgents` / `agents.defaults`
- **Risk**: Overly permissive agent allowlists let skills spawn arbitrary sub-agents
- **Good**: Explicit allowlist with only needed agents
- **Flag if**: wildcard (`*`) or very broad list when not needed

### `exec.security` / `exec.ask`
- **Risk**: `security: full` with `ask: off` means exec runs without confirmation
- **Good**: `ask: on-miss` or `ask: always` for elevated commands
- **Flag if**: both `security: full` and `ask: off`

### `channels.*.token` / `channels.*.apiKey`
- **Risk**: Leaked or hardcoded tokens expose messaging accounts
- **Good**: Loaded from env vars (`$ENV_VAR_NAME` syntax)
- **Flag if**: token looks like a literal value (not `$VAR`) and is long/looks like a secret

### `sessions.main.model` / `agents.defaults.model`
- **Risk**: Model pointed at an unknown/third-party relay could exfiltrate conversation data
- **Good**: Known providers (anthropic, openai, google) or trusted relays
- **Flag if**: model URL is an unknown domain

### `skills.dir` / `skills.allowlist`
- **Risk**: Skills directory pointing outside workspace, or no allowlist (all skills auto-load)
- **Good**: Explicit allowlist of trusted skills
- **Flag if**: no allowlist and skills dir is writable by others

---

## Medium-Risk Fields

### `cron.jobs` (many jobs)
- **Flag if**: many active cron jobs with `agentTurn` payloads and no delivery config — could be resource drain or hard to audit

### `sessions.isolated.*`
- **Flag if**: isolated sessions have very long timeouts with no supervision

### `logging.level: debug`
- **Note**: Debug logging may capture sensitive data in logs
- **Flag if**: debug logging enabled in production with log files written to disk

---

## Low-Risk / Informational

- `gateway.restartDelayMs` — operational, not a security concern
- `ui.*` — UI preferences, not security-sensitive
- `tts.*` — output only
- `memory.*` — local storage paths

---

## Config Audit Scoring

The audit script assigns a simple risk tier to the overall config:

| Tier | Criteria |
|------|----------|
| 🟢 Low | No high-risk flags, all tokens look like env vars |
| 🟡 Medium | 1-2 high-risk flags, no critical exposure |
| 🔴 High | Gateway exposed without auth, hardcoded secrets, or unknown model relay |
