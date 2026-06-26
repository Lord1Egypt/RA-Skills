---
name: multi-account-config
description: Configure multiple messaging platform accounts for OpenClaw. Use when the user wants to add or configure additional accounts for Telegram, WhatsApp, Discord, or other supported channels. Triggers on requests like "configure multiple accounts", "add another telegram bot", "setup multi-account", "add work account", etc.
---

# Multi-Account Configuration

Guide users through configuring multiple accounts for messaging platforms in OpenClaw.

## Supported Platforms

- Telegram
- WhatsApp
- Discord
- Slack
- Signal
- Other OpenClaw-supported channels

## Workflow

### Step 1: Identify Platform

Ask the user which platform they want to configure:
> "你想配置哪个平台的多账号？支持的选项：Telegram、WhatsApp、Discord、Slack、Signal 等。"

### Step 2: Collect Account Information

For each account, collect:
1. **Account ID/Name** - A short identifier (e.g., "work", "personal", "friendA")
2. **Platform-specific credentials:**
   - Telegram: Bot Token (from @BotFather)
   - WhatsApp: Pairing code or existing credentials
   - Discord: Bot Token
   - Slack: Bot Token
   - Signal: Phone number

Suggest meaningful names based on use case:
- "work" - 工作相关
- "personal" - 个人使用
- "side-project" - 副业项目
- "family" - 家人群组

### Step 3: Get Current Config

Use `gateway config.get` to retrieve current configuration.

### Step 4: Build Updated Config

Structure the configuration following this pattern:

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "<platform>",
        "accountId": "<account-id>"
      }
    }
  ],
  "channels": {
    "<platform>": {
      "enabled": true,
      "accounts": {
        "<account-id>": {
          "name": "<Display Name>",
          "enabled": true,
          "dmPolicy": "allowlist",
          "allowFrom": ["<user-id>"],
          "botToken": "<token>",
          "groupPolicy": "open",
          "streaming": "block"
        }
      }
    }
  }
}
```

### Step 5: Apply Configuration

Use `gateway config.patch` to apply the new configuration.

### Step 6: Verify

Confirm the configuration was applied successfully and provide next steps.

## Configuration Schema Reference

### Bindings

Each account needs a binding entry:
```json
{
  "agentId": "main",
  "match": {
    "channel": "telegram",
    "accountId": "work"
  }
}
```

### Account Properties

| Property | Type | Description |
|----------|------|-------------|
| name | string | Display name for the account |
| enabled | boolean | Whether the account is active |
| dmPolicy | string | "allowlist", "blocklist", or "open" |
| allowFrom | array | List of allowed sender IDs (for allowlist) |
| botToken | string | Platform-specific token |
| groupPolicy | string | "open", "closed", or "admin-only" |
| streaming | string | "block" or "allow" |

## Example: Adding Telegram Work Account

User provides:
- Platform: Telegram
- Account name: work
- Bot Token: 123456:ABC-DEF...

Configuration to add:
```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "work"
      }
    }
  ],
  "channels": {
    "telegram": {
      "enabled": true,
      "accounts": {
        "work": {
          "name": "Work",
          "enabled": true,
          "dmPolicy": "allowlist",
          "allowFrom": ["USER_ID"],
          "botToken": "123456:ABC-DEF...",
          "groupPolicy": "open",
          "streaming": "block"
        }
      }
    }
  }
}
```

## Important Notes

1. **Preserve existing accounts** - When adding new accounts, merge with existing config
2. **Get user ID from context** - Use the current user's sender ID for allowFrom
3. **Validate tokens** - Ensure tokens are complete and properly formatted
4. **Restart required** - Configuration changes require gateway restart to take effect
5. **Security** - Never log or expose tokens in responses
