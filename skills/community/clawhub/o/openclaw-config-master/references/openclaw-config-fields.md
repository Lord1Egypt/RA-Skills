# OpenClaw Config Field Index — OpenClaw 2026.3.28

Reference source: `openclaw gateway call config.schema` (version 2026.3.28, generated 2026-03-22).

Config file: `~/.openclaw/openclaw.json` (JSON5). Override path via `OPENCLAW_CONFIG_PATH`. Split config via `$include` (preprocessing directive handled in `src/config/includes.ts`).

---

## Root Keys (Top-Level)

The root object is strict — aside from `$include`, unknown keys fail validation.

| Key | Description |
|-----|-------------|
| `meta` | System metadata (`lastTouchedVersion`, `lastTouchedAt`) |
| `env` | Shell env import + env var sugar (string catchall) |
| `wizard` | Wizard run metadata |
| `diagnostics` | Diagnostics / otel / cacheTrace |
| `logging` | Log level / output / redaction |
| `update` | Update channel + check-on-start |
| `browser` | Browser / CDP settings |
| `ui` | UI styling + assistant name / avatar |
| `auth` | Auth profiles / order / cooldowns |
| `models` | Model providers / definitions |
| `nodeHost` | Node host settings (includes `browserProxy`) |
| `agents` | `agents.defaults` + `agents.list`（完整文档见下方） |
| `channels` | Channel providers（完整文档见 `channels-config.md`） |
| `tools` | Global tool policy + exec / web / media / links |
| `bindings` | **Array** of route objects — route channel/account/peer to agents |
| `broadcast` | Broadcast strategy + peer→agentId mapping |
| `audio` | Audio settings (e.g., transcription) |
| `media` | Media pipeline settings (e.g., `preserveFilenames`) |
| `messages` | Message behavior / prefixing |
| `commands` | Chat command settings |
| `approvals` | Approvals policy (exec/plugin modes, target-based rules) |
| `session` | Session policy |
| `cron` | Cron store / concurrency |
| `hooks` | Hooks server + gmail / internal mappings |
| `web` | WebSocket / reconnect settings |
| `channels` | Channel providers (telegram / discord / slack / feishu / ...) |
| `discovery` | mdns / wideArea |
| `canvasHost` | Canvas Host |
| `talk` | Talk / TTS shortcuts |
| `gateway` | Gateway service / auth / remote / tls / http endpoints / nodes |
| `memory` | Memory backend / citations / qmd |
| `skills` | Skills loading / install / entries |
| `plugins` | Plugins loading / entries / installs |
| `acp` | ACP runtime configuration (dispatch, backend, stream settings) |
| `cli` | CLI-specific configuration |
| `mcp` | MCP (Model Context Protocol) servers configuration |
| `secrets` | Secrets management (providers, resolution, defaults) |

---

## `agents` — Agent Configuration

### `agents.defaults` (All Fields)

Default values applied to every agent. These 40+ fields cover model selection, bootstrap, context management, streaming, timing, and sandbox behavior.

```json
"agents": {
  "defaults": {
    "model": { "primary": "...", "fallbacks": ["..."] },
    "imageModel": "...",
    "imageGenerationModel": { "primary": "..." },
    "pdfModel": "...",
    "pdfMaxBytesMb": 50,
    "pdfMaxPages": 1000,
    "models": { ... },
    "workspace": "/home/node/.openclaw/workspace",
    "repoRoot": "/home/node",
    "skipBootstrap": false,
    "bootstrapMaxChars": 60000,
    "bootstrapTotalMaxChars": 200000,
    "bootstrapPromptTruncationWarning": true,
    "userTimezone": "UTC",
    "timeFormat": "system",
    "envelopeTimezone": "UTC",
    "envelopeTimestamp": true,
    "envelopeElapsed": true,
    "contextTokens": 8192,
    "cliBackends": { ... },
    "memorySearch": { ... },
    "contextPruning": { ... },
    "compaction": { "mode": "safeguard" },
    "embeddedPi": { ... },
    "thinkingDefault": false,
    "verboseDefault": false,
    "elevatedDefault": false,
    "blockStreamingDefault": false,
    "blockStreamingBreak": null,
    "blockStreamingChunk": { ... },
    "blockStreamingCoalesce": { ... },
    "humanDelay": { "min": 0, "max": 0 },
    "timeoutSeconds": 120,
    "mediaMaxMb": 100,
    "imageMaxDimensionPx": 4096,
    "typingIntervalSeconds": 30,
    "typingMode": "fast",
    "heartbeat": { ... },
    "maxConcurrent": 5,
    "subagents": { "maxConcurrent": 3, "maxChildrenPerAgent": 2 },
    "sandbox": { ... }
  }
}
```

#### Model Fields
- **`model`** — Primary chat model with fallback chain: `{ primary: "provider/model", fallbacks: ["..."] }`
- **`imageModel`** — Model for image understanding (for backward compat; prefer `imageGenerationModel` for generation)
- **`imageGenerationModel`** — Model for image generation: `{ primary: "provider/model" }`
- **`pdfModel`** — Model for PDF parsing
- **`pdfMaxBytesMb`** / **`pdfMaxPages`** — PDF size/page limits
- **`models`** — Full models config object (providers, definitions, etc.)

#### Workspace & Paths
- **`workspace`** — Default workspace directory for agents
- **`repoRoot`** — Root directory for repository operations

#### Bootstrap
- **`skipBootstrap`** — Skip bootstrap prompt injection (`boolean`)
- **`bootstrapMaxChars`** — Per-step bootstrap character limit (`integer`)
- **`bootstrapTotalMaxChars`** — Total bootstrap character budget (`integer`)
- **`bootstrapPromptTruncationWarning`** — Warn when truncating bootstrap prompt (`boolean`)

