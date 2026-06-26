# OpenClaw Reference Documentation

## Table of Contents
- [Configuration System Overview](#configuration-system-overview)
- [Configuration Reference — Full Schema](#configuration-reference--full-schema)
- [Agent Configuration Reference](#agent-configuration-reference)
- [Heartbeat Reference](#heartbeat-reference)
- [Agent Workspace Reference](#agent-workspace-reference)
- [Session Management Reference](#session-management-reference)
- [Authentication Reference](#authentication-reference)
- [Gateway Protocol Reference](#gateway-protocol-reference)
- [RPC Adapters Reference](#rpc-adapters-reference)
- [CLI Reference](#cli-reference)
- [Onboarding Reference](#onboarding-reference)
- [File Locations Quick Reference](#file-locations-quick-reference)
- [Environment Variables Quick Reference](#environment-variables-quick-reference)

## Configuration System Overview

OpenClaw reads an optional **JSON5** config from `~/.openclaw/openclaw.json` (supports comments and trailing commas). The active config path must be a regular file — symlinked `openclaw.json` layouts are unsupported for OpenClaw-owned writes; an atomic write may replace the path instead of preserving the symlink. If you keep config outside the default state directory, point `OPENCLAW_CONFIG_PATH` directly at the real file.

If the file is missing, OpenClaw uses safe defaults.

**Editing config:**
```bash
openclaw onboard           # full onboarding flow
openclaw configure         # config wizard
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

Or edit `~/.openclaw/openclaw.json` directly — the Gateway watches the file and applies changes automatically.

### Strict Validation

OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start**. The only root-level exception is `$schema` (string).

When validation fails:
- The Gateway does not boot
- Only diagnostic commands work (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`)
- Run `openclaw doctor` to see exact issues
- Run `openclaw doctor --fix` to apply repairs

The Gateway keeps a trusted last-known-good copy after each successful startup. If `openclaw.json` later fails validation (drops `gateway.mode`, shrinks sharply, or has a stray log line prepended), OpenClaw preserves the broken file as `.clobbered.*`, restores the last-known-good copy, and logs the recovery reason. The next agent turn also receives a system-event warning so the main agent does not blindly rewrite the restored config. Promotion to last-known-good is skipped when a candidate contains redacted secret placeholders such as `***`.

When every validation issue is scoped to `plugins.entries.<id>...`, OpenClaw does not perform whole-file recovery — it keeps the current config active and surfaces the plugin-local failure so a plugin schema or host-version mismatch cannot roll back unrelated user settings.

**Check live schema:**
```bash
openclaw config schema
```

`config.schema.lookup` fetches a single path-scoped node plus child summaries for drill-down tooling. Field `title`/`description` docs metadata carries through nested objects, wildcard (`*`), array-item (`[]`), and `anyOf`/`oneOf`/`allOf` branches. Runtime plugin and channel schemas merge in when the manifest registry is loaded.

### $include Directive (Split Config)

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/a.json5", "./clients/b.json5"],
  },
}
```

- **Single file**: replaces the containing object
- **Array of files**: deep-merged in order (later wins)
- **Sibling keys**: merged after includes (override included values)
- **Nested includes**: supported up to 10 levels deep
- **Relative paths**: resolved relative to the including file

---

## Configuration Reference — Full Schema

### Gateway

```json5
{
  gateway: {
    mode: "local",         // "local" | "remote"
    port: 18789,           // single multiplexed port for WS + HTTP
    bind: "loopback",      // "auto" | "loopback" | "lan" (0.0.0.0) | "tailnet" | "custom"
    auth: {
      mode: "token",       // "none" | "token" | "password" | "trusted-proxy"
      // Note: "none" is intentionally not offered by onboarding prompts
      token: "your-token", // or OPENCLAW_GATEWAY_TOKEN env var
      password: "...",     // or OPENCLAW_GATEWAY_PASSWORD
      // trustedProxy: { userHeader: "x-forwarded-user" }, // for mode=trusted-proxy
      // Note: trusted-proxy mode fails closed on loopback-source proxies; same-host loopback
      // reverse proxies do NOT satisfy trusted-proxy auth
      allowTailscale: true,
      // Note: HTTP API endpoints do NOT use Tailscale header auth; they follow the
      // gateway's normal HTTP auth mode instead
      // Note: HTTP API endpoints do NOT use Tailscale header auth; they follow the
      // gateway's normal HTTP auth mode instead
      rateLimit: {
        maxAttempts: 10,
        windowMs: 60000,
        lockoutMs: 300000,
        exemptLoopback: true,
        // Note: on async Tailscale Serve Control UI path, failed attempts for the same
        // {scope, clientIp} are serialized before the failure write. Concurrent bad
        // attempts can trip the limiter on the second request instead of both racing through.
        // Browser-origin WS auth attempts are always throttled with loopback exemption
        // disabled (defense-in-depth against browser-based localhost brute force).
      },
    },
    tailscale: {
      mode: "off",         // "off" | "serve" | "funnel"
      resetOnExit: false,
    },
    controlUi: {
      enabled: true,
      basePath: "/",
      // embedSandbox: "scripts",  // "strict" | "scripts" | "trusted"
      // allowExternalEmbedUrls: false,
      // allowedOrigins: ["https://control.example.com"],
      // dangerouslyAllowHostHeaderOriginFallback: false,
      // allowInsecureAuth: false,
      // dangerouslyDisableDeviceAuth: false,
      // allowExternalEmbedUrls: false,
      // allowedOrigins: ["https://control.example.com"],
      // dangerouslyAllowHostHeaderOriginFallback: false,
    },
    remote: {
      url: "ws://gateway.tailnet:18789",
      transport: "ssh",    // "ssh" | "direct"
      token: "your-token",
    },
    trustedProxies: ["10.0.0.1"],
    allowRealIpFallback: false,
    tools: {
      deny: ["browser"],   // Additional /tools/invoke HTTP denies
      allow: ["gateway"],  // Remove tools from the default HTTP deny list
    },
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
          timeoutMs: 10000,
        },
      },
    },
    channelHealthCheckMinutes: 5,
    channelStaleEventThresholdMinutes: 30,
    channelMaxRestartsPerHour: 10,
  },
}
```

**Bind mode notes:**
- Use bind mode values (`auto`, `loopback`, `lan`, `tailnet`, `custom`), NOT host aliases (`0.0.0.0`, `127.0.0.1`, `localhost`)
- **Docker note**: the default `loopback` bind listens on `127.0.0.1` inside the container; use `bind: "lan"` or `bind: "custom"` with `customBindHost: "0.0.0.0"` to listen on all interfaces
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` is a client-side process-environment break-glass override that allows plaintext `ws://` to trusted private-network IPs (no `openclaw.json` equivalent)
- Non-loopback binds require gateway auth
- If both `gateway.auth.token` and `gateway.auth.password` are configured, set `gateway.auth.mode` explicitly

### Skills

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm",  // "npm" | "pnpm" | "yarn" | "bun"
    },
    entries: {
      "image-lab": {
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
        env: { GEMINI_API_KEY: "GEMINI_KEY_HERE" },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

- `allowBundled`: optional allowlist for bundled skills only (managed/workspace skills unaffected)
- `load.extraDirs`: extra shared skill roots (lowest precedence)
- `install.preferBrew`: when true, prefer Homebrew installers when `brew` is available
- `entries.<skillKey>.enabled: false`: disables a skill even if bundled/installed
- `entries.<skillKey>.apiKey`: convenience for skills declaring a primary env var

### Plugins

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: [],
    load: {
      paths: ["~/Projects/oss/voice-call-plugin"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
          allowConversationAccess: false,
        },
        config: { provider: "twilio" },
        subagent: {
          allowModelOverride: false,
          allowedModels: [],
        },
      },
    },
    installs: {},     // CLI-managed install metadata
    slots: {
      memory: null,   // active memory plugin id or "none"
      contextEngine: "legacy",  // active context engine plugin id
    },
  },
}
```

- Loaded from `~/.openclaw/extensions`, `<workspace>/.openclaw/extensions`, plus `plugins.load.paths`
- **Discovery** accepts native OpenClaw plugins plus compatible Codex bundles and Claude bundles, including manifestless Claude default-layout bundles
- `allow`: optional allowlist (only listed plugins load). `deny` wins.
- **Config changes require a gateway restart.**
- `plugins.entries.<id>.hooks.allowPromptInjection`: when `false`, core blocks `before_prompt_build`
- `plugins.entries.<id>.hooks.allowConversationAccess`: enables trusted non-bundled plugins to read raw conversation content from specific typed hooks (`llm_input`, `llm_output`, `agent_end`)
- `plugins.entries.<id>.apiKey`: plugin-level API key convenience field
- `plugins.entries.<id>.env`: plugin-scoped env var map
- `plugins.entries.<id>.subagent.allowModelOverride`: trust this plugin to request per-run model overrides
- `plugins.entries.<id>.subagent.allowedModels`: allowlist of canonical `provider/model` targets
- `plugins.entries.firecrawl.config.webFetch`: Firecrawl web-fetch provider settings:
  - `baseUrl`: default `https://api.firecrawl.dev`
  - `onlyMainContent`: default `true`
  - `maxAgeMs`: default `172800000` (2 days)
  - `timeoutSeconds`: default `60`
  - `apiKey` fallback chain: also checks `webSearch.apiKey`, legacy `tools.web.fetch.firecrawl.apiKey`, and `FIRECRAWL_API_KEY` env var
- `plugins.entries.xai.config.xSearch`: xAI X Search settings (includes `enabled` and `model`, e.g. `"grok-4-1-fast"`)
- `plugins.entries.memory-core.config.dreaming`: memory dreaming settings (see Dreaming docs)
- `plugins.installs`: CLI-managed install metadata (includes `source`, `spec`, `sourcePath`, `installPath`, `version`, `resolvedName`, `resolvedVersion`; prefer CLI commands over manual edits)

### Browser

```json5
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    defaultProfile: "user",
    ssrfPolicy: {
      // dangerouslyAllowPrivateNetwork: true,  // opt in only for trusted private-network
      // hostnameAllowlist: ["*.example.com"],
      // allowedHostnames: ["localhost"],
    },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      user: { driver: "existing-session", attachOnly: true, color: "#00AA00" },
      brave: {
        driver: "existing-session",
        attachOnly: true,
        userDataDir: "~/Library/Application Support/BraveSoftware/Brave-Browser",
        color: "#FB542B",
      },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // headless: false,
    // noSandbox: false,
    // extraArgs: [],
    // executablePath: "/Applications/Brave Browser.app/...",
    // attachOnly: false,
  },
}
```

- `evaluateEnabled: false` disables `act:evaluate` and `wait --fn`
- `ssrfPolicy.dangerouslyAllowPrivateNetwork` is disabled when unset; `ssrfPolicy.allowPrivateNetwork: true` is a supported legacy alias for `dangerouslyAllowPrivateNetwork`
- In strict mode, use `ssrfPolicy.hostnameAllowlist` and `ssrfPolicy.allowedHostnames` for explicit exceptions
- In strict mode, remote CDP profile endpoints (`profiles.*.cdpUrl`) are subject to the same private-network blocking during reachability/discovery checks
- Remote profiles are attach-only (start/stop/reset disabled)
- `profiles.*.cdpUrl` accepts `http://`, `https://`, `ws://`, and `wss://`
- `existing-session` profiles use Chrome MCP instead of CDP. **Chrome MCP route limits**: snapshot/ref-driven actions instead of CSS-selector targeting, one-file upload hooks, no dialog timeout overrides, no `wait --load networkidle`, and no `responsebody`, PDF export, download interception, or batch actions
- `existing-session` profiles can set `userDataDir` to target specific browser profiles like Brave or Edge
- **Auto-detect order for browser executable**: default browser if Chromium-based → Chrome → Brave → Edge → Chromium → Chrome Canary
- Control service: loopback only (port derived from `gateway.port`, default `18791`)
- `extraArgs` appends extra launch flags to local Chromium startup

### UI

```json5
{
  ui: {
    seamColor: "#FF4500",
    assistant: {
      name: "OpenClaw",
      avatar: "CB",  // emoji, short text, image URL, or data URI
    },
  },
}
```

- `seamColor`: accent color for native app UI chrome (Talk Mode bubble tint, etc.)
- `assistant`: Control UI identity override; falls back to active agent identity

### Cron

```json5
{
  cron: {
    enabled: true,
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1,
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    },
    webhookToken: "",
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 },
  },
}
```

### Hooks

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
        deliver: true,
      },
    ],
    gmail: {
      account: "",
      model: null,
      thinking: null,
    },
    internal: {
      enabled: false,
      entries: {},
      load: { extraDirs: [] },
    },
  },
}
```

### Diagnostics and Logging

```json5
{
  diagnostics: {
    flags: ["telegram.http", "gateway.*"],
  },
  logging: {
    level: "info",
    consoleLevel: "warn",
    redactSensitive: "tools",
    file: null,   // custom log file path
  },
  update: {
    channel: "stable",
    checkOnStart: true,
    auto: {
      enabled: false,
      stableDelayHours: 6,
      stableJitterHours: 12,
      betaCheckIntervalHours: 1,
    },
  },
}
```

### Environment Variables

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
    shellEnv: {
      enabled: false,
      timeoutMs: 15000,
    },
  },
}
```

---

## Agent Configuration Reference

### Agent Defaults

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      skipBootstrap: false,
      bootstrapMaxChars: 12000,
      bootstrapTotalMaxChars: 60000,
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4"],
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "openai/gpt-5.4": { alias: "GPT" },
      },
      imageMaxDimensionPx: 1200,
      thinking: "low",     // "off" | "low" | "medium" | "high" | "auto"
      tools: {
        profile: "coding", // "minimal" | "messaging" | "coding"
        allow: [],
        deny: [],
        fs: { workspaceOnly: false },
        exec: {
          host: "auto",    // "auto" | "gateway" | "node" | "sandbox"
          security: "full",// "full" | "allowlist" | "deny"
          ask: "off",      // "off" | "on-miss" | "always"
          node: null,      // node id or name when host=node
        },
        elevated: { enabled: false },
        agentToAgent: {
          enabled: false,
          allow: [],
        },
      },
      sandbox: {
        mode: "off",       // "off" | "non-main" | "all"
        scope: "agent",    // "session" | "agent" | "shared"
        docker: {
          image: null,
          user: null,
          setupCommand: null,
          dangerouslyAllowReservedContainerTargets: false,
          dangerouslyAllowExternalBindSources: false,
          dangerouslyAllowContainerNamespaceJoin: false,
        },
      },
      heartbeat: {
        every: "30m",
        model: null,       // optional model override for heartbeat runs (provider/model)
        target: "none",    // "none" | "last" | <channel-id>
        to: null,
        accountId: null,
        session: null,     // optional session key override ("main" or explicit session key)
        directPolicy: "allow",
        lightContext: false,
        isolatedSession: false,
        includeReasoning: false,
        prompt: "...",
        ackMaxChars: 300,
        activeHours: null,
        timeoutSeconds: null,  // optional timeout for heartbeat runs
        suppressToolErrorWarnings: false,  // suppresses tool error warning payloads
      },
      subagents: {
        model: null,
      },
      skills: null,        // null = all skills; [] = no skills; ["skill1"] = allowlist
      memorySearch: {
        qmd: {
          extraCollections: [],
        },
      },
    },
    list: [
      {
        id: "main",
        default: true,
        name: "Main",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        model: null,       // override agents.defaults.model
        // tools, sandbox, heartbeat, skills, etc. (per-agent overrides)
      },
    ],
  },
}
```

### Session Configuration

```json5
{
  session: {
    dmScope: "per-channel-peer",  // "main" | "per-peer" | "per-channel-peer" | "per-account-channel-peer"
    mainKey: "main",
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
    reset: {
      mode: "daily",       // "daily" | "idle" | "none"
      atHour: 4,
      idleMinutes: 120,
    },
    maintenance: {
      mode: "warn",        // "warn" | "enforce"
      pruneAfter: "30d",
      maxEntries: 500,
    },
    identityLinks: [],     // link same person across channels
  },
}
```

### Multi-Agent Routing (Bindings)

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    // Most specific first: peer match > parentPeer > guildId+roles > guildId > teamId > accountId > channel > default
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
    // Per-peer override
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "120363...@g.us" },
      },
    },
  ],
}
```

