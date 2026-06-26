# memory-core-plus

> Enhanced workspace memory with auto-recall and auto-capture for OpenClaw.

## What It Does

`memory-core-plus` is an OpenClaw plugin that extends the built-in `memory-core` with two automated hooks:

- **Auto-Recall** — Before each LLM turn, semantically searches workspace memory and injects relevant memories into the prompt context.
- **Auto-Capture** — After each agent run, extracts durable facts, preferences, and decisions from the conversation and persists them to memory files.

Together they form a closed-loop memory system: information captured from past conversations is automatically surfaced when contextually relevant in future interactions.

## Install

```bash
openclaw plugins install memory-core-plus
openclaw gateway restart
```

Auto-Recall and Auto-Capture are both enabled by default.

## Configuration

```jsonc
{
  "plugins": {
    "entries": {
      "memory-core-plus": {
        "enabled": true,
        "config": {
          "autoRecall": true,
          "autoCapture": true
        }
      }
    },
    "slots": {
      "memory": "memory-core-plus"
    }
  }
}
```

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `autoRecall` | boolean | true | Enable automatic memory recall before each agent turn |
| `autoRecallMaxResults` | number | 5 | Maximum memories to inject per turn |
| `autoRecallMinPromptLength` | number | 5 | Minimum prompt length (chars) to trigger recall |
| `autoCapture` | boolean | true | Enable automatic memory capture after each agent run |
| `autoCaptureMaxMessages` | number | 10 | Maximum recent messages to analyze for capture |

## Uninstall

```bash
openclaw plugins uninstall memory-core-plus
openclaw gateway restart
```

The gateway automatically falls back to the built-in `memory-core`.

## Links

- [GitHub](https://github.com/aloong-planet/openclaw-memory-core-plus)
- [npm](https://www.npmjs.com/package/memory-core-plus)
