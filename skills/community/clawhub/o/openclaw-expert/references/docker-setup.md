# Docker-Deployment — Containerized Gateway

## Wann Docker?

| Szenario | Docker? | Begründung |
|---|---|---|
| VPS/Server (24/7) | ✅ Ja | Isolation, Reproduzierbarkeit |
| macOS lokal | ❌ Nein | VM-Overhead, npm direkt schneller |
| Sandbox für Tools | ✅ Ja | Gateway lokal, Tools in Container |
| Erstmalig testen | ✅ Ja | Sicher, leicht entfernbar |

**Wichtig:** Docker ist optional. Für lokale Entwicklung ist `pnpm add -g openclaw@latest` schneller.

---

## Quick Start (Empfohlen)

```bash
# Im Repo-Root:
./docker-setup.sh
```

### Was das Script macht:

1. **Image bauen** (oder pull wenn `OPENCLAW_IMAGE` gesetzt)
2. **Onboarding** starten (interaktiv)
3. **Config schreiben** mit `gateway.bind: lan`
4. **Gateway starten** via Docker Compose
5. **Token generieren** und in `.env` schreiben

### Nach Abschluss:

- Dashboard öffnen: `http://127.0.0.1:18789/`
- Token in Settings einfügen
- URL erneut holen: `docker compose run --rm openclaw-cli dashboard --no-open`

---

## Environment-Variablen

| Variable | Beschreibung |
|---|---|
| `OPENCLAW_IMAGE` | Remote-Image statt lokalem Build (z.B. `ghcr.io/openclaw/openclaw:latest`) |
| `OPENCLAW_DOCKER_APT_PACKAGES` | Extra apt-Pakete während Build |
| `OPENCLAW_EXTENSIONS` | Extensions vorinstallieren (`diagnostics-otel matrix`) |
| `OPENCLAW_EXTRA_MOUNTS` | Zusätzliche Bind-Mounts |
| `OPENCLAW_HOME_VOLUME` | Named Volume für `/home/node` |
| `OPENCLAW_SANDBOX` | Sandbox-Bootstrap aktivieren (`1`, `true`, `yes`, `on`) |
| `OPENCLAW_INSTALL_DOCKER_CLI` | Docker CLI im Image installieren |
| `OPENCLAW_DOCKER_SOCKET` | Docker-Socket-Pfad override |
| `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` | Private `ws://` für CLI erlauben |
| `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS` | Chromium-Flags deaktivieren |
| `OPENCLAW_BROWSER_DISABLE_EXTENSIONS` | Extensions aktiviert lassen |
| `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT` | Chromium Renderer-Limit |

---

## Containerized Gateway (Docker Compose)

### compose.yml (Default)

```yaml
services:
  openclaw-gateway:
    image: openclaw:local
    restart: unless-stopped
    ports:
      - "18789:18789"
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ~/openclaw/workspace:/home/node/.openclaw/workspace
    # Optional: User-Mapping
    # user: "1000:1000"

  openclaw-cli:
    image: openclaw:local
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ~/openclaw/workspace:/home/node/.openclaw/workspace
    profiles: ["cli"]
    entrypoint: ["openclaw"]
```

### CLI via Docker Compose

```bash
docker compose run --rm openclaw-cli doctor
docker compose run --rm openclaw-cli channels add --channel telegram --token <TOKEN>
docker compose run --rm openclaw-cli dashboard --no-open
```

---

## Remote Image (ohne lokalen Build)

Offizielle Images: **GitHub Container Registry**

```bash
# Tags:
# - ghcr.io/openclaw/openclaw:main       (latest main branch)
# - ghcr.io/openclaw/openclaw:2026.2.26   (Release-Tag)
# - ghcr.io/openclaw/openclaw:latest      (latest stable)

export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./docker-setup.sh
```

Das Script pullt statt zu bauen wenn `OPENCLAW_IMAGE` gesetzt ist.

---

## Base Image Metadata

Default-Image: `node:24-bookworm`

