---
name: Feishu Integration
description: Feishu (飞书) integration - Send messages, manage groups, and automate workflows
homepage: https://github.com/lukaizj/feishu-integration-skill
tags:
  - productivity
  - integration
  - messaging
  - feishu
requires:
  env:
    - FEISHU_APP_ID
    - FEISHU_APP_SECRET
files:
  - feishu.py
---

# Feishu Integration (飞书集成)

Feishu (飞书) integration skill for OpenClaw. Send messages, manage groups, and automate workflows with Feishu.

## Capabilities

- Send text messages to chats
- Send rich interactive cards
- Create new chat groups
- List chat members
- Send scheduled messages
- Webhook notifications

## Setup

1. Create a Feishu application at https://open.feishu.cn/
2. Get App ID and App Secret from the application settings
3. Add required permissions:
   - `im:message:send_as_bot`
   - `im:chat:create`
   - `im:chat:update`
   - `im:message:p2p_msg:send`
4. Publish the app and get the Tenant Access Token
5. Configure environment variables

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FEISHU_APP_ID` | Yes | Your Feishu App ID |
| `FEISHU_APP_SECRET` | Yes | Your Feishu App Secret |
| `FEISHU_VERIFY_TOKEN` | No | Verification token for callbacks |

## Usage

### Send a message

```
Send a message "Hello from OpenClaw" to chat chat_id_123
Send a card message to chat chat_id_456 with title "Daily Report"
```

### Create a group

```
Create a new Feishu group named "Project Alpha"
Add user "zhangsan" to group "Project Alpha"
```

### List chats

```
List my Feishu chats
Show recent chat messages
```

## Message Types

This skill supports:
- **Text**: Plain text messages
- **Post**: Rich text messages with formatting
- **Interactive**: Cards with buttons, inputs, and actions

## Troubleshooting

- Ensure your app is published in the Feishu admin console
- Check that all required permissions are granted
- Verify the App ID and Secret are correct
- Make sure the app is added to required chats