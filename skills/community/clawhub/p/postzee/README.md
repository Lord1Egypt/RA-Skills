# Postzee Skill

AI-powered social media studio. Generate stunning images and videos with AI, optimize prompts automatically, and post to 30+ social networks — all from your AI agent.

## Features

- **15+ AI image models** (GPT Image 2, Recraft V4, Nano Banana, Ideogram V3, FLUX, and more)
- **20+ AI video models** (Veo 3.1, Sora 2, Kling, Luma Ray, Seedance, and more)
- **Smart prompt optimizer** — transforms simple descriptions into professional-grade prompts
- **30+ social networks** — Instagram, TikTok, YouTube, LinkedIn, X, Facebook, Pinterest, and more
- **Platform-aware** — automatically selects the right aspect ratio for each platform

## Installation

### Claude Code

```bash
gh skill install Zee-Labs/postzee-skill
```

Or manually:

```bash
mkdir -p ~/.claude/skills/postzee
curl -o ~/.claude/skills/postzee/SKILL.md https://raw.githubusercontent.com/Zee-Labs/postzee-skill/main/SKILL.md
```

### OpenClaw

```bash
clawhub install postzee
```

## Setup

After installation, tell your agent:

> "Configure Postzee with my API key: pk_your_key_here"

Get your API key at [dashboard.postzee.app/settings](https://dashboard.postzee.app/settings).

The agent will configure the MCP connection automatically.

## Usage Examples

```
"Generate a professional photo of a coffee shop"
"Create a video of ocean waves for Instagram Reels"
"Generate and post to all my channels"
"Create a TikTok video about productivity tips"
"Post this text to LinkedIn and X"
```

## Requirements

- A [Postzee](https://postzee.app) account (free or paid)
- AI credits for media generation (starting at $2 for 2,000 credits)
- At least one connected social media channel (for posting)

## Links

- [Postzee App](https://dashboard.postzee.app)
- [Documentation](https://docs.postzee.app)
- [Buy Credits](https://dashboard.postzee.app/credits)
- [Connect Channels](https://dashboard.postzee.app/channels)

## License

MIT
