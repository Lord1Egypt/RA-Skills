# Reactions

Source: https://docs.openclaw.ai/tools/reactions

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationBuilt-in toolsReactionsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
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
- [Reaction tooling](#reaction-tooling)

​Reaction tooling
Shared reaction semantics across channels:

- `emoji` is required when adding a reaction.

- `emoji=""` removes the bot’s reaction(s) when supported.

- `remove: true` removes the specified emoji when supported (requires `emoji`).

Channel notes:

- **Discord/Slack**: empty `emoji` removes all of the bot’s reactions on the message; `remove: true` removes just that emoji.

- **Google Chat**: empty `emoji` removes the app’s reactions on the message; `remove: true` removes just that emoji.

- **Telegram**: empty `emoji` removes the bot’s reactions; `remove: true` also removes reactions but still requires a non-empty `emoji` for tool validation.

- **WhatsApp**: empty `emoji` removes the bot reaction; `remove: true` maps to empty emoji (still requires `emoji`).

- **Signal**: inbound reaction notifications emit system events when `channels.signal.reactionNotifications` is enabled.

Thinking LevelsBrowser (OpenClaw-managed)⌘I