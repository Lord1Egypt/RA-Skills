# Security-Hardening — OpenClaw absichern

## Threat Model

OpenClaw hat **volle Kontrolle über den Rechner** — kann Dateien erstellen/löschen,
Software installieren, Skripte ausführen, Internet-Dienste kontaktieren.
Deshalb: Isolation und Least-Privilege sind Pflicht.

---

## Checkliste (Minimum-Sicherheit)

```bash
# 1. Gateway nur lokal binden
openclaw config set gateway.bind loopback

# 2. DM-Policy auf Allowlist
openclaw config set channels.defaults.dmPolicy allowlist
# Eigene User-IDs eintragen!

# 3. Token rotieren (64+ Zeichen)
openclaw token:rotate --force --length 64

# 4. Secrets mit SecretRef (nicht Plaintext!)
openclaw secrets configure
openclaw secrets audit --check

# 5. Credentials schützen
chmod 600 ~/.openclaw/credentials/*

# 6. Doctor prüft Security-Config
openclaw doctor
openclaw doctor --run doctor    # DM-Policy-Check
openclaw security audit --deep  # Tiefes Audit
```

---

## Personal Assistant Security Model

OpenClaw ist für **Personal Assistant** Workloads konzipiert, nicht für Multi-Tenant-SaaS.

**Implikation:**
- Gateway läuft als regulärer User (nicht root)
- Operator-Trust-Boundary: Du vertraust dir selbst
- Keine Tenant-Isolation zwischen verschiedenen WhatsApp/Telegram-Absendern
- Bei Shared-Slack-Workspace: Reale Risk, allen im Channel zu vertrauen

**Best Practice:**
- `dmPolicy: "allowlist"` — Nur deine eigenen Nummern/User-IDs
- `groupPolicy: "allowlist"` — Gruppen mit bekannten Mitgliedern
- Sandbox für Tools aktivieren — Isoliert Tool-Ausführung

---

## DM-Policy (Access Control)

```json5
// Channel-Level Default
channels: {
  defaults: {
    dmPolicy: "allowlist",    // Globaler Default für alle Channels
  },
  whatsapp: {
    dmPolicy: "pairing",      // Override für WhatsApp
    allowFrom: ["+49123456789"],
    groupPolicy: "allowlist",
    groupAllowFrom: ["+49123456789"],
    reject_action: "silent_drop",
    log_rejections: true,
  },
}
```

**DM-Policy-Modi:**

| Modus | Verhalten | Empfehlung |
|---|---|---|
| `pairing` | User muss Code anfordern und genehmigt werden | Ersteinrichtung |
| `allowlist` | Nur `allowFrom`-IDs dürfen schreiben | ✅ Produktion |
| `open` | Jeder darf schreiben (erfordert `allowFrom: ["*"]`) | ❌ Vermeiden |
| `disabled` | Keine DMs erlaubt | Spezifische Use-Cases |

**Active-Surface-Filtering:**
- Deaktivierte Channels/Accounts: SecretRefs blockieren Startup NICHT
- `SECRETS_REF_IGNORED_INACTIVE_SURFACE` — Non-fatal Warning

**Wichtig:** `allowFrom`-IDs sind plattformspezifisch:
- WhatsApp: E.164-String mit `+` (z.B. `"+4915568920209"`)
- Telegram: Numerische User-ID als Zahl (z.B. `7403482253`)

---

## SecretRef — Sichere Credential-Verwaltung

API-Keys **niemals** im Plaintext in Config speichern!

### SecretRef-Contract

```json5
// Basis-Objekt (überall gleich):
{ source: "env" | "file" | "exec", provider: "...", id: "..." }
```

### source: "env" — Environment Variable

```json5
models: {
  providers: {
    openai: {
      apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
    },
  },
}
```

**Validierung:**
- `provider` muss `^[a-z][a-z0-9_-]{0,63}$` matchen
- `id` muss `^[A-Z][A-Z0-9_]{0,127}$` matchen

### source: "file" — JSON-File mit Pointer