OCI Annotations:
- `org.opencontainers.image.base.name=docker.io/library/node:24-bookworm`
- `org.opencontainers.image.source=https://github.com/openclaw/openclaw`
- `org.opencontainers.image.url=https://openclaw.ai`
- `org.opencontainers.image.documentation=https://docs.openclaw.ai/install/docker`

---

## Agent Sandbox (Docker Gateway + Containerized Tools)

### Enable Sandbox

```bash
export OPENCLAW_SANDBOX=1
./docker-setup.sh
```

Custom Socket (rootless Docker):
```bash
export OPENCLAW_SANDBOX=1
export OPENCLAW_DOCKER_SOCKET=/run/user/1000/docker.sock
./docker-setup.sh
```

**Hinweise:**
- `docker.sock` wird erst nach Sandbox-Prerequisites gemountet
- Bei Fehlern wird `agents.defaults.sandbox.mode` auf `off` zurückgesetzt
- `Dockerfile.sandbox` muss existieren (oder `scripts/sandbox-setup.sh` laufen)

### Sandbox-Config

```json5
agents: {
  defaults: {
    sandbox: {
      mode: "non-main",       // "off" | "non-main" | "all"
      scope: "agent",         // "session" | "agent" | "shared"
      workspaceAccess: "none", // "none" | "ro" | "rw"
      docker: {
        image: "openclaw-sandbox:bookworm-slim",
        network: "none",      // Kein Netzwerk (sicherste)
        readOnlyRoot: true,
        tmpfs: ["/tmp", "/var/tmp", "/run"],
        user: "1000:1000",
        capDrop: ["ALL"],
        setupCommand: "apt-get update && apt-get install -y git curl jq",
      },
      prune: {
        idleHours: 24,
        maxAgeDays: 7,
      },
    },
  },
}
```

**Setup-Command-Hinweise:**
- Default: `network: "none"` → apt-get schlägt fehl
- Für Pakete: `network: "bridge"` + `readOnlyRoot: false` + `user: "0:0"`
- Container wird bei `setupCommand`-Änderung neu erstellt (~5min Cooldown)

### Sandbox-Images bauen

```bash
# Standard-Sandbox
scripts/sandbox-setup.sh          # openclaw-sandbox:bookworm-slim

# Mit Tooling (node, go, python, curl, jq)
scripts/sandbox-common-setup.sh    # openclaw-sandbox-common:bookworm-slim

# Browser-Sandbox (Chromium + noVNC)
scripts/sandbox-browser-setup.sh   # openclaw-sandbox-browser:bookworm-slim
```

### Sandbox-Backend-Optionen

| Backend | Beschreibung |
|---|---|
| `docker` | Lokale Docker-Container (Default) |
| `ssh` | SSH-Remote-Server |
| `openshell` | OpenShell-Remote-Workspace |

### Tool-Policy in Sandbox

```json5
tools: {
  sandbox: {
    tools: {
      allow: ["exec", "process", "read", "write", "edit", "sessions_list"],
      deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
    },
  },
}
```

- `deny` gewinnt über `allow`
- Leeres `allow` = alle Tools (minus deny)

---

## Power-User Container

Default-Image ist **security-first** (non-root `node`, kein Chromium, kein sudo).

### Vollständiger Container

```bash
# 1. /home/node persistieren
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh

# 2. System-Packages backen
export OPENCLAW_DOCKER_APT_PACKAGES="git curl jq"
./docker-setup.sh

# 3. Playwright ohne npx
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

---

## Extra Mounts

```bash
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

**Hinweise:**
- Pfade müssen in Docker Desktop (macOS/Windows) geteilt sein
- Format: `source:target[:options]`
- Bei Änderungen: `docker-setup.sh` neu laufen lassen

---

## Permissions-Probleme

Image läuft als `node` (UID 1000).

```bash
# Option 1 (empfohlen): Ownership auf UID 1000
sudo chown -R 1000:$(id -g) ~/.openclaw
sudo chmod -R u+rwX,g+rwX,o-rwx ~/.openclaw

# Option 2: Gruppe beschreibbar
chmod -R 775 ~/.openclaw

# Option 3 (LETZTER AUSWEG): World-writable
chmod -R 777 ~/.openclaw
```

