# Polls

Source: https://docs.openclaw.ai/automation/poll

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationAutomationPollsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
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
- [Polls](#polls)
- [Supported channels](#supported-channels)
- [CLI](#cli)
- [Gateway RPC](#gateway-rpc)
- [Channel differences](#channel-differences)
- [Agent tool (Message)](#agent-tool-message)

​Polls
​Supported channels

- WhatsApp (web channel)

- Discord

- MS Teams (Adaptive Cards)

​CLI
Copy```
# WhatsApp
openclaw message poll --target +15555550123 \
  --poll-question "Lunch today?" --poll-option "Yes" --poll-option "No" --poll-option "Maybe"
openclaw message poll --target 123456789@g.us \
  --poll-question "Meeting time?" --poll-option "10am" --poll-option "2pm" --poll-option "4pm" --poll-multi

# Discord
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Snack?" --poll-option "Pizza" --poll-option "Sushi"
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Plan?" --poll-option "A" --poll-option "B" --poll-duration-hours 48

# MS Teams
openclaw message poll --channel msteams --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" --poll-option "Pizza" --poll-option "Sushi"

```

Options:

- `--channel`: `whatsapp` (default), `discord`, or `msteams`

- `--poll-multi`: allow selecting multiple options

- `--poll-duration-hours`: Discord-only (defaults to 24 when omitted)

​Gateway RPC
Method: `poll`
Params:

- `to` (string, required)

- `question` (string, required)

- `options` (string[], required)

- `maxSelections` (number, optional)

- `durationHours` (number, optional)

- `channel` (string, optional, default: `whatsapp`)

- `idempotencyKey` (string, required)

​Channel differences

- WhatsApp: 2-12 options, `maxSelections` must be within option count, ignores `durationHours`.

- Discord: 2-10 options, `durationHours` clamped to 1-768 hours (default 24). `maxSelections > 1` enables multi-select; Discord does not support a strict selection count.

- MS Teams: Adaptive Card polls (OpenClaw-managed). No native poll API; `durationHours` is ignored.

​Agent tool (Message)
Use the `message` tool with `poll` action (`to`, `pollQuestion`, `pollOption`, optional `pollMulti`, `pollDurationHours`, `channel`).
Note: Discord has no “pick exactly N” mode; `pollMulti` maps to multi-select.
Teams polls are rendered as Adaptive Cards and require the gateway to stay online
to record votes in `~/.openclaw/msteams-polls.json`.Gmail PubSubAuth Monitoring⌘I