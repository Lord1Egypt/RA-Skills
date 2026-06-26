# Quick Reference — Schnellnachschlage

> Einseitige Referenz für häufige Konfigurationen und Befehle.

---

## Verzeichnisstruktur

```
~/.openclaw/
├── openclaw.json          # Haupt-Config (JSON5)
├── credentials/           # API-Keys (chmod 600!)
├── agents/<id>/sessions/  # Session-Logs
├── skills/                # Managed-Skills
└── workspace/             # Agent-Workspace
    ├── AGENTS.md          # Betriebsanweisungen
    ├── SOUL.md            # Persönlichkeit
    ├── USER.md            # Nutzerprofil
    ├── MEMORY.md          # Langzeit-Gedächtnis
    └── memory/            # Tagesnotizen
```

---

## Minimal-Config

```json5
{
  gateway: { bind: "loopback", auth: { mode: "token", token: "<64+ chars>" } },
  channels: { telegram: { enabled: true, botToken: "..." } },
  models: { default: "anthropic/claude-sonnet-4-20250514" },
}
```

---

## Security-Checkliste

| Setting | Wert | Befehl |
|---------|------|--------|
| Gateway-Bind | `loopback` | `openclaw config set gateway.bind loopback` |
| DM-Policy | `allowlist` | `openclaw config set channels.defaults.dmPolicy allowlist` |
| Token | 64+ chars | `openclaw token:rotate --force --length 64` |
| Secrets | SecretRef | `openclaw secrets configure` |
| Credentials | chmod 600 | `chmod 600 ~/.openclaw/credentials/*` |

---

## DM-Policy Modi

| Modus | Verhalten | Use-Case |
|-------|-----------|----------|
| `pairing` | Code anfordern + genehmigen | Ersteinrichtung |
| `allowlist` | Nur allowFrom-IDs | ✅ Produktion |
| `open` | Jeder darf (gefährlich!) | ❌ Vermeiden |
| `disabled` | Keine DMs | Spezifisch |

---

## Channel-Quick-Setup

### Telegram
```bash
@BotFather → /newbot → Token kopieren
openclaw channels add --channel telegram --token "<TOKEN>"
# User-ID finden: @userinfobot anschreiben
```

### WhatsApp
```bash
openclaw channels login --channel whatsapp
# QR im Dashboard scannen
# Pairing: openclaw pairing approve whatsapp <CODE>
```

### Discord
```bash
# Discord Dev Portal → Bot → Token + Message Content Intent!
openclaw channels add --channel discord --token "<TOKEN>"
```

---

## Models hinzufügen

```json5
models: {
  default: "anthropic/claude-sonnet-4-20250514",
  heartbeat: "anthropic/claude-haiku-3-20250307",  // Günstig für Heartbeat
  providers: {
    openai: { apiKey: { source: "env", id: "OPENAI_API_KEY" } },
    ollama: { baseUrl: "http://localhost:11434", api: "openai-completions" },
  },
}
```

---

## Sandbox-Quick-Config

```json5
agents: {
  defaults: {
    sandbox: {
      mode: "non-main",      // "off" | "non-main" | "all"
      scope: "agent",         // "session" | "agent" | "shared"
      workspaceAccess: "ro",  // "none" | "ro" | "rw"
      docker: {
        image: "openclaw-sandbox:bookworm-slim",
        network: "none",      // Sicherste Option
      },
    },
  },
}
```

---

## Multi-Agent Quick-Setup

```json5
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
```

```bash
openclaw agents add work
openclaw agents bind work "whatsapp:biz"
```

---

## Memory mit Semantic Search

```json5
agents: {
  defaults: {
    memorySearch: {
      enabled: true,
      provider: "openai",
      model: "text-embedding-3-small",
      query: {
        hybrid: { enabled: true },
        mmr: { enabled: true, lambda: 0.7 },
        temporalDecay: { enabled: true, halfLifeDays: 30 },
      },
    },
    compaction: {
      memoryFlush: { enabled: true },
    },
  },
}
```

---

## Docker Quick-Start

```bash
# Mit Sandbox
export OPENCLAW_SANDBOX=1
./docker-setup.sh

# Ohne Sandbox
./docker-setup.sh

# Remote Image
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./docker-setup.sh
```

---

## Tailscale Modi

| Modus | Zugriff | Auth |
|-------|---------|------|
| `serve` | Tailnet-only | Token oder Tailscale-Identity |
| `funnel` | Öffentlich (VORSICHT!) | Password PFLICHT |
| `tailnet` bind | Tailnet-IP, kein HTTPS | Token |

```json5
gateway: {
  bind: "loopback",
  tailscale: { mode: "serve" },
  auth: { mode: "token", token: "...", allowTailscale: true },
}
```

---

## SecretRef Formate

```json5
// Environment Variable
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }

// JSON-File
{ source: "file", provider: "filemain", id: "/providers/openai/apiKey" }

// External (1Password, Vault, sops)
{ source: "exec", provider: "onepassword", id: "value" }
```

---

## CLI-Einzeiler

```bash
# Status
openclaw doctor && openclaw status

# Gateway
openclaw gateway restart

# Config validieren
openclaw config validate

# Channels testen
openclaw channels status --probe

# Skills neu laden
openclaw skills reload

# Pairing
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>

# Token rotieren
openclaw token:rotate --force --length 64

# Logs
openclaw logs --follow --channel telegram

# Session-Status
openclaw sessions list
```

---

## Troubleshooting-Patterns

| Problem | Erster Schritt |
|---------|----------------|
| Gateway startet nicht | `openclaw doctor` |
| Config-Fehler | JSON5-Syntax prüfen (trailing commas OK) |
| Channel verbindet nicht | `openclaw channels status --probe` |
| Token nicht erkannt | Environment-Variable gesetzt? |
| Sandbox-Container fehlt | `scripts/sandbox-setup.sh` |
| Permissions in Docker | `sudo chown -R 1000:$(id -g) ~/.openclaw` |
| QR-Code abgelaufen | `openclaw channels login` erneut |
| Node verbindet nicht | `tailscale status` auf beiden Seiten |

---

## Kosten sparen

```json5
agent: {
  heartbeat: { every: "6h" },  // Statt 30m → 90% weniger
},
models: {
  default: "anthropic/claude-sonnet-4-20250514",
  heartbeat: "anthropic/claude-haiku-3-20250307",
},
```

---

## Referenz-Links

| Thema | Datei |
|-------|-------|
| Installation | `references/installation.md` |
| Config-Details | `references/config-reference.md` |
| Channels | `references/channels.md` |
| Security | `references/security-hardening.md` |
| Docker | `references/docker-setup.md` |
| Multi-Agent | `references/multi-agent.md` |
| Skills | `references/skills-guide.md` |
| Memory | `references/memory-system.md` |
| CLI-Befehle | `references/cli-reference.md` |