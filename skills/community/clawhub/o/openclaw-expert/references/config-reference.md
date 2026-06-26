# Config-Referenz — openclaw.json vollständig

## Datei & Format

- Pfad: `~/.openclaw/openclaw.json`
- Format: **JSON5** (Kommentare `//`, trailing commas erlaubt)
- Hot-Reload: Gateway beobachtet die Datei und wendet Änderungen automatisch an
  - Ausnahme: `gateway.reload` und `gateway.remote` triggern KEINEN Restart
- Validierung: `openclaw config validate`

### $include — Config aufteilen

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  channels: { $include: "./channels.json5" },
  broadcast: {
    $include: ["./clients/a.json5", "./clients/b.json5"],
  },
}
```

Regeln:
- **Einzelne Datei**: ersetzt das enthaltende Objekt
- **Array von Dateien**: deep-merge in Reihenfolge (spätere gewinnen)
- **Sibling-Keys**: werden nach includes gemergt (überschreiben included values)
- **Nested includes**: bis zu 10 Ebenen tief unterstützt
- **Relative Pfade**: relativ zur einbindenden Datei aufgelöst
- **Fehlerbehandlung**: klare Fehler bei fehlenden Dateien, Parse-Fehlern und Zyklen

---

## Alle Top-Level Sections

```
meta / wizard / update / agents / models / tools / messages /
commands / session / hooks / cron / channels / canvasHost / gateway / skills / plugins / secrets / bindings / env
```

---

## meta

Automatisch verwaltet — nicht manuell editieren.

```json5
{
  meta: {
    lastTouchedVersion: "2026.3.17",
    lastTouchedAt: "2026-03-17T10:30:00.000Z",
  },
}
```

---

## wizard

Tracking des Setup-Wizards — nicht manuell editieren.

```json5
{
  wizard: {
    lastRunAt: "...",
    lastRunVersion: "2026.3.17",
    lastRunCommand: "configure",    // "setup" | "configure" | "onboard"
    lastRunMode: "local",           // "local" | "remote"
  },
}
```

---

## update

```json5
{
  update: {
    channel: "stable",    // "stable" | "beta" | "nightly"
    auto: { enabled: true },
  },
}
```

`beta` für neue Features, `stable` für Produktion.

---

## agents — Agent-Konfiguration

### agents.defaults

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-6",
        fallbacks: ["openai/gpt-5.2"],
      },

      // Modelle mit Aliases (für /model <alias>)
      models: {
        "anthropic/claude-sonnet-4-6": { alias: "Sonnet" },
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "openai/gpt-5.2": { alias: "GPT" },
        "google/gemini-3-pro-preview": { alias: "gemini" },
      },

      workspace: "~/.openclaw/workspace",
      skipBootstrap: false,

      // Context-Pruning: alte Tool-Ergebnisse entfernen
      contextPruning: {
        mode: "cache-ttl",
        ttl: "1h",
      },

      // Compaction
      compaction: {
        mode: "safeguard",    // "safeguard" | "aggressive" | "manual"
      },

      timeoutSeconds: 1800,
      heartbeat: { every: "1h" },
      maxConcurrent: 4,
      subagents: { maxConcurrent: 8 },

      // Group-Chat-Mention-Patterns
      groupChat: {
        mentionPatterns: ["@bot", "bot"],
      },

      // Sandbox (per-agent)
      sandbox: {
        mode: "off",         // "off" | "non-main" | "all"
        scope: "session",    // "session" | "agent" | "shared"
        workspaceAccess: "rw",  // "rw" | "ro" | "none"
        docker: {
          image: "openclaw-sandbox:latest",
          setupCommand: "apt-get update && apt-get install -y git curl",
        },
        ssh: {
          target: "user@gateway-host:22",
          identityData: { source: "env", provider: "default", id: "SSH_IDENTITY" },
          certificateData: { source: "env", provider: "default", id: "SSH_CERTIFICATE" },
          knownHostsData: { source: "env", provider: "default", id: "SSH_KNOWN_HOSTS" },
        },
      },

      // Per-Agent Tools
      tools: {
        allow: ["read", "sessions_list"],
        deny: ["exec", "write", "edit", "apply_patch", "browser"],
      },

      // Bootstrap-Limits
      bootstrapMaxChars: 20000,
      bootstrapTotalMaxChars: 150000,
    },
  },
}
```