#### Context & Envelope
- **`contextTokens`** — Context window size hint (`integer`)
- **`contextPruning`** — Object with pruning strategy settings
- **`cliBackends`** — CLI backend overrides (object)
- **`memorySearch`** — Memory search configuration (object)
- **`envelopeTimezone`** / **`timeFormat`** / **`envelopeTimestamp`** / **`envelopeElapsed`** — Envelope formatting controls
- **`userTimezone`** — User timezone for date/time formatting

#### Agent Behavior Flags
- **`thinkingDefault`** — Enable chain-of-thought reasoning by default
- **`verboseDefault`** — Verbose output mode by default
- **`elevatedDefault`** — Run with elevated permissions by default
- **`blockStreamingDefault`** — Block streaming output by default
- **`blockStreamingBreak`** / **`blockStreamingChunk`** / **`blockStreamingCoalesce`** — Streaming control sub-objects

#### Timing & Interaction
- **`humanDelay`** — Simulated human delay: `{ min: ms, max: ms }`
- **`timeoutSeconds`** — Default request timeout (`integer`)
- **`typingIntervalSeconds`** / **`typingMode`** — Typing simulation controls
- **`heartbeat`** — Heartbeat interval configuration (object)

#### Media & Images
- **`mediaMaxMb`** — Max media file size in MB (`number`)
- **`imageMaxDimensionPx`** — Max image dimension in pixels (`integer`)

#### Concurrency & Sandbox
- **`maxConcurrent`** — Max concurrent operations (`integer`)
- **`subagents`** — Subagent policy: `{ maxConcurrent: N, maxChildrenPerAgent: N }`
- **`sandbox`** — Sandbox configuration (object)

#### Compacttion
- **`compaction`** — Compaction strategy: `{ mode: "safeguard" | "aggressive" }`

#### Embedded Pi
- **`embeddedPi`** — Embedded PI configuration (object)

---

### `agents.list` (Per-Agent Overrides)

Array of agent definitions. Each agent can override `agents.defaults` and specify additional fields:

```json
"agents": {
  "list": [{
    "id": "agent-id",
    "name": "Agent Name",
    "model": { ... },
    "fastModeDefault": false,
    "reasoningDefault": false,
    "thinkingDefault": false,
    "runtime": "local",
    "params": { ... },
    "identity": { ... },
    "groupChat": { ... },
    "workspace": "/path",
    "agentDir": "/path",
    "skills": ["skill-id", ...],
    "tools": { ... },
    "subagents": { ... },
    "sandbox": { ... },
    "heartbeat": { ... },
    "humanDelay": { ... },
    "memorySearch": { ... }
  }]
}
```

Key per-agent fields:
- **`id`** / **`name`** — Agent identifier and display name
- **`runtime`** — Runtime backend: `"local"` | `"acp"` (ACP runtime)
- **`model`** / **`fastModeDefault`** / **`reasoningDefault`** / **`thinkingDefault`** — Model and behavior overrides
- **`identity`** — Identity configuration for this agent
- **`groupChat`** — Group chat settings
- **`workspace`** / **`agentDir`** — Paths specific to this agent
- **`skills`** — List of skill IDs to load for this agent
- **`tools`** / **`subagents`** / **`sandbox`** — Tool/subagent/sandbox overrides
- **`params`** — Arbitrary agent parameters
- **`heartbeat`** / **`humanDelay`** / **`memorySearch`** — Per-agent timing/memory overrides

---

### `agents.list` (Per-Agent Overrides)

Array of agent definitions. Each agent can override `agents.defaults` and specify additional fields:

```json
"agents": {
  "list": [{
    "id": "agent-id",
    "name": "Agent Name",
    "model": { "primary": "provider/model", "fallbacks": ["..."] },
    "fastModeDefault": false,
    "reasoningDefault": false,
    "thinkingDefault": false,
    "runtime": "local",
    "params": { ... },
    "identity": { ... },
    "groupChat": { ... },
    "workspace": "/path",
    "agentDir": "/path",
    "skills": ["skill-id", ...],
    "tools": { ... },
    "subagents": { ... },
    "sandbox": { ... },
    "heartbeat": { ... },
    "humanDelay": { ... },
    "memorySearch": { ... }
  }]
}
```

Key per-agent fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Agent unique identifier |
| `name` | string | Display name |
| `runtime` | enum | Runtime backend: `"local"` \| `"acp"` (ACP runtime) |
| `model.primary` | string | Primary model override: `"provider/model"` |
| `model.fallbacks` | array | Fallback model chain |
| `fastModeDefault` | boolean | Enable fast mode by default |
| `reasoningDefault` | boolean | Enable chain-of-thought reasoning by default |
| `thinkingDefault` | boolean | Enable thinking by default |
| `identity` | object | Identity overrides for this agent |
| `groupChat` | object | `{ mentionPatterns, ... }` — group chat behavior |
| `workspace` | string | Agent-specific workspace directory |
| `agentDir` | string | Agent-specific persistent state directory |
| `skills` | array | List of skill IDs to load for this agent |
| `tools` | object | Tool allowlist/denylist overrides for this agent |
| `subagents` | object | Subagent policy overrides |
| `sandbox` | object | Sandbox configuration overrides |
| `heartbeat` | object | Per-agent heartbeat interval override |
| `humanDelay` | object | Per-agent `{ min, max }` human delay override |
| `memorySearch` | object | Per-agent memory search config |
| `params` | object | Arbitrary agent parameters |

**`runtime: "acp"`** — When `runtime` is set to `"acp"`, the agent runs under the ACP runtime. The `params` object can include ACP-specific settings.

**`groupChat.mentionPatterns`** — Safe regex patterns to trigger agent in group chats without native @-mention:

```json
"groupChat": {
  "mentionPatterns": ["@openclaw", "openclaw", "jarvis"]
}
```

**`identity`** — Override agent identity for this specific agent:

```json
"identity": {
  "name": "Custom Name",
  "avatar": "https://example.com/avatar.png",
  "emoji": "🤖"
}
```

---

## `tools` — Tool Configuration

