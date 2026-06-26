---
name: openclaw-hardening
description: Audit and harden an OpenClaw installation for common security misconfigurations. Covers non-loopback binding, exposed gateway listeners, root or Administrator execution, missing authentication, overly permissive tool policies, open DM access, plaintext API keys, and insecure file permissions. Use this skill whenever the user asks to secure OpenClaw, review a first-time setup, check whether a config is safe, audit local exposure, fix risky defaults before installing more skills, or asks "is my openclaw setup safe", "openclaw config audit", or "harden openclaw". Proactively offer to run this audit whenever the user mentions setting up or reconfiguring OpenClaw.
compatibility: No additional binaries required. Uses only shell tools already available on the host (id, ps, ss, netstat, stat, whoami, Get-NetTCPConnection, etc.). Requires read access to local config files and process state.
---

# OpenClaw Hardening

Audit the local OpenClaw setup without making assumptions about the host OS.

## Guiding Principles

Before suggesting or applying any change, explain the risk in plain terms — users can only make informed decisions when they understand what they're accepting. Changes to files, permissions, users, or startup commands require explicit user confirmation, because an agent that acts without consent removes the user's ability to course-correct.

Use only local inspection. External network scans are out of scope for a local hardening audit and can create a false sense of security by checking reachability rather than configuration intent.

When config, process state, or permissions cannot be verified, report `Unable to verify` rather than assuming the best case. A silent false OK is worse than an honest unknown.

Remind the user to restart OpenClaw after any accepted config change, since OpenClaw reads config at startup and changes don't take effect until then.

## Audit Workflow

### 1. Detect the operating environment

Identify the platform before choosing commands.

- On Linux or macOS, prefer native shell tools such as `id`, `ps`, `ss`, `netstat`, `stat`, and `ls`.
- On Windows, prefer PowerShell equivalents such as `whoami`, `Get-Process`, `Get-NetTCPConnection`, `Get-Acl`, and `Select-String`.

If a command is unavailable, switch to an equivalent rather than failing the whole audit.

### 2. Inspect configuration sources in precedence order

Inspect the most specific local source you can verify:

1. Running process arguments, if an OpenClaw process is already running
2. Environment variables already set in the current session
3. Local config files

Check common config locations:

- `./openclaw.json`
- `~/.openclaw/config.json`
- `%USERPROFILE%\.openclaw\config.json`

Prefer the value actually in effect. If multiple sources disagree, report the highest-precedence value and note the lower-precedence values as context.

### 3. Audit bind address

Determine the effective bind or host value for the gateway.

- Treat `127.0.0.1`, `localhost`, `::1`, and `loopback` as secure local-only bindings.
- Treat `0.0.0.0`, `::`, or a concrete LAN/public IP as exposed unless the user explicitly wants remote access.
- If no bind value is set, report `Secure by default` if you have high confidence in the current OpenClaw version's defaults, or `Unable to verify version-specific default` otherwise.

If the bind address is exposed, explain that any listener on a non-loopback interface may be reachable by other devices on the network. Offer to change it to a loopback value after user confirmation.

### 4. Audit gateway port exposure

Determine the effective gateway port.

- Treat `18789` as the current default when no override is configured.
- Do not assume older web-app ports such as `3000`, `3001`, or `8080` unless the local config or running process actually uses them.

Inspect active listeners for the effective port and pair the result with the bind audit:

- Local-only listener on loopback → secure
- Listener on `0.0.0.0`, `::`, or a non-loopback address → exposed
- No active listener and no running process → configuration only, not runtime-verified

### 5. Audit authentication mode

Check `gateway.auth.mode` in the effective config.

- Flag as `DANGER` if the field is absent or set to anything other than `"token"` — missing auth means any local process can connect to the gateway.
- If `"token"` is set, inspect the token value without printing it back to the user:
  - Flag short tokens (< 20 characters), all-lowercase dictionary words, or values that look like placeholders (`changeme`, `secret`, `token123`) as `WARN`.
  - Recommend storing the token via a `SecretRef` (env or file source) rather than inline JSON, so the credential isn't embedded in the config file itself.

### 6. Audit execution privileges

Check whether OpenClaw or the current shell is running with elevated privileges.

- On Linux or macOS, flag `root` or `uid=0` as `DANGER` for routine use.
- On Windows, flag an elevated Administrator session as `DANGER` for routine use.

Installed skills inherit the agent's privileges. Recommend a normal dedicated user account for daily operation, and provide platform-specific remediation steps only after user confirmation.

