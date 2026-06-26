# Channel Troubleshooting

Source: https://docs.openclaw.ai/channels/troubleshooting

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfigurationChannel TroubleshootingGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [Channel troubleshooting](#channel-troubleshooting)
- [Command ladder](#command-ladder)
- [WhatsApp](#whatsapp)
- [WhatsApp failure signatures](#whatsapp-failure-signatures)
- [Telegram](#telegram)
- [Telegram failure signatures](#telegram-failure-signatures)
- [Discord](#discord)
- [Discord failure signatures](#discord-failure-signatures)
- [Slack](#slack)
- [Slack failure signatures](#slack-failure-signatures)
- [iMessage and BlueBubbles](#imessage-and-bluebubbles)
- [iMessage and BlueBubbles failure signatures](#imessage-and-bluebubbles-failure-signatures)
- [Signal](#signal)
- [Signal failure signatures](#signal-failure-signatures)
- [Matrix](#matrix)
- [Matrix failure signatures](#matrix-failure-signatures)

​Channel troubleshooting
Use this page when a channel connects but behavior is wrong.
​Command ladder
Run these in order first:
Copy```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe

```

Healthy baseline:

- `Runtime: running`

- `RPC probe: ok`

- Channel probe shows connected/ready

​WhatsApp
​WhatsApp failure signatures
SymptomFastest checkFixConnected but no DM replies`openclaw pairing list whatsapp`Approve sender or switch DM policy/allowlist.Group messages ignoredCheck `requireMention` + mention patterns in configMention the bot or relax mention policy for that group.Random disconnect/relogin loops`openclaw channels status --probe` + logsRe-login and verify credentials directory is healthy.
Full troubleshooting: [/channels/whatsapp#troubleshooting-quick](/channels/whatsapp#troubleshooting-quick)
​Telegram
​Telegram failure signatures
SymptomFastest checkFix`/start` but no usable reply flow`openclaw pairing list telegram`Approve pairing or change DM policy.Bot online but group stays silentVerify mention requirement and bot privacy modeDisable privacy mode for group visibility or mention bot.Send failures with network errorsInspect logs for Telegram API call failuresFix DNS/IPv6/proxy routing to `api.telegram.org`.Upgraded and allowlist blocks you`openclaw security audit` and config allowlistsRun `openclaw doctor --fix` or replace `@username` with numeric sender IDs.
Full troubleshooting: [/channels/telegram#troubleshooting](/channels/telegram#troubleshooting)
​Discord
​Discord failure signatures
SymptomFastest checkFixBot online but no guild replies`openclaw channels status --probe`Allow guild/channel and verify message content intent.Group messages ignoredCheck logs for mention gating dropsMention bot or set guild/channel `requireMention: false`.DM replies missing`openclaw pairing list discord`Approve DM pairing or adjust DM policy.
Full troubleshooting: [/channels/discord#troubleshooting](/channels/discord#troubleshooting)
​Slack
​Slack failure signatures
SymptomFastest checkFixSocket mode connected but no responses`openclaw channels status --probe`Verify app token + bot token and required scopes.DMs blocked`openclaw pairing list slack`Approve pairing or relax DM policy.Channel message ignoredCheck `groupPolicy` and channel allowlistAllow the channel or switch policy to `open`.
Full troubleshooting: [/channels/slack#troubleshooting](/channels/slack#troubleshooting)
​iMessage and BlueBubbles
​iMessage and BlueBubbles failure signatures
SymptomFastest checkFixNo inbound eventsVerify webhook/server reachability and app permissionsFix webhook URL or BlueBubbles server state.Can send but no receive on macOSCheck macOS privacy permissions for Messages automationRe-grant TCC permissions and restart channel process.DM sender blocked`openclaw pairing list imessage` or `openclaw pairing list bluebubbles`Approve pairing or update allowlist.
Full troubleshooting:

- [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)

- [/channels/bluebubbles#troubleshooting](/channels/bluebubbles#troubleshooting)

​Signal
​Signal failure signatures
SymptomFastest checkFixDaemon reachable but bot silent`openclaw channels status --probe`Verify `signal-cli` daemon URL/account and receive mode.DM blocked`openclaw pairing list signal`Approve sender or adjust DM policy.Group replies do not triggerCheck group allowlist and mention patternsAdd sender/group or loosen gating.
Full troubleshooting: [/channels/signal#troubleshooting](/channels/signal#troubleshooting)
​Matrix
​Matrix failure signatures
SymptomFastest checkFixLogged in but ignores room messages`openclaw channels status --probe`Check `groupPolicy` and room allowlist.DMs do not process`openclaw pairing list matrix`Approve sender or adjust DM policy.Encrypted rooms failVerify crypto module and encryption settingsEnable encryption support and rejoin/sync room.
Full troubleshooting: [/channels/matrix#troubleshooting](/channels/matrix#troubleshooting)Channel Location Parsing⌘I