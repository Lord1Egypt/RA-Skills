# Linux App

Source: https://docs.openclaw.ai/platforms/linux

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationPlatforms overviewLinux AppGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [Linux App](#linux-app)
- [Beginner quick path (VPS)](#beginner-quick-path-vps)
- [Install](#install)
- [Gateway](#gateway)
- [Gateway service install (CLI)](#gateway-service-install-cli)
- [System control (systemd user unit)](#system-control-systemd-user-unit)

​Linux App
The Gateway is fully supported on Linux. **Node is the recommended runtime**.
Bun is not recommended for the Gateway (WhatsApp/Telegram bugs).
Native Linux companion apps are planned. Contributions are welcome if you want to help build one.
​Beginner quick path (VPS)

- Install Node 22+

- `npm i -g openclaw@latest`

- `openclaw onboard --install-daemon`

- From your laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`

- Open `http://127.0.0.1:18789/` and paste your token

Step-by-step VPS guide: [exe.dev](/install/exe-dev)
​Install

- [Getting Started](/start/getting-started)

- [Install & updates](/install/updating)

- Optional flows: [Bun (experimental)](/install/bun), [Nix](/install/nix), [Docker](/install/docker)

​Gateway

- [Gateway runbook](/gateway)

- [Configuration](/gateway/configuration)

​Gateway service install (CLI)
Use one of these:
Copy```
openclaw onboard --install-daemon

```

Or:
Copy```
openclaw gateway install

```

Or:
Copy```
openclaw configure

```

Select **Gateway service** when prompted.
Repair/migrate:
Copy```
openclaw doctor

```

​System control (systemd user unit)
OpenClaw installs a systemd **user** service by default. Use a **system**
service for shared or always-on servers. The full unit example and guidance
live in the [Gateway runbook](/gateway).
Minimal setup:
Create `~/.config/systemd/user/openclaw-gateway[-<profile>].service`:
Copy```
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
Copy```
systemctl --user enable --now openclaw-gateway[-<profile>].service

```

macOS AppWindows (WSL2)⌘I