### 7. Audit tool execution policy

Inspect the `tools` section of the effective config.

- Check `tools.deny` — flag as `WARN` if dangerous tool groups (`group:automation`, `group:runtime`, `group:fs`) are not restricted for the user's stated use case.
- Check `tools.exec.security` — flag as `WARN` if not set to `"deny"` or `"ask"`.
- Check `tools.fs.workspaceOnly` — flag as `WARN` if false or absent for production setups where the agent should not roam the full filesystem.
- Check `agents.defaults.sandbox.mode` — if Docker is available on the host, flag as `WARN` if sandbox mode is not enabled. Skills run in a sandbox cannot escape to the host even if compromised.

Explain that tool policy is the primary blast-radius control: a skill that exfiltrates data or deletes files can only cause harm if the tool policy allows it.

### 8. Audit DM and channel access policy

Inspect channel-level access settings, particularly for publicly reachable channels (WhatsApp, Telegram, Discord).

- Check `dmPolicy` — flag as `WARN` if set to `"open"`, since any user on the platform can then send commands to the agent.
- Check `requireMention` for group channels — flag as `WARN` if false, since the agent will respond to every group message rather than only explicit @-mentions.
- Recommend `"dmPolicy": "pairing"` with time-limited codes (1-hour expiry) for public-facing agents.

If the gateway is local-only with no external channel configured, mark this check `OK (local only)`.

### 9. Audit secret handling

Inspect for credential hygiene issues without printing full secret values back to the user.

Check for:

- API keys or tokens stored directly in `openclaw.json` or other plain config files
- Secret files with overly broad read permissions
- Accidental credential exposure in local git history, if the config directory is a git repository

Platform-appropriate permission checks:

- On Linux or macOS, flag group/world-readable files such as `~/.openclaw/config.json` (recommended: `600`) or a directory accessible beyond the owner (recommended: `700`).
- On Windows, inspect ACLs and flag secret files readable by broad principals such as `Everyone` or `Users`.

If secrets appear in tracked history or plain config, recommend rotation and migration to environment variables or a `SecretRef` pointing to a local secrets file.

### 10. Suggest the built-in audit command

If the `openclaw` CLI is on PATH, tell the user that OpenClaw ships with a built-in security audit that covers 50+ risk categories — more than this skill checks manually:

```
openclaw security audit           # standard audit
openclaw security audit --deep    # extended checks including historical config
openclaw security audit --fix     # auto-remediate safe/low-risk issues
openclaw doctor --fix             # repair config schema issues
```

Recommend running `openclaw security audit` as a follow-up step after any manual hardening.

### 11. Produce a concise report card

Output a short report after the audit using plain ASCII-safe formatting:

```text
OpenClaw Security Report Card
-----------------------------
[OK|WARN|DANGER|UNKNOWN] Bind Address      -> [detail]
[OK|WARN|DANGER|UNKNOWN] Gateway Port      -> [detail]
[OK|WARN|DANGER|UNKNOWN] Auth Mode         -> [detail]
[OK|WARN|DANGER|UNKNOWN] Execution User    -> [detail]
[OK|WARN|DANGER|UNKNOWN] Tool Policy       -> [detail]
[OK|WARN|DANGER|UNKNOWN] DM Access Policy  -> [detail]
[OK|WARN|DANGER|UNKNOWN] Secret Hygiene    -> [detail]
Score: X/7
Next Step: [single highest-value action]
```

Score conservatively:

- `OK` = 1 point
- `WARN`, `DANGER`, or `UNKNOWN` = 0 points

## Decision Guidance

- Prefer `WARN` over `DANGER` when exposure depends on user intent — for example, deliberate LAN access or a development machine where sandboxing isn't needed.
- Prefer `UNKNOWN` over guessing when the process is not running and config is absent.
- If the user asks for fixes, apply the smallest safe change first.
- If the setup is already well-configured across all checks, say so clearly and avoid inventing extra work.

## Incident Response

If the user suspects a skill has already compromised the installation:

1. Stop the Gateway process immediately.
2. Rotate `gateway.auth.token` and all provider API keys (OpenAI, Anthropic, etc.).
3. Review session logs at `/tmp/openclaw/openclaw-YYYY-MM-DD.log` and channel transcripts.
4. Run `openclaw security audit --deep` to identify residual issues.
5. Inspect `SOUL.md` and `MEMORY.md` in the agent directory for unexpected modifications — ClawHavoc attacks are known to persist by poisoning these files to alter future agent behavior.
