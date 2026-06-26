# Multi-Agent-Routing

## Konzept

OpenClaw kann mehrere isolierte Agenten in einem Gateway hosten. Jeder Agent hat:
- **Eigenen Workspace** (Dateien, AGENTS.md, SOUL.md, USER.md, Memory)
- **Eigenes agentDir** (Auth-Profile, Model-Registry)
- **Eigene Sessions** (`~/.openclaw/agents/<agentId>/sessions/`)

Auth-Profile sind **per-Agent**. Credentials werden nicht automatisch geteilt.

---

## Single-Agent-Modus (Default)

Wenn keine Multi-Agent-Konfiguration vorhanden ist:

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
    },
  },
}
```

- `agentId` defaultet zu **`main`**
- Sessions keyed als `agent:main:<mainKey>`
- State: `~/.openclaw/agents/main/agent`

---

## Multi-Agent-Setup

### Mit Wizard

```bash
openclaw agents add work
openclaw agents add personal
```

Der Wizard erstellt:
- Workspace-Verzeichnis (`~/.openclaw/workspace-<id>`)
- `agentDir` (`~/.openclaw/agents/<id>/agent`)
- Session-Store (`~/.openclaw/agents/<id>/sessions`)

### Manuell in openclaw.json

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
        model: "anthropic/claude-sonnet-4-5",
        sandbox: {
          mode: "off",
        },
        tools: {
          allow: ["exec", "read", "write"],
          deny: [],
        },
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
        model: "anthropic/claude-opus-4-6",
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "browser"],
        },
        groupChat: {
          mentionPatterns: ["@work", "@workbot"],
        },
      },
    ],
  },
}
```

---

## Bindings (Routing-Regeln)

Bindings bestimmen, welcher Agent welche Nachrichten empfängt. **Most-specific-wins**:

1. `peer` Match (exakte DM/Group/Channel-ID)
2. `parentPeer` Match (Thread-Inheritance)
3. `guildId + roles` (Discord Role-Routing)
4. `guildId` (Discord Server)
5. `teamId` (Slack Team)
6. `accountId` Match für Channel
7. Channel-level (`accountId: "*"`)
8. Default Agent (`agents.list[].default`, oder erster Eintrag, oder `main`)

### Binding-Beispiele

```json5
bindings: [
  // Specifischer DM zu Opus-Agent
  {
    agentId: "opus",
    match: {
      channel: "whatsapp",
      peer: { kind: "direct", id: "+15551234567" },
    },
  },

  // Kanal-weiter Fallback für WhatsApp
  {
    agentId: "home",
    match: { channel: "whatsapp" },
  },

  // Account-spezifisch
  {
    agentId: "work",
    match: { channel: "whatsapp", accountId: "biz" },
  },

  // Channel-weit (accountId: "*")
  {
    agentId: "chat",
    match: { channel: "telegram", accountId: "*" },
  },

  // Discord-Group mit Mention-Pattern
  {
    agentId: "family",
    match: {
      channel: "discord",
      peer: { kind: "group", id: "120363999999999999" },
    },
  },
],
```

### Account-Scoping

- Binding ohne `accountId` → matcht nur Default-Account
- `accountId: "*"` → matcht alle Accounts auf dem Channel
- Duplicate Bindings werden automatisch auf Account-Scoping umgestellt

---

## Per-Agent Sandbox & Tools

Jeder Agent kann eigene Sandbox- und Tool-Einstellungen haben:

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
        // Keine Tool-Einschränkungen
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          docker: {
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "apply_patch", "browser", "nodes", "cron"],
        },
        groupChat: {
          mentionPatterns: ["@family", "@familybot"],
        },
      },
    ],
  },
}
```

**Hinweis**: `setupCommand` läuft unter `sandbox.docker.*`. Per-Agent Docker-Overrides werden ignoriert, wenn der Scope `"shared"` ist.

---

## Session-DmScope

Isolations-Level für Direct Messages:

| dmScope | Beschreibung | Use-Case |
|---------|--------------|----------|
| `main` | Alle DMs teilen eine Session | Single-User |
| `per-channel-peer` | DMs pro Channel+Sender isoliert | Multi-User |
| `per-account-channel-peer` | DMs pro Account+Channel+Sender | Multi-Account |

```json5
session: {
  dmScope: "per-channel-peer",
  threadBindings: "auto",  // "auto" | "manual"
}
```

---

## CLI-Befehle

```bash
# Agent-Liste
openclaw agents list
openclaw agents list --bindings

# Neuen Agent erstellen
openclaw agents add <id>

# Binding hinzufügen
openclaw agents bind <agentId> "channel:telegram:accountId:alerts"

# Binding entfernen
openclaw agents unbind <agentId> "channel:telegram:accountId:alerts"
```

---

## Pfade

| Pfad | Beschreibung |
|------|--------------|
| `~/.openclaw/openclaw.json` | Haupt-Config |
| `~/.openclaw/workspace-<id>/` | Agent-Workspace |
| `~/.openclaw/agents/<id>/agent/` | Auth-Profile, Model-Registry |
| `~/.openclaw/agents/<id>/sessions/` | Session-Logs (*.jsonl) |

---

## Platform-Beispiele

### Discord-Bots per Agent

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
  channels: {
    discord: {
      groupPolicy: "allowlist",
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
        coding: {
          token: "DISCORD_BOT_TOKEN_CODING",
          guilds: {
            "123456789012345678": {
              channels: {
                "333333333333333333": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },
  },
}
```

### WhatsApp-Nummern per Agent

```bash
# Accounts verlinken
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
```

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

---

## Best Practices

1. **Isolierte Workspaces**: Jeder Agent bekommt eigenen Workspace-Ordner
2. **dmScope: `per-channel-peer`**: Für Multi-User-Setups
3. **Sandbox pro Agent**: Verschiedene Trust-Level mit `sandbox.mode`
4. **Binding-Reihenfolge**: Spezifischere Regeln zuerst
5. **Account-Trennung**: Ein WhatsApp-Account kann mehrere Agenten via `bindings` routen
6. **Niemals agentDir teilen**: Verursacht Auth/Session-Kollisionen
7. **Credentials kopieren**: Bei Bedarf `auth-profiles.json` manuell kopieren

---

## Agent-to-Agent Messaging

Agenten können sich gegenseitig Nachrichten senden (opt-in):

```json5
tools: {
  agentToAgent: {
    enabled: true,
    allow: ["home", "work"],  // Whitelist der Agenten
  },
}
```

**Standardmäßig deaktiviert.** Wenn aktiviert, können Agenten via `agentToAgent` Tool kommunizieren.

---

## Identity & Name

Jeder Agent kann eigene Identitäts-Informationen haben:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "Family Bot"],
        },
      },
    ],
  },
}
```

---

## Workspace-Isolation

**Wichtig:** Der Workspace ist das Default-Arbeitsverzeichnis, aber KEINE harte Sandbox.

- Relative Pfade → innerhalb Workspace
- Absolute Pfade → können andere Host-Verzeichnisse erreichen
- Für echte Isolation: `sandbox.mode` aktivieren

---

## Referenz

- Docs: https://docs.openclaw.ai/concepts/multi-agent
- **Config-Referenz**: `references/config-reference.md` — agents.list Schema
- **Security**: `references/security-hardening.md` — Per-Agent Sandbox & Tools
- **Docker**: `references/docker-setup.md` — Sandbox-Container Setup
- **CLI**: `references/cli-reference.md` — `openclaw agents` Befehle
- **Quick-Ref**: `references/quick-reference.md` — Multi-Agent Quick-Setup