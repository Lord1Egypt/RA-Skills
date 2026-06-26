# Skills

Source: https://docs.openclaw.ai/platforms/mac/skills

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationmacOS companion appSkillsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [Skills (macOS)](#skills-macos)
- [Data source](#data-source)
- [Install actions](#install-actions)
- [Env/API keys](#env%2Fapi-keys)
- [Remote mode](#remote-mode)

​Skills (macOS)
The macOS app surfaces OpenClaw skills via the gateway; it does not parse skills locally.
​Data source

- `skills.status` (gateway) returns all skills plus eligibility and missing requirements
(including allowlist blocks for bundled skills).

- Requirements are derived from `metadata.openclaw.requires` in each `SKILL.md`.

​Install actions

- `metadata.openclaw.install` defines install options (brew/node/go/uv).

- The app calls `skills.install` to run installers on the gateway host.

- The gateway surfaces only one preferred installer when multiple are provided
(brew when available, otherwise node manager from `skills.install`, default npm).

​Env/API keys

- The app stores keys in `~/.openclaw/openclaw.json` under `skills.entries.<skillKey>`.

- `skills.update` patches `enabled`, `apiKey`, and `env`.

​Remote mode

- Install + config updates happen on the gateway host (not the local Mac).

macOS IPCPeekaboo Bridge⌘I