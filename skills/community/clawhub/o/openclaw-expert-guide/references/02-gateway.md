# OpenClaw Gateway — Complete Reference

> Compiled from all 39 official Gateway documentation pages at docs.openclaw.ai/gateway

---

## Table of Contents
- [Gateway Runbook (Overview)](#gateway-runbook-overview)
- [Authentication](#authentication)
- [Background Process (exec & process tools)](#background-process-exec--process-tools)
- [Bonjour / mDNS Discovery](#bonjour--mdns-discovery)
- [Bridge Protocol (REMOVED)](#bridge-protocol-removed)
- [CLI Backends](#cli-backends)
- [Config — Agents](#config--agents)
- [Config — Channels](#config--channels)
- [Config — Tools](#config--tools)
- [Configuration](#configuration)
- [Configuration Examples](#configuration-examples)
- [Configuration Reference](#configuration-reference)
- [Diagnostics Export](#diagnostics-export)
- [Discovery & Transports](#discovery--transports)
- [Doctor](#doctor)
- [Gateway Lock](#gateway-lock)
- [Health Checks](#health-checks)
- [Heartbeat](#heartbeat)
- [Local Models](#local-models)
- [Logging](#logging)
- [Multiple Gateways](#multiple-gateways)
- [Network Model](#network-model)
- [OpenAI Chat Completions HTTP API](#openai-chat-completions-http-api)
- [OpenResponses HTTP API](#openresponses-http-api)
- [OpenShell](#openshell)
- [Gateway-Owned Pairing](#gateway-owned-pairing)
- [Gateway Protocol](#gateway-protocol)
- [Remote Access](#remote-access)
- [Remote Gateway Setup (macOS)](#remote-gateway-setup-macos)
- [Sandboxing](#sandboxing)
- [Sandbox vs Tool Policy vs Elevated](#sandbox-vs-tool-policy-vs-elevated)
- [Secrets Management](#secrets-management)
- [Secrets Plan Contract](#secrets-plan-contract)
- [Security](#security)
- [Security Audit Checks](#security-audit-checks)
- [Tailscale](#tailscale)
- [Tools Invoke HTTP API](#tools-invoke-http-api)
- [Troubleshooting](#troubleshooting)
- [Trusted Proxy Auth](#trusted-proxy-auth)

## Gateway Runbook (Overview)

### What it is
The Gateway is OpenClaw's single always-on process for routing, control plane, and channel connections. It serves as the central hub multiplexing WebSocket control/RPC, HTTP APIs, Control UI, and hooks on a single port.

### Runtime Model
- **Single multiplexed port** for: WebSocket control/RPC, HTTP APIs (OpenAI-compatible), Control UI, hooks
- **Default bind**: `loopback` (127.0.0.1)
- **Default port**: `18789`
- **Auth required by default** — shared-secret or trusted-proxy

### Port and Bind Precedence

| Setting | Resolution order |
|---------|-----------------|
| Gateway port | `--port` → `OPENCLAW_GATEWAY_PORT` → `gateway.port` → `18789` |
| Bind mode | CLI/override → `gateway.bind` → `loopback` |

### 5-Minute Startup
```bash
openclaw gateway --port 18789
openclaw gateway --port 18789 --verbose  # debug/trace
openclaw gateway --force                  # force-kill listener, then start
openclaw gateway status
openclaw status
openclaw logs --follow
openclaw channels status --probe
```

### Hot Reload Modes

| `gateway.reload.mode` | Behavior |
|----------------------|----------|
| `off` | No config reload |
| `hot` | Apply only hot-safe changes |
| `restart` | Restart on reload-required changes |
| `hybrid` (default) | Hot-apply when safe, restart when required |

### Operator Commands
```bash
openclaw gateway status
openclaw gateway status --deep   # system-level service scan (LaunchDaemons/systemd/schtasks), NOT a deeper RPC probe
openclaw gateway status --require-rpc  # need read-scope RPC proof, not just reachability
openclaw gateway status --json
openclaw gateway probe           # can warn about "multiple reachable gateways"
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw secrets reload
openclaw logs --follow
openclaw doctor
```

**Environment overrides for isolated instances:**
- `OPENCLAW_CONFIG_PATH` — config file path
- `OPENCLAW_STATE_DIR` — state directory
- `OPENCLAW_SKIP_CHANNELS=1` — skip channel initialization (useful for VoiceClaw-only test gateways)

### OpenAI-Compatible Endpoints
- `GET /v1/models` — returns agent targets (`openclaw`, `openclaw/default`, `openclaw/<agentId>`)
- `GET /v1/models/{id}`
- `POST /v1/embeddings`
- `POST /v1/chat/completions`
- `POST /v1/responses`

### VoiceClaw Real-Time Brain
- Endpoint: `/voiceclaw/realtime` (WebSocket)
- Uses Gemini Live for real-time audio
- Requires `GEMINI_API_KEY`
- Tool calls return immediate "working" result, then async execution

### Notes
- By default, the Gateway refuses to start unless `gateway.mode=local` is set in config. Use `--allow-unconfigured` for ad-hoc/dev runs **without** modifying the config file.
- `SIGUSR1` triggers an in-process restart when authorized. `commands.restart` is enabled by default; set `commands.restart: false` to block manual SIGUSR1 restarts while still allowing gateway tool/config apply/update.

### Common Failure Signatures

| Signature | Likely issue |
|-----------|-------------|
| `refusing to bind gateway ... without auth` | Non-loopback bind without auth |
| `another gateway instance is already listening` / `EADDRINUSE` | Port conflict |
| `Gateway start blocked: set gateway.mode=local` | Config set to remote mode |
| `unauthorized` during connect | Auth mismatch |

### Supervision
- **macOS**: launchd (`ai.openclaw.gateway` label)
- **Linux**: systemd user unit
- **Windows**: Scheduled Task or Startup-folder fallback

```bash
# macOS
openclaw gateway install
openclaw gateway status

# Linux
openclaw gateway install
systemctl --user enable --now openclaw-gateway.service
sudo loginctl enable-linger <user>  # for persistence

# Dev profile
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
```

---

## Authentication

### What it is
Covers **model provider** authentication (API keys, OAuth, Claude CLI reuse). For gateway connection auth, see Configuration and Trusted Proxy Auth.

### API Key Setup (Recommended)
```bash
export <PROVIDER>_API_KEY="..."
# For daemon (systemd/launchd):
cat >> ~/.openclaw/.env <<'EOF'
<PROVIDER>_API_KEY=...
EOF
openclaw models status
```

### Claude CLI Reuse (Anthropic)
```bash
claude auth login
claude auth status --text
openclaw models auth login --provider anthropic --method cli --set-default
```

### API Key Rotation
Priority order:
1. `OPENCLAW_LIVE_<PROVIDER>_KEY` (single override)
2. `<PROVIDER>_API_KEYS`
3. `<PROVIDER>_API_KEY`
4. `<PROVIDER>_API_KEY_*`
- Google providers add `GOOGLE_API_KEY` as fallback
- Retries only on rate-limit errors (429, quota, throttle, concurrency)

### Per-Session Credential Control
```
/model <alias>@<profileId>
```

### Per-Agent Auth Order
```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

### Automation Check
```bash
openclaw models status --check   # exit 1=expired/missing, 2=expiring
openclaw models status --probe   # live probes
```

### Auth Profile Refs
- `api_key` credentials: `keyRef: { source, provider, id }`
- `token` credentials: `tokenRef: { source, provider, id }`
- OAuth profiles reject SecretRef input

---

## Background Process (exec & process tools)

### exec Tool Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `command` | required | Shell command |
| `yieldMs` | 10000 | Auto-background after this delay |
| `background` | false | Background immediately |
| `timeout` | 1800s | Kill after timeout |
| `elevated` | false | Run outside sandbox |
| `pty` | false | Real TTY |
| `workdir` | — | Working directory |
| `env` | — | Environment overrides |

### Config Keys
| Key | Default | Description |
|-----|---------|-------------|
| `tools.exec.backgroundMs` | 10000 | Auto-background delay |
| `tools.exec.timeoutSec` | 1800 | Process timeout |
| `tools.exec.cleanupMs` | 1800000 | Cleanup delay |
| `tools.exec.notifyOnExit` | true | System event on exit |
| `tools.exec.notifyOnExitEmptySuccess` | false | Notify on clean exit |

### process Tool Actions
- `list` — running + finished sessions
- `poll` — drain new output (reports exit status)
- `log` — read aggregated output (offset + limit; default last 200 lines)
- `write` — send stdin (data, optional eof)
- `send-keys` — explicit key tokens to PTY
- `submit` — send Enter to PTY
- `paste` — literal text with optional bracketed paste
- `kill` — terminate background session
- `clear` — remove finished session
- `remove` — kill if running, clear if finished

### Important Notes
- Sessions scoped per agent
- Lost on process restart (no disk persistence)
- Logs saved to chat only if polled
- `OPENCLAW_SHELL=exec` set in spawned commands

---

## Bonjour / mDNS Discovery

### What it is
Uses mDNS/DNS-SD to discover Gateway via `_openclaw-gw._tcp` service type. LAN-only multicast via bundled bonjour plugin (enabled by default).

### Wide-Area Bonjour (Tailscale)
```json5
{
  gateway: { bind: "tailnet" },
  discovery: { wideArea: { enabled: true } },
}
```
```bash
openclaw dns setup --apply
```

### TXT Keys (non-secret hints)
`role`, `displayName`, `lanHost`, `gatewayPort`, `gatewayTls`, `gatewayTlsSha256`, `canvasPort`, `transport`, `tailnetDns`, `sshPort`, `cliPath`

### Disabling
```bash
openclaw plugins disable bonjour
# or
OPENCLAW_DISABLE_BONJOUR=1
```

---

## Bridge Protocol (REMOVED)

**TCP bridge has been removed** from current builds. `bridge.*` config keys no longer in schema. Historical reference only. Current clients use WebSocket Gateway Protocol.

---

## CLI Backends

### What it is
Local AI CLIs as text-only fallback when API providers are down. Conservative safety net, not primary path.

### Bundled Backends
- `codex-cli` (OpenAI plugin)
- `claude-cli` (Anthropic)
- `google-gemini-cli` (Google)

### Configuration
```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "codex-cli": {
          command: "/opt/homebrew/bin/codex",
        },
      },
    },
  },
}
```

### Key Config Fields
| Field | Description |
|-------|-------------|
| `command` | Path to CLI binary |
| `args` | CLI arguments |
| `output` | `json` (default), `jsonl`, `text` |
| `input` | `arg` (default), `stdin` |
| `modelArg` | Model flag (e.g. `--model`) |
| `sessionArg` | Session ID flag |
| `sessionMode` | `always`, `existing`, `none` |
| `bundleMcp` | Enable loopback MCP bridge for gateway tools |
| `imageArg` | Image file path flag |

### bundleMcp
When `true`, spawns loopback HTTP MCP server exposing gateway tools to the CLI. Authenticated per-session.

---

## Config — Agents

### Workspace & Bootstrap
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      repoRoot: "~/Projects/openclaw",
      skipBootstrap: false,
      contextInjection: "always",  // or "continuation-skip"
      bootstrapMaxChars: 12000,
      bootstrapTotalMaxChars: 60000,
    },
  },
}
```

### Model Configuration
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
      },
      imageModel: { primary: "..." },
      imageGenerationModel: { primary: "openai/gpt-image-2" },
      videoGenerationModel: { primary: "qwen/wan2.6-t2v" },
      pdfModel: { primary: "anthropic/claude-opus-4-6" },
    },
  },
}
```

### Built-in Aliases
| Alias | Model |
|-------|-------|
| `opus` | `anthropic/claude-opus-4-6` |
| `sonnet` | `anthropic/claude-sonnet-4-6` |
| `gpt` | `openai/gpt-5.4` |
| `gpt-mini` | `openai/gpt-5.4-mini` |
| `gpt-nano` | `openai/gpt-5.4-nano` |
| `gemini` | `google/gemini-3.1-pro-preview` |
| `gemini-flash` | `google/gemini-3-flash-preview` |
| `gemini-flash-lite` | `google/gemini-3.1-flash-lite-preview` |

### Embedded Harness
```json5
{
  agents: {
    defaults: {
      embeddedHarness: {
        runtime: "auto",  // auto | pi | <harness-id>
        fallback: "pi",   // pi | none
      },
    },
  },
}
```

### Context Budget Keys
- `agents.defaults.bootstrapMaxChars` / `bootstrapTotalMaxChars` — workspace bootstrap
- `agents.defaults.startupContext.*` — /new and /reset prelude
- `skills.limits.maxSkillsPromptChars` — skills list injection
- `agents.defaults.contextLimits.*` — runtime excerpts
- `memory.qmd.limits.*` — memory search snippets

### Other Key Settings
- `maxConcurrent`: 4 (default) — max parallel agent runs
- `imageMaxDimensionPx`: 1200 — image downscaling
- `userTimezone` — system prompt timezone
- `timeFormat`: `auto` | `12` | `24`

---

## Config — Channels

### DM Policies
| Policy | Behavior |
|--------|----------|
| `pairing` (default) | One-time pairing code; owner approves |
| `allowlist` | Only senders in `allowFrom` |
| `open` | Allow all (requires `allowFrom: ["*"]`) |
| `disabled` | Ignore all DMs |

### Group Policies
| Policy | Behavior |
|--------|----------|
| `allowlist` (default) | Only matching allowlist |
| `open` | Bypass allowlists (mention-gating applies) |
| `disabled` | Block all group messages |

### Channel Model Overrides
```json5
{
  channels: {
    modelByChannel: {
      telegram: { "-1001234567890": "openai/gpt-4.1-mini" },
    },
  },
}
```

### WhatsApp
- Multi-account via `accounts` sub-object
- `sendReadReceipts`, `textChunkLimit`, `mediaMaxMb`
- Groups: `requireMention`, `groupPolicy`, `groupAllowFrom`

### Telegram
- `botToken`, topics support, `customCommands`
- Streaming modes: `off` | `partial` | `block` | `progress`
- Proxy: `proxy: "socks5://localhost:9050"`
- Webhook: `webhookUrl`, `webhookSecret`, `webhookPath`

### Discord
- Guilds with channels, voice, `threadBindings`
- `execApprovals` with approvers and target (dm/channel/both)
- Components v2 with `ui.components.accentColor`
- Voice with auto-join and DAVE encryption

### Slack
- Socket mode: `botToken` + `appToken`
- HTTP mode: `botToken` + `signingSecret`
- Native streaming, slash commands
- `execApprovals` similar to Discord

---

## Config — Tools

### Tool Profiles
| Profile | Includes |
|---------|----------|
| `minimal` | `session_status` only |
| `coding` | fs, runtime, web, sessions, memory, cron, image tools |
| `messaging` | messaging, sessions_list/history/send, session_status |
| `full` | No restriction |

### Tool Groups
| Group | Tools |
|-------|-------|
| `group:runtime` | exec, process, code_execution |
| `group:fs` | read, write, edit, apply_patch |
| `group:sessions` | sessions_list/history/send/spawn/yield, subagents, session_status |
| `group:memory` | memory_search, memory_get |
| `group:web` | web_search, x_search, web_fetch |
| `group:ui` | browser, canvas |
| `group:automation` | cron, gateway |
| `group:messaging` | message |
| `group:nodes` | nodes |
| `group:agents` | agents_list |
| `group:media` | image, image_generate, video_generate, tts |
| `group:openclaw` | All built-in tools |

### Allow/Deny
```json5
{ tools: { deny: ["browser", "canvas"] } }
```
- `deny` always wins
- Non-empty `allow` = everything else blocked
- Case-insensitive, supports `*` wildcards

### Per-Provider Tool Restrictions
```json5
{
  tools: {
    byProvider: {
      "openai/gpt-5.4": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

### Elevated Exec
```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["1234567890123"],
      },
    },
  },
}
```

### Loop Detection
```json5
{
  tools: {
    loopDetection: {
      enabled: true,  // disabled by default
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
    },
  },
}
```

### Custom Providers
```json5
{
  models: {
    mode: "merge",  // merge | replace
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions",  // openai-responses | anthropic-messages | google-generative-ai
        models: [{ id: "llama-3.1-8b", contextWindow: 128000, maxTokens: 32000 }],
      },
    },
  },
}
```

---

## Configuration

### What it is
JSON5 config at `~/.openclaw/openclaw.json`. Strict validation — unknown keys refuse startup.

### Editing Methods
1. `openclaw onboard` / `openclaw configure` — interactive wizard
2. `openclaw config get/set/unset` — CLI one-liners
3. Control UI at `http://127.0.0.1:18789` — Config tab
4. Direct edit — file watched for hot reload

### Strict Validation
- Unknown keys = Gateway refuses to start
- Only `$schema` allowed as unknown root key
- Run `openclaw doctor` to diagnose, `openclaw doctor --fix` to repair
- Last-known-good recovery: broken config saved as `.clobbered.*`
- **Plugin-local failures:** When every validation issue is scoped to `plugins.entries.<id>...`, OpenClaw does **not** perform whole-file recovery. It surfaces the plugin-local failure so a plugin schema mismatch cannot roll back unrelated user settings.
- Promotion to last-known-good is skipped when a candidate contains redacted secret placeholders (`***`).
- **Symlink warning:** Symlinked `openclaw.json` is unsupported for OpenClaw-owned writes; an atomic write may replace the path instead of preserving the symlink. Use `OPENCLAW_CONFIG_PATH` to point directly at the real file.
- `openclaw config schema` prints the canonical JSON Schema. `config.schema.lookup` fetches a single path-scoped node plus child summaries for drill-down tooling.

### $include (Config Splitting)
```json5
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: { $include: ["./clients/a.json5", "./clients/b.json5"] },
}
```
- Single file: replaces containing object
- Array: deep-merged in order
- Nested: up to 10 levels

---

## Configuration Examples

### Minimal
```json5
{
  agent: { workspace: "~/.openclaw/workspace" },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

### Multi-Platform
```json5
{
  channels: {
    whatsapp: { allowFrom: ["+15555550123"] },
    telegram: { enabled: true, botToken: "...", allowFrom: ["123456789"] },
    discord: { enabled: true, token: "...", dm: { allowFrom: ["123456789012345678"] } },
  },
}
```

### Secure DM Mode
```json5
{
  session: { dmScope: "per-channel-peer" },
  channels: {
    whatsapp: { dmPolicy: "allowlist", allowFrom: ["+1...", "+1..."] },
  },
}
```

---

## Configuration Reference

### Top-Level Sections
- `agents.*` → see Config — Agents
- `channels.*` → see Config — Channels
- `tools.*` → see Config — Tools
- `gateway.*` → Gateway runtime
- `session.*` → Session lifecycle
- `messages.*` → Message delivery
- `talk.*` → Talk mode
- `models.*` → Custom providers
- `skills.*` — skill allowlists, install prefs, entries
- `plugins.*` — plugin enable/disable, config, hooks
- `browser.*` — browser profiles, SSRF policy
- `cron.*` — scheduled jobs
- `hooks.*` — webhook endpoints
- `logging.*` — log level, file, redaction

### Gateway Section
```json5
{
  gateway: {
    mode: "local",          // local | remote
    port: 18789,
    bind: "loopback",       // auto | loopback | lan | tailnet | custom
    auth: {
      mode: "token",        // none | token | password | trusted-proxy
      token: "your-token",
      allowTailscale: true,
      rateLimit: { maxAttempts: 10, windowMs: 60000, lockoutMs: 300000 },
    },
    tailscale: { mode: "off" },  // off | serve | funnel
    controlUi: { enabled: true, basePath: "/openclaw" },
    remote: { url: "ws://...", token: "..." },
    trustedProxies: ["10.0.0.1"],
    channelHealthCheckMinutes: 5,
    channelStaleEventThresholdMinutes: 30,
    channelMaxRestartsPerHour: 10,
  },
}
```

---

## Diagnostics Export

### Quick Start
```bash
openclaw gateway diagnostics export
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
openclaw gateway diagnostics export --json
```

### Contents
- `summary.md` — human-readable overview
- `diagnostics.json` — machine-readable
- Sanitized config shape (no secrets)
- Sanitized log summaries
- Stability bundle

### Stability Recorder
```bash
openclaw gateway stability
openclaw gateway stability --bundle latest
openclaw gateway stability --bundle latest --export
```

Set `diagnostics.enabled: false` to disable the stability recorder entirely.

### Privacy Model
- Keeps: subsystem names, status codes, durations, byte counts
- Omits: chat text, credentials, tokens, raw bodies, account IDs

---

## Discovery & Transports

### Discovery Inputs
1. **Bonjour/DNS-SD** — LAN multicast + optional wide-area unicast
2. **Tailnet** — MagicDNS name or stable IP
3. **Manual/SSH** — SSH tunnel fallback

### Transport Selection (Recommended)
1. Paired direct endpoint if reachable → use it
2. Discovery finds gateway → offer "Use this gateway"
3. Tailnet DNS/IP configured → try direct
4. Fall back to SSH

---

## Doctor

### What it is
Repair + migration tool. Fixes stale config/state, checks health, provides repair steps.

```bash
openclaw doctor              # interactive
openclaw doctor --yes        # accept all defaults
openclaw doctor --repair     # apply recommended repairs
openclaw doctor --deep       # scan system services
openclaw doctor --non-interactive  # safe migrations only
```

### What it Does
- Config normalization for legacy values
- Legacy state migrations (sessions, agent dir, WhatsApp auth)
- Model auth health (OAuth expiry check/refresh)
- Sandbox image repair
- Service config audit
- Security warnings for open DM policies
- Shell completion auto-install
- Memory search embedding readiness check

---

## Gateway Lock

### Mechanism
- Gateway binds WebSocket listener exclusively on startup
- `EADDRINUSE` → throws `GatewayLockError`
- OS releases listener on any process exit (crashes, SIGKILL)
- No separate lock file needed

---

## Health Checks

### Quick Checks
```bash
openclaw status              # local summary
openclaw status --all        # full diagnosis
openclaw status --deep       # live health probe
openclaw health              # gateway health snapshot
openclaw health --verbose    # force live probe
openclaw health --json       # machine-readable
```

### Health Monitor Config
| Key | Default | Description |
|-----|---------|-------------|
| `gateway.channelHealthCheckMinutes` | 5 | Check interval (0 disables) |
| `gateway.channelStaleEventThresholdMinutes` | 30 | Idle threshold |
| `gateway.channelMaxRestartsPerHour` | 10 | Restart cap |

### Per-Channel Override
```json5
{
  channels: {
    telegram: { healthMonitor: { enabled: false } },
  },
}
```

---

## Heartbeat

### What it is
Periodic agent turns in the main session so the model can surface anything needing attention.

### Configuration
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",             // default; 1h for Anthropic OAuth/CLI
        target: "last",           // none | last | <channel-id>
        to: "+15551234567",       // optional recipient override (E.164 for WhatsApp, Telegram chat id, or topic format)
        accountId: "ops-bot",     // optional account id for multi-account channels
        session: "main",          // optional session key: "main" (default) or explicit session key
        directPolicy: "allow",    // allow | block
        lightContext: false,       // only inject HEARTBEAT.md
        isolatedSession: false,    // fresh session each run
        includeReasoning: false,   // deliver separate Reasoning: message when available
        suppressToolErrorWarnings: false, // suppress tool error warning payloads during heartbeat runs
        model: "anthropic/claude-opus-4-6",
        prompt: "Read HEARTBEAT.md...",
        ackMaxChars: 300,
        activeHours: { start: "09:00", end: "22:00", timezone: "America/New_York" },
      },
    },
  },
}
```

### Response Contract
- Nothing to report → reply `HEARTBEAT_OK`
- `HEARTBEAT_OK` at start/end stripped if remaining ≤ `ackMaxChars`
- Alerts → do NOT include `HEARTBEAT_OK`

### activeHours Timezone Options
- Omitted / `"user"`: uses `agents.defaults.userTimezone` if set, otherwise host timezone
- `"local"`: always uses the host system timezone
- Any IANA identifier (e.g. `"America/New_York"`): used directly
- **⚠️ Zero-width window gotcha:** Do NOT set `start` and `end` to the same time (e.g., `08:00` to `08:00`). This is treated as a zero-width window, so heartbeats will always be skipped.

### HEARTBEAT.md Tasks Block
```md
tasks:
- name: inbox-triage
  interval: 30m
  prompt: "Check for urgent unread emails."
- name: calendar-scan
  interval: 2h
  prompt: "Check for upcoming meetings."
```

Tasks behavior:
- Only **due** tasks are included in each heartbeat tick.
- If no tasks are due, the heartbeat is **skipped entirely** (`reason=no-tasks-due`) to avoid a wasted model call.
- Task timestamps are only advanced after a heartbeat run completes its **normal reply path**. Skipped runs (`empty-heartbeat-file` or `no-tasks-due`) do **NOT** mark tasks as completed.

### HEARTBEAT.md Empty Detection
If `HEARTBEAT.md` exists but is effectively empty (only blank lines and markdown headers like `# Heading`), OpenClaw skips the heartbeat run (`reason=empty-heartbeat-file`) to save API calls.

### Visibility Controls
```yaml
channels:
  defaults:
    heartbeat:
      showOk: false      # suppress OK acks
      showAlerts: true    # deliver alerts
      useIndicator: true  # emit indicator events
  telegram:
    heartbeat:
      showOk: true       # show OK acks on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false  # suppress alerts for this account
```

**Precedence:** per-account → per-channel → channel defaults → built-in defaults

If **all three** flags (`showOk`, `showAlerts`, `useIndicator`) are false, OpenClaw skips the heartbeat run entirely (no model call).

### Per-Agent Heartbeats
If any `agents.list[]` entry includes a `heartbeat` block, **only those agents** run heartbeats. The per-agent block merges on top of `agents.defaults.heartbeat`.

### Queue and Delivery Behavior
- If the main queue is busy, the heartbeat is **skipped** and retried later.
- If the resolved heartbeat target supports typing, OpenClaw **shows typing** while the heartbeat run is active (disabled by `typingMode: "never"`).
- **Background task wake:** Detached background tasks can enqueue a system event to wake heartbeat when the main session should notice something quickly. That wake does not make the heartbeat run a background task.
- **Control UI/WebChat:** Heartbeat prompts and OK-only acks are hidden in history. The session transcript still contains those turns for audit/replay.
- **Stray HEARTBEAT_OK:** Outside heartbeat runs, `HEARTBEAT_OK` at start/end of a message is stripped and logged; a message that is only `HEARTBEAT_OK` is dropped.

### Heartbeat Session Keep-alive
Heartbeat-only replies do **not** keep the session alive. The last `updatedAt` timestamp is restored after a heartbeat run, so idle expiry behaves normally.

### Manual Wake (On-Demand)
To trigger an immediate heartbeat run:
```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

---

## Local Models

### Requirements
- Aim for ≥2 maxed-out Mac Studios or equivalent (~$30k+)
- Single 24GB GPU works for lighter prompts
- Use largest model variant you can run

### LM Studio Setup (Recommended)
```json5
{
  agents: { defaults: { model: { primary: "lmstudio/my-local-model" } } },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [{ id: "my-local-model", contextWindow: 196608, maxTokens: 8192 }],
      },
    },
  },
}
```

### Compatibility Notes
- `compat.requiresStringContent: true` for string-only backends
- `compat.supportsTools: false` for backends that can't handle tool schemas
- Context warning at <32k, blocked at <16k

---

## Logging

### Two Surfaces
- **Console output** — controlled by `logging.consoleLevel` and `--verbose`
- **File logs** (JSONL) — controlled by `logging.level`

### Config
```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    consoleLevel: "info",
    consoleStyle: "pretty",  // pretty | compact | json
    redactSensitive: "tools",  // off | tools
    redactPatterns: [],  // custom regex array
  },
}
```

### WS Log Modes
- Normal: only errors and slow calls (≥50ms)
- Verbose (`--verbose`): all WS traffic
- `--ws-log auto|compact|full`

---

## Multiple Gateways

### When to Use
- One gateway recommended for most setups
- Separate for isolation or rescue bot

### Rescue Bot Quickstart
```bash
openclaw --profile rescue onboard
openclaw --profile rescue gateway install --port 19789
```

### Isolation Checklist
- Unique `OPENCLAW_CONFIG_PATH`
- Unique `OPENCLAW_STATE_DIR`
- Unique `agents.defaults.workspace`
- Unique `gateway.port`
- Leave ≥20 ports between base ports

### Derived Ports
- Browser control = base + 2
- CDP auto-allocates from controlPort+9..+108

---

## Network Model

Core rules:
- One Gateway per host recommended
- Loopback WS default: `ws://127.0.0.1:18789`
- Canvas served on same port: `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`
- Remote use via SSH tunnel or tailnet VPN

---

## OpenAI Chat Completions HTTP API

### Enabling
```json5
{
  gateway: {
    http: { endpoints: { chatCompletions: { enabled: true } } },
  },
}
```

### Endpoints (disabled by default)
- `POST /v1/chat/completions`
- `GET /v1/models` / `GET /v1/models/{id}`
- `POST /v1/embeddings`

### Agent-First Model Contract
- `model: "openclaw"` → default agent
- `model: "openclaw/default"` → stable alias
- `model: "openclaw/<agentId>"` → specific agent
- `x-openclaw-model` → backend model override
- `x-openclaw-session-key` → session routing

### Security
- **Full operator-access surface** — treat token like owner credential
- Shared-secret auth ignores narrower `x-openclaw-scopes`
- Keep on loopback/tailnet/private only

### Open WebUI Quick Setup
- Base URL: `http://127.0.0.1:18789/v1`
- API key: gateway bearer token
- Model: `openclaw/default`

---

## OpenResponses HTTP API

### Enabling
```json5
{
  gateway: {
    http: { endpoints: { responses: { enabled: true } } },
  },
}
```

### Supported Input Types
- `message` — roles: system, developer, user, assistant
- `function_call_output` — tool results
- `input_image` — base64/URL (jpeg/png/gif/webp/heic/heif, max 10MB)
- `input_file` — base64/URL (text/markdown/html/csv/json/pdf, max 5MB)

### Config
```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          maxUrlParts: 8,
          files: { allowUrl: true, maxBytes: 5242880, maxChars: 200000 },
          images: { allowUrl: true, maxBytes: 10485760 },
        },
      },
    },
  },
}
```

### SSE Events
`response.created`, `response.in_progress`, `response.output_item.added`, `response.content_part.added`, `response.output_text.delta`, `response.output_text.done`, `response.content_part.done`, `response.output_item.done`, `response.completed`, `response.failed`

---

## OpenShell

### What it is
Managed sandbox backend. Delegates lifecycle to `openshell` CLI via SSH transport.

### Workspace Modes
| | `mirror` | `remote` |
|--|---------|---------|
| **Canonical** | Local host | Remote OpenShell |
| **Sync** | Bidirectional (each exec) | One-time seed |
| **Per-turn overhead** | Higher | Lower |
| **Best for** | Dev workflows | Long-running agents, CI |

### Configuration
```json5
{
  agents: { defaults: { sandbox: { mode: "all", backend: "openshell" } } },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: { from: "openclaw", mode: "remote" },
      },
    },
  },
}
```

### Key Config Keys
`mode`, `command`, `from`, `gateway`, `gatewayEndpoint`, `policy`, `providers`, `gpu`, `autoProviders`, `remoteWorkspaceDir` (/sandbox), `remoteAgentWorkspaceDir` (/agent), `timeoutSeconds` (120)

---

## Gateway-Owned Pairing

### What it is
Node identity/trust system. Gateway is source of truth for allowed nodes.

### Flow
1. Node connects → pending request stored → `node.pair.requested` emitted
2. Approve/reject via CLI or UI
3. Approval issues fresh token
4. Node reconnects with token

### CLI
```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name> --name "Living Room iPad"
```

### Approval Scope Requirements
- Commandless: `operator.pairing`
- Non-exec commands: + `operator.write`
- `system.run`: + `operator.admin`

### Important (2026.3.31+)
- Node commands disabled until pairing approved
- Node-originated runs on reduced trusted surface

### Storage
- `~/.openclaw/nodes/paired.json`
- `~/.openclaw/nodes/pending.json`

---

## Gateway Protocol

### Transport
- WebSocket, text frames with JSON payloads
- First frame **must** be `connect`
- Pre-connect: 64 KiB cap; post-handshake: follow `hello-ok.policy.maxPayload`

### Handshake
1. Gateway sends `connect.challenge` (nonce + timestamp)
2. Client sends `connect` with role, scopes, caps, commands, auth, device info
3. Gateway returns `hello-ok` with protocol version, server info, features, snapshot, policy

### Framing
- **Request**: `{type:"req", id, method, params}`
- **Response**: `{type:"res", id, ok, payload|error}`
- **Event**: `{type:"event", event, payload, seq?, stateVersion?}`

### Roles
- `operator` — control plane (CLI/UI/automation)
- `node` — capability host (camera/screen/canvas/system.run)

### Operator Scopes
`operator.read`, `operator.write`, `operator.admin`, `operator.approvals`, `operator.pairing`, `operator.talk.secrets`

### Broadcast Scoping
- Chat/agent/tool-result: require `operator.read`
- Plugin broadcasts: `operator.write` or `operator.admin`
- Status/transport events: unrestricted

### Major RPC Families
- System: `health`, `status`, `system-presence`, `system-event`
- Models: `models.list`, `usage.status`, `usage.cost`
- Channels: `channels.status`, `channels.logout`, `web.login.*`
- Sessions: `sessions.list/create/send/steer/abort/patch/reset/delete/compact`
- Config: `config.get/set/patch/apply/schema`
- Agents: `agents.list/create/update/delete`
- Nodes: `node.list/describe/invoke/event`
- Automation: `cron.list/status/add/update/remove/run`

---

## Remote Access

### SSH Tunnel (Universal Fallback)
```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

### CLI Remote Defaults
```json5
{
  gateway: {
    mode: "remote",
    remote: { url: "ws://127.0.0.1:18789", token: "your-token" },
  },
}
```

### Credential Precedence
- Explicit `--token`/`--password` always win
- CLI `--url` never reuses implicit credentials
- Local mode: `OPENCLAW_GATEWAY_TOKEN` → `gateway.auth.token` → `gateway.remote.token`
- Remote mode: `gateway.remote.token` → `OPENCLAW_GATEWAY_TOKEN` → `gateway.auth.token`

### Security
- Keep Gateway loopback-only unless needed
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` for plaintext ws:// on private networks (process env only)
- `gateway.remote.tlsFingerprint` pins remote TLS cert

---

## Remote Gateway Setup (macOS)

Merged into Remote Access. SSH tunnel + LaunchAgent for persistence.

```xml
<!-- ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist -->
<plist version="1.0"><dict>
  <key>Label</key><string>ai.openclaw.ssh-tunnel</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/ssh</string><string>-N</string><string>remote-gateway</string>
  </array>
  <key>KeepAlive</key><true/>
  <key>RunAtLoad</key><true/>
</dict></plist>
```

---

## Sandboxing

### Modes
| Mode | Behavior |
|------|----------|
| `off` | No sandboxing |
| `non-main` | Sandbox only non-main sessions |
| `all` | Every session sandboxed |

### Scope
| Scope | Containers |
|-------|-----------|
| `agent` (default) | One per agent |
| `session` | One per session |
| `shared` | One for all |

### Backends
| Backend | Where | Setup |
|---------|-------|-------|
| `docker` (default) | Local container | `scripts/sandbox-setup.sh` |
| `ssh` | SSH-accessible host | SSH key + target |
| `openshell` | OpenShell managed | Plugin enabled |

### Workspace Access
- `none` (default): sandbox workspace only
- `ro`: workspace read-only at `/agent`
- `rw`: workspace read-write at `/workspace`

### Docker Bind Mounts
```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro"],
          network: "none",  // default: no network
        },
      },
    },
  },
}
```

**Blocked bind sources**: docker.sock, /etc, /proc, /sys, /dev, credential roots (~/.aws, ~/.ssh, etc.)

### Docker-out-of-Docker (DooD)
When the Gateway itself runs as a Docker container, it orchestrates sibling sandbox containers via the host's Docker socket. **Config `workspace` must contain the host's absolute path**, not the Gateway container path. The Gateway deployment must include an identical volume map (`-v /home/user/.openclaw:/home/user/.openclaw`) for FS bridge parity.

### Sandbox Browser
- Auto-starts by default (`sandbox.browser.autoStart`, `sandbox.browser.autoStartTimeoutMs`)
- Dedicated Docker network (`openclaw-sandbox-browser`, configurable via `sandbox.browser.network`)
- noVNC password-protected; short-lived token URL with password in URL fragment
- `cdpSourceRange` for CIDR allowlist
- `allowHostControl` lets sandboxed sessions target the host browser
- Custom target allowlists: `allowedControlUrls`, `allowedControlHosts`, `allowedControlPorts`

---

## Sandbox vs Tool Policy vs Elevated

### Three Controls
1. **Sandbox** (`sandbox.*`) — where tools run
2. **Tool policy** (`tools.*`) — which tools allowed
3. **Elevated** (`tools.elevated.*`) — exec-only host escape

### Key Rules
- `deny` always wins in tool policy
- Tool policy is the hard stop — /exec cannot override denied tool
- Elevated only affects `exec`, not other tools
- Elevated is NOT skill-scoped

### Debug
```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --json
```

---

## Secrets Management

### SecretRef Contract
```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

### Sources
- **env**: `{ source: "env", provider: "default", id: "OPENAI_API_KEY" }`
- **file**: `{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }`
- **exec**: `{ source: "exec", provider: "vault", id: "providers/openai/apiKey" }`

### Provider Config
```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: { source: "file", path: "~/.openclaw/secrets.json", mode: "json" },
      vault: { source: "exec", command: "/usr/local/bin/resolver", jsonOnly: true },
    },
  },
}
```

### Runtime Model
- Resolution is eager during activation, not lazy
- Startup fails fast on unresolvable active refs
- Reload uses atomic swap (full success or keep last-known-good)
- Inactive surfaces don't block startup

### Exec Provider
- Runs absolute binary path, no shell
- `allowSymlinkCommand: true` for Homebrew shims
- Request: `{ protocolVersion: 1, provider: "vault", ids: [...] }`
- Response: `{ protocolVersion: 1, values: { ... } }`

---

## Secrets Plan Contract

### `secrets apply` Format
```json
{ "version": 1, "protocolVersion": 1, "targets": [...] }
```

### Target Fields
- `type` — recognized target type
- `path` — config path
- `ref` — SecretRef object
- Forbidden segments: `__proto__`, `prototype`, `constructor`

### Validation
```bash
openclaw secrets apply --from plan.json --dry-run
openclaw secrets apply --from plan.json
```
- Exec SecretRefs rejected in write mode unless `--allow-exec`

---

## Security

### Trust Model
- **Personal assistant model** — one trusted operator per gateway
- NOT a hostile multi-tenant boundary
- Gateway = control plane; Node = remote execution surface
- `sessionKey` = routing, not auth
- Exec approvals are guardrails, not isolation

### Security Audit
```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

### Hardened Baseline
```json5
{
  gateway: { mode: "local", bind: "loopback", auth: { mode: "token", token: "..." } },
  session: { dmScope: "per-channel-peer" },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: { whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } } },
}
```

### Context Visibility
- `all` (default) — include all context
- `allowlist` — filter to allowlisted senders
- `allowlist_quote` — allowlist but keep explicit quote

### Credential Storage Map
- WhatsApp: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- Telegram: config/env or `tokenFile`
- Pairing: `~/.openclaw/credentials/<channel>-allowFrom.json`
- Auth profiles: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Secrets: `~/.openclaw/secrets.json`

---

## Security Audit Checks

### Critical Checks
| checkId | Description |
|---------|-------------|
| `fs.state_dir.perms_world_writable` | State dir world-writable |
| `fs.config.perms_writable` | Config writable by others |
| `fs.config.perms_world_readable` | Config world-readable |
| `fs.config_include.perms_writable` | Config include file writable |
| `fs.config_include.perms_world_readable` | Included secrets world-readable |
| `fs.auth_profiles.perms_writable` | Auth profiles writable |
| `fs.credentials_dir.perms_writable` | Pairing/credential state writable |
| `gateway.bind_no_auth` | Remote bind without auth |
| `gateway.loopback_no_auth` | Reverse-proxied loopback unauthenticated |
| `gateway.http.no_auth` | HTTP APIs reachable with `auth.mode="none"` |
| `gateway.tailscale_funnel` | Public internet exposure |
| `gateway.control_ui.device_auth_disabled` | Device auth disabled |
| `gateway.control_ui.allowed_origins_required` | Non-loopback Control UI without origin allowlist |
| `gateway.nodes.allow_commands_dangerous` | High-impact node commands enabled |
| `gateway.tools_invoke_http.dangerous_allow` | Dangerous tools re-enabled over HTTP |
| `hooks.token_reuse_gateway_token` | Hook token = gateway token |
| `sandbox.dangerous_bind_mount` | Dangerous bind mount |

### Warn/Info Checks
| checkId | Description |
|---------|-------------|
| `fs.state_dir.perms_group_writable` | Group-writable state |
| `fs.config.symlink` | Symlinked config (unsupported for writes) |
| `fs.synced_dir` | State/config in iCloud/Dropbox/Drive |
| `fs.sessions_store.perms_readable` | Others can read session transcripts |
| `gateway.trusted_proxies_missing` | Proxy headers without trust |
| `gateway.token_too_short` | Short auth token |
| `gateway.http.session_key_override_enabled` | HTTP callers can override sessionKey |
| `gateway.nodes.deny_commands_ineffective` | Pattern deny doesn't match shell text |
| `logging.redact_off` | Redaction disabled |

---

## Tailscale

### Modes
| Mode | Description |
|------|-------------|
| `off` (default) | No Tailscale integration |
| `serve` | Tailnet-only via tailscale serve |
| `funnel` | Public HTTPS (requires password auth) |

### Tailscale Identity Auth
```json5
{ gateway: { auth: { allowTailscale: true } } }
```
- Verifies via `tailscale whois`
- Only for WS/Control UI, NOT HTTP API endpoints
- Requires request from loopback with X-Forwarded-* headers

### Gateway Bind
- `gateway.bind: "tailnet"` — direct Tailnet IP bind
- `loopback` + `serve` — HTTPS via MagicDNS

---

## Tools Invoke HTTP API

### Endpoint
`POST /tools/invoke` — always enabled, same port as Gateway

### Request
```json
{ "tool": "web_fetch", "action": "...", "args": {...}, "sessionKey": "main" }
```

### Default Hard Deny List
`exec`, `spawn`, `shell`, `fs_write`, `fs_delete`, `fs_move`, `apply_patch`, `sessions_spawn`, `sessions_send`, `cron`, `gateway`, `nodes`, `whatsapp_login`

### Customize
- `gateway.tools.deny` — add to deny list
- `gateway.tools.allow` — remove from deny list

### Responses
- 200: `ok:true` + result
- 400: invalid body
- 401: auth failure
- 404: tool not found
- 429: rate-limited
- 500: error

---

## Troubleshooting

### Command Ladder
```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

### Common Issues

**Anthropic 429 long context**: Disable `context1m` param, or use eligible credential, or configure fallback.

**Local backend fails on agent runs**: Set `compat.requiresStringContent: true` or `compat.supportsTools: false`.

**No replies**: Check pairing pending, mention gating, allowlist mismatches.

**Config restored**: `.clobbered.*` = rejected config; `.rejected.*` = failed write. Next agent turn warned.

**Gateway not starting**: Set `gateway.mode=local`; check EADDRINUSE; check auth for non-loopback.

### Auth Detail Codes
| Code | Meaning | Action |
|------|---------|--------|
| `AUTH_TOKEN_MISSING` | No token sent | Set token in client |
| `AUTH_TOKEN_MISMATCH` | Token mismatch | Check `canRetryWithDeviceToken` |
| `AUTH_DEVICE_TOKEN_MISMATCH` | Stale device token | Rotate/re-approve |
| `PAIRING_REQUIRED` | Device needs approval | `openclaw devices approve` |

---

## Trusted Proxy Auth

### When to Use
- Identity-aware proxy (Pomerium, Caddy+OAuth, nginx+oauth2-proxy, Traefik forward auth)
- Proxy handles ALL auth

### When NOT to Use
- Proxy doesn't authenticate (TLS terminator only)
- Any bypass path exists
- Same-host loopback proxy (fails closed)

### Configuration
```json5
{
  gateway: {
    bind: "lan",
    trustedProxies: ["10.0.0.1"],
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user",       // required
        requiredHeaders: ["x-auth-verified"],  // optional
        allowUsers: ["admin@example.com"],     // optional
      },
    },
  },
}
```

### Error Codes
- `trusted_proxy_untrusted_source` — request not from trusted proxy
- `trusted_proxy_loopback_source` — same-host loopback rejected
- `trusted_proxy_user_missing` — no user header
- `trusted_proxy_user_not_allowed` — user not in allowlist
- `trusted_proxy_origin_not_allowed` — browser origin rejected

### Proxy Examples
- Pomerium: `x-pomerium-claim-email`
- Caddy: `x-forwarded-user`
- nginx+oauth2-proxy: `x-auth-request-email`
- Traefik: `x-forwarded-user`

---

## Cross-References

| Topic | Related Pages |
|-------|--------------|
| Gateway startup | Runbook, Troubleshooting, Doctor |
| Authentication | Authentication, Secrets, Trusted Proxy Auth |
| Configuration | Configuration, Config-Agents, Config-Channels, Config-Tools, Configuration-Reference, Configuration-Examples |
| Network/Remote | Remote, Remote-Gateway-Readme, Tailscale, Network-Model |
| Security | Security, Security/Audit-Checks, Sandbox-vs-Tool-Policy, Sandboxing |
| Protocol | Protocol, Bridge-Protocol (removed) |
| Discovery | Discovery, Bonjour, Pairing |
| HTTP APIs | OpenAI-HTTP-API, OpenResponses-HTTP-API, Tools-Invoke-HTTP-API |
| Operations | Health, Heartbeat, Diagnostics, Logging, Doctor, Gateway-Lock |
| Sandbox | Sandboxing, OpenShell, Sandbox-vs-Tool-Policy |
| Models | Local-Models, CLI-Backends, Authentication |
| Multi-Gateway | Multiple-Gateways, Gateway-Lock |
