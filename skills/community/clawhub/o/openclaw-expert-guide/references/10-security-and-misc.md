# OpenClaw Security, Help, Nodes & Diagnostics Reference

## Table of Contents
- [Security](#security)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Debugging](#debugging)
- [Environment Variables](#environment-variables)
- [Scripts Reference](#scripts-reference)
- [Nodes](#nodes)
- [Diagnostics Export](#diagnostics-export)
- [Diagnostics Flags](#diagnostics-flags)
- [CI Pipeline](#ci-pipeline)
- [RPC Adapters](#rpc-adapters)

---

## Security

### Security Model

**Personal assistant trust model**: This guidance assumes one trusted operator boundary per gateway (single-user, personal-assistant model). OpenClaw is **NOT** a hostile multi-tenant security boundary for multiple adversarial users sharing one agent or gateway.

- Supported: one user/trust boundary per gateway (prefer one OS user/host/VPS per boundary)
- Not supported: one shared gateway/agent used by mutually untrusted or adversarial users
- If adversarial-user isolation is required: split by trust boundary (separate gateway + credentials, separate OS users/hosts)

### Quick Check

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

See also: [Formal Verification (Security Models)](/security/formal-verification).

`security audit --fix` flips common open group policies to allowlists, restores `logging.redactSensitive: "tools"`, tightens state/config/include-file permissions, and uses Windows ACL resets instead of POSIX `chmod` when running on Windows.

### Deployment and Host Trust

- If someone can modify Gateway host state/config (`~/.openclaw`), treat them as a trusted operator
- Running one Gateway for multiple mutually untrusted/adversarial operators is **not recommended**
- For mixed-trust teams: split trust boundaries with separate gateways (or at minimum separate OS users/hosts)
- Inside one Gateway instance, authenticated operator access is a trusted control-plane role, not a per-user tenant role
- Session identifiers (`sessionKey`, session IDs, labels) are **routing selectors, not authorization tokens**
- If several people can message one tool-enabled agent, each can steer that same permission set

### Shared Slack Workspace: Real Risk

If "everyone in Slack can message the bot", risks include:
- Any allowed sender can induce tool calls (`exec`, browser, network/file tools) within the agent's policy
- Prompt/content injection from one sender can cause actions affecting shared state
- Any allowed sender can potentially drive exfiltration via tool usage

Use separate agents/gateways with minimal tools for team workflows.

### Company-Shared Agent: Acceptable Pattern

This is acceptable when everyone using that agent is in the same trust boundary (for example, one company team) and the agent is strictly business-scoped:

- Run it on a dedicated machine/VM/container
- Use a dedicated OS user + dedicated browser/profile/accounts for that runtime
- Do not sign that runtime into personal Apple/Google accounts or personal password-manager/browser profiles

If you mix personal and company identities on the same runtime, you collapse the separation and increase personal-data exposure risk.

### Gateway and Node Trust Concept

Treat Gateway and node as one operator trust domain, with different roles:

- **Gateway** is the control plane and policy surface (`gateway.auth`, tool policy, routing)
- **Node** is the remote execution surface paired to that Gateway (commands, device actions, host-local capabilities)
- A caller authenticated to the Gateway is trusted at Gateway scope; after pairing, node actions are trusted operator actions on that node
- `sessionKey` is routing/context selection, not per-user auth
- Exec approvals (allowlist + ask) are operator-intent guardrails, not hostile multi-tenant isolation
- OpenClaw's product default for trusted single-operator setups is that host exec on `gateway`/`node` is allowed without approval prompts (`security="full"`, `ask="off"` unless you tighten it) — that default is intentional UX, not a vulnerability
- Exec approvals bind exact request context and best-effort direct local file operands; they do not semantically model every runtime/interpreter loader path — use sandboxing and host isolation for strong boundaries

If you need hostile-user isolation, split trust boundaries by OS user/host and run separate gateways.

### Trust Boundary Matrix

| Boundary or control | What it means | Common misread |
|---|---|---|
| `gateway.auth` (token/password/trusted-proxy/device auth) | Authenticates callers to gateway APIs | "Needs per-message signatures on every frame" |
| `sessionKey` | Routing key for context/session selection | "Session key is a user auth boundary" |
| Prompt/content guardrails | Reduce model abuse risk | "Prompt injection alone proves auth bypass" |
| `canvas.eval` / browser evaluate | Intentional operator capability when enabled | "Any JS eval primitive is automatically a vuln" |
| Local TUI `!` shell | Explicit operator-triggered local execution | "Local shell convenience command is remote injection" |
| Node pairing and node commands | Operator-level remote execution on paired devices | "Remote device control should be untrusted by default" |

### NOT Vulnerabilities by Design

These patterns are commonly reported but are closed as no-action:
- Prompt-injection-only chains without a policy, auth, or sandbox bypass
- Claims that assume hostile multi-tenant operation on one shared host
- Claims that classify normal operator read-path access (e.g. `sessions.list` / `sessions.preview` / `chat.history`) as IDOR in a shared-gateway setup
- Localhost-only deployment findings (e.g., HSTS on a loopback-only gateway)
- Discord inbound webhook signature findings for inbound paths that do not exist in this repo
- Reports that treat node pairing metadata as a hidden second per-command approval layer for `system.run`, when the real execution boundary is still the gateway's global node command policy plus the node's own exec approvals
- Reports that treat configured `gateway.nodes.pairing.autoApproveCidrs` as a vulnerability by itself — disabled by default, requires explicit CIDR/IP entries, only applies to first-time `role: node` pairing with no requested scopes, does not auto-approve operator/browser/Control UI/WebChat/role upgrades/scope upgrades/metadata changes/public-key changes/same-host loopback trusted-proxy paths
- "Missing per-user authorization" findings that treat `sessionKey` as an auth token

### Hardened Baseline (60 Seconds)

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

### Shared Inbox Quick Rule

If more than one person can DM your bot:
- Set `session.dmScope: "per-channel-peer"` (or `"per-account-channel-peer"` for multi-account channels)
- Keep `dmPolicy: "pairing"` or strict allowlists
- Never combine shared DMs with broad tool access

### Context Visibility Model

- **Trigger authorization**: who can trigger the agent (`dmPolicy`, `groupPolicy`, allowlists, mention gates)
- **Context visibility**: what supplemental context is injected into model input

Settings:
- `contextVisibility: "all"` (default): keeps supplemental context as received
- `contextVisibility: "allowlist"`: filters supplemental context to senders allowed by active allowlist checks
- `contextVisibility: "allowlist_quote"`: like `allowlist`, but still keeps one explicit quoted reply

Advisory triage guidance: claims that only show "model can see quoted or historical text from non-allowlisted senders" are hardening findings addressable with `contextVisibility`, not auth or sandbox boundary bypasses by themselves. To be security-impacting, reports still need a demonstrated trust-boundary bypass (auth, policy, sandbox, approval, or another documented boundary).

### What the Security Audit Checks

- **Inbound access** (DM policies, group policies, allowlists): can strangers trigger the bot?
- **Tool blast radius** (elevated tools + open rooms): could prompt injection turn into shell/file/network actions?
- **Exec approval drift** (`security=full` — broad posture warning, not proof of a bug; `autoAllowSkills`, interpreter allowlists without `strictInlineEval`)
- **Network exposure** (Gateway bind/auth, Tailscale Serve/Funnel, weak/short auth tokens)
- **Browser control exposure** (remote nodes, relay ports, remote CDP endpoints)
- **Local disk hygiene** (permissions, symlinks, config includes, "synced folder" paths like iCloud/CloudStorage)
- **Plugins** (plugins load without an explicit allowlist)
- **Policy drift/misconfig** (sandbox docker settings configured but sandbox mode off; ineffective `gateway.nodes.denyCommands` patterns — matching is exact command-name only (e.g. `system.run`) and does not inspect shell text; dangerous `gateway.nodes.allowCommands` entries; global `tools.profile="minimal"` overridden by per-agent profiles; plugin-owned tools reachable under permissive tool policy)
- **Runtime expectation drift** (e.g. assuming implicit exec still means `sandbox` when `tools.exec.host` now defaults to `auto`, or explicitly setting `tools.exec.host="sandbox"` while sandbox mode is off)
- **Model hygiene** (warn when configured models look legacy)

With `--deep`, OpenClaw also attempts a best-effort live Gateway probe.

### Security Audit Checklist (Priority Order)

1. **Anything "open" + tools enabled**: lock down DMs/groups first, then tighten tool policy/sandboxing
2. **Public network exposure** (LAN bind, Funnel, missing auth): fix immediately
3. **Browser control remote exposure**: treat like operator access (tailnet-only, pair nodes deliberately)
4. **Permissions**: state/config/credentials/auth not group/world-readable
5. **Plugins**: only load what you explicitly trust
6. **Model choice**: prefer modern, instruction-hardened models for any bot with tools

### Security Audit Glossary

Each audit finding is keyed by a structured `checkId` (e.g., `gateway.bind_no_auth` or `tools.exec.security_full_configured`). Common severity classes:

- `fs.*` — filesystem permissions on state, config, credentials, auth profiles
- `gateway.*` — bind mode, auth, Tailscale, Control UI, trusted-proxy setup
- `hooks.*`, `browser.*`, `sandbox.*`, `tools.exec.*` — per-surface hardening
- `plugins.*`, `skills.*` — plugin/skill supply chain and scan findings
- `security.exposure.*` — cross-cutting checks where access policy meets tool blast radius

See the full catalog with severity levels, fix keys, and auto-fix support at the Security audit checks page.

### Credential Storage Map

| Credential | Location |
|---|---|
| WhatsApp | `~/.openclaw/credentials/whatsapp/<accountId>/creds.json` |
| Telegram bot token | config/env or `channels.telegram.tokenFile` |
| Discord bot token | config/env or SecretRef |
| Slack tokens | config/env (`channels.slack.*`) |
| Pairing allowlists (default account) | `~/.openclaw/credentials/<channel>-allowFrom.json` |
| Pairing allowlists (non-default accounts) | `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json` |
| Model auth profiles | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| File-backed secrets payload (optional) | `~/.openclaw/secrets.json` |
| Legacy OAuth import | `~/.openclaw/credentials/oauth.json` |

### Control UI over HTTP

The Control UI needs a **secure context** (HTTPS or localhost).

`gateway.controlUi.allowInsecureAuth`:
- Allows Control UI auth without device identity when page is loaded over non-secure HTTP on localhost
- Does NOT bypass pairing checks
- Does NOT relax remote device identity requirements

`gateway.controlUi.dangerouslyDisableDeviceAuth`:
- Disables device identity checks entirely
- Severe security downgrade — use only for emergency debugging

Separate from those dangerous flags, successful `gateway.auth.mode: "trusted-proxy"` can admit **operator** Control UI sessions without device identity. That is an intentional auth-mode behavior, not an `allowInsecureAuth` shortcut, and it still does not extend to node-role Control UI sessions.

### Insecure/Dangerous Flags

`openclaw security audit` raises `config.insecure_or_dangerous_flags` when these are enabled:
- `gateway.controlUi.allowInsecureAuth=true`
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true`
- `gateway.controlUi.dangerouslyDisableDeviceAuth=true`
- `hooks.gmail.allowUnsafeExternalContent=true`
- `hooks.mappings[<index>].allowUnsafeExternalContent=true`
- `tools.exec.applyPatch.workspaceOnly=false`
- `plugins.entries.acpx.config.permissionMode=approve-all`

All `dangerous*` / `dangerously*` keys in the config schema:

Control UI and browser:
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback`
- `gateway.controlUi.dangerouslyDisableDeviceAuth`
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`

Channel name-matching (bundled and plugin channels; also available per `accounts.<accountId>` where applicable):
- `channels.discord.dangerouslyAllowNameMatching`
- `channels.slack.dangerouslyAllowNameMatching`
- `channels.googlechat.dangerouslyAllowNameMatching`
- `channels.msteams.dangerouslyAllowNameMatching`
- `channels.synology-chat.dangerouslyAllowNameMatching` (plugin channel)
- `channels.synology-chat.dangerouslyAllowInheritedWebhookPath` (plugin channel)
- `channels.zalouser.dangerouslyAllowNameMatching` (plugin channel)
- `channels.irc.dangerouslyAllowNameMatching` (plugin channel)
- `channels.mattermost.dangerouslyAllowNameMatching` (plugin channel)

Network exposure:
- `channels.telegram.network.dangerouslyAllowPrivateNetwork` (also per account)

Sandbox Docker (defaults + per-agent):
- `agents.defaults.sandbox.docker.dangerouslyAllowReservedContainerTargets`
- `agents.defaults.sandbox.docker.dangerouslyAllowExternalBindSources`
- `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin`

### Reverse Proxy Configuration

If running the Gateway behind a reverse proxy (nginx, Caddy, Traefik), configure `gateway.trustedProxies` for proper forwarded-client IP handling.

When the Gateway detects proxy headers from an address **not** in `trustedProxies`, it will **not** treat connections as local clients. This prevents authentication bypass where proxied connections would appear to come from localhost.

`gateway.trustedProxies` also feeds `gateway.auth.mode: "trusted-proxy"`, but that auth mode is stricter: it **fails closed on loopback-source proxies** — same-host loopback reverse proxies do NOT satisfy trusted-proxy auth.

---

## FAQ

### First 60 Seconds if Something is Broken

1. **Quick status (first check)**: `openclaw status` — fast local summary
2. **Pasteable report (safe to share)**: `openclaw status --all`
3. **Daemon + port state**: `openclaw gateway status`
4. **Deep probes**: `openclaw status --deep` — runs live gateway health probe
5. **Tail the latest log**: `openclaw logs --follow`
6. **Run the doctor**: `openclaw doctor`
7. **Gateway snapshot**: `openclaw health --json` / `openclaw health --verbose`

```bash
openclaw status
openclaw status --all
openclaw gateway status
openclaw status --deep
openclaw logs --follow
openclaw doctor
openclaw health --json
openclaw health --verbose
```

### What is OpenClaw?

**In one paragraph:** OpenClaw is a personal AI assistant you run on your own devices. It replies on the messaging surfaces you already use (WhatsApp, Telegram, Slack, Mattermost, Discord, Google Chat, Signal, iMessage, WebChat) and can also do voice + a live Canvas on supported platforms. The Gateway is the always-on control plane.

**Value proposition:** OpenClaw is a local-first control plane that lets you run a capable assistant on your own hardware, reachable from the chat apps you already use, with stateful sessions, memory, and tools — without handing control of your workflows to a hosted SaaS. Run local models so all data can stay on your device, or use Anthropic/OpenAI/OpenRouter with per-agent routing and failover.

### Skills and Automation

**How to customize skills without keeping the repo dirty:**
Use managed overrides in `~/.openclaw/skills/<name>/SKILL.md` or add a folder via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`. Precedence: `<workspace>/skills` → `<workspace>/.agents/skills` → `~/.agents/skills` → `~/.openclaw/skills` → bundled → `skills.load.extraDirs`.

**How to use different models for different tasks:**
- **Cron jobs**: isolated jobs can set a `model` override per job
- **Sub-agents**: route tasks to separate agents with different default models
- **On-demand switch**: use `/model` to switch the current session model

**The bot freezes while doing heavy work:**
Use **sub-agents** for long or parallel tasks. Set cheaper model for sub-agents via `agents.defaults.subagents.model`.

**How do Discord thread-bound subagent sessions work?**

Use thread bindings. Bind a Discord thread to a subagent or session target so follow-up messages stay on that bound session:
- Spawn with `sessions_spawn` using `thread: true` (and optionally `mode: "session"` for persistent follow-up)
- Or manually bind with `/focus <target>`; use `/agents` to inspect binding state
- Use `/session idle <duration|off>` and `/session max-age <duration|off>` to control auto-unfocus
- Use `/unfocus` to detach the thread

Required config: `session.threadBindings.enabled`, `session.threadBindings.idleHours`, `session.threadBindings.maxAgeHours`. Discord overrides: `channels.discord.threadBindings.enabled`, `channels.discord.threadBindings.idleHours`, `channels.discord.threadBindings.maxAgeHours`. Auto-bind on spawn: `channels.discord.threadBindings.spawnSubagentSessions: true`.

**A subagent finished, but the completion went to the wrong place or never posted:**

Check the resolved requester route first:
- Completion-mode subagent delivery prefers any bound thread or conversation route when one exists
- If the completion origin only carries a channel, OpenClaw falls back to the requester session's stored route (`lastChannel` / `lastTo` / `lastAccountId`)
- If neither a bound route nor a usable stored route exists, delivery can fail and result falls back to queued session delivery
- If the child's last visible assistant reply is exactly `NO_REPLY` / `no_reply` or `ANNOUNCE_SKIP`, OpenClaw intentionally suppresses the announce

Debug: `openclaw tasks show <runId-or-sessionKey>`

**Why did an isolated cron run switch models or retry once?**

That is usually the live model-switch path, not duplicate scheduling. Isolated cron can persist a runtime model handoff and retry when the active run throws `LiveSessionModelSwitchError`. The retry keeps the switched provider/model. After the initial attempt plus 2 switch retries, cron aborts instead of looping forever. Model selection order: Gmail hook override → per-job `model` → stored cron-session model override → normal agent/default selection.

**Can OpenClaw run macOS-only skills from Linux?**

Not directly (macOS skills are gated by `metadata.openclaw.os`). Three supported patterns:

1. **Run the Gateway on a Mac (simplest)**: connect from Linux in remote mode or over Tailscale
2. **Use a macOS node (no SSH)**: pair a macOS node (menubar app) and set Node Run Commands to "Always Ask" or "Always Allow"
3. **Proxy macOS binaries over SSH**: create SSH wrappers for required CLI binaries, override the skill metadata to allow Linux

**Cron or reminders do not fire:**
- Confirm cron is enabled (`cron.enabled`) and `OPENCLAW_SKIP_CRON` is not set
- Check the Gateway is running 24/7 (no sleep/restarts)
- Verify timezone settings for the job (`--tz` vs host timezone)

**Cron fired, but nothing was sent to the channel:**
- `--no-deliver` / `delivery.mode: "none"` means no runner fallback send
- Missing or invalid announce target means outbound was skipped
- A silent isolated result (`NO_REPLY` / `no_reply` only) is treated as intentionally non-deliverable
- Channel auth failures (`unauthorized`, `Forbidden`) mean delivery was tried but credentials blocked it

**Install skills on Linux:**
```bash
openclaw skills search "calendar"
openclaw skills install <skill-slug>
openclaw skills update --all
openclaw skills list --eligible
```

### Where Things Live on Disk

| Item | Location |
|---|---|
| Config | `~/.openclaw/openclaw.json` |
| State directory | `~/.openclaw/` |
| Agent dirs | `~/.openclaw/agents/<agentId>/` |
| Auth profiles | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| Sessions | `~/.openclaw/agents/<agentId>/sessions/` |
| WhatsApp credentials | `~/.openclaw/credentials/whatsapp/<accountId>/creds.json` |
| Task records | `$OPENCLAW_STATE_DIR/tasks/runs.sqlite` |
| Cron jobs | `~/.openclaw/cron/jobs.json` |
| Cron state | `~/.openclaw/cron/jobs-state.json` |
| Media | `~/.openclaw/media/` |
| Logs | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |

---

## Troubleshooting

### First 60 Seconds Triage

Run this exact ladder in order:
```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

**Good output indicators:**
- `openclaw status` → shows configured channels and no obvious auth errors
- `openclaw status --all` → full report, present and shareable
- `openclaw gateway probe` → `Reachable: yes`, `Capability: ...` line. Note: `Read probe: limited - missing scope: operator.read` is degraded diagnostics, not a connect failure. Use `--require-rpc` if you need read-scope RPC proof.
- `openclaw gateway status` → `Runtime: running`, `Connectivity probe: ok`, and a `Capability: ...` line
- `openclaw doctor` → no blocking config/service errors
- `openclaw channels status --probe` → live per-account transport state plus probe/audit results such as `works` or `audit ok`; if gateway is unreachable, falls back to config-only summaries

### Decision Tree

| Symptom | Section |
|---|---|
| No replies | No replies section |
| Dashboard / Control UI won't connect | Control UI section |
| Gateway won't start | Gateway section |
| Channel connects but messages don't flow | Channel flow section |
| Cron or heartbeat didn't fire | Automation section |
| Node is paired but tool fails | Node tools section |
| Browser tool fails | Browser section |

### No Replies

```bash
openclaw status
openclaw gateway status
openclaw channels status --probe
openclaw pairing list --channel <channel>
openclaw logs --follow
```

**Common log signatures:**
- `drop guild message (mention required` → mention gating blocked message
- `pairing request` → sender is unapproved and waiting for DM pairing approval
- `blocked` / `allowlist` in channel logs → sender, room, or group is filtered

### Dashboard / Control UI Won't Connect

**Common log signatures:**
- `device identity required` → non-secure context or missing device auth
- `origin not allowed` → browser `Origin` not in `gateway.controlUi.allowedOrigins`
- `AUTH_TOKEN_MISMATCH` with `canRetryWithDeviceToken=true` → one trusted device-token retry may occur automatically; cached-token retry reuses the cached scope set
- `too many failed authentication attempts (retry later)` → repeated failures from that `Origin` temporarily locked out; another localhost origin uses a separate bucket
- `gateway connect failed:` → UI targeting wrong URL/port

### Gateway Won't Start

**Common log signatures:**
- `Gateway start blocked: set gateway.mode=local` or `existing config is missing gateway.mode` → gateway mode is remote or missing, needs repair
- `refusing to bind gateway ... without auth` → non-loopback bind without valid auth
- `another gateway instance is already listening` or `EADDRINUSE` → port already taken

### Channel Connects but Messages Don't Flow

**Common log signatures:**
- `mention required` → group mention gating blocked processing
- `pairing` / `pending` → DM sender not approved yet
- `not_in_channel`, `missing_scope`, `Forbidden`, `401/403` → channel permission token issue

### Cron or Heartbeat Didn't Fire

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
```

**Common log signatures:**
- `cron: scheduler disabled; jobs will not run automatically` → cron is disabled
- `heartbeat skipped` with `reason=quiet-hours` → outside configured active hours
- `heartbeat skipped` with `reason=empty-heartbeat-file` → HEARTBEAT.md only contains blank/header-only scaffolding
- `heartbeat skipped` with `reason=no-tasks-due` → task mode active but no tasks are due
- `requests-in-flight` → main lane busy; heartbeat wake was deferred

### Node Paired but Tool Fails

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

**Common log signatures:**
- `NODE_BACKGROUND_UNAVAILABLE` → bring node app to foreground
- `*_PERMISSION_REQUIRED` → OS permission was denied/missing
- `SYSTEM_RUN_DENIED: approval required` → exec approval is pending
- `SYSTEM_RUN_DENIED: allowlist miss` → command not on exec allowlist

### Exec Suddenly Asks for Approval

**What changed:**
- If `tools.exec.host` is unset, the default is `auto`
- `host=auto` resolves to `sandbox` when sandbox runtime is active, `gateway` otherwise
- The no-prompt behavior comes from `security=full` plus `ask=off` on gateway/node

**Restore default no-approval behavior:**
```bash
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
```

### Browser Tool Fails

```bash
openclaw browser status
openclaw doctor
```

**Common log signatures:**
- `unknown command "browser"` → `plugins.allow` is set and does not include `browser`
- `Failed to start Chrome CDP on port` → local browser launch failed
- `browser.executablePath not found` → configured binary path is wrong
- `No Chrome tabs found for profile="user"` → Chrome MCP attach profile has no open tabs

### Anthropic Long Context 429

If you see `HTTP 429: rate_limit_error: Extra usage is required for long context requests`, see the gateway troubleshooting doc at `/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context`.

### Local OpenAI-Compatible Backend Fails in OpenClaw

If your local backend answers small direct probes but fails on OpenClaw agent turns:
1. If error mentions `messages[].content` expecting a string: set `models.providers.<provider>.models[].compat.requiresStringContent: true`
2. If backend fails only on OpenClaw agent turns: set `models.providers.<provider>.models[].compat.supportsTools: false`
3. Set `compat.requiresStringContent: true` for string-only Chat Completions backends
4. If tiny direct requests keep passing while OpenClaw agent turns crash: treat as upstream server/model limitation

Additional notes:
- `compat.requiresStringContent: true` handles backends that reject structured Chat Completions content parts
- `compat.supportsTools: false` handles models/backends that cannot handle OpenClaw's tool schema surface reliably

### Plugin Install Fails with Missing openclaw extensions

```json
{
  "name": "@openclaw/my-plugin",
  "version": "1.2.3",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

The plugin package must add `openclaw.extensions` to `package.json`.

---

## Debugging

### Runtime Debug Overrides (`/debug`)

`/debug` is disabled by default; enable with `commands.debug: true`.

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` clears all overrides and returns to the on-disk config.

### Session Trace Output (`/trace`)

Use `/trace` when you want to see plugin-owned trace/debug lines in one session without turning on full verbose mode.

```text
/trace
/trace on
/trace off
```

### Dev Profile + Dev Gateway (`--dev`)

Two `--dev` flags:
- **Global `--dev` (profile)**: isolates state under `~/.openclaw-dev`, defaults gateway port to `19001`
- **`gateway --dev`**: auto-creates a default config + workspace when missing

**Note:** `--dev` is a global profile flag that gets "eaten by some runners" before they can pass it down. Use the env var form instead when needed:
```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

**Dev bootstrap behavior (`gateway --dev`):**
- Writes a minimal config if missing
- Sets `agent.workspace` to the dev workspace
- Seeds workspace files if missing
- Default identity: **C3‑PO** (protocol droid)
- Skips channel providers (`OPENCLAW_SKIP_CHANNELS=1`)

**Reset:**
```bash
pnpm gateway:dev:reset
# Or:
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

### Raw Stream Logging

Enable raw assistant stream logging:
```bash
pnpm gateway:watch --raw-stream
pnpm gateway:watch --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Or via env vars:
```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Default file: `~/.openclaw/logs/raw-stream.jsonl`

**Safety notes**: Raw stream logs can include full prompts, tool output, and user data. Keep logs local and delete after debugging.

### Raw Chunk Logging (pi-mono)

For capturing raw OpenAI-compatible chunks before they are parsed into blocks (pi-mono specific):

```bash
PI_RAW_STREAM=1 openclaw gateway run
PI_RAW_STREAM=1 PI_RAW_STREAM_PATH=~/.openclaw/logs/pi-raw.jsonl openclaw gateway run
```

- `PI_RAW_STREAM=1`: enable raw chunk capture
- `PI_RAW_STREAM_PATH`: custom output path for raw chunks (JSONL format)

This captures chunks at a lower level than `OPENCLAW_RAW_STREAM`, before the pi-mono parser converts them into blocks.

### Gateway Watch Mode

```bash
pnpm gateway:watch
```

This maps to:
```bash
node scripts/watch-node.mjs gateway --force
```

The watcher restarts on build-relevant files under `src/`, extension source files, `tsconfig.json`, `package.json`, and `tsdown.config.ts`.

**Notes:**
- Re-running the same watch command for the same repo/flag set now **replaces** the older watcher instead of leaving duplicate watcher parents behind
- Extension metadata changes restart the gateway without forcing a tsdown rebuild
- Extension metadata changes restart the gateway without forcing a tsdown rebuild

### Temporary CLI Debug Timing

OpenClaw keeps `src/cli/debug-timing.ts` for local investigation. Enable with:

```bash
OPENCLAW_DEBUG_TIMING=1 pnpm openclaw models list --all --provider moonshot
```

Or JSON output:
```bash
OPENCLAW_DEBUG_TIMING=json pnpm openclaw models list --all --provider moonshot \
  2> .artifacts/models-list-timing.jsonl
```

**Clean up before landing:**
```bash
rg 'createCliDebugTiming|debug:[a-z0-9_-]+:' src/commands src/cli \
  --glob '!src/cli/debug-timing.*' \
  --glob '!*.test.ts'
```

---

## Environment Variables

### Precedence (Highest → Lowest)

1. **Process environment** (what the Gateway process already has)
2. **`.env` in the current working directory** (does not override)
3. **Global `.env`** at `~/.openclaw/.env` (does not override)
4. **Config `env` block** in `~/.openclaw/openclaw.json` (applied only if missing)
5. **Optional login-shell import** (`env.shellEnv.enabled` or `OPENCLAW_LOAD_SHELL_ENV=1`)

**Ubuntu compatibility fallback:** On Ubuntu fresh installs using the default state dir, OpenClaw also treats `~/.config/openclaw/gateway.env` as a compatibility fallback after the global `.env`. If both files exist and disagree, OpenClaw keeps `~/.openclaw/.env` and prints a warning.

**Ubuntu compatibility fallback:** On Ubuntu fresh installs that use the default state dir, OpenClaw also treats `~/.config/openclaw/gateway.env` as a compatibility fallback after the global `.env`. If both files exist and disagree, OpenClaw keeps `~/.openclaw/.env` and prints a warning.

### Config `env` Block

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

### Shell Env Import

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalents:
- `OPENCLAW_LOAD_SHELL_ENV=1`
- `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

### Runtime-Injected Env Vars

- `OPENCLAW_SHELL=exec`: set for commands run through the `exec` tool
- `OPENCLAW_SHELL=acp`: set for ACP runtime backend process spawns
- `OPENCLAW_SHELL=acp-client`: set for `openclaw acp client` when it spawns the ACP bridge process
- `OPENCLAW_SHELL=tui-local`: set for local TUI `!` shell commands

### UI Env Vars

- `OPENCLAW_THEME=light`: force the light TUI palette
- `OPENCLAW_THEME=dark`: force the dark TUI palette
- `COLORFGBG`: auto-pick TUI palette from background color hint

### Env Var Substitution in Config

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

### Path-Related Env Vars

| Variable | Purpose |
|---|---|
| `OPENCLAW_HOME` | Override the home directory used for all internal path resolution |
| `OPENCLAW_STATE_DIR` | Override the state directory (default `~/.openclaw`) |
| `OPENCLAW_CONFIG_PATH` | Override the config file path (default `~/.openclaw/openclaw.json`) |
| `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` | Client-side break-glass override: allows plaintext `ws://` to trusted private-network IPs (no config equivalent) |
| `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` | Client-side break-glass override that allows plaintext `ws://` to trusted private-network IPs (no `openclaw.json` equivalent) |

### Logging

| Variable | Purpose |
|---|---|
| `OPENCLAW_LOG_LEVEL` | Override log level for both file and console (e.g. `debug`, `trace`) |

### APNs Environment Variables (iOS Push Relay)

For configuring Apple Push Notification Service (APNs) for local/manual iOS builds (without the hosted relay):

| Variable | Purpose |
|---|---|
| `OPENCLAW_APNS_RELAY_BASE_URL` | Override relay base URL (temporary env override) |
| `OPENCLAW_APNS_RELAY_TIMEOUT_MS` | Override relay timeout in milliseconds |
| `OPENCLAW_APNS_RELAY_ALLOW_HTTP` | Allow HTTP relay URL (loopback-only development escape hatch) |
| `OPENCLAW_APNS_TEAM_ID` | Apple Developer Team ID for direct APNs |
| `OPENCLAW_APNS_KEY_ID` | APNs Key ID |
| `OPENCLAW_APNS_PRIVATE_KEY_P8` | APNs private key content (inline p8 content) |
| `OPENCLAW_APNS_PRIVATE_KEY_PATH` | Path to APNs private key `.p8` file (preferred over inline key) |

### OPENCLAW_CHILD_OOM_SCORE_ADJ

On Linux, OpenClaw biases child processes (supervisor children, PTY shells, MCP stdio servers, Chrome processes) to be killed before the Gateway under OOM pressure. The child's `oom_score_adj` is raised to `1000` via a short `/bin/sh` wrapper before exec.

To disable this behavior for specific child processes, set in the child env:
```bash
OPENCLAW_CHILD_OOM_SCORE_ADJ=0  # or: false, no, off
```

This env var is only checked in the child wrapper; the Gateway itself keeps its normal OOM score.

### nvm Users: web_fetch TLS Failures

If Node.js was installed via **nvm**, the built-in `fetch()` may be missing modern root CAs, causing `web_fetch` to fail with `"fetch failed"` on most HTTPS sites.

On Linux, OpenClaw automatically detects nvm and applies the fix:
- `openclaw gateway install` writes `NODE_EXTRA_CA_CERTS` into the systemd service environment
- The `openclaw` CLI entrypoint re-execs itself with `NODE_EXTRA_CA_CERTS` set before Node startup

**Manual fix:**
```bash
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
openclaw gateway run
```

---

## Scripts Reference

The `scripts/` directory contains helper scripts for local workflows and ops tasks.

**Conventions:**
- Scripts are **optional** unless referenced in docs or release checklists
- Prefer CLI surfaces when they exist
- Assume scripts are host-specific; read them before running on a new machine

**Auth monitoring**: Covered in Authentication docs. Scripts under `scripts/` are optional extras for systemd/Termux phone workflows.

**GitHub read helper** (`scripts/gh-read`):
- Uses GitHub App installation token for repo-scoped read calls
- Required env: `OPENCLAW_GH_READ_APP_ID`, `OPENCLAW_GH_READ_PRIVATE_KEY_FILE`
- Optional: `OPENCLAW_GH_READ_INSTALLATION_ID`, `OPENCLAW_GH_READ_PERMISSIONS`

```bash
scripts/gh-read pr view 123
scripts/gh-read run list -R openclaw/openclaw
scripts/gh-read api repos/openclaw/openclaw/pulls/123
```

---

## Nodes

A **node** is a companion device (macOS/iOS/Android/headless) that connects to the Gateway **WebSocket** with `role: "node"` and exposes a command surface via `node.invoke`.

- Nodes are **peripherals**, not gateways — they don't run the gateway service
- Telegram/WhatsApp/etc. messages land on the **gateway**, not on nodes

### Pairing and Status

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

If a node retries with changed auth details (role/scopes/public key), the prior pending request is superseded and a new `requestId` is created. Re-run `openclaw devices list` before approving.

Notes:
- The device pairing record is the durable approved-role contract. Token rotation stays inside that contract; it cannot upgrade a paired node into a different role that pairing approval never granted.
- `node.pair.*` (CLI: `openclaw nodes pending/approve/reject/rename`) is a separate gateway-owned node pairing store; it does **not** gate the WS `connect` handshake.

**Approval scope:**
- Commandless request: `operator.pairing`
- Non-exec node commands: `operator.pairing` + `operator.write`
- `system.run` / `system.run.prepare` / `system.which`: `operator.pairing` + `operator.admin`

### Remote Node Host (system.run)

Use a **node host** when your Gateway runs on one machine and you want commands to execute on another.

**What runs where:**
- **Gateway host**: receives messages, runs the model, routes tool calls
- **Node host**: executes `system.run`/`system.which` on the node machine
- **Approvals**: enforced on the node host via `~/.openclaw/exec-approvals.json`

**Start a node host (foreground):**
```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

**Remote gateway via SSH tunnel (loopback bind):**
```bash
# Terminal A: forward local 18790 → gateway 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B: export the gateway token and connect through the tunnel
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

**Auth resolution (node host):**
- `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` env vars (preferred)
- `gateway.auth.token` / `gateway.auth.password` config fallback
- In local mode, node host intentionally ignores `gateway.remote.token` / `gateway.remote.password`
- In remote mode, `gateway.remote.token` / `gateway.remote.password` are eligible per remote precedence rules
- If active local `gateway.auth.*` SecretRefs are configured but unresolved, node-host auth fails closed
- Node-host auth resolution only honors `OPENCLAW_GATEWAY_*` env vars

**Start a node host (service):**
```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

**Pair and name:**
```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw nodes status
```

**Naming:**
- `--display-name` on `openclaw node run` / `openclaw node install` (persists in `~/.openclaw/node.json`)
- `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (gateway override)

**Allowlist exec commands (on gateway):**
```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Approvals live on the node host at `~/.openclaw/exec-approvals.json`.

**Configure exec to use the node:**
```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Or per session:
```
/exec host=node security=allowlist node=<id-or-name>
```

**Note**: `host=auto` will not implicitly choose the node. Use explicit `host=node` or set `tools.exec.host=node`.

### Invoking Commands

```bash
# Low-level raw RPC
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

### Screenshots (Canvas Snapshots)

```bash
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

### Canvas Controls

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

### A2UI (Canvas)

```bash
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Only A2UI v0.8 JSONL is supported (v0.9/createSurface is rejected).

### Photos + Videos (Node Camera)

```bash
# List cameras
openclaw nodes camera list --node <idOrNameOrIp>

# Photos (jpg)
openclaw nodes camera snap --node <idOrNameOrIp>            # default: both facings
openclaw nodes camera snap --node <idOrNameOrIp> --facing front

# Video clips (mp4)
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

**Notes:**
- Node must be **foregrounded** for `canvas.*` and `camera.*`
- Clip duration is clamped (`<= 60s`)

### Screen Recordings

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

- Screen recordings are clamped to `<= 60s`
- Use `--screen <index>` to select a display when multiple screens are available

### Location

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

- Location is **off by default**
- Response includes lat/lon, accuracy (meters), and timestamp

### SMS (Android Nodes)

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Wi-Fi-only devices without telephony will not advertise `sms.send`.

### Android Device + Personal Data Commands

Available families (availability depends on device + permissions):
- `device.status`, `device.info`, `device.permissions`, `device.health`
- `notifications.list`, `notifications.actions`
- `photos.latest`
- `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `callLog.search`
- `sms.search`
- `motion.activity`, `motion.pedometer`

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command device.status --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command notifications.list --params '{}'
openclaw nodes invoke --node <idOrNameOrIp> --command photos.latest --params '{"limit":1}'
```

### System Commands (Node Host / Mac Node)

```bash
# Send notification
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"

# Check which binary
openclaw nodes invoke --node <idOrNameOrIp> --command system.which --params '{"name":"git"}'
```

**Notes on `system.run`:**
- `nodes invoke` does not expose `system.run` or `system.run.prepare` — those stay on the exec path only
- `system.run` environment overrides are filtered (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`)
- For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped env overrides are reduced to a small allowlist (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`)
- For approval-backed `host=node` runs, the gateway binds execution to the prepared canonical `systemRunPlan`. If a later caller mutates command/cwd or session metadata before the approved run is forwarded, the gateway rejects as approval mismatch
- On Windows node hosts, shell-wrapper forms like `cmd.exe /c ...` are treated as allowlist misses in allowlist mode unless approved via ask flow
- `system.notify` respects notification permission state
- Supports `--priority <passive|active|timeSensitive>` and `--delivery <system|overlay|auto>`

### Exec Node Binding

```bash
# Global default
openclaw config set tools.exec.node "node-id-or-name"

# Per-agent override
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"

# Unset to allow any node
openclaw config unset tools.exec.node
```

### Headless Node Host (Cross-Platform)

```bash
openclaw node run --host <gateway-host> --port 18789
```

- Pairing is still required
- Node host stores its info in `~/.openclaw/node.json`
- Exec approvals enforced locally via `~/.openclaw/exec-approvals.json`
- Add `--tls` / `--tls-fingerprint` when the Gateway WS uses TLS

### Mac Node Mode

The macOS menubar app connects to the Gateway WS server as a node. In remote mode, the app opens an SSH tunnel for the Gateway port and connects to `localhost`.

---

## Diagnostics Export

OpenClaw can create a local diagnostics zip safe to attach to bug reports:

```bash
openclaw gateway diagnostics export
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
openclaw gateway diagnostics export --json
```

The zip includes: `summary.md`, `diagnostics.json`, `manifest.json`, sanitized config shape, redacted log summaries, best-effort gateway status/health snapshots, and `stability/latest.json` (newest persisted stability bundle). The export is useful even when the gateway is unhealthy.

**Privacy model**: The export omits chat text, prompts, credentials, API keys, tokens, raw request/response bodies, account/message/session IDs, hostnames, and local usernames. It keeps operational metadata (subsystem names, plugin/provider/channel IDs, status codes, durations, byte counts, queue state, memory readings).

**Stability recorder** (enabled by default): records bounded, payload-free stability stream. Inspect with `openclaw gateway stability` or `--type payload.large` or `--json`. After fatal exit/restart failure: `openclaw gateway stability --bundle latest`. Create zip from latest bundle: `openclaw gateway stability --bundle latest --export`. Persisted bundles live under `~/.openclaw/logs/stability/`. Disable with `diagnostics.enabled: false`.

## Diagnostics Flags

Diagnostics flags enable targeted debug logs without turning on verbose logging everywhere. Flags are opt-in and case-insensitive.

Wildcards supported:
- `telegram.*` matches `telegram.http`
- `*` enables all flags

### Enable via Config

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Multiple flags:
```json
{
  "diagnostics": {
    "flags": ["telegram.http", "gateway.*"]
  }
}
```

Restart the gateway after changing flags.

### Env Override (One-off)

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Disable all flags:
```bash
OPENCLAW_DIAGNOSTICS=0
```

### Where Logs Go

Default: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

If you set `logging.file`, use that path instead. Logs are JSONL (one JSON object per line). Redaction still applies based on `logging.redactSensitive`.

### Extract Logs

```bash
# Pick the latest log file
ls -t /tmp/openclaw/openclaw-*.log | head -n 1

# Filter for Telegram HTTP diagnostics
rg "telegram http error" /tmp/openclaw/openclaw-*.log

# Tail while reproducing
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"

# For remote gateways
openclaw logs --follow
```

**Notes:**
- If `logging.level` is set higher than `warn`, these logs may be suppressed
- Flags are safe to leave enabled; they only affect log volume for the specific subsystem

---

## CI Pipeline

The CI runs on every push to `main` and every pull request. It uses smart scoping to skip expensive jobs when only unrelated areas changed.

Additional workflows:
- **QA Lab**: dedicated lanes outside main smart-scoped workflow. `Parity gate` runs on matching PR changes; `QA-Lab - All Lanes` runs nightly on `main`. Live jobs use `qa-live-shared` environment.
- **Duplicate PRs After Merge**: manual maintainer workflow for post-land duplicate cleanup. Defaults to dry-run; `apply=true` to close.
- **Docs Agent**: event-driven Codex lane for keeping docs aligned with landed changes. Triggered by successful non-bot push CI on `main`; skips when main has moved on or another run created in last hour.
- **Test Performance Agent**: event-driven Codex lane for slow tests. Skips if another run already ran that UTC day. Makes small coverage-preserving performance fixes, reruns full-suite report, rejects changes that reduce passing baseline.

### Job Overview

| Job | Purpose | When it runs |
|---|---|---|
| `preflight` | Detect docs-only changes, changed scopes, changed extensions, build CI manifest | Always on non-draft pushes and PRs |
| `security-scm-fast` | Private key detection and workflow audit via `zizmor` | Always |
| `security-dependency-audit` | Dependency-free production lockfile audit against npm advisories | Always |
| `security-fast` | Required aggregate for the fast security jobs | Always |
| `build-artifacts` | Build `dist/`, Control UI, built-artifact checks, and reusable downstream artifacts | Node-relevant changes |
| `checks-fast-core` | Fast Linux correctness lanes (bundled/plugin-contract/protocol checks) | Node-relevant changes |
| `checks-fast-contracts-channels` | Sharded channel contract checks with stable aggregate | Node-relevant changes |
| `checks-node-extensions` | Full bundled-plugin test shards across extension suite | Node-relevant changes |
| `checks-node-core-test` | Core Node test shards, excluding channel/bundled/contract/extension | Node-relevant changes |
| `extension-fast` | Focused tests for only changed bundled plugins | PRs with extension changes |
| `check` | Sharded main local gate: prod types, lint, guards, test types, strict smoke | Node-relevant changes |
| `check-additional` | Architecture, boundary, extension-surface, package-boundary, gateway-watch shards | Node-relevant changes |
| `build-smoke` | Built-CLI smoke tests and startup-memory smoke | Node-relevant changes |
| `checks` | Verifier for built-artifact channel tests plus push-only Node 22 compat | Node-relevant changes |
| `check-docs` | Docs formatting, lint, and broken-link checks | Docs changed |
| `skills-python` | Ruff + pytest for Python-backed skills | Python-skill-relevant changes |
| `checks-windows` | Windows-specific test lanes | Windows-relevant changes |
| `macos-node` | macOS TypeScript test lane using shared built artifacts | macOS-relevant changes |
| `macos-swift` | Swift lint, build, and tests for the macOS app | macOS-relevant changes |
| `android` | Android unit tests for both flavors plus one debug APK build | Android-relevant changes |
| `test-performance-agent` | Daily Codex slow-test optimization after trusted activity | Main CI success or manual dispatch |

### Fail-Fast Order

1. `preflight` decides which lanes exist
2. `security-*`, `check`, `check-additional`, `check-docs`, `skills-python` fail quickly
3. `build-artifacts` overlaps with fast Linux lanes
4. Heavier platform and runtime lanes fan out after that

Scope logic: `scripts/ci-changed-scope.mjs` (unit tests in `src/scripts/ci-changed-scope.test.ts`).

### Runners

| Runner | Jobs |
|---|---|
| `ubuntu-24.04` | `preflight`, fast security jobs, fast protocol/contract/bundled checks, check shards except lint, docs checks |
| `blacksmith-8vcpu-ubuntu-2404` | `build-artifacts`, build-smoke, Linux Node test shards, bundled plugin test shards, `android` |
| `blacksmith-16vcpu-ubuntu-2404` | `check-lint`, install-smoke Docker builds |
| `blacksmith-16vcpu-windows-2025` | `checks-windows` |
| `blacksmith-6vcpu-macos-latest` | `macos-node` |
| `blacksmith-12vcpu-macos-latest` | `macos-swift` |

### Local Equivalents

```bash
pnpm changed:lanes   # inspect the local changed-lane classifier
```

CI concurrency key is versioned (`CI-v7-*`) so zombie queued groups don't block newer main runs.

---

## RPC Adapters

OpenClaw integrates external CLIs via JSON-RPC using two patterns.

### Pattern A: HTTP Daemon (signal-cli)

- `signal-cli` runs as a daemon with JSON-RPC over HTTP
- Event stream is SSE (`/api/v1/events`)
- Health probe: `/api/v1/check`
- OpenClaw owns lifecycle when `channels.signal.autoStart=true`

### Pattern B: stdio Child Process (legacy: imsg)

> **Note**: For new iMessage setups, use [BlueBubbles](/channels/bluebubbles) instead.

- OpenClaw spawns `imsg rpc` as a child process (legacy iMessage integration)
- JSON-RPC is line-delimited over stdin/stdout
- No TCP port, no daemon required

Core methods:
- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (probe/diagnostics)

### Adapter Guidelines

- Gateway owns the process (start/stop tied to provider lifecycle)
- Keep RPC clients resilient: timeouts, restart on exit
- Prefer stable IDs (e.g., `chat_id`) over display strings
