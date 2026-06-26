# Installation & Erste Schritte

## Voraussetzungen

- **Node.js 22+** (required) — **Node.js 24 empfohlen** für beste Performance
- macOS, Linux, oder Windows (via WSL2, **dringend empfohlen**)
- 2 GB RAM minimum (4 GB empfohlen)
- 10 GB+ Disk

---

## Methode 1: npm/pnpm (empfohlen für lokale Nutzung)

### Mit pnpm (empfohlen)

```bash
# pnpm aktivieren
corepack enable

# OpenClaw installieren
pnpm add -g openclaw@latest
pnpm approve-builds -g

# Onboarding-Wizard starten
openclaw onboard
```

### Mit npm

```bash
npm install -g openclaw@latest

# Onboarding-Wizard starten
openclaw onboard
```

### Onboarding-Wizard

Der Wizard fragt ab:

1. **Gateway bind-Modus** → `loopback` wählen! (nur lokal)
2. **Auth-Modus** → `token` wählen! (empfohlen)
3. **Gateway-Token** → automatisch generiert oder eigenes
4. **Tailscale?** → Off, es sei denn Tailscale wird verwendet
5. **AI-Provider** → Anthropic/OpenAI/Ollama/etc.
6. **API-Key** → Interaktiv oder via Environment-Variable
7. **Channel-Setup** → WhatsApp/Telegram/Discord etc.
8. **Daemon installieren?** → `--install-daemon` für systemd user service

### Alternative: Direktes Setup ohne Wizard

```bash
# Daemon installieren und starten
openclaw gateway install --install-daemon

# Alternativ: Ohne Daemon
openclaw gateway start
```

### Nach der Installation

```bash
openclaw doctor              # Gesundheitscheck (IMMER!)
openclaw status              # Kurzer Status
openclaw dashboard           # Browser-UI (Port 18789)
```

---

## Methode 2: Docker (empfohlen für VPS/Server)

### Standard-Setup

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
bash docker-setup.sh
```

Das Script:

1. Baut das Docker-Image
2. Startet den Onboarding-Wizard (interaktiv)
3. Konfiguriert Docker Compose
4. Startet den Gateway-Container

### Docker-Compose-Befehle

```bash
# Gateway starten
docker compose up -d openclaw-gateway

# CLI-Befehle ausführen
docker compose run --rm openclaw-cli doctor
docker compose run --rm openclaw-cli channels add --channel telegram --token <TOKEN>
docker compose run --rm openclaw-cli dashboard --no-open

# Logs
docker compose logs -f openclaw-gateway

# Shell im Container
docker compose exec openclaw-gateway bash

# Als root (für Paketinstallation):
docker compose exec -u root openclaw-gateway bash
```

### Alternative Docker-Images

```bash
# Alpine-basiertes Community-Image:
docker pull alpine/openclaw:latest

# Phioranex Community-Image mit install-Script:
curl -fsSL https://raw.githubusercontent.com/phioranex/openclaw-docker/main/install.sh | sudo bash
```

### Docker-Volumes

```
~/.openclaw           → /home/node/.openclaw     (Config, Sessions, Credentials)
~/openclaw/workspace   → /home/node/.openclaw/workspace (Agent-Workspace)
```

### Docker + Ollama (lokale Modelle)

```json5
// In openclaw.json:
models: {
  providers: {
    ollama: {
      // Auf macOS mit Docker Desktop:
      baseUrl: "http://host.docker.internal:11434",
      // Auf Linux:
      baseUrl: "http://172.17.0.1:11434",
    },
  },
}
```

---

## Methode 3: DigitalOcean 1-Click

DigitalOcean bietet ein vorkonfiguriertes Droplet-Image mit:

- OpenClaw vorinstalliert
- Docker-Container-Isolation
- Non-Root-User-Execution
- Hardened Firewall

---

## Methode 4: Docker Sandbox (maximale Isolation)

```bash
docker sandbox create --name my-openclaw shell .
docker sandbox network proxy my-openclaw --allow-host localhost
docker sandbox run my-openclaw
# Im Sandbox:
npm install -g n && n 22
hash -r
npm install -g openclaw@latest
openclaw setup
```

Vorteile: Micro-VM-Isolation, API-Key-Injection über Network-Proxy (Keys nie im Container).

---

## Nach der Installation

### 1. API-Key einrichten

Provider wählen (Anthropic empfohlen für Claude):

```bash
# Environment-Variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Oder in Config
openclaw config set models.providers.anthropic.apiKey "sk-ant-..."
```

### 2. Channel verbinden

Mindestens einen Messaging-Kanal einrichten:

```bash
# Telegram
openclaw channels add --channel telegram --token "123456:ABC..."

