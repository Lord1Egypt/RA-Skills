---
name: pipeworx-bored
description: Beat boredom with random activity suggestions — filter by type (education, social, cooking) or group size
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🎲"
    homepage: https://pipeworx.io/packs/bored
---

# Bored API

Nothing to do? This pack suggests activities to try — from solo hobbies to group outings. Filter by category or participant count, or just roll the dice and see what comes up.

## Tools

| Tool | Description |
|------|-------------|
| `random_activity` | Get a completely random activity suggestion |
| `activity_by_type` | Filter by category: education, recreational, social, diy, charity, cooking, relaxation, music, busywork |
| `activity_by_participants` | Suggest an activity for a specific group size (1 for solo, 2 for pairs, etc.) |

## Perfect for

- "I'm bored" moments — instant suggestion with no decision fatigue
- Team-building tools that need icebreaker activity ideas
- Daily challenge apps that rotate through activity types
- Onboarding flows that want to show a fun placeholder activity

## Quick example

Get a social activity for a group of 4:

```bash
curl -s -X POST https://gateway.pipeworx.io/bored/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"activity_by_participants","arguments":{"participants":4}}}'
```

```json
{
  "activity": "Start a book club",
  "type": "social",
  "participants": 4,
  "accessibility": 0.2,
  "price": 0.1
}
```

## Connect

```json
{
  "mcpServers": {
    "pipeworx-bored": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/bored/mcp"]
    }
  }
}
```
