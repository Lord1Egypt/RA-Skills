# Installation & Setup

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 11

---

<!-- SOURCE: https://docs.openclaw.ai/install/installer -->

# Installer Internals - OpenClaw

OpenClaw ships three installer scripts, served from `openclaw.ai`.

| Script | Platform | What it does |
| --- | --- | --- |
| [`install.sh`](https://docs.openclaw.ai/install/installer#installsh) | macOS / Linux / WSL | Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding. |
| [`install-cli.sh`](https://docs.openclaw.ai/install/installer#install-clish) | macOS / Linux / WSL | Installs Node + OpenClaw into a local prefix (`~/.openclaw`). No root required. |
| [`install.ps1`](https://docs.openclaw.ai/install/installer#installps1) | Windows (PowerShell) | Installs Node if needed, installs OpenClaw via npm (default) or git, and can run onboarding. |

## Quick commands

*   install.sh
    
*   install-cli.sh
    
*   install.ps1
    

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --help
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --help
```

```
iwr -useb https://openclaw.ai/install.ps1 | iex
```

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -Tag beta -NoOnboard -DryRun
```

* * *

## install.sh

### Flow (install.sh)

### Source checkout detection

If run inside an OpenClaw checkout (`package.json` + `pnpm-workspace.yaml`), the script offers:

*   use checkout (`git`), or
*   use global install (`npm`)

If no TTY is available and no install method is set, it defaults to `npm` and warns. The script exits with code `2` for invalid method selection or invalid `--install-method` values.

### Examples (install.sh)

*   Default
    
*   Skip onboarding
    
*   Git install
    
*   Dry run
    

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --dry-run
```

* * *

## install-cli.sh

### Flow (install-cli.sh)

### Examples (install-cli.sh)

*   Default
    
*   Custom prefix + version
    
*   Automation JSON output
    
*   Run onboarding
    

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --prefix /opt/openclaw --version latest
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --onboard
```

* * *

## install.ps1

### Flow (install.ps1)

### Examples (install.ps1)

*   Default
    
*   Git install
    
*   Custom git directory
    
*   Dry run
    
*   Debug trace
    

```
iwr -useb https://openclaw.ai/install.ps1 | iex
```

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git
```

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -InstallMethod git -GitDir "C:\openclaw"
```

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -DryRun
```

```
# install.ps1 has no dedicated -Verbose flag yet.
Set-PSDebug -Trace 1
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
Set-PSDebug -Trace 0
```

* * *

## CI and automation

Use non-interactive flags/env vars for predictable runs.

*   install.sh (non-interactive npm)
    
*   install.sh (non-interactive git)
    
*   install-cli.sh (JSON)
    
*   install.ps1 (skip onboarding)
    

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-prompt --no-onboard
```

```
OPENCLAW_INSTALL_METHOD=git OPENCLAW_NO_PROMPT=1 \
  curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash
```

```
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install-cli.sh | bash -s -- --json --prefix /opt/openclaw
```

```
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

* * *

## Troubleshooting

---

<!-- SOURCE: https://docs.openclaw.ai/install/podman -->

# Podman - OpenClaw

Run the OpenClaw gateway in a **rootless** Podman container. Uses the same image as Docker (build from the repo [Dockerfile](https://github.com/openclaw/openclaw/blob/main/Dockerfile)).

## Requirements

*   Podman (rootless)
*   Sudo for one-time setup (create user, build image)

## Quick start

**1\. One-time setup** (from repo root; creates user, builds image, installs launch script):

This also creates a minimal `~openclaw/.openclaw/openclaw.json` (sets `gateway.mode="local"`) so the gateway can start without running the wizard. By default the container is **not** installed as a systemd service, you start it manually (see below). For a production-style setup with auto-start and restarts, install it as a systemd Quadlet user service instead:

```
./setup-podman.sh --quadlet
```

(Or set `OPENCLAW_PODMAN_QUADLET=1`; use `--container` to install only the container and launch script.) Optional build-time env vars (set before running `setup-podman.sh`):

*   `OPENCLAW_DOCKER_APT_PACKAGES` — install extra apt packages during image build
*   `OPENCLAW_EXTENSIONS` — pre-install extension dependencies (space-separated extension names, e.g. `diagnostics-otel matrix`)

**2\. Start gateway** (manual, for quick smoke testing):

```
./scripts/run-openclaw-podman.sh launch
```

**3\. Onboarding wizard** (e.g. to add channels or providers):

```
./scripts/run-openclaw-podman.sh launch setup
```

Then open `http://127.0.0.1:18789/` and use the token from `~openclaw/.openclaw/.env` (or the value printed by setup).

## Systemd (Quadlet, optional)

If you ran `./setup-podman.sh --quadlet` (or `OPENCLAW_PODMAN_QUADLET=1`), a [Podman Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) unit is installed so the gateway runs as a systemd user service for the openclaw user. The service is enabled and started at the end of setup.

*   **Start:** `sudo systemctl --machine openclaw@ --user start openclaw.service`
*   **Stop:** `sudo systemctl --machine openclaw@ --user stop openclaw.service`
*   **Status:** `sudo systemctl --machine openclaw@ --user status openclaw.service`
*   **Logs:** `sudo journalctl --machine openclaw@ --user -u openclaw.service -f`

The quadlet file lives at `~openclaw/.config/containers/systemd/openclaw.container`. To change ports or env, edit that file (or the `.env` it sources), then `sudo systemctl --machine openclaw@ --user daemon-reload` and restart the service. On boot, the service starts automatically if lingering is enabled for openclaw (setup does this when loginctl is available). To add quadlet **after** an initial setup that did not use it, re-run: `./setup-podman.sh --quadlet`.

## The openclaw user (non-login)

`setup-podman.sh` creates a dedicated system user `openclaw`:

*   **Shell:** `nologin` — no interactive login; reduces attack surface.
*   **Home:** e.g. `/home/openclaw` — holds `~/.openclaw` (config, workspace) and the launch script `run-openclaw-podman.sh`.
*   **Rootless Podman:** The user must have a **subuid** and **subgid** range. Many distros assign these automatically when the user is created. If setup prints a warning, add lines to `/etc/subuid` and `/etc/subgid`: Then start the gateway as that user (e.g. from cron or systemd):
    
    ```
    sudo -u openclaw /home/openclaw/run-openclaw-podman.sh
    sudo -u openclaw /home/openclaw/run-openclaw-podman.sh setup
    ```
    
*   **Config:** Only `openclaw` and root can access `/home/openclaw/.openclaw`. To edit config: use the Control UI once the gateway is running, or `sudo -u openclaw $EDITOR /home/openclaw/.openclaw/openclaw.json`.

## Environment and config

*   **Token:** Stored in `~openclaw/.openclaw/.env` as `OPENCLAW_GATEWAY_TOKEN`. `setup-podman.sh` and `run-openclaw-podman.sh` generate it if missing (uses `openssl`, `python3`, or `od`).
*   **Optional:** In that `.env` you can set provider keys (e.g. `GROQ_API_KEY`, `OLLAMA_API_KEY`) and other OpenClaw env vars.
*   **Host ports:** By default the script maps `18789` (gateway) and `18790` (bridge). Override the **host** port mapping with `OPENCLAW_PODMAN_GATEWAY_HOST_PORT` and `OPENCLAW_PODMAN_BRIDGE_HOST_PORT` when launching.
*   **Gateway bind:** By default, `run-openclaw-podman.sh` starts the gateway with `--bind loopback` for safe local access. To expose on LAN, set `OPENCLAW_GATEWAY_BIND=lan` and configure `gateway.controlUi.allowedOrigins` (or explicitly enable host-header fallback) in `openclaw.json`.
*   **Paths:** Host config and workspace default to `~openclaw/.openclaw` and `~openclaw/.openclaw/workspace`. Override the host paths used by the launch script with `OPENCLAW_CONFIG_DIR` and `OPENCLAW_WORKSPACE_DIR`.

## Storage model

*   **Persistent host data:** `OPENCLAW_CONFIG_DIR` and `OPENCLAW_WORKSPACE_DIR` are bind-mounted into the container and retain state on the host.
*   **Ephemeral sandbox tmpfs:** if you enable `agents.defaults.sandbox`, the tool sandbox containers mount `tmpfs` at `/tmp`, `/var/tmp`, and `/run`. Those paths are memory-backed and disappear with the sandbox container; the top-level Podman container setup does not add its own tmpfs mounts.
*   **Disk growth hotspots:** the main paths to watch are `media/`, `agents/<agentId>/sessions/sessions.json`, transcript JSONL files, `cron/runs/*.jsonl`, and rolling file logs under `/tmp/openclaw/` (or your configured `logging.file`).

`setup-podman.sh` now stages the image tar in a private temp directory and prints the chosen base dir during setup. For non-root runs it accepts `TMPDIR` only when that base is safe to use; otherwise it falls back to `/var/tmp`, then `/tmp`. The saved tar stays owner-only and is streamed into the target user’s `podman load`, so private caller temp dirs do not block setup.

## Useful commands

*   **Logs:** With quadlet: `sudo journalctl --machine openclaw@ --user -u openclaw.service -f`. With script: `sudo -u openclaw podman logs -f openclaw`
*   **Stop:** With quadlet: `sudo systemctl --machine openclaw@ --user stop openclaw.service`. With script: `sudo -u openclaw podman stop openclaw`
*   **Start again:** With quadlet: `sudo systemctl --machine openclaw@ --user start openclaw.service`. With script: re-run the launch script or `podman start openclaw`
*   **Remove container:** `sudo -u openclaw podman rm -f openclaw` — config and workspace on the host are kept

## Troubleshooting

*   **Permission denied (EACCES) on config or auth-profiles:** The container defaults to `--userns=keep-id` and runs as the same uid/gid as the host user running the script. Ensure your host `OPENCLAW_CONFIG_DIR` and `OPENCLAW_WORKSPACE_DIR` are owned by that user.
*   **Gateway start blocked (missing `gateway.mode=local`):** Ensure `~openclaw/.openclaw/openclaw.json` exists and sets `gateway.mode="local"`. `setup-podman.sh` creates this file if missing.
*   **Rootless Podman fails for user openclaw:** Check `/etc/subuid` and `/etc/subgid` contain a line for `openclaw` (e.g. `openclaw:100000:65536`). Add it if missing and restart.
*   **Container name in use:** The launch script uses `podman run --replace`, so the existing container is replaced when you start again. To clean up manually: `podman rm -f openclaw`.
*   **Script not found when running as openclaw:** Ensure `setup-podman.sh` was run so that `run-openclaw-podman.sh` is copied to openclaw’s home (e.g. `/home/openclaw/run-openclaw-podman.sh`).
*   **Quadlet service not found or fails to start:** Run `sudo systemctl --machine openclaw@ --user daemon-reload` after editing the `.container` file. Quadlet requires cgroups v2: `podman info --format '{{.Host.CgroupsVersion}}'` should show `2`.

## Optional: run as your own user

To run the gateway as your normal user (no dedicated openclaw user): build the image, create `~/.openclaw/.env` with `OPENCLAW_GATEWAY_TOKEN`, and run the container with `--userns=keep-id` and mounts to your `~/.openclaw`. The launch script is designed for the openclaw-user flow; for a single-user setup you can instead run the `podman run` command from the script manually, pointing config and workspace to your home. Recommended for most users: use `setup-podman.sh` and run as the openclaw user so config and process are isolated.

---

<!-- SOURCE: https://docs.openclaw.ai/install/nix -->

# Nix - OpenClaw

## Nix Installation

The recommended way to run OpenClaw with Nix is via **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** — a batteries-included Home Manager module.

## Quick Start

Paste this to your AI agent (Claude, Cursor, etc.):

```
I want to set up nix-openclaw on my Mac.
Repository: github:openclaw/nix-openclaw

What I need you to do:
1. Check if Determinate Nix is installed (if not, install it)
2. Create a local flake at ~/code/openclaw-local using templates/agent-first/flake.nix
3. Help me create a Telegram bot (@BotFather) and get my chat ID (@userinfobot)
4. Set up secrets (bot token, model provider API key) - plain files at ~/.secrets/ is fine
5. Fill in the template placeholders and run home-manager switch
6. Verify: launchd running, bot responds to messages

Reference the nix-openclaw README for module options.
```

> **📦 Full guide: [github.com/openclaw/nix-openclaw](https://github.com/openclaw/nix-openclaw)** The nix-openclaw repo is the source of truth for Nix installation. This page is just a quick overview.

## What you get

*   Gateway + macOS app + tools (whisper, spotify, cameras) — all pinned
*   Launchd service that survives reboots
*   Plugin system with declarative config
*   Instant rollback: `home-manager switch --rollback`

* * *

## Nix Mode Runtime Behavior

When `OPENCLAW_NIX_MODE=1` is set (automatic with nix-openclaw): OpenClaw supports a **Nix mode** that makes configuration deterministic and disables auto-install flows. Enable it by exporting:

On macOS, the GUI app does not automatically inherit shell env vars. You can also enable Nix mode via defaults:

```
defaults write ai.openclaw.mac openclaw.nixMode -bool true
```

### Config + state paths

OpenClaw reads JSON5 config from `OPENCLAW_CONFIG_PATH` and stores mutable data in `OPENCLAW_STATE_DIR`. When needed, you can also set `OPENCLAW_HOME` to control the base home directory used for internal path resolution.

*   `OPENCLAW_HOME` (default precedence: `HOME` / `USERPROFILE` / `os.homedir()`)
*   `OPENCLAW_STATE_DIR` (default: `~/.openclaw`)
*   `OPENCLAW_CONFIG_PATH` (default: `$OPENCLAW_STATE_DIR/openclaw.json`)

When running under Nix, set these explicitly to Nix-managed locations so runtime state and config stay out of the immutable store.

### Runtime behavior in Nix mode

*   Auto-install and self-mutation flows are disabled
*   Missing dependencies surface Nix-specific remediation messages
*   UI surfaces a read-only Nix mode banner when present

## Packaging note (macOS)

The macOS packaging flow expects a stable Info.plist template at:

```
apps/macos/Sources/OpenClaw/Resources/Info.plist
```

[`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) copies this template into the app bundle and patches dynamic fields (bundle ID, version/build, Git SHA, Sparkle keys). This keeps the plist deterministic for SwiftPM packaging and Nix builds (which do not rely on a full Xcode toolchain).

*   [nix-openclaw](https://github.com/openclaw/nix-openclaw) — full setup guide
*   [Wizard](https://docs.openclaw.ai/start/wizard) — non-Nix CLI setup
*   [Docker](https://docs.openclaw.ai/install/docker) — containerized setup

---

<!-- SOURCE: https://docs.openclaw.ai/install/ansible -->

# Ansible - OpenClaw

## Ansible Installation

The recommended way to deploy OpenClaw to production servers is via **[openclaw-ansible](https://github.com/openclaw/openclaw-ansible)** — an automated installer with security-first architecture.

## Quick Start

One-command install:

```
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

> **📦 Full guide: [github.com/openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible)** The openclaw-ansible repo is the source of truth for Ansible deployment. This page is a quick overview.

## What You Get

*   🔒 **Firewall-first security**: UFW + Docker isolation (only SSH + Tailscale accessible)
*   🔐 **Tailscale VPN**: Secure remote access without exposing services publicly
*   🐳 **Docker**: Isolated sandbox containers, localhost-only bindings
*   🛡️ **Defense in depth**: 4-layer security architecture
*   🚀 **One-command setup**: Complete deployment in minutes
*   🔧 **Systemd integration**: Auto-start on boot with hardening

## Requirements

*   **OS**: Debian 11+ or Ubuntu 20.04+
*   **Access**: Root or sudo privileges
*   **Network**: Internet connection for package installation
*   **Ansible**: 2.14+ (installed automatically by quick-start script)

## What Gets Installed

The Ansible playbook installs and configures:

1.  **Tailscale** (mesh VPN for secure remote access)
2.  **UFW firewall** (SSH + Tailscale ports only)
3.  **Docker CE + Compose V2** (for agent sandboxes)
4.  **Node.js 22.x + pnpm** (runtime dependencies)
5.  **OpenClaw** (host-based, not containerized)
6.  **Systemd service** (auto-start with security hardening)

Note: The gateway runs **directly on the host** (not in Docker), but agent sandboxes use Docker for isolation. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) for details.

## Post-Install Setup

After installation completes, switch to the openclaw user:

The post-install script will guide you through:

1.  **Onboarding wizard**: Configure OpenClaw settings
2.  **Provider login**: Connect WhatsApp/Telegram/Discord/Signal
3.  **Gateway testing**: Verify the installation
4.  **Tailscale setup**: Connect to your VPN mesh

### Quick commands

```
# Check service status
sudo systemctl status openclaw

# View live logs
sudo journalctl -u openclaw -f

# Restart gateway
sudo systemctl restart openclaw

# Provider login (run as openclaw user)
sudo -i -u openclaw
openclaw channels login
```

## Security Architecture

### 4-Layer Defense

1.  **Firewall (UFW)**: Only SSH (22) + Tailscale (41641/udp) exposed publicly
2.  **VPN (Tailscale)**: Gateway accessible only via VPN mesh
3.  **Docker Isolation**: DOCKER-USER iptables chain prevents external port exposure
4.  **Systemd Hardening**: NoNewPrivileges, PrivateTmp, unprivileged user

### Verification

Test external attack surface:

Should show **only port 22** (SSH) open. All other services (gateway, Docker) are locked down.

### Docker Availability

Docker is installed for **agent sandboxes** (isolated tool execution), not for running the gateway itself. The gateway binds to localhost only and is accessible via Tailscale VPN. See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for sandbox configuration.

## Manual Installation

If you prefer manual control over the automation:

```
# 1. Install prerequisites
sudo apt update && sudo apt install -y ansible git

# 2. Clone repository
git clone https://github.com/openclaw/openclaw-ansible.git
cd openclaw-ansible

# 3. Install Ansible collections
ansible-galaxy collection install -r requirements.yml

# 4. Run playbook
./run-playbook.sh

# Or run directly (then manually execute /tmp/openclaw-setup.sh after)
# ansible-playbook playbook.yml --ask-become-pass
```

## Updating OpenClaw

The Ansible installer sets up OpenClaw for manual updates. See [Updating](https://docs.openclaw.ai/install/updating) for the standard update flow. To re-run the Ansible playbook (e.g., for configuration changes):

```
cd openclaw-ansible
./run-playbook.sh
```

Note: This is idempotent and safe to run multiple times.

## Troubleshooting

### Firewall blocks my connection

If you’re locked out:

*   Ensure you can access via Tailscale VPN first
*   SSH access (port 22) is always allowed
*   The gateway is **only** accessible via Tailscale by design

### Service won’t start

```
# Check logs
sudo journalctl -u openclaw -n 100

# Verify permissions
sudo ls -la /opt/openclaw

# Test manual start
sudo -i -u openclaw
cd ~/openclaw
pnpm start
```

### Docker sandbox issues

```
# Verify Docker is running
sudo systemctl status docker

# Check sandbox image
sudo docker images | grep openclaw-sandbox

# Build sandbox image if missing
cd /opt/openclaw/openclaw
sudo -u openclaw ./scripts/sandbox-setup.sh
```

### Provider login fails

Make sure you’re running as the `openclaw` user:

```
sudo -i -u openclaw
openclaw channels login
```

## Advanced Configuration

For detailed security architecture and troubleshooting:

*   [Security Architecture](https://github.com/openclaw/openclaw-ansible/blob/main/docs/security.md)
*   [Technical Details](https://github.com/openclaw/openclaw-ansible/blob/main/docs/architecture.md)
*   [Troubleshooting Guide](https://github.com/openclaw/openclaw-ansible/blob/main/docs/troubleshooting.md)

*   [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) — full deployment guide
*   [Docker](https://docs.openclaw.ai/install/docker) — containerized gateway setup
*   [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing) — agent sandbox configuration
*   [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) — per-agent isolation

---

<!-- SOURCE: https://docs.openclaw.ai/install/docker -->

# Docker - OpenClaw

## Docker (optional)

Docker is **optional**. Use it only if you want a containerized gateway or to validate the Docker flow.

## Is Docker right for me?

*   **Yes**: you want an isolated, throwaway gateway environment or to run OpenClaw on a host without local installs.
*   **No**: you’re running on your own machine and just want the fastest dev loop. Use the normal install flow instead.
*   **Sandboxing note**: agent sandboxing uses Docker too, but it does **not** require the full gateway to run in Docker. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing).

This guide covers:

*   Containerized Gateway (full OpenClaw in Docker)
*   Per-session Agent Sandbox (host gateway + Docker-isolated agent tools)

Sandboxing details: [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing)

## Requirements

*   Docker Desktop (or Docker Engine) + Docker Compose v2
*   At least 2 GB RAM for image build (`pnpm install` may be OOM-killed on 1 GB hosts with exit 137)
*   Enough disk for images + logs
*   If running on a VPS/public host, review [Security hardening for network exposure](https://docs.openclaw.ai/gateway/security#04-network-exposure-bind--port--firewall), especially Docker `DOCKER-USER` firewall policy.

## Containerized Gateway (Docker Compose)

### Quick start (recommended)

From repo root:

This script:

*   builds the gateway image locally (or pulls a remote image if `OPENCLAW_IMAGE` is set)
*   runs the onboarding wizard
*   prints optional provider setup hints
*   starts the gateway via Docker Compose
*   generates a gateway token and writes it to `.env`

Optional env vars:

*   `OPENCLAW_IMAGE` — use a remote image instead of building locally (e.g. `ghcr.io/openclaw/openclaw:latest`)
*   `OPENCLAW_DOCKER_APT_PACKAGES` — install extra apt packages during build
*   `OPENCLAW_EXTENSIONS` — pre-install extension dependencies at build time (space-separated extension names, e.g. `diagnostics-otel matrix`)
*   `OPENCLAW_EXTRA_MOUNTS` — add extra host bind mounts
*   `OPENCLAW_HOME_VOLUME` — persist `/home/node` in a named volume
*   `OPENCLAW_SANDBOX` — opt in to Docker gateway sandbox bootstrap. Only explicit truthy values enable it: `1`, `true`, `yes`, `on`
*   `OPENCLAW_INSTALL_DOCKER_CLI` — build arg passthrough for local image builds (`1` installs Docker CLI in the image). `docker-setup.sh` sets this automatically when `OPENCLAW_SANDBOX=1` for local builds.
*   `OPENCLAW_DOCKER_SOCKET` — override Docker socket path (default: `DOCKER_HOST=unix://...` path, else `/var/run/docker.sock`)
*   `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` — break-glass: allow trusted private-network `ws://` targets for CLI/onboarding client paths (default is loopback-only)
*   `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` — disable container browser hardening flags `--disable-3d-apis`, `--disable-software-rasterizer`, `--disable-gpu` when you need WebGL/3D compatibility.
*   `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` — keep extensions enabled when browser flows require them (default keeps extensions disabled in sandbox browser).
*   `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` — set Chromium renderer process limit; set to `0` to skip the flag and use Chromium default behavior.

After it finishes:

*   Open `http://127.0.0.1:18789/` in your browser.
*   Paste the token into the Control UI (Settings → token).
*   Need the URL again? Run `docker compose run --rm openclaw-cli dashboard --no-open`.

### Enable agent sandbox for Docker gateway (opt-in)

`docker-setup.sh` can also bootstrap `agents.defaults.sandbox.*` for Docker deployments. Enable with:

```
export OPENCLAW_SANDBOX=1
./docker-setup.sh
```

Custom socket path (for example rootless Docker):

```
export OPENCLAW_SANDBOX=1
export OPENCLAW_DOCKER_SOCKET=/run/user/1000/docker.sock
./docker-setup.sh
```

Notes:

*   The script mounts `docker.sock` only after sandbox prerequisites pass.
*   If sandbox setup cannot be completed, the script resets `agents.defaults.sandbox.mode` to `off` to avoid stale/broken sandbox config on reruns.
*   If `Dockerfile.sandbox` is missing, the script prints a warning and continues; build `openclaw-sandbox:bookworm-slim` with `scripts/sandbox-setup.sh` if needed.
*   For non-local `OPENCLAW_IMAGE` values, the image must already contain Docker CLI support for sandbox execution.

### Automation/CI (non-interactive, no TTY noise)

For scripts and CI, disable Compose pseudo-TTY allocation with `-T`:

```
docker compose run -T --rm openclaw-cli gateway probe
docker compose run -T --rm openclaw-cli devices list --json
```

If your automation exports no Claude session vars, leaving them unset now resolves to empty values by default in `docker-compose.yml` to avoid repeated “variable is not set” warnings.

### Shared-network security note (CLI + gateway)

`openclaw-cli` uses `network_mode: "service:openclaw-gateway"` so CLI commands can reliably reach the gateway over `127.0.0.1` in Docker. Treat this as a shared trust boundary: loopback binding is not isolation between these two containers. If you need stronger separation, run commands from a separate container/host network path instead of the bundled `openclaw-cli` service. To reduce impact if the CLI process is compromised, the compose config drops `NET_RAW`/`NET_ADMIN` and enables `no-new-privileges` on `openclaw-cli`. It writes config/workspace on the host:

*   `~/.openclaw/`
*   `~/.openclaw/workspace`

Running on a VPS? See [Hetzner (Docker VPS)](https://docs.openclaw.ai/install/hetzner).

### Use a remote image (skip local build)

Official pre-built images are published at:

*   [GitHub Container Registry package](https://github.com/openclaw/openclaw/pkgs/container/openclaw)

Use image name `ghcr.io/openclaw/openclaw` (not similarly named Docker Hub images). Common tags:

*   `main` — latest build from `main`
*   `<version>` — release tag builds (for example `2026.2.26`)
*   `latest` — latest stable release tag

### Base image metadata

The main Docker image currently uses:

*   `node:22-bookworm`

The docker image now publishes OCI base-image annotations (sha256 is an example, and points at the pinned multi-arch manifest list for that tag):

*   `org.opencontainers.image.base.name=docker.io/library/node:22-bookworm`
*   `org.opencontainers.image.base.digest=sha256:b501c082306a4f528bc4038cbf2fbb58095d583d0419a259b2114b5ac53d12e9`
*   `org.opencontainers.image.source=https://github.com/openclaw/openclaw`
*   `org.opencontainers.image.url=https://openclaw.ai`
*   `org.opencontainers.image.documentation=https://docs.openclaw.ai/install/docker`
*   `org.opencontainers.image.licenses=MIT`
*   `org.opencontainers.image.title=OpenClaw`
*   `org.opencontainers.image.description=OpenClaw gateway and CLI runtime container image`
*   `org.opencontainers.image.revision=<git-sha>`
*   `org.opencontainers.image.version=<tag-or-main>`
*   `org.opencontainers.image.created=<rfc3339 timestamp>`

Reference: [OCI image annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md) Release context: this repository’s tagged history already uses Bookworm in `v2026.2.22` and earlier 2026 tags (for example `v2026.2.21`, `v2026.2.9`). By default the setup script builds the image from source. To pull a pre-built image instead, set `OPENCLAW_IMAGE` before running the script:

```
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./docker-setup.sh
```

The script detects that `OPENCLAW_IMAGE` is not the default `openclaw:local` and runs `docker pull` instead of `docker build`. Everything else (onboarding, gateway start, token generation) works the same way. `docker-setup.sh` still runs from the repository root because it uses the local `docker-compose.yml` and helper files. `OPENCLAW_IMAGE` skips local image build time; it does not replace the compose/setup workflow.

### Shell Helpers (optional)

For easier day-to-day Docker management, install `ClawDock`:

```
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/shell-helpers/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
```

**Add to your shell config (zsh):**

```
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

Then use `clawdock-start`, `clawdock-stop`, `clawdock-dashboard`, etc. Run `clawdock-help` for all commands. See [`ClawDock` Helper README](https://github.com/openclaw/openclaw/blob/main/scripts/shell-helpers/README.md) for details.

### Manual flow (compose)

```
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

Note: run `docker compose ...` from the repo root. If you enabled `OPENCLAW_EXTRA_MOUNTS` or `OPENCLAW_HOME_VOLUME`, the setup script writes `docker-compose.extra.yml`; include it when running Compose elsewhere:

```
docker compose -f docker-compose.yml -f docker-compose.extra.yml <command>
```

### Control UI token + pairing (Docker)

If you see “unauthorized” or “disconnected (1008): pairing required”, fetch a fresh dashboard link and approve the browser device:

```
docker compose run --rm openclaw-cli dashboard --no-open
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

More detail: [Dashboard](https://docs.openclaw.ai/web/dashboard), [Devices](https://docs.openclaw.ai/cli/devices).

If you want to mount additional host directories into the containers, set `OPENCLAW_EXTRA_MOUNTS` before running `docker-setup.sh`. This accepts a comma-separated list of Docker bind mounts and applies them to both `openclaw-gateway` and `openclaw-cli` by generating `docker-compose.extra.yml`. Example:

```
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notes:

*   Paths must be shared with Docker Desktop on macOS/Windows.
*   Each entry must be `source:target[:options]` with no spaces, tabs, or newlines.
*   If you edit `OPENCLAW_EXTRA_MOUNTS`, rerun `docker-setup.sh` to regenerate the extra compose file.
*   `docker-compose.extra.yml` is generated. Don’t hand-edit it.

### Persist the entire container home (optional)

If you want `/home/node` to persist across container recreation, set a named volume via `OPENCLAW_HOME_VOLUME`. This creates a Docker volume and mounts it at `/home/node`, while keeping the standard config/workspace bind mounts. Use a named volume here (not a bind path); for bind mounts, use `OPENCLAW_EXTRA_MOUNTS`. Example:

```
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

You can combine this with extra mounts:

```
export OPENCLAW_HOME_VOLUME="openclaw_home"
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notes:

*   Named volumes must match `^[A-Za-z0-9][A-Za-z0-9_.-]*$`.
*   If you change `OPENCLAW_HOME_VOLUME`, rerun `docker-setup.sh` to regenerate the extra compose file.
*   The named volume persists until removed with `docker volume rm <name>`.

If you need system packages inside the image (for example, build tools or media libraries), set `OPENCLAW_DOCKER_APT_PACKAGES` before running `docker-setup.sh`. This installs the packages during the image build, so they persist even if the container is deleted. Example:

```
export OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg build-essential"
./docker-setup.sh
```

Notes:

*   This accepts a space-separated list of apt package names.
*   If you change `OPENCLAW_DOCKER_APT_PACKAGES`, rerun `docker-setup.sh` to rebuild the image.

### Pre-install extension dependencies (optional)

Extensions with their own `package.json` (e.g. `diagnostics-otel`, `matrix`, `msteams`) install their npm dependencies on first load. To bake those dependencies into the image instead, set `OPENCLAW_EXTENSIONS` before running `docker-setup.sh`:

```
export OPENCLAW_EXTENSIONS="diagnostics-otel matrix"
./docker-setup.sh
```

Or when building directly:

```
docker build --build-arg OPENCLAW_EXTENSIONS="diagnostics-otel matrix" .
```

Notes:

*   This accepts a space-separated list of extension directory names (under `extensions/`).
*   Only extensions with a `package.json` are affected; lightweight plugins without one are ignored.
*   If you change `OPENCLAW_EXTENSIONS`, rerun `docker-setup.sh` to rebuild the image.

### Power-user / full-featured container (opt-in)

The default Docker image is **security-first** and runs as the non-root `node` user. This keeps the attack surface small, but it means:

*   no system package installs at runtime
*   no Homebrew by default
*   no bundled Chromium/Playwright browsers

If you want a more full-featured container, use these opt-in knobs:

1.  **Persist `/home/node`** so browser downloads and tool caches survive:

```
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

2.  **Bake system deps into the image** (repeatable + persistent):

```
export OPENCLAW_DOCKER_APT_PACKAGES="git curl jq"
./docker-setup.sh
```

3.  **Install Playwright browsers without `npx`** (avoids npm override conflicts):

```
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

If you need Playwright to install system deps, rebuild the image with `OPENCLAW_DOCKER_APT_PACKAGES` instead of using `--with-deps` at runtime.

4.  **Persist Playwright browser downloads**:

*   Set `PLAYWRIGHT_BROWSERS_PATH=/home/node/.cache/ms-playwright` in `docker-compose.yml`.
*   Ensure `/home/node` persists via `OPENCLAW_HOME_VOLUME`, or mount `/home/node/.cache/ms-playwright` via `OPENCLAW_EXTRA_MOUNTS`.

### Permissions + EACCES

The image runs as `node` (uid 1000). If you see permission errors on `/home/node/.openclaw`, make sure your host bind mounts are owned by uid 1000. Example (Linux host):

```
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
```

If you choose to run as root for convenience, you accept the security tradeoff.

### Faster rebuilds (recommended)

To speed up rebuilds, order your Dockerfile so dependency layers are cached. This avoids re-running `pnpm install` unless lockfiles change:

```
FROM node:22-bookworm

# Install Bun (required for build scripts)
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

RUN corepack enable

WORKDIR /app

# Cache dependencies unless package metadata changes
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

### Channel setup (optional)

Use the CLI container to configure channels, then restart the gateway if needed. WhatsApp (QR):

```
docker compose run --rm openclaw-cli channels login
```

Telegram (bot token):

```
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"
```

Discord (bot token):

```
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

Docs: [WhatsApp](https://docs.openclaw.ai/channels/whatsapp), [Telegram](https://docs.openclaw.ai/channels/telegram), [Discord](https://docs.openclaw.ai/channels/discord)

### OpenAI Codex OAuth (headless Docker)

If you pick OpenAI Codex OAuth in the wizard, it opens a browser URL and tries to capture a callback on `http://127.0.0.1:1455/auth/callback`. In Docker or headless setups that callback can show a browser error. Copy the full redirect URL you land on and paste it back into the wizard to finish auth.

### Health checks

Container probe endpoints (no auth required):

```
curl -fsS http://127.0.0.1:18789/healthz
curl -fsS http://127.0.0.1:18789/readyz
```

Aliases: `/health` and `/ready`. `/healthz` is a shallow liveness probe for “the gateway process is up”. `/readyz` stays ready during startup grace, then becomes `503` only if required managed channels are still disconnected after grace or disconnect later. The Docker image includes a built-in `HEALTHCHECK` that pings `/healthz` in the background. In plain terms: Docker keeps checking if OpenClaw is still responsive. If checks keep failing, Docker marks the container as `unhealthy`, and orchestration systems (Docker Compose restart policy, Swarm, Kubernetes, etc.) can automatically restart or replace it. Authenticated deep health snapshot (gateway + channels):

```
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

### E2E smoke test (Docker)

```
scripts/e2e/onboard-docker.sh
```

### QR import smoke test (Docker)

### LAN vs loopback (Docker Compose)

`docker-setup.sh` defaults `OPENCLAW_GATEWAY_BIND=lan` so host access to `http://127.0.0.1:18789` works with Docker port publishing.

*   `lan` (default): host browser + host CLI can reach the published gateway port.
*   `loopback`: only processes inside the container network namespace can reach the gateway directly; host-published port access may fail.

The setup script also pins `gateway.mode=local` after onboarding so Docker CLI commands default to local loopback targeting. Legacy config note: use bind mode values in `gateway.bind` (`lan` / `loopback` / `custom` / `tailnet` / `auto`), not host aliases (`0.0.0.0`, `127.0.0.1`, `localhost`, `::`, `::1`). If you see `Gateway target: ws://172.x.x.x:18789` or repeated `pairing required` errors from Docker CLI commands, run:

```
docker compose run --rm openclaw-cli config set gateway.mode local
docker compose run --rm openclaw-cli config set gateway.bind lan
docker compose run --rm openclaw-cli devices list --url ws://127.0.0.1:18789
```

### Notes

*   Gateway bind defaults to `lan` for container use (`OPENCLAW_GATEWAY_BIND`).
*   Dockerfile CMD uses `--allow-unconfigured`; mounted config with `gateway.mode` not `local` will still start. Override CMD to enforce the guard.
*   The gateway container is the source of truth for sessions (`~/.openclaw/agents/<agentId>/sessions/`).

### Storage model

*   **Persistent host data:** Docker Compose bind-mounts `OPENCLAW_CONFIG_DIR` to `/home/node/.openclaw` and `OPENCLAW_WORKSPACE_DIR` to `/home/node/.openclaw/workspace`, so those paths survive container replacement.
*   **Ephemeral sandbox tmpfs:** when `agents.defaults.sandbox` is enabled, the sandbox containers use `tmpfs` for `/tmp`, `/var/tmp`, and `/run`. Those mounts are separate from the top-level Compose stack and disappear with the sandbox container.
*   **Disk growth hotspots:** watch `media/`, `agents/<agentId>/sessions/sessions.json`, transcript JSONL files, `cron/runs/*.jsonl`, and rolling file logs under `/tmp/openclaw/` (or your configured `logging.file`). If you also run the macOS app outside Docker, its service logs are separate again: `~/.openclaw/logs/gateway.log`, `~/.openclaw/logs/gateway.err.log`, and `/tmp/openclaw/openclaw-gateway.log`.

Deep dive: [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing)

### What it does

When `agents.defaults.sandbox` is enabled, **non-main sessions** run tools inside a Docker container. The gateway stays on your host, but the tool execution is isolated:

*   scope: `"agent"` by default (one container + workspace per agent)
*   scope: `"session"` for per-session isolation
*   per-scope workspace folder mounted at `/workspace`
*   optional agent workspace access (`agents.defaults.sandbox.workspaceAccess`)
*   allow/deny tool policy (deny wins)
*   inbound media is copied into the active sandbox workspace (`media/inbound/*`) so tools can read it (with `workspaceAccess: "rw"`, this lands in the agent workspace)

Warning: `scope: "shared"` disables cross-session isolation. All sessions share one container and one workspace.

### Per-agent sandbox profiles (multi-agent)

If you use multi-agent routing, each agent can override sandbox + tool settings: `agents.list[].sandbox` and `agents.list[].tools` (plus `agents.list[].tools.sandbox.tools`). This lets you run mixed access levels in one gateway:

*   Full access (personal agent)
*   Read-only tools + read-only workspace (family/work agent)
*   No filesystem/shell tools (public agent)

See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for examples, precedence, and troubleshooting.

### Default behavior

*   Image: `openclaw-sandbox:bookworm-slim`
*   One container per agent
*   Agent workspace access: `workspaceAccess: "none"` (default) uses `~/.openclaw/sandboxes`
    *   `"ro"` keeps the sandbox workspace at `/workspace` and mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`)
    *   `"rw"` mounts the agent workspace read/write at `/workspace`
*   Auto-prune: idle > 24h OR age > 7d
*   Network: `none` by default (explicitly opt-in if you need egress)
    *   `host` is blocked.
    *   `container:<id>` is blocked by default (namespace-join risk).
*   Default allow: `exec`, `process`, `read`, `write`, `edit`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
*   Default deny: `browser`, `canvas`, `nodes`, `cron`, `discord`, `gateway`

### Enable sandboxing

If you plan to install packages in `setupCommand`, note:

*   Default `docker.network` is `"none"` (no egress).
*   `docker.network: "host"` is blocked.
*   `docker.network: "container:<id>"` is blocked by default.
*   Break-glass override: `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true`.
*   `readOnlyRoot: true` blocks package installs.
*   `user` must be root for `apt-get` (omit `user` or set `user: "0:0"`). OpenClaw auto-recreates containers when `setupCommand` (or docker config) changes unless the container was **recently used** (within ~5 minutes). Hot containers log a warning with the exact `openclaw sandbox recreate ...` command.

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared (agent is default)
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
        },
        prune: {
          idleHours: 24, // 0 disables idle pruning
          maxAgeDays: 7, // 0 disables max-age pruning
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

Hardening knobs live under `agents.defaults.sandbox.docker`: `network`, `user`, `pidsLimit`, `memory`, `memorySwap`, `cpus`, `ulimits`, `seccompProfile`, `apparmorProfile`, `dns`, `extraHosts`, `dangerouslyAllowContainerNamespaceJoin` (break-glass only). Multi-agent: override `agents.defaults.sandbox.{docker,browser,prune}.*` per agent via `agents.list[].sandbox.{docker,browser,prune}.*` (ignored when `agents.defaults.sandbox.scope` / `agents.list[].sandbox.scope` is `"shared"`).

### Build the default sandbox image

This builds `openclaw-sandbox:bookworm-slim` using `Dockerfile.sandbox`.

### Sandbox common image (optional)

If you want a sandbox image with common build tooling (Node, Go, Rust, etc.), build the common image:

```
scripts/sandbox-common-setup.sh
```

This builds `openclaw-sandbox-common:bookworm-slim`. To use it:

```
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "openclaw-sandbox-common:bookworm-slim" } },
    },
  },
}
```

### Sandbox browser image

To run the browser tool inside the sandbox, build the browser image:

```
scripts/sandbox-browser-setup.sh
```

This builds `openclaw-sandbox-browser:bookworm-slim` using `Dockerfile.sandbox-browser`. The container runs Chromium with CDP enabled and an optional noVNC observer (headful via Xvfb). Notes:

*   Headful (Xvfb) reduces bot blocking vs headless.
*   Headless can still be used by setting `agents.defaults.sandbox.browser.headless=true`.
*   No full desktop environment (GNOME) is needed; Xvfb provides the display.
*   Browser containers default to a dedicated Docker network (`openclaw-sandbox-browser`) instead of global `bridge`.
*   Optional `agents.defaults.sandbox.browser.cdpSourceRange` restricts container-edge CDP ingress by CIDR (for example `172.21.0.1/32`).
*   noVNC observer access is password-protected by default; OpenClaw provides a short-lived observer token URL that serves a local bootstrap page and keeps the password in URL fragment (instead of URL query).
*   Browser container startup defaults are conservative for shared/container workloads, including:
    *   `--remote-debugging-address=127.0.0.1`
    *   `--remote-debugging-port=<derived from OPENCLAW_BROWSER_CDP_PORT>`
    *   `--user-data-dir=${HOME}/.chrome`
    *   `--no-first-run`
    *   `--no-default-browser-check`
    *   `--disable-3d-apis`
    *   `--disable-software-rasterizer`
    *   `--disable-gpu`
    *   `--disable-dev-shm-usage`
    *   `--disable-background-networking`
    *   `--disable-features=TranslateUI`
    *   `--disable-breakpad`
    *   `--disable-crash-reporter`
    *   `--metrics-recording-only`
    *   `--renderer-process-limit=2`
    *   `--no-zygote`
    *   `--disable-extensions`
    *   If `agents.defaults.sandbox.browser.noSandbox` is set, `--no-sandbox` and `--disable-setuid-sandbox` are also appended.
    *   The three graphics hardening flags above are optional. If your workload needs WebGL/3D, set `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` to run without `--disable-3d-apis`, `--disable-software-rasterizer`, and `--disable-gpu`.
    *   Extension behavior is controlled by `--disable-extensions` and can be disabled (enables extensions) via `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` for extension-dependent pages or extensions-heavy workflows.
    *   `--renderer-process-limit=2` is also configurable with `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT`; set `0` to let Chromium choose its default process limit when browser concurrency needs tuning.

Defaults are applied by default in the bundled image. If you need different Chromium flags, use a custom browser image and provide your own entrypoint. Use config:

```
{
  agents: {
    defaults: {
      sandbox: {
        browser: { enabled: true },
      },
    },
  },
}
```

Custom browser image:

```
{
  agents: {
    defaults: {
      sandbox: { browser: { image: "my-openclaw-browser" } },
    },
  },
}
```

When enabled, the agent receives:

*   a sandbox browser control URL (for the `browser` tool)
*   a noVNC URL (if enabled and headless=false)

Remember: if you use an allowlist for tools, add `browser` (and remove it from deny) or the tool remains blocked. Prune rules (`agents.defaults.sandbox.prune`) apply to browser containers too.

### Custom sandbox image

Build your own image and point config to it:

```
docker build -t my-openclaw-sbx -f Dockerfile.sandbox .
```

```
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "my-openclaw-sbx" } },
    },
  },
}
```

### Tool policy (allow/deny)

*   `deny` wins over `allow`.
*   If `allow` is empty: all tools (except deny) are available.
*   If `allow` is non-empty: only tools in `allow` are available (minus deny).

### Pruning strategy

Two knobs:

*   `prune.idleHours`: remove containers not used in X hours (0 = disable)
*   `prune.maxAgeDays`: remove containers older than X days (0 = disable)

Example:

*   Keep busy sessions but cap lifetime: `idleHours: 24`, `maxAgeDays: 7`
*   Never prune: `idleHours: 0`, `maxAgeDays: 0`

### Security notes

*   Hard wall only applies to **tools** (exec/read/write/edit/apply\_patch).
*   Host-only tools like browser/camera/canvas are blocked by default.
*   Allowing `browser` in sandbox **breaks isolation** (browser runs on host).

## Troubleshooting

*   Image missing: build with [`scripts/sandbox-setup.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/sandbox-setup.sh) or set `agents.defaults.sandbox.docker.image`.
*   Container not running: it will auto-create per session on demand.
*   Permission errors in sandbox: set `docker.user` to a UID:GID that matches your mounted workspace ownership (or chown the workspace folder).
*   Custom tools not found: OpenClaw runs commands with `sh -lc` (login shell), which sources `/etc/profile` and may reset PATH. Set `docker.env.PATH` to prepend your custom tool paths (e.g., `/custom/bin:/usr/local/share/npm-global/bin`), or add a script under `/etc/profile.d/` in your Dockerfile.

---

<!-- SOURCE: https://docs.openclaw.ai/install/updating -->

# Updating - OpenClaw

OpenClaw is moving fast (pre “1.0”). Treat updates like shipping infra: update → run checks → restart (or use `openclaw update`, which restarts) → verify.

## Recommended: re-run the website installer (upgrade in place)

The **preferred** update path is to re-run the installer from the website. It detects existing installs, upgrades in place, and runs `openclaw doctor` when needed.

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

Notes:

*   Add `--no-onboard` if you don’t want the onboarding wizard to run again.
*   For **source installs**, use:
    
    ```
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
    ```
    
    The installer will `git pull --rebase` **only** if the repo is clean.
*   For **global installs**, the script uses `npm install -g openclaw@latest` under the hood.
*   Legacy note: `clawdbot` remains available as a compatibility shim.

## Before you update

*   Know how you installed: **global** (npm/pnpm) vs **from source** (git clone).
*   Know how your Gateway is running: **foreground terminal** vs **supervised service** (launchd/systemd).
*   Snapshot your tailoring:
    *   Config: `~/.openclaw/openclaw.json`
    *   Credentials: `~/.openclaw/credentials/`
    *   Workspace: `~/.openclaw/workspace`

## Update (global install)

Global install (pick one):

```
pnpm add -g openclaw@latest
```

We do **not** recommend Bun for the Gateway runtime (WhatsApp/Telegram bugs). To switch update channels (git + npm installs):

```
openclaw update --channel beta
openclaw update --channel dev
openclaw update --channel stable
```

Use `--tag <dist-tag|version>` for a one-off install tag/version. See [Development channels](https://docs.openclaw.ai/install/development-channels) for channel semantics and release notes. Note: on npm installs, the gateway logs an update hint on startup (checks the current channel tag). Disable via `update.checkOnStart: false`.

### Core auto-updater (optional)

Auto-updater is **off by default** and is a core Gateway feature (not a plugin).

```
{
  "update": {
    "channel": "stable",
    "auto": {
      "enabled": true,
      "stableDelayHours": 6,
      "stableJitterHours": 12,
      "betaCheckIntervalHours": 1
    }
  }
}
```

Behavior:

*   `stable`: when a new version is seen, OpenClaw waits `stableDelayHours` and then applies a deterministic per-install jitter in `stableJitterHours` (spread rollout).
*   `beta`: checks on `betaCheckIntervalHours` cadence (default: hourly) and applies when an update is available.
*   `dev`: no automatic apply; use manual `openclaw update`.

Use `openclaw update --dry-run` to preview update actions before enabling automation. Then:

```
openclaw doctor
openclaw gateway restart
openclaw health
```

Notes:

*   If your Gateway runs as a service, `openclaw gateway restart` is preferred over killing PIDs.
*   If you’re pinned to a specific version, see “Rollback / pinning” below.

## Update (`openclaw update`)

For **source installs** (git checkout), prefer:

It runs a safe-ish update flow:

*   Requires a clean worktree.
*   Switches to the selected channel (tag or branch).
*   Fetches + rebases against the configured upstream (dev channel).
*   Installs deps, builds, builds the Control UI, and runs `openclaw doctor`.
*   Restarts the gateway by default (use `--no-restart` to skip).

If you installed via **npm/pnpm** (no git metadata), `openclaw update` will try to update via your package manager. If it can’t detect the install, use “Update (global install)” instead.

## Update (Control UI / RPC)

The Control UI has **Update & Restart** (RPC: `update.run`). It:

1.  Runs the same source-update flow as `openclaw update` (git checkout only).
2.  Writes a restart sentinel with a structured report (stdout/stderr tail).
3.  Restarts the gateway and pings the last active session with the report.

If the rebase fails, the gateway aborts and restarts without applying the update.

## Update (from source)

From the repo checkout: Preferred:

Manual (equivalent-ish):

```
git pull
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw doctor
openclaw health
```

Notes:

*   `pnpm build` matters when you run the packaged `openclaw` binary ([`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs)) or use Node to run `dist/`.
*   If you run from a repo checkout without a global install, use `pnpm openclaw ...` for CLI commands.
*   If you run directly from TypeScript (`pnpm openclaw ...`), a rebuild is usually unnecessary, but **config migrations still apply** → run doctor.
*   Switching between global and git installs is easy: install the other flavor, then run `openclaw doctor` so the gateway service entrypoint is rewritten to the current install.

## Always Run: `openclaw doctor`

Doctor is the “safe update” command. It’s intentionally boring: repair + migrate + warn. Note: if you’re on a **source install** (git checkout), `openclaw doctor` will offer to run `openclaw update` first. Typical things it does:

*   Migrate deprecated config keys / legacy config file locations.
*   Audit DM policies and warn on risky “open” settings.
*   Check Gateway health and can offer to restart.
*   Detect and migrate older gateway services (launchd/systemd; legacy schtasks) to current OpenClaw services.
*   On Linux, ensure systemd user lingering (so the Gateway survives logout).

Details: [Doctor](https://docs.openclaw.ai/gateway/doctor)

## Start / stop / restart the Gateway

CLI (works regardless of OS):

```
openclaw gateway status
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789
openclaw logs --follow
```

If you’re supervised:

*   macOS launchd (app-bundled LaunchAgent): `launchctl kickstart -k gui/$UID/ai.openclaw.gateway` (use `ai.openclaw.<profile>`; legacy `com.openclaw.*` still works)
*   Linux systemd user service: `systemctl --user restart openclaw-gateway[-<profile>].service`
*   Windows (WSL2): `systemctl --user restart openclaw-gateway[-<profile>].service`
    *   `launchctl`/`systemctl` only work if the service is installed; otherwise run `openclaw gateway install`.

Runbook + exact service labels: [Gateway runbook](https://docs.openclaw.ai/gateway)

## Rollback / pinning (when something breaks)

### Pin (global install)

Install a known-good version (replace `<version>` with the last working one):

```
npm i -g openclaw@<version>
```

```
pnpm add -g openclaw@<version>
```

Tip: to see the current published version, run `npm view openclaw version`. Then restart + re-run doctor:

```
openclaw doctor
openclaw gateway restart
```

### Pin (source) by date

Pick a commit from a date (example: “state of main as of 2026-01-01”):

```
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
```

Then reinstall deps + restart:

```
pnpm install
pnpm build
openclaw gateway restart
```

If you want to go back to latest later:

```
git checkout main
git pull
```

## If you’re stuck

*   Run `openclaw doctor` again and read the output carefully (it often tells you the fix).
*   Check: [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   Ask in Discord: [https://discord.gg/clawd](https://discord.gg/clawd)

---

<!-- SOURCE: https://docs.openclaw.ai/install/bun -->

# Bun (Experimental) - OpenClaw

Goal: run this repo with **Bun** (optional, not recommended for WhatsApp/Telegram) without diverging from pnpm workflows. ⚠️ **Not recommended for Gateway runtime** (WhatsApp/Telegram bugs). Use Node for production.

## Status

*   Bun is an optional local runtime for running TypeScript directly (`bun run …`, `bun --watch …`).
*   `pnpm` is the default for builds and remains fully supported (and used by some docs tooling).
*   Bun cannot use `pnpm-lock.yaml` and will ignore it.

## Install

Default:

Note: `bun.lock`/`bun.lockb` are gitignored, so there’s no repo churn either way. If you want _no lockfile writes_:

## Build / Test (Bun)

```
bun run build
bun run vitest run
```

## Bun lifecycle scripts (blocked by default)

Bun may block dependency lifecycle scripts unless explicitly trusted (`bun pm untrusted` / `bun pm trust`). For this repo, the commonly blocked scripts are not required:

*   `@whiskeysockets/baileys` `preinstall`: checks Node major >= 20 (we run Node 22+).
*   `protobufjs` `postinstall`: emits warnings about incompatible version schemes (no build artifacts).

If you hit a real runtime issue that requires these scripts, trust them explicitly:

```
bun pm trust @whiskeysockets/baileys protobufjs
```

## Caveats

*   Some scripts still hardcode pnpm (e.g. `docs:build`, `ui:*`, `protocol:check`). Run those via pnpm for now.

---

<!-- SOURCE: https://docs.openclaw.ai/install/migrating -->

# Migration Guide - OpenClaw

## Migrating OpenClaw to a new machine

This guide migrates a OpenClaw Gateway from one machine to another **without redoing onboarding**. The migration is simple conceptually:

*   Copy the **state directory** (`$OPENCLAW_STATE_DIR`, default: `~/.openclaw/`) — this includes config, auth, sessions, and channel state.
*   Copy your **workspace** (`~/.openclaw/workspace/` by default) — this includes your agent files (memory, prompts, etc.).

But there are common footguns around **profiles**, **permissions**, and **partial copies**.

## Before you start (what you are migrating)

### 1) Identify your state directory

Most installs use the default:

*   **State dir:** `~/.openclaw/`

But it may be different if you use:

*   `--profile <name>` (often becomes `~/.openclaw-<profile>/`)
*   `OPENCLAW_STATE_DIR=/some/path`

If you’re not sure, run on the **old** machine:

Look for mentions of `OPENCLAW_STATE_DIR` / profile in the output. If you run multiple gateways, repeat for each profile.

### 2) Identify your workspace

Common defaults:

*   `~/.openclaw/workspace/` (recommended workspace)
*   a custom folder you created

Your workspace is where files like `MEMORY.md`, `USER.md`, and `memory/*.md` live.

### 3) Understand what you will preserve

If you copy **both** the state dir and workspace, you keep:

*   Gateway configuration (`openclaw.json`)
*   Auth profiles / API keys / OAuth tokens
*   Session history + agent state
*   Channel state (e.g. WhatsApp login/session)
*   Your workspace files (memory, skills notes, etc.)

If you copy **only** the workspace (e.g., via Git), you do **not** preserve:

*   sessions
*   credentials
*   channel logins

Those live under `$OPENCLAW_STATE_DIR`.

## Migration steps (recommended)

### Step 0 — Make a backup (old machine)

On the **old** machine, stop the gateway first so files aren’t changing mid-copy:

(Optional but recommended) archive the state dir and workspace:

```
# Adjust paths if you use a profile or custom locations
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

If you have multiple profiles/state dirs (e.g. `~/.openclaw-main`, `~/.openclaw-work`), archive each.

### Step 1 — Install OpenClaw on the new machine

On the **new** machine, install the CLI (and Node if needed):

*   See: [Install](https://docs.openclaw.ai/install)

At this stage, it’s OK if onboarding creates a fresh `~/.openclaw/` — you will overwrite it in the next step.

### Step 2 — Copy the state dir + workspace to the new machine

Copy **both**:

*   `$OPENCLAW_STATE_DIR` (default `~/.openclaw/`)
*   your workspace (default `~/.openclaw/workspace/`)

Common approaches:

*   `scp` the tarballs and extract
*   `rsync -a` over SSH
*   external drive

After copying, ensure:

*   Hidden directories were included (e.g. `.openclaw/`)
*   File ownership is correct for the user running the gateway

### Step 3 — Run Doctor (migrations + service repair)

On the **new** machine:

Doctor is the “safe boring” command. It repairs services, applies config migrations, and warns about mismatches. Then:

```
openclaw gateway restart
openclaw status
```

### Footgun: profile / state-dir mismatch

If you ran the old gateway with a profile (or `OPENCLAW_STATE_DIR`), and the new gateway uses a different one, you’ll see symptoms like:

*   config changes not taking effect
*   channels missing / logged out
*   empty session history

Fix: run the gateway/service using the **same** profile/state dir you migrated, then rerun:

### Footgun: copying only `openclaw.json`

`openclaw.json` is not enough. Many providers store state under:

*   `$OPENCLAW_STATE_DIR/credentials/`
*   `$OPENCLAW_STATE_DIR/agents/<agentId>/...`

Always migrate the entire `$OPENCLAW_STATE_DIR` folder.

### Footgun: permissions / ownership

If you copied as root or changed users, the gateway may fail to read credentials/sessions. Fix: ensure the state dir + workspace are owned by the user running the gateway.

### Footgun: migrating between remote/local modes

*   If your UI (WebUI/TUI) points at a **remote** gateway, the remote host owns the session store + workspace.
*   Migrating your laptop won’t move the remote gateway’s state.

If you’re in remote mode, migrate the **gateway host**.

### Footgun: secrets in backups

`$OPENCLAW_STATE_DIR` contains secrets (API keys, OAuth tokens, WhatsApp creds). Treat backups like production secrets:

*   store encrypted
*   avoid sharing over insecure channels
*   rotate keys if you suspect exposure

## Verification checklist

On the new machine, confirm:

*   `openclaw status` shows the gateway running
*   Your channels are still connected (e.g. WhatsApp doesn’t require re-pair)
*   The dashboard opens and shows existing sessions
*   Your workspace files (memory, configs) are present

*   [Doctor](https://docs.openclaw.ai/gateway/doctor)
*   [Gateway troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   [Where does OpenClaw store its data?](https://docs.openclaw.ai/help/faq#where-does-openclaw-store-its-data)

---

<!-- SOURCE: https://docs.openclaw.ai/install/uninstall -->

# Uninstall - OpenClaw

Two paths:

*   **Easy path** if `openclaw` is still installed.
*   **Manual service removal** if the CLI is gone but the service is still running.

## Easy path (CLI still installed)

Recommended: use the built-in uninstaller:

Non-interactive (automation / npx):

```
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

Manual steps (same result):

1.  Stop the gateway service:

2.  Uninstall the gateway service (launchd/systemd/schtasks):

```
openclaw gateway uninstall
```

3.  Delete state + config:

```
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

If you set `OPENCLAW_CONFIG_PATH` to a custom location outside the state dir, delete that file too.

4.  Delete your workspace (optional, removes agent files):

```
rm -rf ~/.openclaw/workspace
```

5.  Remove the CLI install (pick the one you used):

```
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6.  If you installed the macOS app:

```
rm -rf /Applications/OpenClaw.app
```

Notes:

*   If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for each state dir (defaults are `~/.openclaw-<profile>`).
*   In remote mode, the state dir lives on the **gateway host**, so run steps 1-4 there too.

## Manual service removal (CLI not installed)

Use this if the gateway service keeps running but `openclaw` is missing.

### macOS (launchd)

Default label is `ai.openclaw.gateway` (or `ai.openclaw.<profile>`; legacy `com.openclaw.*` may still exist):

```
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

If you used a profile, replace the label and plist name with `ai.openclaw.<profile>`. Remove any legacy `com.openclaw.*` plists if present.

### Linux (systemd user unit)

Default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`):

```
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Scheduled Task)

Default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`). The task script lives under your state dir.

```
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.

## Normal install vs source checkout

### Normal install (install.sh / npm / pnpm / bun)

If you used `https://openclaw.ai/install.sh` or `install.ps1`, the CLI was installed with `npm install -g openclaw@latest`. Remove it with `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g` if you installed that way).

### Source checkout (git clone)

If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`):

1.  Uninstall the gateway service **before** deleting the repo (use the easy path above or manual service removal).
2.  Delete the repo directory.
3.  Remove state + workspace as shown above.

---

<!-- SOURCE: https://docs.openclaw.ai/install/node -->

# Node.js - OpenClaw

OpenClaw requires **Node 22 or newer**. The [installer script](https://docs.openclaw.ai/install#install-methods) will detect and install Node automatically — this page is for when you want to set up Node yourself and make sure everything is wired up correctly (versions, PATH, global installs).

## Check your version

If this prints `v22.x.x` or higher, you’re good. If Node isn’t installed or the version is too old, pick an install method below.

## Install Node

*   macOS
    
*   Linux
    
*   Windows
    

**Homebrew** (recommended):

Or download the macOS installer from [nodejs.org](https://nodejs.org/).

**Ubuntu / Debian:**

```
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora / RHEL:**

Or use a version manager (see below).

**winget** (recommended):

```
winget install OpenJS.NodeJS.LTS
```

**Chocolatey:**

Or download the Windows installer from [nodejs.org](https://nodejs.org/).

Using a version manager (nvm, fnm, mise, asdf)

Version managers let you switch between Node versions easily. Popular options:

*   [**fnm**](https://github.com/Schniz/fnm) — fast, cross-platform
*   [**nvm**](https://github.com/nvm-sh/nvm) — widely used on macOS/Linux
*   [**mise**](https://mise.jdx.dev/) — polyglot (Node, Python, Ruby, etc.)

Example with fnm:

```
fnm install 22
fnm use 22
```

## Troubleshooting

### `openclaw: command not found`

This almost always means npm’s global bin directory isn’t on your PATH.

### Permission errors on `npm install -g` (Linux)

If you see `EACCES` errors, switch npm’s global prefix to a user-writable directory:

```
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"
```

Add the `export PATH=...` line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

---

<!-- SOURCE: https://docs.openclaw.ai/install/development-channels -->

# Development Channels - OpenClaw

Last updated: 2026-01-21 OpenClaw ships three update channels:

*   **stable**: npm dist-tag `latest`.
*   **beta**: npm dist-tag `beta` (builds under test).
*   **dev**: moving head of `main` (git). npm dist-tag: `dev` (when published).

We ship builds to **beta**, test them, then **promote a vetted build to `latest`** without changing the version number — dist-tags are the source of truth for npm installs.

## Switching channels

Git checkout:

```
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

*   `stable`/`beta` check out the latest matching tag (often the same tag).
*   `dev` switches to `main` and rebases on the upstream.

npm/pnpm global install:

```
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

This updates via the corresponding npm dist-tag (`latest`, `beta`, `dev`). When you **explicitly** switch channels with `--channel`, OpenClaw also aligns the install method:

*   `dev` ensures a git checkout (default `~/openclaw`, override with `OPENCLAW_GIT_DIR`), updates it, and installs the global CLI from that checkout.
*   `stable`/`beta` installs from npm using the matching dist-tag.

Tip: if you want stable + dev in parallel, keep two clones and point your gateway at the stable one.

## Plugins and channels

When you switch channels with `openclaw update`, OpenClaw also syncs plugin sources:

*   `dev` prefers bundled plugins from the git checkout.
*   `stable` and `beta` restore npm-installed plugin packages.

## Tagging best practices

*   Tag releases you want git checkouts to land on (`vYYYY.M.D` for stable, `vYYYY.M.D-beta.N` for beta).
*   `vYYYY.M.D.beta.N` is also recognized for compatibility, but prefer `-beta.N`.
*   Legacy `vYYYY.M.D-<patch>` tags are still recognized as stable (non-beta).
*   Keep tags immutable: never move or reuse a tag.
*   npm dist-tags remain the source of truth for npm installs:
    *   `latest` → stable
    *   `beta` → candidate build
    *   `dev` → main snapshot (optional)

## macOS app availability

Beta and dev builds may **not** include a macOS app release. That’s OK:

*   The git tag and npm dist-tag can still be published.
*   Call out “no macOS build for this beta” in release notes or changelog.



---

<!-- SOURCE: https://docs.openclaw.ai/install -->

# Install - OpenClaw

Already followed [Getting Started](https://docs.openclaw.ai/start/getting-started)? You’re all set — this page is for alternative install methods, platform-specific instructions, and maintenance.

## System requirements

*   **[Node 22+](https://docs.openclaw.ai/install/node)** (the [installer script](https://docs.openclaw.ai/install#install-methods) will install it if missing)
*   macOS, Linux, or Windows
*   `pnpm` only if you build from source

## Install methods

## Other install methods

## After install

Verify everything is working:

```
openclaw doctor         # check for config issues
openclaw status         # gateway status
openclaw dashboard      # open the browser UI
```

If you need custom runtime paths, use:

*   `OPENCLAW_HOME` for home-directory based internal paths
*   `OPENCLAW_STATE_DIR` for mutable state location
*   `OPENCLAW_CONFIG_PATH` for config file location

See [Environment vars](https://docs.openclaw.ai/help/environment) for precedence and full details.

## Troubleshooting: `openclaw` not found

PATH diagnosis and fix

Quick diagnosis:

```
node -v
npm -v
npm prefix -g
echo "$PATH"
```

If `$(npm prefix -g)/bin` (macOS/Linux) or `$(npm prefix -g)` (Windows) is **not** in your `$PATH`, your shell can’t find global npm binaries (including `openclaw`).Fix — add it to your shell startup file (`~/.zshrc` or `~/.bashrc`):

```
export PATH="$(npm prefix -g)/bin:$PATH"
```

On Windows, add the output of `npm prefix -g` to your PATH.Then open a new terminal (or `rehash` in zsh / `hash -r` in bash).

## Update / uninstall

