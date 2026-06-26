# OpenClaw Installation & Setup Reference

## Table of Contents
- [Getting Started](#getting-started)
- [Updating](#updating)
- [Docker](#docker)
- [Nix](#nix)
- [Raspberry Pi](#raspberry-pi)
- [Uninstall](#uninstall)
- [Onboarding (CLI Wizard)](#onboarding-cli-wizard)
- [VPS / Linux Server Deployment](#vps--linux-server-deployment)
- [Migration Guide](#migration-guide)
- [Platform Notes](#platform-notes)
- [Control UI (Custom Build)](#control-ui-custom-build)

## Getting Started

### Requirements

- **Node.js** — Node 24 recommended (Node 22.14+ also supported)
- **API key** from a model provider (Anthropic, OpenAI, Google, etc.)

Check Node version: `node --version`

### Quick Setup

**macOS / Linux:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Run onboarding:**
```bash
openclaw onboard --install-daemon
```

**Verify install:**
```bash
openclaw --version      # confirm the CLI is available
openclaw doctor         # check for config issues
openclaw gateway status # verify the Gateway is running
```

**Open dashboard:**
```bash
openclaw dashboard
```

### Alternative Install Methods

**Local prefix installer (`install-cli.sh`)** — keeps OpenClaw and Node under `~/.openclaw` without a system-wide Node install:
```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

**Install from GitHub main branch:**
```bash
npm install -g github:openclaw/openclaw#main
```

**pnpm** — requires explicit build approval after first install:
```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g   # required: pnpm requires explicit approval for packages with build scripts
openclaw onboard --install-daemon
```

**From source:**
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm build && pnpm ui:build
pnpm link --global
openclaw onboard --install-daemon
```

**Troubleshooting sharp build errors (npm):** If `sharp` fails due to a globally installed libvips:
```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

---

## Updating

### Recommended: `openclaw update`

```bash
openclaw update
```

The fastest way to update. Detects your install type (npm or git), fetches the latest version, runs `openclaw doctor`, and restarts the gateway.

**Switch channels or target a specific version:**
```bash
openclaw update --channel beta
openclaw update --tag main
openclaw update --dry-run   # preview without applying
```

`--channel beta` prefers beta but falls back to stable/latest when the beta tag is missing or older. Use `--tag beta` if you want the raw npm beta dist-tag for a one-off package update.

### Alternative: Re-run the installer

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Add `--no-onboard` to skip onboarding. For source installs: `--install-method git --no-onboard`.

### Alternative: Manual npm/pnpm/bun

```bash
npm i -g openclaw@latest
pnpm add -g openclaw@latest  # also run: pnpm approve-builds -g
bun add -g openclaw@latest   # Bun is supported for CLI; for the Gateway runtime, Node is recommended
```

Tip: `npm view openclaw version` shows the current published version.

### Root-Owned Global npm Installs

Some Linux npm setups install global packages under root-owned directories. OpenClaw supports that layout: the installed package is treated as read-only at runtime, and bundled plugin runtime dependencies are staged into a writable runtime directory.

For hardened systemd units:
```ini
Environment=OPENCLAW_PLUGIN_STAGE_DIR=/var/lib/openclaw/plugin-runtime-deps
ReadWritePaths=/var/lib/openclaw /home/openclaw/.openclaw /tmp
```

If `OPENCLAW_PLUGIN_STAGE_DIR` is not set, OpenClaw uses `$STATE_DIRECTORY` when systemd provides it, then falls back to `~/.openclaw/plugin-runtime-deps`.

### Auto-Updater

Off by default. Enable in `~/.openclaw/openclaw.json`:

```json5
{
  update: {
    channel: "stable",
    checkOnStart: false,  // set false to disable startup update hint
    auto: {
      enabled: true,
      stableDelayHours: 6,
      stableJitterHours: 12,
      betaCheckIntervalHours: 1,
    },
  },
}
```

**Bundled plugin runtime dependencies**: Packaged installs keep bundled plugin runtime dependencies out of the read-only package tree. On startup and during `openclaw doctor --fix`, OpenClaw repairs runtime dependencies only for bundled plugins that are active in config, active through legacy channel config, or enabled by their bundled manifest default. Explicit disablement wins — a disabled plugin or channel does not get its runtime dependencies repaired just because it exists in the package. External plugins and custom load paths still use `openclaw plugins install` or `openclaw plugins update`. The `OPENCLAW_PLUGIN_STAGE_DIR` env var controls where staged deps land.

OpenClaw treats packaged global installs as read-only at runtime, even when writable by the current user. This keeps `openclaw update` from racing with a running gateway or local agent repairing plugin dependencies during the same install.

| Channel | Behavior |
|---|---|
| `stable` | Waits `stableDelayHours`, then applies with deterministic jitter |
| `beta` | Checks every `betaCheckIntervalHours` (default: hourly) and applies immediately |
| `dev` | No automatic apply. Use `openclaw update` manually |

### After Updating

```bash
# Run doctor (migrates config, audits DM policies, checks gateway health)
openclaw doctor

# Restart the gateway
openclaw gateway restart

# Verify
openclaw health
```

### Rollback

**Pin a version (npm):**
```bash
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

**Pin a commit (source):**
```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
pnpm install && pnpm build
openclaw gateway restart
```

---

## Docker

Docker is **optional**. Use it only if you want a containerized gateway or to validate the Docker flow.

**Is Docker right for me?**
- **Yes**: you want an isolated, throwaway gateway environment or to run OpenClaw on a host without local installs
- **No**: you are running on your own machine and just want the fastest dev loop
- **Note**: the default sandbox backend uses Docker when sandboxing is enabled, but sandboxing is off by default and does **not** require the full gateway to run in Docker. SSH and OpenShell sandbox backends are also available. See [Sandboxing](/gateway/sandboxing).
- If running on a VPS/public host, review [Security hardening for network exposure](/gateway/security), especially Docker `DOCKER-USER` firewall policy

### Prerequisites

- Docker Desktop (or Docker Engine) + Docker Compose v2
- At least 2 GB RAM for image build (`pnpm install` may be OOM-killed on 1 GB hosts)
- Enough disk for images and logs

### Containerized Gateway Setup

```bash
# Step 1: Build the image
./scripts/docker/setup.sh

# Or use a pre-built image
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh
```

Pre-built image tags: `main`, `latest`, `<version>` (e.g. `2026.2.26`)

During setup, onboarding runs automatically (prompts for API keys, generates gateway token, starts gateway via Docker Compose).

**Open the Control UI:**
```bash
docker compose run --rm openclaw-cli dashboard --no-open
```

**Configure channels:**
```bash
# WhatsApp (QR)
docker compose run --rm openclaw-cli channels login

# Telegram
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"

# Discord
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

### Manual Docker Flow

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js onboard --mode local --no-install-daemon
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set --batch-json '[{"path":"gateway.mode","value":"local"},{"path":"gateway.bind","value":"lan"},{"path":"gateway.controlUi.allowedOrigins","value":["http://localhost:18789","http://127.0.0.1:18789"]}]'
docker compose up -d openclaw-gateway
```

### Environment Variables

| Variable | Purpose |
|---|---|
| `OPENCLAW_IMAGE` | Use a remote image instead of building locally |
| `OPENCLAW_DOCKER_APT_PACKAGES` | Install extra apt packages during build (space-separated) |
| `OPENCLAW_EXTENSIONS` | Pre-install plugin deps at build time (space-separated names) |
| `OPENCLAW_EXTRA_MOUNTS` | Extra host bind mounts (comma-separated `source:target[:opts]`) |
| `OPENCLAW_HOME_VOLUME` | Persist `/home/node` in a named Docker volume |
| `OPENCLAW_SANDBOX` | Opt in to sandbox bootstrap (`1`, `true`, `yes`, `on`) |
| `OPENCLAW_DOCKER_SOCKET` | Override Docker socket path |

### Health Checks

```bash
# Container probe endpoints (no auth required)
curl -fsS http://127.0.0.1:18789/healthz   # liveness
curl -fsS http://127.0.0.1:18789/readyz     # readiness

# Authenticated deep health snapshot
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

The Docker image includes a built-in `HEALTHCHECK` that pings `/healthz`. If checks keep failing, Docker marks the container as `unhealthy` and orchestration systems can restart or replace it.

**Shared-network security note**: `openclaw-cli` uses `network_mode: "service:openclaw-gateway"` so CLI commands can reach the gateway over `127.0.0.1`. Treat this as a shared trust boundary. The compose config drops `NET_RAW`/`NET_ADMIN` and enables `no-new-privileges` on `openclaw-cli`.

Note: `openclaw-cli` is a post-start tool (it shares the gateway's network namespace). Before `docker compose up -d openclaw-gateway`, run onboarding and setup-time config writes through `openclaw-gateway` with `--no-deps --entrypoint node`.

### LAN vs Loopback

`scripts/docker/setup.sh` defaults `OPENCLAW_GATEWAY_BIND=lan`.

- `lan` (default): host browser and host CLI can reach the published gateway port
- `loopback`: only processes inside the container network namespace can reach the gateway directly

Use bind mode values: `lan` / `loopback` / `custom` / `tailnet` / `auto` — NOT host aliases like `0.0.0.0` or `127.0.0.1`.

### Storage and Persistence

Docker Compose bind-mounts:
- `OPENCLAW_CONFIG_DIR` → `/home/node/.openclaw`
- `OPENCLAW_WORKSPACE_DIR` → `/home/node/.openclaw/workspace`

**Disk growth hotspots:** watch `media/`, session JSONL files, `cron/runs/*.jsonl`, and rolling file logs under `/tmp/openclaw/`.

### Shell Helpers (ClawDock)

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

Use `clawdock-start`, `clawdock-stop`, `clawdock-dashboard`, etc. Run `clawdock-help` for all commands.

### Agent Sandbox

When `agents.defaults.sandbox` is enabled with the Docker backend:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared
      },
    },
  },
}
```

Build the default sandbox image:
```bash
scripts/sandbox-setup.sh
```

### Docker Troubleshooting

- **Image missing**: build with `scripts/sandbox-setup.sh` or set `agents.defaults.sandbox.docker.image`
- **Permission errors in sandbox**: set `docker.user` to a UID:GID matching workspace ownership
- **Custom tools not found**: set `docker.env.PATH` or add a script under `/etc/profile.d/` in Dockerfile
- **OOM-killed during build (exit 137)**: needs at least 2 GB RAM
- **Unauthorized in Control UI**: `docker compose run --rm openclaw-cli devices list` and approve
- **Gateway target shows ws://172.x.x.x**: reset `gateway.mode=local` and `gateway.bind=lan`

---

## Nix

Install OpenClaw declaratively with **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** — a batteries-included Home Manager module.

**What you get:**
- Gateway + macOS app + tools — all pinned
- Launchd service that survives reboots
- Plugin system with declarative config
- Instant rollback: `home-manager switch --rollback`

### Quick Start

1. Install Determinate Nix
2. Create a local flake (from the nix-openclaw repo templates)
3. Configure secrets (plain files at `~/.secrets/` work)
4. Fill in template placeholders and run `home-manager switch`
5. Verify the launchd service is running

### Nix Mode Runtime Behavior

When `OPENCLAW_NIX_MODE=1` is set (automatic with nix-openclaw), OpenClaw enters a deterministic mode that disables auto-install flows.

```bash
export OPENCLAW_NIX_MODE=1
```

On macOS, enable via defaults instead:
```bash
defaults write ai.openclaw.mac openclaw.nixMode -bool true
```

**What changes in Nix mode:**
- Auto-install and self-mutation flows are disabled
- Missing dependencies surface Nix-specific remediation messages
- UI surfaces a read-only Nix mode banner

### Config and State Paths

| Variable | Default |
|---|---|
| `OPENCLAW_HOME` | `HOME` / `USERPROFILE` / `os.homedir()` |
| `OPENCLAW_STATE_DIR` | `~/.openclaw` |
| `OPENCLAW_CONFIG_PATH` | `$OPENCLAW_STATE_DIR/openclaw.json` |

**Service PATH discovery**: The launchd/systemd gateway service auto-discovers Nix-profile binaries so plugins and tools that shell out to `nix`-installed executables work without manual PATH setup. When `NIX_PROFILES` is set, every entry is added to the service PATH in right-to-left precedence (matches Nix shell precedence — rightmost wins). When `NIX_PROFILES` is unset, `~/.nix-profile/bin` is added as a fallback. This applies to both macOS launchd and Linux systemd service environments.

---

## Raspberry Pi

Run a persistent, always-on OpenClaw Gateway on a Raspberry Pi (models run in the cloud via API, so even a modest Pi handles the workload).

### Prerequisites

- Raspberry Pi 4 or 5 with 2 GB+ RAM (4 GB recommended)
- MicroSD card (16 GB+) or USB SSD (better performance)
- 64-bit Raspberry Pi OS (**do not use 32-bit**)
- About 30 minutes

### Setup Steps

1. **Flash OS**: Raspberry Pi OS Lite (64-bit) using Raspberry Pi Imager with SSH enabled
2. **Connect via SSH**: `ssh user@gateway-host`
3. **Update system**: `sudo apt update && sudo apt upgrade -y && sudo apt install -y git curl build-essential`
4. **Set timezone**: `sudo timedatectl set-timezone America/Chicago`
5. **Install Node.js 24**: `curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash - && sudo apt install -y nodejs`

**Add swap (important for 2 GB or less):**
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

6. **Install OpenClaw**: `curl -fsSL https://openclaw.ai/install.sh | bash`
7. **Run onboarding**: `openclaw onboard --install-daemon`
8. **Verify**: `openclaw status && systemctl --user status openclaw-gateway.service`

**Access the Control UI** (from your laptop):
```bash
# Get dashboard URL from the Pi
ssh user@gateway-host 'openclaw dashboard --no-open'

# Create SSH tunnel in another terminal
ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
```

### Performance Tips

- **Use a USB SSD** — SD cards are slow and wear out
- **Enable module compile cache**:
```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```
- **Reduce memory usage**:
```bash
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt
sudo systemctl disable bluetooth
```

### Raspberry Pi Troubleshooting

- **Out of memory**: verify swap with `free -h`, disable unused services
- **Slow performance**: use USB SSD, check CPU throttling with `vcgencmd get_throttled` (should be `0x0`)
- **Service won't start**: check logs with `journalctl --user -u openclaw-gateway.service --no-pager -n 100` and run `openclaw doctor --non-interactive`. For headless Pi, verify lingering is enabled: `sudo loginctl enable-linger "$(whoami)"`
- **ARM binary issues**: verify `uname -m` shows `aarch64`
- **WiFi drops**: `sudo iwconfig wlan0 power off`

---

## Uninstall

### Easy Path (CLI Still Installed)

**Recommended:**
```bash
openclaw uninstall
```

**Non-interactive:**
```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

**Manual steps:**
1. Stop the gateway: `openclaw gateway stop`
2. Uninstall the gateway service: `openclaw gateway uninstall`
3. Delete state + config: `rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"`
4. Delete workspace (optional): `rm -rf ~/.openclaw/workspace`
5. Remove CLI: `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g`)
6. If macOS app: `rm -rf /Applications/OpenClaw.app`

### Manual Service Removal (CLI Not Installed)

If you used profiles (`--profile`/`OPENCLAW_PROFILE`), repeat state deletion for each dir (defaults to `~/.openclaw-<profile>`). If `OPENCLAW_CONFIG_PATH` is set to a custom location outside the state dir, delete that file too. For source checkouts: uninstall the gateway service **before** deleting the repo.

**macOS (launchd):**

Default label is `ai.openclaw.gateway` (or `ai.openclaw.<profile>` with named profiles; legacy `com.openclaw.*` may still exist — remove those too):
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Linux (systemd user unit):**

Default unit: `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):
```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

**Windows (Scheduled Task):**
```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

---

## Onboarding (CLI Wizard)

CLI onboarding is the **recommended** way to set up OpenClaw on macOS, Linux, or Windows (via WSL2).

```bash
openclaw onboard
```

**To reconfigure later:**
```bash
openclaw configure
openclaw agents add <name>
```

### QuickStart vs Advanced

**QuickStart (defaults):**
- Local gateway (loopback)
- Workspace default (or existing workspace)
- Gateway port **18789**
- Gateway auth **Token** (auto-generated)
- Tool policy default: `tools.profile: "coding"` (when unset)
- DM isolation default: `session.dmScope: "per-channel-peer"` when unset
- Tailscale exposure **Off**
- Telegram + WhatsApp DMs default to **allowlist**

**Advanced (full control):**
- Exposes every step (mode, workspace, gateway, channels, daemon, skills)

**Note**: `--json` does not imply non-interactive mode. For scripts, use `--non-interactive`.

Onboarding includes a **web search** step where you can pick a provider (Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax Search, Ollama Web Search, Perplexity, SearXNG, or Tavily). Configure later with `openclaw configure --section web`.

### What Onboarding Configures (Local Mode)

1. **Model/Auth** — choose any supported provider/auth flow (API key, OAuth, or provider-specific manual auth), including Custom Provider (OpenAI-compatible, Anthropic-compatible, or Unknown auto-detect). Security note: if this agent will run tools or process webhook/hooks content, prefer the strongest latest-generation model and keep tool policy strict. Weaker/older tiers are easier to prompt-inject. For non-interactive runs, `--secret-input-mode ref` stores env-backed refs instead of plaintext API key values. For Anthropic, interactive onboarding offers **Anthropic Claude CLI** as the preferred local path.
2. **Workspace** — Location for agent files (default `~/.openclaw/workspace`). Seeds bootstrap files.
3. **Gateway** — Port, bind address, auth mode, Tailscale exposure. In interactive token mode, choose default plaintext token storage or opt into SecretRef. Non-interactive: `--gateway-token-ref-env <ENV_VAR>`.
4. **Channels** — built-in and bundled chat channels: BlueBubbles, Discord, Feishu, Google Chat, Mattermost, Microsoft Teams, QQ Bot, Signal, Slack, Telegram, WhatsApp, and more
5. **Daemon** — installs LaunchAgent (macOS), systemd user unit (Linux/WSL2), or native Windows Scheduled Task with per-user Startup-folder fallback. If token auth is SecretRef-managed, daemon validates it but does not persist the resolved token. If token SecretRef is unresolved, daemon install is blocked with actionable guidance. If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, daemon install is blocked until mode is set.
6. **Health check** — starts the Gateway and verifies it's running
7. **Skills** — installs recommended skills and optional dependencies

Re-running onboarding does **NOT** wipe anything unless you explicitly choose **Reset** (or pass `--reset`). CLI `--reset` defaults to config, credentials, and sessions; use `--reset-scope full` to include workspace. If the config is invalid or contains legacy keys, onboarding asks you to run `openclaw doctor` first.

**Remote mode** only configures the local client to connect to a Gateway elsewhere. It does **not** install or change anything on the remote host.

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

Add `--json` for machine-readable summary.

**Gateway token SecretRef in non-interactive mode:**
```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
```

### Add Another Agent

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.4 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

### What the Wizard Writes

Typical fields in `~/.openclaw/openclaw.json`:
- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers`
- `tools.profile`
- `gateway.*` (mode, bind, auth, tailscale)
- `session.dmScope`
- Channel tokens (`channels.telegram.botToken`, etc.)
- `wizard.lastRunAt`, `wizard.lastRunVersion`, etc.

### Onboarding Reference Details

**Existing config detection:**
- If `~/.openclaw/openclaw.json` exists, choose **Keep / Modify / Reset**
- `--reset` defaults to `config+creds+sessions`; use `--reset-scope full` to also remove workspace
- Reset uses `trash` (never `rm`) and offers scopes: Config only | Config + credentials + sessions | Full reset

**Auth profiles** live at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

**Non-interactive secret reference:**
- `--secret-input-mode ref` stores env-backed refs instead of plaintext API key values
- For Anthropic, interactive onboarding offers **Anthropic Claude CLI** as the preferred local path

**Daemon install notes:**
- If token auth requires a token and `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist the resolved token
- If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly
- Native Windows: Scheduled Task first, with a per-user Startup-folder login item fallback if task creation is denied

**Signal setup (signal-cli):**
- Onboarding can install `signal-cli` from GitHub releases
- JVM builds require **Java 21**; native builds are used when available
- Windows uses WSL2 for the Linux flow

---

## VPS / Linux Server Deployment

### Provider Options

- **Railway**: one-click, browser setup
- **Northflank**: one-click, browser setup
- **DigitalOcean**: simple paid VPS
- **Oracle Cloud**: always Free ARM tier
- **Fly.io**: Fly Machines (see below)
- **Hetzner**: Docker on Hetzner VPS (see below)
- **GCP**: Compute Engine
- **Azure**: Linux VM
- **Raspberry Pi**: ARM self-hosted
- **Render**: managed cloud hosting
- **Kubernetes**: K8s deployment
- **Podman**: rootless container alternative to Docker
- **Ansible**: automated fleet provisioning

### How Cloud Setups Work

- The **Gateway runs on the VPS** and owns state + workspace
- You connect from your laptop or phone via the **Control UI** or **Tailscale/SSH**
- Treat the VPS as the source of truth and **back up** the state + workspace regularly
- Secure default: keep the Gateway on loopback and access it via SSH tunnel or Tailscale Serve

### Startup Tuning for Small VMs and ARM Hosts

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

**systemd tuning:**
```bash
systemctl --user edit openclaw-gateway.service
```
```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

### Hetzner (Docker, Production Guide)

**Goal**: Run a persistent OpenClaw Gateway on a Hetzner VPS using Docker.

**Quick path:**
1. Provision Hetzner VPS
2. Install Docker: `apt-get update && apt-get install -y git curl ca-certificates && curl -fsSL https://get.docker.com | sh`
3. Clone repo: `git clone https://github.com/openclaw/openclaw.git && cd openclaw`
4. Create persistent host directories: `mkdir -p /root/.openclaw/workspace && chown -R 1000:1000 /root/.openclaw`
5. Configure `.env` and `docker-compose.yml`
6. `docker compose up -d`

**Environment variables (`.env`):**
```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace
GOG_KEYRING_PASSWORD=
XDG_CONFIG_HOME=/home/node/.openclaw
```

**docker-compose.yml snippet:**
```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command: ["node", "dist/index.js", "gateway", "--bind", "${OPENCLAW_GATEWAY_BIND}", "--port", "${OPENCLAW_GATEWAY_PORT}", "--allow-unconfigured"]
```

**Access (SSH tunnel from laptop):**
```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
# Then open http://127.0.0.1:18789/
```

**Terraform community resource:**
- Infrastructure: [openclaw-terraform-hetzner](https://github.com/andreesg/openclaw-terraform-hetzner)
- Docker config: [openclaw-docker-config](https://github.com/andreesg/openclaw-docker-config)

### Fly.io Deployment

**Prerequisites:**
- `flyctl` CLI installed
- Fly.io account
- Model auth API key
- Channel credentials

**Quick path:**
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
fly apps create my-openclaw
fly volumes create openclaw_data --size 1 --region iad
```

**fly.toml (key settings):**
```toml
app = "my-openclaw"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  min_machines_running = 1

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

**Set secrets:**
```bash
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)
fly secrets set ANTHROPIC_API_KEY=sk-ant-...
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Deploy:**
```bash
fly deploy
fly status
fly logs
```

**Fly.io Troubleshooting:**
- "App is not listening on expected address": add `--bind lan` to process command
- Health checks failing: ensure `internal_port` matches gateway port
- OOM issues: increase memory to `2048mb`
- Gateway lock issues: `fly ssh console --command "rm -f /data/gateway.*.lock"` then restart
- Config not being read: verify `/data/openclaw.json` exists with `gateway.mode="local"`

**Cost**: ~$10-15/month with recommended config (shared-cpu-2x, 2GB RAM)

**Private Deployment (Hardened):**
```bash
# Release public IPs
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Deploy with private config
fly deploy -c fly.private.toml

# Access via proxy
fly proxy 3000:3000 -a my-openclaw
```

---

## Migration Guide

### What Gets Migrated

When you copy the **state directory** (`~/.openclaw/` by default) and your **workspace**, you preserve:
- **Config** — `openclaw.json` and all gateway settings
- **Auth** — per-agent `auth-profiles.json` (API keys + OAuth), plus credentials
- **Sessions** — conversation history and agent state
- **Channel state** — WhatsApp login, Telegram session, etc.
- **Workspace files** — `MEMORY.md`, `USER.md`, skills, and prompts

### Migration Steps

1. **Stop and back up**: `openclaw gateway stop && cd ~ && tar -czf openclaw-state.tgz .openclaw`
2. **Install on new machine**: `curl -fsSL https://openclaw.ai/install.sh | bash`
3. **Copy and extract**: `cd ~ && tar -xzf openclaw-state.tgz`
4. **Run doctor**: `openclaw doctor && openclaw gateway restart && openclaw status`

### Common Pitfalls

- **Profile/state-dir mismatch**: use the same `--profile` or `OPENCLAW_STATE_DIR` you migrated
- **Copying only `openclaw.json`**: Always migrate the entire state directory — model auth profiles are in `agents/<agentId>/agent/auth-profiles.json`
- **Permissions**: ensure state directory and workspace are owned by the user running the gateway
- **Remote mode**: migrate the gateway host itself, not your local laptop
- **Secrets in backups**: store backups encrypted

### Verification Checklist

- `openclaw status` shows the gateway running
- Channels are still connected (no re-pairing needed)
- Dashboard opens and shows existing sessions
- Workspace files (memory, configs) are present
- To return to latest after rollback: `git checkout main && git pull`

---

## Platform Notes

### macOS

**Install**: `curl -fsSL https://openclaw.ai/install.sh | bash`

The macOS **menu-bar app** owns permissions, manages/attaches to the Gateway locally (launchd), and exposes macOS capabilities to the agent as a node.

**What it does:**
- Shows native notifications and status in the menu bar
- Owns TCC prompts (Notifications, Accessibility, Screen Recording, Microphone, Speech Recognition, Automation/AppleScript)
- Runs or connects to the Gateway (local or remote)
- Exposes macOS-only tools (Canvas, Camera, Screen Recording, `system.run`)
- Optionally hosts **PeekabooBridge** for UI automation
- Installs the global CLI (`openclaw`) on request via npm, pnpm, or bun (app prefers npm → pnpm → bun; Node remains the recommended Gateway runtime)

**Local vs Remote mode:**
- **Local**: app attaches to a running local Gateway or enables the launchd service via `openclaw gateway install`. Does NOT spawn the Gateway as a child process.
- **Remote**: app connects to a Gateway over SSH/Tailscale and starts the local **node host service** (so the remote Gateway can reach this Mac). Gateway discovery prefers Tailscale MagicDNS names over raw tailnet IPs for more reliable recovery when IPs change.

**Launchd control:**
```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

**State dir placement**: Avoid iCloud or other cloud-synced folders. Use `OPENCLAW_STATE_DIR=~/.openclaw`.

**Exec approvals (system.run)**: Controlled by Settings → Exec approvals. Stored at `~/.openclaw/exec-approvals.json`. `system.run` environment overrides are filtered (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`). For shell wrappers (`bash|sh|zsh ... -c/-lc`), environment overrides are reduced to a small allowlist (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`). For allow-always in allowlist mode, known dispatch wrappers (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths.

**Deep links** (`openclaw://agent`):
```bash
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

### Windows

OpenClaw supports both **native Windows** and **WSL2**. WSL2 is the more stable path and recommended for the full experience.

**Native Windows status**: Core CLI and Gateway work natively. `openclaw onboard --non-interactive --install-daemon` tries Windows Scheduled Tasks first; if denied, falls back to a per-user Startup-folder login item. If `schtasks` itself hangs, OpenClaw aborts that path quickly and falls back instead of hanging forever. WSL2 is still recommended for the full experience.

**WSL2 Setup:**
1. `wsl --install` (or `wsl --install -d Ubuntu-24.04`)
2. Enable systemd: add `[boot]` `systemd=true` to `/etc/wsl.conf`, then `wsl --shutdown`
3. Inside WSL: `curl -fsSL https://openclaw.ai/install.sh | bash`

**Gateway auto-start before Windows login:**
```bash
# Inside WSL
sudo loginctl enable-linger "$(whoami)"
openclaw gateway install

# In PowerShell as Administrator
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

**Expose WSL services over LAN (portproxy):**
```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22
$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort connectaddress=$WslIp connectport=$TargetPort
```

### Linux

**Node is the recommended runtime.** Bun is supported for the global CLI install path. For the Gateway runtime, Node remains the recommended daemon runtime.

**Beginner quick path (VPS):**
1. `npm i -g openclaw@latest`
2. `openclaw onboard --install-daemon`
3. From laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
4. Open `http://127.0.0.1:18789/` and authenticate

**Gateway service (systemd user unit):**
```ini
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group

[Install]
WantedBy=default.target
```

```bash
systemctl --user enable --now openclaw-gateway.service
```

**Linux OOM protection**: For eligible child process spawns, OpenClaw uses a `/bin/sh` wrapper that raises the child's `oom_score_adj` to `1000`. Skip with `OPENCLAW_CHILD_OOM_SCORE_ADJ=0`.

### iOS

- Status: **internal preview** (not publicly distributed yet)
- Connects to a Gateway over WebSocket (LAN or tailnet)
- Exposes node capabilities: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake

**Quick start:**
1. Start the Gateway: `openclaw gateway --port 18789`
2. Open iOS app → Settings → pick discovered gateway (or manual host/port)
3. Approve pairing: `openclaw devices list && openclaw devices approve <requestId>`
4. Verify: `openclaw nodes status`

**Relay-backed push**: Official builds use an external push relay instead of publishing raw APNs token to the gateway. Set `gateway.push.apns.relay.baseUrl` in config.

**Common errors:**
- `NODE_BACKGROUND_UNAVAILABLE`: bring iOS app to foreground
- `A2UI_HOST_NOT_CONFIGURED`: check `canvasHost` in gateway configuration
- Pairing prompt never appears: run `openclaw devices list` and approve manually

### Android

- **Not publicly released yet**; source available in repo under `apps/android`
- Build: `./gradlew :app:assemblePlayDebug` (requires Java 17 and Android SDK)
- Role: companion node app (Android does not host the Gateway)

**Connection:**
- Android connects directly to the Gateway WebSocket and uses device pairing (`role: node`)
- The app keeps its gateway connection alive via a **foreground service** (persistent notification)
- For Tailscale/public hosts: requires secure endpoint (`wss://` or Tailscale Serve) — a plain `gateway.bind: "tailnet"` setup is not enough for first-time remote Android pairing unless TLS is terminated separately
- Cleartext `ws://` supported on private LAN addresses, `.local` hosts, `localhost`, `127.0.0.1`, and the Android emulator bridge (`10.0.2.2`)
- After first successful pairing, Android auto-reconnects on launch (manual endpoint if enabled, otherwise last discovered gateway)
- Optional node auto-approval for controlled subnets: `gateway.nodes.pairing.autoApproveCidrs: ["192.168.1.0/24"]` (disabled by default)

**Android notification forwarding config:**
```json5
{
  notifications: {
    allowPackages: ["com.slack", "com.whatsapp"],
    denyPackages: ["com.android.systemui"],
    quietHours: {
      start: "22:00",
      end: "07:00",
    },
    rateLimit: 5,  // requests per minute
  },
}
```

**Android command families** (availability depends on device + permissions):
- `device.status`, `device.info`, `device.permissions`, `device.health`
- `notifications.list`, `notifications.actions`
- `photos.latest`
- `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `callLog.search`
- `sms.search`
- `motion.activity`, `motion.pedometer`

---

## Control UI (Custom Build)

If you maintain a localized or customized dashboard build, point `gateway.controlUi.root` to a directory that contains your built static assets and `index.html`:

```json5
{
  gateway: {
    controlUi: {
      enabled: true,
      root: "/path/to/your/custom-dashboard/dist",
    },
  },
}
```

This allows you to serve a custom Control UI from the Gateway without modifying the OpenClaw package itself.