```json5
secrets: {
  providers: {
    filemain: {
      source: "file",
      path: "~/.openclaw/secrets.json",
      mode: "json",  // oder "singleValue"
    },
  },
}

models: {
  providers: {
    openai: {
      apiKey: { source: "file", provider: "filemain", id: "/providers/openai/apiKey" },
    },
  },
}
```

**Validierung:**
- `id` muss JSON-Pointer sein (`/...`)
- RFC6901 Escaping: `~` → `~0`, `/` → `~1`

### source: "exec" — External Secret Manager (1Password, Vault, sops)

```json5
secrets: {
  providers: {
    onepassword_openai: {
      source: "exec",
      command: "/opt/homebrew/bin/op",
      allowSymlinkCommand: true,  // Für Homebrew-Shims
      trustedDirs: ["/opt/homebrew"],
      args: ["read", "op://Personal/OpenClaw QA API Key/password"],
      passEnv: ["HOME"],
      jsonOnly: false,
    },
  },
}

models: {
  providers: {
    openai: {
      apiKey: { source: "exec", provider: "onepassword_openai", id: "value" },
    },
  },
}
```

**Exec-Integrationen:**
- **1Password CLI**: `op read op://...`
- **HashiCorp Vault**: `vault kv get -field=KEY secret/openclaw`
- **sops**: `sops -d --extract '["providers"]["openai"]["apiKey"]' secrets.enc.json`

**Request/Response-Protokoll (stdin/stdout JSON):**
```json
// Request:
{ "protocolVersion": 1, "provider": "vault", "ids": ["providers/openai/apiKey"] }

// Response:
{ "protocolVersion": 1, "values": { "providers/openai/apiKey": "sk-..." } }

// Mit Fehlern:
{ "protocolVersion": 1, "values": {}, "errors": { "providers/openai/apiKey": { "message": "not found" } } }
```

### Secrets-CLI

```bash
# Audit (Plaintext-Scan)
openclaw secrets audit --check

# Interaktiver Wizard
openclaw secrets configure

# Nur Provider setup
openclaw secrets configure --providers-only

# Plan anwenden
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json

# Runtime-Refresh
openclaw secrets reload
```

**Sicherheits-Modell:**
- SecretRefs werden beim Gateway-Start eager aufgelöst
- Startup fail-fast wenn Active-Surface SecretRef nicht auflösbar
- Reload nutzt atomic swap: Full success oder last-known-good snapshot
- Keine Rollback-Backups mit Plaintext-Values (one-way safety)

---

## Gateway-Sicherheit

| Setting | Sicher | Gefährlich |
|---|---|---|
| `gateway.bind` | `loopback` | `lan`, `0.0.0.0` |
| `gateway.auth.mode` | `token` | `none` |
| `dmPolicy` | `allowlist` | `open` |
| `tools.exec.host` | `sandbox` | `gateway` |
| `tools.exec.security` | `full` | `relaxed` |

### Remote-Zugriff (wenn nötig)
- **Tailscale** (empfohlen): `gateway.mode: "tailscale"`, `gateway.bind: "tailscale"`
- **SSH-Tunnel**: `ssh -L 18789:127.0.0.1:18789 user@server`
- **NIEMALS** Port 18789 direkt ins Internet exponieren!

### Gateway Auth Surface Diagnostics

Bei SecretRef auf `gateway.auth.token`, `gateway.auth.password`, `gateway.remote.token`, oder `gateway.remote.password` loggt Gateway den Surface-State:

- `active`: SecretRef ist Teil des effektiven Auth-Surface (muss auflösen)
- `inactive`: SecretRef wird ignoriert (anderer Auth-Surface gewinnt)

Code: `SECRETS_GATEWAY_AUTH_SURFACE`

---

## Skill-Sicherheit

Skills sind die größte Angriffsfläche. OpenClaw lädt Skills aus drei Orten:

| Ort | Präzedenz | Sichtbarkeit |
|---|---|---|
| `<workspace>/skills` | Höchste | Nur dieser Agent |
| `~/.openclaw/skills` | Mitte | Alle Agents auf dieser Maschine |
| Bundled Skills | Niedrigste | Mitgeliefert |

