---
name: openclaw-msteams-bot-elvatis
description: Microsoft Teams connector plugin for OpenClaw Gateway. Bridges Teams channels to OpenClaw AI sessions with per-channel system prompts, model configuration, and Azure Bot Framework authentication. Supports channels, group chats, and direct messages.
---

# openclaw-msteams-bot-elvatis

Microsoft Teams connector plugin for [OpenClaw Gateway](https://github.com/openclaw/openclaw).

## What it does

Connects Microsoft Teams channels to your OpenClaw AI agent. Each Teams channel gets its own session with a configurable system prompt and model. Supports channels, group chats, and 1:1 direct messages.

## Features

- Per-channel AI personas (Accounting, Marketing, HR, General)
- Per-channel model selection
- Azure Bot Framework authentication (JWT verified)
- Single-tenant and multi-tenant Azure AD support
- Typing indicators while the agent is processing
- WebSocket-based agent communication (direct connection to OpenClaw Gateway)
- Native vision support: images sent as base64 via WebSocket
- Message splitting for long responses (Teams 28KB limit)
- Full deployment guide included (Azure setup, Apache reverse proxy, Teams App Manifest)

## Requirements

- OpenClaw Gateway
- Microsoft Azure account (Bot registration)
- Domain with HTTPS for the messaging endpoint
- Node.js 18+

## Quick start

See `README.md` for the full 9-step deployment guide covering:
Azure Bot registration, Teams channel activation, server setup, Apache reverse proxy, manifest creation, and Teams App deployment.

**Version:** 0.1.3
