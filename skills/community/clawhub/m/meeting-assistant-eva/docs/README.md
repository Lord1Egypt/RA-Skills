# Meeting Assistant — Developer Documentation

AI-powered meeting bot that joins Google Meet / Zoom as a participant, captures audio and chat, provides real-time transcription, and lets you interact with a Claude AI agent directly through the meeting chat.

## Table of Contents

- [Architecture Overview](architecture.md)
- [Setup & Installation](setup.md)
- [Agent Usage Guide](agent-usage.md)
- [API Reference](api-reference.md)
- [Troubleshooting](troubleshooting.md)

## Quick Start

```bash
# 1. Start infrastructure
cd skills/meeting-assistant
docker compose -f <compose-file> up -d

# 2. Open a Google Meet and share the link with the agent
# 3. Agent joins and you can chat with it inside the meeting
```

## Current Status (as of 2026-03-14)

| Feature | Status | Notes |
|---|---|---|
| Google Meet join | ✅ Working | Bot joins as browser participant |
| Zoom join | ❌ Not working | `vexa-lite` image lacks proprietary Zoom SDK binaries |
| Chat send/receive | ✅ Working | Full UTF-8 Chinese/English support |
| Participant detection | ✅ Working | Bot can see participant list in real-time |
| Audio recording | ✅ Working | WAV files recorded per session |
| Microphone transcription | ✅ Working (pipeline verified) | Requires active mic audio; screen share audio not captured |
| Screen share video capture | ❌ Not available | Vexa only captures audio, not video frames |
| Bot screen share (output) | ✅ Available | Bot can present images/URLs/HTML to meeting |
| Claude AI chat replies | ✅ Implemented | Responds to questions, mentions, `?` messages |
| Meeting summary | ✅ Implemented | Generated post-meeting with Claude |

## Project Structure

```
meeting-assistant/
├── config.json              # Runtime configuration
├── docker-compose.yml       # Vexa infrastructure (source of truth)
├── SKILL.md                 # Claude Code skill descriptor
├── docs/                    # This documentation
│   ├── README.md
│   ├── architecture.md
│   ├── setup.md
│   ├── agent-usage.md
│   ├── api-reference.md
│   └── troubleshooting.md
├── scripts/
│   ├── meeting_bot.py       # Vexa API wrapper + AI assistant loop
│   ├── claude_client.py     # Claude API integration
│   ├── agent_tool.py        # High-level tool interface for Claude Code
│   ├── launch.py            # One-click startup script
│   ├── whisper_proxy.py     # HTTP proxy: rewrites model=default → correct name
│   ├── audio_capture.py     # Local audio capture (non-bot mode)
│   ├── transcribe.py        # Whisper transcription utilities
│   └── meeting_analyzer.py  # Analysis utilities
├── recordings/              # Session data (audio, screenshots, transcripts)
└── references/              # Integration guides
```