### `tools` Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile` | enum | Tool profile preset: `"minimal"` \| `"coding"` \| `"messaging"` \| `"full"` |
| `allow` | array | Allowed tool names (empty = all allowed) |
| `alsoAllow` | array | Additional allowed tools beyond profile |
| `deny` | array | Explicitly denied tool names |
| `byProvider` | object | Per-provider tool allowlist/denylist |
| `elevated` | object | `{ enabled, allowFrom }` — elevated tool permissions |
| `sessions` | object | `{ visibility }` — session tool settings |
| `sessions_spawn` | object | `{ attachments }` — spawn session attachments config |
| `loopDetection` | object | Loop/circuit-breaker detection config |
| `message` | object | `{ allowCrossContextSend, broadcast, crossContext }` — message tool |
| `agentToAgent` | object | `{ enabled, allow }` — agent-to-agent calls |
| `subagents` | object | `{ tools }` — subagent tool config |
| `sandbox` | object | `{ tools }` — sandbox tool config |
| `exec` | object | Exec tool configuration |
| `web` | object | Web tool (search, fetch, x_search) |
| `links` | object | Link-expansion tool settings |
| `media` | object | Media pipeline (audio, image, video, concurrency) |
| `fs` | object | `{ workspaceOnly }` — filesystem access controls |

---

### `tools.profile` — Tool Presets

Four preset profiles control which tools are available by default:

- **`"minimal"`** — Core tools only (read, write, exec, browser basics)
- **`"coding"`** — Minimal + coding tools (code review, git, etc.)
- **`"messaging"`** — Minimal + messaging/send tools (NEW in 2026.3.x)
- **`"full"`** — All tools enabled

Customize with `tools.alsoAllow` / `tools.deny` to add or remove from a profile.

---

### `tools.exec` — Shell Execution Tool

Controls where and how `exec` tool runs.

> **重要**：`tools.exec` 只支持以下字段。**不支持** `approvals`、`allowFrom` 等字段。
> 添加不支持的字段会导致 schema 验证失败，Gateway 无法启动。
> exec 审批配置请使用 `channels.<channel>.execApprovals`。
> 命令权限白名单请使用 `commands.allowFrom`。

```json
"tools": {
  "exec": {
    "security": "allowlist",
    "ask": "on-miss"
  }
}
```

**完整字段示例**：