**Routing rule precedence (most-specific wins):**
1. `peer` match (exact DM/group/channel id)
2. `parentPeer` match (thread inheritance)
3. `guildId + roles` (Discord role routing)
4. `guildId` (Discord)
5. `teamId` (Slack)
6. `accountId` match for a channel
7. channel-level match (`accountId: "*"`)
8. fallback to default agent

**Notes:**
- A binding that omits `accountId` matches the default account only
- Use `accountId: "*"` for a channel-wide fallback across all accounts
- If multiple bindings match in the same tier, first in config order wins
- Multiple match fields = AND semantics (all fields required)

---

## Heartbeat Reference

Heartbeat runs **periodic agent turns** in the main session so the model can surface anything that needs attention without spamming you.

Key behaviors:
- Heartbeat turns do **NOT** create background task records
- Default interval: `30m` (or `1h` for Anthropic OAuth/token auth including Claude CLI reuse)
- `0m` disables heartbeats; also omits `HEARTBEAT.md` from bootstrap context
- Empty `HEARTBEAT.md` (only blank lines + markdown headers) → skipped as `reason=empty-heartbeat-file`
- No tasks due in task mode → skipped as `reason=no-tasks-due`
- All three visibility flags false → skipped as `reason=alerts-disabled`
- Active hours (`heartbeat.activeHours`) are checked in the configured timezone; outside the window, heartbeats are skipped

