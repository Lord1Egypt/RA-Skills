# Auth Monitoring

Source: https://docs.openclaw.ai/automation/auth-monitoring

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationAutomationAuth MonitoringGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Tools
Built-in tools
LobsterLLM TaskExec ToolWeb Toolsapply_patch ToolElevated ModeThinking LevelsReactions
Browser
Browser (OpenClaw-managed)Browser LoginChrome ExtensionBrowser Troubleshooting
Agent coordination
Agent SendSub-AgentsMulti-Agent Sandbox & Tools
Skills
Slash CommandsSkillsSkills ConfigClawHubPlugins
Extensions
Voice Call PluginZalo Personal Plugin
Automation
HooksCron JobsCron vs HeartbeatAutomation TroubleshootingWebhooksGmail PubSubPollsAuth Monitoring
Media and devices
NodesNode TroubleshootingImage and Media SupportAudio and Voice NotesCamera CaptureTalk ModeVoice WakeLocation Command
On this page
- [Auth monitoring](#auth-monitoring)
- [Preferred: CLI check (portable)](#preferred-cli-check-portable)
- [Optional scripts (ops / phone workflows)](#optional-scripts-ops-%2F-phone-workflows)

​Auth monitoring
OpenClaw exposes OAuth expiry health via `openclaw models status`. Use that for
automation and alerting; scripts are optional extras for phone workflows.
​Preferred: CLI check (portable)
Copy```
openclaw models status --check

```

Exit codes:

- `0`: OK

- `1`: expired or missing credentials

- `2`: expiring soon (within 24h)

This works in cron/systemd and requires no extra scripts.
​Optional scripts (ops / phone workflows)
These live under `scripts/` and are **optional**. They assume SSH access to the
gateway host and are tuned for systemd + Termux.

- `scripts/claude-auth-status.sh` now uses `openclaw models status --json` as the
source of truth (falling back to direct file reads if the CLI is unavailable),
so keep `openclaw` on `PATH` for timers.

- `scripts/auth-monitor.sh`: cron/systemd timer target; sends alerts (ntfy or phone).

- `scripts/systemd/openclaw-auth-monitor.{service,timer}`: systemd user timer.

- `scripts/claude-auth-status.sh`: Claude Code + OpenClaw auth checker (full/json/simple).

- `scripts/mobile-reauth.sh`: guided re‑auth flow over SSH.

- `scripts/termux-quick-auth.sh`: one‑tap widget status + open auth URL.

- `scripts/termux-auth-widget.sh`: full guided widget flow.

- `scripts/termux-sync-widget.sh`: sync Claude Code creds → OpenClaw.

If you don’t need phone automation or systemd timers, skip these scripts.PollsNodes⌘I