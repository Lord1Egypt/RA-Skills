---
name: DingTalk Integration
description: DingTalk (钉钉) integration - Send messages, create groups, and automate DingTalk workflows
homepage: https://github.com/lukaizj/dingtalk-integration-skill
tags:
  - productivity
  - integration
  - messaging
  - dingtalk
  - chinese
requires:
  env:
    - DINGTALK_APP_ID
    - DINGTALK_APP_SECRET
files:
  - dingtalk.py
---

# DingTalk Integration (钉钉集成)

DingTalk (钉钉) integration skill for OpenClaw. Send messages, manage groups, and automate workflows with DingTalk.

## Capabilities

- Send text messages to chats
- Send rich interactive cards
- Create new chat groups
- List chat members
- Send webhook notifications
- Handle incoming callbacks

## Setup

1. Create a DingTalk mini app at https://open.dingtalk.com/
2. Get App ID and App Secret from the application settings
3. Add required permissions
4. Configure environment variables

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DINGTALK_APP_ID` | Yes | Your DingTalk App ID |
| `DINGTALK_APP_SECRET` | Yes | Your DingTalk App Secret |
| `DINGTALK_AGENT_ID` | Yes | Your DingTalk Agent ID |

## Usage

### Send a message

```
Send a message "Hello from OpenClaw" to user user123
Send a card message to chat chat_id_456
```

### Create a group

```
Create a new DingTalk group named "Project Alpha"
Add user "zhangsan" to group "Project Alpha"
```

### List chats

```
List my DingTalk chats
Show recent chat messages
```

## Message Types

This skill supports:
- **Text**: Plain text messages
- **Markdown**: Markdown formatted messages
- **Interactive**: Cards with buttons, inputs, and actions

## Troubleshooting

- Ensure your app is published in the DingTalk admin console
- Check that all required permissions are granted
- Verify the App ID and Secret are correct
- Make sure the app is added to required chats