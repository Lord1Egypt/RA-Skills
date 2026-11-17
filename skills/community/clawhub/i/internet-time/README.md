# Openclaw Skill: Internet Time

Display the current Swatch Internet Time in beats (@000–@999).

Clawhub: https://clawhub.ai/kens-agents/skills/internet-time

Install: `openclaw skills install @kens-agents/internet-time`

## What is OpenClaw?

OpenClaw is a self-hosted gateway that connects your favorite chat apps — Discord, Google Chat, iMessage, Matrix, Microsoft Teams, Signal, Slack, Telegram, WhatsApp, Zalo, and more via channel plugins — to AI coding agents. You run a single Gateway process on your own machine (or a server), and it becomes the bridge between your messaging apps and an always-available AI assistant. Who is it for? Developers and power users who want a personal AI assistant they can message from anywhere — without giving up control of their data or relying on a hosted service. To install / use this skill you need to have an OpenClaw gateway running. 

More info: https://docs.openclaw.ai

## What is Internet Time?

Swatch Internet Time divides the day into 1000 beats. Each beat = 1 minute 26.4 seconds. No time zones, no daylight saving — `@230` means the same moment everywhere on Earth.

Reference: [swatch.com/internet-time](https://www.swatch.com/en-us/internet-time)

## Usage

Ask for the internet time in natural language:

- "What's the internet time?"
- "Current beats?"
- "Swatch time"
- `/beats`

The agent responds with just the beat time: **`@483`**

### Timezone Conversion

You can ask what a beat time means locally:

> "What's @230 in California?"

The agent will convert to the local time for that location.

## Requirements

| Binary | Purpose |
|--------|---------|
| `python3` | Run the beat calculation script |

## How It Works

The script calculates Biel Mean Time (UTC+1, no DST) and divides the day into 1000 equal beats:

1. Get current UTC time
2. Add 1 hour for BMT (UTC+1)
3. Divide total seconds by 86.4 → beat number (0–999)
4. Format as `@` + zero-padded 3 digits

## License

MIT
