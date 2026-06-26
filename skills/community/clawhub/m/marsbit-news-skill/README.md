# MarsBit OpenNews Skill

This skill provides blockchain news capabilities from `www.marsbit.io` /
`www.marsbit.co` for OpenClaw and other agent runtimes.

## What it does

After installation, the agent can use the hosted MarsBit MCP endpoint to:

1. Get latest news
2. Get news channels
3. Search news by keyword
4. Get news detail by ID
5. Get related news by ID
6. Get latest flash updates
7. Search flash updates by keyword

Default MCP endpoint:

`https://www.marsbit.co/api/mcp`

## Installation

### 1) Install via ClawHub (recommended)

Login first (recommended to avoid anonymous rate limits):

```bash
clawhub login
clawhub whoami
```

Install:

```bash
clawhub install domilin/marsbit-news-skill
```

Verify:

```bash
openclaw skills list
```

If you get `Rate limit exceeded` (429):

1. Ensure you are logged in
2. Wait 1-5 minutes and retry
3. Use the GitHub installation method below

### 2) Install from GitHub

```bash
git clone https://github.com/domilin/marsbit-news-skill /tmp/marsbit-news-skill
mkdir -p ~/.openclaw/skills/opennews
cp -R /tmp/marsbit-news-skill/openclaw-skill/opennews/* ~/.openclaw/skills/opennews/
openclaw skills list
```

## Files

1. `SKILL.md`: Skill definition and tool usage guide
2. `package.json`: Skill package metadata

## ClawHub page

`https://clawhub.ai/domilin/marsbit-news-skill`
