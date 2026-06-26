---
name: openclaw-cli-bridge-elvatis
description: Bridge local AI CLIs + web browser sessions (Grok, Gemini, Claude.ai, ChatGPT) into OpenClaw as model providers. Includes /cli-* slash commands for instant model switching and persistent browser profiles for all 4 web providers.
homepage: https://github.com/elvatis/openclaw-cli-bridge-elvatis
metadata:
  {
    "openclaw":
      {
        "emoji": "🌉",
        "requires": { "bins": ["openclaw", "claude", "gemini"] },
        "commands": ["/cli-sonnet", "/cli-opus", "/cli-haiku", "/cli-gemini", "/cli-gemini-flash", "/cli-gemini3"]
      }
  }
---

# OpenClaw CLI Bridge

Bridges locally installed AI CLIs + web browser sessions into OpenClaw as model providers. Four phases:

## Phase 1 — Codex Auth Bridge
Registers `openai-codex` provider from existing `~/.codex/auth.json` tokens. No re-login.

## Phase 2 — Request Proxy
Local OpenAI-compatible HTTP proxy (`127.0.0.1:31337`) routes vllm model calls to CLI subprocesses:
- `vllm/cli-gemini/gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-3-pro`
- `vllm/cli-claude/claude-sonnet-4-6` / `claude-opus-4-6` / `claude-haiku-4-5`
- `vllm/local-bitnet/bitnet-2b` → BitNet llama-server on 127.0.0.1:8082

Prompts go via stdin/tmpfile — never as CLI args (prevents `E2BIG` for long sessions).

## Phase 3 — Slash Commands
Six instant model-switch commands (authorized senders only):

| Command | Model |
|---|---|
| `/cli-sonnet` | `vllm/cli-claude/claude-sonnet-4-6` |
| `/cli-opus` | `vllm/cli-claude/claude-opus-4-6` |
| `/cli-haiku` | `vllm/cli-claude/claude-haiku-4-5` |
| `/cli-gemini` | `vllm/cli-gemini/gemini-2.5-pro` |
| `/cli-gemini-flash` | `vllm/cli-gemini/gemini-2.5-flash` |
| `/cli-gemini3` | `vllm/cli-gemini/gemini-3-pro` |
| `/cli-codex` | `openai-codex/gpt-5.3-codex` |
| `/cli-codex54` | `openai-codex/gpt-5.4` |
| `/cli-bitnet` | `vllm/local-bitnet/bitnet-2b` |
| `/cli-back` | Restore previous model |
| `/cli-test [model]` | Health check (no model switch) |

Each command uses staged switching by default (apply with `/cli-apply`).

## Phase 4 — Web Browser Providers
Persistent Chromium profiles for 4 web providers (no API key needed):
- **Grok** (`web-grok/*`): `/grok-login`, `/grok-status`, `/grok-logout`
- **Gemini** (`web-gemini/*`): `/gemini-login`, `/gemini-status`, `/gemini-logout`
- **Claude.ai** (`web-claude/*`): `/claude-login`, `/claude-status`, `/claude-logout`
- **ChatGPT** (`web-chatgpt/*`): `/chatgpt-login`, `/chatgpt-status`, `/chatgpt-logout`

Sessions survive gateway restarts. `/bridge-status` shows all 4 at a glance.

On gateway restart, if any session has expired, a **WhatsApp alert** is sent automatically with the exact `/xxx-login` commands needed — no guessing required.

**Browser health dashboard:** `http://127.0.0.1:31337/status` — live overview of all 4 providers, cookie expiry, and model list. Auto-refreshes every 30s.

## Setup

1. Enable plugin + restart gateway
2. (Optional) Register Codex auth: `openclaw models auth login --provider openai-codex`
3. Use `/cli-*` commands to switch models from any channel

See `README.md` for full configuration reference and architecture diagram.

**Version:** 2.8.1
