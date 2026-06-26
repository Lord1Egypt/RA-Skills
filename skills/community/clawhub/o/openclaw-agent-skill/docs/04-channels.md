# Channels (Chat Platforms)

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 29

---

<!-- SOURCE: https://docs.openclaw.ai/channels/telegram -->

# Telegram - OpenClaw

## Telegram (Bot API)

Status: production-ready for bot DMs + groups via grammY. Long polling is the default mode; webhook mode is optional.

## Quick setup

## Telegram side settings

## Access control and activation

*   DM policy
    
*   Group policy and allowlists
    
*   Mention behavior
    

`channels.telegram.dmPolicy` controls direct message access:

*   `pairing` (default)
*   `allowlist` (requires at least one sender ID in `allowFrom`)
*   `open` (requires `allowFrom` to include `"*"`)
*   `disabled`

`channels.telegram.allowFrom` accepts numeric Telegram user IDs. `telegram:` / `tg:` prefixes are accepted and normalized. `dmPolicy: "allowlist"` with empty `allowFrom` blocks all DMs and is rejected by config validation. The onboarding wizard accepts `@username` input and resolves it to numeric IDs. If you upgraded and your config contains `@username` allowlist entries, run `openclaw doctor --fix` to resolve them (best-effort; requires a Telegram bot token). If you previously relied on pairing-store allowlist files, `openclaw doctor --fix` can recover entries into `channels.telegram.allowFrom` in allowlist flows (for example when `dmPolicy: "allowlist"` has no explicit IDs yet).For one-owner bots, prefer `dmPolicy: "allowlist"` with explicit numeric `allowFrom` IDs to keep access policy durable in config (instead of depending on previous pairing approvals).

### Finding your Telegram user ID

Safer (no third-party bot):

1.  DM your bot.
2.  Run `openclaw logs --follow`.
3.  Read `from.id`.

Official Bot API method:

```
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

Third-party method (less private): `@userinfobot` or `@getidsbot`.

Two controls apply together:

1.  **Which groups are allowed** (`channels.telegram.groups`)
    *   no `groups` config:
        *   with `groupPolicy: "open"`: any group can pass group-ID checks
        *   with `groupPolicy: "allowlist"` (default): groups are blocked until you add `groups` entries (or `"*"`)
    *   `groups` configured: acts as allowlist (explicit IDs or `"*"`)
2.  **Which senders are allowed in groups** (`channels.telegram.groupPolicy`)
    *   `open`
    *   `allowlist` (default)
    *   `disabled`

`groupAllowFrom` is used for group sender filtering. If not set, Telegram falls back to `allowFrom`. `groupAllowFrom` entries should be numeric Telegram user IDs (`telegram:` / `tg:` prefixes are normalized). Non-numeric entries are ignored for sender authorization. Security boundary (`2026.2.25+`): group sender auth does **not** inherit DM pairing-store approvals. Pairing stays DM-only. For groups, set `groupAllowFrom` or per-group/per-topic `allowFrom`. Runtime note: if `channels.telegram` is completely missing, runtime defaults to fail-closed `groupPolicy="allowlist"` unless `channels.defaults.groupPolicy` is explicitly set.Example: allow any member in one specific group:

```
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

Group replies require mention by default.Mention can come from:

*   native `@botusername` mention, or
*   mention patterns in:
    *   `agents.list[].groupChat.mentionPatterns`
    *   `messages.groupChat.mentionPatterns`

Session-level command toggles:

*   `/activation always`
*   `/activation mention`

These update session state only. Use config for persistence.Persistent config example:

```
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false },
      },
    },
  },
}
```

Getting the group chat ID:

*   forward a group message to `@userinfobot` / `@getidsbot`
*   or read `chat.id` from `openclaw logs --follow`
*   or inspect Bot API `getUpdates`

## Runtime behavior

*   Telegram is owned by the gateway process.
*   Routing is deterministic: Telegram inbound replies back to Telegram (the model does not pick channels).
*   Inbound messages normalize into the shared channel envelope with reply metadata and media placeholders.
*   Group sessions are isolated by group ID. Forum topics append `:topic:<threadId>` to keep topics isolated.
*   DM messages can carry `message_thread_id`; OpenClaw routes them with thread-aware session keys and preserves thread ID for replies.
*   Long polling uses grammY runner with per-chat/per-thread sequencing. Overall runner sink concurrency uses `agents.defaults.maxConcurrent`.
*   Telegram Bot API has no read-receipt support (`sendReadReceipts` does not apply).

## Feature reference

## Troubleshooting

More help: [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting).

## Telegram config reference pointers

Primary reference:

*   `channels.telegram.enabled`: enable/disable channel startup.
*   `channels.telegram.botToken`: bot token (BotFather).
*   `channels.telegram.tokenFile`: read token from file path.
*   `channels.telegram.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).
*   `channels.telegram.allowFrom`: DM allowlist (numeric Telegram user IDs). `allowlist` requires at least one sender ID. `open` requires `"*"`. `openclaw doctor --fix` can resolve legacy `@username` entries to IDs and can recover allowlist entries from pairing-store files in allowlist migration flows.
*   `channels.telegram.actions.poll`: enable or disable Telegram poll creation (default: enabled; still requires `sendMessage`).
*   `channels.telegram.defaultTo`: default Telegram target used by CLI `--deliver` when no explicit `--reply-to` is provided.
*   `channels.telegram.groupPolicy`: `open | allowlist | disabled` (default: allowlist).
*   `channels.telegram.groupAllowFrom`: group sender allowlist (numeric Telegram user IDs). `openclaw doctor --fix` can resolve legacy `@username` entries to IDs. Non-numeric entries are ignored at auth time. Group auth does not use DM pairing-store fallback (`2026.2.25+`).
*   Multi-account precedence:
    *   When two or more account IDs are configured, set `channels.telegram.defaultAccount` (or include `channels.telegram.accounts.default`) to make default routing explicit.
    *   If neither is set, OpenClaw falls back to the first normalized account ID and `openclaw doctor` warns.
    *   `channels.telegram.accounts.default.allowFrom` and `channels.telegram.accounts.default.groupAllowFrom` apply only to the `default` account.
    *   Named accounts inherit `channels.telegram.allowFrom` and `channels.telegram.groupAllowFrom` when account-level values are unset.
    *   Named accounts do not inherit `channels.telegram.accounts.default.allowFrom` / `groupAllowFrom`.
*   `channels.telegram.groups`: per-group defaults + allowlist (use `"*"` for global defaults).
    *   `channels.telegram.groups.<id>.groupPolicy`: per-group override for groupPolicy (`open | allowlist | disabled`).
    *   `channels.telegram.groups.<id>.requireMention`: mention gating default.
    *   `channels.telegram.groups.<id>.skills`: skill filter (omit = all skills, empty = none).
    *   `channels.telegram.groups.<id>.allowFrom`: per-group sender allowlist override.
    *   `channels.telegram.groups.<id>.systemPrompt`: extra system prompt for the group.
    *   `channels.telegram.groups.<id>.enabled`: disable the group when `false`.
    *   `channels.telegram.groups.<id>.topics.<threadId>.*`: per-topic overrides (group fields + topic-only `agentId`).
    *   `channels.telegram.groups.<id>.topics.<threadId>.agentId`: route this topic to a specific agent (overrides group-level and binding routing).
    *   `channels.telegram.groups.<id>.topics.<threadId>.groupPolicy`: per-topic override for groupPolicy (`open | allowlist | disabled`).
    *   `channels.telegram.groups.<id>.topics.<threadId>.requireMention`: per-topic mention gating override.
    *   top-level `bindings[]` with `type: "acp"` and canonical topic id `chatId:topic:topicId` in `match.peer.id`: persistent ACP topic binding fields (see [ACP Agents](https://docs.openclaw.ai/tools/acp-agents#channel-specific-settings)).
    *   `channels.telegram.direct.<id>.topics.<threadId>.agentId`: route DM topics to a specific agent (same behavior as forum topics).
*   `channels.telegram.capabilities.inlineButtons`: `off | dm | group | all | allowlist` (default: allowlist).
*   `channels.telegram.accounts.<account>.capabilities.inlineButtons`: per-account override.
*   `channels.telegram.commands.nativeSkills`: enable/disable Telegram native skills commands.
*   `channels.telegram.replyToMode`: `off | first | all` (default: `off`).
*   `channels.telegram.textChunkLimit`: outbound chunk size (chars).
*   `channels.telegram.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
*   `channels.telegram.linkPreview`: toggle link previews for outbound messages (default: true).
*   `channels.telegram.streaming`: `off | partial | block | progress` (live stream preview; default: `partial`; `progress` maps to `partial`; `block` is legacy preview mode compatibility). Telegram preview streaming uses a single preview message that is edited in place.
*   `channels.telegram.mediaMaxMb`: inbound/outbound Telegram media cap (MB, default: 100).
*   `channels.telegram.retry`: retry policy for Telegram send helpers (CLI/tools/actions) on recoverable outbound API errors (attempts, minDelayMs, maxDelayMs, jitter).
*   `channels.telegram.network.autoSelectFamily`: override Node autoSelectFamily (true=enable, false=disable). Defaults to enabled on Node 22+, with WSL2 defaulting to disabled.
*   `channels.telegram.network.dnsResultOrder`: override DNS result order (`ipv4first` or `verbatim`). Defaults to `ipv4first` on Node 22+.
*   `channels.telegram.proxy`: proxy URL for Bot API calls (SOCKS/HTTP).
*   `channels.telegram.webhookUrl`: enable webhook mode (requires `channels.telegram.webhookSecret`).
*   `channels.telegram.webhookSecret`: webhook secret (required when webhookUrl is set).
*   `channels.telegram.webhookPath`: local webhook path (default `/telegram-webhook`).
*   `channels.telegram.webhookHost`: local webhook bind host (default `127.0.0.1`).
*   `channels.telegram.webhookPort`: local webhook bind port (default `8787`).
*   `channels.telegram.actions.reactions`: gate Telegram tool reactions.
*   `channels.telegram.actions.sendMessage`: gate Telegram tool message sends.
*   `channels.telegram.actions.deleteMessage`: gate Telegram tool message deletes.
*   `channels.telegram.actions.sticker`: gate Telegram sticker actions — send and search (default: false).
*   `channels.telegram.reactionNotifications`: `off | own | all` — control which reactions trigger system events (default: `own` when not set).
*   `channels.telegram.reactionLevel`: `off | ack | minimal | extensive` — control agent’s reaction capability (default: `minimal` when not set).
*   [Configuration reference - Telegram](https://docs.openclaw.ai/gateway/configuration-reference#telegram)

Telegram-specific high-signal fields:

*   startup/auth: `enabled`, `botToken`, `tokenFile`, `accounts.*`
*   access control: `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`, `groups.*.topics.*`, top-level `bindings[]` (`type: "acp"`)
*   command/menu: `commands.native`, `commands.nativeSkills`, `customCommands`
*   threading/replies: `replyToMode`
*   streaming: `streaming` (preview), `blockStreaming`
*   formatting/delivery: `textChunkLimit`, `chunkMode`, `linkPreview`, `responsePrefix`
*   media/network: `mediaMaxMb`, `timeoutSeconds`, `retry`, `network.autoSelectFamily`, `proxy`
*   webhook: `webhookUrl`, `webhookSecret`, `webhookPath`, `webhookHost`
*   actions/capabilities: `capabilities.inlineButtons`, `actions.sendMessage|editMessage|deleteMessage|reactions|sticker`
*   reactions: `reactionNotifications`, `reactionLevel`
*   writes/history: `configWrites`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`

*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [Channel routing](https://docs.openclaw.ai/channels/channel-routing)
*   [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
*   [Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

---

<!-- SOURCE: https://docs.openclaw.ai/channels -->

# Chat Channels - OpenClaw

OpenClaw can talk to you on any chat app you already use. Each channel connects via the Gateway. Text is supported everywhere; media and reactions vary by channel.

## Supported channels

*   [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles) — **Recommended for iMessage**; uses the BlueBubbles macOS server REST API with full feature support (edit, unsend, effects, reactions, group management — edit currently broken on macOS 26 Tahoe).
*   [Discord](https://docs.openclaw.ai/channels/discord) — Discord Bot API + Gateway; supports servers, channels, and DMs.
*   [Feishu](https://docs.openclaw.ai/channels/feishu) — Feishu/Lark bot via WebSocket (plugin, installed separately).
*   [Google Chat](https://docs.openclaw.ai/channels/googlechat) — Google Chat API app via HTTP webhook.
*   [iMessage (legacy)](https://docs.openclaw.ai/channels/imessage) — Legacy macOS integration via imsg CLI (deprecated, use BlueBubbles for new setups).
*   [IRC](https://docs.openclaw.ai/channels/irc) — Classic IRC servers; channels + DMs with pairing/allowlist controls.
*   [LINE](https://docs.openclaw.ai/channels/line) — LINE Messaging API bot (plugin, installed separately).
*   [Matrix](https://docs.openclaw.ai/channels/matrix) — Matrix protocol (plugin, installed separately).
*   [Mattermost](https://docs.openclaw.ai/channels/mattermost) — Bot API + WebSocket; channels, groups, DMs (plugin, installed separately).
*   [Microsoft Teams](https://docs.openclaw.ai/channels/msteams) — Bot Framework; enterprise support (plugin, installed separately).
*   [Nextcloud Talk](https://docs.openclaw.ai/channels/nextcloud-talk) — Self-hosted chat via Nextcloud Talk (plugin, installed separately).
*   [Nostr](https://docs.openclaw.ai/channels/nostr) — Decentralized DMs via NIP-04 (plugin, installed separately).
*   [Signal](https://docs.openclaw.ai/channels/signal) — signal-cli; privacy-focused.
*   [Synology Chat](https://docs.openclaw.ai/channels/synology-chat) — Synology NAS Chat via outgoing+incoming webhooks (plugin, installed separately).
*   [Slack](https://docs.openclaw.ai/channels/slack) — Bolt SDK; workspace apps.
*   [Telegram](https://docs.openclaw.ai/channels/telegram) — Bot API via grammY; supports groups.
*   [Tlon](https://docs.openclaw.ai/channels/tlon) — Urbit-based messenger (plugin, installed separately).
*   [Twitch](https://docs.openclaw.ai/channels/twitch) — Twitch chat via IRC connection (plugin, installed separately).
*   [WebChat](https://docs.openclaw.ai/web/webchat) — Gateway WebChat UI over WebSocket.
*   [WhatsApp](https://docs.openclaw.ai/channels/whatsapp) — Most popular; uses Baileys and requires QR pairing.
*   [Zalo](https://docs.openclaw.ai/channels/zalo) — Zalo Bot API; Vietnam’s popular messenger (plugin, installed separately).
*   [Zalo Personal](https://docs.openclaw.ai/channels/zalouser) — Zalo personal account via QR login (plugin, installed separately).

## Notes

*   Channels can run simultaneously; configure multiple and OpenClaw will route per chat.
*   Fastest setup is usually **Telegram** (simple bot token). WhatsApp requires QR pairing and stores more state on disk.
*   Group behavior varies by channel; see [Groups](https://docs.openclaw.ai/channels/groups).
*   DM pairing and allowlists are enforced for safety; see [Security](https://docs.openclaw.ai/gateway/security).
*   Troubleshooting: [Channel troubleshooting](https://docs.openclaw.ai/channels/troubleshooting).
*   Model providers are documented separately; see [Model Providers](https://docs.openclaw.ai/providers/models).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/feishu -->

# Feishu - OpenClaw

## Feishu bot

Feishu (Lark) is a team chat platform used by companies for messaging and collaboration. This plugin connects OpenClaw to a Feishu/Lark bot using the platform’s WebSocket event subscription so messages can be received without exposing a public webhook URL.

* * *

## Bundled plugin

Feishu ships bundled with current OpenClaw releases, so no separate plugin install is required. If you are using an older build or a custom install that does not include bundled Feishu, install it manually:

```
openclaw plugins install @openclaw/feishu
```

* * *

## Quickstart

There are two ways to add the Feishu channel:

### Method 1: onboarding wizard (recommended)

If you just installed OpenClaw, run the wizard:

The wizard guides you through:

1.  Creating a Feishu app and collecting credentials
2.  Configuring app credentials in OpenClaw
3.  Starting the gateway

✅ **After configuration**, check gateway status:

*   `openclaw gateway status`
*   `openclaw logs --follow`

### Method 2: CLI setup

If you already completed initial install, add the channel via CLI:

Choose **Feishu**, then enter the App ID and App Secret. ✅ **After configuration**, manage the gateway:

*   `openclaw gateway status`
*   `openclaw gateway restart`
*   `openclaw logs --follow`

* * *

## Step 1: Create a Feishu app

### 1\. Open Feishu Open Platform

Visit [Feishu Open Platform](https://open.feishu.cn/app) and sign in. Lark (global) tenants should use [https://open.larksuite.com/app](https://open.larksuite.com/app) and set `domain: "lark"` in the Feishu config.

### 2\. Create an app

1.  Click **Create enterprise app**
2.  Fill in the app name + description
3.  Choose an app icon

![Create enterprise app](https://mintcdn.com/clawdhub/6NERQ7Dymau_gJ4k/images/feishu-step2-create-app.png?fit=max&auto=format&n=6NERQ7Dymau_gJ4k&q=85&s=a3d0a511fea278250c353f5c33f03584)

### 3\. Copy credentials

From **Credentials & Basic Info**, copy:

*   **App ID** (format: `cli_xxx`)
*   **App Secret**

❗ **Important:** keep the App Secret private. ![Get credentials](https://mintcdn.com/clawdhub/6NERQ7Dymau_gJ4k/images/feishu-step3-credentials.png?fit=max&auto=format&n=6NERQ7Dymau_gJ4k&q=85&s=3a6ac22e96d76e4b85a1171ea207608b)

### 4\. Configure permissions

On **Permissions**, click **Batch import** and paste:

```
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

![Configure permissions](https://mintcdn.com/clawdhub/6NERQ7Dymau_gJ4k/images/feishu-step4-permissions.png?fit=max&auto=format&n=6NERQ7Dymau_gJ4k&q=85&s=a386d201628f65771d9d423056d9dc59)

### 5\. Enable bot capability

In **App Capability** > **Bot**:

1.  Enable bot capability
2.  Set the bot name

![Enable bot capability](https://mintcdn.com/clawdhub/6NERQ7Dymau_gJ4k/images/feishu-step5-bot-capability.png?fit=max&auto=format&n=6NERQ7Dymau_gJ4k&q=85&s=4c330500fd7db2e72569dc2a379697ee)

### 6\. Configure event subscription

⚠️ **Important:** before setting event subscription, make sure:

1.  You already ran `openclaw channels add` for Feishu
2.  The gateway is running (`openclaw gateway status`)

In **Event Subscription**:

1.  Choose **Use long connection to receive events** (WebSocket)
2.  Add the event: `im.message.receive_v1`

⚠️ If the gateway is not running, the long-connection setup may fail to save. ![Configure event subscription](https://mintcdn.com/clawdhub/6NERQ7Dymau_gJ4k/images/feishu-step6-event-subscription.png?fit=max&auto=format&n=6NERQ7Dymau_gJ4k&q=85&s=00aeb4809d9df159d846e0be19bc871e)

### 7\. Publish the app

1.  Create a version in **Version Management & Release**
2.  Submit for review and publish
3.  Wait for admin approval (enterprise apps usually auto-approve)

* * *

## Step 2: Configure OpenClaw

### Configure with the wizard (recommended)

Choose **Feishu** and paste your App ID + App Secret.

### Configure via config file

Edit `~/.openclaw/openclaw.json`:

```
{
  channels: {
    feishu: {
      enabled: true,
      dmPolicy: "pairing",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          botName: "My AI assistant",
        },
      },
    },
  },
}
```

If you use `connectionMode: "webhook"`, set `verificationToken`. The Feishu webhook server binds to `127.0.0.1` by default; set `webhookHost` only if you intentionally need a different bind address.

#### Verification Token (webhook mode)

When using webhook mode, set `channels.feishu.verificationToken` in your config. To get the value:

1.  In Feishu Open Platform, open your app
2.  Go to **Development** → **Events & Callbacks** (开发配置 → 事件与回调)
3.  Open the **Encryption** tab (加密策略)
4.  Copy **Verification Token**

![Verification Token location](https://mintcdn.com/clawdhub/coDyKPKdey9mC-El/images/feishu-verification-token.png?fit=max&auto=format&n=coDyKPKdey9mC-El&q=85&s=5595773f961373eb8de4267054eef1e8)

### Configure via environment variables

```
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

### Lark (global) domain

If your tenant is on Lark (international), set the domain to `lark` (or a full domain string). You can set it at `channels.feishu.domain` or per account (`channels.feishu.accounts.<id>.domain`).

```
{
  channels: {
    feishu: {
      domain: "lark",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
        },
      },
    },
  },
}
```

### Quota optimization flags

You can reduce Feishu API usage with two optional flags:

*   `typingIndicator` (default `true`): when `false`, skip typing reaction calls.
*   `resolveSenderNames` (default `true`): when `false`, skip sender profile lookup calls.

Set them at top level or per account:

```
{
  channels: {
    feishu: {
      typingIndicator: false,
      resolveSenderNames: false,
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          typingIndicator: true,
          resolveSenderNames: false,
        },
      },
    },
  },
}
```

* * *

## Step 3: Start + test

### 1\. Start the gateway

### 2\. Send a test message

In Feishu, find your bot and send a message.

### 3\. Approve pairing

By default, the bot replies with a pairing code. Approve it:

```
openclaw pairing approve feishu <CODE>
```

After approval, you can chat normally.

* * *

## Overview

*   **Feishu bot channel**: Feishu bot managed by the gateway
*   **Deterministic routing**: replies always return to Feishu
*   **Session isolation**: DMs share a main session; groups are isolated
*   **WebSocket connection**: long connection via Feishu SDK, no public URL needed

* * *

## Access control

### Direct messages

*   **Default**: `dmPolicy: "pairing"` (unknown users get a pairing code)
*   **Approve pairing**:
    
    ```
    openclaw pairing list feishu
    openclaw pairing approve feishu <CODE>
    ```
    
*   **Allowlist mode**: set `channels.feishu.allowFrom` with allowed Open IDs

### Group chats

**1\. Group policy** (`channels.feishu.groupPolicy`):

*   `"open"` = allow everyone in groups (default)
*   `"allowlist"` = only allow `groupAllowFrom`
*   `"disabled"` = disable group messages

**2\. Mention requirement** (`channels.feishu.groups.<chat_id>.requireMention`):

*   `true` = require @mention (default)
*   `false` = respond without mentions

* * *

## Group configuration examples

### Allow all groups, require @mention (default)

```
{
  channels: {
    feishu: {
      groupPolicy: "open",
      // Default requireMention: true
    },
  },
}
```

### Allow all groups, no @mention required

```
{
  channels: {
    feishu: {
      groups: {
        oc_xxx: { requireMention: false },
      },
    },
  },
}
```

### Allow specific groups only

```
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      // Feishu group IDs (chat_id) look like: oc_xxx
      groupAllowFrom: ["oc_xxx", "oc_yyy"],
    },
  },
}
```

### Restrict which senders can message in a group (sender allowlist)

In addition to allowing the group itself, **all messages** in that group are gated by the sender open\_id: only users listed in `groups.<chat_id>.allowFrom` have their messages processed; messages from other members are ignored (this is full sender-level gating, not only for control commands like /reset or /new).

```
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_xxx"],
      groups: {
        oc_xxx: {
          // Feishu user IDs (open_id) look like: ou_xxx
          allowFrom: ["ou_user1", "ou_user2"],
        },
      },
    },
  },
}
```

* * *

## Get group/user IDs

### Group IDs (chat\_id)

Group IDs look like `oc_xxx`. **Method 1 (recommended)**

1.  Start the gateway and @mention the bot in the group
2.  Run `openclaw logs --follow` and look for `chat_id`

**Method 2** Use the Feishu API debugger to list group chats.

### User IDs (open\_id)

User IDs look like `ou_xxx`. **Method 1 (recommended)**

1.  Start the gateway and DM the bot
2.  Run `openclaw logs --follow` and look for `open_id`

**Method 2** Check pairing requests for user Open IDs:

```
openclaw pairing list feishu
```

* * *

## Common commands

| Command | Description |
| --- | --- |
| `/status` | Show bot status |
| `/reset` | Reset the session |
| `/model` | Show/switch model |

> Note: Feishu does not support native command menus yet, so commands must be sent as text.

## Gateway management commands

| Command | Description |
| --- | --- |
| `openclaw gateway status` | Show gateway status |
| `openclaw gateway install` | Install/start gateway service |
| `openclaw gateway stop` | Stop gateway service |
| `openclaw gateway restart` | Restart gateway service |
| `openclaw logs --follow` | Tail gateway logs |

* * *

## Troubleshooting

### Bot does not respond in group chats

1.  Ensure the bot is added to the group
2.  Ensure you @mention the bot (default behavior)
3.  Check `groupPolicy` is not set to `"disabled"`
4.  Check logs: `openclaw logs --follow`

### Bot does not receive messages

1.  Ensure the app is published and approved
2.  Ensure event subscription includes `im.message.receive_v1`
3.  Ensure **long connection** is enabled
4.  Ensure app permissions are complete
5.  Ensure the gateway is running: `openclaw gateway status`
6.  Check logs: `openclaw logs --follow`

### App Secret leak

1.  Reset the App Secret in Feishu Open Platform
2.  Update the App Secret in your config
3.  Restart the gateway

### Message send failures

1.  Ensure the app has `im:message:send_as_bot` permission
2.  Ensure the app is published
3.  Check logs for detailed errors

* * *

## Advanced configuration

### Multiple accounts

```
{
  channels: {
    feishu: {
      defaultAccount: "main",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          botName: "Primary bot",
        },
        backup: {
          appId: "cli_yyy",
          appSecret: "yyy",
          botName: "Backup bot",
          enabled: false,
        },
      },
    },
  },
}
```

`defaultAccount` controls which Feishu account is used when outbound APIs do not specify an `accountId` explicitly.

### Message limits

*   `textChunkLimit`: outbound text chunk size (default: 2000 chars)
*   `mediaMaxMb`: media upload/download limit (default: 30MB)

### Streaming

Feishu supports streaming replies via interactive cards. When enabled, the bot updates a card as it generates text.

```
{
  channels: {
    feishu: {
      streaming: true, // enable streaming card output (default true)
      blockStreaming: true, // enable block-level streaming (default true)
    },
  },
}
```

Set `streaming: false` to wait for the full reply before sending.

### Multi-agent routing

Use `bindings` to route Feishu DMs or groups to different agents.

```
{
  agents: {
    list: [
      { id: "main" },
      {
        id: "clawd-fan",
        workspace: "/home/user/clawd-fan",
        agentDir: "/home/user/.openclaw/agents/clawd-fan/agent",
      },
      {
        id: "clawd-xi",
        workspace: "/home/user/clawd-xi",
        agentDir: "/home/user/.openclaw/agents/clawd-xi/agent",
      },
    ],
  },
  bindings: [
    {
      agentId: "main",
      match: {
        channel: "feishu",
        peer: { kind: "direct", id: "ou_xxx" },
      },
    },
    {
      agentId: "clawd-fan",
      match: {
        channel: "feishu",
        peer: { kind: "direct", id: "ou_yyy" },
      },
    },
    {
      agentId: "clawd-xi",
      match: {
        channel: "feishu",
        peer: { kind: "group", id: "oc_zzz" },
      },
    },
  ],
}
```

Routing fields:

*   `match.channel`: `"feishu"`
*   `match.peer.kind`: `"direct"` or `"group"`
*   `match.peer.id`: user Open ID (`ou_xxx`) or group ID (`oc_xxx`)

See [Get group/user IDs](https://docs.openclaw.ai/channels/feishu#get-groupuser-ids) for lookup tips.

* * *

## Configuration reference

Full configuration: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) Key options:

| Setting | Description | Default |
| --- | --- | --- |
| `channels.feishu.enabled` | Enable/disable channel | `true` |
| `channels.feishu.domain` | API domain (`feishu` or `lark`) | `feishu` |
| `channels.feishu.connectionMode` | Event transport mode | `websocket` |
| `channels.feishu.defaultAccount` | Default account ID for outbound routing | `default` |
| `channels.feishu.verificationToken` | Required for webhook mode | \-  |
| `channels.feishu.webhookPath` | Webhook route path | `/feishu/events` |
| `channels.feishu.webhookHost` | Webhook bind host | `127.0.0.1` |
| `channels.feishu.webhookPort` | Webhook bind port | `3000` |
| `channels.feishu.accounts.<id>.appId` | App ID | \-  |
| `channels.feishu.accounts.<id>.appSecret` | App Secret | \-  |
| `channels.feishu.accounts.<id>.domain` | Per-account API domain override | `feishu` |
| `channels.feishu.dmPolicy` | DM policy | `pairing` |
| `channels.feishu.allowFrom` | DM allowlist (open\_id list) | \-  |
| `channels.feishu.groupPolicy` | Group policy | `open` |
| `channels.feishu.groupAllowFrom` | Group allowlist | \-  |
| `channels.feishu.groups.<chat_id>.requireMention` | Require @mention | `true` |
| `channels.feishu.groups.<chat_id>.enabled` | Enable group | `true` |
| `channels.feishu.textChunkLimit` | Message chunk size | `2000` |
| `channels.feishu.mediaMaxMb` | Media size limit | `30` |
| `channels.feishu.streaming` | Enable streaming card output | `true` |
| `channels.feishu.blockStreaming` | Enable block streaming | `true` |

* * *

## dmPolicy reference

| Value | Behavior |
| --- | --- |
| `"pairing"` | **Default.** Unknown users get a pairing code; must be approved |
| `"allowlist"` | Only users in `allowFrom` can chat |
| `"open"` | Allow all users (requires `"*"` in allowFrom) |
| `"disabled"` | Disable DMs |

* * *

## Supported message types

### Receive

*   ✅ Text
*   ✅ Rich text (post)
*   ✅ Images
*   ✅ Files
*   ✅ Audio
*   ✅ Video
*   ✅ Stickers

### Send

*   ✅ Text
*   ✅ Images
*   ✅ Files
*   ✅ Audio
*   ⚠️ Rich text (partial support)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/bluebubbles -->

# BlueBubbles - OpenClaw

## BlueBubbles (macOS REST)

Status: bundled plugin that talks to the BlueBubbles macOS server over HTTP. **Recommended for iMessage integration** due to its richer API and easier setup compared to the legacy imsg channel.

## Overview

*   Runs on macOS via the BlueBubbles helper app ([bluebubbles.app](https://bluebubbles.app/)).
*   Recommended/tested: macOS Sequoia (15). macOS Tahoe (26) works; edit is currently broken on Tahoe, and group icon updates may report success but not sync.
*   OpenClaw talks to it through its REST API (`GET /api/v1/ping`, `POST /message/text`, `POST /chat/:id/*`).
*   Incoming messages arrive via webhooks; outgoing replies, typing indicators, read receipts, and tapbacks are REST calls.
*   Attachments and stickers are ingested as inbound media (and surfaced to the agent when possible).
*   Pairing/allowlist works the same way as other channels (`/channels/pairing` etc) with `channels.bluebubbles.allowFrom` + pairing codes.
*   Reactions are surfaced as system events just like Slack/Telegram so agents can “mention” them before replying.
*   Advanced features: edit, unsend, reply threading, message effects, group management.

## Quick start

1.  Install the BlueBubbles server on your Mac (follow the instructions at [bluebubbles.app/install](https://bluebubbles.app/install)).
2.  In the BlueBubbles config, enable the web API and set a password.
3.  Run `openclaw onboard` and select BlueBubbles, or configure manually:
    
    ```
    {
      channels: {
        bluebubbles: {
          enabled: true,
          serverUrl: "http://192.168.1.100:1234",
          password: "example-password",
          webhookPath: "/bluebubbles-webhook",
        },
      },
    }
    ```
    
4.  Point BlueBubbles webhooks to your gateway (example: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`).
5.  Start the gateway; it will register the webhook handler and start pairing.

Security note:

*   Always set a webhook password.
*   Webhook authentication is always required. OpenClaw rejects BlueBubbles webhook requests unless they include a password/guid that matches `channels.bluebubbles.password` (for example `?password=<password>` or `x-password`), regardless of loopback/proxy topology.
*   Password authentication is checked before reading/parsing full webhook bodies.

## Keeping Messages.app alive (VM / headless setups)

Some macOS VM / always-on setups can end up with Messages.app going “idle” (incoming events stop until the app is opened/foregrounded). A simple workaround is to **poke Messages every 5 minutes** using an AppleScript + LaunchAgent.

### 1) Save the AppleScript

Save this as:

*   `~/Scripts/poke-messages.scpt`

Example script (non-interactive; does not steal focus):

```
try
  tell application "Messages"
    if not running then
      launch
    end if

    -- Touch the scripting interface to keep the process responsive.
    set _chatCount to (count of chats)
  end tell
on error
  -- Ignore transient failures (first-run prompts, locked session, etc).
end try
```

### 2) Install a LaunchAgent

Save this as:

*   `~/Library/LaunchAgents/com.user.poke-messages.plist`

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.user.poke-messages</string>

    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>-lc</string>
      <string>/usr/bin/osascript &quot;$HOME/Scripts/poke-messages.scpt&quot;</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>StandardOutPath</key>
    <string>/tmp/poke-messages.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/poke-messages.err</string>
  </dict>
</plist>
```

Notes:

*   This runs **every 300 seconds** and **on login**.
*   The first run may trigger macOS **Automation** prompts (`osascript` → Messages). Approve them in the same user session that runs the LaunchAgent.

Load it:

```
launchctl unload ~/Library/LaunchAgents/com.user.poke-messages.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.user.poke-messages.plist
```

## Onboarding

BlueBubbles is available in the interactive setup wizard:

The wizard prompts for:

*   **Server URL** (required): BlueBubbles server address (e.g., `http://192.168.1.100:1234`)
*   **Password** (required): API password from BlueBubbles Server settings
*   **Webhook path** (optional): Defaults to `/bluebubbles-webhook`
*   **DM policy**: pairing, allowlist, open, or disabled
*   **Allow list**: Phone numbers, emails, or chat targets

You can also add BlueBubbles via CLI:

```
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

## Access control (DMs + groups)

DMs:

*   Default: `channels.bluebubbles.dmPolicy = "pairing"`.
*   Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
*   Approve via:
    *   `openclaw pairing list bluebubbles`
    *   `openclaw pairing approve bluebubbles <CODE>`
*   Pairing is the default token exchange. Details: [Pairing](https://docs.openclaw.ai/channels/pairing)

Groups:

*   `channels.bluebubbles.groupPolicy = open | allowlist | disabled` (default: `allowlist`).
*   `channels.bluebubbles.groupAllowFrom` controls who can trigger in groups when `allowlist` is set.

### Mention gating (groups)

BlueBubbles supports mention gating for group chats, matching iMessage/WhatsApp behavior:

*   Uses `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`) to detect mentions.
*   When `requireMention` is enabled for a group, the agent only responds when mentioned.
*   Control commands from authorized senders bypass mention gating.

Per-group configuration:

```
{
  channels: {
    bluebubbles: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }, // default for all groups
        "iMessage;-;chat123": { requireMention: false }, // override for specific group
      },
    },
  },
}
```

### Command gating

*   Control commands (e.g., `/config`, `/model`) require authorization.
*   Uses `allowFrom` and `groupAllowFrom` to determine command authorization.
*   Authorized senders can run control commands even without mentioning in groups.

## Typing + read receipts

*   **Typing indicators**: Sent automatically before and during response generation.
*   **Read receipts**: Controlled by `channels.bluebubbles.sendReadReceipts` (default: `true`).
*   **Typing indicators**: OpenClaw sends typing start events; BlueBubbles clears typing automatically on send or timeout (manual stop via DELETE is unreliable).

```
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false, // disable read receipts
    },
  },
}
```

## Advanced actions

BlueBubbles supports advanced message actions when enabled in config:

```
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true, // tapbacks (default: true)
        edit: true, // edit sent messages (macOS 13+, broken on macOS 26 Tahoe)
        unsend: true, // unsend messages (macOS 13+)
        reply: true, // reply threading by message GUID
        sendWithEffect: true, // message effects (slam, loud, etc.)
        renameGroup: true, // rename group chats
        setGroupIcon: true, // set group chat icon/photo (flaky on macOS 26 Tahoe)
        addParticipant: true, // add participants to groups
        removeParticipant: true, // remove participants from groups
        leaveGroup: true, // leave group chats
        sendAttachment: true, // send attachments/media
      },
    },
  },
}
```

Available actions:

*   **react**: Add/remove tapback reactions (`messageId`, `emoji`, `remove`)
*   **edit**: Edit a sent message (`messageId`, `text`)
*   **unsend**: Unsend a message (`messageId`)
*   **reply**: Reply to a specific message (`messageId`, `text`, `to`)
*   **sendWithEffect**: Send with iMessage effect (`text`, `to`, `effectId`)
*   **renameGroup**: Rename a group chat (`chatGuid`, `displayName`)
*   **setGroupIcon**: Set a group chat’s icon/photo (`chatGuid`, `media`) — flaky on macOS 26 Tahoe (API may return success but the icon does not sync).
*   **addParticipant**: Add someone to a group (`chatGuid`, `address`)
*   **removeParticipant**: Remove someone from a group (`chatGuid`, `address`)
*   **leaveGroup**: Leave a group chat (`chatGuid`)
*   **sendAttachment**: Send media/files (`to`, `buffer`, `filename`, `asVoice`)
    *   Voice memos: set `asVoice: true` with **MP3** or **CAF** audio to send as an iMessage voice message. BlueBubbles converts MP3 → CAF when sending voice memos.

### Message IDs (short vs full)

OpenClaw may surface _short_ message IDs (e.g., `1`, `2`) to save tokens.

*   `MessageSid` / `ReplyToId` can be short IDs.
*   `MessageSidFull` / `ReplyToIdFull` contain the provider full IDs.
*   Short IDs are in-memory; they can expire on restart or cache eviction.
*   Actions accept short or full `messageId`, but short IDs will error if no longer available.

Use full IDs for durable automations and storage:

*   Templates: `{{MessageSidFull}}`, `{{ReplyToIdFull}}`
*   Context: `MessageSidFull` / `ReplyToIdFull` in inbound payloads

See [Configuration](https://docs.openclaw.ai/gateway/configuration) for template variables.

## Block streaming

Control whether responses are sent as a single message or streamed in blocks:

```
{
  channels: {
    bluebubbles: {
      blockStreaming: true, // enable block streaming (off by default)
    },
  },
}
```

*   Inbound attachments are downloaded and stored in the media cache.
*   Media cap via `channels.bluebubbles.mediaMaxMb` for inbound and outbound media (default: 8 MB).
*   Outbound text is chunked to `channels.bluebubbles.textChunkLimit` (default: 4000 chars).

## Configuration reference

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.bluebubbles.enabled`: Enable/disable the channel.
*   `channels.bluebubbles.serverUrl`: BlueBubbles REST API base URL.
*   `channels.bluebubbles.password`: API password.
*   `channels.bluebubbles.webhookPath`: Webhook endpoint path (default: `/bluebubbles-webhook`).
*   `channels.bluebubbles.dmPolicy`: `pairing | allowlist | open | disabled` (default: `pairing`).
*   `channels.bluebubbles.allowFrom`: DM allowlist (handles, emails, E.164 numbers, `chat_id:*`, `chat_guid:*`).
*   `channels.bluebubbles.groupPolicy`: `open | allowlist | disabled` (default: `allowlist`).
*   `channels.bluebubbles.groupAllowFrom`: Group sender allowlist.
*   `channels.bluebubbles.groups`: Per-group config (`requireMention`, etc.).
*   `channels.bluebubbles.sendReadReceipts`: Send read receipts (default: `true`).
*   `channels.bluebubbles.blockStreaming`: Enable block streaming (default: `false`; required for streaming replies).
*   `channels.bluebubbles.textChunkLimit`: Outbound chunk size in chars (default: 4000).
*   `channels.bluebubbles.chunkMode`: `length` (default) splits only when exceeding `textChunkLimit`; `newline` splits on blank lines (paragraph boundaries) before length chunking.
*   `channels.bluebubbles.mediaMaxMb`: Inbound/outbound media cap in MB (default: 8).
*   `channels.bluebubbles.mediaLocalRoots`: Explicit allowlist of absolute local directories permitted for outbound local media paths. Local path sends are denied by default unless this is configured. Per-account override: `channels.bluebubbles.accounts.<accountId>.mediaLocalRoots`.
*   `channels.bluebubbles.historyLimit`: Max group messages for context (0 disables).
*   `channels.bluebubbles.dmHistoryLimit`: DM history limit.
*   `channels.bluebubbles.actions`: Enable/disable specific actions.
*   `channels.bluebubbles.accounts`: Multi-account configuration.

Related global options:

*   `agents.list[].groupChat.mentionPatterns` (or `messages.groupChat.mentionPatterns`).
*   `messages.responsePrefix`.

## Addressing / delivery targets

Prefer `chat_guid` for stable routing:

*   `chat_guid:iMessage;-;+15555550123` (preferred for groups)
*   `chat_id:123`
*   `chat_identifier:...`
*   Direct handles: `+15555550123`, `user@example.com`
    *   If a direct handle does not have an existing DM chat, OpenClaw will create one via `POST /api/v1/chat/new`. This requires the BlueBubbles Private API to be enabled.

## Security

*   Webhook requests are authenticated by comparing `guid`/`password` query params or headers against `channels.bluebubbles.password`. Requests from `localhost` are also accepted.
*   Keep the API password and webhook endpoint secret (treat them like credentials).
*   Localhost trust means a same-host reverse proxy can unintentionally bypass the password. If you proxy the gateway, require auth at the proxy and configure `gateway.trustedProxies`. See [Gateway security](https://docs.openclaw.ai/gateway/security#reverse-proxy-configuration).
*   Enable HTTPS + firewall rules on the BlueBubbles server if exposing it outside your LAN.

## Troubleshooting

*   If typing/read events stop working, check the BlueBubbles webhook logs and verify the gateway path matches `channels.bluebubbles.webhookPath`.
*   Pairing codes expire after one hour; use `openclaw pairing list bluebubbles` and `openclaw pairing approve bluebubbles <code>`.
*   Reactions require the BlueBubbles private API (`POST /api/v1/message/react`); ensure the server version exposes it.
*   Edit/unsend require macOS 13+ and a compatible BlueBubbles server version. On macOS 26 (Tahoe), edit is currently broken due to private API changes.
*   Group icon updates can be flaky on macOS 26 (Tahoe): the API may return success but the new icon does not sync.
*   OpenClaw auto-hides known-broken actions based on the BlueBubbles server’s macOS version. If edit still appears on macOS 26 (Tahoe), disable it manually with `channels.bluebubbles.actions.edit=false`.
*   For status/health info: `openclaw status --all` or `openclaw status --deep`.

For general channel workflow reference, see [Channels](https://docs.openclaw.ai/channels) and the [Plugins](https://docs.openclaw.ai/tools/plugin) guide.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/imessage -->

# iMessage - OpenClaw

## iMessage (legacy: imsg)

Status: legacy external CLI integration. Gateway spawns `imsg rpc` and communicates over JSON-RPC on stdio (no separate daemon/port).

## Quick setup

*   Local Mac (fast path)
    
*   Remote Mac over SSH
    

OpenClaw only requires a stdio-compatible `cliPath`, so you can point `cliPath` at a wrapper script that SSHes to a remote Mac and runs `imsg`.

```
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

Recommended config when attachments are enabled:

```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "user@gateway-host", // used for SCP attachment fetches
      includeAttachments: true,
      // Optional: override allowed attachment roots.
      // Defaults include /Users/*/Library/Messages/Attachments
      attachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      remoteAttachmentRoots: ["/Users/*/Library/Messages/Attachments"],
    },
  },
}
```

If `remoteHost` is not set, OpenClaw attempts to auto-detect it by parsing the SSH wrapper script. `remoteHost` must be `host` or `user@host` (no spaces or SSH options). OpenClaw uses strict host-key checking for SCP, so the relay host key must already exist in `~/.ssh/known_hosts`. Attachment paths are validated against allowed roots (`attachmentRoots` / `remoteAttachmentRoots`).

## Requirements and permissions (macOS)

*   Messages must be signed in on the Mac running `imsg`.
*   Full Disk Access is required for the process context running OpenClaw/`imsg` (Messages DB access).
*   Automation permission is required to send messages through Messages.app.

## Access control and routing

*   DM policy
    
*   Group policy + mentions
    
*   Sessions and deterministic replies
    

`channels.imessage.dmPolicy` controls direct messages:

*   `pairing` (default)
*   `allowlist`
*   `open` (requires `allowFrom` to include `"*"`)
*   `disabled`

Allowlist field: `channels.imessage.allowFrom`.Allowlist entries can be handles or chat targets (`chat_id:*`, `chat_guid:*`, `chat_identifier:*`).

`channels.imessage.groupPolicy` controls group handling:

*   `allowlist` (default when configured)
*   `open`
*   `disabled`

Group sender allowlist: `channels.imessage.groupAllowFrom`.Runtime fallback: if `groupAllowFrom` is unset, iMessage group sender checks fall back to `allowFrom` when available. Runtime note: if `channels.imessage` is completely missing, runtime falls back to `groupPolicy="allowlist"` and logs a warning (even if `channels.defaults.groupPolicy` is set).Mention gating for groups:

*   iMessage has no native mention metadata
*   mention detection uses regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
*   with no configured patterns, mention gating cannot be enforced

Control commands from authorized senders can bypass mention gating in groups.

*   DMs use direct routing; groups use group routing.
*   With default `session.dmScope=main`, iMessage DMs collapse into the agent main session.
*   Group sessions are isolated (`agent:<agentId>:imessage:group:<chat_id>`).
*   Replies route back to iMessage using originating channel/target metadata.

Group-ish thread behavior:Some multi-participant iMessage threads can arrive with `is_group=false`. If that `chat_id` is explicitly configured under `channels.imessage.groups`, OpenClaw treats it as group traffic (group gating + group session isolation).

## Deployment patterns

## Config writes

iMessage allows channel-initiated config writes by default (for `/config set|unset` when `commands.config: true`). Disable:

```
{
  channels: {
    imessage: {
      configWrites: false,
    },
  },
}
```

## Troubleshooting

## Configuration reference pointers

*   [Configuration reference - iMessage](https://docs.openclaw.ai/gateway/configuration-reference#imessage)
*   [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/matrix -->

# Matrix - OpenClaw

## Matrix (plugin)

Matrix is an open, decentralized messaging protocol. OpenClaw connects as a Matrix **user** on any homeserver, so you need a Matrix account for the bot. Once it is logged in, you can DM the bot directly or invite it to rooms (Matrix “groups”). Beeper is a valid client option too, but it requires E2EE to be enabled. Status: supported via plugin (@vector-im/matrix-bot-sdk). Direct messages, rooms, threads, media, reactions, polls (send + poll-start as text), location, and E2EE (with crypto support).

## Plugin required

Matrix ships as a plugin and is not bundled with the core install. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/matrix
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/matrix
```