**ClawHub-Sicherheit:**
- 5700+ Skills verfügbar — nicht alle sicher
- "Hide Suspicious" auf ClawHub aktivieren
- VirusTotal-Report auf ClawHub-Seite prüfen
- Quellcode reviewen vor Installation

### Skill-Gating (Load-Time Filter)

Skills können Requirements definieren:

```json5
---
name: gemini
description: Use Gemini CLI for coding assistance
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"], "env": ["GEMINI_API_KEY"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

**Gating-Fields:**
- `requires.bins` — Binary muss auf PATH existieren
- `requires.env` — Env-Var muss existieren ODER in Config gesetzt sein
- `requires.config` — `openclaw.json`-Pfad muss truthy sein
- `primaryEnv` — Env-Var für `skills.entries.<name>.apiKey`

**Wichtig bei Sandbox:**
- `requires.bins` wird auf dem HOST geprüft (Load-Time)
- In Sandbox muss Binary zusätzlich IM CONTAINER existieren
- Installiere via `agents.defaults.sandbox.docker.setupCommand`

### Config-Overrides

```json5
skills: {
  entries: {
    "my-skill": {
      enabled: true,
      apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
      env: { MY_VAR: "value" },
      config: { endpoint: "https://example.com" },
    },
  },
}
```

**Regeln:**
- `enabled: false` deaktiviert Skill (auch bundled)
- `env` wird nur injiziert wenn Var nicht bereits gesetzt
- `apiKey` kann Plaintext-String ODER SecretRef sein
- `allowBundled`: Allowlist für bundled Skills (managed/workspace Skills nicht betroffen)

---

## Sandbox-Konfiguration

Sandboxing isoliert Tool-Ausführung in Docker-Container.

### Was wird sandboxed?
- Tool-Execution (`exec`, `read`, `write`, `edit`, `apply_patch`, `process`)
- Optional: Sandbox-Browser (`agents.defaults.sandbox.browser.enabled`)

**Nicht sandboxed:**
- Gateway-Prozess selbst
- `tools.elevated` (läuft auf dem Host, bypasses Sandbox)

### Sandbox-Modes

| Mode | Verhalten |
|---|---|
| `off` | Kein Sandboxing |
| `non-main` | Nur nicht-main Sessions (Default für Normal-Chat auf Host) |
| `all` | Alle Sessions in Sandbox |

**Wichtig:** `non-main` basiert auf `session.mainKey` (default `"main"`), nicht Agent-ID. Gruppen/Channel-Sessions haben eigene Keys → werden sandboxed.

### Sandbox-Scope

| Scope | Container-Anzahl |
|---|---|
| `session` | Ein Container pro Session (Default) |
| `agent` | Ein Container pro Agent |
| `shared` | Ein Container für alle (keine Isolation!) |

### Sandbox-Backend

| Backend | Beschreibung |
|---|---|
| `docker` | Lokale Docker-Container (Default) |
| `ssh` | SSH-Remote-Server |
| `openshell` | OpenShell-Remote-Workspace |

### Workspace-Access

| Mode | Zugriff |
|---|---|
| `none` | Sandbox-Workspace unter `~/.openclaw/sandboxes` (Default) |
| `ro` | Agent-Workspace read-only unter `/agent` |
| `rw` | Agent-Workspace read/write unter `/workspace` |

### Sandbox-Config-Beispiel

```json5
agents: {
  defaults: {
    sandbox: {
      mode: "non-main",
      scope: "agent",
      workspaceAccess: "none",
      docker: {
        image: "openclaw-sandbox:bookworm-slim",
        network: "none",            // Kein Netzwerk (sicherste Option)
        readOnlyRoot: true,
        tmpfs: ["/tmp", "/var/tmp", "/run"],
        user: "1000:1000",
        capDrop: ["ALL"],
        pidsLimit: 256,
        memory: "1g",
        memorySwap: "2g",
        cpus: 1,
        setupCommand: "apt-get update && apt-get install -y git curl jq",
        // setupCommand braucht network != "none" + user: "0:0" für apt-get
      },
      prune: {
        idleHours: 24,     // Container >24h idle löschen
        maxAgeDays: 7,      // Container >7 Tage löschen
      },
    },
  },
}
```

### Sandbox-Images bauen

```bash
# Standard-Image
scripts/sandbox-setup.sh  # baut openclaw-sandbox:bookworm-slim