**Additional key fields:**
- `heartbeat.model`: optional model override (`provider/model`) for heartbeat runs
- `heartbeat.timeoutSeconds`: optional timeout for heartbeat runs
- `heartbeat.suppressToolErrorWarnings`: when true, suppresses tool error warning payloads during heartbeat runs
- `heartbeat.session`: optional session key override (`"main"` default, or explicit session key)

**Delivery behavior notes:**
- If the main queue is busy, the heartbeat is skipped and retried later
- Heartbeat-only replies do **NOT** keep the session alive; the last `updatedAt` is restored so idle expiry behaves normally
- If the resolved heartbeat target supports typing, OpenClaw shows typing while the heartbeat run is active
- Heartbeat can react to completed background tasks, but a heartbeat run itself does not create a task record

**Per-agent heartbeats:** If any `agents.list[]` entry includes a `heartbeat` block, **only those agents** run heartbeats. The per-agent block merges on top of `agents.defaults.heartbeat`.

**24/7 setup:** To run heartbeats all day, omit `activeHours` entirely (default) or set `activeHours: { start: "00:00", end: "24:00" }`. Do NOT set the same `start` and `end` time (e.g., `08:00` to `08:00`) — that is treated as a zero-width window and heartbeats are always skipped.

**Manual wake:** If multiple agents have `heartbeat` configured, a manual wake runs each of those agent heartbeats immediately.

**Delivery behavior notes:**
- If the main queue is busy, the heartbeat is skipped and retried later
- If `target` resolves to no external destination, the run still happens but no outbound message is sent
- Heartbeat-only replies do **NOT** keep the session alive; the last `updatedAt` is restored so idle expiry behaves normally
- If the resolved heartbeat target supports typing, OpenClaw shows typing while the heartbeat run is active

**Response contract:**
- If nothing needs attention → reply with `HEARTBEAT_OK`
- `HEARTBEAT_OK` at the start/end of reply: stripped; reply dropped if remaining content ≤ `ackMaxChars` (default: 300)
- `HEARTBEAT_OK` in the **middle** of a reply: not treated specially
- For alerts: do NOT include `HEARTBEAT_OK`
- Outside heartbeats, stray `HEARTBEAT_OK` at the start/end of a message is stripped and logged; a message that is only `HEARTBEAT_OK` is dropped

### HEARTBEAT.md

Optional file in workspace that the agent reads each heartbeat. Keep it tiny to avoid token burn.

**`tasks:` block support:**
```markdown
tasks:

- name: inbox-triage
  interval: 30m
  prompt: "Check for urgent unread emails and flag anything time sensitive."
- name: calendar-scan
  interval: 2h
  prompt: "Check for upcoming meetings that need prep or follow-up."

# Additional instructions

- Keep alerts short.
- If nothing needs attention after all due tasks, reply HEARTBEAT_OK.
```