If you choose Matrix during configure/onboarding and a git checkout is detected, OpenClaw will offer the local install path automatically. Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Setup

1.  Install the Matrix plugin:
    *   From npm: `openclaw plugins install @openclaw/matrix`
    *   From a local checkout: `openclaw plugins install ./extensions/matrix`
2.  Create a Matrix account on a homeserver:
    *   Browse hosting options at [https://matrix.org/ecosystem/hosting/](https://matrix.org/ecosystem/hosting/)
    *   Or host it yourself.
3.  Get an access token for the bot account:
    
    *   Use the Matrix login API with `curl` at your home server:
    
    ```
    curl --request POST \
      --url https://matrix.example.org/_matrix/client/v3/login \
      --header 'Content-Type: application/json' \
      --data '{
      "type": "m.login.password",
      "identifier": {
        "type": "m.id.user",
        "user": "your-user-name"
      },
      "password": "your-password"
    }'
    ```
    
    *   Replace `matrix.example.org` with your homeserver URL.
    *   Or set `channels.matrix.userId` + `channels.matrix.password`: OpenClaw calls the same login endpoint, stores the access token in `~/.openclaw/credentials/matrix/credentials.json`, and reuses it on next start.
4.  Configure credentials:
    *   Env: `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` (or `MATRIX_USER_ID` + `MATRIX_PASSWORD`)
    *   Or config: `channels.matrix.*`
    *   If both are set, config takes precedence.
    *   With access token: user ID is fetched automatically via `/whoami`.
    *   When set, `channels.matrix.userId` should be the full Matrix ID (example: `@bot:example.org`).
5.  Restart the gateway (or finish onboarding).
6.  Start a DM with the bot or invite it to a room from any Matrix client (Element, Beeper, etc.; see [https://matrix.org/ecosystem/clients/](https://matrix.org/ecosystem/clients/)). Beeper requires E2EE, so set `channels.matrix.encryption: true` and verify the device.

Minimal config (access token, user ID auto-fetched):

```
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      dm: { policy: "pairing" },
    },
  },
}
```

E2EE config (end to end encryption enabled):

```
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      encryption: true,
      dm: { policy: "pairing" },
    },
  },
}
```

## Encryption (E2EE)

End-to-end encryption is **supported** via the Rust crypto SDK. Enable with `channels.matrix.encryption: true`:

*   If the crypto module loads, encrypted rooms are decrypted automatically.
*   Outbound media is encrypted when sending to encrypted rooms.
*   On first connection, OpenClaw requests device verification from your other sessions.
*   Verify the device in another Matrix client (Element, etc.) to enable key sharing.
*   If the crypto module cannot be loaded, E2EE is disabled and encrypted rooms will not decrypt; OpenClaw logs a warning.
*   If you see missing crypto module errors (for example, `@matrix-org/matrix-sdk-crypto-nodejs-*`), allow build scripts for `@matrix-org/matrix-sdk-crypto-nodejs` and run `pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs` or fetch the binary with `node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js`.

Crypto state is stored per account + access token in `~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/crypto/` (SQLite database). Sync state lives alongside it in `bot-storage.json`. If the access token (device) changes, a new store is created and the bot must be re-verified for encrypted rooms. **Device verification:** When E2EE is enabled, the bot will request verification from your other sessions on startup. Open Element (or another client) and approve the verification request to establish trust. Once verified, the bot can decrypt messages in encrypted rooms.

## Multi-account

Multi-account support: use `channels.matrix.accounts` with per-account credentials and optional `name`. See [`gateway/configuration`](https://docs.openclaw.ai/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) for the shared pattern. Each account runs as a separate Matrix user on any homeserver. Per-account config inherits from the top-level `channels.matrix` settings and can override any option (DM policy, groups, encryption, etc.).

```
{
  channels: {
    matrix: {
      enabled: true,
      dm: { policy: "pairing" },
      accounts: {
        assistant: {
          name: "Main assistant",
          homeserver: "https://matrix.example.org",
          accessToken: "syt_assistant_***",
          encryption: true,
        },
        alerts: {
          name: "Alerts bot",
          homeserver: "https://matrix.example.org",
          accessToken: "syt_alerts_***",
          dm: { policy: "allowlist", allowFrom: ["@admin:example.org"] },
        },
      },
    },
  },
}
```

Notes:

*   Account startup is serialized to avoid race conditions with concurrent module imports.
*   Env variables (`MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN`, etc.) only apply to the **default** account.
*   Base channel settings (DM policy, group policy, mention gating, etc.) apply to all accounts unless overridden per account.
*   Use `bindings[].match.accountId` to route each account to a different agent.
*   Crypto state is stored per account + access token (separate key stores per account).

## Routing model

*   Replies always go back to Matrix.
*   DMs share the agent’s main session; rooms map to group sessions.

## Access control (DMs)

*   Default: `channels.matrix.dm.policy = "pairing"`. Unknown senders get a pairing code.
*   Approve via:
    *   `openclaw pairing list matrix`
    *   `openclaw pairing approve matrix <CODE>`
*   Public DMs: `channels.matrix.dm.policy="open"` plus `channels.matrix.dm.allowFrom=["*"]`.
*   `channels.matrix.dm.allowFrom` accepts full Matrix user IDs (example: `@user:server`). The wizard resolves display names to user IDs when directory search finds a single exact match.
*   Do not use display names or bare localparts (example: `"Alice"` or `"alice"`). They are ambiguous and are ignored for allowlist matching. Use full `@user:server` IDs.

## Rooms (groups)

*   Default: `channels.matrix.groupPolicy = "allowlist"` (mention-gated). Use `channels.defaults.groupPolicy` to override the default when unset.
*   Runtime note: if `channels.matrix` is completely missing, runtime falls back to `groupPolicy="allowlist"` for room checks (even if `channels.defaults.groupPolicy` is set).
*   Allowlist rooms with `channels.matrix.groups` (room IDs or aliases; names are resolved to IDs when directory search finds a single exact match):

```
{
  channels: {
    matrix: {
      groupPolicy: "allowlist",
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
      groupAllowFrom: ["@owner:example.org"],
    },
  },
}
```

*   `requireMention: false` enables auto-reply in that room.
*   `groups."*"` can set defaults for mention gating across rooms.
*   `groupAllowFrom` restricts which senders can trigger the bot in rooms (full Matrix user IDs).
*   Per-room `users` allowlists can further restrict senders inside a specific room (use full Matrix user IDs).
*   The configure wizard prompts for room allowlists (room IDs, aliases, or names) and resolves names only on an exact, unique match.
*   On startup, OpenClaw resolves room/user names in allowlists to IDs and logs the mapping; unresolved entries are ignored for allowlist matching.
*   Invites are auto-joined by default; control with `channels.matrix.autoJoin` and `channels.matrix.autoJoinAllowlist`.
*   To allow **no rooms**, set `channels.matrix.groupPolicy: "disabled"` (or keep an empty allowlist).
*   Legacy key: `channels.matrix.rooms` (same shape as `groups`).

## Threads

*   Reply threading is supported.
*   `channels.matrix.threadReplies` controls whether replies stay in threads:
    *   `off`, `inbound` (default), `always`
*   `channels.matrix.replyToMode` controls reply-to metadata when not replying in a thread:
    *   `off` (default), `first`, `all`

## Capabilities

| Feature | Status |
| --- | --- |
| Direct messages | ✅ Supported |
| Rooms | ✅ Supported |
| Threads | ✅ Supported |
| Media | ✅ Supported |
| E2EE | ✅ Supported (crypto module required) |
| Reactions | ✅ Supported (send/read via tools) |
| Polls | ✅ Send supported; inbound poll starts are converted to text (responses/ends ignored) |
| Location | ✅ Supported (geo URI; altitude ignored) |
| Native commands | ✅ Supported |

## Troubleshooting

Run this ladder first:

```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Then confirm DM pairing state if needed:

```
openclaw pairing list matrix
```

Common failures:

*   Logged in but room messages ignored: room blocked by `groupPolicy` or room allowlist.
*   DMs ignored: sender pending approval when `channels.matrix.dm.policy="pairing"`.
*   Encrypted rooms fail: crypto support or encryption settings mismatch.

For triage flow: [/channels/troubleshooting](https://docs.openclaw.ai/channels/troubleshooting).

## Configuration reference (Matrix)

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.matrix.enabled`: enable/disable channel startup.
*   `channels.matrix.homeserver`: homeserver URL.
*   `channels.matrix.userId`: Matrix user ID (optional with access token).
*   `channels.matrix.accessToken`: access token.
*   `channels.matrix.password`: password for login (token stored).
*   `channels.matrix.deviceName`: device display name.
*   `channels.matrix.encryption`: enable E2EE (default: false).
*   `channels.matrix.initialSyncLimit`: initial sync limit.
*   `channels.matrix.threadReplies`: `off | inbound | always` (default: inbound).
*   `channels.matrix.textChunkLimit`: outbound text chunk size (chars).
*   `channels.matrix.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
*   `channels.matrix.dm.policy`: `pairing | allowlist | open | disabled` (default: pairing).
*   `channels.matrix.dm.allowFrom`: DM allowlist (full Matrix user IDs). `open` requires `"*"`. The wizard resolves names to IDs when possible.
*   `channels.matrix.groupPolicy`: `allowlist | open | disabled` (default: allowlist).
*   `channels.matrix.groupAllowFrom`: allowlisted senders for group messages (full Matrix user IDs).
*   `channels.matrix.allowlistOnly`: force allowlist rules for DMs + rooms.
*   `channels.matrix.groups`: group allowlist + per-room settings map.
*   `channels.matrix.rooms`: legacy group allowlist/config.
*   `channels.matrix.replyToMode`: reply-to mode for threads/tags.
*   `channels.matrix.mediaMaxMb`: inbound/outbound media cap (MB).
*   `channels.matrix.autoJoin`: invite handling (`always | allowlist | off`, default: always).
*   `channels.matrix.autoJoinAllowlist`: allowed room IDs/aliases for auto-join.
*   `channels.matrix.accounts`: multi-account configuration keyed by account ID (each account inherits top-level settings).
*   `channels.matrix.actions`: per-action tool gating (reactions/messages/pins/memberInfo/channelInfo).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/irc -->

# IRC - OpenClaw

Use IRC when you want OpenClaw in classic channels (`#room`) and direct messages. IRC ships as an extension plugin, but it is configured in the main config under `channels.irc`.

## Quick start

1.  Enable IRC config in `~/.openclaw/openclaw.json`.
2.  Set at least:

```
{
  "channels": {
    "irc": {
      "enabled": true,
      "host": "irc.libera.chat",
      "port": 6697,
      "tls": true,
      "nick": "openclaw-bot",
      "channels": ["#openclaw"]
    }
  }
}
```

3.  Start/restart gateway:

## Security defaults

*   `channels.irc.dmPolicy` defaults to `"pairing"`.
*   `channels.irc.groupPolicy` defaults to `"allowlist"`.
*   With `groupPolicy="allowlist"`, set `channels.irc.groups` to define allowed channels.
*   Use TLS (`channels.irc.tls=true`) unless you intentionally accept plaintext transport.

## Access control

There are two separate “gates” for IRC channels:

1.  **Channel access** (`groupPolicy` + `groups`): whether the bot accepts messages from a channel at all.
2.  **Sender access** (`groupAllowFrom` / per-channel `groups["#channel"].allowFrom`): who is allowed to trigger the bot inside that channel.

Config keys:

*   DM allowlist (DM sender access): `channels.irc.allowFrom`
*   Group sender allowlist (channel sender access): `channels.irc.groupAllowFrom`
*   Per-channel controls (channel + sender + mention rules): `channels.irc.groups["#channel"]`
*   `channels.irc.groupPolicy="open"` allows unconfigured channels (**still mention-gated by default**)

Allowlist entries should use stable sender identities (`nick!user@host`). Bare nick matching is mutable and only enabled when `channels.irc.dangerouslyAllowNameMatching: true`.

### Common gotcha: `allowFrom` is for DMs, not channels

If you see logs like:

*   `irc: drop group sender alice!ident@host (policy=allowlist)`

…it means the sender wasn’t allowed for **group/channel** messages. Fix it by either:

*   setting `channels.irc.groupAllowFrom` (global for all channels), or
*   setting per-channel sender allowlists: `channels.irc.groups["#channel"].allowFrom`

Example (allow anyone in `#tuirc-dev` to talk to the bot):

```
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": { allowFrom: ["*"] },
      },
    },
  },
}
```

## Reply triggering (mentions)

Even if a channel is allowed (via `groupPolicy` + `groups`) and the sender is allowed, OpenClaw defaults to **mention-gating** in group contexts. That means you may see logs like `drop channel … (missing-mention)` unless the message includes a mention pattern that matches the bot. To make the bot reply in an IRC channel **without needing a mention**, disable mention gating for that channel:

```
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": {
          requireMention: false,
          allowFrom: ["*"],
        },
      },
    },
  },
}
```

Or to allow **all** IRC channels (no per-channel allowlist) and still reply without mentions:

```
{
  channels: {
    irc: {
      groupPolicy: "open",
      groups: {
        "*": { requireMention: false, allowFrom: ["*"] },
      },
    },
  },
}
```

## Security note (recommended for public channels)

If you allow `allowFrom: ["*"]` in a public channel, anyone can prompt the bot. To reduce risk, restrict tools for that channel.

### Same tools for everyone in the channel

```
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          tools: {
            deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
          },
        },
      },
    },
  },
}
```

### Different tools per sender (owner gets more power)

Use `toolsBySender` to apply a stricter policy to `"*"` and a looser one to your nick:

```
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          toolsBySender: {
            "*": {
              deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
            },
            "id:eigen": {
              deny: ["gateway", "nodes", "cron"],
            },
          },
        },
      },
    },
  },
}
```

Notes:

*   `toolsBySender` keys should use `id:` for IRC sender identity values: `id:eigen` or `id:eigen!~eigen@174.127.248.171` for stronger matching.
*   Legacy unprefixed keys are still accepted and matched as `id:` only.
*   The first matching sender policy wins; `"*"` is the wildcard fallback.

For more on group access vs mention-gating (and how they interact), see: [/channels/groups](https://docs.openclaw.ai/channels/groups).

## NickServ

To identify with NickServ after connect:

```
{
  "channels": {
    "irc": {
      "nickserv": {
        "enabled": true,
        "service": "NickServ",
        "password": "your-nickserv-password"
      }
    }
  }
}
```

Optional one-time registration on connect:

```
{
  "channels": {
    "irc": {
      "nickserv": {
        "register": true,
        "registerEmail": "bot@example.com"
      }
    }
  }
}
```

Disable `register` after the nick is registered to avoid repeated REGISTER attempts.

## Environment variables

Default account supports:

*   `IRC_HOST`
*   `IRC_PORT`
*   `IRC_TLS`
*   `IRC_NICK`
*   `IRC_USERNAME`
*   `IRC_REALNAME`
*   `IRC_PASSWORD`
*   `IRC_CHANNELS` (comma-separated)
*   `IRC_NICKSERV_PASSWORD`
*   `IRC_NICKSERV_REGISTER_EMAIL`

## Troubleshooting

*   If the bot connects but never replies in channels, verify `channels.irc.groups` **and** whether mention-gating is dropping messages (`missing-mention`). If you want it to reply without pings, set `requireMention:false` for the channel.
*   If login fails, verify nick availability and server password.
*   If TLS fails on a custom network, verify host/port and certificate setup.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/googlechat -->

# Google Chat - OpenClaw

Status: ready for DMs + spaces via Google Chat API webhooks (HTTP only).

## Quick setup (beginner)

1.  Create a Google Cloud project and enable the **Google Chat API**.
    *   Go to: [Google Chat API Credentials](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials)
    *   Enable the API if it is not already enabled.
2.  Create a **Service Account**:
    *   Press **Create Credentials** > **Service Account**.
    *   Name it whatever you want (e.g., `openclaw-chat`).
    *   Leave permissions blank (press **Continue**).
    *   Leave principals with access blank (press **Done**).
3.  Create and download the **JSON Key**:
    *   In the list of service accounts, click on the one you just created.
    *   Go to the **Keys** tab.
    *   Click **Add Key** > **Create new key**.
    *   Select **JSON** and press **Create**.
4.  Store the downloaded JSON file on your gateway host (e.g., `~/.openclaw/googlechat-service-account.json`).
5.  Create a Google Chat app in the [Google Cloud Console Chat Configuration](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat):
    *   Fill in the **Application info**:
        *   **App name**: (e.g. `OpenClaw`)
        *   **Avatar URL**: (e.g. `https://openclaw.ai/logo.png`)
        *   **Description**: (e.g. `Personal AI Assistant`)
    *   Enable **Interactive features**.
    *   Under **Functionality**, check **Join spaces and group conversations**.
    *   Under **Connection settings**, select **HTTP endpoint URL**.
    *   Under **Triggers**, select **Use a common HTTP endpoint URL for all triggers** and set it to your gateway’s public URL followed by `/googlechat`.
        *   _Tip: Run `openclaw status` to find your gateway’s public URL._
    *   Under **Visibility**, check **Make this Chat app available to specific people and groups in <Your Domain>**.
    *   Enter your email address (e.g. `user@example.com`) in the text box.
    *   Click **Save** at the bottom.
6.  **Enable the app status**:
    *   After saving, **refresh the page**.
    *   Look for the **App status** section (usually near the top or bottom after saving).
    *   Change the status to **Live - available to users**.
    *   Click **Save** again.
7.  Configure OpenClaw with the service account path + webhook audience:
    *   Env: `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`
    *   Or config: `channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8.  Set the webhook audience type + value (matches your Chat app config).
9.  Start the gateway. Google Chat will POST to your webhook path.

## Add to Google Chat

Once the gateway is running and your email is added to the visibility list:

1.  Go to [Google Chat](https://chat.google.com/).
2.  Click the **+** (plus) icon next to **Direct Messages**.
3.  In the search bar (where you usually add people), type the **App name** you configured in the Google Cloud Console.
    *   **Note**: The bot will _not_ appear in the “Marketplace” browse list because it is a private app. You must search for it by name.
4.  Select your bot from the results.
5.  Click **Add** or **Chat** to start a 1:1 conversation.
6.  Send “Hello” to trigger the assistant!

## Public URL (Webhook-only)

Google Chat webhooks require a public HTTPS endpoint. For security, **only expose the `/googlechat` path** to the internet. Keep the OpenClaw dashboard and other sensitive endpoints on your private network.

### Option A: Tailscale Funnel (Recommended)

Use Tailscale Serve for the private dashboard and Funnel for the public webhook path. This keeps `/` private while exposing only `/googlechat`.

1.  **Check what address your gateway is bound to:** Note the IP address (e.g., `127.0.0.1`, `0.0.0.0`, or your Tailscale IP like `100.x.x.x`).
2.  **Expose the dashboard to the tailnet only (port 8443):**
    
    ```
    # If bound to localhost (127.0.0.1 or 0.0.0.0):
    tailscale serve --bg --https 8443 http://127.0.0.1:18789
    
    # If bound to Tailscale IP only (e.g., 100.106.161.80):
    tailscale serve --bg --https 8443 http://100.106.161.80:18789
    ```
    
3.  **Expose only the webhook path publicly:**
    
    ```
    # If bound to localhost (127.0.0.1 or 0.0.0.0):
    tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat
    
    # If bound to Tailscale IP only (e.g., 100.106.161.80):
    tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
    ```
    
4.  **Authorize the node for Funnel access:** If prompted, visit the authorization URL shown in the output to enable Funnel for this node in your tailnet policy.
5.  **Verify the configuration:**
    
    ```
    tailscale serve status
    tailscale funnel status
    ```
    

Your public webhook URL will be: `https://<node-name>.<tailnet>.ts.net/googlechat` Your private dashboard stays tailnet-only: `https://<node-name>.<tailnet>.ts.net:8443/` Use the public URL (without `:8443`) in the Google Chat app config.

> Note: This configuration persists across reboots. To remove it later, run `tailscale funnel reset` and `tailscale serve reset`.

### Option B: Reverse Proxy (Caddy)

If you use a reverse proxy like Caddy, only proxy the specific path:

```
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

With this config, any request to `your-domain.com/` will be ignored or returned as 404, while `your-domain.com/googlechat` is safely routed to OpenClaw.

### Option C: Cloudflare Tunnel

Configure your tunnel’s ingress rules to only route the webhook path:

*   **Path**: `/googlechat` -> `http://localhost:18789/googlechat`
*   **Default Rule**: HTTP 404 (Not Found)

## How it works

1.  Google Chat sends webhook POSTs to the gateway. Each request includes an `Authorization: Bearer <token>` header.
    *   OpenClaw verifies bearer auth before reading/parsing full webhook bodies when the header is present.
    *   Google Workspace Add-on requests that carry `authorizationEventObject.systemIdToken` in the body are supported via a stricter pre-auth body budget.
2.  OpenClaw verifies the token against the configured `audienceType` + `audience`:
    *   `audienceType: "app-url"` → audience is your HTTPS webhook URL.
    *   `audienceType: "project-number"` → audience is the Cloud project number.
3.  Messages are routed by space:
    *   DMs use session key `agent:<agentId>:googlechat:dm:<spaceId>`.
    *   Spaces use session key `agent:<agentId>:googlechat:group:<spaceId>`.
4.  DM access is pairing by default. Unknown senders receive a pairing code; approve with:
    *   `openclaw pairing approve googlechat <code>`
5.  Group spaces require @-mention by default. Use `botUser` if mention detection needs the app’s user name.

## Targets

Use these identifiers for delivery and allowlists:

*   Direct messages: `users/<userId>` (recommended).
*   Raw email `name@example.com` is mutable and only used for direct allowlist matching when `channels.googlechat.dangerouslyAllowNameMatching: true`.
*   Deprecated: `users/<email>` is treated as a user id, not an email allowlist.
*   Spaces: `spaces/<spaceId>`.

## Config highlights

```
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      // or serviceAccountRef: { source: "file", provider: "filemain", id: "/channels/googlechat/serviceAccount" }
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; helps mention detection
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Notes:

*   Service account credentials can also be passed inline with `serviceAccount` (JSON string).
*   `serviceAccountRef` is also supported (env/file SecretRef), including per-account refs under `channels.googlechat.accounts.<id>.serviceAccountRef`.
*   Default webhook path is `/googlechat` if `webhookPath` isn’t set.
*   `dangerouslyAllowNameMatching` re-enables mutable email principal matching for allowlists (break-glass compatibility mode).
*   Reactions are available via the `reactions` tool and `channels action` when `actions.reactions` is enabled.
*   `typingIndicator` supports `none`, `message` (default), and `reaction` (reaction requires user OAuth).
*   Attachments are downloaded through the Chat API and stored in the media pipeline (size capped by `mediaMaxMb`).

Secrets reference details: [Secrets Management](https://docs.openclaw.ai/gateway/secrets).

## Troubleshooting

### 405 Method Not Allowed

If Google Cloud Logs Explorer shows errors like:

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

This means the webhook handler isn’t registered. Common causes:

1.  **Channel not configured**: The `channels.googlechat` section is missing from your config. Verify with:
    
    ```
    openclaw config get channels.googlechat
    ```
    
    If it returns “Config path not found”, add the configuration (see [Config highlights](https://docs.openclaw.ai/channels/googlechat#config-highlights)).
2.  **Plugin not enabled**: Check plugin status:
    
    ```
    openclaw plugins list | grep googlechat
    ```
    
    If it shows “disabled”, add `plugins.entries.googlechat.enabled: true` to your config.
3.  **Gateway not restarted**: After adding config, restart the gateway:

Verify the channel is running:

```
openclaw channels status
# Should show: Google Chat default: enabled, configured, ...
```

### Other issues

*   Check `openclaw channels status --probe` for auth errors or missing audience config.
*   If no messages arrive, confirm the Chat app’s webhook URL + event subscriptions.
*   If mention gating blocks replies, set `botUser` to the app’s user resource name and verify `requireMention`.
*   Use `openclaw logs --follow` while sending a test message to see if requests reach the gateway.

Related docs:

*   [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Security](https://docs.openclaw.ai/gateway/security)
*   [Reactions](https://docs.openclaw.ai/tools/reactions)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/discord -->

# Discord - OpenClaw

## Discord (Bot API)

Status: ready for DMs and guild channels via the official Discord gateway.

## Quick setup

You will need to create a new application with a bot, add the bot to your server, and pair it to OpenClaw. We recommend adding your bot to your own private server. If you don’t have one yet, [create one first](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server) (choose **Create My Own > For me and my friends**).

## Recommended: Set up a guild workspace

Once DMs are working, you can set up your Discord server as a full workspace where each channel gets its own agent session with its own context. This is recommended for private servers where it’s just you and your bot.

Now create some channels on your Discord server and start chatting. Your agent can see the channel name, and each channel gets its own isolated session — so you can set up `#coding`, `#home`, `#research`, or whatever fits your workflow.

## Runtime model

*   Gateway owns the Discord connection.
*   Reply routing is deterministic: Discord inbound replies back to Discord.
*   By default (`session.dmScope=main`), direct chats share the agent main session (`agent:main:main`).
*   Guild channels are isolated session keys (`agent:<agentId>:discord:channel:<channelId>`).
*   Group DMs are ignored by default (`channels.discord.dm.groupEnabled=false`).
*   Native slash commands run in isolated command sessions (`agent:<agentId>:discord:slash:<userId>`), while still carrying `CommandTargetSessionKey` to the routed conversation session.

## Forum channels

Discord forum and media channels only accept thread posts. OpenClaw supports two ways to create them:

*   Send a message to the forum parent (`channel:<forumId>`) to auto-create a thread. The thread title uses the first non-empty line of your message.
*   Use `openclaw message thread create` to create a thread directly. Do not pass `--message-id` for forum channels.

Example: send to forum parent to create a thread

```
openclaw message send --channel discord --target channel:<forumId> \
  --message "Topic title\nBody of the post"
```

Example: create a forum thread explicitly

```
openclaw message thread create --channel discord --target channel:<forumId> \
  --thread-name "Topic title" --message "Body of the post"
```

Forum parents do not accept Discord components. If you need components, send to the thread itself (`channel:<threadId>`).

## Interactive components

OpenClaw supports Discord components v2 containers for agent messages. Use the message tool with a `components` payload. Interaction results are routed back to the agent as normal inbound messages and follow the existing Discord `replyToMode` settings. Supported blocks:

*   `text`, `section`, `separator`, `actions`, `media-gallery`, `file`
*   Action rows allow up to 5 buttons or a single select menu
*   Select types: `string`, `user`, `role`, `mentionable`, `channel`

By default, components are single use. Set `components.reusable=true` to allow buttons, selects, and forms to be used multiple times until they expire. To restrict who can click a button, set `allowedUsers` on that button (Discord user IDs, tags, or `*`). When configured, unmatched users receive an ephemeral denial. The `/model` and `/models` slash commands open an interactive model picker with provider and model dropdowns plus a Submit step. The picker reply is ephemeral and only the invoking user can use it. File attachments:

*   `file` blocks must point to an attachment reference (`attachment://<filename>`)
*   Provide the attachment via `media`/`path`/`filePath` (single file); use `media-gallery` for multiple files
*   Use `filename` to override the upload name when it should match the attachment reference

Modal forms:

*   Add `components.modal` with up to 5 fields
*   Field types: `text`, `checkbox`, `radio`, `select`, `role-select`, `user-select`
*   OpenClaw adds a trigger button automatically

Example:

```
{
  channel: "discord",
  action: "send",
  to: "channel:123456789012345678",
  message: "Optional fallback text",
  components: {
    reusable: true,
    text: "Choose a path",
    blocks: [
      {
        type: "actions",
        buttons: [
          {
            label: "Approve",
            style: "success",
            allowedUsers: ["123456789012345678"],
          },
          { label: "Decline", style: "danger" },
        ],
      },
      {
        type: "actions",
        select: {
          type: "string",
          placeholder: "Pick an option",
          options: [
            { label: "Option A", value: "a" },
            { label: "Option B", value: "b" },
          ],
        },
      },
    ],
    modal: {
      title: "Details",
      triggerLabel: "Open form",
      fields: [
        { type: "text", label: "Requester" },
        {
          type: "select",
          label: "Priority",
          options: [
            { label: "Low", value: "low" },
            { label: "High", value: "high" },
          ],
        },
      ],
    },
  },
}
```

## Access control and routing

*   DM policy
    
*   Guild policy
    
*   Mentions and group DMs
    

`channels.discord.dmPolicy` controls DM access (legacy: `channels.discord.dm.policy`):

*   `pairing` (default)
*   `allowlist`
*   `open` (requires `channels.discord.allowFrom` to include `"*"`; legacy: `channels.discord.dm.allowFrom`)
*   `disabled`

If DM policy is not open, unknown users are blocked (or prompted for pairing in `pairing` mode).Multi-account precedence:

*   `channels.discord.accounts.default.allowFrom` applies only to the `default` account.
*   Named accounts inherit `channels.discord.allowFrom` when their own `allowFrom` is unset.
*   Named accounts do not inherit `channels.discord.accounts.default.allowFrom`.

DM target format for delivery:

*   `user:<id>`
*   `<@id>` mention

Bare numeric IDs are ambiguous and rejected unless an explicit user/channel target kind is provided.

Guild handling is controlled by `channels.discord.groupPolicy`:

*   `open`
*   `allowlist`
*   `disabled`

Secure baseline when `channels.discord` exists is `allowlist`.`allowlist` behavior:

*   guild must match `channels.discord.guilds` (`id` preferred, slug accepted)
*   optional sender allowlists: `users` (stable IDs recommended) and `roles` (role IDs only); if either is configured, senders are allowed when they match `users` OR `roles`
*   direct name/tag matching is disabled by default; enable `channels.discord.dangerouslyAllowNameMatching: true` only as break-glass compatibility mode
*   names/tags are supported for `users`, but IDs are safer; `openclaw security audit` warns when name/tag entries are used
*   if a guild has `channels` configured, non-listed channels are denied
*   if a guild has no `channels` block, all channels in that allowlisted guild are allowed

Example:

```
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "123456789012345678": {
          requireMention: true,
          ignoreOtherMentions: true,
          users: ["987654321098765432"],
          roles: ["123456789012345678"],
          channels: {
            general: { allow: true },
            help: { allow: true, requireMention: true },
          },
        },
      },
    },
  },
}
```

If you only set `DISCORD_BOT_TOKEN` and do not create a `channels.discord` block, runtime fallback is `groupPolicy="allowlist"` (with a warning in logs), even if `channels.defaults.groupPolicy` is `open`.

Guild messages are mention-gated by default.Mention detection includes:

*   explicit bot mention
*   configured mention patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
*   implicit reply-to-bot behavior in supported cases

`requireMention` is configured per guild/channel (`channels.discord.guilds...`). `ignoreOtherMentions` optionally drops messages that mention another user/role but not the bot (excluding @everyone/@here).Group DMs:

*   default: ignored (`dm.groupEnabled=false`)
*   optional allowlist via `dm.groupChannels` (channel IDs or slugs)

### Role-based agent routing

Use `bindings[].match.roles` to route Discord guild members to different agents by role ID. Role-based bindings accept role IDs only and are evaluated after peer or parent-peer bindings and before guild-only bindings. If a binding also sets other match fields (for example `peer` + `guildId` + `roles`), all configured fields must match.

```
{
  bindings: [
    {
      agentId: "opus",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
        roles: ["111111111111111111"],
      },
    },
    {
      agentId: "sonnet",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
      },
    },
  ],
}
```

## Developer Portal setup

## Native commands and command auth

*   `commands.native` defaults to `"auto"` and is enabled for Discord.
*   Per-channel override: `channels.discord.commands.native`.
*   `commands.native=false` explicitly clears previously registered Discord native commands.
*   Native command auth uses the same Discord allowlists/policies as normal message handling.
*   Commands may still be visible in Discord UI for users who are not authorized; execution still enforces OpenClaw auth and returns “not authorized”.

See [Slash commands](https://docs.openclaw.ai/tools/slash-commands) for command catalog and behavior. Default slash command settings:

*   `ephemeral: true`

## Feature details

Discord message actions include messaging, channel admin, moderation, presence, and metadata actions. Core examples:

*   messaging: `sendMessage`, `readMessages`, `editMessage`, `deleteMessage`, `threadReply`
*   reactions: `react`, `reactions`, `emojiList`
*   moderation: `timeout`, `kick`, `ban`
*   presence: `setPresence`

Action gates live under `channels.discord.actions.*`. Default gate behavior:

| Action group | Default |
| --- | --- |
| reactions, messages, threads, pins, polls, search, memberInfo, roleInfo, channelInfo, channels, voiceStatus, events, stickers, emojiUploads, stickerUploads, permissions | enabled |
| roles | disabled |
| moderation | disabled |
| presence | disabled |

## Components v2 UI

OpenClaw uses Discord components v2 for exec approvals and cross-context markers. Discord message actions can also accept `components` for custom UI (advanced; requires Carbon component instances), while legacy `embeds` remain available but are not recommended.

*   `channels.discord.ui.components.accentColor` sets the accent color used by Discord component containers (hex).
*   Set per account with `channels.discord.accounts.<id>.ui.components.accentColor`.
*   `embeds` are ignored when components v2 are present.

Example:

```
{
  channels: {
    discord: {
      ui: {
        components: {
          accentColor: "#5865F2",
        },
      },
    },
  },
}
```

## Voice channels

OpenClaw can join Discord voice channels for realtime, continuous conversations. This is separate from voice message attachments. Requirements:

*   Enable native commands (`commands.native` or `channels.discord.commands.native`).
*   Configure `channels.discord.voice`.
*   The bot needs Connect + Speak permissions in the target voice channel.

Use the Discord-only native command `/vc join|leave|status` to control sessions. The command uses the account default agent and follows the same allowlist and group policy rules as other Discord commands. Auto-join example:

```
{
  channels: {
    discord: {
      voice: {
        enabled: true,
        autoJoin: [
          {
            guildId: "123456789012345678",
            channelId: "234567890123456789",
          },
        ],
        daveEncryption: true,
        decryptionFailureTolerance: 24,
        tts: {
          provider: "openai",
          openai: { voice: "alloy" },
        },
      },
    },
  },
}
```

Notes:

*   `voice.tts` overrides `messages.tts` for voice playback only.
*   Voice transcript turns derive owner status from Discord `allowFrom` (or `dm.allowFrom`); non-owner speakers cannot access owner-only tools (for example `gateway` and `cron`).
*   Voice is enabled by default; set `channels.discord.voice.enabled=false` to disable it.
*   `voice.daveEncryption` and `voice.decryptionFailureTolerance` pass through to `@discordjs/voice` join options.
*   `@discordjs/voice` defaults are `daveEncryption=true` and `decryptionFailureTolerance=24` if unset.
*   OpenClaw also watches receive decrypt failures and auto-recovers by leaving/rejoining the voice channel after repeated failures in a short window.
*   If receive logs repeatedly show `DecryptionFailed(UnencryptedWhenPassthroughDisabled)`, this may be the upstream `@discordjs/voice` receive bug tracked in [discord.js #11419](https://github.com/discordjs/discord.js/issues/11419).

## Voice messages

Discord voice messages show a waveform preview and require OGG/Opus audio plus metadata. OpenClaw generates the waveform automatically, but it needs `ffmpeg` and `ffprobe` available on the gateway host to inspect and convert audio files. Requirements and constraints:

*   Provide a **local file path** (URLs are rejected).
*   Omit text content (Discord does not allow text + voice message in the same payload).
*   Any audio format is accepted; OpenClaw converts to OGG/Opus when needed.

Example:

```
message(action="send", channel="discord", target="channel:123", path="/path/to/audio.mp3", asVoice=true)
```

## Troubleshooting

## Configuration reference pointers

Primary reference:

*   [Configuration reference - Discord](https://docs.openclaw.ai/gateway/configuration-reference#discord)

High-signal Discord fields:

*   startup/auth: `enabled`, `token`, `accounts.*`, `allowBots`
*   policy: `groupPolicy`, `dm.*`, `guilds.*`, `guilds.*.channels.*`
*   command: `commands.native`, `commands.useAccessGroups`, `configWrites`, `slashCommand.*`
*   event queue: `eventQueue.listenerTimeout` (listener budget), `eventQueue.maxQueueSize`, `eventQueue.maxConcurrency`
*   inbound worker: `inboundWorker.runTimeoutMs`
*   reply/history: `replyToMode`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
*   delivery: `textChunkLimit`, `chunkMode`, `maxLinesPerMessage`
*   streaming: `streaming` (legacy alias: `streamMode`), `draftChunk`, `blockStreaming`, `blockStreamingCoalesce`
*   media/retry: `mediaMaxMb`, `retry`
    *   `mediaMaxMb` caps outbound Discord uploads (default: `8MB`)
*   actions: `actions.*`
*   presence: `activity`, `status`, `activityType`, `activityUrl`
*   UI: `ui.components.accentColor`
*   features: `threadBindings`, top-level `bindings[]` (`type: "acp"`), `pluralkit`, `execApprovals`, `intents`, `agentComponents`, `heartbeat`, `responsePrefix`

## Safety and operations

*   Treat bot tokens as secrets (`DISCORD_BOT_TOKEN` preferred in supervised environments).
*   Grant least-privilege Discord permissions.
*   If command deploy/state is stale, restart gateway and re-check with `openclaw channels status --probe`.

*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [Channel routing](https://docs.openclaw.ai/channels/channel-routing)
*   [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
*   [Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)
*   [Slash commands](https://docs.openclaw.ai/tools/slash-commands)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/mattermost -->

# Mattermost - OpenClaw

## Mattermost (plugin)

Status: supported via plugin (bot token + WebSocket events). Channels, groups, and DMs are supported. Mattermost is a self-hostable team messaging platform; see the official site at [mattermost.com](https://mattermost.com/) for product details and downloads.

## Plugin required

Mattermost ships as a plugin and is not bundled with the core install. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/mattermost
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/mattermost
```

If you choose Mattermost during configure/onboarding and a git checkout is detected, OpenClaw will offer the local install path automatically. Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup

1.  Install the Mattermost plugin.
2.  Create a Mattermost bot account and copy the **bot token**.
3.  Copy the Mattermost **base URL** (e.g., `https://chat.example.com`).
4.  Configure OpenClaw and start the gateway.

Minimal config:

```
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

## Native slash commands

Native slash commands are opt-in. When enabled, OpenClaw registers `oc_*` slash commands via the Mattermost API and receives callback POSTs on the gateway HTTP server.

```
{
  channels: {
    mattermost: {
      commands: {
        native: true,
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        // Use when Mattermost cannot reach the gateway directly (reverse proxy/public URL).
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
    },
  },
}
```

Notes:

*   `native: "auto"` defaults to disabled for Mattermost. Set `native: true` to enable.
*   If `callbackUrl` is omitted, OpenClaw derives one from gateway host/port + `callbackPath`.
*   For multi-account setups, `commands` can be set at the top level or under `channels.mattermost.accounts.<id>.commands` (account values override top-level fields).
*   Command callbacks are validated with per-command tokens and fail closed when token checks fail.
*   Reachability requirement: the callback endpoint must be reachable from the Mattermost server.
    *   Do not set `callbackUrl` to `localhost` unless Mattermost runs on the same host/network namespace as OpenClaw.
    *   Do not set `callbackUrl` to your Mattermost base URL unless that URL reverse-proxies `/api/channels/mattermost/command` to OpenClaw.
    *   A quick check is `curl https://<gateway-host>/api/channels/mattermost/command`; a GET should return `405 Method Not Allowed` from OpenClaw, not `404`.
*   Mattermost egress allowlist requirement:
    *   If your callback targets private/tailnet/internal addresses, set Mattermost `ServiceSettings.AllowedUntrustedInternalConnections` to include the callback host/domain.
    *   Use host/domain entries, not full URLs.
        *   Good: `gateway.tailnet-name.ts.net`
        *   Bad: `https://gateway.tailnet-name.ts.net`

## Environment variables (default account)

Set these on the gateway host if you prefer env vars:

*   `MATTERMOST_BOT_TOKEN=...`
*   `MATTERMOST_URL=https://chat.example.com`

Env vars apply only to the **default** account (`default`). Other accounts must use config values.

## Chat modes

Mattermost responds to DMs automatically. Channel behavior is controlled by `chatmode`:

*   `oncall` (default): respond only when @mentioned in channels.
*   `onmessage`: respond to every channel message.
*   `onchar`: respond when a message starts with a trigger prefix.

Config example:

```
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

*   `onchar` still responds to explicit @mentions.
*   `channels.mattermost.requireMention` is honored for legacy configs but `chatmode` is preferred.

## Access control (DMs)

*   Default: `channels.mattermost.dmPolicy = "pairing"` (unknown senders get a pairing code).
*   Approve via:
    *   `openclaw pairing list mattermost`
    *   `openclaw pairing approve mattermost <CODE>`
*   Public DMs: `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.

## Channels (groups)

*   Default: `channels.mattermost.groupPolicy = "allowlist"` (mention-gated).
*   Allowlist senders with `channels.mattermost.groupAllowFrom` (user IDs recommended).
*   `@username` matching is mutable and only enabled when `channels.mattermost.dangerouslyAllowNameMatching: true`.
*   Open channels: `channels.mattermost.groupPolicy="open"` (mention-gated).
*   Runtime note: if `channels.mattermost` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks (even if `channels.defaults.groupPolicy` is set).

## Targets for outbound delivery

Use these target formats with `openclaw message send` or cron/webhooks:

*   `channel:<id>` for a channel
*   `user:<id>` for a DM
*   `@username` for a DM (resolved via the Mattermost API)

Bare IDs are treated as channels.

*   Use `message action=react` with `channel=mattermost`.
*   `messageId` is the Mattermost post id.
*   `emoji` accepts names like `thumbsup` or `:+1:` (colons are optional).
*   Set `remove=true` (boolean) to remove a reaction.
*   Reaction add/remove events are forwarded as system events to the routed agent session.

Examples:

```
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup remove=true
```

Config:

*   `channels.mattermost.actions.reactions`: enable/disable reaction actions (default true).
*   Per-account override: `channels.mattermost.accounts.<id>.actions.reactions`.

Send messages with clickable buttons. When a user clicks a button, the agent receives the selection and can respond. Enable buttons by adding `inlineButtons` to the channel capabilities:

```
{
  channels: {
    mattermost: {
      capabilities: ["inlineButtons"],
    },
  },
}
```

Use `message action=send` with a `buttons` parameter. Buttons are a 2D array (rows of buttons):

```
message action=send channel=mattermost target=channel:<channelId> buttons=[[{"text":"Yes","callback_data":"yes"},{"text":"No","callback_data":"no"}]]
```

Button fields:

*   `text` (required): display label.
*   `callback_data` (required): value sent back on click (used as the action ID).
*   `style` (optional): `"default"`, `"primary"`, or `"danger"`.

When a user clicks a button:

1.  All buttons are replaced with a confirmation line (e.g., ”✓ **Yes** selected by @user”).
2.  The agent receives the selection as an inbound message and responds.

Notes:

*   Button callbacks use HMAC-SHA256 verification (automatic, no config needed).
*   Mattermost strips callback data from its API responses (security feature), so all buttons are removed on click — partial removal is not possible.
*   Action IDs containing hyphens or underscores are sanitized automatically (Mattermost routing limitation).

Config:

*   `channels.mattermost.capabilities`: array of capability strings. Add `"inlineButtons"` to enable the buttons tool description in the agent system prompt.
*   `channels.mattermost.interactions.callbackBaseUrl`: optional external base URL for button callbacks (for example `https://gateway.example.com`). Use this when Mattermost cannot reach the gateway at its bind host directly.
*   In multi-account setups, you can also set the same field under `channels.mattermost.accounts.<id>.interactions.callbackBaseUrl`.
*   If `interactions.callbackBaseUrl` is omitted, OpenClaw derives the callback URL from `gateway.customBindHost` + `gateway.port`, then falls back to `http://localhost:<port>`.
*   Reachability rule: the button callback URL must be reachable from the Mattermost server. `localhost` only works when Mattermost and OpenClaw run on the same host/network namespace.
*   If your callback target is private/tailnet/internal, add its host/domain to Mattermost `ServiceSettings.AllowedUntrustedInternalConnections`.

### Direct API integration (external scripts)

External scripts and webhooks can post buttons directly via the Mattermost REST API instead of going through the agent’s `message` tool. Use `buildButtonAttachments()` from the extension when possible; if posting raw JSON, follow these rules: **Payload structure:**

```
{
  channel_id: "<channelId>",
  message: "Choose an option:",
  props: {
    attachments: [
      {
        actions: [
          {
            id: "mybutton01", // alphanumeric only — see below
            type: "button", // required, or clicks are silently ignored
            name: "Approve", // display label
            style: "primary", // optional: "default", "primary", "danger"
            integration: {
              url: "https://gateway.example.com/mattermost/interactions/default",
              context: {
                action_id: "mybutton01", // must match button id (for name lookup)
                action: "approve",
                // ... any custom fields ...
                _token: "<hmac>", // see HMAC section below
              },
            },
          },
        ],
      },
    ],
  },
}
```

**Critical rules:**

1.  Attachments go in `props.attachments`, not top-level `attachments` (silently ignored).
2.  Every action needs `type: "button"` — without it, clicks are swallowed silently.
3.  Every action needs an `id` field — Mattermost ignores actions without IDs.
4.  Action `id` must be **alphanumeric only** (`[a-zA-Z0-9]`). Hyphens and underscores break Mattermost’s server-side action routing (returns 404). Strip them before use.
5.  `context.action_id` must match the button’s `id` so the confirmation message shows the button name (e.g., “Approve”) instead of a raw ID.
6.  `context.action_id` is required — the interaction handler returns 400 without it.

**HMAC token generation:** The gateway verifies button clicks with HMAC-SHA256. External scripts must generate tokens that match the gateway’s verification logic:

1.  Derive the secret from the bot token: `HMAC-SHA256(key="openclaw-mattermost-interactions", data=botToken)`
2.  Build the context object with all fields **except** `_token`.
3.  Serialize with **sorted keys** and **no spaces** (the gateway uses `JSON.stringify` with sorted keys, which produces compact output).
4.  Sign: `HMAC-SHA256(key=secret, data=serializedContext)`
5.  Add the resulting hex digest as `_token` in the context.

Python example:

```
import hmac, hashlib, json

secret = hmac.new(
    b"openclaw-mattermost-interactions",
    bot_token.encode(), hashlib.sha256
).hexdigest()

ctx = {"action_id": "mybutton01", "action": "approve"}
payload = json.dumps(ctx, sort_keys=True, separators=(",", ":"))
token = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

context = {**ctx, "_token": token}
```

Common HMAC pitfalls:

*   Python’s `json.dumps` adds spaces by default (`{"key": "val"}`). Use `separators=(",", ":")` to match JavaScript’s compact output (`{"key":"val"}`).
*   Always sign **all** context fields (minus `_token`). The gateway strips `_token` then signs everything remaining. Signing a subset causes silent verification failure.
*   Use `sort_keys=True` — the gateway sorts keys before signing, and Mattermost may reorder context fields when storing the payload.
*   Derive the secret from the bot token (deterministic), not random bytes. The secret must be the same across the process that creates buttons and the gateway that verifies.

## Directory adapter

The Mattermost plugin includes a directory adapter that resolves channel and user names via the Mattermost API. This enables `#channel-name` and `@username` targets in `openclaw message send` and cron/webhook deliveries. No configuration is needed — the adapter uses the bot token from the account config.

## Multi-account

Mattermost supports multiple accounts under `channels.mattermost.accounts`:

```
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

## Troubleshooting

*   No replies in channels: ensure the bot is in the channel and mention it (oncall), use a trigger prefix (onchar), or set `chatmode: "onmessage"`.
*   Auth errors: check the bot token, base URL, and whether the account is enabled.
*   Multi-account issues: env vars only apply to the `default` account.
*   Buttons appear as white boxes: the agent may be sending malformed button data. Check that each button has both `text` and `callback_data` fields.
*   Buttons render but clicks do nothing: verify `AllowedUntrustedInternalConnections` in Mattermost server config includes `127.0.0.1 localhost`, and that `EnablePostActionIntegration` is `true` in ServiceSettings.
*   Buttons return 404 on click: the button `id` likely contains hyphens or underscores. Mattermost’s action router breaks on non-alphanumeric IDs. Use `[a-zA-Z0-9]` only.
*   Gateway logs `invalid _token`: HMAC mismatch. Check that you sign all context fields (not a subset), use sorted keys, and use compact JSON (no spaces). See the HMAC section above.
*   Gateway logs `missing _token in context`: the `_token` field is not in the button’s context. Ensure it is included when building the integration payload.
*   Confirmation shows raw ID instead of button name: `context.action_id` does not match the button’s `id`. Set both to the same sanitized value.
*   Agent doesn’t know about buttons: add `capabilities: ["inlineButtons"]` to the Mattermost channel config.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/nextcloud-talk -->

# Nextcloud Talk - OpenClaw

## Nextcloud Talk (plugin)

Status: supported via plugin (webhook bot). Direct messages, rooms, reactions, and markdown messages are supported.

## Plugin required

Nextcloud Talk ships as a plugin and is not bundled with the core install. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/nextcloud-talk
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/nextcloud-talk
```

If you choose Nextcloud Talk during configure/onboarding and a git checkout is detected, OpenClaw will offer the local install path automatically. Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup (beginner)

1.  Install the Nextcloud Talk plugin.
2.  On your Nextcloud server, create a bot:
    
    ```
    ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
    ```
    
3.  Enable the bot in the target room settings.
4.  Configure OpenClaw:
    *   Config: `channels.nextcloud-talk.baseUrl` + `channels.nextcloud-talk.botSecret`
    *   Or env: `NEXTCLOUD_TALK_BOT_SECRET` (default account only)
5.  Restart the gateway (or finish onboarding).

Minimal config:

```
{
  channels: {
    "nextcloud-talk": {
      enabled: true,
      baseUrl: "https://cloud.example.com",
      botSecret: "shared-secret",
      dmPolicy: "pairing",
    },
  },
}
```

## Notes

*   Bots cannot initiate DMs. The user must message the bot first.
*   Webhook URL must be reachable by the Gateway; set `webhookPublicUrl` if behind a proxy.
*   Media uploads are not supported by the bot API; media is sent as URLs.
*   The webhook payload does not distinguish DMs vs rooms; set `apiUser` + `apiPassword` to enable room-type lookups (otherwise DMs are treated as rooms).

## Access control (DMs)

*   Default: `channels.nextcloud-talk.dmPolicy = "pairing"`. Unknown senders get a pairing code.
*   Approve via:
    *   `openclaw pairing list nextcloud-talk`
    *   `openclaw pairing approve nextcloud-talk <CODE>`
*   Public DMs: `channels.nextcloud-talk.dmPolicy="open"` plus `channels.nextcloud-talk.allowFrom=["*"]`.
*   `allowFrom` matches Nextcloud user IDs only; display names are ignored.

## Rooms (groups)

*   Default: `channels.nextcloud-talk.groupPolicy = "allowlist"` (mention-gated).
*   Allowlist rooms with `channels.nextcloud-talk.rooms`:

```
{
  channels: {
    "nextcloud-talk": {
      rooms: {
        "room-token": { requireMention: true },
      },
    },
  },
}
```

*   To allow no rooms, keep the allowlist empty or set `channels.nextcloud-talk.groupPolicy="disabled"`.

## Capabilities

| Feature | Status |
| --- | --- |
| Direct messages | Supported |
| Rooms | Supported |
| Threads | Not supported |
| Media | URL-only |
| Reactions | Supported |
| Native commands | Not supported |

## Configuration reference (Nextcloud Talk)

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.nextcloud-talk.enabled`: enable/disable channel startup.
*   `channels.nextcloud-talk.baseUrl`: Nextcloud instance URL.
*   `channels.nextcloud-talk.botSecret`: bot shared secret.
*   `channels.nextcloud-talk.botSecretFile`: secret file path.
*   `channels.nextcloud-talk.apiUser`: API user for room lookups (DM detection).
*   `channels.nextcloud-talk.apiPassword`: API/app password for room lookups.
*   `channels.nextcloud-talk.apiPasswordFile`: API password file path.
*   `channels.nextcloud-talk.webhookPort`: webhook listener port (default: 8788).
*   `channels.nextcloud-talk.webhookHost`: webhook host (default: 0.0.0.0).
*   `channels.nextcloud-talk.webhookPath`: webhook path (default: /nextcloud-talk-webhook).
*   `channels.nextcloud-talk.webhookPublicUrl`: externally reachable webhook URL.
*   `channels.nextcloud-talk.dmPolicy`: `pairing | allowlist | open | disabled`.
*   `channels.nextcloud-talk.allowFrom`: DM allowlist (user IDs). `open` requires `"*"`.
*   `channels.nextcloud-talk.groupPolicy`: `allowlist | open | disabled`.
*   `channels.nextcloud-talk.groupAllowFrom`: group allowlist (user IDs).
*   `channels.nextcloud-talk.rooms`: per-room settings and allowlist.
*   `channels.nextcloud-talk.historyLimit`: group history limit (0 disables).
*   `channels.nextcloud-talk.dmHistoryLimit`: DM history limit (0 disables).
*   `channels.nextcloud-talk.dms`: per-DM overrides (historyLimit).
*   `channels.nextcloud-talk.textChunkLimit`: outbound text chunk size (chars).
*   `channels.nextcloud-talk.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
*   `channels.nextcloud-talk.blockStreaming`: disable block streaming for this channel.
*   `channels.nextcloud-talk.blockStreamingCoalesce`: block streaming coalesce tuning.
*   `channels.nextcloud-talk.mediaMaxMb`: inbound media cap (MB).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/msteams -->

# Microsoft Teams - OpenClaw

## Microsoft Teams (plugin)

> “Abandon all hope, ye who enter here.”

Updated: 2026-01-21 Status: text + DM attachments are supported; channel/group file sending requires `sharePointSiteId` + Graph permissions (see [Sending files in group chats](https://docs.openclaw.ai/channels/msteams#sending-files-in-group-chats)). Polls are sent via Adaptive Cards.

## Plugin required

Microsoft Teams ships as a plugin and is not bundled with the core install. **Breaking change (2026.1.15):** MS Teams moved out of core. If you use it, you must install the plugin. Explainable: keeps core installs lighter and lets MS Teams dependencies update independently. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/msteams
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/msteams
```

If you choose Teams during configure/onboarding and a git checkout is detected, OpenClaw will offer the local install path automatically. Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup (beginner)

1.  Install the Microsoft Teams plugin.
2.  Create an **Azure Bot** (App ID + client secret + tenant ID).
3.  Configure OpenClaw with those credentials.
4.  Expose `/api/messages` (port 3978 by default) via a public URL or tunnel.
5.  Install the Teams app package and start the gateway.

Minimal config:

```
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      appPassword: "<APP_PASSWORD>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Note: group chats are blocked by default (`channels.msteams.groupPolicy: "allowlist"`). To allow group replies, set `channels.msteams.groupAllowFrom` (or use `groupPolicy: "open"` to allow any member, mention-gated).

## Goals

*   Talk to OpenClaw via Teams DMs, group chats, or channels.
*   Keep routing deterministic: replies always go back to the channel they arrived on.
*   Default to safe channel behavior (mentions required unless configured otherwise).

## Config writes

By default, Microsoft Teams is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`). Disable with:

```
{
  channels: { msteams: { configWrites: false } },
}
```

## Access control (DMs + groups)

**DM access**

*   Default: `channels.msteams.dmPolicy = "pairing"`. Unknown senders are ignored until approved.
*   `channels.msteams.allowFrom` should use stable AAD object IDs.
*   UPNs/display names are mutable; direct matching is disabled by default and only enabled with `channels.msteams.dangerouslyAllowNameMatching: true`.
*   The wizard can resolve names to IDs via Microsoft Graph when credentials allow.

**Group access**

*   Default: `channels.msteams.groupPolicy = "allowlist"` (blocked unless you add `groupAllowFrom`). Use `channels.defaults.groupPolicy` to override the default when unset.
*   `channels.msteams.groupAllowFrom` controls which senders can trigger in group chats/channels (falls back to `channels.msteams.allowFrom`).
*   Set `groupPolicy: "open"` to allow any member (still mention‑gated by default).
*   To allow **no channels**, set `channels.msteams.groupPolicy: "disabled"`.

Example:

```
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
  },
}
```

**Teams + channel allowlist**

*   Scope group/channel replies by listing teams and channels under `channels.msteams.teams`.
*   Keys can be team IDs or names; channel keys can be conversation IDs or names.
*   When `groupPolicy="allowlist"` and a teams allowlist is present, only listed teams/channels are accepted (mention‑gated).
*   The configure wizard accepts `Team/Channel` entries and stores them for you.
*   On startup, OpenClaw resolves team/channel and user allowlist names to IDs (when Graph permissions allow) and logs the mapping; unresolved entries are kept as typed.

Example:

```
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

## How it works

1.  Install the Microsoft Teams plugin.
2.  Create an **Azure Bot** (App ID + secret + tenant ID).
3.  Build a **Teams app package** that references the bot and includes the RSC permissions below.
4.  Upload/install the Teams app into a team (or personal scope for DMs).
5.  Configure `msteams` in `~/.openclaw/openclaw.json` (or env vars) and start the gateway.
6.  The gateway listens for Bot Framework webhook traffic on `/api/messages` by default.

## Azure Bot Setup (Prerequisites)

Before configuring OpenClaw, you need to create an Azure Bot resource.

### Step 1: Create Azure Bot

1.  Go to [Create Azure Bot](https://portal.azure.com/#create/Microsoft.AzureBot)
2.  Fill in the **Basics** tab:
    
    | Field | Value |
    | --- | --- |
    | **Bot handle** | Your bot name, e.g., `openclaw-msteams` (must be unique) |
    | **Subscription** | Select your Azure subscription |
    | **Resource group** | Create new or use existing |
    | **Pricing tier** | **Free** for dev/testing |
    | **Type of App** | **Single Tenant** (recommended - see note below) |
    | **Creation type** | **Create new Microsoft App ID** |
    

> **Deprecation notice:** Creation of new multi-tenant bots was deprecated after 2025-07-31. Use **Single Tenant** for new bots.

3.  Click **Review + create** → **Create** (wait ~1-2 minutes)

### Step 2: Get Credentials

1.  Go to your Azure Bot resource → **Configuration**
2.  Copy **Microsoft App ID** → this is your `appId`
3.  Click **Manage Password** → go to the App Registration
4.  Under **Certificates & secrets** → **New client secret** → copy the **Value** → this is your `appPassword`
5.  Go to **Overview** → copy **Directory (tenant) ID** → this is your `tenantId`

### Step 3: Configure Messaging Endpoint

1.  In Azure Bot → **Configuration**
2.  Set **Messaging endpoint** to your webhook URL:
    *   Production: `https://your-domain.com/api/messages`
    *   Local dev: Use a tunnel (see [Local Development](https://docs.openclaw.ai/channels/msteams#local-development-tunneling) below)

### Step 4: Enable Teams Channel

1.  In Azure Bot → **Channels**
2.  Click **Microsoft Teams** → Configure → Save
3.  Accept the Terms of Service

## Local Development (Tunneling)

Teams can’t reach `localhost`. Use a tunnel for local development: **Option A: ngrok**

```
ngrok http 3978
# Copy the https URL, e.g., https://abc123.ngrok.io
# Set messaging endpoint to: https://abc123.ngrok.io/api/messages
```

**Option B: Tailscale Funnel**

```
tailscale funnel 3978
# Use your Tailscale funnel URL as the messaging endpoint
```

## Teams Developer Portal (Alternative)

Instead of manually creating a manifest ZIP, you can use the [Teams Developer Portal](https://dev.teams.microsoft.com/apps):

1.  Click **\+ New app**
2.  Fill in basic info (name, description, developer info)
3.  Go to **App features** → **Bot**
4.  Select **Enter a bot ID manually** and paste your Azure Bot App ID
5.  Check scopes: **Personal**, **Team**, **Group Chat**
6.  Click **Distribute** → **Download app package**
7.  In Teams: **Apps** → **Manage your apps** → **Upload a custom app** → select the ZIP

This is often easier than hand-editing JSON manifests.

## Testing the Bot

**Option A: Azure Web Chat (verify webhook first)**

1.  In Azure Portal → your Azure Bot resource → **Test in Web Chat**
2.  Send a message - you should see a response
3.  This confirms your webhook endpoint works before Teams setup

**Option B: Teams (after app installation)**

1.  Install the Teams app (sideload or org catalog)
2.  Find the bot in Teams and send a DM
3.  Check gateway logs for incoming activity

## Setup (minimal text-only)

1.  **Install the Microsoft Teams plugin**
    *   From npm: `openclaw plugins install @openclaw/msteams`
    *   From a local checkout: `openclaw plugins install ./extensions/msteams`
2.  **Bot registration**
    *   Create an Azure Bot (see above) and note:
        *   App ID
        *   Client secret (App password)
        *   Tenant ID (single-tenant)
3.  **Teams app manifest**
    *   Include a `bot` entry with `botId = <App ID>`.
    *   Scopes: `personal`, `team`, `groupChat`.
    *   `supportsFiles: true` (required for personal scope file handling).
    *   Add RSC permissions (below).
    *   Create icons: `outline.png` (32x32) and `color.png` (192x192).
    *   Zip all three files together: `manifest.json`, `outline.png`, `color.png`.
4.  **Configure OpenClaw**
    
    ```
    {
      "msteams": {
        "enabled": true,
        "appId": "<APP_ID>",
        "appPassword": "<APP_PASSWORD>",
        "tenantId": "<TENANT_ID>",
        "webhook": { "port": 3978, "path": "/api/messages" }
      }
    }
    ```
    
    You can also use environment variables instead of config keys:
    *   `MSTEAMS_APP_ID`
    *   `MSTEAMS_APP_PASSWORD`
    *   `MSTEAMS_TENANT_ID`
5.  **Bot endpoint**
    *   Set the Azure Bot Messaging Endpoint to:
        *   `https://<host>:3978/api/messages` (or your chosen path/port).
6.  **Run the gateway**
    *   The Teams channel starts automatically when the plugin is installed and `msteams` config exists with credentials.

## History context

*   `channels.msteams.historyLimit` controls how many recent channel/group messages are wrapped into the prompt.
*   Falls back to `messages.groupChat.historyLimit`. Set `0` to disable (default 50).
*   DM history can be limited with `channels.msteams.dmHistoryLimit` (user turns). Per-user overrides: `channels.msteams.dms["<user_id>"].historyLimit`.

## Current Teams RSC Permissions (Manifest)

These are the **existing resourceSpecific permissions** in our Teams app manifest. They only apply inside the team/chat where the app is installed. **For channels (team scope):**

*   `ChannelMessage.Read.Group` (Application) - receive all channel messages without @mention
*   `ChannelMessage.Send.Group` (Application)
*   `Member.Read.Group` (Application)
*   `Owner.Read.Group` (Application)
*   `ChannelSettings.Read.Group` (Application)
*   `TeamMember.Read.Group` (Application)
*   `TeamSettings.Read.Group` (Application)

**For group chats:**

*   `ChatMessage.Read.Chat` (Application) - receive all group chat messages without @mention

## Example Teams Manifest (redacted)

Minimal, valid example with the required fields. Replace IDs and URLs.

```
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json",
  "manifestVersion": "1.23",
  "version": "1.0.0",
  "id": "00000000-0000-0000-0000-000000000000",
  "name": { "short": "OpenClaw" },
  "developer": {
    "name": "Your Org",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "description": { "short": "OpenClaw in Teams", "full": "OpenClaw in Teams" },
  "icons": { "outline": "outline.png", "color": "color.png" },
  "accentColor": "#5B6DEF",
  "bots": [
    {
      "botId": "11111111-1111-1111-1111-111111111111",
      "scopes": ["personal", "team", "groupChat"],
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false,
      "supportsFiles": true
    }
  ],
  "webApplicationInfo": {
    "id": "11111111-1111-1111-1111-111111111111"
  },
  "authorization": {
    "permissions": {
      "resourceSpecific": [
        { "name": "ChannelMessage.Read.Group", "type": "Application" },
        { "name": "ChannelMessage.Send.Group", "type": "Application" },
        { "name": "Member.Read.Group", "type": "Application" },
        { "name": "Owner.Read.Group", "type": "Application" },
        { "name": "ChannelSettings.Read.Group", "type": "Application" },
        { "name": "TeamMember.Read.Group", "type": "Application" },
        { "name": "TeamSettings.Read.Group", "type": "Application" },
        { "name": "ChatMessage.Read.Chat", "type": "Application" }
      ]
    }
  }
}
```

### Manifest caveats (must-have fields)

*   `bots[].botId` **must** match the Azure Bot App ID.
*   `webApplicationInfo.id` **must** match the Azure Bot App ID.
*   `bots[].scopes` must include the surfaces you plan to use (`personal`, `team`, `groupChat`).
*   `bots[].supportsFiles: true` is required for file handling in personal scope.
*   `authorization.permissions.resourceSpecific` must include channel read/send if you want channel traffic.

### Updating an existing app

To update an already-installed Teams app (e.g., to add RSC permissions):

1.  Update your `manifest.json` with the new settings
2.  **Increment the `version` field** (e.g., `1.0.0` → `1.1.0`)
3.  **Re-zip** the manifest with icons (`manifest.json`, `outline.png`, `color.png`)
4.  Upload the new zip:
    *   **Option A (Teams Admin Center):** Teams Admin Center → Teams apps → Manage apps → find your app → Upload new version
    *   **Option B (Sideload):** In Teams → Apps → Manage your apps → Upload a custom app
5.  **For team channels:** Reinstall the app in each team for new permissions to take effect
6.  **Fully quit and relaunch Teams** (not just close the window) to clear cached app metadata

## Capabilities: RSC only vs Graph

### With **Teams RSC only** (app installed, no Graph API permissions)

Works:

*   Read channel message **text** content.
*   Send channel message **text** content.
*   Receive **personal (DM)** file attachments.

Does NOT work:

*   Channel/group **image or file contents** (payload only includes HTML stub).
*   Downloading attachments stored in SharePoint/OneDrive.
*   Reading message history (beyond the live webhook event).

### With **Teams RSC + Microsoft Graph Application permissions**

Adds:

*   Downloading hosted contents (images pasted into messages).
*   Downloading file attachments stored in SharePoint/OneDrive.
*   Reading channel/chat message history via Graph.

### RSC vs Graph API

| Capability | RSC Permissions | Graph API |
| --- | --- | --- |
| **Real-time messages** | Yes (via webhook) | No (polling only) |
| **Historical messages** | No  | Yes (can query history) |
| **Setup complexity** | App manifest only | Requires admin consent + token flow |
| **Works offline** | No (must be running) | Yes (query anytime) |

**Bottom line:** RSC is for real-time listening; Graph API is for historical access. For catching up on missed messages while offline, you need Graph API with `ChannelMessage.Read.All` (requires admin consent).

## Graph-enabled media + history (required for channels)

If you need images/files in **channels** or want to fetch **message history**, you must enable Microsoft Graph permissions and grant admin consent.

1.  In Entra ID (Azure AD) **App Registration**, add Microsoft Graph **Application permissions**:
    *   `ChannelMessage.Read.All` (channel attachments + history)
    *   `Chat.Read.All` or `ChatMessage.Read.All` (group chats)
2.  **Grant admin consent** for the tenant.
3.  Bump the Teams app **manifest version**, re-upload, and **reinstall the app in Teams**.
4.  **Fully quit and relaunch Teams** to clear cached app metadata.

**Additional permission for user mentions:** User @mentions work out of the box for users in the conversation. However, if you want to dynamically search and mention users who are **not in the current conversation**, add `User.Read.All` (Application) permission and grant admin consent.

## Known Limitations

### Webhook timeouts

Teams delivers messages via HTTP webhook. If processing takes too long (e.g., slow LLM responses), you may see:

*   Gateway timeouts
*   Teams retrying the message (causing duplicates)
*   Dropped replies

OpenClaw handles this by returning quickly and sending replies proactively, but very slow responses may still cause issues.

### Formatting

Teams markdown is more limited than Slack or Discord:

*   Basic formatting works: **bold**, _italic_, `code`, links
*   Complex markdown (tables, nested lists) may not render correctly
*   Adaptive Cards are supported for polls and arbitrary card sends (see below)

## Configuration

Key settings (see `/gateway/configuration` for shared channel patterns):

*   `channels.msteams.enabled`: enable/disable the channel.
*   `channels.msteams.appId`, `channels.msteams.appPassword`, `channels.msteams.tenantId`: bot credentials.
*   `channels.msteams.webhook.port` (default `3978`)
*   `channels.msteams.webhook.path` (default `/api/messages`)
*   `channels.msteams.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing)
*   `channels.msteams.allowFrom`: DM allowlist (AAD object IDs recommended). The wizard resolves names to IDs during setup when Graph access is available.
*   `channels.msteams.dangerouslyAllowNameMatching`: break-glass toggle to re-enable mutable UPN/display-name matching.
*   `channels.msteams.textChunkLimit`: outbound text chunk size.
*   `channels.msteams.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
*   `channels.msteams.mediaAllowHosts`: allowlist for inbound attachment hosts (defaults to Microsoft/Teams domains).
*   `channels.msteams.mediaAuthAllowHosts`: allowlist for attaching Authorization headers on media retries (defaults to Graph + Bot Framework hosts).
*   `channels.msteams.requireMention`: require @mention in channels/groups (default true).
*   `channels.msteams.replyStyle`: `thread | top-level` (see [Reply Style](https://docs.openclaw.ai/channels/msteams#reply-style-threads-vs-posts)).
*   `channels.msteams.teams.<teamId>.replyStyle`: per-team override.
*   `channels.msteams.teams.<teamId>.requireMention`: per-team override.
*   `channels.msteams.teams.<teamId>.tools`: default per-team tool policy overrides (`allow`/`deny`/`alsoAllow`) used when a channel override is missing.
*   `channels.msteams.teams.<teamId>.toolsBySender`: default per-team per-sender tool policy overrides (`"*"` wildcard supported).
*   `channels.msteams.teams.<teamId>.channels.<conversationId>.replyStyle`: per-channel override.
*   `channels.msteams.teams.<teamId>.channels.<conversationId>.requireMention`: per-channel override.
*   `channels.msteams.teams.<teamId>.channels.<conversationId>.tools`: per-channel tool policy overrides (`allow`/`deny`/`alsoAllow`).
*   `channels.msteams.teams.<teamId>.channels.<conversationId>.toolsBySender`: per-channel per-sender tool policy overrides (`"*"` wildcard supported).
*   `toolsBySender` keys should use explicit prefixes: `id:`, `e164:`, `username:`, `name:` (legacy unprefixed keys still map to `id:` only).
*   `channels.msteams.sharePointSiteId`: SharePoint site ID for file uploads in group chats/channels (see [Sending files in group chats](https://docs.openclaw.ai/channels/msteams#sending-files-in-group-chats)).

## Routing & Sessions

*   Session keys follow the standard agent format (see [/concepts/session](https://docs.openclaw.ai/concepts/session)):
    *   Direct messages share the main session (`agent:<agentId>:<mainKey>`).
    *   Channel/group messages use conversation id:
        *   `agent:<agentId>:msteams:channel:<conversationId>`
        *   `agent:<agentId>:msteams:group:<conversationId>`

## Reply Style: Threads vs Posts

Teams recently introduced two channel UI styles over the same underlying data model:

| Style | Description | Recommended `replyStyle` |
| --- | --- | --- |
| **Posts** (classic) | Messages appear as cards with threaded replies underneath | `thread` (default) |
| **Threads** (Slack-like) | Messages flow linearly, more like Slack | `top-level` |

**The problem:** The Teams API does not expose which UI style a channel uses. If you use the wrong `replyStyle`:

*   `thread` in a Threads-style channel → replies appear nested awkwardly
*   `top-level` in a Posts-style channel → replies appear as separate top-level posts instead of in-thread

**Solution:** Configure `replyStyle` per-channel based on how the channel is set up:

```
{
  "msteams": {
    "replyStyle": "thread",
    "teams": {
      "19:abc...@thread.tacv2": {
        "channels": {
          "19:xyz...@thread.tacv2": {
            "replyStyle": "top-level"
          }
        }
      }
    }
  }
}
```

## Attachments & Images

**Current limitations:**

*   **DMs:** Images and file attachments work via Teams bot file APIs.
*   **Channels/groups:** Attachments live in M365 storage (SharePoint/OneDrive). The webhook payload only includes an HTML stub, not the actual file bytes. **Graph API permissions are required** to download channel attachments.

Without Graph permissions, channel messages with images will be received as text-only (the image content is not accessible to the bot). By default, OpenClaw only downloads media from Microsoft/Teams hostnames. Override with `channels.msteams.mediaAllowHosts` (use `["*"]` to allow any host). Authorization headers are only attached for hosts in `channels.msteams.mediaAuthAllowHosts` (defaults to Graph + Bot Framework hosts). Keep this list strict (avoid multi-tenant suffixes).

## Sending files in group chats

Bots can send files in DMs using the FileConsentCard flow (built-in). However, **sending files in group chats/channels** requires additional setup:

| Context | How files are sent | Setup needed |
| --- | --- | --- |
| **DMs** | FileConsentCard → user accepts → bot uploads | Works out of the box |
| **Group chats/channels** | Upload to SharePoint → share link | Requires `sharePointSiteId` + Graph permissions |
| **Images (any context)** | Base64-encoded inline | Works out of the box |

### Why group chats need SharePoint

Bots don’t have a personal OneDrive drive (the `/me/drive` Graph API endpoint doesn’t work for application identities). To send files in group chats/channels, the bot uploads to a **SharePoint site** and creates a sharing link.

### Setup

1.  **Add Graph API permissions** in Entra ID (Azure AD) → App Registration:
    *   `Sites.ReadWrite.All` (Application) - upload files to SharePoint
    *   `Chat.Read.All` (Application) - optional, enables per-user sharing links
2.  **Grant admin consent** for the tenant.
3.  **Get your SharePoint site ID:**
    
    ```
    # Via Graph Explorer or curl with a valid token:
    curl -H "Authorization: Bearer $TOKEN" \
      "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}"
    
    # Example: for a site at "contoso.sharepoint.com/sites/BotFiles"
    curl -H "Authorization: Bearer $TOKEN" \
      "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles"
    
    # Response includes: "id": "contoso.sharepoint.com,guid1,guid2"
    ```
    
4.  **Configure OpenClaw:**
    
    ```
    {
      channels: {
        msteams: {
          // ... other config ...
          sharePointSiteId: "contoso.sharepoint.com,guid1,guid2",
        },
      },
    }
    ```
    

### Sharing behavior

| Permission | Sharing behavior |
| --- | --- |
| `Sites.ReadWrite.All` only | Organization-wide sharing link (anyone in org can access) |
| `Sites.ReadWrite.All` + `Chat.Read.All` | Per-user sharing link (only chat members can access) |

Per-user sharing is more secure as only the chat participants can access the file. If `Chat.Read.All` permission is missing, the bot falls back to organization-wide sharing.

### Fallback behavior

| Scenario | Result |
| --- | --- |
| Group chat + file + `sharePointSiteId` configured | Upload to SharePoint, send sharing link |
| Group chat + file + no `sharePointSiteId` | Attempt OneDrive upload (may fail), send text only |
| Personal chat + file | FileConsentCard flow (works without SharePoint) |
| Any context + image | Base64-encoded inline (works without SharePoint) |

### Files stored location

Uploaded files are stored in a `/OpenClawShared/` folder in the configured SharePoint site’s default document library.

## Polls (Adaptive Cards)

OpenClaw sends Teams polls as Adaptive Cards (there is no native Teams poll API).

*   CLI: `openclaw message poll --channel msteams --target conversation:<id> ...`
*   Votes are recorded by the gateway in `~/.openclaw/msteams-polls.json`.
*   The gateway must stay online to record votes.
*   Polls do not auto-post result summaries yet (inspect the store file if needed).

## Adaptive Cards (arbitrary)

Send any Adaptive Card JSON to Teams users or conversations using the `message` tool or CLI. The `card` parameter accepts an Adaptive Card JSON object. When `card` is provided, the message text is optional. **Agent tool:**

```
{
  "action": "send",
  "channel": "msteams",
  "target": "user:<id>",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello!" }]
  }
}
```

**CLI:**

```
openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello!"}]}'
```

See [Adaptive Cards documentation](https://adaptivecards.io/) for card schema and examples. For target format details, see [Target formats](https://docs.openclaw.ai/channels/msteams#target-formats) below.

## Target formats

MSTeams targets use prefixes to distinguish between users and conversations:

| Target type | Format | Example |
| --- | --- | --- |
| User (by ID) | `user:<aad-object-id>` | `user:40a1a0ed-4ff2-4164-a219-55518990c197` |
| User (by name) | `user:<display-name>` | `user:John Smith` (requires Graph API) |
| Group/channel | `conversation:<conversation-id>` | `conversation:19:abc123...@thread.tacv2` |
| Group/channel (raw) | `<conversation-id>` | `19:abc123...@thread.tacv2` (if contains `@thread`) |

**CLI examples:**

```
# Send to a user by ID
openclaw message send --channel msteams --target "user:40a1a0ed-..." --message "Hello"

# Send to a user by display name (triggers Graph API lookup)
openclaw message send --channel msteams --target "user:John Smith" --message "Hello"

# Send to a group chat or channel
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" --message "Hello"

# Send an Adaptive Card to a conversation
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello"}]}'
```

**Agent tool examples:**

```
{
  "action": "send",
  "channel": "msteams",
  "target": "user:John Smith",
  "message": "Hello!"
}
```

```
{
  "action": "send",
  "channel": "msteams",
  "target": "conversation:19:abc...@thread.tacv2",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello" }]
  }
}
```

Note: Without the `user:` prefix, names default to group/team resolution. Always use `user:` when targeting people by display name.

## Proactive messaging

*   Proactive messages are only possible **after** a user has interacted, because we store conversation references at that point.
*   See `/gateway/configuration` for `dmPolicy` and allowlist gating.

## Team and Channel IDs (Common Gotcha)

The `groupId` query parameter in Teams URLs is **NOT** the team ID used for configuration. Extract IDs from the URL path instead: **Team URL:**

```
https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
                                    └────────────────────────────┘
                                    Team ID (URL-decode this)
```

**Channel URL:**

```
https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
                                      └─────────────────────────┘
                                      Channel ID (URL-decode this)
```

**For config:**

*   Team ID = path segment after `/team/` (URL-decoded, e.g., `19:Bk4j...@thread.tacv2`)
*   Channel ID = path segment after `/channel/` (URL-decoded)
*   **Ignore** the `groupId` query parameter

## Private Channels

Bots have limited support in private channels:

| Feature | Standard Channels | Private Channels |
| --- | --- | --- |
| Bot installation | Yes | Limited |
| Real-time messages (webhook) | Yes | May not work |
| RSC permissions | Yes | May behave differently |
| @mentions | Yes | If bot is accessible |
| Graph API history | Yes | Yes (with permissions) |

**Workarounds if private channels don’t work:**

1.  Use standard channels for bot interactions
2.  Use DMs - users can always message the bot directly
3.  Use Graph API for historical access (requires `ChannelMessage.Read.All`)

## Troubleshooting

### Common issues

*   **Images not showing in channels:** Graph permissions or admin consent missing. Reinstall the Teams app and fully quit/reopen Teams.
*   **No responses in channel:** mentions are required by default; set `channels.msteams.requireMention=false` or configure per team/channel.
*   **Version mismatch (Teams still shows old manifest):** remove + re-add the app and fully quit Teams to refresh.
*   **401 Unauthorized from webhook:** Expected when testing manually without Azure JWT - means endpoint is reachable but auth failed. Use Azure Web Chat to test properly.

### Manifest upload errors

*   **“Icon file cannot be empty”:** The manifest references icon files that are 0 bytes. Create valid PNG icons (32x32 for `outline.png`, 192x192 for `color.png`).
*   **“webApplicationInfo.Id already in use”:** The app is still installed in another team/chat. Find and uninstall it first, or wait 5-10 minutes for propagation.
*   **“Something went wrong” on upload:** Upload via [https://admin.teams.microsoft.com](https://admin.teams.microsoft.com/) instead, open browser DevTools (F12) → Network tab, and check the response body for the actual error.
*   **Sideload failing:** Try “Upload an app to your org’s app catalog” instead of “Upload a custom app” - this often bypasses sideload restrictions.

### RSC permissions not working

1.  Verify `webApplicationInfo.id` matches your bot’s App ID exactly
2.  Re-upload the app and reinstall in the team/chat
3.  Check if your org admin has blocked RSC permissions
4.  Confirm you’re using the right scope: `ChannelMessage.Read.Group` for teams, `ChatMessage.Read.Chat` for group chats

## References

*   [Create Azure Bot](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration) - Azure Bot setup guide
*   [Teams Developer Portal](https://dev.teams.microsoft.com/apps) - create/manage Teams apps
*   [Teams app manifest schema](https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema)
*   [Receive channel messages with RSC](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc)
*   [RSC permissions reference](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
*   [Teams bot file handling](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/bots-filesv4) (channel/group requires Graph)
*   [Proactive messaging](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/send-proactive-messages)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/synology-chat -->

# Synology Chat - OpenClaw

## Synology Chat (plugin)

Status: supported via plugin as a direct-message channel using Synology Chat webhooks. The plugin accepts inbound messages from Synology Chat outgoing webhooks and sends replies through a Synology Chat incoming webhook.

## Plugin required

Synology Chat is plugin-based and not part of the default core channel install. Install from a local checkout:

```
openclaw plugins install ./extensions/synology-chat
```

Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup

1.  Install and enable the Synology Chat plugin.
2.  In Synology Chat integrations:
    *   Create an incoming webhook and copy its URL.
    *   Create an outgoing webhook with your secret token.
3.  Point the outgoing webhook URL to your OpenClaw gateway:
    *   `https://gateway-host/webhook/synology` by default.
    *   Or your custom `channels.synology-chat.webhookPath`.
4.  Configure `channels.synology-chat` in OpenClaw.
5.  Restart gateway and send a DM to the Synology Chat bot.

Minimal config:

```
{
  channels: {
    "synology-chat": {
      enabled: true,
      token: "synology-outgoing-token",
      incomingUrl: "https://nas.example.com/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=...",
      webhookPath: "/webhook/synology",
      dmPolicy: "allowlist",
      allowedUserIds: ["123456"],
      rateLimitPerMinute: 30,
      allowInsecureSsl: false,
    },
  },
}
```

## Environment variables

For the default account, you can use env vars:

*   `SYNOLOGY_CHAT_TOKEN`
*   `SYNOLOGY_CHAT_INCOMING_URL`
*   `SYNOLOGY_NAS_HOST`
*   `SYNOLOGY_ALLOWED_USER_IDS` (comma-separated)
*   `SYNOLOGY_RATE_LIMIT`
*   `OPENCLAW_BOT_NAME`

Config values override env vars.

## DM policy and access control

*   `dmPolicy: "allowlist"` is the recommended default.
*   `allowedUserIds` accepts a list (or comma-separated string) of Synology user IDs.
*   In `allowlist` mode, an empty `allowedUserIds` list is treated as misconfiguration and the webhook route will not start (use `dmPolicy: "open"` for allow-all).
*   `dmPolicy: "open"` allows any sender.
*   `dmPolicy: "disabled"` blocks DMs.
*   Pairing approvals work with:
    *   `openclaw pairing list synology-chat`
    *   `openclaw pairing approve synology-chat <CODE>`

## Outbound delivery

Use numeric Synology Chat user IDs as targets. Examples:

```
openclaw message send --channel synology-chat --target 123456 --text "Hello from OpenClaw"
openclaw message send --channel synology-chat --target synology-chat:123456 --text "Hello again"
```

Media sends are supported by URL-based file delivery.

## Multi-account

Multiple Synology Chat accounts are supported under `channels.synology-chat.accounts`. Each account can override token, incoming URL, webhook path, DM policy, and limits.

```
{
  channels: {
    "synology-chat": {
      enabled: true,
      accounts: {
        default: {
          token: "token-a",
          incomingUrl: "https://nas-a.example.com/...token=...",
        },
        alerts: {
          token: "token-b",
          incomingUrl: "https://nas-b.example.com/...token=...",
          webhookPath: "/webhook/synology-alerts",
          dmPolicy: "allowlist",
          allowedUserIds: ["987654"],
        },
      },
    },
  },
}
```

## Security notes

*   Keep `token` secret and rotate it if leaked.
*   Keep `allowInsecureSsl: false` unless you explicitly trust a self-signed local NAS cert.
*   Inbound webhook requests are token-verified and rate-limited per sender.
*   Prefer `dmPolicy: "allowlist"` for production.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/nostr -->

# Nostr - OpenClaw

**Status:** Optional plugin (disabled by default). Nostr is a decentralized protocol for social networking. This channel enables OpenClaw to receive and respond to encrypted direct messages (DMs) via NIP-04.

## Install (on demand)

### Onboarding (recommended)

*   The onboarding wizard (`openclaw onboard`) and `openclaw channels add` list optional channel plugins.
*   Selecting Nostr prompts you to install the plugin on demand.

Install defaults:

*   **Dev channel + git checkout available:** uses the local plugin path.
*   **Stable/Beta:** downloads from npm.

You can always override the choice in the prompt.

### Manual install

```
openclaw plugins install @openclaw/nostr
```

Use a local checkout (dev workflows):

```
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Restart the Gateway after installing or enabling plugins.

## Quick setup

1.  Generate a Nostr keypair (if needed):

```
# Using nak
nak key generate
```

2.  Add to config:

```
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}"
    }
  }
}
```

3.  Export the key:

```
export NOSTR_PRIVATE_KEY="nsec1..."
```

4.  Restart the Gateway.

## Configuration reference

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `privateKey` | string | required | Private key in `nsec` or hex format |
| `relays` | string\[\] | `['wss://relay.damus.io', 'wss://nos.lol']` | Relay URLs (WebSocket) |
| `dmPolicy` | string | `pairing` | DM access policy |
| `allowFrom` | string\[\] | `[]` | Allowed sender pubkeys |
| `enabled` | boolean | `true` | Enable/disable channel |
| `name` | string | \-  | Display name |
| `profile` | object | \-  | NIP-01 profile metadata |

Profile data is published as a NIP-01 `kind:0` event. You can manage it from the Control UI (Channels -> Nostr -> Profile) or set it directly in config. Example:

```
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "profile": {
        "name": "openclaw",
        "displayName": "OpenClaw",
        "about": "Personal assistant DM bot",
        "picture": "https://example.com/avatar.png",
        "banner": "https://example.com/banner.png",
        "website": "https://example.com",
        "nip05": "openclaw@example.com",
        "lud16": "openclaw@example.com"
      }
    }
  }
}
```

Notes:

*   Profile URLs must use `https://`.
*   Importing from relays merges fields and preserves local overrides.

## Access control

### DM policies

*   **pairing** (default): unknown senders get a pairing code.
*   **allowlist**: only pubkeys in `allowFrom` can DM.
*   **open**: public inbound DMs (requires `allowFrom: ["*"]`).
*   **disabled**: ignore inbound DMs.

### Allowlist example

```
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "dmPolicy": "allowlist",
      "allowFrom": ["npub1abc...", "npub1xyz..."]
    }
  }
}
```

## Key formats

Accepted formats:

*   **Private key:** `nsec...` or 64-char hex
*   **Pubkeys (`allowFrom`):** `npub...` or hex

## Relays

Defaults: `relay.damus.io` and `nos.lol`.

```
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"]
    }
  }
}
```

Tips:

*   Use 2-3 relays for redundancy.
*   Avoid too many relays (latency, duplication).
*   Paid relays can improve reliability.
*   Local relays are fine for testing (`ws://localhost:7777`).

## Protocol support

| NIP | Status | Description |
| --- | --- | --- |
| NIP-01 | Supported | Basic event format + profile metadata |
| NIP-04 | Supported | Encrypted DMs (`kind:4`) |
| NIP-17 | Planned | Gift-wrapped DMs |
| NIP-44 | Planned | Versioned encryption |

## Testing

### Local relay

```
# Start strfry
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

```
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["ws://localhost:7777"]
    }
  }
}
```

### Manual test

1.  Note the bot pubkey (npub) from logs.
2.  Open a Nostr client (Damus, Amethyst, etc.).
3.  DM the bot pubkey.
4.  Verify the response.

## Troubleshooting

### Not receiving messages

*   Verify the private key is valid.
*   Ensure relay URLs are reachable and use `wss://` (or `ws://` for local).
*   Confirm `enabled` is not `false`.
*   Check Gateway logs for relay connection errors.

### Not sending responses

*   Check relay accepts writes.
*   Verify outbound connectivity.
*   Watch for relay rate limits.

### Duplicate responses

*   Expected when using multiple relays.
*   Messages are deduplicated by event ID; only the first delivery triggers a response.

## Security

*   Never commit private keys.
*   Use environment variables for keys.
*   Consider `allowlist` for production bots.

## Limitations (MVP)

*   Direct messages only (no group chats).
*   No media attachments.
*   NIP-04 only (NIP-17 gift-wrap planned).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/slack -->

# Slack - OpenClaw

Status: production-ready for DMs + channels via Slack app integrations. Default mode is Socket Mode; HTTP Events API mode is also supported.

## Quick setup

*   Socket Mode (default)
    
*   HTTP Events API mode
    

## Token model

*   `botToken` + `appToken` are required for Socket Mode.
*   HTTP mode requires `botToken` + `signingSecret`.
*   Config tokens override env fallback.
*   `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` env fallback applies only to the default account.
*   `userToken` (`xoxp-...`) is config-only (no env fallback) and defaults to read-only behavior (`userTokenReadOnly: true`).
*   Optional: add `chat:write.customize` if you want outgoing messages to use the active agent identity (custom `username` and icon). `icon_emoji` uses `:emoji_name:` syntax.

## Access control and routing

*   DM policy
    
*   Channel policy
    
*   Mentions and channel users
    

`channels.slack.dmPolicy` controls DM access (legacy: `channels.slack.dm.policy`):

*   `pairing` (default)
*   `allowlist`
*   `open` (requires `channels.slack.allowFrom` to include `"*"`; legacy: `channels.slack.dm.allowFrom`)
*   `disabled`

DM flags:

*   `dm.enabled` (default true)
*   `channels.slack.allowFrom` (preferred)
*   `dm.allowFrom` (legacy)
*   `dm.groupEnabled` (group DMs default false)
*   `dm.groupChannels` (optional MPIM allowlist)

Multi-account precedence:

*   `channels.slack.accounts.default.allowFrom` applies only to the `default` account.
*   Named accounts inherit `channels.slack.allowFrom` when their own `allowFrom` is unset.
*   Named accounts do not inherit `channels.slack.accounts.default.allowFrom`.

Pairing in DMs uses `openclaw pairing approve slack <code>`.

`channels.slack.groupPolicy` controls channel handling:

*   `open`
*   `allowlist`
*   `disabled`

Channel allowlist lives under `channels.slack.channels`.Runtime note: if `channels.slack` is completely missing (env-only setup), runtime falls back to `groupPolicy="allowlist"` and logs a warning (even if `channels.defaults.groupPolicy` is set).Name/ID resolution:

*   channel allowlist entries and DM allowlist entries are resolved at startup when token access allows
*   unresolved entries are kept as configured
*   inbound authorization matching is ID-first by default; direct username/slug matching requires `channels.slack.dangerouslyAllowNameMatching: true`

Channel messages are mention-gated by default.Mention sources:

*   explicit app mention (`<@botId>`)
*   mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
*   implicit reply-to-bot thread behavior

Per-channel controls (`channels.slack.channels.<id|name>`):

*   `requireMention`
*   `users` (allowlist)
*   `allowBots`
*   `skills`
*   `systemPrompt`
*   `tools`, `toolsBySender`
*   `toolsBySender` key format: `id:`, `e164:`, `username:`, `name:`, or `"*"` wildcard (legacy unprefixed keys still map to `id:` only)

## Commands and slash behavior

*   Native command auto-mode is **off** for Slack (`commands.native: "auto"` does not enable Slack native commands).
*   Enable native Slack command handlers with `channels.slack.commands.native: true` (or global `commands.native: true`).
*   When native commands are enabled, register matching slash commands in Slack (`/<command>` names), with one exception:
    *   register `/agentstatus` for the status command (Slack reserves `/status`)
*   If native commands are not enabled, you can run a single configured slash command via `channels.slack.slashCommand`.
*   Native arg menus now adapt their rendering strategy:
    *   up to 5 options: button blocks
    *   6-100 options: static select menu
    *   more than 100 options: external select with async option filtering when interactivity options handlers are available
    *   if encoded option values exceed Slack limits, the flow falls back to buttons
*   For long option payloads, Slash command argument menus use a confirm dialog before dispatching a selected value.

Default slash command settings:

*   `enabled: false`
*   `name: "openclaw"`
*   `sessionPrefix: "slack:slash"`
*   `ephemeral: true`

Slash sessions use isolated keys:

*   `agent:<agentId>:slack:slash:<userId>`

and still route command execution against the target conversation session (`CommandTargetSessionKey`).

*   DMs route as `direct`; channels as `channel`; MPIMs as `group`.
*   With default `session.dmScope=main`, Slack DMs collapse to agent main session.
*   Channel sessions: `agent:<agentId>:slack:channel:<channelId>`.
*   Thread replies can create thread session suffixes (`:thread:<threadTs>`) when applicable.
*   `channels.slack.thread.historyScope` default is `thread`; `thread.inheritParent` default is `false`.
*   `channels.slack.thread.initialHistoryLimit` controls how many existing thread messages are fetched when a new thread session starts (default `20`; set `0` to disable).

Reply threading controls:

*   `channels.slack.replyToMode`: `off|first|all` (default `off`)
*   `channels.slack.replyToModeByChatType`: per `direct|group|channel`
*   legacy fallback for direct chats: `channels.slack.dm.replyToMode`

Manual reply tags are supported:

*   `[[reply_to_current]]`
*   `[[reply_to:<id>]]`

Note: `replyToMode="off"` disables **all** reply threading in Slack, including explicit `[[reply_to_*]]` tags. This differs from Telegram, where explicit tags are still honored in `"off"` mode. The difference reflects the platform threading models: Slack threads hide messages from the channel, while Telegram replies remain visible in the main chat flow.

## Actions and gates

Slack actions are controlled by `channels.slack.actions.*`. Available action groups in current Slack tooling:

| Group | Default |
| --- | --- |
| messages | enabled |
| reactions | enabled |
| pins | enabled |
| memberInfo | enabled |
| emojiList | enabled |

## Events and operational behavior

*   Message edits/deletes/thread broadcasts are mapped into system events.
*   Reaction add/remove events are mapped into system events.
*   Member join/leave, channel created/renamed, and pin add/remove events are mapped into system events.
*   Assistant thread status updates (for “is typing…” indicators in threads) use `assistant.threads.setStatus` and require bot scope `assistant:write`.
*   `channel_id_changed` can migrate channel config keys when `configWrites` is enabled.
*   Channel topic/purpose metadata is treated as untrusted context and can be injected into routing context.
*   Block actions and modal interactions emit structured `Slack interaction: ...` system events with rich payload fields:
    *   block actions: selected values, labels, picker values, and `workflow_*` metadata
    *   modal `view_submission` and `view_closed` events with routed channel metadata and form inputs

## Ack reactions

`ackReaction` sends an acknowledgement emoji while OpenClaw is processing an inbound message. Resolution order:

*   `channels.slack.accounts.<accountId>.ackReaction`
*   `channels.slack.ackReaction`
*   `messages.ackReaction`
*   agent identity emoji fallback (`agents.list[].identity.emoji`, else ”👀”)

Notes:

*   Slack expects shortcodes (for example `"eyes"`).
*   Use `""` to disable the reaction for the Slack account or globally.

## Typing reaction fallback

`typingReaction` adds a temporary reaction to the inbound Slack message while OpenClaw is processing a reply, then removes it when the run finishes. This is a useful fallback when Slack native assistant typing is unavailable, especially in DMs. Resolution order:

*   `channels.slack.accounts.<accountId>.typingReaction`
*   `channels.slack.typingReaction`

Notes:

*   Slack expects shortcodes (for example `"hourglass_flowing_sand"`).
*   The reaction is best-effort and cleanup is attempted automatically after the reply or failure path completes.

## Manifest and scope checklist

## Troubleshooting

## Text streaming

OpenClaw supports Slack native text streaming via the Agents and AI Apps API. `channels.slack.streaming` controls live preview behavior:

*   `off`: disable live preview streaming.
*   `partial` (default): replace preview text with the latest partial output.
*   `block`: append chunked preview updates.
*   `progress`: show progress status text while generating, then send final text.

`channels.slack.nativeStreaming` controls Slack’s native streaming API (`chat.startStream` / `chat.appendStream` / `chat.stopStream`) when `streaming` is `partial` (default: `true`). Disable native Slack streaming (keep draft preview behavior):

```
channels:
  slack:
    streaming: partial
    nativeStreaming: false
```

Legacy keys:

*   `channels.slack.streamMode` (`replace | status_final | append`) is auto-migrated to `channels.slack.streaming`.
*   boolean `channels.slack.streaming` is auto-migrated to `channels.slack.nativeStreaming`.

### Requirements

1.  Enable **Agents and AI Apps** in your Slack app settings.
2.  Ensure the app has the `assistant:write` scope.
3.  A reply thread must be available for that message. Thread selection still follows `replyToMode`.

### Behavior

*   First text chunk starts a stream (`chat.startStream`).
*   Later text chunks append to the same stream (`chat.appendStream`).
*   End of reply finalizes stream (`chat.stopStream`).
*   Media and non-text payloads fall back to normal delivery.
*   If streaming fails mid-reply, OpenClaw falls back to normal delivery for remaining payloads.

## Configuration reference pointers

Primary reference:

*   [Configuration reference - Slack](https://docs.openclaw.ai/gateway/configuration-reference#slack) High-signal Slack fields:
    *   mode/auth: `mode`, `botToken`, `appToken`, `signingSecret`, `webhookPath`, `accounts.*`
    *   DM access: `dm.enabled`, `dmPolicy`, `allowFrom` (legacy: `dm.policy`, `dm.allowFrom`), `dm.groupEnabled`, `dm.groupChannels`
    *   compatibility toggle: `dangerouslyAllowNameMatching` (break-glass; keep off unless needed)
    *   channel access: `groupPolicy`, `channels.*`, `channels.*.users`, `channels.*.requireMention`
    *   threading/history: `replyToMode`, `replyToModeByChatType`, `thread.*`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
    *   delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `streaming`, `nativeStreaming`
    *   ops/features: `configWrites`, `commands.native`, `slashCommand.*`, `actions.*`, `userToken`, `userTokenReadOnly`

*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [Channel routing](https://docs.openclaw.ai/channels/channel-routing)
*   [Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)
*   [Configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Slash commands](https://docs.openclaw.ai/tools/slash-commands)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/twitch -->

# Twitch - OpenClaw

## Twitch (plugin)

Twitch chat support via IRC connection. OpenClaw connects as a Twitch user (bot account) to receive and send messages in channels.

## Plugin required

Twitch ships as a plugin and is not bundled with the core install. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/twitch
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/twitch
```

Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup (beginner)

1.  Create a dedicated Twitch account for the bot (or use an existing account).
2.  Generate credentials: [Twitch Token Generator](https://twitchtokengenerator.com/)
    *   Select **Bot Token**
    *   Verify scopes `chat:read` and `chat:write` are selected
    *   Copy the **Client ID** and **Access Token**
3.  Find your Twitch user ID: [https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/)
4.  Configure the token:
    *   Env: `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (default account only)
    *   Or config: `channels.twitch.accessToken`
    *   If both are set, config takes precedence (env fallback is default-account only).
5.  Start the gateway.

**⚠️ Important:** Add access control (`allowFrom` or `allowedRoles`) to prevent unauthorized users from triggering the bot. `requireMention` defaults to `true`. Minimal config:

```
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Bot's Twitch account
      accessToken: "oauth:abc123...", // OAuth Access Token (or use OPENCLAW_TWITCH_ACCESS_TOKEN env var)
      clientId: "xyz789...", // Client ID from Token Generator
      channel: "vevisk", // Which Twitch channel's chat to join (required)
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only - get it from https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## What it is

*   A Twitch channel owned by the Gateway.
*   Deterministic routing: replies always go back to Twitch.
*   Each account maps to an isolated session key `agent:<agentId>:twitch:<accountName>`.
*   `username` is the bot’s account (who authenticates), `channel` is which chat room to join.

## Setup (detailed)

### Generate credentials

Use [Twitch Token Generator](https://twitchtokengenerator.com/):

*   Select **Bot Token**
*   Verify scopes `chat:read` and `chat:write` are selected
*   Copy the **Client ID** and **Access Token**

No manual app registration needed. Tokens expire after several hours.

### Configure the bot

**Env var (default account only):**

```
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Or config:**

```
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
    },
  },
}
```

If both env and config are set, config takes precedence.

### Access control (recommended)

```
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only
    },
  },
}
```

Prefer `allowFrom` for a hard allowlist. Use `allowedRoles` instead if you want role-based access. **Available roles:** `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, `"all"`. **Why user IDs?** Usernames can change, allowing impersonation. User IDs are permanent. Find your Twitch user ID: [https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/) (Convert your Twitch username to ID)

## Token refresh (optional)

Tokens from [Twitch Token Generator](https://twitchtokengenerator.com/) cannot be automatically refreshed - regenerate when expired. For automatic token refresh, create your own Twitch application at [Twitch Developer Console](https://dev.twitch.tv/console) and add to config:

```
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```

The bot automatically refreshes tokens before expiration and logs refresh events.

## Multi-account support

Use `channels.twitch.accounts` with per-account tokens. See [`gateway/configuration`](https://docs.openclaw.ai/gateway/configuration) for the shared pattern. Example (one bot account in two channels):

```
{
  channels: {
    twitch: {
      accounts: {
        channel1: {
          username: "openclaw",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "vevisk",
        },
        channel2: {
          username: "openclaw",
          accessToken: "oauth:def456...",
          clientId: "uvw012...",
          channel: "secondchannel",
        },
      },
    },
  },
}
```

**Note:** Each account needs its own token (one token per channel).

## Access control

### Role-based restrictions

```
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator", "vip"],
        },
      },
    },
  },
}
```

### Allowlist by User ID (most secure)

```
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowFrom: ["123456789", "987654321"],
        },
      },
    },
  },
}
```

### Role-based access (alternative)

`allowFrom` is a hard allowlist. When set, only those user IDs are allowed. If you want role-based access, leave `allowFrom` unset and configure `allowedRoles` instead:

```
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

### Disable @mention requirement

By default, `requireMention` is `true`. To disable and respond to all messages:

```
{
  channels: {
    twitch: {
      accounts: {
        default: {
          requireMention: false,
        },
      },
    },
  },
}
```

## Troubleshooting

First, run diagnostic commands:

```
openclaw doctor
openclaw channels status --probe
```

### Bot doesn’t respond to messages

**Check access control:** Ensure your user ID is in `allowFrom`, or temporarily remove `allowFrom` and set `allowedRoles: ["all"]` to test. **Check the bot is in the channel:** The bot must join the channel specified in `channel`.

### Token issues

**“Failed to connect” or authentication errors:**

*   Verify `accessToken` is the OAuth access token value (typically starts with `oauth:` prefix)
*   Check token has `chat:read` and `chat:write` scopes
*   If using token refresh, verify `clientSecret` and `refreshToken` are set

### Token refresh not working

**Check logs for refresh events:**

```
Using env token source for mybot
Access token refreshed for user 123456 (expires in 14400s)
```

If you see “token refresh disabled (no refresh token)”:

*   Ensure `clientSecret` is provided
*   Ensure `refreshToken` is provided

## Config

**Account config:**

*   `username` - Bot username
*   `accessToken` - OAuth access token with `chat:read` and `chat:write`
*   `clientId` - Twitch Client ID (from Token Generator or your app)
*   `channel` - Channel to join (required)
*   `enabled` - Enable this account (default: `true`)
*   `clientSecret` - Optional: For automatic token refresh
*   `refreshToken` - Optional: For automatic token refresh
*   `expiresIn` - Token expiry in seconds
*   `obtainmentTimestamp` - Token obtained timestamp
*   `allowFrom` - User ID allowlist
*   `allowedRoles` - Role-based access control (`"moderator" | "owner" | "vip" | "subscriber" | "all"`)
*   `requireMention` - Require @mention (default: `true`)

**Provider options:**

*   `channels.twitch.enabled` - Enable/disable channel startup
*   `channels.twitch.username` - Bot username (simplified single-account config)
*   `channels.twitch.accessToken` - OAuth access token (simplified single-account config)
*   `channels.twitch.clientId` - Twitch Client ID (simplified single-account config)
*   `channels.twitch.channel` - Channel to join (simplified single-account config)
*   `channels.twitch.accounts.<accountName>` - Multi-account config (all account fields above)

Full example:

```
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
      clientSecret: "secret123...",
      refreshToken: "refresh456...",
      allowFrom: ["123456789"],
      allowedRoles: ["moderator", "vip"],
      accounts: {
        default: {
          username: "mybot",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "your_channel",
          enabled: true,
          clientSecret: "secret123...",
          refreshToken: "refresh456...",
          expiresIn: 14400,
          obtainmentTimestamp: 1706092800000,
          allowFrom: ["123456789", "987654321"],
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

The agent can call `twitch` with action:

*   `send` - Send a message to a channel

Example:

```
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## Safety & ops

*   **Treat tokens like passwords** - Never commit tokens to git
*   **Use automatic token refresh** for long-running bots
*   **Use user ID allowlists** instead of usernames for access control
*   **Monitor logs** for token refresh events and connection status
*   **Scope tokens minimally** - Only request `chat:read` and `chat:write`
*   **If stuck**: Restart the gateway after confirming no other process owns the session

## Limits

*   **500 characters** per message (auto-chunked at word boundaries)
*   Markdown is stripped before chunking
*   No rate limiting (uses Twitch’s built-in rate limits)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/zalo -->

# Zalo - OpenClaw

## Zalo (Bot API)

Status: experimental. DMs are supported; group handling is available with explicit group policy controls.

## Plugin required

Zalo ships as a plugin and is not bundled with the core install.

*   Install via CLI: `openclaw plugins install @openclaw/zalo`
*   Or select **Zalo** during onboarding and confirm the install prompt
*   Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Quick setup (beginner)

1.  Install the Zalo plugin:
    *   From a source checkout: `openclaw plugins install ./extensions/zalo`
    *   From npm (if published): `openclaw plugins install @openclaw/zalo`
    *   Or pick **Zalo** in onboarding and confirm the install prompt
2.  Set the token:
    *   Env: `ZALO_BOT_TOKEN=...`
    *   Or config: `channels.zalo.botToken: "..."`.
3.  Restart the gateway (or finish onboarding).
4.  DM access is pairing by default; approve the pairing code on first contact.

Minimal config:

```
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

## What it is

Zalo is a Vietnam-focused messaging app; its Bot API lets the Gateway run a bot for 1:1 conversations. It is a good fit for support or notifications where you want deterministic routing back to Zalo.

*   A Zalo Bot API channel owned by the Gateway.
*   Deterministic routing: replies go back to Zalo; the model never chooses channels.
*   DMs share the agent’s main session.
*   Groups are supported with policy controls (`groupPolicy` + `groupAllowFrom`) and default to fail-closed allowlist behavior.

## Setup (fast path)

### 1) Create a bot token (Zalo Bot Platform)

1.  Go to [https://bot.zaloplatforms.com](https://bot.zaloplatforms.com/) and sign in.
2.  Create a new bot and configure its settings.
3.  Copy the bot token (format: `12345689:abc-xyz`).

### 2) Configure the token (env or config)

Example:

```
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

Env option: `ZALO_BOT_TOKEN=...` (works for the default account only). Multi-account support: use `channels.zalo.accounts` with per-account tokens and optional `name`.

3.  Restart the gateway. Zalo starts when a token is resolved (env or config).
4.  DM access defaults to pairing. Approve the code when the bot is first contacted.

## How it works (behavior)

*   Inbound messages are normalized into the shared channel envelope with media placeholders.
*   Replies always route back to the same Zalo chat.
*   Long-polling by default; webhook mode available with `channels.zalo.webhookUrl`.

## Limits

*   Outbound text is chunked to 2000 characters (Zalo API limit).
*   Media downloads/uploads are capped by `channels.zalo.mediaMaxMb` (default 5).
*   Streaming is blocked by default due to the 2000 char limit making streaming less useful.

## Access control (DMs)

### DM access

*   Default: `channels.zalo.dmPolicy = "pairing"`. Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
*   Approve via:
    *   `openclaw pairing list zalo`
    *   `openclaw pairing approve zalo <CODE>`
*   Pairing is the default token exchange. Details: [Pairing](https://docs.openclaw.ai/channels/pairing)
*   `channels.zalo.allowFrom` accepts numeric user IDs (no username lookup available).

## Access control (Groups)

*   `channels.zalo.groupPolicy` controls group inbound handling: `open | allowlist | disabled`.
*   Default behavior is fail-closed: `allowlist`.
*   `channels.zalo.groupAllowFrom` restricts which sender IDs can trigger the bot in groups.
*   If `groupAllowFrom` is unset, Zalo falls back to `allowFrom` for sender checks.
*   `groupPolicy: "disabled"` blocks all group messages.
*   `groupPolicy: "open"` allows any group member (mention-gated).
*   Runtime note: if `channels.zalo` is missing entirely, runtime still falls back to `groupPolicy="allowlist"` for safety.

## Long-polling vs webhook

*   Default: long-polling (no public URL required).
*   Webhook mode: set `channels.zalo.webhookUrl` and `channels.zalo.webhookSecret`.
    *   The webhook secret must be 8-256 characters.
    *   Webhook URL must use HTTPS.
    *   Zalo sends events with `X-Bot-Api-Secret-Token` header for verification.
    *   Gateway HTTP handles webhook requests at `channels.zalo.webhookPath` (defaults to the webhook URL path).
    *   Requests must use `Content-Type: application/json` (or `+json` media types).
    *   Duplicate events (`event_name + message_id`) are ignored for a short replay window.
    *   Burst traffic is rate-limited per path/source and may return HTTP 429.

**Note:** getUpdates (polling) and webhook are mutually exclusive per Zalo API docs.

## Supported message types

*   **Text messages**: Full support with 2000 character chunking.
*   **Image messages**: Download and process inbound images; send images via `sendPhoto`.
*   **Stickers**: Logged but not fully processed (no agent response).
*   **Unsupported types**: Logged (e.g., messages from protected users).

## Capabilities

| Feature | Status |
| --- | --- |
| Direct messages | ✅ Supported |
| Groups | ⚠️ Supported with policy controls (allowlist by default) |
| Media (images) | ✅ Supported |
| Reactions | ❌ Not supported |
| Threads | ❌ Not supported |
| Polls | ❌ Not supported |
| Native commands | ❌ Not supported |
| Streaming | ⚠️ Blocked (2000 char limit) |

## Delivery targets (CLI/cron)

*   Use a chat id as the target.
*   Example: `openclaw message send --channel zalo --target 123456789 --message "hi"`.

## Troubleshooting

**Bot doesn’t respond:**

*   Check that the token is valid: `openclaw channels status --probe`
*   Verify the sender is approved (pairing or allowFrom)
*   Check gateway logs: `openclaw logs --follow`

**Webhook not receiving events:**

*   Ensure webhook URL uses HTTPS
*   Verify secret token is 8-256 characters
*   Confirm the gateway HTTP endpoint is reachable on the configured path
*   Check that getUpdates polling is not running (they’re mutually exclusive)

## Configuration reference (Zalo)

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.zalo.enabled`: enable/disable channel startup.
*   `channels.zalo.botToken`: bot token from Zalo Bot Platform.
*   `channels.zalo.tokenFile`: read token from file path.
*   `channels.zalo.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).
*   `channels.zalo.allowFrom`: DM allowlist (user IDs). `open` requires `"*"`. The wizard will ask for numeric IDs.
*   `channels.zalo.groupPolicy`: `open | allowlist | disabled` (default: allowlist).
*   `channels.zalo.groupAllowFrom`: group sender allowlist (user IDs). Falls back to `allowFrom` when unset.
*   `channels.zalo.mediaMaxMb`: inbound/outbound media cap (MB, default 5).
*   `channels.zalo.webhookUrl`: enable webhook mode (HTTPS required).
*   `channels.zalo.webhookSecret`: webhook secret (8-256 chars).
*   `channels.zalo.webhookPath`: webhook path on the gateway HTTP server.
*   `channels.zalo.proxy`: proxy URL for API requests.

Multi-account options:

*   `channels.zalo.accounts.<id>.botToken`: per-account token.
*   `channels.zalo.accounts.<id>.tokenFile`: per-account token file.
*   `channels.zalo.accounts.<id>.name`: display name.
*   `channels.zalo.accounts.<id>.enabled`: enable/disable account.
*   `channels.zalo.accounts.<id>.dmPolicy`: per-account DM policy.
*   `channels.zalo.accounts.<id>.allowFrom`: per-account allowlist.
*   `channels.zalo.accounts.<id>.groupPolicy`: per-account group policy.
*   `channels.zalo.accounts.<id>.groupAllowFrom`: per-account group sender allowlist.
*   `channels.zalo.accounts.<id>.webhookUrl`: per-account webhook URL.
*   `channels.zalo.accounts.<id>.webhookSecret`: per-account webhook secret.
*   `channels.zalo.accounts.<id>.webhookPath`: per-account webhook path.
*   `channels.zalo.accounts.<id>.proxy`: per-account proxy URL.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/signal -->

# Signal - OpenClaw

Status: external CLI integration. Gateway talks to `signal-cli` over HTTP JSON-RPC + SSE.

## Prerequisites

*   OpenClaw installed on your server (Linux flow below tested on Ubuntu 24).
*   `signal-cli` available on the host where the gateway runs.
*   A phone number that can receive one verification SMS (for SMS registration path).
*   Browser access for Signal captcha (`signalcaptchas.org`) during registration.

## Quick setup (beginner)

1.  Use a **separate Signal number** for the bot (recommended).
2.  Install `signal-cli` (Java required if you use the JVM build).
3.  Choose one setup path:
    *   **Path A (QR link):** `signal-cli link -n "OpenClaw"` and scan with Signal.
    *   **Path B (SMS register):** register a dedicated number with captcha + SMS verification.
4.  Configure OpenClaw and restart the gateway.
5.  Send a first DM and approve pairing (`openclaw pairing approve signal <CODE>`).

Minimal config:

```
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Field reference:

| Field | Description |
| --- | --- |
| `account` | Bot phone number in E.164 format (`+15551234567`) |
| `cliPath` | Path to `signal-cli` (`signal-cli` if on `PATH`) |
| `dmPolicy` | DM access policy (`pairing` recommended) |
| `allowFrom` | Phone numbers or `uuid:<id>` values allowed to DM |

## What it is

*   Signal channel via `signal-cli` (not embedded libsignal).
*   Deterministic routing: replies always go back to Signal.
*   DMs share the agent’s main session; groups are isolated (`agent:<agentId>:signal:group:<groupId>`).

## Config writes

By default, Signal is allowed to write config updates triggered by `/config set|unset` (requires `commands.config: true`). Disable with:

```
{
  channels: { signal: { configWrites: false } },
}
```

## The number model (important)

*   The gateway connects to a **Signal device** (the `signal-cli` account).
*   If you run the bot on **your personal Signal account**, it will ignore your own messages (loop protection).
*   For “I text the bot and it replies,” use a **separate bot number**.

## Setup path A: link existing Signal account (QR)

1.  Install `signal-cli` (JVM or native build).
2.  Link a bot account:
    *   `signal-cli link -n "OpenClaw"` then scan the QR in Signal.
3.  Configure Signal and start the gateway.

Example:

```
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Multi-account support: use `channels.signal.accounts` with per-account config and optional `name`. See [`gateway/configuration`](https://docs.openclaw.ai/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) for the shared pattern.

## Setup path B: register dedicated bot number (SMS, Linux)

Use this when you want a dedicated bot number instead of linking an existing Signal app account.

1.  Get a number that can receive SMS (or voice verification for landlines).
    *   Use a dedicated bot number to avoid account/session conflicts.
2.  Install `signal-cli` on the gateway host:

```
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz"
sudo tar xf "signal-cli-${VERSION}-Linux-native.tar.gz" -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/
signal-cli --version
```

If you use the JVM build (`signal-cli-${VERSION}.tar.gz`), install JRE 25+ first. Keep `signal-cli` updated; upstream notes that old releases can break as Signal server APIs change.

3.  Register and verify the number:

```
signal-cli -a +<BOT_PHONE_NUMBER> register
```

If captcha is required:

1.  Open `https://signalcaptchas.org/registration/generate.html`.
2.  Complete captcha, copy the `signalcaptcha://...` link target from “Open Signal”.
3.  Run from the same external IP as the browser session when possible.
4.  Run registration again immediately (captcha tokens expire quickly):

```
signal-cli -a +<BOT_PHONE_NUMBER> register --captcha '<SIGNALCAPTCHA_URL>'
signal-cli -a +<BOT_PHONE_NUMBER> verify <VERIFICATION_CODE>
```

4.  Configure OpenClaw, restart gateway, verify channel:

```
# If you run the gateway as a user systemd service:
systemctl --user restart openclaw-gateway

# Then verify:
openclaw doctor
openclaw channels status --probe
```

5.  Pair your DM sender:
    *   Send any message to the bot number.
    *   Approve code on the server: `openclaw pairing approve signal <PAIRING_CODE>`.
    *   Save the bot number as a contact on your phone to avoid “Unknown contact”.

Important: registering a phone number account with `signal-cli` can de-authenticate the main Signal app session for that number. Prefer a dedicated bot number, or use QR link mode if you need to keep your existing phone app setup. Upstream references:

*   `signal-cli` README: `https://github.com/AsamK/signal-cli`
*   Captcha flow: `https://github.com/AsamK/signal-cli/wiki/Registration-with-captcha`
*   Linking flow: `https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-(Provisioning)`

## External daemon mode (httpUrl)

If you want to manage `signal-cli` yourself (slow JVM cold starts, container init, or shared CPUs), run the daemon separately and point OpenClaw at it:

```
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

This skips auto-spawn and the startup wait inside OpenClaw. For slow starts when auto-spawning, set `channels.signal.startupTimeoutMs`.

## Access control (DMs + groups)

DMs:

*   Default: `channels.signal.dmPolicy = "pairing"`.
*   Unknown senders receive a pairing code; messages are ignored until approved (codes expire after 1 hour).
*   Approve via:
    *   `openclaw pairing list signal`
    *   `openclaw pairing approve signal <CODE>`
*   Pairing is the default token exchange for Signal DMs. Details: [Pairing](https://docs.openclaw.ai/channels/pairing)
*   UUID-only senders (from `sourceUuid`) are stored as `uuid:<id>` in `channels.signal.allowFrom`.

Groups:

*   `channels.signal.groupPolicy = open | allowlist | disabled`.
*   `channels.signal.groupAllowFrom` controls who can trigger in groups when `allowlist` is set.
*   Runtime note: if `channels.signal` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks (even if `channels.defaults.groupPolicy` is set).

## How it works (behavior)

*   `signal-cli` runs as a daemon; the gateway reads events via SSE.
*   Inbound messages are normalized into the shared channel envelope.
*   Replies always route back to the same number or group.

*   Outbound text is chunked to `channels.signal.textChunkLimit` (default 4000).
*   Optional newline chunking: set `channels.signal.chunkMode="newline"` to split on blank lines (paragraph boundaries) before length chunking.
*   Attachments supported (base64 fetched from `signal-cli`).
*   Default media cap: `channels.signal.mediaMaxMb` (default 8).
*   Use `channels.signal.ignoreAttachments` to skip downloading media.
*   Group history context uses `channels.signal.historyLimit` (or `channels.signal.accounts.*.historyLimit`), falling back to `messages.groupChat.historyLimit`. Set `0` to disable (default 50).

## Typing + read receipts

*   **Typing indicators**: OpenClaw sends typing signals via `signal-cli sendTyping` and refreshes them while a reply is running.
*   **Read receipts**: when `channels.signal.sendReadReceipts` is true, OpenClaw forwards read receipts for allowed DMs.
*   Signal-cli does not expose read receipts for groups.

*   Use `message action=react` with `channel=signal`.
*   Targets: sender E.164 or UUID (use `uuid:<id>` from pairing output; bare UUID works too).
*   `messageId` is the Signal timestamp for the message you’re reacting to.
*   Group reactions require `targetAuthor` or `targetAuthorUuid`.

Examples:

```
message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥
message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true
message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅
```

Config:

*   `channels.signal.actions.reactions`: enable/disable reaction actions (default true).
*   `channels.signal.reactionLevel`: `off | ack | minimal | extensive`.
    *   `off`/`ack` disables agent reactions (message tool `react` will error).
    *   `minimal`/`extensive` enables agent reactions and sets the guidance level.
*   Per-account overrides: `channels.signal.accounts.<id>.actions.reactions`, `channels.signal.accounts.<id>.reactionLevel`.

## Delivery targets (CLI/cron)

*   DMs: `signal:+15551234567` (or plain E.164).
*   UUID DMs: `uuid:<id>` (or bare UUID).
*   Groups: `signal:group:<groupId>`.
*   Usernames: `username:<name>` (if supported by your Signal account).

## Troubleshooting

Run this ladder first:

```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Then confirm DM pairing state if needed:

```
openclaw pairing list signal
```

Common failures:

*   Daemon reachable but no replies: verify account/daemon settings (`httpUrl`, `account`) and receive mode.
*   DMs ignored: sender is pending pairing approval.
*   Group messages ignored: group sender/mention gating blocks delivery.
*   Config validation errors after edits: run `openclaw doctor --fix`.
*   Signal missing from diagnostics: confirm `channels.signal.enabled: true`.

Extra checks:

```
openclaw pairing list signal
pgrep -af signal-cli
grep -i "signal" "/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log" | tail -20
```

For triage flow: [/channels/troubleshooting](https://docs.openclaw.ai/channels/troubleshooting).

## Security notes

*   `signal-cli` stores account keys locally (typically `~/.local/share/signal-cli/data/`).
*   Back up Signal account state before server migration or rebuild.
*   Keep `channels.signal.dmPolicy: "pairing"` unless you explicitly want broader DM access.
*   SMS verification is only needed for registration or recovery flows, but losing control of the number/account can complicate re-registration.

## Configuration reference (Signal)

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.signal.enabled`: enable/disable channel startup.
*   `channels.signal.account`: E.164 for the bot account.
*   `channels.signal.cliPath`: path to `signal-cli`.
*   `channels.signal.httpUrl`: full daemon URL (overrides host/port).
*   `channels.signal.httpHost`, `channels.signal.httpPort`: daemon bind (default 127.0.0.1:8080).
*   `channels.signal.autoStart`: auto-spawn daemon (default true if `httpUrl` unset).
*   `channels.signal.startupTimeoutMs`: startup wait timeout in ms (cap 120000).
*   `channels.signal.receiveMode`: `on-start | manual`.
*   `channels.signal.ignoreAttachments`: skip attachment downloads.
*   `channels.signal.ignoreStories`: ignore stories from the daemon.
*   `channels.signal.sendReadReceipts`: forward read receipts.
*   `channels.signal.dmPolicy`: `pairing | allowlist | open | disabled` (default: pairing).
*   `channels.signal.allowFrom`: DM allowlist (E.164 or `uuid:<id>`). `open` requires `"*"`. Signal has no usernames; use phone/UUID ids.
*   `channels.signal.groupPolicy`: `open | allowlist | disabled` (default: allowlist).
*   `channels.signal.groupAllowFrom`: group sender allowlist.
*   `channels.signal.historyLimit`: max group messages to include as context (0 disables).
*   `channels.signal.dmHistoryLimit`: DM history limit in user turns. Per-user overrides: `channels.signal.dms["<phone_or_uuid>"].historyLimit`.
*   `channels.signal.textChunkLimit`: outbound chunk size (chars).
*   `channels.signal.chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
*   `channels.signal.mediaMaxMb`: inbound/outbound media cap (MB).

Related global options:

*   `agents.list[].groupChat.mentionPatterns` (Signal does not support native mentions).
*   `messages.groupChat.mentionPatterns` (global fallback).
*   `messages.responsePrefix`.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/tlon -->

# Tlon - OpenClaw

## Tlon (plugin)

Tlon is a decentralized messenger built on Urbit. OpenClaw connects to your Urbit ship and can respond to DMs and group chat messages. Group replies require an @ mention by default and can be further restricted via allowlists. Status: supported via plugin. DMs, group mentions, thread replies, rich text formatting, and image uploads are supported. Reactions and polls are not yet supported.

## Plugin required

Tlon ships as a plugin and is not bundled with the core install. Install via CLI (npm registry):

```
openclaw plugins install @openclaw/tlon
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/tlon
```

Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Setup

1.  Install the Tlon plugin.
2.  Gather your ship URL and login code.
3.  Configure `channels.tlon`.
4.  Restart the gateway.
5.  DM the bot or mention it in a group channel.

Minimal config (single account):

```
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
      ownerShip: "~your-main-ship", // recommended: your ship, always allowed
    },
  },
}
```

## Private/LAN ships

By default, OpenClaw blocks private/internal hostnames and IP ranges for SSRF protection. If your ship is running on a private network (localhost, LAN IP, or internal hostname), you must explicitly opt in:

```
{
  channels: {
    tlon: {
      url: "http://localhost:8080",
      allowPrivateNetwork: true,
    },
  },
}
```

This applies to URLs like:

*   `http://localhost:8080`
*   `http://192.168.x.x:8080`
*   `http://my-ship.local:8080`

⚠️ Only enable this if you trust your local network. This setting disables SSRF protections for requests to your ship URL.

## Group channels

Auto-discovery is enabled by default. You can also pin channels manually:

```
{
  channels: {
    tlon: {
      groupChannels: ["chat/~host-ship/general", "chat/~host-ship/support"],
    },
  },
}
```

Disable auto-discovery:

```
{
  channels: {
    tlon: {
      autoDiscoverChannels: false,
    },
  },
}
```

## Access control

DM allowlist (empty = no DMs allowed, use `ownerShip` for approval flow):

```
{
  channels: {
    tlon: {
      dmAllowlist: ["~zod", "~nec"],
    },
  },
}
```

Group authorization (restricted by default):

```
{
  channels: {
    tlon: {
      defaultAuthorizedShips: ["~zod"],
      authorization: {
        channelRules: {
          "chat/~host-ship/general": {
            mode: "restricted",
            allowedShips: ["~zod", "~nec"],
          },
          "chat/~host-ship/announcements": {
            mode: "open",
          },
        },
      },
    },
  },
}
```

## Owner and approval system

Set an owner ship to receive approval requests when unauthorized users try to interact:

```
{
  channels: {
    tlon: {
      ownerShip: "~your-main-ship",
    },
  },
}
```

The owner ship is **automatically authorized everywhere** — DM invites are auto-accepted and channel messages are always allowed. You don’t need to add the owner to `dmAllowlist` or `defaultAuthorizedShips`. When set, the owner receives DM notifications for:

*   DM requests from ships not in the allowlist
*   Mentions in channels without authorization
*   Group invite requests

## Auto-accept settings

Auto-accept DM invites (for ships in dmAllowlist):

```
{
  channels: {
    tlon: {
      autoAcceptDmInvites: true,
    },
  },
}
```

Auto-accept group invites:

```
{
  channels: {
    tlon: {
      autoAcceptGroupInvites: true,
    },
  },
}
```

## Delivery targets (CLI/cron)

Use these with `openclaw message send` or cron delivery:

*   DM: `~sampel-palnet` or `dm/~sampel-palnet`
*   Group: `chat/~host-ship/channel` or `group:~host-ship/channel`

## Bundled skill

The Tlon plugin includes a bundled skill ([`@tloncorp/tlon-skill`](https://github.com/tloncorp/tlon-skill)) that provides CLI access to Tlon operations:

*   **Contacts**: get/update profiles, list contacts
*   **Channels**: list, create, post messages, fetch history
*   **Groups**: list, create, manage members
*   **DMs**: send messages, react to messages
*   **Reactions**: add/remove emoji reactions to posts and DMs
*   **Settings**: manage plugin permissions via slash commands

The skill is automatically available when the plugin is installed.

## Capabilities

| Feature | Status |
| --- | --- |
| Direct messages | ✅ Supported |
| Groups/channels | ✅ Supported (mention-gated by default) |
| Threads | ✅ Supported (auto-replies in thread) |
| Rich text | ✅ Markdown converted to Tlon format |
| Images | ✅ Uploaded to Tlon storage |
| Reactions | ✅ Via [bundled skill](https://docs.openclaw.ai/channels/tlon#bundled-skill) |
| Polls | ❌ Not yet supported |
| Native commands | ✅ Supported (owner-only by default) |

## Troubleshooting

Run this ladder first:

```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
```

Common failures:

*   **DMs ignored**: sender not in `dmAllowlist` and no `ownerShip` configured for approval flow.
*   **Group messages ignored**: channel not discovered or sender not authorized.
*   **Connection errors**: check ship URL is reachable; enable `allowPrivateNetwork` for local ships.
*   **Auth errors**: verify login code is current (codes rotate).

## Configuration reference

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Provider options:

*   `channels.tlon.enabled`: enable/disable channel startup.
*   `channels.tlon.ship`: bot’s Urbit ship name (e.g. `~sampel-palnet`).
*   `channels.tlon.url`: ship URL (e.g. `https://sampel-palnet.tlon.network`).
*   `channels.tlon.code`: ship login code.
*   `channels.tlon.allowPrivateNetwork`: allow localhost/LAN URLs (SSRF bypass).
*   `channels.tlon.ownerShip`: owner ship for approval system (always authorized).
*   `channels.tlon.dmAllowlist`: ships allowed to DM (empty = none).
*   `channels.tlon.autoAcceptDmInvites`: auto-accept DMs from allowlisted ships.
*   `channels.tlon.autoAcceptGroupInvites`: auto-accept all group invites.
*   `channels.tlon.autoDiscoverChannels`: auto-discover group channels (default: true).
*   `channels.tlon.groupChannels`: manually pinned channel nests.
*   `channels.tlon.defaultAuthorizedShips`: ships authorized for all channels.
*   `channels.tlon.authorization.channelRules`: per-channel auth rules.
*   `channels.tlon.showModelSignature`: append model name to messages.

## Notes

*   Group replies require a mention (e.g. `~your-bot-ship`) to respond.
*   Thread replies: if the inbound message is in a thread, OpenClaw replies in-thread.
*   Rich text: Markdown formatting (bold, italic, code, headers, lists) is converted to Tlon’s native format.
*   Images: URLs are uploaded to Tlon storage and embedded as image blocks.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/pairing -->

# Pairing - OpenClaw

“Pairing” is OpenClaw’s explicit **owner approval** step. It is used in two places:

1.  **DM pairing** (who is allowed to talk to the bot)
2.  **Node pairing** (which devices/nodes are allowed to join the gateway network)

Security context: [Security](https://docs.openclaw.ai/gateway/security)

## 1) DM pairing (inbound chat access)

When a channel is configured with DM policy `pairing`, unknown senders get a short code and their message is **not processed** until you approve. Default DM policies are documented in: [Security](https://docs.openclaw.ai/gateway/security) Pairing codes:

*   8 characters, uppercase, no ambiguous chars (`0O1I`).
*   **Expire after 1 hour**. The bot only sends the pairing message when a new request is created (roughly once per hour per sender).
*   Pending DM pairing requests are capped at **3 per channel** by default; additional requests are ignored until one expires or is approved.

### Approve a sender

```
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`, `feishu`.

### Where the state lives

Stored under `~/.openclaw/credentials/`:

*   Pending requests: `<channel>-pairing.json`
*   Approved allowlist store:
    *   Default account: `<channel>-allowFrom.json`
    *   Non-default account: `<channel>-<accountId>-allowFrom.json`

Account scoping behavior:

*   Non-default accounts read/write only their scoped allowlist file.
*   Default account uses the channel-scoped unscoped allowlist file.

Treat these as sensitive (they gate access to your assistant).

## 2) Node device pairing (iOS/Android/macOS/headless nodes)

Nodes connect to the Gateway as **devices** with `role: node`. The Gateway creates a device pairing request that must be approved.

### Pair via Telegram (recommended for iOS)

If you use the `device-pair` plugin, you can do first-time device pairing entirely from Telegram:

1.  In Telegram, message your bot: `/pair`
2.  The bot replies with two messages: an instruction message and a separate **setup code** message (easy to copy/paste in Telegram).
3.  On your phone, open the OpenClaw iOS app → Settings → Gateway.
4.  Paste the setup code and connect.
5.  Back in Telegram: `/pair approve`

The setup code is a base64-encoded JSON payload that contains:

*   `url`: the Gateway WebSocket URL (`ws://...` or `wss://...`)
*   `token`: a short-lived pairing token

Treat the setup code like a password while it is valid.

### Approve a node device

```
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

### Node pairing state storage

Stored under `~/.openclaw/devices/`:

*   `pending.json` (short-lived; pending requests expire)
*   `paired.json` (paired devices + tokens)

### Notes

*   The legacy `node.pair.*` API (CLI: `openclaw nodes pending/approve`) is a separate gateway-owned pairing store. WS nodes still require device pairing.

*   Security model + prompt injection: [Security](https://docs.openclaw.ai/gateway/security)
*   Updating safely (run doctor): [Updating](https://docs.openclaw.ai/install/updating)
*   Channel configs:
    *   Telegram: [Telegram](https://docs.openclaw.ai/channels/telegram)
    *   WhatsApp: [WhatsApp](https://docs.openclaw.ai/channels/whatsapp)
    *   Signal: [Signal](https://docs.openclaw.ai/channels/signal)
    *   BlueBubbles (iMessage): [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles)
    *   iMessage (legacy): [iMessage](https://docs.openclaw.ai/channels/imessage)
    *   Discord: [Discord](https://docs.openclaw.ai/channels/discord)
    *   Slack: [Slack](https://docs.openclaw.ai/channels/slack)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/line -->

# LINE - OpenClaw

## LINE (plugin)

LINE connects to OpenClaw via the LINE Messaging API. The plugin runs as a webhook receiver on the gateway and uses your channel access token + channel secret for authentication. Status: supported via plugin. Direct messages, group chats, media, locations, Flex messages, template messages, and quick replies are supported. Reactions and threads are not supported.

## Plugin required

Install the LINE plugin:

```
openclaw plugins install @openclaw/line
```

Local checkout (when running from a git repo):

```
openclaw plugins install ./extensions/line
```

## Setup

1.  Create a LINE Developers account and open the Console: [https://developers.line.biz/console/](https://developers.line.biz/console/)
2.  Create (or pick) a Provider and add a **Messaging API** channel.
3.  Copy the **Channel access token** and **Channel secret** from the channel settings.
4.  Enable **Use webhook** in the Messaging API settings.
5.  Set the webhook URL to your gateway endpoint (HTTPS required):

```
https://gateway-host/line/webhook
```

The gateway responds to LINE’s webhook verification (GET) and inbound events (POST). If you need a custom path, set `channels.line.webhookPath` or `channels.line.accounts.<id>.webhookPath` and update the URL accordingly. Security note:

*   LINE signature verification is body-dependent (HMAC over the raw body), so OpenClaw applies strict pre-auth body limits and timeout before verification.

## Configure

Minimal config:

```
{
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "pairing",
    },
  },
}
```

Env vars (default account only):

*   `LINE_CHANNEL_ACCESS_TOKEN`
*   `LINE_CHANNEL_SECRET`

Token/secret files:

```
{
  channels: {
    line: {
      tokenFile: "/path/to/line-token.txt",
      secretFile: "/path/to/line-secret.txt",
    },
  },
}
```

Multiple accounts:

```
{
  channels: {
    line: {
      accounts: {
        marketing: {
          channelAccessToken: "...",
          channelSecret: "...",
          webhookPath: "/line/marketing",
        },
      },
    },
  },
}
```

## Access control

Direct messages default to pairing. Unknown senders get a pairing code and their messages are ignored until approved.

```
openclaw pairing list line
openclaw pairing approve line <CODE>
```

Allowlists and policies:

*   `channels.line.dmPolicy`: `pairing | allowlist | open | disabled`
*   `channels.line.allowFrom`: allowlisted LINE user IDs for DMs
*   `channels.line.groupPolicy`: `allowlist | open | disabled`
*   `channels.line.groupAllowFrom`: allowlisted LINE user IDs for groups
*   Per-group overrides: `channels.line.groups.<groupId>.allowFrom`
*   Runtime note: if `channels.line` is completely missing, runtime falls back to `groupPolicy="allowlist"` for group checks (even if `channels.defaults.groupPolicy` is set).

LINE IDs are case-sensitive. Valid IDs look like:

*   User: `U` + 32 hex chars
*   Group: `C` + 32 hex chars
*   Room: `R` + 32 hex chars

## Message behavior

*   Text is chunked at 5000 characters.
*   Markdown formatting is stripped; code blocks and tables are converted into Flex cards when possible.
*   Streaming responses are buffered; LINE receives full chunks with a loading animation while the agent works.
*   Media downloads are capped by `channels.line.mediaMaxMb` (default 10).

## Channel data (rich messages)

Use `channelData.line` to send quick replies, locations, Flex cards, or template messages.

```
{
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: {
        title: "Office",
        address: "123 Main St",
        latitude: 35.681236,
        longitude: 139.767125,
      },
      flexMessage: {
        altText: "Status card",
        contents: {
          /* Flex payload */
        },
      },
      templateMessage: {
        type: "confirm",
        text: "Proceed?",
        confirmLabel: "Yes",
        confirmData: "yes",
        cancelLabel: "No",
        cancelData: "no",
      },
    },
  },
}
```

The LINE plugin also ships a `/card` command for Flex message presets:

```
/card info "Welcome" "Thanks for joining!"
```

## Troubleshooting

*   **Webhook verification fails:** ensure the webhook URL is HTTPS and the `channelSecret` matches the LINE console.
*   **No inbound events:** confirm the webhook path matches `channels.line.webhookPath` and that the gateway is reachable from LINE.
*   **Media download errors:** raise `channels.line.mediaMaxMb` if media exceeds the default limit.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/group-messages -->

# Group Messages - OpenClaw

## Group messages (WhatsApp web channel)

Goal: let Clawd sit in WhatsApp groups, wake up only when pinged, and keep that thread separate from the personal DM session. Note: `agents.list[].groupChat.mentionPatterns` is now used by Telegram/Discord/Slack/iMessage as well; this doc focuses on WhatsApp-specific behavior. For multi-agent setups, set `agents.list[].groupChat.mentionPatterns` per agent (or use `messages.groupChat.mentionPatterns` as a global fallback).

## What’s implemented (2025-12-03)

*   Activation modes: `mention` (default) or `always`. `mention` requires a ping (real WhatsApp @-mentions via `mentionedJids`, regex patterns, or the bot’s E.164 anywhere in the text). `always` wakes the agent on every message but it should reply only when it can add meaningful value; otherwise it returns the silent token `NO_REPLY`. Defaults can be set in config (`channels.whatsapp.groups`) and overridden per group via `/activation`. When `channels.whatsapp.groups` is set, it also acts as a group allowlist (include `"*"` to allow all).
*   Group policy: `channels.whatsapp.groupPolicy` controls whether group messages are accepted (`open|disabled|allowlist`). `allowlist` uses `channels.whatsapp.groupAllowFrom` (fallback: explicit `channels.whatsapp.allowFrom`). Default is `allowlist` (blocked until you add senders).
*   Per-group sessions: session keys look like `agent:<agentId>:whatsapp:group:<jid>` so commands such as `/verbose on` or `/think high` (sent as standalone messages) are scoped to that group; personal DM state is untouched. Heartbeats are skipped for group threads.
*   Context injection: **pending-only** group messages (default 50) that _did not_ trigger a run are prefixed under `[Chat messages since your last reply - for context]`, with the triggering line under `[Current message - respond to this]`. Messages already in the session are not re-injected.
*   Sender surfacing: every group batch now ends with `[from: Sender Name (+E164)]` so Pi knows who is speaking.
*   Ephemeral/view-once: we unwrap those before extracting text/mentions, so pings inside them still trigger.
*   Group system prompt: on the first turn of a group session (and whenever `/activation` changes the mode) we inject a short blurb into the system prompt like `You are replying inside the WhatsApp group "<subject>". Group members: Alice (+44...), Bob (+43...), … Activation: trigger-only … Address the specific sender noted in the message context.` If metadata isn’t available we still tell the agent it’s a group chat.

## Config example (WhatsApp)

Add a `groupChat` block to `~/.openclaw/openclaw.json` so display-name pings work even when WhatsApp strips the visual `@` in the text body:

```
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          historyLimit: 50,
          mentionPatterns: ["@?openclaw", "\\+?15555550123"],
        },
      },
    ],
  },
}
```

Notes:

*   The regexes are case-insensitive; they cover a display-name ping like `@openclaw` and the raw number with or without `+`/spaces.
*   WhatsApp still sends canonical mentions via `mentionedJids` when someone taps the contact, so the number fallback is rarely needed but is a useful safety net.

### Activation command (owner-only)

Use the group chat command:

*   `/activation mention`
*   `/activation always`

Only the owner number (from `channels.whatsapp.allowFrom`, or the bot’s own E.164 when unset) can change this. Send `/status` as a standalone message in the group to see the current activation mode.

## How to use

1.  Add your WhatsApp account (the one running OpenClaw) to the group.
2.  Say `@openclaw …` (or include the number). Only allowlisted senders can trigger it unless you set `groupPolicy: "open"`.
3.  The agent prompt will include recent group context plus the trailing `[from: …]` marker so it can address the right person.
4.  Session-level directives (`/verbose on`, `/think high`, `/new` or `/reset`, `/compact`) apply only to that group’s session; send them as standalone messages so they register. Your personal DM session remains independent.

## Testing / verification

*   Manual smoke:
    *   Send an `@openclaw` ping in the group and confirm a reply that references the sender name.
    *   Send a second ping and verify the history block is included then cleared on the next turn.
*   Check gateway logs (run with `--verbose`) to see `inbound web message` entries showing `from: <groupJid>` and the `[from: …]` suffix.

## Known considerations

*   Heartbeats are intentionally skipped for groups to avoid noisy broadcasts.
*   Echo suppression uses the combined batch string; if you send identical text twice without mentions, only the first will get a response.
*   Session store entries will appear as `agent:<agentId>:whatsapp:group:<jid>` in the session store (`~/.openclaw/agents/<agentId>/sessions/sessions.json` by default); a missing entry just means the group hasn’t triggered a run yet.
*   Typing indicators in groups follow `agents.defaults.typingMode` (default: `message` when unmentioned).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/whatsapp -->

# WhatsApp - OpenClaw

## WhatsApp (Web channel)

Status: production-ready via WhatsApp Web (Baileys). Gateway owns linked session(s).

## Quick setup

## Deployment patterns

## Runtime model

*   Gateway owns the WhatsApp socket and reconnect loop.
*   Outbound sends require an active WhatsApp listener for the target account.
*   Status and broadcast chats are ignored (`@status`, `@broadcast`).
*   Direct chats use DM session rules (`session.dmScope`; default `main` collapses DMs to the agent main session).
*   Group sessions are isolated (`agent:<agentId>:whatsapp:group:<jid>`).

## Access control and activation

*   DM policy
    
*   Group policy + allowlists
    
*   Mentions + /activation
    

`channels.whatsapp.dmPolicy` controls direct chat access:

*   `pairing` (default)
*   `allowlist`
*   `open` (requires `allowFrom` to include `"*"`)
*   `disabled`

`allowFrom` accepts E.164-style numbers (normalized internally).Multi-account override: `channels.whatsapp.accounts.<id>.dmPolicy` (and `allowFrom`) take precedence over channel-level defaults for that account.Runtime behavior details:

*   pairings are persisted in channel allow-store and merged with configured `allowFrom`
*   if no allowlist is configured, the linked self number is allowed by default
*   outbound `fromMe` DMs are never auto-paired

Group access has two layers:

1.  **Group membership allowlist** (`channels.whatsapp.groups`)
    *   if `groups` is omitted, all groups are eligible
    *   if `groups` is present, it acts as a group allowlist (`"*"` allowed)
2.  **Group sender policy** (`channels.whatsapp.groupPolicy` + `groupAllowFrom`)
    *   `open`: sender allowlist bypassed
    *   `allowlist`: sender must match `groupAllowFrom` (or `*`)
    *   `disabled`: block all group inbound

Sender allowlist fallback:

*   if `groupAllowFrom` is unset, runtime falls back to `allowFrom` when available
*   sender allowlists are evaluated before mention/reply activation

Note: if no `channels.whatsapp` block exists at all, runtime group-policy fallback is `allowlist` (with a warning log), even if `channels.defaults.groupPolicy` is set.

Group replies require mention by default.Mention detection includes:

*   explicit WhatsApp mentions of the bot identity
*   configured mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)
*   implicit reply-to-bot detection (reply sender matches bot identity)

Security note:

*   quote/reply only satisfies mention gating; it does **not** grant sender authorization
*   with `groupPolicy: "allowlist"`, non-allowlisted senders are still blocked even if they reply to an allowlisted user’s message

Session-level activation command:

*   `/activation mention`
*   `/activation always`

`activation` updates session state (not global config). It is owner-gated.

## Personal-number and self-chat behavior

When the linked self number is also present in `allowFrom`, WhatsApp self-chat safeguards activate:

*   skip read receipts for self-chat turns
*   ignore mention-JID auto-trigger behavior that would otherwise ping yourself
*   if `messages.responsePrefix` is unset, self-chat replies default to `[{identity.name}]` or `[openclaw]`

## Message normalization and context

## Acknowledgment reactions

WhatsApp supports immediate ack reactions on inbound receipt via `channels.whatsapp.ackReaction`.

```
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

*   sent immediately after inbound is accepted (pre-reply)
*   failures are logged but do not block normal reply delivery
*   group mode `mentions` reacts on mention-triggered turns; group activation `always` acts as bypass for this check
*   WhatsApp uses `channels.whatsapp.ackReaction` (legacy `messages.ackReaction` is not used here)

## Multi-account and credentials

*   Agent tool support includes WhatsApp reaction action (`react`).
*   Action gates:
    *   `channels.whatsapp.actions.reactions`
    *   `channels.whatsapp.actions.polls`
*   Channel-initiated config writes are enabled by default (disable via `channels.whatsapp.configWrites=false`).

## Troubleshooting

## Configuration reference pointers

Primary reference:

*   [Configuration reference - WhatsApp](https://docs.openclaw.ai/gateway/configuration-reference#whatsapp)

High-signal WhatsApp fields:

*   access: `dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`
*   delivery: `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `sendReadReceipts`, `ackReaction`
*   multi-account: `accounts.<id>.enabled`, `accounts.<id>.authDir`, account-level overrides
*   operations: `configWrites`, `debounceMs`, `web.enabled`, `web.heartbeatSeconds`, `web.reconnect.*`
*   session behavior: `session.dmScope`, `historyLimit`, `dmHistoryLimit`, `dms.<id>.historyLimit`

*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [Channel routing](https://docs.openclaw.ai/channels/channel-routing)
*   [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
*   [Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/zalouser -->

# Zalo Personal - OpenClaw

## Zalo Personal (unofficial)

Status: experimental. This integration automates a **personal Zalo account** via native `zca-js` inside OpenClaw.

> **Warning:** This is an unofficial integration and may result in account suspension/ban. Use at your own risk.

## Plugin required

Zalo Personal ships as a plugin and is not bundled with the core install.

*   Install via CLI: `openclaw plugins install @openclaw/zalouser`
*   Or from a source checkout: `openclaw plugins install ./extensions/zalouser`
*   Details: [Plugins](https://docs.openclaw.ai/tools/plugin)

No external `zca`/`openzca` CLI binary is required.

## Quick setup (beginner)

1.  Install the plugin (see above).
2.  Login (QR, on the Gateway machine):
    *   `openclaw channels login --channel zalouser`
    *   Scan the QR code with the Zalo mobile app.
3.  Enable the channel:

```
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

4.  Restart the Gateway (or finish onboarding).
5.  DM access defaults to pairing; approve the pairing code on first contact.

## What it is

*   Runs entirely in-process via `zca-js`.
*   Uses native event listeners to receive inbound messages.
*   Sends replies directly through the JS API (text/media/link).
*   Designed for “personal account” use cases where Zalo Bot API is not available.

## Naming

Channel id is `zalouser` to make it explicit this automates a **personal Zalo user account** (unofficial). We keep `zalo` reserved for a potential future official Zalo API integration.

## Finding IDs (directory)

Use the directory CLI to discover peers/groups and their IDs:

```
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## Limits

*   Outbound text is chunked to ~2000 characters (Zalo client limits).
*   Streaming is blocked by default.

## Access control (DMs)

`channels.zalouser.dmPolicy` supports: `pairing | allowlist | open | disabled` (default: `pairing`). `channels.zalouser.allowFrom` accepts user IDs or names. During onboarding, names are resolved to IDs using the plugin’s in-process contact lookup. Approve via:

*   `openclaw pairing list zalouser`
*   `openclaw pairing approve zalouser <code>`

## Group access (optional)

*   Default: `channels.zalouser.groupPolicy = "open"` (groups allowed). Use `channels.defaults.groupPolicy` to override the default when unset.
*   Restrict to an allowlist with:
    *   `channels.zalouser.groupPolicy = "allowlist"`
    *   `channels.zalouser.groups` (keys are group IDs or names; controls which groups are allowed)
    *   `channels.zalouser.groupAllowFrom` (controls which senders in allowed groups can trigger the bot)
*   Block all groups: `channels.zalouser.groupPolicy = "disabled"`.
*   The configure wizard can prompt for group allowlists.
*   On startup, OpenClaw resolves group/user names in allowlists to IDs and logs the mapping; unresolved entries are kept as typed.
*   If `groupAllowFrom` is unset, runtime falls back to `allowFrom` for group sender checks.
*   Sender checks apply to both normal group messages and control commands (for example `/new`, `/reset`).

Example:

```
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["1471383327500481391"],
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

### Group mention gating

*   `channels.zalouser.groups.<group>.requireMention` controls whether group replies require a mention.
*   Resolution order: exact group id/name -> normalized group slug -> `*` -> default (`true`).
*   This applies both to allowlisted groups and open group mode.
*   Authorized control commands (for example `/new`) can bypass mention gating.
*   When a group message is skipped because mention is required, OpenClaw stores it as pending group history and includes it on the next processed group message.
*   Group history limit defaults to `messages.groupChat.historyLimit` (fallback `50`). You can override per account with `channels.zalouser.historyLimit`.

Example:

```
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "*": { allow: true, requireMention: true },
        "Work Chat": { allow: true, requireMention: false },
      },
    },
  },
}
```

## Multi-account

Accounts map to `zalouser` profiles in OpenClaw state. Example:

```
{
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## Typing, reactions, and delivery acknowledgements

*   OpenClaw sends a typing event before dispatching a reply (best-effort).
*   Message reaction action `react` is supported for `zalouser` in channel actions.
    *   Use `remove: true` to remove a specific reaction emoji from a message.
    *   Reaction semantics: [Reactions](https://docs.openclaw.ai/tools/reactions)
*   For inbound messages that include event metadata, OpenClaw sends delivered + seen acknowledgements (best-effort).

## Troubleshooting

**Login doesn’t stick:**

*   `openclaw channels status --probe`
*   Re-login: `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`

**Allowlist/group name didn’t resolve:**

*   Use numeric IDs in `allowFrom`/`groupAllowFrom`/`groups`, or exact friend/group names.

**Upgraded from old CLI-based setup:**

*   Remove any old external `zca` process assumptions.
*   The channel now runs fully in OpenClaw without external CLI binaries.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/channel-routing -->

# Channel Routing - OpenClaw

## Channels & routing

OpenClaw routes replies **back to the channel where a message came from**. The model does not choose a channel; routing is deterministic and controlled by the host configuration.

## Key terms

*   **Channel**: `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`, `webchat`.
*   **AccountId**: per‑channel account instance (when supported).
*   Optional channel default account: `channels.<channel>.defaultAccount` chooses which account is used when an outbound path does not specify `accountId`.
    *   In multi-account setups, set an explicit default (`defaultAccount` or `accounts.default`) when two or more accounts are configured. Without it, fallback routing may pick the first normalized account ID.
*   **AgentId**: an isolated workspace + session store (“brain”).
*   **SessionKey**: the bucket key used to store context and control concurrency.

## Session key shapes (examples)

Direct messages collapse to the agent’s **main** session:

*   `agent:<agentId>:<mainKey>` (default: `agent:main:main`)

Groups and channels remain isolated per channel:

*   Groups: `agent:<agentId>:<channel>:group:<id>`
*   Channels/rooms: `agent:<agentId>:<channel>:channel:<id>`

Threads:

*   Slack/Discord threads append `:thread:<threadId>` to the base key.
*   Telegram forum topics embed `:topic:<topicId>` in the group key.

Examples:

*   `agent:main:telegram:group:-1001234567890:topic:42`
*   `agent:main:discord:channel:123456:thread:987654`

## Main DM route pinning

When `session.dmScope` is `main`, direct messages may share one main session. To prevent the session’s `lastRoute` from being overwritten by non-owner DMs, OpenClaw infers a pinned owner from `allowFrom` when all of these are true:

*   `allowFrom` has exactly one non-wildcard entry.
*   The entry can be normalized to a concrete sender ID for that channel.
*   The inbound DM sender does not match that pinned owner.

In that mismatch case, OpenClaw still records inbound session metadata, but it skips updating the main session `lastRoute`.

## Routing rules (how an agent is chosen)

Routing picks **one agent** for each inbound message:

1.  **Exact peer match** (`bindings` with `peer.kind` + `peer.id`).
2.  **Parent peer match** (thread inheritance).
3.  **Guild + roles match** (Discord) via `guildId` + `roles`.
4.  **Guild match** (Discord) via `guildId`.
5.  **Team match** (Slack) via `teamId`.
6.  **Account match** (`accountId` on the channel).
7.  **Channel match** (any account on that channel, `accountId: "*"`).
8.  **Default agent** (`agents.list[].default`, else first list entry, fallback to `main`).

When a binding includes multiple match fields (`peer`, `guildId`, `teamId`, `roles`), **all provided fields must match** for that binding to apply. The matched agent determines which workspace and session store are used.

## Broadcast groups (run multiple agents)

Broadcast groups let you run **multiple agents** for the same peer **when OpenClaw would normally reply** (for example: in WhatsApp groups, after mention/activation gating). Config:

```
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```

See: [Broadcast Groups](https://docs.openclaw.ai/channels/broadcast-groups).

## Config overview

*   `agents.list`: named agent definitions (workspace, model, etc.).
*   `bindings`: map inbound channels/accounts/peers to agents.

Example:

```
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

## Session storage

Session stores live under the state directory (default `~/.openclaw`):

*   `~/.openclaw/agents/<agentId>/sessions/sessions.json`
*   JSONL transcripts live alongside the store

You can override the store path via `session.store` and `{agentId}` templating.

## WebChat behavior

WebChat attaches to the **selected agent** and defaults to the agent’s main session. Because of this, WebChat lets you see cross‑channel context for that agent in one place.

## Reply context

Inbound replies include:

*   `ReplyToId`, `ReplyToBody`, and `ReplyToSender` when available.
*   Quoted context is appended to `Body` as a `[Replying to ...]` block.

This is consistent across channels.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/groups -->

# Groups - OpenClaw

OpenClaw treats group chats consistently across surfaces: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Zalo.

## Beginner intro (2 minutes)

OpenClaw “lives” on your own messaging accounts. There is no separate WhatsApp bot user. If **you** are in a group, OpenClaw can see that group and respond there. Default behavior:

*   Groups are restricted (`groupPolicy: "allowlist"`).
*   Replies require a mention unless you explicitly disable mention gating.

Translation: allowlisted senders can trigger OpenClaw by mentioning it.

> TL;DR
> 
> *   **DM access** is controlled by `*.allowFrom`.
> *   **Group access** is controlled by `*.groupPolicy` + allowlists (`*.groups`, `*.groupAllowFrom`).
> *   **Reply triggering** is controlled by mention gating (`requireMention`, `/activation`).

Quick flow (what happens to a group message):

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
otherwise -> reply
```

![Group message flow](https://mintcdn.com/clawdhub/A8OxQpxR3DcyCCHY/images/groups-flow.svg?fit=max&auto=format&n=A8OxQpxR3DcyCCHY&q=85&s=9cb1d2837115f2d744dc27374ce33e2b) If you want…

| Goal | What to set |
| --- | --- |
| Allow all groups but only reply on @mentions | `groups: { "*": { requireMention: true } }` |
| Disable all group replies | `groupPolicy: "disabled"` |
| Only specific groups | `groups: { "<group-id>": { ... } }` (no `"*"` key) |
| Only you can trigger in groups | `groupPolicy: "allowlist"`, `groupAllowFrom: ["+1555..."]` |

## Session keys

*   Group sessions use `agent:<agentId>:<channel>:group:<id>` session keys (rooms/channels use `agent:<agentId>:<channel>:channel:<id>`).
*   Telegram forum topics add `:topic:<threadId>` to the group id so each topic has its own session.
*   Direct chats use the main session (or per-sender if configured).
*   Heartbeats are skipped for group sessions.

## Pattern: personal DMs + public groups (single agent)

Yes — this works well if your “personal” traffic is **DMs** and your “public” traffic is **groups**. Why: in single-agent mode, DMs typically land in the **main** session key (`agent:main:main`), while groups always use **non-main** session keys (`agent:main:<channel>:group:<id>`). If you enable sandboxing with `mode: "non-main"`, those group sessions run in Docker while your main DM session stays on-host. This gives you one agent “brain” (shared workspace + memory), but two execution postures:

*   **DMs**: full tools (host)
*   **Groups**: sandbox + restricted tools (Docker)

> If you need truly separate workspaces/personas (“personal” and “public” must never mix), use a second agent + bindings. See [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent).

Example (DMs on host, groups sandboxed + messaging-only tools):

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // groups/channels are non-main -> sandboxed
        scope: "session", // strongest isolation (one container per group/channel)
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // If allow is non-empty, everything else is blocked (deny still wins).
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

Want “groups can only see folder X” instead of “no host access”? Keep `workspaceAccess: "none"` and mount only allowlisted paths into the sandbox:

```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          binds: [
            // hostPath:containerPath:mode
            "/home/user/FriendsShared:/data:ro",
          ],
        },
      },
    },
  },
}
```

Related:

*   Configuration keys and defaults: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration#agentsdefaultssandbox)
*   Debugging why a tool is blocked: [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated)
*   Bind mounts details: [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing#custom-bind-mounts)

## Display labels

*   UI labels use `displayName` when available, formatted as `<channel>:<token>`.
*   `#room` is reserved for rooms/channels; group chats use `g-<slug>` (lowercase, spaces -> `-`, keep `#@+._-`).

## Group policy

Control how group/room messages are handled per channel:

```
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789"], // numeric Telegram user id (wizard can resolve @username)
    },
    signal: {
      groupPolicy: "disabled",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "disabled",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "disabled",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: { channels: { help: { allow: true } } },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
    matrix: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["@owner:example.org"],
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
    },
  },
}
```

| Policy | Behavior |
| --- | --- |
| `"open"` | Groups bypass allowlists; mention-gating still applies. |
| `"disabled"` | Block all group messages entirely. |
| `"allowlist"` | Only allow groups/rooms that match the configured allowlist. |

Notes:

*   `groupPolicy` is separate from mention-gating (which requires @mentions).
*   WhatsApp/Telegram/Signal/iMessage/Microsoft Teams/Zalo: use `groupAllowFrom` (fallback: explicit `allowFrom`).
*   DM pairing approvals (`*-allowFrom` store entries) apply to DM access only; group sender authorization stays explicit to group allowlists.
*   Discord: allowlist uses `channels.discord.guilds.<id>.channels`.
*   Slack: allowlist uses `channels.slack.channels`.
*   Matrix: allowlist uses `channels.matrix.groups` (room IDs, aliases, or names). Use `channels.matrix.groupAllowFrom` to restrict senders; per-room `users` allowlists are also supported.
*   Group DMs are controlled separately (`channels.discord.dm.*`, `channels.slack.dm.*`).
*   Telegram allowlist can match user IDs (`"123456789"`, `"telegram:123456789"`, `"tg:123456789"`) or usernames (`"@alice"` or `"alice"`); prefixes are case-insensitive.
*   Default is `groupPolicy: "allowlist"`; if your group allowlist is empty, group messages are blocked.
*   Runtime safety: when a provider block is completely missing (`channels.<provider>` absent), group policy falls back to a fail-closed mode (typically `allowlist`) instead of inheriting `channels.defaults.groupPolicy`.

Quick mental model (evaluation order for group messages):

1.  `groupPolicy` (open/disabled/allowlist)
2.  group allowlists (`*.groups`, `*.groupAllowFrom`, channel-specific allowlist)
3.  mention gating (`requireMention`, `/activation`)

## Mention gating (default)

Group messages require a mention unless overridden per group. Defaults live per subsystem under `*.groups."*"`. Replying to a bot message counts as an implicit mention (when the channel supports reply metadata). This applies to Telegram, WhatsApp, Slack, Discord, and Microsoft Teams.

```
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
    telegram: {
      groups: {
        "*": { requireMention: true },
        "123456789": { requireMention: false },
      },
    },
    imessage: {
      groups: {
        "*": { requireMention: true },
        "123": { requireMention: false },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
          historyLimit: 50,
        },
      },
    ],
  },
}
```

Notes:

*   `mentionPatterns` are case-insensitive regexes.
*   Surfaces that provide explicit mentions still pass; patterns are a fallback.
*   Per-agent override: `agents.list[].groupChat.mentionPatterns` (useful when multiple agents share a group).
*   Mention gating is only enforced when mention detection is possible (native mentions or `mentionPatterns` are configured).
*   Discord defaults live in `channels.discord.guilds."*"` (overridable per guild/channel).
*   Group history context is wrapped uniformly across channels and is **pending-only** (messages skipped due to mention gating); use `messages.groupChat.historyLimit` for the global default and `channels.<channel>.historyLimit` (or `channels.<channel>.accounts.*.historyLimit`) for overrides. Set `0` to disable.

Some channel configs support restricting which tools are available **inside a specific group/room/channel**.

*   `tools`: allow/deny tools for the whole group.
*   `toolsBySender`: per-sender overrides within the group. Use explicit key prefixes: `id:<senderId>`, `e164:<phone>`, `username:<handle>`, `name:<displayName>`, and `"*"` wildcard. Legacy unprefixed keys are still accepted and matched as `id:` only.

Resolution order (most specific wins):

1.  group/channel `toolsBySender` match
2.  group/channel `tools`
3.  default (`"*"`) `toolsBySender` match
4.  default (`"*"`) `tools`

Example (Telegram):

```
{
  channels: {
    telegram: {
      groups: {
        "*": { tools: { deny: ["exec"] } },
        "-1001234567890": {
          tools: { deny: ["exec", "read", "write"] },
          toolsBySender: {
            "id:123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

Notes:

*   Group/channel tool restrictions are applied in addition to global/agent tool policy (deny still wins).
*   Some channels use different nesting for rooms/channels (e.g., Discord `guilds.*.channels.*`, Slack `channels.*`, MS Teams `teams.*.channels.*`).

## Group allowlists

When `channels.whatsapp.groups`, `channels.telegram.groups`, or `channels.imessage.groups` is configured, the keys act as a group allowlist. Use `"*"` to allow all groups while still setting default mention behavior. Common intents (copy/paste):

1.  Disable all group replies

```
{
  channels: { whatsapp: { groupPolicy: "disabled" } },
}
```

2.  Allow only specific groups (WhatsApp)

```
{
  channels: {
    whatsapp: {
      groups: {
        "123@g.us": { requireMention: true },
        "456@g.us": { requireMention: false },
      },
    },
  },
}
```

3.  Allow all groups but require mention (explicit)

```
{
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
  },
}
```

4.  Only the owner can trigger in groups (WhatsApp)

```
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Activation (owner-only)

Group owners can toggle per-group activation:

*   `/activation mention`
*   `/activation always`

Owner is determined by `channels.whatsapp.allowFrom` (or the bot’s self E.164 when unset). Send the command as a standalone message. Other surfaces currently ignore `/activation`.

## Context fields

Group inbound payloads set:

*   `ChatType=group`
*   `GroupSubject` (if known)
*   `GroupMembers` (if known)
*   `WasMentioned` (mention gating result)
*   Telegram forum topics also include `MessageThreadId` and `IsForum`.

The agent system prompt includes a group intro on the first turn of a new group session. It reminds the model to respond like a human, avoid Markdown tables, and avoid typing literal `\n` sequences.

## iMessage specifics

*   Prefer `chat_id:<id>` when routing or allowlisting.
*   List chats: `imsg chats --limit 20`.
*   Group replies always go back to the same `chat_id`.

## WhatsApp specifics

See [Group messages](https://docs.openclaw.ai/channels/group-messages) for WhatsApp-only behavior (history injection, mention handling details).

---

<!-- SOURCE: https://docs.openclaw.ai/channels/location -->

# Channel Location Parsing - OpenClaw

OpenClaw normalizes shared locations from chat channels into:

*   human-readable text appended to the inbound body, and
*   structured fields in the auto-reply context payload.

Currently supported:

*   **Telegram** (location pins + venues + live locations)
*   **WhatsApp** (locationMessage + liveLocationMessage)
*   **Matrix** (`m.location` with `geo_uri`)

## Text formatting

Locations are rendered as friendly lines without brackets:

*   Pin:
    *   `📍 48.858844, 2.294351 ±12m`
*   Named place:
    *   `📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`
*   Live share:
    *   `🛰 Live location: 48.858844, 2.294351 ±12m`

If the channel includes a caption/comment, it is appended on the next line:

```
📍 48.858844, 2.294351 ±12m
Meet here
```

## Context fields

When a location is present, these fields are added to `ctx`:

*   `LocationLat` (number)
*   `LocationLon` (number)
*   `LocationAccuracy` (number, meters; optional)
*   `LocationName` (string; optional)
*   `LocationAddress` (string; optional)
*   `LocationSource` (`pin | place | live`)
*   `LocationIsLive` (boolean)

## Channel notes

*   **Telegram**: venues map to `LocationName/LocationAddress`; live locations use `live_period`.
*   **WhatsApp**: `locationMessage.comment` and `liveLocationMessage.caption` are appended as the caption line.
*   **Matrix**: `geo_uri` is parsed as a pin location; altitude is ignored and `LocationIsLive` is always false.

---

<!-- SOURCE: https://docs.openclaw.ai/channels/broadcast-groups -->

# Broadcast Groups - OpenClaw

**Status:** Experimental  
**Version:** Added in 2026.1.9

## Overview

Broadcast Groups enable multiple agents to process and respond to the same message simultaneously. This allows you to create specialized agent teams that work together in a single WhatsApp group or DM — all using one phone number. Current scope: **WhatsApp only** (web channel). Broadcast groups are evaluated after channel allowlists and group activation rules. In WhatsApp groups, this means broadcasts happen when OpenClaw would normally reply (for example: on mention, depending on your group settings).

## Use Cases

### 1\. Specialized Agent Teams

Deploy multiple agents with atomic, focused responsibilities:

```
Group: "Development Team"
Agents:
  - CodeReviewer (reviews code snippets)
  - DocumentationBot (generates docs)
  - SecurityAuditor (checks for vulnerabilities)
  - TestGenerator (suggests test cases)
```

Each agent processes the same message and provides its specialized perspective.

### 2\. Multi-Language Support

```
Group: "International Support"
Agents:
  - Agent_EN (responds in English)
  - Agent_DE (responds in German)
  - Agent_ES (responds in Spanish)
```

### 3\. Quality Assurance Workflows

```
Group: "Customer Support"
Agents:
  - SupportAgent (provides answer)
  - QAAgent (reviews quality, only responds if issues found)
```

### 4\. Task Automation

```
Group: "Project Management"
Agents:
  - TaskTracker (updates task database)
  - TimeLogger (logs time spent)
  - ReportGenerator (creates summaries)
```

## Configuration

### Basic Setup

Add a top-level `broadcast` section (next to `bindings`). Keys are WhatsApp peer ids:

*   group chats: group JID (e.g. `120363403215116621@g.us`)
*   DMs: E.164 phone number (e.g. `+15551234567`)

```
{
  "broadcast": {
    "120363403215116621@g.us": ["alfred", "baerbel", "assistant3"]
  }
}
```

**Result:** When OpenClaw would reply in this chat, it will run all three agents.

### Processing Strategy

Control how agents process messages:

#### Parallel (Default)

All agents process simultaneously:

```
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

#### Sequential

Agents process in order (one waits for previous to finish):

```
{
  "broadcast": {
    "strategy": "sequential",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

### Complete Example

```
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

## How It Works

### Message Flow

1.  **Incoming message** arrives in a WhatsApp group
2.  **Broadcast check**: System checks if peer ID is in `broadcast`
3.  **If in broadcast list**:
    *   All listed agents process the message
    *   Each agent has its own session key and isolated context
    *   Agents process in parallel (default) or sequentially
4.  **If not in broadcast list**:
    *   Normal routing applies (first matching binding)

Note: broadcast groups do not bypass channel allowlists or group activation rules (mentions/commands/etc). They only change _which agents run_ when a message is eligible for processing.

### Session Isolation

Each agent in a broadcast group maintains completely separate:

*   **Session keys** (`agent:alfred:whatsapp:group:120363...` vs `agent:baerbel:whatsapp:group:120363...`)
*   **Conversation history** (agent doesn’t see other agents’ messages)
*   **Workspace** (separate sandboxes if configured)
*   **Tool access** (different allow/deny lists)
*   **Memory/context** (separate IDENTITY.md, SOUL.md, etc.)
*   **Group context buffer** (recent group messages used for context) is shared per peer, so all broadcast agents see the same context when triggered

This allows each agent to have:

*   Different personalities
*   Different tool access (e.g., read-only vs. read-write)
*   Different models (e.g., opus vs. sonnet)
*   Different skills installed

### Example: Isolated Sessions

In group `120363403215116621@g.us` with agents `["alfred", "baerbel"]`: **Alfred’s context:**

```
Session: agent:alfred:whatsapp:group:120363403215116621@g.us
History: [user message, alfred's previous responses]
Workspace: /Users/pascal/openclaw-alfred/
Tools: read, write, exec
```

**Bärbel’s context:**

```
Session: agent:baerbel:whatsapp:group:120363403215116621@g.us
History: [user message, baerbel's previous responses]
Workspace: /Users/pascal/openclaw-baerbel/
Tools: read only
```

## Best Practices

### 1\. Keep Agents Focused

Design each agent with a single, clear responsibility:

```
{
  "broadcast": {
    "DEV_GROUP": ["formatter", "linter", "tester"]
  }
}
```

✅ **Good:** Each agent has one job  
❌ **Bad:** One generic “dev-helper” agent

### 2\. Use Descriptive Names

Make it clear what each agent does:

```
{
  "agents": {
    "security-scanner": { "name": "Security Scanner" },
    "code-formatter": { "name": "Code Formatter" },
    "test-generator": { "name": "Test Generator" }
  }
}
```

### 3\. Configure Different Tool Access

Give agents only the tools they need:

```
{
  "agents": {
    "reviewer": {
      "tools": { "allow": ["read", "exec"] } // Read-only
    },
    "fixer": {
      "tools": { "allow": ["read", "write", "edit", "exec"] } // Read-write
    }
  }
}
```

### 4\. Monitor Performance

With many agents, consider:

*   Using `"strategy": "parallel"` (default) for speed
*   Limiting broadcast groups to 5-10 agents
*   Using faster models for simpler agents

### 5\. Handle Failures Gracefully

Agents fail independently. One agent’s error doesn’t block others:

```
Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]
Result: Agent A and C respond, Agent B logs error
```

## Compatibility

### Providers

Broadcast groups currently work with:

*   ✅ WhatsApp (implemented)
*   🚧 Telegram (planned)
*   🚧 Discord (planned)
*   🚧 Slack (planned)

### Routing

Broadcast groups work alongside existing routing:

```
{
  "bindings": [
    {
      "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "GROUP_A" } },
      "agentId": "alfred"
    }
  ],
  "broadcast": {
    "GROUP_B": ["agent1", "agent2"]
  }
}
```

*   `GROUP_A`: Only alfred responds (normal routing)
*   `GROUP_B`: agent1 AND agent2 respond (broadcast)

**Precedence:** `broadcast` takes priority over `bindings`.

## Troubleshooting

### Agents Not Responding

**Check:**

1.  Agent IDs exist in `agents.list`
2.  Peer ID format is correct (e.g., `120363403215116621@g.us`)
3.  Agents are not in deny lists

**Debug:**

```
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

### Only One Agent Responding

**Cause:** Peer ID might be in `bindings` but not `broadcast`. **Fix:** Add to broadcast config or remove from bindings.

### Performance Issues

**If slow with many agents:**

*   Reduce number of agents per group
*   Use lighter models (sonnet instead of opus)
*   Check sandbox startup time

## Examples

### Example 1: Code Review Team

```
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": [
      "code-formatter",
      "security-scanner",
      "test-coverage",
      "docs-checker"
    ]
  },
  "agents": {
    "list": [
      {
        "id": "code-formatter",
        "workspace": "~/agents/formatter",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "security-scanner",
        "workspace": "~/agents/security",
        "tools": { "allow": ["read", "exec"] }
      },
      {
        "id": "test-coverage",
        "workspace": "~/agents/testing",
        "tools": { "allow": ["read", "exec"] }
      },
      { "id": "docs-checker", "workspace": "~/agents/docs", "tools": { "allow": ["read"] } }
    ]
  }
}
```

**User sends:** Code snippet  
**Responses:**

*   code-formatter: “Fixed indentation and added type hints”
*   security-scanner: “⚠️ SQL injection vulnerability in line 12”
*   test-coverage: “Coverage is 45%, missing tests for error cases”
*   docs-checker: “Missing docstring for function `process_data`”

### Example 2: Multi-Language Support

```
{
  "broadcast": {
    "strategy": "sequential",
    "+15555550123": ["detect-language", "translator-en", "translator-de"]
  },
  "agents": {
    "list": [
      { "id": "detect-language", "workspace": "~/agents/lang-detect" },
      { "id": "translator-en", "workspace": "~/agents/translate-en" },
      { "id": "translator-de", "workspace": "~/agents/translate-de" }
    ]
  }
}
```

## API Reference

### Config Schema

```
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

### Fields

*   `strategy` (optional): How to process agents
    *   `"parallel"` (default): All agents process simultaneously
    *   `"sequential"`: Agents process in array order
*   `[peerId]`: WhatsApp group JID, E.164 number, or other peer ID
    *   Value: Array of agent IDs that should process messages

## Limitations

1.  **Max agents:** No hard limit, but 10+ agents may be slow
2.  **Shared context:** Agents don’t see each other’s responses (by design)
3.  **Message ordering:** Parallel responses may arrive in any order
4.  **Rate limits:** All agents count toward WhatsApp rate limits

## Future Enhancements

Planned features:

*   Shared context mode (agents see each other’s responses)
*   Agent coordination (agents can signal each other)
*   Dynamic agent selection (choose agents based on message content)
*   Agent priorities (some agents respond before others)

## See Also

*   [Multi-Agent Configuration](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools)
*   [Routing Configuration](https://docs.openclaw.ai/channels/channel-routing)
*   [Session Management](https://docs.openclaw.ai/concepts/session)

---

<!-- SOURCE: https://docs.openclaw.ai/channels/troubleshooting -->

# Channel Troubleshooting - OpenClaw

Use this page when a channel connects but behavior is wrong.

## Command ladder

Run these in order first:

```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Healthy baseline:

*   `Runtime: running`
*   `RPC probe: ok`
*   Channel probe shows connected/ready

## WhatsApp

### WhatsApp failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| Connected but no DM replies | `openclaw pairing list whatsapp` | Approve sender or switch DM policy/allowlist. |
| Group messages ignored | Check `requireMention` + mention patterns in config | Mention the bot or relax mention policy for that group. |
| Random disconnect/relogin loops | `openclaw channels status --probe` + logs | Re-login and verify credentials directory is healthy. |

Full troubleshooting: [/channels/whatsapp#troubleshooting-quick](https://docs.openclaw.ai/channels/whatsapp#troubleshooting-quick)

## Telegram

### Telegram failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| `/start` but no usable reply flow | `openclaw pairing list telegram` | Approve pairing or change DM policy. |
| Bot online but group stays silent | Verify mention requirement and bot privacy mode | Disable privacy mode for group visibility or mention bot. |
| Send failures with network errors | Inspect logs for Telegram API call failures | Fix DNS/IPv6/proxy routing to `api.telegram.org`. |
| Upgraded and allowlist blocks you | `openclaw security audit` and config allowlists | Run `openclaw doctor --fix` or replace `@username` with numeric sender IDs. |

Full troubleshooting: [/channels/telegram#troubleshooting](https://docs.openclaw.ai/channels/telegram#troubleshooting)

## Discord

### Discord failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| Bot online but no guild replies | `openclaw channels status --probe` | Allow guild/channel and verify message content intent. |
| Group messages ignored | Check logs for mention gating drops | Mention bot or set guild/channel `requireMention: false`. |
| DM replies missing | `openclaw pairing list discord` | Approve DM pairing or adjust DM policy. |

Full troubleshooting: [/channels/discord#troubleshooting](https://docs.openclaw.ai/channels/discord#troubleshooting)

## Slack

### Slack failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| Socket mode connected but no responses | `openclaw channels status --probe` | Verify app token + bot token and required scopes. |
| DMs blocked | `openclaw pairing list slack` | Approve pairing or relax DM policy. |
| Channel message ignored | Check `groupPolicy` and channel allowlist | Allow the channel or switch policy to `open`. |

Full troubleshooting: [/channels/slack#troubleshooting](https://docs.openclaw.ai/channels/slack#troubleshooting)

## iMessage and BlueBubbles

### iMessage and BlueBubbles failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| No inbound events | Verify webhook/server reachability and app permissions | Fix webhook URL or BlueBubbles server state. |
| Can send but no receive on macOS | Check macOS privacy permissions for Messages automation | Re-grant TCC permissions and restart channel process. |
| DM sender blocked | `openclaw pairing list imessage` or `openclaw pairing list bluebubbles` | Approve pairing or update allowlist. |

Full troubleshooting:

*   [/channels/imessage#troubleshooting-macos-privacy-and-security-tcc](https://docs.openclaw.ai/channels/imessage#troubleshooting-macos-privacy-and-security-tcc)
*   [/channels/bluebubbles#troubleshooting](https://docs.openclaw.ai/channels/bluebubbles#troubleshooting)

## Signal

### Signal failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| Daemon reachable but bot silent | `openclaw channels status --probe` | Verify `signal-cli` daemon URL/account and receive mode. |
| DM blocked | `openclaw pairing list signal` | Approve sender or adjust DM policy. |
| Group replies do not trigger | Check group allowlist and mention patterns | Add sender/group or loosen gating. |

Full troubleshooting: [/channels/signal#troubleshooting](https://docs.openclaw.ai/channels/signal#troubleshooting)

## Matrix

### Matrix failure signatures

| Symptom | Fastest check | Fix |
| --- | --- | --- |
| Logged in but ignores room messages | `openclaw channels status --probe` | Check `groupPolicy` and room allowlist. |
| DMs do not process | `openclaw pairing list matrix` | Approve sender or adjust DM policy. |
| Encrypted rooms fail | Verify crypto module and encryption settings | Enable encryption support and rejoin/sync room. |

Full troubleshooting: [/channels/matrix#troubleshooting](https://docs.openclaw.ai/channels/matrix#troubleshooting)

