# oauth-coder-bridge

HTTP bridge that enables OpenClaw to use [oauth-coder](https://github.com/codeninja/oauth-cli-coder) for Claude Code access.

**Upstream project:** [codeninja/oauth-cli-coder](https://github.com/codeninja/oauth-cli-coder)

## Overview

This OpenClaw skill creates a local HTTP server that translates between:
- **Input:** Anthropic-messages API format (from OpenClaw)
- **Output:** oauth-coder CLI calls → real `claude` binary

Why this matters: From Anthropic's perspective, requests come from the official CLI tool with legitimate OAuth tokens — no API keys needed.

## Installation

Via ClawHub:
```bash
clawhub install oauth-coder-bridge
```

Manual:
```bash
git clone https://github.com/earlvanze/oauth-coder-bridge.git ~/.openclaw/workspace/skills/oauth-coder-bridge
cd ~/.openclaw/workspace/skills/oauth-coder-bridge
bash scripts/setup.sh
```

## Usage

```bash
# Start bridge
python3 ~/.openclaw/scripts/oauth-coder-bridge.py &

# Test
curl http://127.0.0.1:8787/health

# Set OpenClaw model
openclaw models set claude-cli/claude-opus-4-6
# or use alias:
openclaw models set claude
```

## How It Works

```
OpenClaw ──HTTP──▶ oauth-coder-bridge ──subprocess──▶ oauth-coder ──tmux──▶ claude CLI
     │                                                    │
     └────────────────── Anthropic API format ────────────┘
```

## Security Notes

- Prompts are passed to the `oauth-coder`/`claude` CLI subprocess
- Bridge binds to localhost only (127.0.0.1)
- Rate limited: 30 requests/minute per IP
- `OAUTH_CODER_BIN` auto-detected from PATH or `$HOME/bin/oauth-coder`

## License

MIT
