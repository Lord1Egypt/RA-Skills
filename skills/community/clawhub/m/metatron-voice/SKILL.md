---
name: metatron-voice
description: >
  Discord standup and meeting intelligence workflow for OpenClaw. Use when the
  user needs help configuring, operating, or troubleshooting Metatron Voice for
  Discord voice capture, transcription, meeting summaries, Jira task approval,
  and Confluence handoff.
homepage: https://github.com/toomij99/discord-voice
metadata:
  clawdbot:
    emoji: "🎙️"
    config:
      requiredEnv: []
      stateDirs:
        - ".openclaw/workspace/meetings"
      example: |
        {
          "plugins": {
            "entries": {
              "metatron-voice": {
                "enabled": true,
                "config": {
                  "meetingsDir": "/home/youruser/.openclaw/workspace/meetings",
                  "jiraProjectKey": "MYPROJECT",
                  "transcriptionProvider": "whisper-local",
                  "whisperModel": "base",
                  "sidecarBaseUrl": "http://127.0.0.1:8765"
                }
              }
            }
          }
        }
---

# Metatron Voice Skill

Metatron Voice is an OpenClaw plugin for Discord standups and voice meetings.

It extends the existing OpenClaw Discord integration with a meeting workflow that:

- records Discord voice conversations
- transcribes meeting audio
- generates meeting summaries
- extracts Jira task candidates
- supports approval in Discord before Jira push

## What It Owns

- plugin configuration guidance
- command usage guidance
- operator troubleshooting
- meeting artifact inspection
- Discord-first standup workflow guidance

## What It Does Not Replace

- OpenClaw's existing Discord bot identity
- OpenClaw's configured summary model
- OpenClaw's Jira integration
- OpenClaw's Confluence integration

## Config Shape

Use:

```json
{
  "plugins": {
    "entries": {
      "metatron-voice": {
        "enabled": true,
        "config": {
          "meetingsDir": "/home/youruser/.openclaw/workspace/meetings",
          "jiraProjectKey": "MYPROJECT",
          "transcriptionProvider": "whisper-local",
          "whisperModel": "base",
          "sidecarBaseUrl": "http://127.0.0.1:8765"
        }
      }
    }
  }
}
```

## Discord Workflow

Typical flow:

1. Team joins a Discord voice channel.
2. Someone brings OpenClaw/Metatron into the channel.
3. Start the meeting with `/recordstart`.
4. Stop the meeting with `/recordstop`.
5. Review the summary with `/voicesummary`.
6. Review candidate tasks with `/createtasks`.
7. Approve tasks with `/approvetasks 1 2` or `/approvetasks all`.
8. Push approved tasks with `/pushjira`.

## Notes

- This repository contains the OpenClaw-native plugin at the repository root.
- The sidecar worker lives under `sidecar/`.
- The older Python prototype under `metatron-voice/` is kept as migration reference.
