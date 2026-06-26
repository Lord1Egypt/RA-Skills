# HelloFresh Skill for OpenClaw

Interact with your HelloFresh meal subscription — discover recipes, manage selections, convert instructions to speech.

## Features

- **Recipe Discovery** — Browse available recipes for any week
- **Meal Selection** — Change your weekly meal selection
- **Cooking Instructions** — Text-to-speech for step-by-step guidance
- **Order History** — View past deliveries and preferences
- **AI Recommendations** — Smart recipe suggestions based on your history
- **Notifications** — Reminders before meal selection cutoff
- **Cloud Support** — Works locally or with Kernel.sh cloud browsers

## Installation

```bash
# Clone into your OpenClaw workspace skills
git clone https://github.com/YOUR_USERNAME/hellofresh-skill.git ~/.openclaw/workspace/skills/hellofresh

# Install dependencies
cd ~/.openclaw/workspace/skills/hellofresh
npm install
```

## Configuration

### Local Mode (Default)
Uses your browser via Chrome Extension Relay. No additional setup needed.

### Cloud Mode (Optional)
For running on remote servers, set environment variables:

```bash
export USE_KERNEL=true
export KERNEL_API_KEY=sk_your_kernel_api_key
```

Get your Kernel API key from https://dashboard.onkernel.com

## Commands

| Command | Description |
|---------|-------------|
| `/hello-fresh setup` | First-time setup |
| `/hello-fresh status` | Show subscription |
| `/hello-fresh discover [week]` | List recipes (this/next/last) |
| `/hello-fresh select` | Change meal selection |
| `/hello-fresh history` | View past orders |
| `/hello-fresh recommend` | AI recommendations |
| `/hello-fresh convert <recipe>` | Text-to-speech instructions |
| `/hello-fresh notify` | Check notifications |

## Requirements

- OpenClaw
- Browser (Chrome/Chromium) for local mode
- HelloFresh account

## License

MIT
