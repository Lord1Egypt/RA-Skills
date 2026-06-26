# OpenClaw CLI-Referenz (Vollständig)

> Stand: März 2026. OpenClaw ändert sich häufig — bei unbekannten Flags `openclaw <command> --help` nutzen.

## Inhaltsverzeichnis
1. [Setup & Onboarding](#setup--onboarding)
2. [Gateway](#gateway)
3. [Doctor & Diagnose](#doctor--diagnose)
4. [Channels](#channels)
5. [Agents (Multi-Agent)](#agents-multi-agent)
6. [Models](#models)
7. [Skills & Plugins](#skills--plugins)
8. [Nodes & Devices](#nodes--devices)
9. [Browser](#browser)
10. [Sandbox](#sandbox)
11. [Cron (Scheduled Jobs)](#cron-scheduled-jobs)
12. [Config](#config)
13. [Secrets](#secrets)
14. [Sessions](#sessions)
15. [Memory](#memory)
16. [Security](#security)
17. [Pairing & Devices](#pairing--devices)
18. [Hooks & Webhooks](#hooks--webhooks)
19. [Update & Versioning](#update--versioning)
20. [Dashboard & TUI](#dashboard--tui)

---

## Setup & Onboarding

### `openclaw setup`

Initialisiert Config + Workspace.

```bash
openclaw setup                              # Workspace erstellen
openclaw setup --workspace <dir>           # Eigenes Workspace-Verzeichnis
openclaw setup --wizard                     # Onboarding-Wizard
openclaw setup --non-interactive            # Headless-Setup
openclaw setup --mode <local|remote>        # Setup-Modus
```

### `openclaw onboard` (empfohlen)

Interaktiver Onboarding-Wizard für Gateway, Workspace und Skills.

```bash
openclaw onboard                            # Vollständiger Wizard
openclaw onboard --install-daemon           # + systemd Service installieren
openclaw onboard --reset                    # Config + Credentials + Sessions zurücksetzen
openclaw onboard --reset-scope full         # Auch Workspace löschen
openclaw onboard --non-interactive          # Headless (alle Flags erforderlich)
openclaw onboard --mode <local|remote>      # Lokal oder Remote-Gateway
openclaw onboard --flow <quickstart|advanced|manual>
openclaw onboard --auth-choice <provider>   # Auth-Provider wählen
# Auth-Options: setup-token|token|chutes|openai-codex|openai-api-key|
#               openrouter-api-key|ollama|ai-gateway-api-key|moonshot-api-key|
#               kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|
#               zai-api-key|mistral-api-key|apiKey|minimax-api|minimax-api-lightning|
#               opencode-zen|opencode-go|custom-api-key|skip
openclaw onboard --gateway-port <port>      # Gateway-Port (default 18789)
openclaw onboard --gateway-bind <bind>      # loopback|lan|tailnet|auto|custom
openclaw onboard --gateway-token <token>    # Gateway-Token setzen
openclaw onboard --tailscale <off|serve|funnel>  # Tailscale-Integration
openclaw onboard --skip-channels            # Channel-Setup überspringen
openclaw onboard --skip-skills              # Skill-Setup überspringen
```

### `openclaw configure`

Interaktiver Konfigurations-Wizard (Modelle, Channels, Skills, Gateway).

### `openclaw config`

Nicht-interaktive Config-Helfer.

```bash
openclaw config get <path>                  # Wert lesen (Dot/Bracket-Notation)
openclaw config set <path> <value>          # Wert setzen (JSON5 oder String)
openclaw config unset <path>                # Wert entfernen
openclaw config file                        # Config-Dateipfad anzeigen
openclaw config validate                    # Config validieren (ohne Gateway-Start)
openclaw config validate --json             # JSON-Ausgabe
```

---

## Gateway

```bash
openclaw gateway                           # Gateway starten (Vordergrund)
openclaw gateway --port 18789               # Port wählen
openclaw gateway --bind <loopback|lan|tailnet|auto|custom>
openclaw gateway --token <token>            # Auth-Token
openclaw gateway --password <password>     # Auth-Passwort
openclaw gateway --tailscale <off|serve|funnel>
openclaw gateway --dev                      # Dev-Modus
openclaw gateway --reset                    # Dev-Config zurücksetzen
openclaw gateway --force                    # Existierenden Listener killen

# Gateway Service (systemd)
openclaw gateway install                    # systemd user service installieren
openclaw gateway uninstall                  # Service entfernen
openclaw gateway start                      # Service starten
openclaw gateway stop                       # Service stoppen
openclaw gateway restart                    # Service neu starten
openclaw gateway status                     # Gateway-Status (probes RPC by default)
openclaw gateway status --no-probe           # Nur Service-Status, kein RPC
openclaw gateway status --deep               # Tiefes System-Scan
openclaw gateway status --json               # JSON-Ausgabe

# Gateway RPC
openclaw gateway health                      # Health-Check
openclaw gateway probe                      # Live-Gateway-Check
openclaw gateway discover                    # Verfügbare Gateways finden
openclaw gateway call <method> [--params '<json>']  # RPC-Methode aufrufen
```

**Wichtige RPC-Methoden:**
```bash
openclaw gateway call config.get --params '{}'
openclaw gateway call config.apply --params '{"raw": "...", "baseHash": "<hash>"}'
openclaw gateway call config.patch --params '{"raw": "...", "baseHash": "<hash>"}'
openclaw gateway call update.run --params '{}'
```

### Logs

```bash
openclaw logs                               # Gateway-Logs (file)
openclaw logs --follow                      # Live-Logs
openclaw logs --limit 200                   # Letzte 200 Zeilen
openclaw logs --json                         # JSON-Ausgabe
openclaw logs --plain                        # Klartext
```

---

## Doctor & Diagnose

```bash
openclaw doctor                             # Vollständiger Gesundheitscheck
openclaw doctor --fix                       # Auto-Fix versuchen
openclaw doctor --yes                       # Headless (keine Prompts)
openclaw doctor --deep                      # System-Level Scan
openclaw doctor --run doctor                # DM-Policy prüfen
openclaw doctor --no-workspace-suggestions  # Workspace-Hints deaktivieren
openclaw status                             # Kompakter Status
openclaw status --deep                      # Channel-Status + Probes
openclaw status --usage                     # Model-Provider Usage/Quota
openclaw health                             # Health vom laufenden Gateway
```

**GOLDENE REGEL**: `openclaw doctor` VOR und NACH jeder Config-Änderung ausführen.

---

## Channels

```bash
openclaw channels list                      # Alle Kanäle + Auth-Profile
openclaw channels status                     # Gateway-Erreichbarkeit + Channel-Health
openclaw channels status --probe             # Live-Channel-Check
openclaw channels logs                       # Channel-Logs
openclaw channels logs --channel whatsapp    # Logs für spezifischen Channel
openclaw channels logs --lines 500          # Letzte 500 Zeilen
openclaw channels add                        # Interaktiver Wizard
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels login                      # WhatsApp QR-Login
openclaw channels login --channel whatsapp --account work
openclaw channels logout --channel whatsapp --account personal
```

**Unterstützte Kanäle (Stand 03/2026):**
WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Google Chat,
Mattermost (Plugin), MS Teams, Matrix, Zalo, Zalo Personal,
BlueBubbles, WebChat, LINE, IRC, Feishu, Nostr

### Channel-Login (WhatsApp)

```bash
openclaw channels login                     # Interaktiver QR-Login
openclaw channels login --channel whatsapp --account work
openclaw channels login --verbose           # Debug-Output
```

---

## Agents (Multi-Agent)

Multi-Agent-Routing für isolierte Workspaces und Sessions.

```bash
openclaw agents list                        # Alle Agenten anzeigen
openclaw agents list --bindings            # Mit Routing-Bindings
openclaw agents add [name]                  # Neuen Agent anlegen
openclaw agents add --workspace <dir>       # Workspace-Pfad
openclaw agents add --model <id>            # Standard-Modell
openclaw agents add --bind <channel[:account]>  # Routing-Binding
openclaw agents add --non-interactive        # Headless
openclaw agents bind --agent <id> --bind <channel[:account]>  # Binding hinzufügen
openclaw agents unbind --agent <id> --bind <channel[:account]>  # Binding entfernen
openclaw agents unbind --agent <id> --all   # Alle Bindings entfernen
openclaw agents delete <id>                 # Agent löschen (Workspace + State)
openclaw agents delete <id> --force         # Ohne Bestätigung
```

**Bindings-Syntax:**
- `whatsapp` → Kanal-Default (Default-Account)
- `whatsapp:personal` → Kanal + Account
- `--bind whatsapp --bind telegram` → Mehrere Kanäle

---

## Models

```bash
openclaw models                             # Alias für models status
openclaw models list                        # Verfügbare Modelle
openclaw models list --all                  # Alle Modelle
openclaw models list --local                # Nur lokale Modelle
openclaw models list --provider <name>      # Nach Provider filtern
openclaw models status                      # Auth-Status + Modelle
openclaw models status --check              # Exit-Code bei expired/missing
openclaw models status --probe              # Live-Provider-Check
openclaw models set <model-id>              # Primary-Modell setzen
openclaw models set-image <model-id>        # Image-Modell setzen

# Aliases
openclaw models aliases list                 # Alle Aliases
openclaw models aliases add <alias> <model>  # Alias hinzufügen
openclaw models aliases remove <alias>      # Alias entfernen

# Fallbacks
openclaw models fallbacks list              # Fallback-Modelle anzeigen
openclaw models fallbacks add <model>        # Fallback hinzufügen
openclaw models fallbacks remove <model>    # Fallback entfernen
openclaw models fallbacks clear             # Alle Fallbacks entfernen

# Image-Fallbacks
openclaw models image-fallbacks list
openclaw models image-fallbacks add <model>
openclaw models image-fallbacks remove <model>
openclaw models image-fallbacks clear

# Scan
openclaw models scan                        # Model-Parameter scannen
openclaw models scan --set-default          # Gefundenes als Default setzen

# Auth
openclaw models auth add                    # Interaktiv API-Key hinzufügen
openclaw models auth setup-token --provider anthropic  # Claude Code OAuth
openclaw models auth paste-token --provider <id> --profile-id <id> --expires-in <duration>
openclaw models auth order get --provider <name>  # Auth-Reihenfolge
openclaw models auth order set --provider <name> <profileIds...>
openclaw models auth order clear --provider <name>
```

**Model-ID-Format:**
```
provider/model-name
```

Beispiele:
```
anthropic/claude-sonnet-4-6
anthropic/claude-opus-4-6
openai-codex/gpt-5.3-codex
openai/gpt-4.1
google/gemini-3-pro-preview
ollama/kimi-k2.5:cloud
openrouter/moonshotai/kimi-k2     # Bei / im Model-Name: Provider-Prefix!
```

---

## Skills & Plugins

```bash
openclaw skills list                        # Verfügbare Skills
openclaw skills info <name>                 # Skill-Details
openclaw skills check                        # Readiness-Check

# ClawHub (Skill-Marktplatz)
clawhub search <query>                      # Skills suchen
clawhub install <name>                      # Skill installieren
clawhub update <name>                        # Skill updaten
clawhub update --all                        # Alle Skills updaten

# Plugins
openclaw plugins list                        # Verfügbare Plugins
openclaw plugins info <id>                   # Plugin-Details
openclaw plugins install <path|.tgz|npm-spec>  # Plugin installieren
openclaw plugins marketplace list <marketplace>  # Marketplace durchsuchen
openclaw plugins enable <id>                # Plugin aktivieren
openclaw plugins disable <id>                # Plugin deaktivieren
openclaw plugins doctor                      # Plugin-Load-Errors
```

**Skill-Verzeichnisse:**
```
~/.openclaw/skills/             # Managed Skills (clawhub install)
~/.openclaw/workspace/skills/   # Workspace Skills (manuell)
```

---

## Nodes & Devices

```bash
# Nodes (verbundene Geräte)
openclaw nodes status                        # Verbundene Nodes
openclaw nodes describe --node <id|name|ip>  # Node-Capabilities
openclaw nodes list --connected              # Nur verbundene
openclaw nodes pending                       # Ausstehende Pairing-Requests
openclaw nodes approve <requestId>           # Node-Pairing genehmigen
openclaw nodes reject <requestId>            # Node-Pairing ablehnen
openclaw nodes rename --node <id> --name <name>  # Node umbenennen
openclaw nodes invoke --node <id> --command <cmd> [--params '<json>']  # RPC aufrufen
openclaw nodes run --node <id> <cmd...>      # Befehl auf Node ausführen

# Node Host (Headless)
openclaw node run --host <gateway-host> --port 18789
openclaw node status
openclaw node install [--host <host>] [--port <port>]
openclaw node uninstall
openclaw node start
openclaw node stop
openclaw node restart

# Devices (Gateway Device Pairing)
openclaw devices list                        # Paired Devices
openclaw devices approve <requestId>         # Device-Pairing genehmigen
openclaw devices approve --latest            # Letzten Request genehmigen
openclaw devices reject <requestId>          # Device ablehnen
openclaw devices remove <deviceId>          # Device entfernen
openclaw devices clear --yes                # Alle Devices entfernen
openclaw devices rotate --device <id> --role <role>  # Token rotieren
openclaw devices revoke --device <id> --role <role>  # Token widerrufen

# Kamera (Node)
openclaw nodes camera list --node <id>
openclaw nodes camera snap --node <id> [--facing front|back|both]
openclaw nodes camera clip --node <id> [--duration 10s]

# Canvas (Node)
openclaw nodes canvas snapshot --node <id>
openclaw nodes canvas present --node <id> [--target <url>]
openclaw nodes canvas hide --node <id>
openclaw nodes canvas navigate <url> --node <id>
openclaw nodes canvas eval [<js>] --node <id>

# Location (Node)
openclaw nodes location get --node <id> [--max-age 60s]
```

---

## Browser

Browser-Steuerung für agentische Workflows.

```bash
openclaw browser status                     # Browser-Status
openclaw browser start                      # Browser starten
openclaw browser stop                       # Browser stoppen
openclaw browser reset-profile             # Profil zurücksetzen
openclaw browser tabs                       # Offene Tabs
openclaw browser open <url>                 # URL öffnen
openclaw browser close [targetId]           # Tab schließen
openclaw browser profiles                   # Profile anzeigen
openclaw browser create-profile --name <name>  # Neues Profil
openclaw browser delete-profile --name <name>  # Profil löschen

# Inspect
openclaw browser screenshot [--full-page]   # Screenshot
openclaw browser snapshot [--format aria|ai]  # Accessibility-Tree
openclaw browser console [--level error|warn|info]  # Console-Logs

# Actions
openclaw browser navigate <url>
openclaw browser resize <width> <height>
openclaw browser click <ref>
openclaw browser type <ref> <text>
openclaw browser press <key>
openclaw browser hover <ref>
openclaw browser drag <startRef> <endRef>
openclaw browser select <ref> <values...>
openclaw browser upload <paths...> [--ref <ref>]
openclaw browser fill [--fields '<json>']
openclaw browser dialog --accept|--dismiss
openclaw browser wait --time <ms>
openclaw browser evaluate --fn '<code>'
openclaw browser pdf                         # PDF generieren
```

---

## Sandbox

```bash
openclaw sandbox list                       # Sandbox-Container anzeigen
openclaw sandbox recreate --agent <id>      # Sandbox neu erstellen
openclaw sandbox explain                    # Sandbox-Konzept erklären
```

**Sandbox-Config:**
```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",     // off | non-main | all
        scope: "agent",       // session | agent | shared
        workspaceAccess: "none",  // none | ro | rw
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          readOnlyRoot: true,
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
        },
      },
    },
  },
}
```

---

## Cron (Scheduled Jobs)

```bash
openclaw cron status                        # Cron-Status
openclaw cron list                          # Alle Jobs
openclaw cron add                           # Job erstellen
openclaw cron add --name <name> --every <duration> --system-event <event>
openclaw cron edit <id>                     # Job bearbeiten
openclaw cron rm <id>                       # Job löschen
openclaw cron enable <id>                   # Job aktivieren
openclaw cron disable <id>                  # Job deaktivieren
openclaw cron runs --id <id> [--limit <n>]  # Job-Runs anzeigen
openclaw cron run <id> [--force]            # Job sofort ausführen
```

**Cron-Config:**
```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000,
    },
  },
}
```

---

## Config

Siehe [Config-Referenz](config-reference.md) für alle Felder.

```bash
openclaw config get <path>                  # Wert lesen
openclaw config set <path> <value>          # Wert setzen
openclaw config unset <path>                # Wert entfernen
openclaw config file                        # Config-Dateipfad
openclaw config validate                    # Config validieren
openclaw config validate --json             # JSON-Ausgabe
```

**Hot-Reload:** Die meisten Config-Änderungen werden automatisch übernommen.
Nur `gateway.*` (Port, Bind, Auth, TLS) benötigen einen Gateway-Restart.

---

## Secrets

SecretRef für Credentials (env/file/exec).

```bash
openclaw secrets reload                     # Secrets neu laden
openclaw secrets audit                      # Auf Plaintext-Residuen scannen
openclaw secrets configure                  # Interaktiver Provider-Setup
openclaw secrets apply --from <plan.json>   # Plan anwenden
```

**SecretRef-Config:**
```json5
{
  secrets: {
    providers: {
      env: { enabled: true },
      file: { enabled: true },
      vault: {
        enabled: true,
        type: "exec",
        command: "vault kv get -format=json",
      },
    },
  },
  models: {
    providers: {
      openai: {
        apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
      },
    },
  },
}
```

---

## Sessions

```bash
openclaw sessions list                      # Sessions anzeigen
openclaw sessions list --active <min>       # Nur aktive Sessions
openclaw sessions list --verbose            # Details
openclaw sessions clean                     # Aufräumen
openclaw sessions cleanup --dry-run          # Zeigen was gelöscht würde
openclaw sessions cleanup --enforce         # Wirklich löschen
```

**Session-Speicherort:** `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

**Session-Config:**
```json5
{
  session: {
    dmScope: "per-channel-peer",  // main | per-peer | per-channel-peer | per-account-channel-peer
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
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    },
  },
}
```

---

## Memory

```bash
openclaw memory status                      # Index-Status
openclaw memory index                       # Neu indexieren
openclaw memory search "<query>"            # Semantische Suche
openclaw memory search --query "<query>"    # Alternative Syntax
```

**Memory-Dateien:**
- `MEMORY.md` — Kuratiertes Langzeit-Gedächtnis (nur private Sessions!)
- `memory/YYYY-MM-DD.md` — Tages-Logs

**Memory-Config:**
```json5
{
  agents: {
    defaults: {
      memorySearch: {
        enabled: true,
        provider: "openai",      // openai | gemini | voyage | mistral | ollama | local
        model: "text-embedding-3-small",
        fallback: "openai",
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            mmr: { enabled: true, lambda: 0.7 },
            temporalDecay: { enabled: true, halfLifeDays: 30 },
          },
        },
      },
    },
  },
}
```

---

## Security

```bash
openclaw security audit                     # Config + State auditieren
openclaw security audit --deep              // + Live-Gateway-Probe
openclaw security audit --fix               // Safe defaults + chmod
```

**Sicherheits-Grundregeln:**
1. `gateway.bind: "loopback"` — Niemals `lan` oder `0.0.0.0` ohne VPN
2. `dmPolicy: "allowlist"` oder `"pairing"` — Niemals `"open"` in Produktion
3. Token ≥ 64 Zeichen — `openclaw gateway --token $(openssl rand -hex 32)`
4. Credentials `chmod 600` — `chmod 600 ~/.openclaw/credentials/*`
5. Skills reviewen — Quellcode prüfen vor Installation
6. Kein root — OpenClaw als eigener User betreiben
7. Workspace privat — Git-Backup in **privates** Repo
8. API-Spending-Limits — Beim Provider setzen
9. Sandbox für Tools — `sandbox.mode: "non-main"` wenn möglich

---

## Pairing & Devices

```bash
openclaw pairing list                       # Ausstehende Pairing-Requests
openclaw pairing list --channel whatsapp    # Nach Channel filtern
openclaw pairing approve <channel> <code>   # Pairing genehmigen
openclaw pairing approve --channel <channel> --account <id> <code> --notify
```

---

## Hooks & Webhooks

```bash
openclaw hooks list                         # Verfügbare Hooks
openclaw hooks info <name>                  # Hook-Details
openclaw hooks check                        # Readiness-Check
openclaw hooks enable <name>                # Hook aktivieren
openclaw hooks disable <name>               # Hook deaktivieren
openclaw hooks install <path|.tgz>          # Hook installieren
openclaw hooks update <name>                # Hook updaten

# Webhooks
openclaw webhooks gmail setup --account <email>  # Gmail Pub/Sub
openclaw webhooks gmail run                 # Gmail-Webhook ausführen
```

**Hooks-Config:**
```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
        deliver: true,
      },
    ],
  },
}
```

---

## Update & Versioning

```bash
openclaw --version                          # Version anzeigen (CalVer: YYYY.M.D-N)

# Update (pnpm empfohlen):
pnpm add -g openclaw@latest && pnpm approve-builds -g && openclaw doctor

# Alternative (npm):
npm install -g openclaw@latest && openclaw doctor

# Docker:
cd openclaw && git pull && bash docker-setup.sh
```

**Release-Channels:**
- `stable` = `npm dist-tag latest` → getaggte Releases
- `beta` = `npm dist-tag beta` → Prereleases

---

## Dashboard & TUI

```bash
openclaw dashboard                          # Browser-UI öffnen (http://127.0.0.1:18789)
openclaw dashboard --no-open               # URL ausgeben ohne Browser
openclaw tui                                # Terminal-UI starten
openclaw tui --session <key>               # Mit Session starten
openclaw tui --url <url> --token <token>    # Remote-Gateway
```

**Dashboard-Bereiche:**
- WebChat — Chat-Interface
- Sessions — Session-Liste + Debug
- Config — Config-Editor
- Health — Health-Monitoring
- Nodes — Verbundene Nodes

---

## System

```bash
openclaw system event --text "<text>"       # System-Event enqueue
openclaw system event --mode <now|next-heartbeat>
openclaw system heartbeat last              # Letzter Heartbeat
openclaw system heartbeat enable            # Heartbeat aktivieren
openclaw system heartbeat disable           # Heartbeat deaktivieren
openclaw system presence                    # Presence-Entries
```

---

## DNS (Discovery)

```bash
openclaw dns setup                         # CoreDNS + Tailscale Setup
openclaw dns setup --apply                  # Config installieren (macOS)
```

---

## Message (Unified Messaging)

```bash
openclaw message send --target <dest> --message "<text>"
openclaw message poll --channel <channel> --target <dest> --poll-question "<q>" --poll-option A --poll-option B
openclaw message react --channel <channel> --target <dest> --emoji "👍"
openclaw message thread create/list/reply
openclaw message emoji list/upload
openclaw message sticker send/upload
openclaw message role info/add/remove
openclaw message channel info/list
openclaw message member info
openclaw message voice status
openclaw message event list/create
```

---

## ACP (Agent Communication Protocol)

```bash
openclaw acp                               # ACP-Bridge für IDE-Integration
openclaw acp --url <url>                   # Remote-Gateway
```

---

## Agent (One-Shot)

```bash
openclaw agent --message "<text>"          # Eine Agent-Turn
openclaw agent --to <dest> --message "<text>"  # Mit Delivery
openclaw agent --channel <channel>         # Channel wählen
openclaw agent --local                      # Lokal (embedded)
openclaw agent --thinking <off|minimal|low|medium|high|xhigh>  # Extended Thinking
openclaw agent --verbose <on|full|off>     # Verbosity
openclaw agent --deliver                    // Antwort zustellen
openclaw agent --json                       // JSON-Ausgabe
```

---

## Reset & Uninstall

```bash
openclaw reset --scope <config|config+creds+sessions|full>
openclaw reset --yes --non-interactive      # Headless

openclaw uninstall --service               # Gateway-Service entfernen
openclaw uninstall --state                  # State löschen
openclaw uninstall --workspace              # Workspace löschen
openclaw uninstall --app                    # App entfernen
openclaw uninstall --all                     # Alles löschen
openclaw uninstall --yes --non-interactive  # Headless
```

---

## Weiterführende Docs

- [Config-Referenz](config-reference.md) — Alle Config-Felder
- [Installation](installation.md) — Setup & Deployment
- [Channels](channels.md) — Kanal-spezifische Config
- [Multi-Agent](multi-agent.md) — Agent-Routing
- [Workspace-Dateien](workspace-files.md) — AGENTS.md, SOUL.md, etc.
- [Memory-System](memory-system.md) — Memory & Vektorsuche
- [Docker-Setup](docker-setup.md) — Containerized Gateway
- [Security-Hardening](security-hardening.md) — Absicherung
- [Troubleshooting](troubleshooting.md) — Fehlerbehebung