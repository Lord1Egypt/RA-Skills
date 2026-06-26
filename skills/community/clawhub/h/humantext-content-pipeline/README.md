# humantext Content Pipeline — OpenClaw Skill

> Detect AI-generated content and humanize it to sound natural. Write → Detect → Humanize → Verify.

## What It Does

This skill turns your OpenClaw agent into a content quality pipeline:

1. **Write** — AI generates a draft on your topic (or you paste existing text)
2. **Detect** — Checks the AI detection score (**free**, no credits used)
3. **Humanize** — If the score is high, transforms the text to sound natural
4. **Verify** — Confirms the humanized text passes AI detection (**free**)

Uses the [humantext.pro](https://humantext.pro) MCP server for detection and humanization.

## Install

### Option 1: ClawHub (recommended)

```bash
clawhub install humantext-content-pipeline
```

### Option 2: Manual

Copy the `SKILL.md` file into your OpenClaw skills directory.

## Setup

### 1. Get Your API Key

Sign up at [humantext.pro](https://humantext.pro) and generate your API key at [humantext.pro/api](https://humantext.pro/api).

Requires an active subscription (starting at $7.99/mo). Detection is free, humanization uses word credits.

### 2. Configure MCP Server

Add to your MCP config (`.claude/mcp.json`, `.cursor/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "humantext": {
      "command": "npx",
      "args": ["-y", "@humantext/mcp-server"],
      "env": {
        "HUMANTEXT_API_KEY": "htpro_your_key_here"
      }
    }
  }
}
```

### 3. Use It

```
> Write a blog post about remote work benefits, then check and humanize it

> Check if this text sounds AI-generated: [paste text]

> Humanize this essay in academic tone: [paste text]
```

## Credits

| Plan | Price | Monthly Credits |
|------|-------|----------------|
| Basic | $7.99/mo | 5,000 words |
| Pro | $19.99/mo | 15,000 words |
| Ultra | $39.99/mo | 30,000 words |

- **AI Detection**: Always free
- **Humanization**: Uses word credits (1 word = 1 credit)
- **Word packs**: $1.99/1K words (never expire)

Start with a [free trial](https://humantext.pro/pricing).

## Publishing to ClawHub

```bash
clawhub login
clawhub publish ./openclaw-skill \
  --slug humantext-content-pipeline \
  --name "Content Quality Pipeline" \
  --version 1.0.0 \
  --changelog "Initial release"
```

Or fork [github.com/openclaw/clawhub](https://github.com/openclaw/clawhub), add the skill folder, and open a PR.

## Links

- [humantext.pro](https://humantext.pro) — Main website
- [API Dashboard](https://humantext.pro/api) — Get API key
- [API Docs](https://humantext.pro/api/docs) — Swagger documentation
- [MCP Server (NPM)](https://www.npmjs.com/package/@humantext/mcp-server) — MCP package
- [Pricing](https://humantext.pro/pricing) — Plans & pricing

## License

MIT
