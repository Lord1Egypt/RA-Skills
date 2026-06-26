# Mattermost

Source: https://docs.openclaw.ai/channels/mattermost

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessaging platformsMattermostGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [Mattermost (plugin)](#mattermost-plugin)
- [Plugin required](#plugin-required)
- [Quick setup](#quick-setup)
- [Environment variables (default account)](#environment-variables-default-account)
- [Chat modes](#chat-modes)
- [Access control (DMs)](#access-control-dms)
- [Channels (groups)](#channels-groups)
- [Targets for outbound delivery](#targets-for-outbound-delivery)
- [Multi-account](#multi-account)
- [Troubleshooting](#troubleshooting)

​Mattermost (plugin)
Status: supported via plugin (bot token + WebSocket events). Channels, groups, and DMs are supported.
Mattermost is a self-hostable team messaging platform; see the official site at
[mattermost.com](https://mattermost.com) for product details and downloads.
​Plugin required
Mattermost ships as a plugin and is not bundled with the core install.
Install via CLI (npm registry):
Copy```
openclaw plugins install @openclaw/mattermost

```

Local checkout (when running from a git repo):
Copy```
openclaw plugins install ./extensions/mattermost

```

If you choose Mattermost during configure/onboarding and a git checkout is detected,
OpenClaw will offer the local install path automatically.
Details: [Plugins](/tools/plugin)
​Quick setup

- Install the Mattermost plugin.

- Create a Mattermost bot account and copy the **bot token**.

- Copy the Mattermost **base URL** (e.g., `https://chat.example.com`).

- Configure OpenClaw and start the gateway.

Minimal config:
Copy```
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}

```

​Environment variables (default account)
Set these on the gateway host if you prefer env vars:

- `MATTERMOST_BOT_TOKEN=...`

- `MATTERMOST_URL=https://chat.example.com`

Env vars apply only to the **default** account (`default`). Other accounts must use config values.
​Chat modes
Mattermost responds to DMs automatically. Channel behavior is controlled by `chatmode`:

- `oncall` (default): respond only when @mentioned in channels.

- `onmessage`: respond to every channel message.

- `onchar`: respond when a message starts with a trigger prefix.

Config example:
Copy```
{
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}

```

Notes:

- `onchar` still responds to explicit @mentions.

- `channels.mattermost.requireMention` is honored for legacy configs but `chatmode` is preferred.

​Access control (DMs)

- Default: `channels.mattermost.dmPolicy = "pairing"` (unknown senders get a pairing code).

Approve via:

- `openclaw pairing list mattermost`

- `openclaw pairing approve mattermost <CODE>`

- Public DMs: `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.

​Channels (groups)

- Default: `channels.mattermost.groupPolicy = "allowlist"` (mention-gated).

- Allowlist senders with `channels.mattermost.groupAllowFrom` (user IDs or `@username`).

- Open channels: `channels.mattermost.groupPolicy="open"` (mention-gated).

​Targets for outbound delivery
Use these target formats with `openclaw message send` or cron/webhooks:

- `channel:<id>` for a channel

- `user:<id>` for a DM

- `@username` for a DM (resolved via the Mattermost API)

Bare IDs are treated as channels.
​Multi-account
Mattermost supports multiple accounts under `channels.mattermost.accounts`:
Copy```
{
  channels: {
    mattermost: {
      accounts: {
        default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },
        alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },
      },
    },
  },
}

```

​Troubleshooting

- No replies in channels: ensure the bot is in the channel and mention it (oncall), use a trigger prefix (onchar), or set `chatmode: "onmessage"`.

- Auth errors: check the bot token, base URL, and whether the account is enabled.

- Multi-account issues: env vars only apply to the `default` account.

Google ChatSignal⌘I