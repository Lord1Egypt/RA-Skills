---
name: openclaw-permissions
description: |
  This skill should be used when the user wants to audit, review, or list the
  permissions and access rights held by OpenClaw. Use it for requests like
  "check openclaw permissions", "show openclaw access", "what can openclaw access",
  "openclaw permission list", "review openclaw capabilities",
  "what APIs does openclaw use", "which channels is openclaw connected to",
  "what models does openclaw use", or "openclaw access audit".
  Produces a structured Markdown report covering API credentials, channel access,
  gateway configuration, tool execution rules, command permissions, device identity,
  and internal hooks — with all sensitive values masked.
version: 1.0.0
---

# OpenClaw Permissions Audit Skill

## Goal

Read OpenClaw configuration files and produce a structured permissions report showing what access rights OpenClaw currently holds, which services it is connected to, and what capabilities are allowed or denied.

## Steps

### 1. Read Configuration Files

Attempt to read the following files in order. If a file does not exist, mark all its fields as `⚠️ not configured` in the report — do not silently skip it.

- `~/.openclaw/openclaw.json` — main configuration
- `~/.openclaw/exec-approvals.json` — tool execution approvals
- `~/.openclaw/identity/device-auth.json` — device authentication
- `~/.openclaw/identity/device.json` — device identity

### 2. Extract Permission Dimensions

Extract and report the following dimensions:

**A. AI Model API Access**
- From `openclaw.json → auth.profiles`, list each configured provider by name (e.g., anthropic, kimi-coding). Do not show credentials.
- From `openclaw.json → env`, list the key names of API keys only. Never show values.
- From `openclaw.json → agents.defaults.model`, show the default primary model and any configured fallbacks.

**B. Channel / Communication Access**
- From `openclaw.json → channels`, for each channel entry show:
  - enabled status
  - count of authorized user IDs plus first 4 chars of each ID (not the full ID). User IDs are nested under `channels.<channel>.guilds[guildId].users[]` — navigate to that path, not a top-level `users` key.
  - count of authorized guild/server IDs only (no partial IDs)
  - group policy (allowlist / open)

**C. Gateway Access**
- From `openclaw.json → gateway`, show:
  - port, bind address, mode
  - auth mode (token / none) — show existence only (✅/❌), not the token value
  - Tailscale enabled status
  - denyCommands list (command names are safe to show in full)

**D. Tool Execution Permissions**
- From `openclaw.json → tools.profile`, show the profile name.
- From `exec-approvals.json → agents`, list per-agent tool approval rules by agent name and rule summary.
- From `exec-approvals.json → defaults`, list the default tool approval rules.
- Do not read or report the `socket` field from `exec-approvals.json`. It contains an IPC auth token and an absolute socket path. Skip it entirely.

**E. Command Permissions**
- From `openclaw.json → commands`, show the allowFrom sources and whether restart is permitted.
- From `openclaw.json → session.dmScope`, show the DM session scope value.

**F. Device Identity & Auth**
- From `identity/device-auth.json`, show: first 8 chars of device ID only, whether a token is present (✅/❌) at `tokens.operator`, operator role at `tokens.operator.role`, operator scopes at `tokens.operator.scopes`.
- From `identity/device.json`, show whether a public key is present (✅/❌). Do not output or acknowledge `privateKeyPem` in any way. Show key algorithm from `publicKeyPem` header only if identifiable without exposing key bytes.

**G. Internal Hooks**
- From `openclaw.json → hooks.internal.entries`, list each hook entry by name and enabled status. Navigate to the `.entries` sub-key, not the parent `hooks.internal` object.

### 3. Output Format

Output as Markdown tables and grouped lists. Example structure:

```
## OpenClaw Permissions Report

### AI Model API
| Provider | Profile | Auth Mode | Status |
|----------|---------|-----------|--------|
| anthropic | anthropic:default | api_key | ✅ configured |
| kimi-coding | kimi-coding:default | api_key | ✅ configured |

Env API Keys: EXAMPLE_API_KEY ✅

Default model: provider/model-id
Fallback: provider/model-id

### Channel Access
| Channel | Status | Policy | Authorized Users | Streaming |
|---------|--------|--------|-----------------|-----------|
| Discord | ✅ enabled | allowlist | 1 user (XXXX...) | off |

Authorized guilds: 1

### Gateway
| Item | Value |
|------|-------|
| Mode | local |
| Port | XXXXX |
| Bind | loopback |
| Auth | token ✅ |
| Tailscale | off |

Denied commands: camera.snap · camera.clip · screen.record · ...

### Tool Permissions
- Permission profile: full
- Default approval rules: (none configured)
- Agent-specific rules: (none configured)

### Command Permissions
- Native commands: auto
- Native skills: auto
- Allow restart: ✅
- Commands allowed from Discord: ✅ (1 user)
- Session DM scope: per-channel-peer

### Internal Hooks
| Hook | Status |
|------|--------|
| boot-md | ✅ enabled |
| command-logger | ✅ enabled |
| session-memory | ✅ enabled |
| bootstrap-extra-files | ✅ enabled |

### Device Identity
- Device ID: XXXXXXXX... (configured)
- Public key: ✅ present (Ed25519)
- Operator token: ✅ present
- Operator role: operator
- Operator scopes: operator.admin
```

### 4. Security Rules

**Never output:**
- Full token values (Discord token, gateway token, device token)
- Full API key values
- Private keys or passwords — including `privateKeyPem` from `device.json`, treat it as equivalent to a password
- Full user IDs or device IDs
- File paths in expanded form — always use `~/.openclaw/` notation, never `/Users/<username>/...`

**Safe to output:**
- Existence status (✅ / ❌)
- First 4–8 characters of IDs for reference (not authentication)
- Counts (e.g., "1 user", "2 guilds")
- Permission scope descriptions

**Default rule for unrecognized fields:** If a config file contains a field not covered by these rules, apply the most restrictive default — show existence only (✅ / ❌), never the value.

### 5. Missing Data Handling

- File not found → mark all its fields as `⚠️ not configured`
- Field is empty → mark as `(empty)`
- Parse error → mark as `⚠️ unreadable`
