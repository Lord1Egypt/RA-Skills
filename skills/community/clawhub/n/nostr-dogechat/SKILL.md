---
name: nostr-dogechat
description: "Bridge to the DogeChat Nostr geohash chat network."
metadata: { "openclaw": { "emoji": "🐕" } }
---

# DogeChat Bridge

Use this skill to interact with decentralized chat rooms based on the user's location.

## Workflow
1. **Locate**: Identify the user's current Geohash (provided in `USER_CONTEXT`).
2. **Channel**: Use `#d0ge` for global chat or the specific Geohash for local chat.
3. **Identity**: You are acting as the user's agent (e.g., {{AGENT_NAME}}).

## Commands
- `node dogechat-bridge.js send --geohash <hash> --message "<text>"`

## Guardrails
- Respect the privacy of the user and others.
- Never share private keys or personal data.
- Stay in character as a helpful, witty agent.
- Answer questions and provide creative perspectives naturally.