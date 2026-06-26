# Platforms - Desktop (Linux/Windows)

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 2

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/linux -->

# Linux App - OpenClaw

The Gateway is fully supported on Linux. **Node is the recommended runtime**. Bun is not recommended for the Gateway (WhatsApp/Telegram bugs). Native Linux companion apps are planned. Contributions are welcome if you want to help build one.

## Beginner quick path (VPS)

1.  Install Node 22+
2.  `npm i -g openclaw@latest`
3.  `openclaw onboard --install-daemon`
4.  From your laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5.  Open `http://127.0.0.1:18789/` and paste your token

Step-by-step VPS guide: [exe.dev](https://docs.openclaw.ai/install/exe-dev)

## Install

*   [Getting Started](https://docs.openclaw.ai/start/getting-started)
*   [Install & updates](https://docs.openclaw.ai/install/updating)
*   Optional flows: [Bun (experimental)](https://docs.openclaw.ai/install/bun), [Nix](https://docs.openclaw.ai/install/nix), [Docker](https://docs.openclaw.ai/install/docker)

## Gateway

*   [Gateway runbook](https://docs.openclaw.ai/gateway)
*   [Configuration](https://docs.openclaw.ai/gateway/configuration)

## Gateway service install (CLI)

Use one of these:

```
openclaw onboard --install-daemon
```

Or:

Or:

Select **Gateway service** when prompted. Repair/migrate:

## System control (systemd user unit)

OpenClaw installs a systemd **user** service by default. Use a **system** service for shared or always-on servers. The full unit example and guidance live in the [Gateway runbook](https://docs.openclaw.ai/gateway). Minimal setup: Create `~/.config/systemd/user/openclaw-gateway[-<profile>].service`:

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Enable it:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/windows -->

# Windows (WSL2) - OpenClaw

OpenClaw on Windows is recommended **via WSL2** (Ubuntu recommended). The CLI + Gateway run inside Linux, which keeps the runtime consistent and makes tooling far more compatible (Node/Bun/pnpm, Linux binaries, skills). Native Windows might be trickier. WSL2 gives you the full Linux experience — one command to install: `wsl --install`. Native Windows companion apps are planned.

## Install (WSL2)

*   [Getting Started](https://docs.openclaw.ai/start/getting-started) (use inside WSL)
*   [Install & updates](https://docs.openclaw.ai/install/updating)
*   Official WSL2 guide (Microsoft): [https://learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/windows/wsl/install)

## Gateway

*   [Gateway runbook](https://docs.openclaw.ai/gateway)
*   [Configuration](https://docs.openclaw.ai/gateway/configuration)

## Gateway service install (CLI)

Inside WSL2:

```
openclaw onboard --install-daemon
```

Or:

Or:

Select **Gateway service** when prompted. Repair/migrate:

## Gateway auto-start before Windows login

For headless setups, ensure the full boot chain runs even when no one logs into Windows.

### 1) Keep user services running without login

Inside WSL:

```
sudo loginctl enable-linger "$(whoami)"
```

### 2) Install the OpenClaw gateway user service

Inside WSL:

### 3) Start WSL automatically at Windows boot

In PowerShell as Administrator:

```
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

Replace `Ubuntu` with your distro name from:

### Verify startup chain

After a reboot (before Windows sign-in), check from WSL:

```
systemctl --user is-enabled openclaw-gateway
systemctl --user status openclaw-gateway --no-pager
```

## Advanced: expose WSL services over LAN (portproxy)

WSL has its own virtual network. If another machine needs to reach a service running **inside WSL** (SSH, a local TTS server, or the Gateway), you must forward a Windows port to the current WSL IP. The WSL IP changes after restarts, so you may need to refresh the forwarding rule. Example (PowerShell **as Administrator**):

```
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort
```

Allow the port through Windows Firewall (one-time):

```
New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Refresh the portproxy after WSL restarts:

```
netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null
netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `
  connectaddress=$WslIp connectport=$TargetPort | Out-Null
```

Notes:

*   SSH from another machine targets the **Windows host IP** (example: `ssh user@windows-host -p 2222`).
*   Remote nodes must point at a **reachable** Gateway URL (not `127.0.0.1`); use `openclaw status --all` to confirm.
*   Use `listenaddress=0.0.0.0` for LAN access; `127.0.0.1` keeps it local only.
*   If you want this automatic, register a Scheduled Task to run the refresh step at login.

## Step-by-step WSL2 install

### 1) Install WSL2 + Ubuntu

Open PowerShell (Admin):

```
wsl --install
# Or pick a distro explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```

Reboot if Windows asks.

### 2) Enable systemd (required for gateway install)

In your WSL terminal:

```
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Then from PowerShell:

Re-open Ubuntu, then verify:

### 3) Install OpenClaw (inside WSL)

Follow the Linux Getting Started flow inside WSL:

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard
```

Full guide: [Getting Started](https://docs.openclaw.ai/start/getting-started)

## Windows companion app

We do not have a Windows companion app yet. Contributions are welcome if you want contributions to make it happen.