### agents.list — Multi-Agent-Routing

```json5
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
        model: { primary: "anthropic/claude-sonnet-4-6" },
        groupChat: { mentionPatterns: ["@home", "Home"] },
        sandbox: { mode: "off" },
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
        model: { primary: "anthropic/claude-opus-4-6" },
        sandbox: { mode: "all", scope: "agent" },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit"],
        },
      },
    ],
  },
}
```

### Compaction-Modi

| Modus | Verhalten | Kosten |
|---|---|---|
| `safeguard` | Auto bei ~80% Context-Limit | Moderat |
| `aggressive` | Häufiger compacten | Spart Tokens |
| `manual` | Nur mit `/compact` | Volle Kontrolle |

### Sandbox-Modi

| Modus | Verhalten |
|---|---|
| `off` | Kein Sandbox (Standard) |
| `non-main` | Nur Nicht-Main-Sessions |
| `all` | Alle Sessions |

### Sandbox-Scopes

| Scope | Container-Isolation |
|---|---|
| `session` | Ein Container pro Session |
| `agent` | Ein Container pro Agent |
| `shared` | Gemeinsamer Container |

---

## models — LLM-Provider & Modelle

```json5
{
  models: {
    mode: "merge",    // "merge" = mit Defaults zusammenführen | "replace" = nur eigene
    providers: {
      "anthropic": {
        baseUrl: "https://api.anthropic.com",
        api: "anthropic-messages",
        models: [
          {
            id: "claude-sonnet-4-6",
            name: "Claude Sonnet 4.6",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 3, output: 15, cacheRead: 0.3, cacheWrite: 3.75 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
      "openai": {
        baseUrl: "https://api.openai.com/v1",
        api: "openai-completions",
        models: [
          { id: "gpt-5.2", name: "GPT-5.2", reasoning: true },
          { id: "gpt-5.2-codex", name: "GPT-5.2 Codex", reasoning: false },
        ],
      },
      "ollama": {
        baseUrl: "http://localhost:11434/v1",
        api: "openai-completions",
        models: [
          { id: "kimi-k2.5:cloud", name: "Kimi K2.5 (Cloud)", reasoning: true },
          { id: "deepseek-v3.2:cloud", name: "DeepSeek V3.2 (Cloud)", reasoning: true },
        ],
      },
    },
  },
}
```

### API-Typen

| api | Für |
|---|---|
| `anthropic-messages` | Anthropic (Claude) |
| `openai-completions` | OpenAI-kompatibel (DeepSeek, Mistral, NVIDIA, Ollama, Moonshot) |
| `google-generative-ai` | Google (Gemini, Antigravity) |
| `deepgram` | Audio: Nova-3 |

### Trick: Gleiche baseUrl, verschiedene API-Keys

```json5
"nvidia":          { baseUrl: "https://integrate.api.nvidia.com/v1", models: [...] },
"nvidia-deepseek": { baseUrl: "https://integrate.api.nvidia.com/v1", models: [...] },
"nvidia-qwen":     { baseUrl: "https://integrate.api.nvidia.com/v1", models: [...] },
```

### Trick: Ollama Cloud-Modelle

```json5
"ollama": {
  baseUrl: "http://localhost:11434/v1",
  models: [
    { id: "kimi-k2.5:cloud", name: "Kimi K2.5 (Cloud)", reasoning: true, contextWindow: 262144 },
    { id: "deepseek-v3.2:cloud", name: "DeepSeek V3.2 (Cloud)", reasoning: true },
    { id: "qwen3-vl:235b-instruct-cloud", input: ["text", "image"] },
  ],
}
```

