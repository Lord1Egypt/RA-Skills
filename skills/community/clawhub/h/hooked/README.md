# Hooked Video API Skill

Give your AI agent the power to create professional videos. Works with Claude Code, Cursor, Windsurf, Codex, OpenClaw, and any agent that supports skills.

## What It Does

This skill teaches your AI agent to:

- **Create videos** from scripts, prompts, or slideshows
- **Browse avatars** — 50+ realistic AI presenters with lip-sync
- **Select voices** — hundreds of options in 30+ languages
- **Discover trends** — see what's viral on TikTok, YouTube, Instagram
- **Track progress** — check rendering status and get download URLs
- **Create UGC ads** — authentic product ads with AI presenters

## Installation

### Claude Code / Cursor / Windsurf

```bash
npx skills add hooked-so/hooked-skill
```

### OpenClaw

```bash
clawhub install hooked-so/hooked-skill
```

### Manual

Download `SKILL.md` and place it in your agent's skills directory:
- Claude Code: `.claude/skills/`
- Cursor: `.cursor/skills/`

## Setup

1. **Get your API key** at [hooked.so](https://hooked.so/settings/api)
2. **Set the environment variable:**
   ```bash
   export HOOKED_API_KEY="your_api_key_here"
   ```
3. **Start creating** — ask your agent to make a video!

## Example Prompts

Once installed, try these:

- "Create a 30-second product video for my fitness app. Use an energetic female avatar."
- "Make a TikTok slideshow with 5 productivity tips."
- "What avatars do you have? I need someone for tech reviews."
- "What's trending on TikTok in the cooking niche? Create a video based on the top trend."
- "Check the status of my last video and download it when ready."

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /v1/project/create/script-to-video` | Create video from script with avatar |
| `POST /v1/project/create/prompt-to-video` | AI generates script and video |
| `POST /v1/project/create/tiktok-slideshow` | Create TikTok-style slideshow |
| `POST /v1/project/create/ugc-ads` | Create UGC-style ad |
| `GET /v1/avatar/list` | List available avatars |
| `GET /v1/voice/list` | List available voices |
| `GET /v1/music/list` | List background music |
| `GET /v1/video/{id}` | Check video status |
| `GET /v1/video/list` | List recent videos |
| `GET /v1/trends/videos` | Get trending content |

## Pricing

- **Pro:** $39/month — 150 credits (~30 videos)
- **Premium:** $79/month — 350 credits (~70 videos)
- **Ultra:** $149/month — 750 credits (~150 videos)

The skill itself is free and open source. You only pay for video generation.

## Links

- [API Documentation](https://docs.hooked.so)
- [Dashboard](https://hooked.so)
- [MCP Server](https://hooked.so/mcp) — for Claude Desktop, ChatGPT
- [OpenClaw Integration](https://hooked.so/openclaw)

## License

MIT