---

## Channel Setup

```bash
# WhatsApp (QR)
docker compose run --rm openclaw-cli channels login

# Telegram (Bot Token)
docker compose run --rm openclaw-cli channels add --channel telegram --token "<TOKEN>"

# Discord (Bot Token)
docker compose run --rm openclaw-cli channels add --channel discord --token "<TOKEN>"
```

---

## Health Checks

```bash
# Container-Probes (kein Auth nötig)
curl -fsS http://127.0.0.1:18789/healthz
curl -fsS http://127.0.0.1:18789/readyz

# Deep Health (Gateway + Channels)
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

---

## LAN vs Loopback

`docker-setup.sh` defaultet `OPENCLAW_GATEWAY_BIND=lan` für Docker.

| Bind | Zugriff |
|---|---|
| `lan` | Host-Browser + Host-CLI erreichen Gateway |
| `loopback` | Nur Prozesse im Container-Namespace |

Bei Pairing-Problemen:
```bash
docker compose run --rm openclaw-cli config set gateway.mode local
docker compose run --rm openclaw-cli config set gateway.bind lan
docker compose run --rm openclaw-cli devices list --url ws://127.0.0.1:18789
```

---

## Automation/CI

Non-Interactive mit `-T`:

```bash
docker compose run -T --rm openclaw-cli gateway probe
docker compose run -T --rm openclaw-cli devices list --json
```

---

## Docker + Ollama

```json5
models: {
  providers: {
    ollama: {
      // macOS Docker Desktop:
      baseUrl: "http://host.docker.internal:11434",
      // Linux (Docker-Bridge-IP):
      // baseUrl: "http://172.17.0.1:11434",
      apiKey: "ollama-local",
      api: "openai-completions",
    },
  },
}
```

---

## Shell Helpers (Optional)

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/shell-helpers/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh

# In ~/.zshrc:
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc

# Commands:
clawdock-start
clawdock-stop
clawdock-dashboard
clawdock-help
```

---

## Storage Model

| Pfad | Persistenz |
|---|---|
| `~/.openclaw/` | Host-Bind-Mount (überlebt Container) |
| `~/.openclaw/workspace/` | Host-Bind-Mount |
| Sandbox `/tmp`, `/var/tmp`, `/run` | `tmpfs` (ephemeral) |
| `/home/node` (optional) | Named Volume wenn `OPENCLAW_HOME_VOLUME` |

---

## Troubleshooting

| Problem | Lösung |
|---|---|
| Build OOM (exit 137) | Mindestens 2 GB RAM |
| Workspace nicht sichtbar | Volume-Mount in `docker-compose.yml` prüfen |
| "Cannot connect to Docker daemon" | `sudo systemctl start docker` |
| Slow auf macOS | VM-Overhead → npm direkt nutzen |
| Permission denied | Ownership/Permissions oben prüfen |
| Container startet nicht nach Config-Änderung | `docker compose run --rm openclaw-cli doctor` |
| QR nicht angezeigt | Dashboard → Channels nutzen |
| "Connection closed" nach Scan | Gateway restart → erneut scannen |
| Sandbox Image fehlt | `scripts/sandbox-setup.sh` |

---

## Security Notes

- Gateway läuft als `node` User (non-root)
- Kein Chromium/Playwright im Default-Image
- Kein sudo
- Sandbox-Default: `network: "none"` (kein Internet für Tools)
- `network: "host"` ist blockiert
- `network: "container:<id>"` ist blockiert (break-glass: `dangerouslyAllowContainerNamespaceJoin`)

---

## Verwandte Docs

- **Quick-Ref**: `references/quick-reference.md` — Docker Quick-Start
- **Security**: `references/security-hardening.md` — Sandbox-Konfiguration Details
- **Installation**: `references/installation.md` — npm/pnpm Setup
- **Config**: `references/config-reference.md` — Sandbox-Config Schema