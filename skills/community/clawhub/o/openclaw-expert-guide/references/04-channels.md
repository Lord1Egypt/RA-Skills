# OpenClaw Channels — Complete Reference

> Generated from official docs at https://docs.openclaw.ai/channels (all 33 pages)

---

## Table of Contents

1. [Channels Overview](#channels-overview)
2. [Channel Routing](#channel-routing)
3. [Groups](#groups)
4. [Group Messages (WhatsApp specifics)](#group-messages-whatsapp-specifics)
5. [Pairing](#pairing)
6. [Broadcast Groups](#broadcast-groups)
7. [Location Parsing](#location-parsing)
8. [QA Channel (Internal Testing)](#qa-channel-internal-testing)
9. [BlueBubbles (iMessage - Recommended)](#bluebubbles-imessage---recommended)
10. [Discord](#discord)
11. [Feishu / Lark](#feishu--lark)
12. [Google Chat](#google-chat)
13. [iMessage (Legacy)](#imessage-legacy)
14. [IRC](#irc)
15. [LINE](#line)
16. [Matrix](#matrix)
17. [Matrix Push Rules](#matrix-push-rules)
18. [Mattermost](#mattermost)
19. [Microsoft Teams](#microsoft-teams)
20. [Nextcloud Talk](#nextcloud-talk)
21. [Nostr](#nostr)
22. [QQ Bot](#qq-bot)
23. [Signal](#signal)
24. [Slack](#slack)
25. [Synology Chat](#synology-chat)
26. [Telegram](#telegram)
27. [Tlon (Urbit)](#tlon-urbit)
28. [Twitch](#twitch)
29. [WeChat](#wechat)
30. [WhatsApp](#whatsapp)
31. [Zalo (Bot API)](#zalo-bot-api)
32. [Zalo Personal](#zalo-personal)
33. [Troubleshooting](#troubleshooting)
34. [Feature Comparison Table](#feature-comparison-table)

---

## Channels Overview

OpenClaw connects to any chat app you already use via the **Gateway**. Text is supported everywhere; media and reactions vary by channel. Multiple channels can run simultaneously.

### Key delivery notes
- Telegram replies with markdown image syntax `![alt](url)` are converted to media replies on the outbound path.
- Slack multi-person DMs route as group chats (group policy applies).
- WhatsApp setup is install-on-demand; the Gateway loads the runtime only when the channel is active.

### Quickest setup
- **Telegram** — just a bot token, no QR required.
- **WhatsApp** — requires QR pairing and stores state on disk.

---

## Channel Routing

OpenClaw routes replies **back to the channel where the message came from**. Routing is deterministic and model-independent.

### Key terms
| Term | Meaning |
|------|---------|
| **Channel** | `telegram`, `whatsapp`, `discord`, `slack`, `signal`, `irc`, `googlechat`, `imessage`, `line`, plus plugin channels |
| **AccountId** | Per-channel account instance when multiple accounts are supported |
| **AgentId** | An isolated workspace + session store ("brain") |
| **SessionKey** | Bucket key for context storage and concurrency control |

### Session key shapes
```
agent:<agentId>:<mainKey>              # DMs → main session (default)
agent:<agentId>:<channel>:group:<id>   # Groups
agent:<agentId>:<channel>:channel:<id> # Rooms/channels
agent:<agentId>:discord:channel:123456:thread:987654  # Threads
agent:<agentId>:telegram:group:-100123:topic:42       # Telegram forum topics
```

### Routing rules (priority order)
1. Exact peer match (`bindings` with `peer.kind` + `peer.id`)
2. Parent peer match (thread inheritance)
3. Guild + roles match (Discord)
4. Guild match (Discord via `guildId`)
5. Team match (Slack via `teamId`)
6. Account match (`accountId`)
7. Channel match (any account on that channel)
8. Default agent (`agents.list[].default`, else first entry, fallback to `main`)

### Bindings config example
```json5
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

### Broadcast groups (run multiple agents per peer)
```json5
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```
`broadcast` takes priority over `bindings`.

---

## Groups

OpenClaw handles group chats consistently across: Discord, iMessage, Matrix, Microsoft Teams, Signal, Slack, Telegram, WhatsApp, Zalo.

### Default behavior
- Groups are restricted (`groupPolicy: "allowlist"`)
- Replies require a mention unless overridden
- Heartbeats are skipped for group sessions

### Group message evaluation flow
```
groupPolicy? disabled → drop
groupPolicy? allowlist → group allowed? no → drop
requireMention? yes → mentioned? no → store for context only
otherwise → reply
```

### Group policy values
| Policy | Behavior |
|--------|----------|
| `"open"` | Groups bypass allowlists; mention-gating still applies |
| `"disabled"` | Block all group messages entirely |
| `"allowlist"` | Only allow groups/rooms matching the configured allowlist |

### Mention gating
Replying to or quoting a bot message counts as an implicit mention on channels that expose reply metadata (Telegram, WhatsApp, Slack, Discord, MS Teams, ZaloUser).

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
  },
  agents: {
    list: [{
      id: "main",
      groupChat: {
        mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
        historyLimit: 50,
      },
    }],
  },
}
```

### Group/channel tool restrictions
```json5
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

`toolsBySender` key prefixes: `id:`, `e164:`, `username:`, `name:`, or `"*"` wildcard.

### Session keys
- Group sessions: `agent:<agentId>:<channel>:group:<id>`
- Telegram forum topics add `:topic:<threadId>`
- DMs use main session (or per-sender if configured)

### Per-group system prompts (where supported)
Under `channels.<channel>.groups.<id>.systemPrompt`.

### Context visibility and allowlists

Two separate controls for group safety:
- **Trigger authorization:** who can trigger the agent (`groupPolicy`, `groups`, `groupAllowFrom`)
- **Context visibility:** what supplemental context is injected (reply text, quotes, thread history, forwarded metadata)

By default, allowlists decide who can trigger actions, not a universal redaction boundary. Current behavior is channel-specific:
- Some channels already filter supplemental context by sender (Slack thread seeding, Matrix reply/thread lookups)
- Others pass quote/reply/forward context as received

**Hardening direction (planned):**
- `contextVisibility: "all"` (default) — as-received behavior
- `contextVisibility: "allowlist"` — filter supplemental context to allowlisted senders
- `contextVisibility: "allowlist_quote"` — allowlist + one explicit quote/reply exception

### Pattern: personal DMs + public groups (single agent)

In single-agent mode, DMs land in the **main** session key, groups use **non-main** keys. With `sandbox.mode: "non-main"`, groups run sandboxed while DMs stay on-host.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

To allow groups to see specific folders: keep `workspaceAccess: "none"` and mount allowlisted paths via `docker.binds: ["/host/path:/data:ro"]`.

For truly separate workspaces/personas, use a second agent + bindings (see Multi-Agent Routing).

---

## Group Messages (WhatsApp specifics)

### Activation modes
- `mention` (default): requires ping via `mentionedJids`, safe regex patterns, or bot's E.164 anywhere in text
- `always`: wakes on every message; agent returns `NO_REPLY` if nothing meaningful to say

### Config example
```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    list: [{
      id: "main",
      groupChat: {
        historyLimit: 50,
        mentionPatterns: ["@?openclaw", "\\+?15555550123"],
      },
    }],
  },
}
```

### Context injection
Pending (unprocessed) group messages (default 50) are prefixed as:
```
[Chat messages since your last reply - for context]
[Current message - respond to this]
```
Already-processed messages are not re-injected.

### Owner-only activation command
- `/activation mention`
- `/activation always`

Only the owner number (from `allowFrom` or self E.164) can change this.

---

## Pairing

Pairing is OpenClaw's explicit **owner approval** step used for:
1. DM pairing (who can talk to the bot)
2. Node pairing (which devices/nodes can join the gateway network)

### DM pairing
When `dmPolicy: "pairing"` is set, unknown senders receive an 8-character code (uppercase, no ambiguous chars), and their messages are **not processed** until approved.

- Codes expire after **1 hour**
- Max **3 pending requests per channel** by default

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Supported channels for pairing: `bluebubbles`, `discord`, `feishu`, `googlechat`, `imessage`, `irc`, `line`, `matrix`, `mattermost`, `msteams`, `nextcloud-talk`, `nostr`, `openclaw-weixin`, `signal`, `slack`, `synology-chat`, `telegram`, `twitch`, `whatsapp`, `zalo`, `zalouser`.

### Pairing state storage
```
~/.openclaw/credentials/<channel>-pairing.json          # Pending
~/.openclaw/credentials/<channel>-allowFrom.json        # Approved (default account)
~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json  # Named accounts
```

> **Important:** DM pairing approval does NOT grant group access. Group sender authorization is separate and requires explicit `groupAllowFrom` config.

### Node/device pairing (iOS/Android/macOS)
```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

Via Telegram: `/pair` → scan QR in app → `/pair pending` → `/pair approve <requestId>`

---

## Broadcast Groups

**Status:** Experimental (added 2026.1.9). Currently **WhatsApp only**.

Broadcast Groups enable multiple agents to process and respond to the same message simultaneously in a single WhatsApp group or DM.

### Key behaviors
- Evaluated after channel allowlists and group activation rules
- Each agent has isolated session key, conversation history, workspace, tool access, and memory
- Shared: group context buffer (recent group messages for context)
- Broadcast takes priority over bindings

### Configuration
```json5
{
  "broadcast": {
    "strategy": "parallel",     // or "sequential"
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

### Strategies
- `"parallel"` (default): all agents process simultaneously
- `"sequential"`: agents process in array order

### TypeScript schema
```typescript
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

### Limitations
1. No hard agent limit, but 10+ agents may be slow
2. Agents don't see each other's responses (by design)
3. Parallel responses may arrive in any order
4. All agents count toward WhatsApp rate limits

### Troubleshooting
```bash
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

---

## Location Parsing

OpenClaw normalizes shared locations from chat channels into terse coordinate text + structured context fields.

### Supported channels
- **Telegram** (location pins + venues + live locations)
- **WhatsApp** (locationMessage + liveLocationMessage)
- **Matrix** (m.location with geo_uri)

### Text rendering
```
📍 48.858844, 2.294351 ±12m          # Pin
🛰 Live location: 48.858844, 2.294351 ±12m  # Live share
```

Labels, addresses, and captions are rendered as fenced untrusted metadata JSON (not inline).

### Context fields added
| Field | Type |
|-------|------|
| `LocationLat` | number |
| `LocationLon` | number |
| `LocationAccuracy` | number (meters, optional) |
| `LocationName` | string (optional) |
| `LocationAddress` | string (optional) |
| `LocationSource` | `pin \| place \| live` |
| `LocationIsLive` | boolean |
| `LocationCaption` | string (optional) |

---

## QA Channel (Internal Testing)

`qa-channel` is a **bundled synthetic message transport for automated OpenClaw QA**. Not a production channel.

### Features
- Slack-class target grammar: `dm:<user>`, `channel:<room>`, `thread:<room>/<thread>`
- HTTP-backed synthetic bus for inbound injection, outbound capture, thread creation, reactions, edits, deletes, search
- Bundled host-side self-check runner (Markdown report output)

### Config
```json
{
  "channels": {
    "qa-channel": {
      "baseUrl": "http://127.0.0.1:43123",
      "botUserId": "openclaw",
      "botDisplayName": "OpenClaw QA",
      "allowFrom": ["*"],
      "pollTimeoutMs": 1000
    }
  }
}
```

### Runner commands
```bash
pnpm qa:e2e         # Run deterministic self-check + Markdown report
pnpm qa:lab:up      # Start QA Lab Docker stack + browser UI
pnpm openclaw qa suite  # Full QA suite
```

---

## BlueBubbles (iMessage - Recommended)

**Status:** Bundled plugin. Recommended for iMessage (over legacy `imsg`).

BlueBubbles runs on macOS via the BlueBubbles helper app and communicates via REST API.

### What it is
- Talks to BlueBubbles macOS server over HTTP
- Incoming messages via webhooks; outgoing via REST
- Supports: edit, unsend, reply threading, message effects, group management, tapbacks
- Tested on macOS Sequoia (15); edit broken on macOS Tahoe (26)

### Quick setup
```json5
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
Webhook URL: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`

Or via CLI:
```bash
openclaw onboard
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

### Access control
DMs:
- Default: `dmPolicy = "pairing"`
- `openclaw pairing list bluebubbles`
- `openclaw pairing approve bluebubbles <CODE>`

Groups:
- `channels.bluebubbles.groupPolicy = open | allowlist | disabled` (default: `allowlist`)
- `channels.bluebubbles.groupAllowFrom`

### Advanced actions config
```json5
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true,     // tapbacks (default: true)
        edit: true,          // edit sent messages (macOS 13+, broken on macOS 26 Tahoe)
        unsend: true,        // unsend messages (macOS 13+)
        reply: true,         // reply threading by message GUID
        sendWithEffect: true, // message effects (slam, loud, etc.)
        renameGroup: true,   // rename group chats
        setGroupIcon: true,  // set group icon (flaky on macOS 26 Tahoe)
        addParticipant: true,
        removeParticipant: true,
        leaveGroup: true,
        sendAttachment: true,
      },
    },
  },
}
```

### Available actions
| Action | Params | Notes |
|--------|--------|-------|
| `react` | `messageId`, `emoji`, `remove` | iMessage tapbacks: love/like/dislike/laugh/emphasize/question; unknown emoji fallbacks to `love` |
| `edit` | `messageId`, `text` | macOS 13+ only |
| `unsend` | `messageId` | macOS 13+ only |
| `reply` | `messageId`, `text`, `to` | Requires Private API |
| `sendWithEffect` | `text`, `to`, `effectId` | |
| `renameGroup` | `chatGuid`, `displayName` | |
| `setGroupIcon` | `chatGuid`, `media` | Flaky on Tahoe |
| `addParticipant` | `chatGuid`, `address` | |
| `removeParticipant` | `chatGuid`, `address` | |
| `leaveGroup` | `chatGuid` | |
| `upload-file` | `to`, `buffer`, `filename`, `asVoice` | Voice memos: `asVoice: true` with MP3 or CAF |

### Message IDs
- Short IDs (e.g., `1`, `2`) expire on restart/cache eviction
- Full IDs via `MessageSidFull` / `ReplyToIdFull` are durable

### Typing + read receipts
```json5
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false,  // disable read receipts
    },
  },
}
```

> **WhatsApp read receipts:** Read receipts are enabled by default for accepted inbound WhatsApp messages. Disable globally with `channels.whatsapp.sendReadReceipts: false`. Per-account override: `channels.whatsapp.accounts.<id>.sendReadReceipts: false`. Self-chat turns skip read receipts even when globally enabled.

### Coalescing split-send DMs
When user types command + URL, Apple splits into 2 webhooks ~1s apart:
```json5
{
  channels: {
    bluebubbles: {
      coalesceSameSenderDms: true,  // 2500ms debounce window
    },
  },
}
```

### Per-group config
```json5
{
  channels: {
    bluebubbles: {
      groups: {
        "*": { requireMention: true },
        "iMessage;-;chat123": {
          requireMention: false,
          systemPrompt: "Keep responses under 3 sentences.",
        },
      },
    },
  },
}
```

### Contact name enrichment
```json5
{
  channels: {
    bluebubbles: {
      enrichGroupParticipantsFromContacts: true,  // default: false
    },
  },
}
```

### ACP bindings
```json5
{
  bindings: [{
    type: "acp",
    agentId: "codex",
    match: {
      channel: "bluebubbles",
      accountId: "default",
      peer: { kind: "dm", id: "+15555550123" },
    },
    acp: { label: "codex-imessage" },
  }],
}
```

### Keeping Messages.app alive (headless)
Create `~/Scripts/poke-messages.scpt` + `~/Library/LaunchAgents/com.user.poke-messages.plist` to touch Messages every 300 seconds.

### Limitations/gotchas
- Edit broken on macOS 26 Tahoe
- Group icon updates may not sync on macOS 26 Tahoe
- Webhook auth always required; password checked before parsing body
- Tapbacks outside iMessage native set fall back to `love`

---

## Discord

**Status:** Ready for DMs and guild channels via the official Discord gateway.

### Quick setup
1. Create application + bot at https://discord.com/developers/applications
2. Enable: Message Content Intent, Server Members Intent (recommended)
3. Reset/copy bot token
4. Invite bot with OAuth2 scopes: `bot`, `applications.commands`
5. Set bot token securely:

```bash
export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
openclaw config set channels.discord.token --ref-provider default --ref-source env --ref-id DISCORD_BOT_TOKEN
openclaw config set channels.discord.enabled true --strict-json
openclaw gateway
```

### Config
```json5
{
  channels: {
    discord: {
      enabled: true,
      token: {
        source: "env",
        provider: "default",
        id: "DISCORD_BOT_TOKEN",
      },
    },
  },
}
```

Env fallback: `DISCORD_BOT_TOKEN=...` (default account only)

### Access control

DM policy (`channels.discord.dmPolicy`):
- `pairing` (default)
- `allowlist`
- `open` (requires `allowFrom: ["*"]`)
- `disabled`

Guild policy (`channels.discord.groupPolicy`):
- `open`, `allowlist` (default secure baseline), `disabled`

Guild config:
```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "123456789012345678": {
          requireMention: true,
          ignoreOtherMentions: true,  // drops messages that mention another user/role but not the bot (excluding @everyone/@here)
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

### Role-based agent routing
```json5
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
      match: { channel: "discord", guildId: "123456789012345678" },
    },
  ],
}
```

### Interactive components (Discord Components v2)
Supported blocks: `text`, `section`, `separator`, `actions`, `media-gallery`, `file`
- Action rows: up to 5 buttons or 1 select menu
- Select types: `string`, `user`, `role`, `mentionable`, `channel`
- Modal forms: up to 5 fields (`text`, `checkbox`, `radio`, `select`, `role-select`, `user-select`)
- Set `components.reusable: true` for multi-use buttons
- `allowedUsers` on buttons restricts who can click (ephemeral denial for others)
- Button `style` values: `success`, `danger`, and `primary` (the `message` tool also supports `default`)

```json5
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
          { label: "Approve", style: "success", allowedUsers: ["123456789012345678"] },
          { label: "Decline", style: "danger" },
        ],
      },
    ],
  },
}
```

### Forum channels
- Send to forum parent to auto-create a thread (title = first non-empty line)
- Or use `openclaw message thread create --channel discord --target channel:<forumId> --thread-name "Title" --message "Body"`
- Forum parents do NOT accept Discord components

### Native slash commands
- `commands.native` defaults to `"auto"` (enabled for Discord)
- `/model` and `/models` open interactive model picker (ephemeral, invoking user only)
- `commands.native=false` clears previously registered native commands

### Reply tags
- `[[reply_to_current]]`
- `[[reply_to:<id>]]`
- Controlled by `channels.discord.replyToMode`

### Session model
- DMs share agent main session (default `session.dmScope=main`)
- Guild channels: `agent:<agentId>:discord:channel:<channelId>`
- Native slash commands: `agent:<agentId>:discord:slash:<userId>`
- Threads: append `:thread:<threadId>`
- Group DMs: ignored by default (`dm.groupEnabled=false`); use `dm.groupChannels` to allowlist specific group DM channel IDs or slugs

### Gotchas
- If `DISCORD_BOT_TOKEN` set without `channels.discord` block, runtime fallback is `groupPolicy="allowlist"` (with log warning)
- `dangerouslyAllowNameMatching: true` needed for name/tag matching (IDs safer)
- Bare numeric IDs are ambiguous and rejected without explicit `user:`/`channel:` prefix

---

## Feishu / Lark

**Status:** Production-ready for bot DMs + group chats. Bundled plugin.

**Requires OpenClaw 2026.4.24+**

### Quick setup
```bash
openclaw channels login --channel feishu   # Scan QR code to auto-create bot
openclaw gateway restart
```

### Access control

DM policy (`channels.feishu.dmPolicy`): `pairing | allowlist | open | disabled`

Group policy:
```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",     // open | allowlist | disabled
      groupAllowFrom: ["oc_xxx", "oc_yyy"],
      requireMention: true,         // default: true
      groups: {
        oc_xxx: {
          allowFrom: ["ou_user1", "ou_user2"],
          requireMention: false,     // per-group override
        },
      },
    },
  },
}
```

### ID formats
- Group IDs: `oc_xxx` (found in group Settings)
- User IDs: `ou_xxx` (open_ids, visible in logs or pairing list)

### Streaming
```json5
{
  channels: {
    feishu: {
      streaming: true,       // enable streaming card output (default: true)
      blockStreaming: true,  // block-level streaming (default: true)
    },
  },
}
```

### Quota optimization
```json5
{
  channels: {
    feishu: {
      typingIndicator: false,       // skip typing reaction calls
      resolveSenderNames: false,    // skip sender profile lookups
    },
  },
}
```

### Multi-account
```json5
{
  channels: {
    feishu: {
      defaultAccount: "main",
      accounts: {
        main: { appId: "cli_xxx", appSecret: "xxx", name: "Primary bot" },
        backup: { appId: "cli_yyy", appSecret: "yyy", enabled: false },
      },
    },
  },
}
```

### ACP bindings
```json5
{
  bindings: [{
    type: "acp",
    agentId: "codex",
    match: {
      channel: "feishu",
      accountId: "default",
      peer: { kind: "direct", id: "ou_1234567890" },
    },
  }],
}
```
In-chat ACP: `/acp spawn codex --thread here`

### Full config reference
| Setting | Description | Default |
|---------|-------------|---------|
| `channels.feishu.enabled` | Enable/disable | `true` |
| `channels.feishu.domain` | `feishu` or `lark` | `feishu` |
| `channels.feishu.connectionMode` | `websocket` or `webhook` | `websocket` |
| `channels.feishu.defaultAccount` | Default outbound account | `default` |
| `channels.feishu.verificationToken` | Required for webhook mode | — |
| `channels.feishu.encryptKey` | Required for webhook mode | — |
| `channels.feishu.webhookPath` | Webhook route | `/feishu/events` |
| `channels.feishu.dmPolicy` | DM policy | `allowlist` |
| `channels.feishu.groupPolicy` | Group policy | `allowlist` |
| `channels.feishu.requireMention` | Require @mention in groups | `true` |
| `channels.feishu.textChunkLimit` | Message chunk size | `2000` |
| `channels.feishu.mediaMaxMb` | Media size limit | `30` |
| `channels.feishu.streaming` | Streaming card output | `true` |
| `channels.feishu.typingIndicator` | Send typing reactions | `true` |
| `channels.feishu.resolveSenderNames` | Resolve sender names | `true` |

### Supported message types
Receive: ✅ Text, Rich text, Images, Files, Audio, Video, Stickers
Send: ✅ Text, Images, Files, Audio, Video, Interactive cards (streaming updates)
Threads: ✅ Inline replies, Thread replies

### Troubleshooting
- Bot not in group → add bot to group
- No @mention → mention required by default
- Not receiving → verify published in Feishu Open Platform, `im.message.receive_v1` event, persistent connection (WebSocket)

---

## Google Chat

**Status:** Ready for DMs + spaces via HTTP webhook.

### Setup
1. Create Google Cloud project + enable Google Chat API
2. Create Service Account → download JSON key
3. Create Google Chat app in Cloud Console with HTTP endpoint URL pointing to your gateway's public URL + `/googlechat`
4. Set status to "Live - available to users"
5. Configure OpenClaw:

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url",   // or "project-number"
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890",  // optional, helps mention detection
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
      typingIndicator: "message",  // none | message | reaction
      mediaMaxMb: 20,
    },
  },
}
```

### Targets
- DMs: `users/<userId>` (recommended)
- Spaces: `spaces/<spaceId>`
- Email matching: only with `dangerouslyAllowNameMatching: true`

### Public URL options
1. **Tailscale Funnel** (recommended): expose only `/googlechat` publicly
2. **Caddy reverse proxy**: `reverse_proxy /googlechat* localhost:18789`
3. **Cloudflare Tunnel**: route only `/googlechat` path

### Auth verification
Google Chat sends `Authorization: Bearer <token>`. OpenClaw verifies via `audienceType` + `audience`.

### Session keys
- DMs: `agent:<agentId>:googlechat:direct:<spaceId>`
- Spaces: `agent:<agentId>:googlechat:group:<spaceId>`

### Troubleshooting
- **405 Method Not Allowed**: channel not configured, plugin not enabled, or gateway not restarted
- Check: `openclaw channels status --probe`
- Missing mentions: set `botUser` to app's user resource name

---

## iMessage (Legacy)

> **Warning:** Deprecated. Use [BlueBubbles](#bluebubbles-imessage---recommended) for new setups. The `imsg` integration may be removed in a future release.

### What it is
- Gateway spawns `imsg rpc` and communicates over JSON-RPC on stdio
- No separate daemon/port

### Quick setup
```bash
brew install steipete/tap/imsg
imsg rpc --help
```

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/user/Library/Messages/chat.db",
    },
  },
}
```

### Requirements
- Messages signed in on Mac
- Full Disk Access for OpenClaw/imsg process
- Automation permission

### DM policy
`channels.imessage.dmPolicy`: `pairing` (default) | `allowlist` | `open` | `disabled`

### Group policy
`channels.imessage.groupPolicy`: `allowlist` (default) | `open` | `disabled`

### Target formats
- `chat_id:123` (recommended, stable)
- `chat_guid:...`
- `chat_identifier:...`
- `imessage:+1555...`
- `user@example.com`

### Remote Mac over SSH
```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```
```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "user@gateway-host",
      includeAttachments: true,
    },
  },
}
```

### ACP bindings supported
`match.peer.id` accepts: normalized handle, `chat_id:<id>`, `chat_guid:<guid>`, `chat_identifier:<identifier>`

---

## IRC

**Status:** Bundled plugin. Classic IRC servers; channels + DMs with pairing/allowlist controls.

### Quick setup
```json5
{
  channels: {
    irc: {
      enabled: true,
      host: "irc.example.com",
      port: 6697,
      tls: true,
      nick: "openclaw-bot",
      channels: ["#openclaw"],
    },
  },
}
```

### Security defaults
- `dmPolicy`: defaults to `"pairing"`
- `groupPolicy`: defaults to `"allowlist"`
- TLS recommended (`tls: true`)

### Two-gate access control
1. **Channel access** (`groupPolicy` + `groups`): whether bot accepts messages from a channel
2. **Sender access** (`groupAllowFrom` / `groups["#channel"].allowFrom`): who can trigger inside that channel

### Config example (allow anyone in a channel, no mention required)
```json5
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": {
          requireMention: false,
          allowFrom: ["*"],
          tools: {
            deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
          },
          toolsBySender: {
            "*": { deny: ["group:runtime", "group:fs"] },
            "id:eigen": { deny: ["gateway", "nodes", "cron"] },
          },
        },
      },
    },
  },
}
```

### NickServ
```json5
{
  channels: {
    irc: {
      nickserv: {
        enabled: true,
        service: "NickServ",
        password: "your-nickserv-password",
        register: true,          // one-time; disable after registration
        registerEmail: "bot@example.com",
      },
    },
  },
}
```

### Environment variables
`IRC_HOST`, `IRC_PORT`, `IRC_TLS`, `IRC_NICK`, `IRC_USERNAME`, `IRC_REALNAME`, `IRC_PASSWORD`, `IRC_CHANNELS` (comma-separated), `IRC_NICKSERV_PASSWORD`, `IRC_NICKSERV_REGISTER_EMAIL`

> Note: `IRC_HOST` cannot be set from workspace `.env`

### Common gotcha
`allowFrom` is for DMs, not channels. Use `groupAllowFrom` or `groups["#channel"].allowFrom` for channel sender access.

---

## LINE

**Status:** Bundled plugin. DMs, group chats, media, locations, Flex messages, template messages, quick replies supported.

### Setup
1. Create LINE Developers account → Provider → Messaging API channel
2. Copy Channel access token + Channel secret
3. Enable "Use webhook"
4. Set webhook URL: `https://gateway-host/line/webhook`

### Config
```json5
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

Env vars: `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET`

File-backed:
```json5
{
  channels: {
    line: {
      tokenFile: "/path/to/line-token.txt",
      secretFile: "/path/to/line-secret.txt",
    },
  },
}
```

### Access control
- `dmPolicy`: `pairing | allowlist | open | disabled`
- `allowFrom`: LINE user IDs (format: `U` + 32 hex chars)
- `groupPolicy`: `allowlist | open | disabled`
- `groupAllowFrom`: user IDs for groups
- Group IDs: `C` + 32 hex chars; Room IDs: `R` + 32 hex chars

### Rich messages via `channelData.line`
```json5
{
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: { title: "Office", address: "123 Main St", latitude: 35.681236, longitude: 139.767125 },
      flexMessage: { altText: "Status card", contents: { /* Flex payload */ } },
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

### Message behavior
- Text chunked at 5000 characters
- Markdown stripped; code blocks/tables → Flex cards
- Streaming responses buffered; LINE receives full chunks with loading animation
- Media cap: `mediaMaxMb` (default 10)
- Outbound media URLs must be public HTTPS; loopback/private addresses rejected

### Outbound media
- Images: LINE image messages with auto preview
- Videos: explicit preview + content-type handling
- Audio: LINE audio messages

### ACP support
`/acp spawn <agent> --bind here` to bind LINE chat to ACP session

### Limitations
- No reactions
- No threads

---

## Matrix

**Status:** Bundled plugin. Supports DMs, rooms, threads, media, reactions, polls, location, E2EE.

### Setup
1. Create Matrix account on your homeserver
2. Configure `channels.matrix` with `homeserver` + `accessToken` (or `userId` + `password`)
3. Restart gateway; invite bot to rooms

**Important:** `channels.matrix.autoJoin` defaults to `off`. Bot won't join invited rooms without it.

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_xxx",
      encryption: true,
      dm: {
        policy: "pairing",
        sessionScope: "per-room",
        threadReplies: "off",
      },
      groupPolicy: "allowlist",
      groupAllowFrom: ["@admin:example.org"],
      groups: {
        "!roomid:example.org": { requireMention: true },
      },
      autoJoin: "allowlist",     // off | allowlist | always
      autoJoinAllowlist: ["!roomid:example.org"],
      threadReplies: "inbound",
      replyToMode: "off",
      streaming: "partial",      // off | partial | quiet
    },
  },
}
```

### Environment variables
- `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN`, `MATRIX_USER_ID`, `MATRIX_PASSWORD`, `MATRIX_DEVICE_ID`, `MATRIX_DEVICE_NAME`
- Non-default accounts: `MATRIX_<ACCOUNT_ID>_*` (punctuation escaped, e.g., `-` → `_X2D_`)

### Credentials cache
`~/.openclaw/credentials/matrix/credentials.json` (default account)
`~/.openclaw/credentials/matrix/credentials-<account>.json` (named accounts)

### Streaming previews
| Setting | Behavior |
|---------|----------|
| `streaming: "off"` (default) | Send complete reply once |
| `streaming: "partial"` | Live preview message, edited in place while generating |
| `streaming: "quiet"` | Quiet draft, finalized with custom push rule; only notifies once done |
| `blockStreaming: true` | Keep completed blocks as separate messages |

### Bot-to-bot rooms
```json5
{
  channels: {
    matrix: {
      allowBots: "mentions",  // true | "mentions"
    },
  },
}
```

### E2EE verification commands
```bash
openclaw matrix verify status [--verbose] [--json]
openclaw matrix verify bootstrap [--force-reset-cross-signing]
openclaw matrix verify device "<recovery-key>"
openclaw matrix verify self
openclaw matrix verify backup status
openclaw matrix verify backup restore
openclaw matrix verify backup reset --yes
openclaw matrix verify accept|start|sas|confirm-sas|cancel <id>
openclaw matrix devices list --account <id>
```

### E2EE in encrypted rooms
- Outbound image events use `thumbnail_file` (encrypted) in E2EE rooms
- Unencrypted rooms use plain `thumbnail_url`
- Auto-detected; no config needed

### Startup behavior with encryption
- `startupVerification` defaults to `"if-unverified"`: requests self-verification on startup for unverified devices
- Tune with `startupVerificationCooldownHours`
- Disable with `startupVerification: "off"`

### Gotchas
- `autoJoin` applies to all invites (can't distinguish DM vs group at invite time)
- Room allowlist entries must use stable IDs: `!roomId:server` or `#alias:server`
- Cross-signing verified ≠ locally trusted alone

---

## Matrix Push Rules

For `streaming: "quiet"` mode, install per-user push rules that match the `com.openclaw.finalized_preview` content flag.

### Prerequisites
- Recipient user access token
- Bot user MXID
- Working pushers already configured for recipient

### Steps
1. Configure quiet previews:
```json5
{ channels: { matrix: { streaming: "quiet" } } }
```
2. Get recipient's access token
3. Verify pushers exist
4. Install override push rule:
```bash
curl -X PUT \
  "https://matrix.example.org/_matrix/client/v3/pushrules/global/override/openclaw-finalized-preview-botname" \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "conditions": [
      { "kind": "event_match", "key": "type", "pattern": "m.room.message" },
      { "kind": "event_property_is", "key": "content.m\\.relates_to.rel_type", "value": "m.replace" },
      { "kind": "event_property_is", "key": "content.com\\.openclaw\\.finalized_preview", "value": true },
      { "kind": "event_match", "key": "sender", "pattern": "@bot:example.org" }
    ],
    "actions": ["notify", {"set_tweak": "sound", "value": "default"}, {"set_tweak": "highlight", "value": false}]
  }'
```
5. Verify + test

For multiple bots, create one rule per bot with distinct rule ID and sender match.

---

## Mattermost

**Status:** Bundled plugin. Channels, groups, and DMs supported via bot token + WebSocket events.

### Quick setup
```json5
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

Env vars: `MATTERMOST_BOT_TOKEN`, `MATTERMOST_URL` (default account only)

### Chat modes
| Mode | Behavior |
|------|----------|
| `oncall` (default) | Respond only when @mentioned |
| `onmessage` | Respond to every channel message |
| `onchar` | Respond when message starts with trigger prefix |

```json5
{
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}
```

### Threading
`channels.mattermost.replyToMode`: `off` (default) | `first` | `all`
- `first`/`all`: start thread under triggering post (thread-scoped sessions)
- DMs: always non-threaded

### Native slash commands
```json5
{
  channels: {
    mattermost: {
      commands: {
        native: true,
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
    },
  },
}
```
Reachability: callback must be reachable from Mattermost server. Check: `curl https://<gateway-host>/api/channels/mattermost/command` should return `405`.

### Reactions
```
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup remove=true
```
Config: `channels.mattermost.actions.reactions` (default: true)

### Interactive buttons
```json5
{
  channels: {
    mattermost: {
      capabilities: ["inlineButtons"],
      interactions: {
        callbackBaseUrl: "https://gateway.example.com",
      },
    },
  },
}
```
Button fields: `text` (required), `callback_data` (required), `style` (optional: `default|primary|danger`)

HMAC verification: automatic. HMAC secret derived from bot token:
```python
secret = hmac.new(b"openclaw-mattermost-interactions", bot_token.encode(), hashlib.sha256).hexdigest()
```

### Preview streaming
```json5
{
  channels: {
    mattermost: {
      streaming: "partial",  // off | partial | block | progress
    },
  },
}
```

### DM channel retry
```json5
{
  channels: {
    mattermost: {
      dmChannelRetry: {
        maxRetries: 3,
        initialDelayMs: 1000,
        maxDelayMs: 10000,
        timeoutMs: 30000,
      },
    },
  },
}
```

### Multi-account
```json5
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

### Targets
- `channel:<id>` for a channel
- `user:<id>` for a DM
- `@username` for a DM (resolved via API)
- Bare opaque IDs: resolved user-first (user then channel)

### Troubleshooting
- Buttons as white boxes: check `text` + `callback_data` fields
- Buttons return 404: button `id` may contain hyphens/underscores (must be alphanumeric only)
- `Unauthorized: invalid command token`: registration failed or wrong callback target

---

## Microsoft Teams

**Status:** Bundled plugin. Text and DM attachments supported. Channel/group file sending requires `sharePointSiteId` + Graph permissions.

### Quick setup (minimal config with client secret)
```json5
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

### Federated authentication (production recommended)

**Certificate-based:**
```json5
{
  channels: {
    msteams: {
      authType: "federated",
      certificatePath: "/path/to/cert.pem",
    },
  },
}
```

**Managed Identity (Azure):**
```json5
{
  channels: {
    msteams: {
      authType: "federated",
      useManagedIdentity: true,
      managedIdentityClientId: "<MI_CLIENT_ID>",  // only for user-assigned
    },
  },
}
```

### Access control
DMs: `dmPolicy` (default: `"pairing"`), `allowFrom` (use stable AAD object IDs)

Groups:
- Default: `groupPolicy = "allowlist"` (blocked until `groupAllowFrom` set)
- `groupPolicy: "open"` → mention-gated
- Teams allowlist: `channels.msteams.teams`

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
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

### RSC permissions (Teams manifest)
```json
"authorization": {
  "permissions": {
    "resourceSpecific": [
      { "name": "ChannelMessage.Read.Group", "type": "Application" },
      { "name": "ChannelMessage.Send.Group", "type": "Application" },
      { "name": "Member.Read.Group", "type": "Application" },
      { "name": "ChatMessage.Read.Chat", "type": "Application" }
      // ... additional permissions
    ]
  }
}
```

### Capabilities comparison
| Capability | RSC only | RSC + Graph API |
|------------|----------|-----------------|
| Real-time messages | ✅ | ✅ |
| Historical messages | ❌ | ✅ |
| Images/file contents | ❌ | ✅ |
| SharePoint/OneDrive attachments | ❌ | ✅ |

### History context
- `channels.msteams.historyLimit` (default 50, set `0` to disable)
- Fetched thread history filtered by sender allowlists

### Local dev tunneling
- ngrok: `ngrok http 3978`
- Tailscale Funnel: `tailscale funnel 3978`

### Config writes
Disable: `channels.msteams.configWrites: false`

---

## Nextcloud Talk

**Status:** Bundled plugin. DMs, rooms, reactions, and markdown messages supported.

### Setup
1. Install OpenClaw bot on Nextcloud server:
```bash
./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
```
2. Enable bot in target room settings
3. Configure OpenClaw:

```json5
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

CLI setup:
```bash
openclaw channels add --channel nextcloud-talk --url https://cloud.example.com --token "<shared-secret>"
```

### Access control
- DMs: `dmPolicy` (default: `pairing`); `allowFrom` = Nextcloud user IDs only
- Rooms: `groupPolicy = allowlist | open | disabled`; per-room config under `rooms`

### Capabilities
| Feature | Status |
|---------|--------|
| Direct messages | Supported |
| Rooms | Supported |
| Threads | Not supported |
| Media | URL-only |
| Reactions | Supported |
| Native commands | Not supported |

### Notes
- Bots cannot initiate DMs; user must message first
- `apiUser` + `apiPassword` needed for DM detection (room-type lookup)
- Webhook URL must be reachable by the Gateway; set `webhookPublicUrl` if behind a proxy

### Config reference
`channels.nextcloud-talk.enabled|baseUrl|botSecret|botSecretFile|apiUser|apiPassword|webhookPort(8788)|webhookHost(0.0.0.0)|webhookPath(/nextcloud-talk-webhook)|webhookPublicUrl|dmPolicy|allowFrom|groupPolicy|groupAllowFrom|rooms|historyLimit|dmHistoryLimit|textChunkLimit|chunkMode|mediaMaxMb`

---

## Nostr

**Status:** Bundled plugin, disabled by default until configured. DMs only via NIP-04.

### Quick setup
```bash
nak key generate  # generate keypair
export NOSTR_PRIVATE_KEY="nsec1..."
```

```json5
{
  channels: {
    nostr: {
      privateKey: "${NOSTR_PRIVATE_KEY}",
      relays: ["wss://relay.damus.io", "wss://relay.primal.net"],
      dmPolicy: "pairing",
    },
  },
}
```

CLI:
```bash
openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY"
openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY" --relay-urls "wss://relay.damus.io,wss://relay.primal.net"
```

### Config reference
| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `privateKey` | string | required | `nsec...` or 64-char hex |
| `relays` | string[] | `['wss://relay.damus.io', 'wss://nos.lol']` | Relay WebSocket URLs |
| `dmPolicy` | string | `pairing` | DM access policy |
| `allowFrom` | string[] | `[]` | Allowed sender pubkeys (`npub...` or hex) |
| `enabled` | boolean | `true` | |
| `profile` | object | — | NIP-01 profile metadata |

### Profile metadata
```json5
{
  channels: {
    nostr: {
      profile: {
        name: "openclaw",
        displayName: "OpenClaw",
        about: "Personal assistant DM bot",
        picture: "https://example.com/avatar.png",
        nip05: "openclaw@example.com",
        lud16: "openclaw@example.com",
      },
    },
  },
}
```

### Security
- Event signatures verified BEFORE sender policy and decryption
- Pairing replies sent without processing original DM body
- Rate limited; oversized payloads dropped before decrypt

### Protocol support
| NIP | Status |
|-----|--------|
| NIP-01 | Supported (basic events + profile) |
| NIP-04 | Supported (encrypted DMs, kind:4) |
| NIP-17 | Planned (gift-wrapped DMs) |
| NIP-44 | Planned (versioned encryption) |

### Limitations
- DMs only (no group chats)
- No media attachments
- NIP-04 only (NIP-17 planned)
- Duplicate responses expected with multiple relays (deduplicated by event ID)

---

## QQ Bot

**Status:** Bundled plugin. C2C private chat, group @messages, guild channels, rich media.

### Setup
1. Register at https://q.qq.com/
2. Create bot → copy AppID + AppSecret (never stored in plaintext by Tencent)

```bash
openclaw channels add --channel qqbot --token "AppID:AppSecret"
```

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      appId: "YOUR_APP_ID",
      clientSecret: "YOUR_APP_SECRET",
    },
  },
}
```

Env vars: `QQBOT_APP_ID`, `QQBOT_CLIENT_SECRET`

### Target formats
| Format | Description |
|--------|-------------|
| `qqbot:c2c:OPENID` | Private chat (C2C) |
| `qqbot:group:GROUP_OPENID` | Group chat |
| `qqbot:channel:CHANNEL_ID` | Guild channel |

> Each bot has its own user OpenIDs; OpenIDs from Bot A cannot be used with Bot B.

### Voice (STT/TTS)
```json5
{
  channels: {
    qqbot: {
      stt: { provider: "your-provider", model: "your-stt-model" },
      tts: { provider: "your-provider", model: "your-tts-model", voice: "your-voice" },
    },
  },
}
```

### Built-in slash commands
`/bot-ping`, `/bot-version`, `/bot-help`, `/bot-upgrade`, `/bot-logs`, `/bot-approve`

### Multi-account
```json5
{
  channels: {
    qqbot: {
      appId: "111111111",
      clientSecret: "secret-of-bot-1",
      accounts: {
        bot2: { appId: "222222222", clientSecret: "secret-of-bot-2" },
      },
    },
  },
}
```

---

## Signal

**Status:** External CLI integration. Gateway talks to `signal-cli` over HTTP JSON-RPC + SSE.

### Prerequisites
- `signal-cli` installed on gateway host (JVM build requires Java)
- Phone number for verification (SMS path) or existing Signal account (QR link path)

### Setup path A: Link existing Signal account (QR)
```bash
signal-cli link -n "OpenClaw"   # scan QR in Signal app
```

### Setup path B: Register dedicated number
```bash
# Install signal-cli native binary
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz"
sudo tar xf "signal-cli-${VERSION}-Linux-native.tar.gz" -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/

# Register (captcha may be required)
signal-cli -a +<BOT_PHONE_NUMBER> register --captcha '<SIGNALCAPTCHA_URL>'
signal-cli -a +<BOT_PHONE_NUMBER> verify <VERIFICATION_CODE>
```

### Config
```json5
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

### Access control
DMs: `dmPolicy` (default: `pairing`); `allowFrom` accepts E.164 or `uuid:<id>`

Groups:
- `groupPolicy = open | allowlist | disabled`
- `groupAllowFrom`
- `channels.signal.groups["<group-id>" | "*"]` for per-group overrides (`requireMention`, `tools`, `toolsBySender`)

### External daemon mode
```json5
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

### Reactions
```
message action=react channel=signal target=uuid:123e4567-... messageId=1737630212345 emoji=🔥
message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅
```

Config: `channels.signal.reactionLevel: off | ack | minimal | extensive`

### Delivery targets
- DMs: `signal:+15551234567` or plain E.164
- UUID DMs: `uuid:<id>`
- Groups: `signal:group:<groupId>`

### Typing + read receipts
- Typing indicators: automatic (via `signal-cli sendTyping`)
- Read receipts: `channels.signal.sendReadReceipts` (for allowed DMs)

### Media
- Text chunk: `channels.signal.textChunkLimit` (default 4000)
- Chunk mode: `length` (default) or `newline`
- Attachments: `channels.signal.ignoreAttachments` to skip
- Media cap: `channels.signal.mediaMaxMb` (default 8)

### Security notes
- `signal-cli` stores account keys in `~/.local/share/signal-cli/data/`
- Registering a number with `signal-cli` can de-authenticate the main Signal app for that number → use dedicated bot number

---

## Slack

**Status:** Production-ready for DMs and channels. Default: Socket Mode; HTTP Request URLs also supported.

### Quick setup (Socket Mode)
1. Create Slack app from manifest at https://api.slack.com/apps/new
2. Generate App-Level Token (`xapp-...`) with `connections:write`
3. Install app, copy Bot Token (`xoxb-...`)

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "socket",          // or "http"
      appToken: "xapp-...",    // Socket Mode only
      botToken: "xoxb-...",
      signingSecret: "...",    // HTTP mode only
    },
  },
}
```

Env fallback: `SLACK_APP_TOKEN`, `SLACK_BOT_TOKEN` (default account only)

### Required OAuth scopes
`app_mentions:read`, `assistant:write`, `channels:history`, `channels:read`, `chat:write`, `commands`, `emoji:read`, `files:read`, `files:write`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`, `mpim:write`, `pins:read`, `pins:write`, `reactions:read`, `reactions:write`, `users:read`

Optional: `chat:write.customize` (for custom agent identity in messages)

### Access control
DM policy (`channels.slack.dmPolicy`): `pairing` (default) | `allowlist` | `open` | `disabled`

Channel policy (`channels.slack.groupPolicy`): `open | allowlist | disabled`

Channel allowlist uses stable channel IDs under `channels.slack.channels`.

Per-channel controls: `requireMention`, `users`, `allowBots`, `skills`, `systemPrompt`, `tools`, `toolsBySender`

### Threading and sessions
- DMs → `direct`; channels → `channel`; MPIMs → `group`
- `channels.slack.replyToMode`: `off | first | all | batched` (default `off`)
- Thread sessions: `agent:<agentId>:slack:channel:<channelId>:thread:<threadTs>`
- `thread.historyScope` default: `thread`; `thread.inheritParent` default: `false`
- `thread.requireExplicitMention` default: `false`

> **Note:** `replyToMode="off"` disables ALL reply threading, including explicit `[[reply_to_*]]` tags. Different from Telegram.

### Ack reactions
Resolution order: account `ackReaction` → channel `ackReaction` → `messages.ackReaction` → agent identity emoji (default "👀")

```json5
{ channels: { slack: { ackReaction: "eyes" } } }
```

### Text streaming
```json5
{
  channels: {
    slack: {
      streaming: "partial",  // off | partial | block | progress
    },
  },
}
```

### Actions
| Group | Default |
|-------|---------|
| messages | enabled |
| reactions | enabled |
| pins | enabled |
| memberInfo | enabled |
| emojiList | enabled |

Actions: `send`, `upload-file`, `download-file`, `read`, `edit`, `delete`, `pin`, `unpin`, `list-pins`, `member-info`, `emoji-list`

### User token (`userToken`)
- Config-only (no env fallback)
- Defaults to read-only (`userTokenReadOnly: true`)
- For writes: `userTokenReadOnly: false` (only when bot token unavailable)

### Multi-account
Use `channels.slack.accounts` with per-account tokens. Named accounts inherit `channels.slack.allowFrom` when own `allowFrom` unset; they do NOT inherit `accounts.default.allowFrom`.

---

## Synology Chat

**Status:** Bundled plugin. Direct messages only via outgoing + incoming webhooks.

### Setup
1. In Synology Chat integrations: create incoming + outgoing webhooks
2. Point outgoing webhook URL to: `https://gateway-host/webhook/synology`
3. Configure OpenClaw:

```json5
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

CLI setup:
```bash
openclaw channels add --channel synology-chat --token <token> --url <incoming-webhook-url>
```

### Webhook auth
OpenClaw accepts token from (in order): `body.token`, `?token=...`, headers (`x-synology-token`, `x-webhook-token`, `x-openclaw-token`, `Authorization: Bearer <token>`)

### Access control
- `dmPolicy`: `allowlist` (recommended) | `open` | `disabled`
- `allowedUserIds`: list of Synology numeric user IDs
- Empty `allowedUserIds` with `dmPolicy: "allowlist"` = misconfiguration (route won't start)

### Targets for outbound delivery
```bash
openclaw message send --channel synology-chat --target 123456 --text "Hello"
openclaw message send --channel synology-chat --target synology-chat:123456 --text "Hello"
```

Media sends are URL-based; outbound URLs must use http/https.

### Multi-account
Give each account a distinct `webhookPath`. Duplicate paths rejected (fail-closed).

### Env vars
`SYNOLOGY_CHAT_TOKEN`, `SYNOLOGY_CHAT_INCOMING_URL`, `SYNOLOGY_NAS_HOST`, `SYNOLOGY_ALLOWED_USER_IDS`, `SYNOLOGY_RATE_LIMIT`, `OPENCLAW_BOT_NAME`

> Note: `SYNOLOGY_CHAT_INCOMING_URL` cannot be set from workspace `.env`

### Security
- Invalid token checks: constant-time comparison, fail-closed
- Rate limited per sender
- `dangerouslyAllowNameMatching: false` (keeps stable numeric user ID matching)
- `dangerouslyAllowInheritedWebhookPath: false`

---

## Telegram

**Status:** Production-ready via grammY. Long polling (default) or webhook mode.

### Quick setup
1. Chat with @BotFather → `/newbot` → save token
2. Configure:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Env fallback: `TELEGRAM_BOT_TOKEN=...` (default account only)

> Token resolution is account-aware: config values win over env; `TELEGRAM_BOT_TOKEN` only applies to the default account. Telegram does NOT use `openclaw channels login telegram`.

3. Approve first DM:
```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### Telegram bot settings
- **Privacy Mode**: disable via `/setprivacy` or make bot admin (allows seeing all group messages)
- When toggling privacy mode, **remove + re-add the bot** in each group so Telegram applies the change
- Group permissions: `/setjoingroups`, `/setprivacy`

### Access control

DM policy (`channels.telegram.dmPolicy`): `pairing` (default) | `allowlist` | `open` | `disabled`

`allowFrom` accepts numeric Telegram user IDs (with optional `telegram:` or `tg:` prefix).

Finding your Telegram user ID:
```bash
# DM your bot, then:
openclaw logs --follow   # read from.id
# Or:
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

Group policy:
- `groupPolicy: "allowlist"` (default) + `channels.telegram.groups` entries
- Groups as negative chat IDs go under `channels.telegram.groups`
- User IDs for sender filtering go in `groupAllowFrom`
- `groupAllowFrom` does NOT inherit DM pairing-store approvals
- Pattern for one-owner bots: set user ID in `allowFrom`, leave `groupAllowFrom` unset, allow target groups under `groups`

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          groupPolicy: "open",
          requireMention: false,
          allowFrom: ["8734062810", "745123456"],  // restrict senders
        },
      },
    },
  },
}
```

### Feature reference

**Live streaming preview:**
```json5
{
  channels: {
    telegram: {
      streaming: "partial",  // off | partial | block | progress
    },
  },
}
```
- DM: keeps same preview, final edit in place
- Group/topic: same behavior
- Reasoning stream: `/reasoning stream` → live preview while generating
- `streaming.preview.toolProgress` (default: `true`): controls whether tool/progress updates reuse the same edited preview message. Set `false` to keep separate tool/progress messages.

**Formatting:** Outbound uses `parse_mode: "HTML"`. Falls back to plain text on parse failure.

**Native commands:** Registered via `setMyCommands`. Custom commands:
```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
    },
  },
}
```

**Inline buttons:**
```json5
{
  channels: {
    telegram: {
      capabilities: {
        inlineButtons: "allowlist",  // off | dm | group | all | allowlist
      },
    },
  },
}
```

Legacy `capabilities: ["inlineButtons"]` (array format) maps to `inlineButtons: "all"`.
```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  message: "Choose an option:",
  buttons: [
    [{ text: "Yes", callback_data: "yes" }, { text: "No", callback_data: "no" }],
    [{ text: "Cancel", callback_data: "cancel" }],
  ],
}
```

**Message actions:**
- `sendMessage`, `react`, `deleteMessage`, `editMessage`, `createForumTopic`
- Config gates: `channels.telegram.actions.sendMessage|deleteMessage|reactions|sticker`

**Reply tags:**
- `[[reply_to_current]]`, `[[reply_to:<id>]]`
- `channels.telegram.replyToMode`: `off (default) | first | all`
- Even with `off`, explicit tags are honored

**Forum topics:**
- Session keys: `agent:<agentId>:telegram:group:<chatId>:topic:<threadId>`
- Per-topic agent routing via `agentId` in topic config
- Topic entries inherit group settings unless overridden (`requireMention`, `allowFrom`, `skills`, `systemPrompt`, `enabled`, `groupPolicy`)
- **Important:** `agentId` is topic-only and does NOT inherit from group defaults. All other listed settings do inherit.

### Runtime model
- Long-polling via grammY runner with per-chat/per-thread sequencing
- Polling watchdog: restart after 120s without `getUpdates` liveness
- `pollingStallThresholdMs`: 30000–600000 ms range
- DM messages can carry `message_thread_id`; OpenClaw routes with thread-aware session keys and preserves thread ID for replies
- No read-receipt support

### Doctor fixes for Telegram
- If config contains `@username` allowlist entries from older setups, run `openclaw doctor --fix` to resolve them (best-effort; requires bot token)
- `doctor --fix` can recover pairing-store entries into `channels.telegram.allowFrom` in allowlist flows

### Device pairing (device-pair plugin)
```
/pair → setup code → paste in iOS app → /pair pending → /pair approve <requestId>
```

### Common mistakes
- `groupAllowFrom` ≠ group chat allowlist (group chat IDs go in `groups`)
- `dmPolicy: "allowlist"` with empty `allowFrom` blocks all DMs

---

## Tlon (Urbit)

**Status:** Bundled plugin. DMs, group mentions, thread replies, rich text, image uploads. No reactions or polls.

### What it is
Connects to your Urbit ship (Tlon messenger) via the `zca-js` API.

### Setup
```json5
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
      ownerShip: "~your-main-ship",  // recommended: always authorized
    },
  },
}
```

For private/LAN ships:
```json5
{
  channels: {
    tlon: {
      url: "http://localhost:8080",
      allowPrivateNetwork: true,  // disables SSRF protection for this URL
    },
  },
}
```

### Access control
DM allowlist:
```json5
{ channels: { tlon: { dmAllowlist: ["~zod", "~nec"] } } }
```

Group authorization:
```json5
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
          "chat/~host-ship/announcements": { mode: "open" },
        },
      },
    },
  },
}
```

### Owner ship
- Always authorized everywhere (DMs auto-accepted, channel messages always allowed)
- Receives notifications for unauthorized access attempts

### Auto-accept settings
```json5
{
  channels: {
    tlon: {
      autoAcceptDmInvites: true,
      autoAcceptGroupInvites: true,
    },
  },
}
```

### Delivery targets
- DM: `~sampel-palnet` or `dm/~sampel-palnet`
- Group: `chat/~host-ship/channel` or `group:~host-ship/channel`

### Bundled skill
Provides CLI access: contacts, channels, groups, DMs, reactions, settings (via slash commands).

### Capabilities
| Feature | Status |
|---------|--------|
| Direct messages | ✅ |
| Groups/channels | ✅ (mention-gated) |
| Threads | ✅ (auto-replies in thread) |
| Rich text | ✅ (Markdown → Tlon format) |
| Images | ✅ (uploaded to Tlon storage) |
| Reactions | ✅ (via bundled skill) |
| Polls | ❌ |
| Native commands | ✅ (owner-only by default) |

---

## Twitch

**Status:** Bundled plugin. Twitch chat via IRC connection.

### Quick setup
1. Create dedicated Twitch account for bot
2. Generate credentials at https://twitchtokengenerator.com/ (select Bot Token, scopes: `chat:read`, `chat:write`)
3. Find your Twitch user ID

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
      allowFrom: ["123456789"],  // your Twitch user ID (permanent, unlike usernames)
    },
  },
}
```

Env var: `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (default account only)

### Access control
- `allowFrom`: hard allowlist by Twitch user ID (permanent, unlike usernames)
- `allowedRoles`: `"moderator" | "owner" | "vip" | "subscriber" | "all"`
- `requireMention`: default `true`

When both are set, `allowFrom` takes precedence.

### Token refresh
```json5
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```
Requires own Twitch application at https://dev.twitch.tv/console.

### Multi-account
```json5
{
  channels: {
    twitch: {
      accounts: {
        channel1: { username: "openclaw", accessToken: "...", clientId: "...", channel: "vevisk" },
        channel2: { username: "openclaw", accessToken: "...", clientId: "...", channel: "secondchannel" },
      },
    },
  },
}
```

### Limits
- 500 characters per message (auto-chunked at word boundaries)
- No built-in rate limiting (uses Twitch's limits)
- Markdown stripped before chunking

### Tool actions
- `action: "twitch"` with `params: { message: "...", to: "#mychannel" }`

---

## WeChat

**Status:** External plugin (`@tencent-weixin/openclaw-weixin`). Direct chats and media supported. Group chats not advertised.

### Naming
- Channel id: `openclaw-weixin`
- npm package: `@tencent-weixin/openclaw-weixin`
- Use `openclaw-weixin` in CLI commands and config paths

### Install
```bash
npx -y @tencent-weixin/openclaw-weixin-cli install
# or manual:
openclaw plugins install "@tencent-weixin/openclaw-weixin"
openclaw config set plugins.entries.openclaw-weixin.enabled true
openclaw gateway restart
```

### Login (QR)
```bash
openclaw channels login --channel openclaw-weixin
```

### Pairing
```bash
openclaw pairing list openclaw-weixin
openclaw pairing approve openclaw-weixin <CODE>
```

### Compatibility
| Plugin line | OpenClaw version |
|-------------|-----------------|
| `2.x` | `>=2026.3.22` |
| `1.x` | `>=2026.1.0 <2026.3.22` |

### Multi-account session isolation
```bash
openclaw config set session.dmScope per-account-channel-peer
```

### Troubleshooting
- Gateway restart loops after enabling WeChat: update both OpenClaw and plugin
- Temporary disable: `openclaw config set plugins.entries.openclaw-weixin.enabled false`

---

## WhatsApp

**Status:** Production-ready via WhatsApp Web (Baileys). Gateway owns linked session(s).

### Install (on demand)
```bash
openclaw plugins install @openclaw/whatsapp
# or: openclaw onboard, openclaw channels add --channel whatsapp
# Custom auth dir:
openclaw channels add --channel whatsapp --account work --auth-dir /path/to/wa-auth
openclaw channels login --channel whatsapp --account work
```

> Recommended: use a separate/dedicated number for OpenClaw. Personal-number setups also supported with `selfChatMode: true`.

### Quick setup
```json5
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

```bash
openclaw channels login --channel whatsapp
openclaw gateway
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

### Access control

DM policy (`channels.whatsapp.dmPolicy`): `pairing | allowlist | open | disabled`

Group access (two layers):
1. **Group membership**: `channels.whatsapp.groups` (when configured, acts as allowlist)
2. **Group sender**: `groupPolicy` + `groupAllowFrom`

Mention detection:
- Explicit WhatsApp mentions
- Configured regex patterns
- Implicit reply-to-bot
- Quote/reply satisfies mention gating but does NOT grant sender authorization

### System prompts
Distinct from Telegram multi-account behavior. Resolution hierarchy:
1. Group-specific: `groups["<groupId>"].systemPrompt` (empty string suppresses wildcard)
2. Group wildcard: `groups["*"].systemPrompt`
3. Direct-specific: `direct["<peerId>"].systemPrompt`
4. Direct wildcard: `direct["*"].systemPrompt`

**Multi-account override behavior:** If an account defines its own `groups` map, it **fully replaces** the root `groups` map (no deep merge). The same applies to `direct`. Prompt lookup then runs on the resulting single map.

### Personal-number and self-chat
When linked self number is in `allowFrom`:
- Skip read receipts for self-chat turns
- Avoid mention-JID auto-trigger
- Response prefix defaults to `[{identity.name}]`
- Set `selfChatMode: true` for personal-number mode
- OpenClaw never auto-pairs outbound `fromMe` DMs (messages sent from linked device)
- `@status` and `@broadcast` chats are ignored

### Media
- Text chunk: `channels.whatsapp.textChunkLimit` (default 4000); `chunkMode: length | newline`
- Images auto-optimized (resize/quality sweep)
- Media cap: `channels.whatsapp.mediaMaxMb` (default 50)
- `audio/ogg` rewritten to `audio/ogg; codecs=opus` for voice-note compatibility
- GIF playback: `gifPlayback: true` on video sends

### Reply quoting
`channels.whatsapp.replyToMode`: `"auto"` (default) | `"on"` | `"off"`

### Reaction level
| Level | Ack reactions | Agent reactions |
|-------|--------------|-----------------|
| `"off"` | No | No |
| `"ack"` | Yes | No |
| `"minimal"` (default) | Yes | Yes (conservative) |
| `"extensive"` | Yes | Yes (encouraged) |

### Acknowledgment reactions
```json5
{
  channels: {
    whatsapp: {
      ackReaction: {
        emoji: "👀",
        direct: true,
        group: "mentions",  // always | mentions | never
      },
    },
  },
}
```

### Plugin hooks (opt-in)
```json5
{
  channels: {
    whatsapp: {
      pluginHooks: { messageReceived: true },
    },
  },
}
```

### Proxy support
Standard proxy env vars: `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY` (preferred over channel-specific proxy settings)

### Config writes
Disable: `channels.whatsapp.configWrites: false`

### Multi-account credentials
- Auth path: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- Logout: `openclaw channels logout --channel whatsapp [--account <id>]`

### Broadcast groups
WhatsApp supports broadcast groups (see [Broadcast Groups](#broadcast-groups) section).

### Troubleshooting
- Not linked: `openclaw channels login --channel whatsapp`
- Reconnect loop: `openclaw doctor && openclaw logs --follow`
- Group messages ignored: check `groupPolicy`, `groupAllowFrom`, `groups` allowlist, mention gating
- Bun runtime: use Node (Bun flagged incompatible for stable WhatsApp/Telegram)
- Pairing requests expire after 1 hour; pending requests capped at 3 per channel

---

## Zalo (Bot API)

**Status:** Experimental. DMs supported. Marketplace bots only (groups not available for Marketplace bots).

### Quick setup
```json5
{
  channels: {
    zalo: {
      enabled: true,
      accounts: {
        default: {
          botToken: "12345689:abc-xyz",
          dmPolicy: "pairing",
        },
      },
    },
  },
}
```

Env var: `ZALO_BOT_TOKEN=...` (default account only)

Get token from https://bot.zaloplatforms.com

### Long-polling vs webhook
- Default: long-polling (no public URL required)
- Webhook: set `channels.zalo.webhookUrl` + `channels.zalo.webhookSecret` (8-256 chars, HTTPS required)
- `X-Bot-Api-Secret-Token` header for webhook verification
- Polling and webhook are mutually exclusive

### Capabilities (Marketplace bots)
| Feature | Status |
|---------|--------|
| Direct messages | ✅ |
| Groups | ❌ Not available |
| Media (inbound images) | ⚠️ Limited |
| Plain URLs | ✅ |
| Link previews | ⚠️ Unreliable |
| Reactions | ❌ |
| Stickers | ⚠️ No agent reply |
| Voice/audio/video | ⚠️ No agent reply |
| Threads | ❌ |
| Native commands | ❌ |
| Streaming | ⚠️ Blocked (2000 char limit) |

### Config reference
`channels.zalo.enabled|botToken|tokenFile|dmPolicy|allowFrom|groupPolicy|groupAllowFrom|mediaMaxMb(5)|webhookUrl|webhookSecret|webhookPath|proxy`

Multi-account: `channels.zalo.accounts.<id>.*`

---

## Zalo Personal

**Status:** Experimental. Automates a **personal Zalo account** via `zca-js`.

> **Warning:** Unofficial integration. May result in account suspension/ban.

### Setup
```bash
openclaw channels login --channel zalouser  # QR code scan
```

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

### Finding IDs
```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

### Access control
DMs: `dmPolicy`: `pairing | allowlist | open | disabled`; `allowFrom` = user IDs or names

Groups: `groupPolicy = open` (default) | `allowlist` | `disabled`

Group allowlist:
```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["1471383327500481391"],
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
        "*": { allow: true, requireMention: true },
      },
    },
  },
}
```

### Group mention gating
- `requireMention` per group (default: `true`)
- Quoting a bot message = implicit mention
- Authorized control commands bypass mention gating

### Multi-account
```json5
{
  channels: {
    zalouser: {
      defaultAccount: "default",
      accounts: { work: { enabled: true, profile: "work" } },
    },
  },
}
```

### Reactions
`message action=react` with `remove: true` to remove specific emoji.

### Limits
- Text chunked to ~2000 chars
- Streaming blocked by default

---

## Troubleshooting

### Universal command ladder
```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

### Healthy baseline
- `Runtime: running`
- `Connectivity probe: ok`
- Channel probe shows transport connected

### Channel-specific troubleshooting

| Channel | Common issue | Quick check | Fix |
|---------|-------------|-------------|-----|
| WhatsApp | No DM replies | `openclaw pairing list whatsapp` | Approve sender or switch DM policy |
| WhatsApp | Group messages ignored | Check `requireMention` + mention patterns | Mention bot or relax policy |
| Telegram | No group replies | Verify mention requirement and privacy mode | Disable privacy mode or mention bot |
| Telegram | Polling stalls | `openclaw logs --follow` | Tune `pollingStallThresholdMs` |
| Discord | No guild replies | `openclaw channels status --probe` | Allow guild/channel, verify message content intent |
| Slack | No responses | Check tokens + scopes | Verify `botTokenStatus` / `appTokenStatus` |
| iMessage/BB | No inbound events | Check webhook/server reachability | Fix webhook URL or BlueBubbles server state |
| Signal | No replies | `openclaw channels status --probe` | Verify signal-cli daemon + account |
| QQ Bot | "Gone to Mars" | Verify appId + clientSecret | Set credentials or restart gateway |
| Matrix | Encrypted rooms fail | `openclaw matrix verify status` | Re-verify device; check backup status |

---

## Feature Comparison Table

| Channel | DMs | Groups | Reactions | Media | Voice | Buttons | Threads | Streaming | E2EE |
|---------|-----|--------|-----------|-------|-------|---------|---------|-----------|------|
| **BlueBubbles** (iMessage) | ✅ | ✅ | ✅ (tapbacks) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ (native) |
| **Discord** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ (Components v2) | ✅ | ❌ | ❌ |
| **Feishu/Lark** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ (cards) | ❌ |
| **Google Chat** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **iMessage (Legacy)** | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ (native) |
| **IRC** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **LINE** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ (quick replies) | ❌ | ❌ | ❌ |
| **Matrix** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ (partial/quiet) | ✅ (E2EE) |
| **Mattermost** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Microsoft Teams** | ✅ | ✅ | ❌ | ✅ (DM) | ❌ | ✅ (Adaptive Cards) | ✅ | ❌ | ✅ (native) |
| **Nextcloud Talk** | ✅ | ✅ | ✅ | ❌ (URL only) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Nostr** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (NIP-04) |
| **QQ Bot** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Signal** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ (native) |
| **Slack** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Synology Chat** | ✅ | ❌ | ❌ | ✅ (URL) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Telegram** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (inline) | ✅ (topics) | ✅ (partial) | ❌ |
| **Tlon** | ✅ | ✅ | ✅ (skill) | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ (Urbit) |
| **Twitch** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **WeChat** | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **WhatsApp** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ (native) |
| **Zalo (Bot API)** | ✅ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Zalo Personal** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### DM Policy options by channel
| Channel | pairing | allowlist | open | disabled |
|---------|---------|-----------|------|---------|
| BlueBubbles | ✅ default | ✅ | ✅ | ✅ |
| Discord | ✅ default | ✅ | ✅ | ✅ |
| Feishu | ✅ | ✅ default | ✅ | ✅ |
| Google Chat | ✅ default | ✅ | ✅ | ✅ |
| iMessage | ✅ default | ✅ | ✅ | ✅ |
| IRC | ✅ default | ✅ | ✅ | ✅ |
| LINE | ✅ default | ✅ | ✅ | ✅ |
| Matrix | ✅ default | ✅ | ✅ | ✅ |
| Mattermost | ✅ default | ✅ | ✅ | ✅ |
| MS Teams | ✅ default | ✅ | ✅ | ✅ |
| Nextcloud Talk | ✅ default | ✅ | ✅ | ✅ |
| Nostr | ✅ default | ✅ | ✅ | ✅ |
| QQ Bot | — | — | — | — |
| Signal | ✅ default | ✅ | ✅ | ✅ |
| Slack | ✅ default | ✅ | ✅ | ✅ |
| Synology Chat | ✅ | ✅ default | ✅ | ✅ |
| Telegram | ✅ default | ✅ | ✅ | ✅ |
| Tlon | — | owner ship | — | — |
| Twitch | — | ✅ | — | — |
| WeChat | ✅ default | ✅ | ✅ | ✅ |
| WhatsApp | ✅ default | ✅ | ✅ | ✅ |
| Zalo (Bot) | ✅ default | ✅ | ✅ | ✅ |
| Zalo Personal | ✅ default | ✅ | ✅ | ✅ |

### Bundled vs external plugins
| Channel | Type | Install |
|---------|------|---------|
| BlueBubbles | Bundled | Included |
| Discord | Core | Included |
| Feishu | Bundled | Included |
| Google Chat | Bundled | `openclaw plugins install @openclaw/googlechat` (older builds) |
| iMessage | Bundled | Included (legacy) |
| IRC | Bundled | Included |
| LINE | Bundled | `openclaw plugins install @openclaw/line` (older builds) |
| Matrix | Bundled | `openclaw plugins install @openclaw/matrix` (older builds) |
| Mattermost | Bundled | `openclaw plugins install @openclaw/mattermost` (older builds) |
| MS Teams | Bundled | `openclaw plugins install @openclaw/msteams` (older builds) |
| Nextcloud Talk | Bundled | `openclaw plugins install @openclaw/nextcloud-talk` (older builds) |
| Nostr | Bundled | `openclaw plugins install @openclaw/nostr` (older builds) |
| QQ Bot | Bundled | Included |
| Signal | External CLI | Requires `signal-cli` |
| Slack | Core | Included |
| Synology Chat | Bundled | Included |
| Telegram | Core | Included |
| Tlon | Bundled | `openclaw plugins install @openclaw/tlon` (older builds) |
| Twitch | Bundled | `openclaw plugins install @openclaw/twitch` (older builds) |
| WeChat | External | `npx -y @tencent-weixin/openclaw-weixin-cli install` |
| WhatsApp | On-demand | `openclaw plugins install @openclaw/whatsapp` |
| Zalo (Bot) | Bundled | `openclaw plugins install @openclaw/zalo` (older builds) |
| Zalo Personal | Bundled | `openclaw plugins install @openclaw/zalouser` (older builds) |
