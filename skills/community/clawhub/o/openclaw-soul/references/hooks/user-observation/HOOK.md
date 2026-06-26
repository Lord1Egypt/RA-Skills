---
name: user-observation
description: "Automatically observes user communication patterns for dynamic personality adjustment"
homepage: https://github.com/openclaw/openclaw-soul
metadata:
  openclaw:
    emoji: "👁️"
    events: ["agent_end"]
    export: "default"
---

# User Observation Hook

Automatically observes and records user communication patterns during the first 10 conversations to enable dynamic personality adjustment.

## What It Does

- Listens for `agent_end` events (after each conversation)
- Analyzes user messages for communication patterns
- Records observations to `memory/metadata/user-observation.json`
- Triggers personality proposal when observation period completes (10 conversations)

## Observation Dimensions

1. **Message Length**: short / medium / long
2. **Tone**: formal / casual / mixed
3. **Emotion**: rational / emotional / balanced
4. **Task Types**: technical / creative / life / mixed
5. **Interaction Frequency**: high / medium / low

## Data Structure

```json
{
  "observation_count": 0,
  "observation_period": 10,
  "patterns": {
    "message_length": "unknown",
    "tone": "unknown",
    "emotion": "unknown",
    "task_types": [],
    "interaction_frequency": "unknown"
  },
  "examples": [],
  "ready_for_proposal": false,
  "proposal_delivered": false,
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

## Requirements

- Node.js
- OpenClaw workspace initialized

## Configuration

No configuration needed. The hook is automatically enabled when installed.