# Mit mehr Tooling (curl, jq, node, python, git)
scripts/sandbox-common-setup.sh  # baut openclaw-sandbox-common:bookworm-slim

# Browser-Image
scripts/sandbox-browser-setup.sh  # baut openclaw-sandbox-browser:bookworm-slim
```

### Tool-Policy (Allow/Deny)

```json5
tools: {
  sandbox: {
    tools: {
      allow: ["exec", "process", "read", "write", "edit", "sessions_list", "sessions_history"],
      deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
    },
  },
}
```

- `deny` gewinnt über `allow`
- Leeres `allow` = alle Tools (minus deny)
- Nicht-leeres `allow` = nur gelistete Tools (minus deny)

### SSH-Backend

```json5
agents: {
  defaults: {
    sandbox: {
      mode: "all",
      backend: "ssh",
      workspaceAccess: "rw",
      ssh: {
        target: "user@gateway-host:22",
        workspaceRoot: "/tmp/openclaw-sandboxes",
        identityFile: "~/.ssh/id_ed25519",
        // ODER SecretRefs:
        identityData: { source: "env", provider: "default", id: "SSH_IDENTITY" },
        certificateData: { source: "env", provider: "default", id: "SSH_CERTIFICATE" },
        knownHostsData: { source: "env", provider: "default", id: "SSH_KNOWN_HOSTS" },
      },
    },
  },
}
```

### Sandbox-Troubleshooting

| Problem | Ursache | Lösung |
|---|---|---|
| Image nicht gefunden | Nicht gebaut | `scripts/sandbox-setup.sh` |
| Container läuft nicht | Wird on-demand erstellt | Warten oder `openclaw sandbox list` |
| Permission denied in Sandbox | UID/GID mismatch | `docker.user` setzen oder Workspace chown |
| Tools nicht gefunden | PATH nicht in Sandbox | `docker.env.PATH` setzen |
| apt-get failed | Kein Netzwerk | `docker.network: "bridge"` + `readOnlyRoot: false` |

---

## API-Key-Management

```bash
# Keys NIE in Workspace-Dateien speichern!
# Keys NIE in öffentliche Repos pushen!

# Secrets-Check:
grep -r "sk-" ~/.openclaw/
grep -r "ANTHROPIC_API_KEY" ~/.openclaw/workspace/
# → Sollte nichts finden

# API-Spending-Limits beim Provider setzen!
# Heartbeat alle 30min kann $0.50-2.00/Tag kosten
```

---

## Betriebssystem-Härtung

```bash
# Eigenen User für OpenClaw anlegen
sudo adduser --system --home /home/openclaw openclaw

# Firewall (ufw)
sudo ufw default deny incoming
sudo ufw allow ssh
# Port 18789 NICHT freigeben (nur loopback!)

# Nicht als root betreiben!
# ssh openclaw@server, dann openclaw-Befehle
```

---

## Empfohlene Architektur für VPS

```
VPS (Contabo/Hetzner/DO)
├── Docker-Container: openclaw-gateway
│   ├── Non-root user (node)
│   ├── Gateway bind: loopback
│   └── Sandbox für Tools
├── ufw: nur SSH erlaubt
├── Tailscale: für Remote-Dashboard-Zugriff
└── Separater User: kein Zugriff auf Prod-Daten
```

---

## Verwandte Docs

- **Quick-Ref**: `references/quick-reference.md` — Security-Checkliste
- **Config**: `references/config-reference.md` — secrets.*, agents.* Schema
- **Docker**: `references/docker-setup.md` — Sandbox-Container Setup
- **Multi-Agent**: `references/multi-agent.md` — Per-Agent Sandbox & Tools
- **CLI**: `references/cli-reference.md` — `openclaw secrets`, `openclaw token:rotate`