```json
"tools": {
  "exec": {
    "host": "sandbox",
    "node": "node-id",
    "security": "deny",
    "ask": "off",
    "pathPrepend": ["/usr/local/bin"],
    "safeBins": ["ls", "cat", "grep", ...],
    "safeBinTrustedDirs": ["/usr/bin", "/bin"],
    "safeBinProfiles": { ... },
    "strictInlineEval": false,
    "backgroundMs": 5000,
    "timeoutSec": 60,
    "cleanupMs": 3000,
    "notifyOnExit": false,
    "notifyOnExitEmptySuccess": false,
    "applyPatch": {
      "enabled": true,
      "allowModels": ["provider/model", ...],
      "workspaceOnly": false
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | Where exec runs: `"sandbox"` \| `"gateway"` \| `"node"` |
| `node` | string | Node name when `host: "node"` |
| `security` | string | Security mode: `"deny"` \| `"allowlist"` \| `"full"` |
| `ask` | string | Approval mode: `"off"` \| `"on-miss"` \| `"always"` |
| `pathPrepend` | array | Directories prepended to `$PATH` |
| `safeBins` | array | List of permitted executables |
| `safeBinTrustedDirs` | array | Trusted directories for executable lookup |
| `safeBinProfiles` | object | Named profiles with different safe bin sets |
| `strictInlineEval` | boolean | Disallow inline code evaluation |
| `backgroundMs` | integer | Max ms to run in background before warning |
| `timeoutSec` | integer | Default exec timeout in seconds |
| `cleanupMs` | integer | Time to wait for cleanup on exit |
| `notifyOnExit` | boolean | Notify when background process exits |
| `notifyOnExitEmptySuccess` | boolean | Notify on zero-exit even if empty output |
| `applyPatch` | object | `{ enabled, allowModels, workspaceOnly }` — patch application |

**不支持的字段**（会导致 schema 验证失败）：
- `approvals` — 应使用 `channels.<channel>.execApprovals`
- `allowFrom` — 应使用 `commands.allowFrom`

---

### `tools.web` — Web Tool

#### `tools.web.search` — Web Search

Restructured in 2026.3.x with provider-specific sub-objects. Top-level fields apply to all providers; each provider block overrides as needed.

```json
"tools": {
  "web": {
    "search": {
      "enabled": true,
      "provider": "brave",
      "maxResults": 10,
      "timeoutSeconds": 30,
      "cacheTtlMinutes": 60,
      "apiKey": "key-or-object",

      "brave": {
        "apiKey": "...",
        "baseUrl": "https://api.search.brave.com",
        "model": "model-name",
        "mode": "default"
      },
      "firecrawl": {
        "apiKey": "...",
        "baseUrl": "https://api.firecrawl.dev",
        "model": "model-name"
      },
      "gemini": {
        "apiKey": "...",
        "baseUrl": "https://generativelanguage.googleapis.com",
        "model": "gemini-model"
      },
      "grok": {
        "apiKey": "...",
        "baseUrl": "https://api.x.ai",
        "model": "grok-model",
        "inlineCitations": true
      },
      "kimi": {
        "apiKey": "...",
        "baseUrl": "https://api.moonshot.cn",
        "model": "kimi-model"
      },
      "perplexity": {
        "apiKey": "...",
        "baseUrl": "https://api.perplexity.ai",
        "model": "sonar-model"
      }
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable web search |
| `provider` | string | Default provider name |
| `maxResults` | integer | Max results per search |
| `timeoutSeconds` | integer | Search timeout |
| `cacheTtlMinutes` | number | Cache TTL in minutes |
| `apiKey` | string/object | Top-level API key (or per-provider) |

Provider blocks (`brave`, `firecrawl`, `gemini`, `grok`, `kimi`, `perplexity`) each accept: `apiKey`, `baseUrl`, `model`. `grok` additionally has `inlineCitations`.

#### `tools.web.fetch` — Page Fetching

```json
"tools": {
  "web": {
    "fetch": {
      "enabled": true,
      "maxChars": 50000,
      "maxCharsCap": 100000,
      "maxResponseBytes": 1048576,
      "maxRedirects": 5,
      "timeoutSeconds": 30,
      "cacheTtlMinutes": 60,
      "userAgent": "Mozilla/5.0 ...",
      "readability": true,
      "firecrawl": { "apiKey": "...", "baseUrl": "..." }
    }
  }
}
```

#### `tools.web.x_search` — X (Twitter) Search

```json
"tools": {
  "web": {
    "x_search": {
      "enabled": true,
      "timeoutSeconds": 30,
      "cacheTtlMinutes": 60,
      "maxTurns": 5,
      "inlineCitations": true,
      "model": "model-name",
      "apiKey": "key-or-object"
    }
  }
}
```

---

### `tools.loopDetection` — Loop & Circuit Breaker

```json
"tools": {
  "loopDetection": {
    "enabled": true,
    "historySize": 100,
    "warningThreshold": 5,
    "criticalThreshold": 10,
    "globalCircuitBreakerThreshold": 50,
    "detectors": { ... }
  }
}
```

---

### `tools.message` — Cross-Context Messaging

```json
"tools": {
  "message": {
    "allowCrossContextSend": false,
    "broadcast": { ... },
    "crossContext": { ... }
  }
}
```

---

## `gateway` — Gateway Service

### `gateway` Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `port` | integer | Gateway port |
| `mode` | string | `"local"` \| `"remote"` |
| `bind` | string | `"auto"` \| `"lan"` \| `"loopback"` \| `"custom"` \| `"tailnet"` |
| `customBindHost` | string | Custom bind host when `bind: "custom"` |
| `allowRealIpFallback` | boolean | Allow real IP fallback when proxy headers unavailable |
| `channelHealthCheckMinutes` | integer | Channel health check interval |
| `channelStaleEventThresholdMinutes` | integer | Stale event threshold |
| `channelMaxRestartsPerHour` | integer | Max channel restarts per hour |
| `auth` | object | Auth mode, token, password, rate limit |
| `trustedProxies` | array | Trusted proxy IPs |
| `tailscale` | object | Tailscale mode + resetOnExit |
| `controlUi` | object | Control UI settings |
| `remote` | object | Remote gateway (url, transport, tls, ssh) |
| `reload` | object | Hot reload mode + debounce/deferral |
| `tls` | object | TLS settings |
| `http` | object | HTTP endpoints + security headers |
| `push` | object | Push notifications (APNS relay) |
| `nodes` | object | Node browser proxy + commands |
| `tools` | object | `{ allow, deny }` — gateway-level tool access |

---

### `gateway.controlUi` — Control UI

```json
"gateway": {
  "controlUi": {
    "enabled": true,
    "basePath": "/",
    "root": "/path/to/ui",
    "allowedOrigins": ["https://example.com"],
    "allowInsecureAuth": false,
    "dangerouslyDisableDeviceAuth": false,
    "dangerouslyAllowHostHeaderOriginFallback": false
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable control UI |
| `basePath` | string | UI base path |
| `root` | string | UI static files root |
| `allowedOrigins` | array | CORS allowed origins |
| `allowInsecureAuth` | boolean | Allow auth over plain HTTP |
| `dangerouslyDisableDeviceAuth` | boolean | Disable device authentication |
| `dangerouslyAllowHostHeaderOriginFallback` | boolean | **NEW** — Fall back to `Host` header for origin (use with caution) |

---

### `gateway.reload` — Hot Reload

```json
"gateway": {
  "reload": {
    "mode": "hot",
    "debounceMs": 500,
    "deferralTimeoutMs": 5000
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `mode` | string | `"off"` \| `"restart"` \| `"hot"` \| `"hybrid"` |
| `debounceMs` | integer | Debounce interval for config changes |
| `deferralTimeoutMs` | integer | **NEW** — Max ms to defer reload during active operations |

---

### `gateway.remote` — Remote Gateway

```json
"gateway": {
  "remote": {
    "url": "https://...",
    "transport": "ssh",
    "token": "...",
    "password": "...",
    "tlsFingerprint": "...",
    "sshTarget": "user@host",
    "sshIdentity": "/path/to/identity"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Remote gateway URL |
| `transport` | string | `"ssh"` \| `"direct"` |
| `token` / `password` | string | Auth credentials |
| `tlsFingerprint` | string | **NEW** — TLS certificate fingerprint |
| `sshTarget` | string | **NEW** — SSH target (`user@host`) |
| `sshIdentity` | string | **NEW** — SSH identity file path |

---

### `gateway.http` — HTTP Endpoints

**NEW** subsystem in 2026.3.x.

```json
"gateway": {
  "http": {
    "endpoints": {
      "chatCompletions": {
        "enabled": true
      },
      "responses": {
        "enabled": true,
        "maxBodyBytes": 10485760,
        "maxUrlParts": 10,
        "files": { ... },
        "images": { ... }
      }
    },
    "securityHeaders": {
      "strictTransportSecurity": "max-age=31536000; includeSubDomains"
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `endpoints.chatCompletions.enabled` | boolean | Enable `/v1/chat/completions` endpoint |
| `endpoints.responses.enabled` | boolean | Enable Responses API endpoint |
| `endpoints.responses.maxBodyBytes` | integer | Max request body size |
| `endpoints.responses.maxUrlParts` | integer | Max URL parts for file URLs |
| `endpoints.responses.files` | object | File download config (allowedMimes, maxBytes, maxRedirects, timeoutMs) |
| `endpoints.responses.images` | object | Image upload config (maxImageParts, maxTotalImageBytes) |
| `securityHeaders.strictTransportSecurity` | string | HSTS header value |

---

### `gateway.push` — Push Notifications

```json
"gateway": {
  "push": {
    "apns": {
      "relay": {
        "baseUrl": "https://push.example.com",
        "timeoutMs": 5000
      }
    }
  }
}
```

---

### `gateway.nodes` — Node Browser Proxy

```json
"gateway": {
  "nodes": {
    "browser": {
      "mode": "auto",
      "node": "node-id"
    },
    "allowCommands": ["npx", "npm"],
    "denyCommands": ["rm", "dd"]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `browser.mode` | string | `"auto"` \| `"manual"` \| `"off"` |
| `browser.node` | string | Specific node for browser proxy |
| `allowCommands` / `denyCommands` | array | Allowed/denied node commands |

---

## `approvals` — Approvals Policy

Controls elevated tool execution approval flows.

```json
"approvals": {
  "exec": {
    "enabled": true,
    "mode": "session",
    "agentFilter": ["agent-id", ...],
    "sessionFilter": ["session-pattern", ...],
    "targets": [
      { "channel": "telegram", "accountId": "123", "threadId": "456" }
    ]
  },
  "plugin": {
    "enabled": true,
    "mode": "session",
    "agentFilter": [...],
    "sessionFilter": [...],
    "targets": [...]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `exec.enabled` | boolean | Enable exec approval |
| `exec.mode` | string | `"session"` \| `"targets"` \| `"both"` — when to trigger approval |
| `exec.agentFilter` | array | Only approve for these agent IDs |
| `exec.sessionFilter` | array | Only approve for matching sessions |
| `exec.targets` | array | Per-target rules: `{ channel, to, accountId, threadId }` |
| `plugin.*` | — | Same structure for plugin execution approvals |

---

## `hooks` — Hooks Server

```json
"hooks": {
  "enabled": true,
  "path": "/path/to/hooks",
  "token": "hook-token",
  "defaultSessionKey": "default-key",
  "allowRequestSessionKey": false,
  "allowedSessionKeyPrefixes": ["prefix:", ...],
  "allowedAgentIds": ["agent-id", ...],
  "maxBodyBytes": 1048576,
  "presets": [...],
  "transformsDir": "/path/to/transforms",
  "mappings": [...],
  "gmail": {
    "hookUrl": "https://...",
    "model": "gpt-4o",
    "account": "user@gmail.com",
    "label": "INBOX",
    "maxBytes": 1048576,
    "includeBody": true,
    "allowUnsafeExternalContent": false,
    "thinking": null,
    "pushToken": "...",
    "renewEveryMinutes": 60,
    "topic": "...",
    "subscription": "...",
    "tailscale": { ... },
    "serve": { ... }
  },
  "internal": {
    "enabled": false,
    "entries": { ... },
    "handlers": [...],
    "installs": { ... },
    "load": { ... }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable hooks server |
| `path` | string | Hooks directory path |
| `token` | string | Hook authentication token |
| `defaultSessionKey` | string | **NEW** — Default session key for hook requests |
| `allowRequestSessionKey` | boolean | **NEW** — Allow hook to specify session key |
| `allowedSessionKeyPrefixes` | array | **NEW** — Allowed session key prefixes |
| `allowedAgentIds` | array | **NEW** — Agents this hook can trigger |
| `maxBodyBytes` | integer | **NEW** — Max request body size |
| `presets` | array | **NEW** — Preset hook configurations |
| `transformsDir` | string | **NEW** — Directory for request/response transforms |
| `mappings` | array | **NEW** — Hook-to-agent mappings |
| `gmail.*` | — | Gmail hook integration (webhook, model, account, etc.) |
| `internal.*` | — | Internal hooks configuration |

---

## `bindings` — Route Binding (Array, Not Object)

**Changed in 2026.3.x from object to array of route objects.**

```json
"bindings": [
  {
    "type": "route",
    "agentId": "agent-id",
    "comment": "optional note",
    "match": {
      "channel": "telegram",
      "accountId": "123456",
      "peer": "user@domain"
    }
  }
]
```

Each binding routes incoming messages from a specific channel/account/peer to a named agent. Empty array = no routing rules (default agent handles all).

---

## `memory` — Memory Configuration

```json
"memory": {
  "backend": "builtin",
  "citations": "auto",
  "qmd": {
    "command": "qmd",
    "includeDefaultMemory": true,
    "paths": ["/default/path"],
    "scope": { ... },
    "searchMode": "semantic",
    "limits": { ... },
    "sessions": { ... },
    "update": { ... },
    "mcporter": {
      "enabled": false,
      "serverName": "qmd-mcp",
      "startDaemon": true
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `backend` | string | `"builtin"` \| `"qmd"` |
| `citations` | string | `"auto"` \| `"on"` \| `"off"` |
| `qmd.command` | string | QMD binary/command path |
| `qmd.includeDefaultMemory` | boolean | Include default memory files |
| `qmd.paths` | array | Additional memory file paths |
| `qmd.searchMode` | string | `"semantic"` — search mode for QMD |
| `qmd.mcporter` | object | `{ enabled, serverName, startDaemon }` — MCP Porter config |

---

## `acp` — ACP Runtime Configuration (NEW)

ACP (Agent Communication Protocol) runtime settings.

```json
"acp": {
  "enabled": true,
  "dispatch": {
    "enabled": true
  },
  "backend": "built-in",
  "defaultAgent": "default-agent-id",
  "allowedAgents": ["agent-1", "agent-2"],
  "maxConcurrentSessions": 10,
  "stream": {
    "coalesceIdleMs": 100,
    "maxChunkChars": 1000,
    "repeatSuppression": true,
    "deliveryMode": "live",
    "hiddenBoundarySeparator": "newline",
    "maxOutputChars": 100000,
    "maxSessionUpdateChars": 4000,
    "tagVisibility": { ... }
  },
  "runtime": {
    "ttlMinutes": 60,
    "installCommand": "npm install -g @openclaw/acp-runtime"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable ACP runtime |
| `dispatch.enabled` | boolean | Enable ACP dispatch |
| `backend` | string | ACP backend type |
| `defaultAgent` | string | Default agent for ACP requests |
| `allowedAgents` | array | Agents allowed to receive ACP messages |
| `maxConcurrentSessions` | integer | Max concurrent ACP sessions |
| `stream.coalesceIdleMs` | integer | Coalesce idle stream chunks |
| `stream.maxChunkChars` | integer | Max chars per stream chunk |
| `stream.repeatSuppression` | boolean | Suppress repeated stream content |
| `stream.deliveryMode` | string | `"live"` \| `"final_only"` |
| `stream.hiddenBoundarySeparator` | string | `"none"` \| `"space"` \| `"newline"` \| `"paragraph"` |
| `stream.maxOutputChars` | integer | Max total output characters |
| `stream.maxSessionUpdateChars` | integer | Max session update size |
| `runtime.ttlMinutes` | integer | ACP runtime instance TTL |
| `runtime.installCommand` | string | Command to install ACP runtime |

---

## `mcp` — MCP (Model Context Protocol) Servers (NEW)

Configure external MCP servers that agents can use as tools.

```json
"mcp": {
  "servers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
      "env": {
        "DEBUG": true,
        "PORT": 3000
      },
      "cwd": "/working/directory",
      "workingDirectory": "/working/directory"
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `servers.<name>.command` | string | Executable to start the MCP server |
| `servers.<name>.args` | array | Command-line arguments |
| `servers.<name>.env` | object | Environment variables (string \| number \| boolean) |
| `servers.<name>.cwd` | string | Working directory for the server process |
| `servers.<name>.workingDirectory` | string | Alias for `cwd` |

---

## `secrets` — Secrets Management (NEW)

```json
"secrets": {
  "providers": {
    "my-provider": { ... }
  },
  "resolution": {
    "maxBatchBytes": 1048576,
    "maxProviderConcurrency": 10,
    "maxRefsPerProvider": 50
  },
  "defaults": {
    "env": "OPENCLAW_SECRET_",
    "exec": "exec-secret-key",
    "file": "/path/to/default/file"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `providers` | object | Named secret providers with their config |
| `resolution.maxBatchBytes` | integer | Max bytes per secret resolution batch |
| `resolution.maxProviderConcurrency` | integer | Max concurrent provider lookups |
| `resolution.maxRefsPerProvider` | integer | Max refs per provider |
| `defaults.env` | string | Env var prefix for secrets |
| `defaults.exec` | string | Default exec secret key |
| `defaults.file` | string | Default secrets file path |

---

## `cli` — CLI Configuration

```json
"cli": {
  "banner": {
    "taglineMode": false
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `banner.taglineMode` | boolean | Show only tagline in CLI banner |

---

## `channels` — Channel Providers

Note: each channel provider (telegram, discord, slack, feishu, etc.) has its own strict schema.

**Feishu-specific note:** Feishu requires **both** `channels.feishu` AND `plugins.entries.feishu` to be consistently configured. If `plugins.entries.feishu.enabled` is `false` while `channels.feishu.enabled` is `true`, the gateway will log a warning about the inconsistency. For Feishu to function, both must be enabled with matching credentials.

---

## `models` — Model Configuration

The `models` section defines provider credentials and per-model settings.

```json
"models": {
  "providers": {
    "openai": {
      "apiKey": "sk-...",
      "baseUrl": "https://api.openai.com/v1",
      "api": "openai",
      "models": [
        { "id": "gpt-4o", "name": "GPT-4o", "maxTokens": 128000 }
      ]
    }
  }
}
```

`apiKey` can be:
- A plain string: `"sk-..."`
- An object with source: `{ source: "env"|"file"|"exec", provider: "...", id: "..." }`

---

## `skills` — Skills Configuration

```json
"skills": {
  "allowBundled": ["skill-id", ...],
  "load": {
    "extraDirs": ["/path/to/skills"],
    "watch": true,
    "watchDebounceMs": 500
  },
  "install": {
    "preferBrew": false,
    "nodeManager": "npm"
  },
  "entries": {
    "skill-id": {
      "enabled": true,
      "apiKey": "...",
      "env": { "KEY": "value" },
      "config": { ... }
    }
  }
}
```

Note: the local skill installation directory (`~/.openclaw/workspace/skills/`) is managed separately from the `skills` config section.

---

## `plugins` — Plugins Configuration

```json
"plugins": {
  "enabled": true,
  "allow": ["plugin-a", "plugin-b"],
  "deny": [],
  "load": {
    "paths": ["/path/to/plugins"]
  },
  "slots": {
    "memory": "my-memory-plugin"
  },
  "entries": {
    "plugin-id": {
      "enabled": true,
      "config": { ... }
    }
  },
  "installs": {
    "plugin-id": {
      "source": "npm",
      "spec": "@org/plugin",
      "version": "1.0.0",
      "installedAt": "2026-01-01T00:00:00Z"
    }
  }
}
```

---

## `web` — WebSocket Configuration (Top-Level)

Separate from `tools.web` — controls gateway WebSocket behavior.

```json
"web": {
  "someSetting": "..."
}
```

---

## `logging` — Logging Configuration

```json
"logging": {
  "level": "info",
  "output": "stdout",
  "redaction": {
    "keys": ["password", "apiKey", "token"]
  }
}
```

---

## `update` — Update Configuration

```json
"update": {
  "channel": "stable",
  "checkOnStart": true
}
```

---

## `browser` — Browser Configuration

```json
"browser": {
  " CDP": { ... }
}
```

---

## `ui` — UI Configuration

```json
"ui": {
  "styling": { ... },
  "assistant": {
    "name": "Jarvis",
    "avatar": "https://..."
  }
}
```

---

## `auth` — Authentication Configuration

```json
"auth": {
  "profiles": [...],
  "order": ["primary", "secondary"],
  "cooldowns": {
    "failedLoginMs": 30000
  }
}
```

---

## `session` — Session Configuration

Controls session behavior, persistence, and limits.

```json
"session": {
  "store": "memory",
  "maxConcurrent": 100
}
```

---

## `cron` — Cron Configuration

```json
"cron": {
  "store": "memory",
  "concurrency": 5
}
```

---

## `discovery` — Discovery Configuration

```json
"discovery": {
  "mdns": { ... },
  "wideArea": { ... }
}
```

---

## `canvasHost` — Canvas Host

```json
"canvasHost": {
  "enabled": true
}
```

---

## `talk` — Talk / TTS Configuration

```json
"talk": {
  "shortcuts": { ... }
}
```

---

## `audio` — Audio Configuration

```json
"audio": {
  "transcription": {
    "model": "whisper-1"
  }
}
```

---

## `media` — Media Configuration

```json
"media": {
  "preserveFilenames": false,
  "pipeline": { ... }
}
```

---

## `messages` — Message Configuration

```json
"messages": {
  "prefixing": { ... }
}
```

---

## `broadcast` — Broadcast Configuration

```json
"broadcast": {
  "strategy": "round-robin",
  "peerMap": { ... }
}
```

---

## `commands` — Chat Commands

控制聊天命令的行为和权限。

> **重要**：`commands.bash` 必须是**布尔值** `true`/`false`，不能是字符串 `"true"`。
> `commands.allowFrom` 是按 channel 分组的对象，不是数组。
> 命令权限白名单在此配置，**不在** `tools.exec` 中。

```json
"commands": {
  "bash": true,
  "native": "auto",
  "nativeSkills": "auto",
  "restart": true,
  "ownerDisplay": "raw",
  "allowFrom": {
    "telegram": ["577958597"]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `bash` | **boolean** | 启用 bash 命令。必须是 `true`/`false`，不能是字符串 |
| `native` | enum | 原生命令模式：`"auto"` \| `"on"` \| `"off"` |
| `nativeSkills` | enum | 原生技能命令：`"auto"` \| `"on"` \| `"off"` |
| `restart` | boolean | 允许通过命令重启 Gateway |
| `ownerDisplay` | enum | 所有者显示模式：`"raw"` \| `"mention"` \| `"name"` |
| `allowFrom` | object | 命令权限白名单，按 channel 分组。格式：`{ "<channel>": ["userId", ...] }` |

---

## `models.providers` — Model Provider Credentials

配置模型提供者的凭证和端点：

```json
"models": {
  "providers": {
    "openai": {
      "apiKey": "sk-...",
      "baseUrl": "https://api.openai.com/v1",
      "api": "openai",
      "models": [
        { "id": "gpt-4o", "name": "GPT-4o", "maxTokens": 128000 }
      ]
    },
    "minimax-portal": {
      "baseUrl": "https://api.minimaxi.com/anthropic",
      "api": "anthropic-messages",
      "models": [
        { "id": "MiniMax-M2.7-highspeed", "name": "M2.7 Highspeed", "reasoning": true }
      ]
    }
  }
}
```

`apiKey` 支持多种形式：
- 明文字符串：`"sk-..."`
- 环境变量引用：`{ source: "env", provider: "...", id: "..." }`
- 文件引用：`{ source: "file", path: "/path/to/key" }`

---

## `auth.profiles` — Auth Profiles Configuration

认证配置文件（OAuth / API Key）：

```json
"auth": {
  "profiles": {
    "minimax-portal:default": {
      "provider": "minimax-portal",
      "mode": "oauth"
    },
    "zai:default": {
      "provider": "zai",
      "mode": "api_key"
    }
  },
  "order": ["primary", "secondary"],
  "cooldowns": {
    "failedLoginMs": 30000
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `profiles` | object | Named auth profiles，key 格式 `"provider:profile"` |
| `profiles.*.provider` | string | 提供者名称 |
| `profiles.*.mode` | enum | `"oauth"` \| `"api_key"` \| `"user_token"` |
| `order` | array | 认证顺序（主要用于 OAuth 流程） |
| `cooldowns.failedLoginMs` | integer | 登录失败冷却时间（毫秒） |

---

## `session` — Session Configuration

控制会话行为、持久化和限制：

```json
"session": {
  "store": "memory",
  "dmScope": "per-channel-peer",
  "maxConcurrent": 100
}
```

| Field | Type | Description |
|-------|------|-------------|
| `store` | string | 存储后端：`"memory"` \| `"disk"` |
| `dmScope` | enum | DM 会话作用域：`"per-channel-peer"`（按频道+用户隔离）\| `"global"` |
| `maxConcurrent` | integer | 最大并发会话数 |

**`dmScope` 示例：**
- `"per-channel-peer"`：Telegram 和 Feishu 的同一用户被视为不同会话（推荐）
- `"global"`：跨所有频道的同一用户共享同一会话

---

## `update` — Update Configuration

```json
"update": {
  "channel": "stable",
  "checkOnStart": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `channel` | string | 更新渠道：`"stable"` \| `"beta"` |
| `checkOnStart` | boolean | 启动时检查更新 |

---

## `ui` — UI Configuration

```json
"ui": {
  "assistant": {
    "name": "Jarvis",
    "avatar": "https://example.com/avatar.png",
    "emoji": "🤖"
  },
  "styling": {
    "theme": "auto"
  }
}
```

---

## `logging` — Logging Configuration

```json
"logging": {
  "level": "info",
  "output": "stdout",
  "redaction": {
    "keys": ["password", "apiKey", "token", "secret"]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `level` | enum | `"debug"` \| `"info"` \| `"warn"` \| `"error"` |
| `output` | string | 输出目标：`"stdout"` \| `"file"` |
| `redaction.keys` | array | 日志脱敏关键词 |

---

## `diagnostics` — Diagnostics Configuration

```json
"diagnostics": {
  "otel": {
    "enabled": false,
    "endpoint": "http://localhost:4318"
  },
  "cacheTrace": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `otel.enabled` | boolean | 启用 OpenTelemetry 追踪 |
| `otel.endpoint` | string | OTLP 接收端点 |
| `cacheTrace` | boolean | 缓存追踪 |

---

## `audio` — Audio Configuration

```json
"audio": {
  "transcription": {
    "model": "whisper-1",
    "language": "zh"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `transcription.model` | string | 音频转录模型 |
| `transcription.language` | string | 转录语言（ISO 639-1） |

---

## `media` — Media Configuration

```json
"media": {
  "preserveFilenames": false,
  "pipeline": {
    "concurrency": 4
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `preserveFilenames` | boolean | 保留原始文件名而非生成 UUID |
| `pipeline.concurrency` | integer | 媒体处理并发数 |

---

## `cron` — Cron Configuration

```json
"cron": {
  "store": "memory",
  "concurrency": 5
}
```

| Field | Type | Description |
|-------|------|-------------|
| `store` | string | Cron 任务存储后端 |
| `concurrency` | integer | 最大并发 Cron 任务数 |

---

## `discovery` — Discovery Configuration

```json
"discovery": {
  "mdns": {
    "enabled": true,
    "serviceName": "openclaw"
  },
  "wideArea": {
    "enabled": false
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `mdns.enabled` | boolean | 启用 mDNS 服务发现 |
| `wideArea.enabled` | boolean | 启用广域网发现 |

---

## `messages` — Message Configuration

```json
"messages": {
  "prefixing": {
    "enabled": true
  },
  "ackReactionScope": "group-mentions"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prefixing.enabled` | boolean | 启用消息前缀 |
| `ackReactionScope` | enum | 消息反应通知范围：`"group-mentions"` \| `"all"` \| `"off"` |

---

## `skills` — Skills Loading Configuration

```json
"skills": {
  "load": {
    "extraDirs": ["/path/to/skills"],
    "watch": true,
    "watchDebounceMs": 500
  },
  "install": {
    "preferBrew": false,
    "nodeManager": "npm"
  },
  "entries": {
    "my-skill": {
      "enabled": true,
      "config": { ... }
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `load.extraDirs` | array | 额外技能加载目录 |
| `load.watch` | boolean | 监视技能文件变化 |
| `install.nodeManager` | string | `"npm"` \| `"yarn"` \| `"pnpm"` |
| `entries` | object | per-skill 启用/配置 |

---

## `plugins.entries` — Plugin Configuration

各插件的具体配置：

```json
"plugins": {
  "allow": ["minimax", "telegram", "openclaw-lark"],
  "entries": {
    "minimax": {
      "enabled": true,
      "config": {}
    },
    "feishu": {
      "enabled": false,
      "config": {}
    },
    "telegram": {
      "enabled": true,
      "config": {}
    },
    "openclaw-lark": {
      "enabled": true,
      "config": {}
    }
  }
}
```

**重要：Feishu 插件需要 `plugins.entries.feishu.enabled` 和 `channels.feishu.enabled` 同时为 `true` 且凭证一致才能正常工作。**

---

## `approvals` — Approvals Policy

控制需要审批的 elevated 操作：

```json
"approvals": {
  "exec": {
    "enabled": true,
    "mode": "session",
    "agentFilter": ["agent-id", ...],
    "sessionFilter": ["session-pattern", ...],
    "targets": [
      { "channel": "telegram", "accountId": "123", "threadId": "456" }
    ]
  },
  "plugin": {
    "enabled": true,
    "mode": "session",
    "agentFilter": [...],
    "sessionFilter": [...],
    "targets": [...]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `exec.enabled` | boolean | 启用 exec 审批 |
| `exec.mode` | enum | `"session"` \| `"targets"` \| `"both"` |
| `exec.agentFilter` | array | 仅对这些 agent 触发审批 |
| `exec.sessionFilter` | array | 仅对匹配模式的会话触发审批 |
| `exec.targets` | array | per-target 审批规则 |

---

## Key Changes in 2026.3.x (Migration Notes)

```json
"commands": {
  "prefix": "/",
  "aliases": { ... }
}
```

---

## Key Changes in 2026.3.x (Migration Notes)

| Area | Old (pre-2026.3) | New (2026.3.x) |
|------|-----------------|----------------|
| `agents.defaults` | `model`, `models` only | 40+ fields (workspace, compaction, subagents, sandbox, streaming, etc.) |
| `tools.web.search` | `{ enabled, allowUserUrls, allowedDomains }` | Provider-specific structure with `brave`, `firecrawl`, `gemini`, `grok`, `kimi`, `perplexity` sub-objects |
| `tools.profile` | `"coding"` \| `"full"` \| `"minimal"` | Adds `"messaging"` |
| `tools.exec` | Basic exec config | Adds `host`, `safeBins`, `safeBinProfiles`, `backgroundMs`, `notifyOnExit`, `applyPatch`, etc. |
| `bindings` | Object with route keys | **Array** of route objects |
| `gateway` | Basic fields | New `http`, `push`, `allowRealIpFallback`, `channelHealthCheckMinutes` subsystems |
| `gateway.controlUi` | Basic fields | Adds `dangerouslyAllowHostHeaderOriginFallback` |
| `gateway.reload` | `mode`, `debounceMs` | Adds `deferralTimeoutMs` |
| `gateway.remote` | `url`, `transport`, `token`, `password` | Adds `tlsFingerprint`, `sshTarget`, `sshIdentity` |
| `approvals` | Partial | Full `exec` and `plugin` schema with modes and target rules |
| `hooks` | `enabled`, `path`, `token`, `gmail`, `internal` | Adds `defaultSessionKey`, `allowRequestSessionKey`, `allowedSessionKeyPrefixes`, `allowedAgentIds`, `maxBodyBytes`, `presets`, `transformsDir`, `mappings` |
| `acp` | Not present | New root key with full ACP runtime config |
| `mcp` | Not present | New root key for MCP server configuration |
| `secrets` | Not present | New root key for secrets management |
| `cli` | Not present | New root key for CLI configuration |
| `memory.qmd` | Basic subfields | Expanded with `mcporter`, `limits`, `sessions`, `update`, `scope`, `searchMode`, `includeDefaultMemory` |
