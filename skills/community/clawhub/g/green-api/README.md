# GREEN-API WhatsApp Skill

OpenClaw skill for sending and receiving WhatsApp messages via [GREEN-API](https://green-api.com).

## What it does

Gives OpenClaw access to 35+ WhatsApp tools: messaging, file sharing, polls, contacts, groups, chat history, instance management, and more — all through the GREEN-API MCP gateway.

## Prerequisites

1. A GREEN-API account — sign up at [console.green-api.com](https://console.green-api.com)
2. A created and authorized instance (with QR code or phone number)
3. The GREEN-API MCP gateway server running (see below)

## Setup

### 1. Install the skill

```bash
openclaw skills install green-api-whatsapp
```

### 2. Connect the MCP server

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "mcpServers": {
    "green-api": {
      "url": "https://api.green-api.com/mcp"
    }
  }
}
```

The exact URL will be available in your [GREEN-API console](https://console.green-api.com).

### 3. Start chatting

Tell OpenClaw to connect your instance, then start messaging:

> "Connect WhatsApp instance 1234567 with token abc123, then send 'Hello!' to +7 987 654 3210"

## Links

- [GREEN-API Documentation](https://green-api.com/en/docs/)
- [GREEN-API Console](https://console.green-api.com)
