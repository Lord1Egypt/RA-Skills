# 🌐 Browser Use — OpenClaw Skill

Autonomous browser automation for AI agents. Built for [OpenClaw](https://openclaw.ai).

## What it does

Two complementary tools in one skill:

| Tool | Best for | How it works |
|------|----------|-------------|
| **agent-browser** | Step-by-step control, scraping, form filling | CLI Playwright — you drive each action |
| **browser-use** | Complex autonomous tasks | Python agent that decides actions itself |

## Quick Start

### Install

```bash
# From your OpenClaw skill directory
bash scripts/install.sh
```

Installs: Chromium, Xvfb, agent-browser (npm), browser-use Python venv + dependencies.

### agent-browser (CLI)

```bash
# Open a page
agent-browser open "https://example.com"

# Get interactive elements
agent-browser snapshot -i

# Interact using @refs from snapshot
agent-browser click @e3
agent-browser fill @e2 "search query"

# Extract data
agent-browser get text @e1

# Done
agent-browser close
```

### browser-use (Autonomous Agent)

```bash
# Set your API key
export ANTHROPIC_API_KEY="sk-..."
# or
export OPENAI_API_KEY="sk-..."

# Run autonomous task
browser-use-agent "Go to news.ycombinator.com and find the top 3 AI-related posts"
```

## Features

- **Headless by default** — works on servers, no GUI needed
- **Session management** — multiple parallel browser sessions
- **State persistence** — save/load cookies and auth state
- **Screenshot capture** — full page or element screenshots
- **Dual model support** — works with Anthropic (Claude) or OpenAI (GPT)
- **Xvfb fallback** — auto-detects display, uses virtual framebuffer when needed

## Requirements

- Linux (Ubuntu 22.04/24.04)
- Node.js 18+
- Python 3.10+
- Chromium

## Known Limitations

- Google/Bing block headless browsers (CAPTCHA) → use DuckDuckGo or `web_search` instead
- `@refs` change on every page load — always re-snapshot after navigation
- Use `fill` (not `type`) for input fields — it clears first

## Skill Structure

```
browser-use/
├── SKILL.md                        # OpenClaw skill instructions
├── scripts/
│   ├── install.sh                  # Idempotent installer
│   └── browser-use-agent.sh        # Autonomous agent wrapper
└── references/
    └── browser-workflow.md         # Detailed workflow guide
```

## License

MIT

## Links

- [OpenClaw](https://openclaw.ai) — AI agent gateway
- [ClawdHub](https://clawhub.ai) — Skill marketplace
- [agent-browser](https://www.npmjs.com/package/agent-browser) — CLI tool
- [browser-use](https://github.com/browser-use/browser-use) — Python library