Behavior:
- Only **due** tasks are included in the heartbeat prompt for that tick
- If no tasks are due, the heartbeat is skipped entirely (`reason=no-tasks-due`)
- Task last-run timestamps stored in session state (`heartbeatTaskState`)
- Timestamps only advanced after heartbeat run completes normal reply path

### Manual Wake

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

### Visibility Controls

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false      # Hide HEARTBEAT_OK (default)
      showAlerts: true   # Show alert messages (default)
      useIndicator: true # Emit indicator events (default)
  telegram:
    heartbeat:
      showOk: true       # Show OK acknowledgments on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false  # Suppress alert delivery for this account
```

Precedence: per-account → per-channel → channel defaults → built-in defaults.

If **all three** are false, OpenClaw skips the heartbeat run entirely (no model call).

---

## Agent Workspace Reference

The workspace is the agent's home directory for file tools and workspace context. Default: `~/.openclaw/workspace`

**Important:** The workspace is the **default cwd**, not a hard sandbox. Tools resolve relative paths against the workspace, but absolute paths can still reach elsewhere on the host unless sandboxing is enabled. When sandboxing is enabled and `workspaceAccess` is not `"rw"`, tools operate inside a sandbox workspace under `~/.openclaw/sandboxes`, not your host workspace.

### Workspace File Map

| File | Purpose | Loaded |
|---|---|---|
| `AGENTS.md` | Operating instructions, rules, priorities, "how to behave" | Every session |
| `SOUL.md` | Persona, tone, and boundaries | Every session |
| `USER.md` | Who the user is and how to address them | Every session |
| `IDENTITY.md` | The agent's name, vibe, and emoji | Every session |
| `TOOLS.md` | Notes about local tools and conventions (guidance only, not tool control) | Every session |
| `HEARTBEAT.md` | Tiny checklist for heartbeat runs | Heartbeat runs |
| `BOOT.md` | Startup checklist run automatically on gateway restart (hooks required; only runs when hooks are required) | Gateway start |
| `BOOT.md` | Startup checklist run automatically on gateway restart (when internal hooks enabled) | Gateway start |
| `BOOTSTRAP.md` | One-time first-run ritual (delete after completing) | Once only |
| `memory/YYYY-MM-DD.md` | Daily memory log (one file per day) | Manually loaded |
| `MEMORY.md` | Curated long-term memory | Main/private session only |
| `skills/` | Workspace-specific skills (highest precedence) | Skills resolution |
| `canvas/` | Canvas UI files for node displays | Canvas tool |

**Bootstrap file size limits:**
- `agents.defaults.bootstrapMaxChars` (default: 12000) — per-file limit
- `agents.defaults.bootstrapTotalMaxChars` (default: 60000) — total limit
- `openclaw setup` can recreate missing defaults without overwriting existing files
- Sandbox seed copies only accept regular in-workspace files; symlink/hardlink aliases that resolve outside the source workspace are ignored

### What is NOT in the Workspace

| Item | Location |
|---|---|
| Config | `~/.openclaw/openclaw.json` |
| Auth profiles (model auth: OAuth + API keys) | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| Channel/provider credentials | `~/.openclaw/credentials/` |
| Session transcripts + metadata | `~/.openclaw/agents/<agentId>/sessions/` |
| Managed skills | `~/.openclaw/skills/` |

### Git Backup (Recommended)

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"

# Add private remote (GitHub CLI)
gh repo create openclaw-workspace --private --source . --remote origin --push

# Ongoing updates
git add . && git commit -m "Update memory" && git push
```

**Suggested `.gitignore`:**
```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

---

## Session Management Reference

Sessions organize conversations. Each message is routed to a session based on where it came from.

### Message Routing

| Source | Behavior |
|---|---|
| Direct messages | Shared session by default |
| Group chats | Isolated per group |
| Rooms/channels | Isolated per room |
| Cron jobs | Fresh session per run |
| Webhooks | Isolated per hook |

### DM Isolation

```json5
{
  session: {
    dmScope: "per-channel-peer",  // recommended for multi-user
  },
}
```

Options:
- `main` (default): all DMs share one session
- `per-peer`: isolate by sender (across channels)
- `per-channel-peer`: isolate by channel + sender (recommended)
- `per-account-channel-peer`: isolate by account + channel + sender

**Thread bindings:** `session.threadBindings` controls thread-bound session routing (Discord supports `/focus`, `/unfocus`, `/agents`, `/session idle`, and `/session max-age`).

**Warning:** If multiple people can message your agent, enable DM isolation. Without it, all users share the same conversation context.

### Session Lifecycle

- **Daily reset** (default): new session at 4:00 AM local time on the gateway host
- **Idle reset** (optional): new session after a period of inactivity (`session.reset.idleMinutes`)
- **Manual reset**: type `/new` or `/reset` in chat; `/new <model>` also switches the model

When both daily and idle resets are configured, whichever expires first wins.

### Session Storage

```
~/.openclaw/agents/<agentId>/sessions/sessions.json    # session index
~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl # transcripts
```

### Session Maintenance

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    },
  },
}
```

Preview with `openclaw sessions cleanup --dry-run`.

### Inspecting Sessions

```bash
openclaw status                              # session store path and recent activity
openclaw sessions --json                     # all sessions
openclaw sessions --json --active 60         # active in last 60 minutes
/status                                      # context usage, model, and toggles (in chat)
/context list                                # what is in the system prompt
```

---

## Authentication Reference

### Model Provider Authentication

OpenClaw supports OAuth and API keys for model providers.

**Recommended setup (API key):**
```bash
export ANTHROPIC_API_KEY="..."
# Or for daemon persistence:
cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=...
EOF
openclaw models status
```

**Anthropic Claude CLI reuse:**
```bash
claude auth login
claude auth status --text
openclaw models auth login --provider anthropic --method cli --set-default
```

**Manual token entry:**
```bash
openclaw models auth paste-token --provider openrouter
```

**Check auth status:**
```bash
openclaw models status
openclaw models status --probe    # live auth probes
openclaw models status --check    # automation-friendly (exit 1=expired/missing, 2=expiring)
```

### API Key Rotation Behavior

Priority order for key rotation on rate limits:
1. `OPENCLAW_LIVE_<PROVIDER>_KEY` (single override)
2. `<PROVIDER>_API_KEYS`
3. `<PROVIDER>_API_KEY`
4. `<PROVIDER>_API_KEY_*`

OpenClaw retries with the next key only for rate-limit errors (`429`, `rate_limit`, `quota`, `resource exhausted`, etc.). Non-rate-limit errors are not retried.

SecretRef support:
- `api_key` credentials can use `keyRef: { source, provider, id }`
- `token` credentials can use `tokenRef: { source, provider, id }`
- OAuth-mode profiles do NOT support SecretRef credentials

