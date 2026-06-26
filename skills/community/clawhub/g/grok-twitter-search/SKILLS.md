# My Skills Index

Personal skill collection for OpenClaw.

---

## Custom Skills (User-Installed)

| Skill | Source | API | Description |
|-------|--------|-----|-------------|
| **grok-twitter-search** | workspace/skills | Grok (xAI) | Real-time Twitter/X search with AI |
| **opentwitter** | ~/.openclaw/skills | 6551 API | Twitter data (profiles, tweets, followers) |
| **opennews** | ~/.openclaw/skills | 6551 API | Crypto news search with AI ratings |

---

## System Skills (Built-in)

Located in: `/opt/homebrew/lib/node_modules/openclaw/skills/`

### Communication
- **discord** - Discord integration
- **slack** - Slack integration
- **telegram** - Telegram integration (in gateway)
- **imsg** - iMessage
- **signal** - Signal

### Productivity
- **notion** - Notion integration
- **obsidian** - Obsidian vault
- **apple-notes** - Apple Notes
- **bear-notes** - Bear Notes
- **things-mac** - Things.app
- **trello** - Trello

### Development
- **github** - GitHub operations
- **gh-issues** - GitHub Issues
- **session-logs** - Session log analysis
- **coding-agent** - Coding assistance

### Media & AI
- **weather** - Weather data
- **sag** - ElevenLabs TTS voice
- **openai-image-gen** - DALL-E image generation
- **openai-whisper** - Whisper transcription
- **summarize** - Content summarization

### Hardware & IoT
- **openhue** - Philips Hue
- **sonoscli** - Sonos speakers
- **spotify-player** - Spotify control

### Other
- **healthcheck** - Security hardening
- **skill-creator** - Create new skills
- **model-usage** - Usage tracking
- **nano-pdf** - PDF operations
- **video-frames** - Video frame extraction

---

## Setup Notes

- `TWITTER_TOKEN` and `OPENNEWS_TOKEN` configured in `env.*`
- `XAI_API_KEY` needed for grok-twitter-search
- System skills available by default

## Adding New Skills

When installing a new skill:
1. Copy to appropriate location (~/.openclaw/skills or workspace/skills)
2. Add entry to this index
3. Configure required env variables if needed

## Skill Locations

- System skills: `/opt/homebrew/lib/node_modules/openclaw/skills/`
- User skills: `~/.openclaw/skills/`
- Workspace skills: `~/.openclaw/workspace/skills/`

---

*Total: 3 custom + 52 system = 55 skills available*