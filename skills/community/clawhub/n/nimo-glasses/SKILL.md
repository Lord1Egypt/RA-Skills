---
name: nimo-glasses
description: Connect AI smart glasses to OpenClaw via Companion App. Provides secure linkCode pairing, chat API, and SSE streaming for voice-controlled AI conversations through smart glasses.
---

# Nimo AI Glasses Plugin

Connect AI smart glasses to your OpenClaw Gateway for private, on-device AI voice conversations.

## What it does

- 🔗 **Secure pairing** — 6-digit one-time link code, auto-rotates after each pairing
- 💬 **Chat API** — `POST /nimo/chat` for text → AI reply
- 📡 **SSE streaming** — real-time token-by-token AI responses via `GET /nimo/events`
- 🔐 **Session tokens** — bearer-token auth with configurable expiry (default 60 days)
- ⚙️ **Configurable** — custom system prompt, max response length

## Installation

```bash
openclaw plugins install nimo-glasses
```

Then enable in your config:

```json5
{
  plugins: {
    entries: {
      "nimo-glasses": {
        enabled: true,
        config: {
          maxResponseLength: 300,
          systemPrompt: "You are an AI assistant in smart glasses. Be concise, no line breaks."
        }
      }
    }
  }
}
```

Restart the gateway:

```bash
openclaw gateway restart
```

## Usage

1. `GET /nimo/health` — get the current link code
2. `POST /nimo/pair` — exchange link code for a session token
3. `POST /nimo/chat` — send a message, get AI reply
4. `GET /nimo/events` — SSE stream for real-time responses

## Data Flow

```
Smart Glasses → STT → Companion App → OpenClaw Gateway (this plugin) → AI Agent → Reply → TTS → Glasses
```

Data does NOT pass through any third-party server. Direct connection to your own Gateway.
