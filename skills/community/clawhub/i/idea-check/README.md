# idea-check

Pre-build reality check for your project ideas. Scans GitHub, Hacker News, npm, PyPI, and Product Hunt to tell you if something already exists before you waste time building it.

## Requirements

- `mcporter` — MCP tool server CLI (`npm install -g mcporter`)
- `uvx` (uv) — runs the MCP server process

## Setup

1. Install mcporter and register the MCP server:
   ```bash
   npm install -g mcporter
   mcporter config add idea-reality --command "uvx idea-reality-mcp"
   ```

2. Install the skill:
   ```bash
   clawhub install idea-check
   ```

## Usage

> "Has anyone built a CLI for tracking habits?"

> "Deep check: AI code review tool"

> "I want to build a Telegram bot for meal planning — does this exist?"

## Install

```bash
clawhub install idea-check
```
