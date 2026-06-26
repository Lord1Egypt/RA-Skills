---
name: Notifications Engine
description: Multi-channel notification delivery with customizable templates, email and SMS sending, and full delivery logging — built for AI agents.
author: MCF Agentic
version: 1.0.0
tags: [notifications, email, sms, templates, messaging, delivery, alerts]
pricing: x402 (USDC on Base)
gateway: https://gateway.mcfagentic.com
---

# Notifications Engine

Let your AI agent send notifications across email and SMS with a single API call. Define reusable templates per event type and channel, then fire notifications without worrying about provider integration or formatting. Every delivery is logged so your agent can verify what was sent, when, and whether it landed. Simple, reliable, multi-channel messaging that keeps humans in the loop when your agent needs to reach them.

## Authentication

All endpoints require x402 payment (USDC on Base L2). Send a request without payment to receive pricing info in the 402 response.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | /api/notifications/templates | $0.001 | List notification templates |
| PUT | /api/notifications/templates/:event_type/:channel | $0.01 | Update template |
| POST | /api/notifications/notifications/send | $0.05 | Send notification (email/SMS) |
| GET | /api/notifications/notifications/log | $0.001 | Notification delivery log |