# WhatsApp (QR-Code scannen)
openclaw channels login --channel whatsapp

# Discord
openclaw channels add --channel discord --token "YOUR_BOT_TOKEN"
```

### 3. Pairing durchführen

```bash
openclaw pairing list
openclaw pairing approve <channel> <code>
```

### 4. Workspace personalisieren

```bash
cd ~/.openclaw/workspace

# Dateien bearbeiten:
# AGENTS.md  - Betriebsanweisungen
# SOUL.md    - Persönlichkeit
# USER.md    - Nutzerprofil
# MEMORY.md  - Langzeit-Gedächtnis
```

### 5. Security-Check

```bash
openclaw doctor
openclaw security audit --deep
```

### 6. Test-Nachricht senden

Im gewählten Kanal den Bot anschreiben.

---

## Update

### Mit pnpm (empfohlen)

```bash
pnpm add -g openclaw@latest && pnpm approve-builds -g && openclaw doctor
```

### Mit npm

```bash
npm install -g openclaw@latest && openclaw doctor
```

### Mit Docker

```bash
cd openclaw && git pull && bash docker-setup.sh
```

**Nach jedem Update**: `openclaw doctor` ausführen!

---

## systemd Daemon

### Installation

```bash
openclaw gateway install --install-daemon
```

### Verwaltung

```bash
# Status
systemctl --user status openclaw-gateway

# Logs
journalctl --user -u openclaw-gateway -f

# Neustart
systemctl --user restart openclaw-gateway

# Stop
systemctl --user stop openclaw-gateway
```

---

## Gateway-Modi

### local (Standard)

Nur localhost kann zugreifen:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789,
  },
}
```

### remote (Tailscale/VPN)

Extern erreichbar via Tailscale:

```json5
{
  gateway: {
    mode: "remote",
    bind: "tailnet",
    auth: {
      mode: "token",
      token: { source: "env", provider: "default", id: "OPENCLAW_GATEWAY_TOKEN" },
      allowTailscale: true,
    },
    trustedProxies: ["100.64.0.0/10"],
    tailscale: {
      mode: "serve",
      resetOnExit: false,
    },
  },
}
```

---

## Häufige Installationsprobleme

### Node.js Version zu alt

```bash
# Prüfen
node --version  # Muss >= 22 sein

# Mit nvm upgraden
nvm install 24
nvm use 24
```

### pnpm approve-builds vergessen

```bash
pnpm approve-builds -g
```

### Gateway startet nicht

```bash
# Logs prüfen
openclaw gateway log

# Doctor laufen lassen
openclaw doctor --fix
```

### Port bereits belegt

```bash
# Anderen Port verwenden
openclaw config set gateway.port 18889
systemctl --user restart openclaw-gateway
```

### Config-Fehler

```bash
# Config validieren
openclaw config validate

# Config reparieren
openclaw doctor --fix
```

---

## Nächste Schritte

1. **Channel-Dokumentation lesen**: `references/channels.md`
2. **Config verstehen**: `references/config-reference.md`
3. **Workspace einrichten**: `references/workspace-files.md`
4. **Security härten**: `references/security-hardening.md`
5. **Skills nutzen**: `references/skills-guide.md`