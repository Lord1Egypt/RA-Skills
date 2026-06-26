# Slack

Source: https://docs.openclaw.ai/channels/slack

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessaging platformsSlackGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [Slack](#slack)
- [Quick setup](#quick-setup)
- [Token model](#token-model)
- [Access control and routing](#access-control-and-routing)
- [Commands and slash behavior](#commands-and-slash-behavior)
- [Threading, sessions, and reply tags](#threading-sessions-and-reply-tags)
- [Media, chunking, and delivery](#media-chunking-and-delivery)
- [Actions and gates](#actions-and-gates)
- [Events and operational behavior](#events-and-operational-behavior)
- [Ack reactions](#ack-reactions)
- [Manifest and scope checklist](#manifest-and-scope-checklist)
- [Troubleshooting](#troubleshooting)
- [Configuration reference pointers](#configuration-reference-pointers)
- [Related](#related)

​Slack
Status: production-ready for DMs + channels via Slack app integrations. Default mode is Socket Mode; HTTP Events API mode is also supported.
## Pairing

Slack DMs default to pairing mode.## Slash commands

Native command behavior and command catalog.## Channel troubleshooting

Cross-channel diagnostics and repair playbooks.
​Quick setup

 Socket Mode (default) HTTP Events API mode
1Create Slack app and tokens

In Slack app settings:

- enable **Socket Mode**

- create **App Token** (`xapp-...`) with `connections:write`

- install app and copy **Bot Token** (`xoxb-...`)

2Configure OpenClaw

Copy```
{
  channels: {
    slack: {
      enabled: true,
      mode: "socket",
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}

```

Env fallback (default account only):Copy```
SLACK_APP_TOKEN=xapp-...
SLACK_BOT_TOKEN=xoxb-...

```

3Subscribe app events

Subscribe bot events for:

- `app_mention`

- `message.channels`, `message.groups`, `message.im`, `message.mpim`

- `reaction_added`, `reaction_removed`

- `member_joined_channel`, `member_left_channel`

- `channel_rename`

- `pin_added`, `pin_removed`

Also enable App Home **Messages Tab** for DMs.4Start gateway

Copy```
openclaw gateway

```

1Configure Slack app for HTTP

- set mode to HTTP (`channels.slack.mode="http"`)

- copy Slack **Signing Secret**

- set Event Subscriptions + Interactivity + Slash command Request URL to the same webhook path (default `/slack/events`)

2Configure OpenClaw HTTP mode

Copy```
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}

```

3Use unique webhook paths for multi-account HTTP

Per-account HTTP mode is supported.Give each account a distinct `webhookPath` so registrations do not collide.
​Token model

- `botToken` + `appToken` are required for Socket Mode.

- HTTP mode requires `botToken` + `signingSecret`.

- Config tokens override env fallback.

- `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` env fallback applies only to the default account.

- `userToken` (`xoxp-...`) is config-only (no env fallback) and defaults to read-only behavior (`userTokenReadOnly: true`).

- Optional: add `chat:write.customize` if you want outgoing messages to use the active agent identity (custom `username` and icon). `icon_emoji` uses `:emoji_name:` syntax.

For actions/directory reads, user token can be preferred when configured. For writes, bot token remains preferred; user-token writes are only allowed when `userTokenReadOnly: false` and bot token is unavailable.
​Access control and routing

 DM policy Channel policy Mentions and channel users
`channels.slack.dmPolicy` controls DM access (legacy: `channels.slack.dm.policy`):

- `pairing` (default)

- `allowlist`

- `open` (requires `channels.slack.allowFrom` to include `"*"`; legacy: `channels.slack.dm.allowFrom`)

- `disabled`

DM flags:

- `dm.enabled` (default true)

- `channels.slack.allowFrom` (preferred)

- `dm.allowFrom` (legacy)

- `dm.groupEnabled` (group DMs default false)

- `dm.groupChannels` (optional MPIM allowlist)

Pairing in DMs uses `openclaw pairing approve slack <code>`.`channels.slack.groupPolicy` controls channel handling:

- `open`

- `allowlist`

- `disabled`

Channel allowlist lives under `channels.slack.channels`.Runtime note: if `channels.slack` is completely missing (env-only setup) and `channels.defaults.groupPolicy` is unset, runtime falls back to `groupPolicy="open"` and logs a warning.Name/ID resolution:

- channel allowlist entries and DM allowlist entries are resolved at startup when token access allows

- unresolved entries are kept as configured

Channel messages are mention-gated by default.Mention sources:

- explicit app mention (`<@botId>`)

- mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)

- implicit reply-to-bot thread behavior

Per-channel controls (`channels.slack.channels.<id|name>`):

- `requireMention`

- `users` (allowlist)

- `allowBots`

- `skills`

- `systemPrompt`

- `tools`, `toolsBySender`

​Commands and slash behavior

- Native command auto-mode is **off** for Slack (`commands.native: "auto"` does not enable Slack native commands).

- Enable native Slack command handlers with `channels.slack.commands.native: true` (or global `commands.native: true`).

- When native commands are enabled, register matching slash commands in Slack (`/<command>` names).

- If native commands are not enabled, you can run a single configured slash command via `channels.slack.slashCommand`.

Native arg menus now adapt their rendering strategy:

- up to 5 options: button blocks

- 6-100 options: static select menu

- more than 100 options: external select with async option filtering when interactivity options handlers are available

- if encoded option values exceed Slack limits, the flow falls back to buttons

- For long option payloads, Slash command argument menus use a confirm dialog before dispatching a selected value.

Default slash command settings:

- `enabled: false`

- `name: "openclaw"`

- `sessionPrefix: "slack:slash"`

- `ephemeral: true`

Slash sessions use isolated keys:

- `agent:<agentId>:slack:slash:<userId>`

and still route command execution against the target conversation session (`CommandTargetSessionKey`).
​Threading, sessions, and reply tags

- DMs route as `direct`; channels as `channel`; MPIMs as `group`.

- With default `session.dmScope=main`, Slack DMs collapse to agent main session.

- Channel sessions: `agent:<agentId>:slack:channel:<channelId>`.

- Thread replies can create thread session suffixes (`:thread:<threadTs>`) when applicable.

- `channels.slack.thread.historyScope` default is `thread`; `thread.inheritParent` default is `false`.

- `channels.slack.thread.initialHistoryLimit` controls how many existing thread messages are fetched when a new thread session starts (default `20`; set `0` to disable).

Reply threading controls:

- `channels.slack.replyToMode`: `off|first|all` (default `off`)

- `channels.slack.replyToModeByChatType`: per `direct|group|channel`

- legacy fallback for direct chats: `channels.slack.dm.replyToMode`

Manual reply tags are supported:

- `[[reply_to_current]]`

- `[[reply_to:<id>]]`

Note: `replyToMode="off"` disables implicit reply threading. Explicit `[[reply_to_*]]` tags are still honored.
​Media, chunking, and delivery
Inbound attachments

Slack file attachments are downloaded from Slack-hosted private URLs (token-authenticated request flow) and written to the media store when fetch succeeds and size limits permit.Runtime inbound size cap defaults to `20MB` unless overridden by `channels.slack.mediaMaxMb`.Outbound text and files

- text chunks use `channels.slack.textChunkLimit` (default 4000)

- `channels.slack.chunkMode="newline"` enables paragraph-first splitting

- file sends use Slack upload APIs and can include thread replies (`thread_ts`)

- outbound media cap follows `channels.slack.mediaMaxMb` when configured; otherwise channel sends use MIME-kind defaults from media pipeline

Delivery targets

Preferred explicit targets:

- `user:<id>` for DMs

- `channel:<id>` for channels

Slack DMs are opened via Slack conversation APIs when sending to user targets.
​Actions and gates
Slack actions are controlled by `channels.slack.actions.*`.
Available action groups in current Slack tooling:
GroupDefaultmessagesenabledreactionsenabledpinsenabledmemberInfoenabledemojiListenabled
​Events and operational behavior

- Message edits/deletes/thread broadcasts are mapped into system events.

- Reaction add/remove events are mapped into system events.

- Member join/leave, channel created/renamed, and pin add/remove events are mapped into system events.

- `channel_id_changed` can migrate channel config keys when `configWrites` is enabled.

- Channel topic/purpose metadata is treated as untrusted context and can be injected into routing context.

Block actions and modal interactions emit structured `Slack interaction: ...` system events with rich payload fields:

- block actions: selected values, labels, picker values, and `workflow_*` metadata

- modal `view_submission` and `view_closed` events with routed channel metadata and form inputs

​Ack reactions
`ackReaction` sends an acknowledgement emoji while OpenClaw is processing an inbound message.
Resolution order:

- `channels.slack.accounts.<accountId>.ackReaction`

- `channels.slack.ackReaction`

- `messages.ackReaction`

- agent identity emoji fallback (`agents.list[].identity.emoji`, else ”👀”)

Notes:

- Slack expects shortcodes (for example `"eyes"`).

- Use `""` to disable the reaction for a channel or account.

​Manifest and scope checklist
Slack app manifest example

Copy```
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "im:history",
        "mpim:history",
        "users:read",
        "app_mentions:read",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}

```

Optional user-token scopes (read operations)

If you configure `channels.slack.userToken`, typical read scopes are:

- `channels:history`, `groups:history`, `im:history`, `mpim:history`

- `channels:read`, `groups:read`, `im:read`, `mpim:read`

- `users:read`

- `reactions:read`

- `pins:read`

- `emoji:read`

- `search:read` (if you depend on Slack search reads)

​Troubleshooting
No replies in channels

Check, in order:

- `groupPolicy`

- channel allowlist (`channels.slack.channels`)

- `requireMention`

- per-channel `users` allowlist

Useful commands:Copy```
openclaw channels status --probe
openclaw logs --follow
openclaw doctor

```

DM messages ignored

Check:

- `channels.slack.dm.enabled`

- `channels.slack.dmPolicy` (or legacy `channels.slack.dm.policy`)

- pairing approvals / allowlist entries

Copy```
openclaw pairing list slack

```

Socket mode not connecting

Validate bot + app tokens and Socket Mode enablement in Slack app settings.HTTP mode not receiving events

Validate:

- signing secret

- webhook path

- Slack Request URLs (Events + Interactivity + Slash Commands)

- unique `webhookPath` per HTTP account

Native/slash commands not firing

Verify whether you intended:

- native command mode (`channels.slack.commands.native: true`) with matching slash commands registered in Slack

- or single slash command mode (`channels.slack.slashCommand.enabled: true`)

Also check `commands.useAccessGroups` and channel/user allowlists.
​Configuration reference pointers
Primary reference:

[Configuration reference - Slack](/gateway/configuration-reference#slack)
High-signal Slack fields:

- mode/auth: `mode`, `botToken`, `appToken`, `signingSecret`, `webhookPath`, `accounts.*`

- DM access: `dm.enabled`, `dmPolicy`, `allowFrom` (legacy: `dm.policy`, `dm.allowFrom`), `dm.groupEnabled`, `dm.groupChannels`

- channel access: `groupPolicy`, `channels.*`, `channels.*.users`, `channels.*.requireMention`

- threading/history: `replyToMode`, `replyToModeByChatType`, `thread.*`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`

- delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`

- ops/features: `configWrites`, `commands.native`, `slashCommand.*`, `actions.*`, `userToken`, `userTokenReadOnly`

​Related

- [Pairing](/channels/pairing)

- [Channel routing](/channels/channel-routing)

- [Troubleshooting](/channels/troubleshooting)

- [Configuration](/gateway/configuration)

- [Slash commands](/tools/slash-commands)

IRCFeishu⌘I