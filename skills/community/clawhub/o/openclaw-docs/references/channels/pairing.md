# Pairing

Source: https://docs.openclaw.ai/channels/pairing

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfigurationPairingGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [Pairing](#pairing)
- [1) DM pairing (inbound chat access)](#1-dm-pairing-inbound-chat-access)
- [Approve a sender](#approve-a-sender)
- [Where the state lives](#where-the-state-lives)
- [2) Node device pairing (iOS/Android/macOS/headless nodes)](#2-node-device-pairing-ios%2Fandroid%2Fmacos%2Fheadless-nodes)
- [Pair via Telegram (recommended for iOS)](#pair-via-telegram-recommended-for-ios)
- [Approve a node device](#approve-a-node-device)
- [Node pairing state storage](#node-pairing-state-storage)
- [Notes](#notes)
- [Related docs](#related-docs)

​Pairing
“Pairing” is OpenClaw’s explicit **owner approval** step.
It is used in two places:

- **DM pairing** (who is allowed to talk to the bot)

- **Node pairing** (which devices/nodes are allowed to join the gateway network)

Security context: [Security](/gateway/security)
​1) DM pairing (inbound chat access)
When a channel is configured with DM policy `pairing`, unknown senders get a short code and their message is **not processed** until you approve.
Default DM policies are documented in: [Security](/gateway/security)
Pairing codes:

- 8 characters, uppercase, no ambiguous chars (`0O1I`).

- **Expire after 1 hour**. The bot only sends the pairing message when a new request is created (roughly once per hour per sender).

- Pending DM pairing requests are capped at **3 per channel** by default; additional requests are ignored until one expires or is approved.

​Approve a sender
Copy```
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>

```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`, `feishu`.
​Where the state lives
Stored under `~/.openclaw/credentials/`:

- Pending requests: `<channel>-pairing.json`

- Approved allowlist store: `<channel>-allowFrom.json`

Treat these as sensitive (they gate access to your assistant).
​2) Node device pairing (iOS/Android/macOS/headless nodes)
Nodes connect to the Gateway as **devices** with `role: node`. The Gateway
creates a device pairing request that must be approved.
​Pair via Telegram (recommended for iOS)
If you use the `device-pair` plugin, you can do first-time device pairing entirely from Telegram:

- In Telegram, message your bot: `/pair`

- The bot replies with two messages: an instruction message and a separate **setup code** message (easy to copy/paste in Telegram).

- On your phone, open the OpenClaw iOS app → Settings → Gateway.

- Paste the setup code and connect.

- Back in Telegram: `/pair approve`

The setup code is a base64-encoded JSON payload that contains:

- `url`: the Gateway WebSocket URL (`ws://...` or `wss://...`)

- `token`: a short-lived pairing token

Treat the setup code like a password while it is valid.
​Approve a node device
Copy```
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>

```

​Node pairing state storage
Stored under `~/.openclaw/devices/`:

- `pending.json` (short-lived; pending requests expire)

- `paired.json` (paired devices + tokens)

​Notes

- The legacy `node.pair.*` API (CLI: `openclaw nodes pending/approve`) is a
separate gateway-owned pairing store. WS nodes still require device pairing.

​Related docs

- Security model + prompt injection: [Security](/gateway/security)

- Updating safely (run doctor): [Updating](/install/updating)

Channel configs:

- Telegram: [Telegram](/channels/telegram)

- WhatsApp: [WhatsApp](/channels/whatsapp)

- Signal: [Signal](/channels/signal)

- BlueBubbles (iMessage): [BlueBubbles](/channels/bluebubbles)

- iMessage (legacy): [iMessage](/channels/imessage)

- Discord: [Discord](/channels/discord)

- Slack: [Slack](/channels/slack)

Zalo PersonalGroup Messages⌘I