### Per-Session Auth

Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session.

```bash
/model anthropic/claude-opus-4-6@anthropic:work
/model list     # compact picker
/model status   # full view with candidates + next auth profile
```

### Per-Agent Auth Order

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use `--agent <id>` to target a specific agent.

### Auth Profiles Storage

Auth profiles live at: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

SecretRef support:
- `api_key` credentials can use `keyRef: { source, provider, id }`
- `token` credentials can use `tokenRef: { source, provider, id }`
- OAuth-mode profiles do NOT support SecretRef credentials

---

## Gateway Protocol Reference

The Gateway WebSocket protocol is the **single control plane + node transport** for OpenClaw.

### Transport

- WebSocket, text frames with JSON payloads
- First frame **must** be a `connect` request
- Pre-connect frames capped at 64 KiB
- After handshake, follow `hello-ok.policy.maxPayload` and `hello-ok.policy.maxBufferedBytes` limits
- With diagnostics enabled, oversized inbound frames and slow outbound buffers emit `payload.large` events before the gateway closes or drops the affected frame (keeps sizes/limits/surfaces/safe reason codes; does not keep message body, attachment contents, tokens, or secrets)

### Handshake

**Gateway → Client (pre-connect challenge):**
```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

**Client → Gateway (connect request):**
```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": { "id": "cli", "version": "1.2.3", "platform": "macos", "mode": "operator" },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

**Gateway → Client (hello-ok):**
```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 3,
    "server": { "version": "…", "connId": "…" },
    "features": { "methods": ["…"], "events": ["…"] },
    "snapshot": {},
    "policy": {
      "maxPayload": 26214400,
      "maxBufferedBytes": 52428800,
      "tickIntervalMs": 15000
    },
    "auth": {
      "deviceToken": "…",
      "role": "operator",
      "scopes": ["operator.read", "operator.write"]
    }
  }
}
```

`server`, `features`, `snapshot`, and `policy` are all required by the schema. `canvasHostUrl` is optional. `auth` reports the negotiated role/scopes when available. When no device token is issued, `hello-ok.auth` can still report just the negotiated permissions.

During trusted bootstrap handoff, `hello-ok.auth` may also include additional bounded role entries in `deviceTokens`. Bootstrap scope checks stay role-prefixed: operator entries only satisfy operator requests.

**Node connect example:**
```json
{
  "method": "connect",
  "params": {
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false }
  }
}
```

### Framing

- **Request**: `{type:"req", id, method, params}`
- **Response**: `{type:"res", id, ok, payload|error}`
- **Event**: `{type:"event", event, payload, seq?, stateVersion?}`

Side-effecting methods require **idempotency keys**.

### Roles + Scopes

**Roles:**
- `operator` = control plane client (CLI/UI/automation)
- `node` = capability host (camera/screen/canvas/system.run)

**Operator scopes:**
- `operator.read`
- `operator.write`
- `operator.admin`
- `operator.approvals`
- `operator.pairing`
- `operator.talk.secrets`

Plugin-registered gateway RPC methods may request their own operator scope, but reserved core admin prefixes (`config.*`, `exec.approvals.*`, `wizard.*`, `update.*`) always resolve to `operator.admin`.

Method scope is only the first gate. Some slash commands reached through `chat.send` apply stricter command-level checks on top (e.g. persistent `/config set` and `/config unset` writes require `operator.admin`).

**Node approval scope checks (`node.pair.approve`):**
- Commandless requests: `operator.pairing`
- Requests with non-exec node commands: `operator.pairing` + `operator.write`
- Requests with `system.run`, `system.run.prepare`, or `system.which`: `operator.pairing` + `operator.admin`

**Presence:**
- `system-presence` returns entries keyed by device identity
- Presence entries include `deviceId`, `roles`, and `scopes` so UIs can show a single row per device even when it connects as both **operator** and **node**

### Broadcast Event Scoping

- **Chat, agent, tool-result frames**: require at least `operator.read`
- **Plugin-defined `plugin.*` broadcasts**: gated to `operator.write` or `operator.admin`
- **Status and transport events**: unrestricted
- **Unknown broadcast event families**: scope-gated by default (fail-closed) unless a registered handler explicitly relaxes them

Each client connection keeps its own per-client sequence number so broadcasts preserve monotonic ordering on that socket even when different clients see different scope-filtered subsets.

### Common RPC Method Families

**System and identity:**
- `health` — cached or fresh gateway health snapshot
- `diagnostics.stability` — recent bounded diagnostic stability recorder (operational metadata; no chat text, webhook bodies, or secrets)
- `status` — gateway summary; sensitive fields included only for admin-scoped operator clients
- `gateway.identity.get` — gateway device identity
- `system-presence` — current presence snapshot
- `system-event` — appends a system event
- `last-heartbeat` — latest persisted heartbeat event
- `set-heartbeats` — toggles heartbeat processing on the gateway

**Models and usage:**
- `models.list` — runtime-allowed model catalog
- `usage.status` — provider usage windows/remaining quota
- `usage.cost` — aggregated cost usage summaries for a date range
- `doctor.memory.status` — vector-memory / embedding readiness
- `sessions.usage` — per-session usage summaries
- `sessions.usage.timeseries` — timeseries usage for one session
- `sessions.usage.logs` — usage log entries for one session

**Channels and login:**
- `channels.status` — channel/plugin status summaries
- `channels.logout` — logs out a specific channel/account
- `web.login.start` / `web.login.wait` — QR/web login flows
- `push.test` — sends a test APNs push
- `voicewake.get` / `voicewake.set` — wake-word triggers

**Messaging and logs:**
- `send` — direct outbound-delivery RPC for channel/account/thread-targeted sends
- `logs.tail` — configured gateway file-log tail with cursor/limit and max-byte controls

**Talk and TTS:**
- `talk.config` — effective Talk config payload
- `talk.mode` — sets/broadcasts current Talk mode state
- `talk.speak` — synthesizes speech
- `tts.status`, `tts.providers`, `tts.enable`, `tts.disable`, `tts.setProvider`, `tts.convert`

**Secrets, config, update, and wizard:**
- `secrets.reload` — re-resolves active SecretRefs
- `config.get` — current config snapshot and hash
- `config.set` — writes a validated config payload
- `config.patch` — merges a partial config update
- `config.apply` — validates + replaces the full config payload
- `secrets.resolve` — resolves command-target secret assignments for a specific command/target set
- `config.schema` — live config schema payload (includes field `title`/`description`, plugin + channel schemas, `uiHints`)
- `config.schema.lookup` — path-scoped schema node for drill-down tooling (normalized path, shallow schema, matched hint + `hintPath`, immediate child summaries)
- `update.run` — runs the gateway update flow
- `wizard.start`, `wizard.next`, `wizard.status`, `wizard.cancel` — onboarding wizard over WS RPC

