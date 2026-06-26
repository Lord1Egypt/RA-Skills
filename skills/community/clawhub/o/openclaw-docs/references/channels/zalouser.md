# Zalo Personal

Source: https://docs.openclaw.ai/channels/zalouser

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessaging platformsZalo PersonalGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Chat Channels
Messaging platforms
WhatsAppTelegramDiscordIRCSlackFeishuGoogle ChatMattermostSignaliMessageMicrosoft TeamsLINEMatrixZaloZalo Personal
Configuration
PairingGroup MessagesGroupsBroadcast GroupsChannel RoutingChannel Location ParsingChannel Troubleshooting
On this page
- [Zalo Personal (unofficial)](#zalo-personal-unofficial)
- [Plugin required](#plugin-required)
- [Prerequisite: zca-cli](#prerequisite-zca-cli)
- [Quick setup (beginner)](#quick-setup-beginner)
- [What it is](#what-it-is)
- [Naming](#naming)
- [Finding IDs (directory)](#finding-ids-directory)
- [Limits](#limits)
- [Access control (DMs)](#access-control-dms)
- [Group access (optional)](#group-access-optional)
- [Multi-account](#multi-account)
- [Troubleshooting](#troubleshooting)

​Zalo Personal (unofficial)
Status: experimental. This integration automates a **personal Zalo account** via `zca-cli`.

**Warning:** This is an unofficial integration and may result in account suspension/ban. Use at your own risk.

​Plugin required
Zalo Personal ships as a plugin and is not bundled with the core install.

- Install via CLI: `openclaw plugins install @openclaw/zalouser`

- Or from a source checkout: `openclaw plugins install ./extensions/zalouser`

- Details: [Plugins](/tools/plugin)

​Prerequisite: zca-cli
The Gateway machine must have the `zca` binary available in `PATH`.

- Verify: `zca --version`

- If missing, install zca-cli (see `extensions/zalouser/README.md` or the upstream zca-cli docs).

​Quick setup (beginner)

- Install the plugin (see above).

Login (QR, on the Gateway machine):

- `openclaw channels login --channel zalouser`

- Scan the QR code in the terminal with the Zalo mobile app.

- Enable the channel:

Copy```
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}

```

- Restart the Gateway (or finish onboarding).

- DM access defaults to pairing; approve the pairing code on first contact.

​What it is

- Uses `zca listen` to receive inbound messages.

- Uses `zca msg ...` to send replies (text/media/link).

- Designed for “personal account” use cases where Zalo Bot API is not available.

​Naming
Channel id is `zalouser` to make it explicit this automates a **personal Zalo user account** (unofficial). We keep `zalo` reserved for a potential future official Zalo API integration.
​Finding IDs (directory)
Use the directory CLI to discover peers/groups and their IDs:
Copy```
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"

```

​Limits

- Outbound text is chunked to ~2000 characters (Zalo client limits).

- Streaming is blocked by default.

​Access control (DMs)
`channels.zalouser.dmPolicy` supports: `pairing | allowlist | open | disabled` (default: `pairing`).
`channels.zalouser.allowFrom` accepts user IDs or names. The wizard resolves names to IDs via `zca friend find` when available.
Approve via:

- `openclaw pairing list zalouser`

- `openclaw pairing approve zalouser <code>`

​Group access (optional)

- Default: `channels.zalouser.groupPolicy = "open"` (groups allowed). Use `channels.defaults.groupPolicy` to override the default when unset.

Restrict to an allowlist with:

- `channels.zalouser.groupPolicy = "allowlist"`

- `channels.zalouser.groups` (keys are group IDs or names)

- Block all groups: `channels.zalouser.groupPolicy = "disabled"`.

- The configure wizard can prompt for group allowlists.

- On startup, OpenClaw resolves group/user names in allowlists to IDs and logs the mapping; unresolved entries are kept as typed.

Example:
Copy```
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}

```

​Multi-account
Accounts map to zca profiles. Example:
Copy```
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

​Troubleshooting
**`zca` not found:**

- Install zca-cli and ensure it’s on `PATH` for the Gateway process.

**Login doesn’t stick:**

- `openclaw channels status --probe`

- Re-login: `openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`

ZaloPairing⌘I