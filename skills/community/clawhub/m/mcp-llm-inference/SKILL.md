---
name: mcp-llm-inference
description: Anonymous LLM inference via L402 micropayments — chat completions, text generation, and model discovery. No API key, no signup, no KYC. Pay per request in sats. Use when agents need LLM access without accounts or identity.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
      env:
        - L402_API_BASE_URL
    emoji: 🧠
---

# LLM Inference (L402)

Anonymous LLM inference — pay per request with Lightning sats. No API key, no signup.

## Setup

```json
{
  "mcpServers": {
    "llm-inference": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-llm-inference"],
      "env": {
        "L402_API_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

## Tools

### `chat_completion`
Multi-turn chat with message history.

### `generate_text`
Single-prompt text generation.

### `list_models`
Discover available models and pricing.

## Payment

Powered by L402 micropayments over Lightning Network. Each request returns a Lightning invoice — pay it, get your response. ~10 sats per request.

## When to Use

- Agents needing LLM access without API key management
- Anonymous inference (no identity required)
- Pay-as-you-go without billing portals
- Agent-to-agent service consumption
