# iMessage

Source: https://docs.openclaw.ai/channels/imessage

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessaging platformsiMessageGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [iMessage (legacy: imsg)](#imessage-legacy-imsg)
- [Quick setup](#quick-setup)
- [Requirements and permissions (macOS)](#requirements-and-permissions-macos)
- [Access control and routing](#access-control-and-routing)
- [Deployment patterns](#deployment-patterns)
- [Media, chunking, and delivery targets](#media-chunking-and-delivery-targets)
- [Config writes](#config-writes)
- [Troubleshooting](#troubleshooting)
- [Configuration reference pointers](#configuration-reference-pointers)

​iMessage (legacy: imsg)
For new iMessage deployments, use [BlueBubbles](/channels/bluebubbles).The `imsg` integration is legacy and may be removed in a future release.
Status: legacy external CLI integration. Gateway spawns `imsg rpc` and communicates over JSON-RPC on stdio (no separate daemon/port).
## BlueBubbles (recommended)

Preferred iMessage path for new setups.## Pairing

iMessage DMs default to pairing mode.## Configuration reference

Full iMessage field reference.
​Quick setup

 Local Mac (fast path) Remote Mac over SSH
1Install and verify imsg

Copy```
brew install steipete/tap/imsg
imsg rpc --help

```

2Configure OpenClaw

Copy```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/<you>/Library/Messages/chat.db",
    },
  },
}

```

3Start gateway

Copy```
openclaw gateway

```

4Approve first DM pairing (default dmPolicy)

Copy```
openclaw pairing list imessage
openclaw pairing approve imessage <CODE>

```

Pairing requests expire after 1 hour.OpenClaw only requires a stdio-compatible `cliPath`, so you can point `cliPath` at a wrapper script that SSHes to a remote Mac and runs `imsg`.Copy```
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"

```

Recommended config when attachments are enabled:Copy```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "user@gateway-host", // used for SCP attachment fetches
      includeAttachments: true,
    },
  },
}

```

If `remoteHost` is not set, OpenClaw attempts to auto-detect it by parsing the SSH wrapper script.
​Requirements and permissions (macOS)

- Messages must be signed in on the Mac running `imsg`.

- Full Disk Access is required for the process context running OpenClaw/`imsg` (Messages DB access).

- Automation permission is required to send messages through Messages.app.

Permissions are granted per process context. If gateway runs headless (LaunchAgent/SSH), run a one-time interactive command in that same context to trigger prompts:Copy```
imsg chats --limit 1
# or
imsg send <handle> "test"

```

​Access control and routing

 DM policy Group policy + mentions Sessions and deterministic replies
`channels.imessage.dmPolicy` controls direct messages:

- `pairing` (default)

- `allowlist`

- `open` (requires `allowFrom` to include `"*"`)

- `disabled`

Allowlist field: `channels.imessage.allowFrom`.Allowlist entries can be handles or chat targets (`chat_id:*`, `chat_guid:*`, `chat_identifier:*`).`channels.imessage.groupPolicy` controls group handling:

- `allowlist` (default when configured)

- `open`

- `disabled`

Group sender allowlist: `channels.imessage.groupAllowFrom`.Runtime fallback: if `groupAllowFrom` is unset, iMessage group sender checks fall back to `allowFrom` when available.Mention gating for groups:

- iMessage has no native mention metadata

- mention detection uses regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`)

- with no configured patterns, mention gating cannot be enforced

Control commands from authorized senders can bypass mention gating in groups.

- DMs use direct routing; groups use group routing.

- With default `session.dmScope=main`, iMessage DMs collapse into the agent main session.

- Group sessions are isolated (`agent:<agentId>:imessage:group:<chat_id>`).

- Replies route back to iMessage using originating channel/target metadata.

Group-ish thread behavior:Some multi-participant iMessage threads can arrive with `is_group=false`.
If that `chat_id` is explicitly configured under `channels.imessage.groups`, OpenClaw treats it as group traffic (group gating + group session isolation).
​Deployment patterns
Dedicated bot macOS user (separate iMessage identity)

Use a dedicated Apple ID and macOS user so bot traffic is isolated from your personal Messages profile.Typical flow:

- Create/sign in a dedicated macOS user.

- Sign into Messages with the bot Apple ID in that user.

- Install `imsg` in that user.

- Create SSH wrapper so OpenClaw can run `imsg` in that user context.

- Point `channels.imessage.accounts.<id>.cliPath` and `.dbPath` to that user profile.

First run may require GUI approvals (Automation + Full Disk Access) in that bot user session.Remote Mac over Tailscale (example)

Common topology:

- gateway runs on Linux/VM

- iMessage + `imsg` runs on a Mac in your tailnet

- `cliPath` wrapper uses SSH to run `imsg`

- `remoteHost` enables SCP attachment fetches

Example:Copy```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}

```

Copy```
#!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"

```

Use SSH keys so both SSH and SCP are non-interactive.Multi-account pattern

iMessage supports per-account config under `channels.imessage.accounts`.Each account can override fields such as `cliPath`, `dbPath`, `allowFrom`, `groupPolicy`, `mediaMaxMb`, and history settings.
​Media, chunking, and delivery targets
Attachments and media

- inbound attachment ingestion is optional: `channels.imessage.includeAttachments`

- remote attachment paths can be fetched via SCP when `remoteHost` is set

- outbound media size uses `channels.imessage.mediaMaxMb` (default 16 MB)

Outbound chunking

- text chunk limit: `channels.imessage.textChunkLimit` (default 4000)

chunk mode: `channels.imessage.chunkMode`

- `length` (default)

- `newline` (paragraph-first splitting)

Addressing formats

Preferred explicit targets:

- `chat_id:123` (recommended for stable routing)

- `chat_guid:...`

- `chat_identifier:...`

Handle targets are also supported:

- `imessage:+1555...`

- `sms:+1555...`

- `user@example.com`

Copy```
imsg chats --limit 20

```

​Config writes
iMessage allows channel-initiated config writes by default (for `/config set|unset` when `commands.config: true`).
Disable:
Copy```
{
  channels: {
    imessage: {
      configWrites: false,
    },
  },
}

```

​Troubleshooting
imsg not found or RPC unsupported

Validate the binary and RPC support:Copy```
imsg rpc --help
openclaw channels status --probe

```

If probe reports RPC unsupported, update `imsg`.DMs are ignored

Check:

- `channels.imessage.dmPolicy`

- `channels.imessage.allowFrom`

- pairing approvals (`openclaw pairing list imessage`)

Group messages are ignored

Check:

- `channels.imessage.groupPolicy`

- `channels.imessage.groupAllowFrom`

- `channels.imessage.groups` allowlist behavior

- mention pattern configuration (`agents.list[].groupChat.mentionPatterns`)

Remote attachments fail

Check:

- `channels.imessage.remoteHost`

- SSH/SCP key auth from the gateway host

- remote path readability on the Mac running Messages

macOS permission prompts were missed

Re-run in an interactive GUI terminal in the same user/session context and approve prompts:Copy```
imsg chats --limit 1
imsg send <handle> "test"

```

Confirm Full Disk Access + Automation are granted for the process context that runs OpenClaw/`imsg`.
​Configuration reference pointers

- [Configuration reference - iMessage](/gateway/configuration-reference#imessage)

- [Gateway configuration](/gateway/configuration)

- [Pairing](/channels/pairing)

- [BlueBubbles](/channels/bluebubbles)

SignalMicrosoft Teams⌘I