---

## channels — Messaging-Kanäle

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "allowlist",       // "pairing" | "allowlist" | "open" | "disabled"
      selfChatMode: true,
      allowFrom: ["+4915568920209"],
      groupPolicy: "allowlist",
      groups: {
        "*": { requireMention: true },
        "120363xxx@g.us": { allow: true, requireMention: false },
      },
      debounceMs: 0,
      mediaMaxMb: 50,
      accounts: {
        personal: { authDir: "~/.openclaw/credentials/whatsapp/personal" },
        biz: { authDir: "~/.openclaw/credentials/whatsapp/biz" },
      },
      defaultAccount: "personal",
      healthMonitor: { enabled: true },
    },

    telegram: {
      enabled: true,
      dmPolicy: "pairing",
      accounts: {
        default: {
          botToken: "123456:ABC...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:7403482253"],
          groupPolicy: "allowlist",
          streaming: "partial",
          mediaMaxMb: 50,
        },
        alerts: {
          botToken: "987654:XYZ...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:123456789"],
        },
      },
    },

    discord: {
      enabled: true,
      accounts: {
        default: {
          token: "DISCORD_BOT_TOKEN_MAIN",
          guilds: {
            "123456789012345678": {
              channels: {
                "222222222222222222": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },

    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      dmPolicy: "allowlist",
      allowFrom: ["slack:U12345"],
    },

    signal: {
      enabled: true,
      account: "+15551234567",
    },
  },
}
```

### dmPolicy

| Wert | Bedeutung | Produktion? |
|---|---|---|
| `pairing` | One-Time-Pairing-Code | ✅ Empfohlen |
| `allowlist` | Nur `allowFrom` | ✅ Sicher |
| `open` | Jeder | ⚠️ Nur Tests |
| `disabled` | Keine DMs | Gruppen-only |

**ACHTUNG**: WhatsApp dmPolicy gilt **GLOBAL** für den Account!

### Multi-Account-Routing

```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Routing-Priorität (Bindings)

Bindings sind **deterministisch** und **spezifischste gewinnt**:

1. `peer` match (exakte DM/Group/Channel-ID)
2. `parentPeer` match (Thread-Vererbung)
3. `guildId + roles` (Discord Role Routing)
4. `guildId` (Discord)
5. `teamId` (Slack)
6. `accountId` match für einen Channel
7. Channel-Level match (`accountId: "*"`)
8. Fallback auf Default-Agent (`agents.list[].default`, sonst erster Eintrag, sonst `main`)

---

## gateway

```json5
{
  gateway: {
    port: 18789,
    mode: "local",           // "local" | "remote"
    bind: "loopback",        // "loopback" | "lan" | "tailnet" | "custom"
    reload: {
      mode: "hybrid",        // "hybrid" | "hot" | "restart" | "off"
      debounceMs: 300,
    },
    controlUi: {
      enabled: true,
      allowedOrigins: ["https://hostname.taildcb944.ts.net"],
    },
    auth: {
      mode: "token",
      token: { source: "env", provider: "default", id: "OPENCLAW_GATEWAY_TOKEN" },
      allowTailscale: true,
    },
    trustedProxies: ["100.64.0.0/10"],  // Tailscale CGNAT
    tailscale: {
      mode: "serve",         // "off" | "serve" | "funnel"
      resetOnExit: false,
    },
    channelHealthCheckMinutes: 5,
    channelStaleEventThresholdMinutes: 30,
    channelMaxRestartsPerHour: 10,
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
          timeoutMs: 10000,
        },
      },
    },
  },
}
```

### Reload-Modi

| Modus | Verhalten |
|---|---|
| `hybrid` | Hot-Applie für sichere Änderungen, Auto-Restart für kritische |
| `hot` | Nur Hot-Applie, loggt Warnung wenn Restart nötig |
| `restart` | Immer Restart bei Config-Änderung |
| `off` | Kein File-Watching, manuell Restart |

### Hot-Applie vs Restart

| Kategorie | Hot-Applie? |
|---|---|
| Channels (`channels.*`) | ✅ Ja |
| Agents & Models (`agent`, `agents`, `models`) | ✅ Ja |
| Automation (`hooks`, `cron`, `heartbeat`) | ✅ Ja |
| Sessions & Messages (`session`, `messages`) | ✅ Ja |
| Tools & Media (`tools`, `browser`, `skills`, `audio`) | ✅ Ja |
| UI & Misc (`ui`, `logging`, `identity`, `bindings`) | ✅ Ja |
| Gateway Server (`gateway.*`) | ❌ Restart |
| Infrastructure (`discovery`, `canvasHost`, `plugins`) | ❌ Restart |

---

## session — Session-Management

```json5
{
  session: {
    dmScope: "per-channel-peer",  // "main" | "per-peer" | "per-channel-peer" | "per-account-channel-peer"
    mainKey: "main",

    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },

    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },

    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },

    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },

    resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
    },

    resetTriggers: ["/new", "/reset"],

    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
      ],
      default: "allow",
    },

    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
      rotateBytes: "10mb",
      maxDiskBytes: "1gb",
      highWaterBytes: "800mb",
      resetArchiveRetention: "14d",
    },

    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
  },
}
```

### dmScope-Optionen

| Wert | Session-Key | Empfohlen für |
|---|---|---|
| `main` | `agent:<id>:<mainKey>` | Single-User |
| `per-peer` | `agent:<id>:direct:<peerId>` | Multi-Device |
| `per-channel-peer` | `agent:<id>:<channel>:direct:<peerId>` | Multi-User Inboxes |
| `per-account-channel-peer` | `agent:<id>:<channel>:<account>:direct:<peerId>` | Multi-Account |

### Maintenance-Modi

| Modus | Verhalten |
|---|---|
| `warn` | Reportet nur, mutiert nicht |
| `enforce` | Wendet Cleanup an |

---

## tools

```json5
{
  tools: {
    web: {
      search: {
        enabled: false,
        provider: "brave",   // "brave" | "tavily"
        apiKey: { source: "env", provider: "default", id: "BRAVE_API_KEY" },
      },
      fetch: { enabled: true },
    },
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        providerOptions: {
          deepgram: { detect_language: true, punctuate: true, smart_format: true },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
    sessions: { visibility: "all" },
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

---

## messages — TTS & Reaktionen

```json5
{
  messages: {
    tts: {
      provider: "edge",
      edge: { enabled: true, voice: "de-DE-ConradNeural", lang: "de-DE" },
    },
    ackReactionScope: "group-mentions",  // "all" | "group-mentions" | "none"
  },
}
```

Deutsche Edge-TTS-Stimmen: `de-DE-ConradNeural` (m), `de-DE-KatjaNeural` (w).

---

## commands / hooks / cron

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    restart: true,
    ownerDisplay: "raw",
  },

  hooks: {
    enabled: true,
    token: { source: "env", provider: "default", id: "HOOKS_TOKEN" },
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
  },

  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000,
    },
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    },
  },
}
```

---

## secrets — Secrets Management

```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        args: ["--profile", "prod"],
        passEnv: ["PATH", "VAULT_ADDR"],
        jsonOnly: true,
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
  },
}
```

### SecretRef-Contract

```json5
// Env-Variable
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }

// File (JSON-Pointer)
{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }

// Exec (externer Resolver)
{ source: "exec", provider: "vault", id: "providers/openai/apiKey" }
```

### Verwendungsbeispiele

```json5
{
  models: {
    providers: {
      openai: {
        apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
      },
    },
  },
  channels: {
    googlechat: {
      serviceAccountRef: {
        source: "exec",
        provider: "vault",
        id: "channels/googlechat/serviceAccount",
      },
    },
  },
}
```

---

## bindings — Multi-Agent-Routing

```json5
{
  bindings: [
    // WhatsApp Personal → Home Agent
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },

    // WhatsApp Business → Work Agent
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Spezifischer DM zu Opus
    {
      agentId: "opus",
      match: {
        channel: "whatsapp",
        peer: { kind: "direct", id: "+15551234567" },
      },
    },

    // Spezifische Gruppe zu Family Agent
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363xxx@g.us" },
      },
    },

    // Discord Guild + Role Routing
    {
      agentId: "mod",
      match: {
        channel: "discord",
        guildId: "123456789",
        roles: ["admin", "moderator"],
      },
    },
  ],
}
```

---

## env — Environment Variables

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
    shellEnv: { enabled: true, timeoutMs: 15000 },
  },
}
```

### Env-Var-Substitution

```json5
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: {
    providers: {
      custom: { apiKey: "${CUSTOM_API_KEY}" },
    },
  },
}
```

Regeln:
- Nur Großbuchstaben: `[A-Z_][A-Z0-9_]*`
- Fehlende/leere Variablen → Fehler
- Escape mit `$${VAR}` für literale Ausgabe
- Funktioniert in `$include`-Dateien

---

## Häufige Config-Fehler

| Fehler | Symptom | Fix |
|---|---|---|
| `allowFrom` als String statt Array | Channel startet nicht | `["+49..."]` (Array!) |
| Telegram allowFrom als String | Keine Nachrichten | `[7403482253]` (Zahl!) |
| WhatsApp ohne Ländercode | Keine Nachrichten | `"+4915568920209"` (E.164) |
| `bind: "lan"` ohne Auth | Gateway-Start verweigert | Auth setzen |
| Doppelte Modell-IDs | Unvorhersehbar | Jede ID nur 1x |
| `trustedProxies` fehlt | allowTailscale ignoriert | `["100.64.0.0/10"]` |
| `allowedOrigins` fehlt | CORS im Dashboard | Tailscale-Domain eintragen |
| Provider ≠ auth.profiles Key | Auth fehlschlag | Namen abgleichen |
| `dmScope: "main"` mit Multi-User | Session-Lecks | `"per-channel-peer"` |

---

## Validierung

```bash
openclaw config validate       # Syntax + Struktur prüfen
openclaw config get <pfad>     # Einzelnen Wert lesen
openclaw config set <pfad> <wert>  # Wert setzen
openclaw config edit           # Im Editor öffnen
openclaw doctor                # Gesundheitscheck nach Änderung
```

---

## Config Hot-Reload

Gateway beobachtet `~/.openclaw/openclaw.json`:

- **Hot-Applie**: Channels, Models, Agents, Tools, Hooks, Cron, Session
- **Restart-Bedingung**: Gateway-Server, Infrastructure

Änderungen triggern automatisch (je nach `gateway.reload.mode`).

---

## Workspace-Dateien

| Datei | Zweck | Geladen |
|---|---|---|
| `AGENTS.md` | Betriebsanweisungen | Jede Session |
| `SOUL.md` | Persönlichkeit, Ton | Jede Session |
| `USER.md` | Nutzerprofil | Jede Session |
| `TOOLS.md` | Tool-Hinweise | Jede Session |
| `IDENTITY.md` | Name, Emoji, Vibe | Bootstrap |
| `HEARTBEAT.md` | Scheduled-Tasks / Cron-Checkliste | Heartbeat |
| `MEMORY.md` | Langzeit-Gedächtnis | Nur private Sessions |
| `BOOT.md` | Startup-Checkliste | Gateway-Restart |
| `BOOTSTRAP.md` | Einmal-Setup | Nur einmal |
| `memory/YYYY-MM-DD.md` | Tages-Logs | Session-Start |

---

## Per-Agent Sandbox & Tools

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
        // Keine Tool-Beschränkungen
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent" },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "apply_patch"],
        },
      },
    ],
  },
}
```

**Hinweis**: `tools.elevated` ist **global** und sender-basiert, nicht per-Agent konfigurierbar.