**Agent and workspace helpers:**
- `agents.list`, `agents.create`, `agents.update`, `agents.delete`
- `agents.files.list`, `agents.files.get`, `agents.files.set` — bootstrap workspace files
- `agent.identity.get` — effective assistant identity
- `agent.wait` — waits for a run to finish

**Session control:**
- `sessions.list`, `sessions.subscribe`, `sessions.unsubscribe`
- `sessions.preview` — bounded transcript previews
- `sessions.create`, `sessions.send`, `sessions.steer`, `sessions.abort`, `sessions.patch`
- `sessions.reset`, `sessions.delete`, `sessions.compact`, `sessions.get`
- `chat.history`, `chat.send`, `chat.abort`, `chat.inject` — for chat execution

**Device pairing:**
- `device.pair.list`, `device.pair.approve`, `device.pair.reject`, `device.pair.remove`
- `device.token.rotate`, `device.token.revoke`

**Node pairing and invoke:**
- `node.pair.request`, `node.pair.list`, `node.pair.approve`, `node.pair.reject`, `node.pair.verify`
- `node.list`, `node.describe`, `node.rename`, `node.invoke`, `node.invoke.result`
- `node.pending.pull`, `node.pending.ack`, `node.pending.enqueue`, `node.pending.drain`

**Approval families:**
- `exec.approval.request`, `exec.approval.get`, `exec.approval.list`, `exec.approval.resolve`, `exec.approval.waitDecision`
- `exec.approvals.get`, `exec.approvals.set`, `exec.approvals.node.get`, `exec.approvals.node.set`
- `plugin.approval.request`, `plugin.approval.list`, `plugin.approval.waitDecision`, `plugin.approval.resolve`

**Automation, skills, and tools:**
- `wake` — schedules an immediate or next-heartbeat wake
- `cron.list`, `cron.status`, `cron.add`, `cron.update`, `cron.remove`, `cron.run`, `cron.runs`
- `commands.list`, `skills.*`, `tools.catalog`, `tools.effective`

### Common Event Families

- `chat` — UI chat updates
- `session.message` / `session.tool` — transcript/event-stream updates
- `sessions.changed` — session index or metadata changed
- `presence` — system presence snapshot updates
- `tick` — periodic keepalive / liveness event
- `health` — gateway health snapshot update
- `heartbeat` — heartbeat event stream update
- `cron` — cron run/job change event
- `shutdown` — gateway shutdown notification
- `node.pair.requested` / `node.pair.resolved` — node pairing lifecycle
- `node.invoke.request` — node invoke request broadcast
- `device.pair.requested` / `device.pair.resolved` — paired-device lifecycle
- `voicewake.changed` — wake-word trigger config changed
- `exec.approval.requested` / `exec.approval.resolved` — exec approval lifecycle
- `plugin.approval.requested` / `plugin.approval.resolved` — plugin approval lifecycle

---

## RPC Adapters Reference

OpenClaw integrates external CLIs via JSON-RPC using two patterns.

### Pattern A: HTTP Daemon (signal-cli)

- `signal-cli` runs as a daemon with JSON-RPC over HTTP
- Event stream is SSE (`/api/v1/events`)
- Health probe: `/api/v1/check`
- OpenClaw owns lifecycle when `channels.signal.autoStart=true`

See [Signal](/channels/signal) for setup and endpoints.

### Pattern B: stdio Child Process (legacy: imsg)

> **Note**: For new iMessage setups, use [BlueBubbles](/channels/bluebubbles) instead.

- OpenClaw spawns `imsg rpc` as a child process
- JSON-RPC is line-delimited over stdin/stdout (one JSON object per line)
- No TCP port, no daemon required

Core methods:
- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (probe/diagnostics)

**Adapter guidelines:**
- Gateway owns the process (start/stop tied to provider lifecycle)
- Keep RPC clients resilient: timeouts, restart on exit
- Prefer stable IDs (e.g., `chat_id`) over display strings

---

## CLI Reference

### Command Index

```
openclaw [--dev] [--profile <name>] <command>
```

| Area | Commands |
|---|---|
| Setup and onboarding | `setup` · `onboard` · `configure` · `config` · `completion` · `doctor` · `dashboard` |
| Reset and uninstall | `backup` · `reset` · `uninstall` · `update` |
| Messaging and agents | `message` · `agent` · `agents` · `acp` · `mcp` |
| Health and sessions | `status` · `health` · `sessions` |
| Gateway and logs | `gateway` · `logs` · `system` |
| Models and inference | `models` · `infer` · `memory` · `wiki` |
| Network and nodes | `directory` · `nodes` · `devices` · `node` |
| Runtime and sandbox | `approvals` · `sandbox` · `tui` · `browser` |
| Automation | `cron` · `tasks` · `hooks` · `webhooks` · `flows` |
| Discovery and docs | `dns` · `docs` |
| Pairing and channels | `pairing` · `qr` · `channels` · `voicecall` |
| Security and plugins | `security` · `secrets` · `skills` · `plugins` · `proxy` |
| Legacy aliases | `daemon` (gateway service) · `clawbot` (namespace) |

### Global Flags

| Flag | Purpose |
|---|---|
| `--dev` | Isolate state under `~/.openclaw-dev` and shift default ports |
| `--profile <name>` | Isolate state under `~/.openclaw-<name>` |
| `--container <name>` | Target a named container for execution |
| `--no-color` | Disable ANSI colors (`NO_COLOR=1` also respected) |
| `--update` | Shorthand for `openclaw update` (source installs only) |
| `-V`, `--version`, `-v` | Print version and exit |

### Output Modes

- ANSI colors and progress indicators render only in TTY sessions
- `--json` (and `--plain` where supported) disables styling for clean output
- OSC-8 hyperlinks render as clickable links where supported

### Core Commands

