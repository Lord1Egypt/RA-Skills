# WhatsApp

Source: https://docs.openclaw.ai/channels/whatsapp

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessaging platformsWhatsAppGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [WhatsApp (Web channel)](#whatsapp-web-channel)
- [Quick setup](#quick-setup)
- [Deployment patterns](#deployment-patterns)
- [Runtime model](#runtime-model)
- [Access control and activation](#access-control-and-activation)
- [Personal-number and self-chat behavior](#personal-number-and-self-chat-behavior)
- [Message normalization and context](#message-normalization-and-context)
- [Delivery, chunking, and media](#delivery-chunking-and-media)
- [Acknowledgment reactions](#acknowledgment-reactions)
- [Multi-account and credentials](#multi-account-and-credentials)
- [Tools, actions, and config writes](#tools-actions-and-config-writes)
- [Troubleshooting](#troubleshooting)
- [Configuration reference pointers](#configuration-reference-pointers)
- [Related](#related)

​WhatsApp (Web channel)
Status: production-ready via WhatsApp Web (Baileys). Gateway owns linked session(s).
## Pairing

Default DM policy is pairing for unknown senders.## Channel troubleshooting

Cross-channel diagnostics and repair playbooks.## Gateway configuration

Full channel config patterns and examples.
​Quick setup
1Configure WhatsApp access policy

Copy```
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}

```

2Link WhatsApp (QR)

Copy```
openclaw channels login --channel whatsapp

```

For a specific account:Copy```
openclaw channels login --channel whatsapp --account work

```

3Start the gateway

Copy```
openclaw gateway

```

4Approve first pairing request (if using pairing mode)

Copy```
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>

```

Pairing requests expire after 1 hour. Pending requests are capped at 3 per channel.
OpenClaw recommends running WhatsApp on a separate number when possible. (The channel metadata and onboarding flow are optimized for that setup, but personal-number setups are also supported.)
​Deployment patterns
Dedicated number (recommended)

This is the cleanest operational mode:

- separate WhatsApp identity for OpenClaw

- clearer DM allowlists and routing boundaries

- lower chance of self-chat confusion

Minimal policy pattern:Copy```
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}

```

Personal-number fallback

Onboarding supports personal-number mode and writes a self-chat-friendly baseline:

- `dmPolicy: "allowlist"`

- `allowFrom` includes your personal number

- `selfChatMode: true`

In runtime, self-chat protections key off the linked self number and `allowFrom`.WhatsApp Web-only channel scope

The messaging platform channel is WhatsApp Web-based (`Baileys`) in current OpenClaw channel architecture.There is no separate Twilio WhatsApp messaging channel in the built-in chat-channel registry.
​Runtime model

- Gateway owns the WhatsApp socket and reconnect loop.

- Outbound sends require an active WhatsApp listener for the target account.

- Status and broadcast chats are ignored (`@status`, `@broadcast`).

- Direct chats use DM session rules (`session.dmScope`; default `main` collapses DMs to the agent main session).

- Group sessions are isolated (`agent:<agentId>:whatsapp:group:<jid>`).

​Access control and activation

 DM policy Group policy + allowlists Mentions + /activation
`channels.whatsapp.dmPolicy` controls direct chat access:

- `pairing` (default)

- `allowlist`

- `open` (requires `allowFrom` to include `"*"`)

- `disabled`

`allowFrom` accepts E.164-style numbers (normalized internally).Multi-account override: `channels.whatsapp.accounts.<id>.dmPolicy` (and `allowFrom`) take precedence over channel-level defaults for that account.Runtime behavior details:

- pairings are persisted in channel allow-store and merged with configured `allowFrom`

- if no allowlist is configured, the linked self number is allowed by default

- outbound `fromMe` DMs are never auto-paired

Group access has two layers:

**Group membership allowlist** (`channels.whatsapp.groups`)

- if `groups` is omitted, all groups are eligible

- if `groups` is present, it acts as a group allowlist (`"*"` allowed)

**Group sender policy** (`channels.whatsapp.groupPolicy` + `groupAllowFrom`)

- `open`: sender allowlist bypassed

- `allowlist`: sender must match `groupAllowFrom` (or `*`)

- `disabled`: block all group inbound

Sender allowlist fallback:

- if `groupAllowFrom` is unset, runtime falls back to `allowFrom` when available

Note: if no `channels.whatsapp` block exists at all, runtime group-policy fallback is effectively `open`.Group replies require mention by default.Mention detection includes:

- explicit WhatsApp mentions of the bot identity

- configured mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)

- implicit reply-to-bot detection (reply sender matches bot identity)

Session-level activation command:

- `/activation mention`

- `/activation always`

`activation` updates session state (not global config). It is owner-gated.
​Personal-number and self-chat behavior
When the linked self number is also present in `allowFrom`, WhatsApp self-chat safeguards activate:

- skip read receipts for self-chat turns

- ignore mention-JID auto-trigger behavior that would otherwise ping yourself

- if `messages.responsePrefix` is unset, self-chat replies default to `[{identity.name}]` or `[openclaw]`

​Message normalization and context
Inbound envelope + reply context

Incoming WhatsApp messages are wrapped in the shared inbound envelope.If a quoted reply exists, context is appended in this form:Copy```
[Replying to <sender> id:<stanzaId>]
<quoted body or media placeholder>
[/Replying]

```

Reply metadata fields are also populated when available (`ReplyToId`, `ReplyToBody`, `ReplyToSender`, sender JID/E.164).Media placeholders and location/contact extraction

Media-only inbound messages are normalized with placeholders such as:

- `<media:image>`

- `<media:video>`

- `<media:audio>`

- `<media:document>`

- `<media:sticker>`

Location and contact payloads are normalized into textual context before routing.Pending group history injection

For groups, unprocessed messages can be buffered and injected as context when the bot is finally triggered.

- default limit: `50`

- config: `channels.whatsapp.historyLimit`

- fallback: `messages.groupChat.historyLimit`

- `0` disables

Injection markers:

- `[Chat messages since your last reply - for context]`

- `[Current message - respond to this]`

Read receipts

Read receipts are enabled by default for accepted inbound WhatsApp messages.Disable globally:Copy```
{
  channels: {
    whatsapp: {
      sendReadReceipts: false,
    },
  },
}

```

Per-account override:Copy```
{
  channels: {
    whatsapp: {
      accounts: {
        work: {
          sendReadReceipts: false,
        },
      },
    },
  },
}

```

Self-chat turns skip read receipts even when globally enabled.
​Delivery, chunking, and media
Text chunking

- default chunk limit: `channels.whatsapp.textChunkLimit = 4000`

- `channels.whatsapp.chunkMode = "length" | "newline"`

- `newline` mode prefers paragraph boundaries (blank lines), then falls back to length-safe chunking

Outbound media behavior

- supports image, video, audio (PTT voice-note), and document payloads

- `audio/ogg` is rewritten to `audio/ogg; codecs=opus` for voice-note compatibility

- animated GIF playback is supported via `gifPlayback: true` on video sends

- captions are applied to the first media item when sending multi-media reply payloads

- media source can be HTTP(S), `file://`, or local paths

Media size limits and fallback behavior

- inbound media save cap: `channels.whatsapp.mediaMaxMb` (default `50`)

- outbound media cap for auto-replies: `agents.defaults.mediaMaxMb` (default `5MB`)

- images are auto-optimized (resize/quality sweep) to fit limits

- on media send failure, first-item fallback sends text warning instead of dropping the response silently

​Acknowledgment reactions
WhatsApp supports immediate ack reactions on inbound receipt via `channels.whatsapp.ackReaction`.
Copy```
{
  channels: {
    whatsapp: {
      ackReaction: {
        emoji: "👀",
        direct: true,
        group: "mentions", // always | mentions | never
      },
    },
  },
}

```

Behavior notes:

- sent immediately after inbound is accepted (pre-reply)

- failures are logged but do not block normal reply delivery

- group mode `mentions` reacts on mention-triggered turns; group activation `always` acts as bypass for this check

- WhatsApp uses `channels.whatsapp.ackReaction` (legacy `messages.ackReaction` is not used here)

​Multi-account and credentials
Account selection and defaults

- account ids come from `channels.whatsapp.accounts`

- default account selection: `default` if present, otherwise first configured account id (sorted)

- account ids are normalized internally for lookup

Credential paths and legacy compatibility

- current auth path: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`

- backup file: `creds.json.bak`

- legacy default auth in `~/.openclaw/credentials/` is still recognized/migrated for default-account flows

Logout behavior

`openclaw channels logout --channel whatsapp [--account <id>]` clears WhatsApp auth state for that account.In legacy auth directories, `oauth.json` is preserved while Baileys auth files are removed.
​Tools, actions, and config writes

- Agent tool support includes WhatsApp reaction action (`react`).

Action gates:

- `channels.whatsapp.actions.reactions`

- `channels.whatsapp.actions.polls`

- Channel-initiated config writes are enabled by default (disable via `channels.whatsapp.configWrites=false`).

​Troubleshooting
Not linked (QR required)

Symptom: channel status reports not linked.Fix:Copy```
openclaw channels login --channel whatsapp
openclaw channels status

```

Linked but disconnected / reconnect loop

Symptom: linked account with repeated disconnects or reconnect attempts.Fix:Copy```
openclaw doctor
openclaw logs --follow

```

If needed, re-link with `channels login`.No active listener when sending

Outbound sends fail fast when no active gateway listener exists for the target account.Make sure gateway is running and the account is linked.Group messages unexpectedly ignored

Check in this order:

- `groupPolicy`

- `groupAllowFrom` / `allowFrom`

- `groups` allowlist entries

- mention gating (`requireMention` + mention patterns)

Bun runtime warning

WhatsApp gateway runtime should use Node. Bun is flagged as incompatible for stable WhatsApp/Telegram gateway operation.
​Configuration reference pointers
Primary reference:

- [Configuration reference - WhatsApp](/gateway/configuration-reference#whatsapp)

High-signal WhatsApp fields:

- access: `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`

- delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `sendReadReceipts`, `ackReaction`

- multi-account: `accounts.<id>.enabled`, `accounts.<id>.authDir`, account-level overrides

- operations: `configWrites`, `debounceMs`, `web.enabled`, `web.heartbeatSeconds`, `web.reconnect.*`

- session behavior: `session.dmScope`, `historyLimit`, `dmHistoryLimit`, `dms.<id>.historyLimit`

​Related

- [Pairing](/channels/pairing)

- [Channel routing](/channels/channel-routing)

- [Troubleshooting](/channels/troubleshooting)

Chat ChannelsTelegram⌘I