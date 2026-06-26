# PaperBox

Upload AI-generated HTML games, apps, or generative art to [PaperBox](https://paperbox-beta.vercel.app) and get a shareable link. When your OpenClaw agent creates an HTML game, app, or art project, this skill publishes it via the PaperBox API and returns a live URL to view and share. You can also [explore others' projects](https://paperbox-beta.vercel.app/explore) on PaperBox.

## What It Does

1. Agent builds an HTML game, app, or generative art in the workspace
2. Agent POSTs the HTML to the PaperBox Games API
3. Agent returns the `shareableUrl` in chat (Telegram, WhatsApp, etc.)
4. User clicks the link to view — no account needed

## Requirements

- **PaperBox API key** — [Log in](https://paperbox-beta.vercel.app/login) (create a profile if needed), then go to Profile settings to generate your API key
- **Network** — Skill needs outbound HTTP to POST to the PaperBox API

## How to Use

1. Install the skill: `clawhub install paperbox`
2. Add your API key to `openclaw.json` under `skills.entries.paperbox.apiKey`
3. When your agent creates an HTML game, app, or art, say "share this to PaperBox" or "upload to PaperBox"

The agent will POST the HTML and reply with the shareable link.

## Permission: network

This skill requests `network:outbound` to send the HTML content to the PaperBox API at `https://paperbox-beta.vercel.app/api/games`. No other endpoints or network access are used. The skill does not read external data; it only uploads.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Check `openclaw.json` → `skills.entries.paperbox.apiKey` |
| 400 Bad request | Missing title/description or invalid HTML | Ensure htmlContent is valid, complete HTML |
| 413 Payload too large | HTML exceeds 2 MB | Minify CSS/JS, remove unused assets |
| 500 Server error | PaperBox backend issue | Retry; if it persists, check PaperBox status |

## License

MIT