```bash
# Gateway management
openclaw gateway status
openclaw gateway start / stop / restart
openclaw gateway install / uninstall
openclaw gateway probe
openclaw gateway discover
openclaw gateway call <method> --params "{}"

# Setup & onboarding
openclaw onboard [--install-daemon] [--non-interactive] [--json]
openclaw configure
openclaw config get <path>
openclaw config set <path> <value>
openclaw config unset <path>
openclaw config schema
openclaw config validate
openclaw doctor [--fix] [--yes] [--non-interactive]

# Status & health
openclaw status [--all] [--deep] [--json]
openclaw health [--verbose] [--json]

# Models and auth
openclaw models list [--all] [--provider <name>]
openclaw models status [--probe] [--check] [--json]
openclaw models set <model>
openclaw models auth login --provider <name> [--method <method>]
openclaw models auth order get/set/clear --provider <name>

# Channels
openclaw channels list
openclaw channels status [--probe]
openclaw channels login [--channel <name>] [--account <id>]
openclaw channels logout --channel <name>

# Sessions
openclaw sessions --json [--active <minutes>]
openclaw sessions cleanup --dry-run

# Tasks
openclaw tasks list [--runtime <type>] [--status <status>] [--json]
openclaw tasks show <lookup>
openclaw tasks cancel <lookup>
openclaw tasks notify <lookup> <policy>
openclaw tasks audit [--json]
openclaw tasks maintenance [--apply] [--json]
openclaw tasks flow list/show/cancel

# Cron
openclaw cron list
openclaw cron add --name "..." --cron "0 7 * * *" --session isolated --message "..."
openclaw cron show <jobId>
openclaw cron edit <jobId> [options]
openclaw cron run <jobId> [--due]
openclaw cron runs --id <jobId> --limit 50
openclaw cron remove <jobId>
openclaw cron status

# Hooks
openclaw hooks list [--eligible] [--verbose] [--json]
openclaw hooks info <hook-name>
openclaw hooks check
openclaw hooks enable/disable <hook-name>

# Security
openclaw security audit [--deep] [--fix] [--json]

# Nodes
openclaw nodes status
openclaw nodes describe --node <id>
openclaw nodes invoke --node <id> --command <cmd> --params '{}'
openclaw nodes canvas snapshot/present/hide/navigate/eval
openclaw nodes camera list/snap/clip
openclaw nodes screen record

# Devices
openclaw devices list
openclaw devices approve/reject <requestId>
openclaw devices remove/revoke <id>

# Skills
openclaw skills search "keyword"
openclaw skills install <slug> [--version <v>] [--force]
openclaw skills update [--all]
openclaw skills list [--eligible]
openclaw skills info <slug>
openclaw skills check

# Plugins
openclaw plugins list [--json]
openclaw plugins install <spec>
openclaw plugins uninstall <id>
openclaw plugins update [<id>]
openclaw plugins enable/disable <id>
openclaw plugins doctor

# Update
openclaw update [--channel beta] [--tag main] [--dry-run]

# Uninstall
openclaw uninstall [--all] [--yes] [--non-interactive]
```

### Chat Slash Commands

Highlights:
- `/status` — quick diagnostics
- `/trace` — session-scoped plugin trace/debug lines
- `/config` — persisted config changes
- `/debug` — runtime-only config overrides (memory, not disk; requires `commands.debug: true`)
- `/model` — switch model for the session
- `/new` — start a new session (optionally with a model)
- `/reset` — reset the current session
- `/reasoning` — toggle reasoning display
- `/verbose` — toggle verbose mode
- `/context list` — show what's in the system prompt
- `/subagents` — show subagent status
- `/tasks` — show background tasks linked to this session
- `/agents` — show agent/binding state
- `/focus <target>` — bind current thread to a target (Discord)
- `/unfocus` — detach thread binding
- `/session idle <duration|off>` — set session idle timeout
- `/session max-age <duration|off>` — set session max age

---

## Onboarding Reference

Full reference for `openclaw onboard`.

### Onboarding Flow (Local Mode)

1. **Existing config detection**: Keep / Modify / Reset
   - `--reset` defaults to `config+creds+sessions`; use `--reset-scope full` to include workspace
   - Reset uses `trash` (never `rm`)
   - If the config is invalid or contains legacy keys, the wizard stops and asks you to run `openclaw doctor` before continuing
2. **Model/Auth**: choose provider and auth flow (API key, OAuth, Claude CLI)
   - API key storage: plaintext (default) or `--secret-input-mode ref` for env-backed refs
3. **Workspace**: default `~/.openclaw/workspace`; seeds bootstrap files. Full workspace layout + backup guide: [Agent workspace](/concepts/agent-workspace)
4. **Gateway**: port, bind address, auth mode, Tailscale exposure
   - Auth recommendation: keep **Token** even for loopback
   - In token mode, interactive setup offers: generate/store plaintext token (default) or use SecretRef (opt-in)
   - Quickstart reuses existing `gateway.auth.token` SecretRefs across `env`, `file`, and `exec` providers
   - If that SecretRef is configured but cannot be resolved, onboarding fails early with a clear fix message
   - Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>` (cannot be combined with `--gateway-token`)
   - If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly
5. **Channels**: Telegram, Discord, WhatsApp, Signal, BlueBubbles, etc.
6. **Web search**: Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax Search, Ollama Web Search, Perplexity, SearXNG, or Tavily
7. **Daemon**: LaunchAgent (macOS) / systemd user unit (Linux/WSL2) / Scheduled Task (Windows native)
   - **Runtime selection:** Node (recommended; required for WhatsApp/Telegram). Bun is **not recommended**
   - Linux onboarding attempts to enable lingering via `loginctl enable-linger <user>` (may prompt for sudo)
   - If token auth requires a token and `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist resolved plaintext token values into supervisor service environment metadata
8. **Health check**: starts Gateway and runs `openclaw health`
9. **Skills**: installs recommended skills

### Non-Interactive Mode

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

**Gateway token SecretRef:**
```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
```

**Add another agent (non-interactive):**
```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.4 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

### Gateway Wizard RPC

The Gateway exposes the onboarding flow over RPC:
- `wizard.start`, `wizard.next`, `wizard.cancel`, `wizard.status`

### Supported Providers in Onboarding

| Provider | Auth Method | Notes |
|---|---|---|
| Anthropic | API key / Claude CLI / setup-token | API key most predictable for servers; setup-token still available though OpenClaw now prefers Claude CLI reuse |
| OpenAI | API key / OAuth / Codex subscription (OAuth or device pairing) | Codex sets model to `openai-codex/gpt-5.5`; API key sets to `openai/gpt-5.4` when unset or OpenAI-family |
| xAI (Grok) | API key (`XAI_API_KEY`) | |
| OpenCode | API key (`OPENCODE_API_KEY`) | Get at https://opencode.ai/auth |
| Ollama | API key / local | Cloud+Local / Cloud only / Local only; auto-pull selected local model |
| Vercel AI Gateway | API key (`AI_GATEWAY_API_KEY`) | Multi-model proxy |
| Cloudflare AI Gateway | Account ID + Gateway ID + API key | |
| MiniMax | Auto-configured | Default: `MiniMax-M2.7`; API-key uses `minimax/...`, OAuth uses `minimax-portal/...` |
| StepFun | Auto-configured | Standard or Step Plan |
| Synthetic | API key (`SYNTHETIC_API_KEY`) | Anthropic-compatible |
| Moonshot (Kimi K2) | Auto-configured | |
| Kimi Coding | Auto-configured | |
| StepFun | Auto-configured | Standard or Step Plan, China or global endpoints |

### What the Wizard Writes

Key fields in `~/.openclaw/openclaw.json`:
- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers`
- `tools.profile` (defaults to `"coding"` when unset on local onboarding; existing explicit values preserved)
- `gateway.*` (mode, bind, auth, tailscale)
- `session.dmScope`
- Channel tokens (`channels.telegram.botToken`, `channels.discord.token`, etc.)
- Channel allowlists when you opt in
- `skills.install.nodeManager` (accepts `npm`, `pnpm`, `yarn`, or `bun`)
- `wizard.lastRunAt`, `wizard.lastRunVersion`, `wizard.lastRunCommit`, `wizard.lastRunCommand`, `wizard.lastRunMode`

