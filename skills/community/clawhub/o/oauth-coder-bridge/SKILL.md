---
name: oauth-coder-bridge
description: Routes OpenClaw Anthropic API calls through oauth-coder (Claude CLI with OAuth), no API key needed.
homepage: https://github.com/earlvanze/oauth-coder-bridge
---

# oauth-coder-bridge

Local HTTP bridge: OpenClaw → oauth-coder → real `claude` CLI (OAuth tokens, no API key).

**Upstream:** [codeninja/oauth-cli-coder](https://github.com/codeninja/oauth-cli-coder)

## Prerequisites

- `oauth-coder` installed and authenticated (`claude login`)
- Binary on PATH or set `OAUTH_CODER_BIN`

## Install & Run

```bash
bash scripts/setup.sh              # copies bridge, adds claude-cli provider to openclaw.json
python3 ~/.openclaw/scripts/oauth-coder-bridge.py &
# Or: systemctl --user enable --now oauth-coder-bridge
```

## Verify

```bash
curl http://127.0.0.1:8787/health  # → {"status":"ok"}
openclaw models set claude         # use alias
openclaw models set claude-cli/claude-opus-4-6  # or full path
```

## Models

**Opus:** `claude-opus-4-6`, `claude-opus-4-5`, `claude-opus-4-1`, `claude-opus-4-0`
**Sonnet:** `claude-sonnet-4-6`, `claude-sonnet-4-5`, `claude-sonnet-4-0`, `claude-3-7-sonnet-latest`, `claude-3-5-sonnet-latest`
**Haiku:** `claude-haiku-4-5`, `claude-3-5-haiku-latest`

All prefixed with `claude-cli/` (e.g. `claude-cli/claude-opus-4-6`).

## How It Works

```
OpenClaw → HTTP :8787 → oauth-coder-bridge → oauth-coder → claude CLI
```

Bridge translates Anthropic-messages JSON → `oauth-coder ask claude ...` subprocess calls.

## Config (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `OAUTH_CODER_BIN` | `$HOME/bin/oauth-coder` | Path to binary |
| `OAUTH_CODER_BRIDGE_PORT` | 8787 | Listen port |
| `OAUTH_CODER_BRIDGE_HOST` | 127.0.0.1 | Bind address |
| `OAUTH_CODER_BRIDGE_TIMEOUT` | 300 | Request timeout (s) |
| `OAUTH_CODER_BRIDGE_MAX_PROMPT` | 100000 | Max prompt length |
| `OAUTH_CODER_BRIDGE_LOG_FILE` | (empty) | Log file (stderr only if unset) |

## Security

- Binds localhost only
- Rate limited: 30 req/min per IP
- Prompts pass through to `claude` CLI subprocess
- If `LOG_FILE` is set, prompts/responses may be logged locally

## Troubleshooting

```bash
curl http://127.0.0.1:8787/health    # check bridge
which oauth-coder                     # check binary
claude login                          # re-auth
oauth-coder stop-all                  # clear stuck sessions
```

## Files

- `scripts/oauth-coder-bridge.py` — bridge server
- `scripts/setup.sh` — installer
- `scripts/update-openclaw-config.py` — config updater
- `references/oauth-coder-bridge.service` — systemd template

MIT License
