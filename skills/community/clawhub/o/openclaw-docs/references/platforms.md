# Platforms

Source: https://docs.openclaw.ai/platforms

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationPlatforms overviewPlatformsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [Platforms](#platforms)
- [Choose your OS](#choose-your-os)
- [VPS & hosting](#vps-%26-hosting)
- [Common links](#common-links)
- [Gateway service install (CLI)](#gateway-service-install-cli)

​Platforms
OpenClaw core is written in TypeScript. **Node is the recommended runtime**.
Bun is not recommended for the Gateway (WhatsApp/Telegram bugs).
Companion apps exist for macOS (menu bar app) and mobile nodes (iOS/Android). Windows and
Linux companion apps are planned, but the Gateway is fully supported today.
Native companion apps for Windows are also planned; the Gateway is recommended via WSL2.
​Choose your OS

- macOS: [macOS](/platforms/macos)

- iOS: [iOS](/platforms/ios)

- Android: [Android](/platforms/android)

- Windows: [Windows](/platforms/windows)

- Linux: [Linux](/platforms/linux)

​VPS & hosting

- VPS hub: [VPS hosting](/vps)

- Fly.io: [Fly.io](/install/fly)

- Hetzner (Docker): [Hetzner](/install/hetzner)

- GCP (Compute Engine): [GCP](/install/gcp)

- exe.dev (VM + HTTPS proxy): [exe.dev](/install/exe-dev)

​Common links

- Install guide: [Getting Started](/start/getting-started)

- Gateway runbook: [Gateway](/gateway)

- Gateway configuration: [Configuration](/gateway/configuration)

- Service status: `openclaw gateway status`

​Gateway service install (CLI)
Use one of these (all supported):

- Wizard (recommended): `openclaw onboard --install-daemon`

- Direct: `openclaw gateway install`

- Configure flow: `openclaw configure` → select **Gateway service**

- Repair/migrate: `openclaw doctor` (offers to install or fix the service)

The service target depends on OS:

- macOS: LaunchAgent (`bot.molt.gateway` or `bot.molt.<profile>`; legacy `com.openclaw.*`)

- Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`)

macOS App⌘I