**Add another agent (non-interactive):**
```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.4 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

`openclaw agents add` writes `agents.list[]` and optional `bindings`.

**Storage locations:**
- WhatsApp credentials: `~/.openclaw/credentials/whatsapp/<accountId>/`
- Sessions: `~/.openclaw/agents/<agentId>/sessions/`
- Auth profiles: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

---

## File Locations Quick Reference

| Item | Location |
|---|---|
| Main config | `~/.openclaw/openclaw.json` |
| State directory | `~/.openclaw/` |
| Agent directories | `~/.openclaw/agents/<agentId>/` |
| Auth profiles | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| Sessions index | `~/.openclaw/agents/<agentId>/sessions/sessions.json` |
| Session transcripts | `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl` |
| WhatsApp credentials | `~/.openclaw/credentials/whatsapp/<accountId>/creds.json` |
| Channel allowlists | `~/.openclaw/credentials/<channel>-allowFrom.json` |
| Task records | `$OPENCLAW_STATE_DIR/tasks/runs.sqlite` |
| Cron jobs | `~/.openclaw/cron/jobs.json` |
| Cron runtime state | `~/.openclaw/cron/jobs-state.json` |
| Managed hooks | `~/.openclaw/hooks/` |
| Managed skills | `~/.openclaw/skills/` |
| Exec approvals (headless node) | `~/.openclaw/exec-approvals.json` |
| Node host info | `~/.openclaw/node.json` |
| Secrets payload | `~/.openclaw/secrets.json` |
| Gateway env | `~/.openclaw/.env` |
| Media | `~/.openclaw/media/` |
| Logs | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| Plugin extensions | `~/.openclaw/extensions/` |
| Workspace (default) | `~/.openclaw/workspace/` |
| Sandbox workspaces | `~/.openclaw/sandboxes/` |

---

## Environment Variables Quick Reference

| Variable | Purpose |
|---|---|
| `OPENCLAW_HOME` | Override home directory for all internal path resolution |
| `OPENCLAW_STATE_DIR` | Override state directory (default `~/.openclaw`) |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway shared secret token |
| `OPENCLAW_GATEWAY_PASSWORD` | Gateway shared secret password |
| `OPENCLAW_GATEWAY_PORT` | Gateway port (default 18789) |
| `OPENCLAW_GATEWAY_BIND` | Gateway bind mode |
| `OPENCLAW_PROFILE` | Active profile name |
| `OPENCLAW_LOG_LEVEL` | Override log level (e.g., `debug`, `trace`) |
| `OPENCLAW_DIAGNOSTICS` | Diagnostics flags (comma-separated) |
| `OPENCLAW_SKIP_CRON` | Skip cron scheduler |
| `OPENCLAW_SKIP_CHANNELS` | Skip channel providers |
| `OPENCLAW_SKIP_GMAIL_WATCHER` | Skip Gmail watcher |
| `OPENCLAW_NIX_MODE` | Enable Nix deterministic mode |
| `OPENCLAW_NO_RESPAWN` | Avoid self-respawn startup overhead |
| `OPENCLAW_LOAD_SHELL_ENV` | Enable login-shell env import |
| `OPENCLAW_SHELL_ENV_TIMEOUT_MS` | Shell env import timeout |
| `OPENCLAW_THEME` | TUI palette (`light` or `dark`) |
| `OPENCLAW_RAW_STREAM` | Enable raw stream logging |
| `OPENCLAW_RAW_STREAM_PATH` | Custom raw stream log path |
| `OPENCLAW_DEBUG_TIMING` | Enable CLI debug timing (`1` or `json`) |
| `OPENCLAW_CHILD_OOM_SCORE_ADJ` | Disable Linux child OOM bias (`0`, `false`, `no`, `off`) |
| `OPENCLAW_PLUGIN_STAGE_DIR` | Plugin runtime deps stage directory |
| `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` | Allow plaintext `ws://` to trusted private-network IPs (break-glass; no config equivalent, client-side process-env override) |
| `OPENCLAW_APNS_RELAY_BASE_URL` | iOS relay base URL override (temporary env override) |
| `OPENCLAW_APNS_RELAY_TIMEOUT_MS` | iOS relay timeout in milliseconds |
| `OPENCLAW_APNS_RELAY_ALLOW_HTTP` | Allow HTTP relay URL (loopback-only dev escape hatch) |
| `OPENCLAW_APNS_TEAM_ID` | Apple Developer Team ID for direct APNs |
| `OPENCLAW_APNS_KEY_ID` | APNs Key ID |
| `OPENCLAW_APNS_PRIVATE_KEY_P8` | APNs private key content (inline p8) |
| `OPENCLAW_APNS_PRIVATE_KEY_PATH` | Path to APNs private key `.p8` file |
| `PI_RAW_STREAM` | Enable pi-mono raw chunk logging (captures chunks before block parsing) |
| `PI_RAW_STREAM_PATH` | Custom output path for pi-mono raw chunks (JSONL) |
| `NODE_EXTRA_CA_CERTS` | Fix nvm TLS failures (auto-set on Linux; nvm bundled CA store may miss modern root CAs) |
| `NODE_COMPILE_CACHE` | Node module compile cache path |

**Runtime-injected env vars (not user config):**

| Variable | Purpose |
|---|---|
| `OPENCLAW_SHELL=exec` | Set for commands run through the `exec` tool |
| `OPENCLAW_SHELL=acp` | Set for ACP runtime backend process spawns |
| `OPENCLAW_SHELL=acp-client` | Set for `openclaw acp client` ACP bridge process |
| `OPENCLAW_SHELL=tui-local` | Set for local TUI `!` shell commands |

**Env var precedence (highest → lowest):**
1. Process environment (from parent shell/daemon)
2. `.env` in current working directory (dotenv default; does not override)
3. Global `.env` at `~/.openclaw/.env` (does not override)
4. Config `env` block in `~/.openclaw/openclaw.json` (applied only if missing)
5. Optional login-shell import (`env.shellEnv.enabled` or `OPENCLAW_LOAD_SHELL_ENV=1`)

On Ubuntu fresh installs, OpenClaw also treats `~/.config/openclaw/gateway.env` as a compatibility fallback after the global `.env`.

**Env var substitution in config:** Reference env vars in config string values using `${VAR_NAME}` syntax.

**Provider API key env vars:**
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `XAI_API_KEY`
- `GEMINI_API_KEY` / `GOOGLE_API_KEY`
- `OPENROUTER_API_KEY`
- `DISCORD_BOT_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `SLACK_BOT_TOKEN`
