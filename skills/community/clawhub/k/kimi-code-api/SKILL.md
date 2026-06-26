---
name: kimi-code-api
description: One-click setup to use Kimi K2.5 (Kimi Code) as your coding model in OpenClaw and Claude Code CLI. Kimi Code is Anthropic Messages API compatible — swap the base URL and you're running. Use when you want a cost-effective coding LLM, need to set up Kimi K2.5 in OpenClaw, or want to run Claude Code CLI with Kimi as the backend. Triggers on "kimi code", "kimi k2.5", "kimi openclaw", "kimi claude code", "openclaw kimi", "coding model setup".
---

# Kimi Code API — OpenClaw + Claude Code Integration

Kimi Code (K2.5) is **Anthropic Messages API compatible**. One config change and your OpenClaw runs Claude Code on Kimi's backend.

## Quick Start: Get Your API Key

1. Open [Kimi Code Console](https://www.kimi.com/code/console)
2. Create an API Key → format: `sk-kimi-...`

## Setup 1: OpenClaw — Add Kimi as a Provider + Model

Add to your `openclaw.json` under `providers` and `models`:

```jsonc
// In providers:
{
  "id": "kimi",
  "type": "anthropic",          // Kimi speaks Anthropic protocol
  "baseUrl": "https://api.kimi.com/coding",
  "apiKey": "sk-kimi-..."
}

// In models (or agents.defaults.models):
{
  "kimi/kimi-k2.5": {
    "alias": "Kimi K2.5",
    "params": {}
  }
}
```

Then use it anywhere in OpenClaw:
- Set as agent model: `"model": "kimi/kimi-k2.5"`
- Switch in chat: `/model kimi/kimi-k2.5`
- Use as default for a specific agent

## Setup 2: Claude Code CLI — Direct

```bash
export ANTHROPIC_BASE_URL="https://api.kimi.com/coding"
export ANTHROPIC_API_KEY="sk-kimi-..."

# Interactive
claude

# One-shot
claude --print "Refactor this function to use async/await"
```

Claude Code auto-appends `/v1/messages` to the base URL. No other changes needed.

## Setup 3: OpenClaw Spawns Claude Code with Kimi

In OpenClaw, spawn a Claude Code (ACP) session that uses Kimi as the backend:

```bash
# In your agent config or via sessions_spawn:
sessions_spawn(
    runtime="acp",
    task="Your coding task here",
    env={
        "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding",
        "ANTHROPIC_API_KEY": "sk-kimi-..."
    }
)
```

Or configure it globally in `openclaw.json` so every ACP spawn uses Kimi by default.

## API Reference

| Property | Value |
|----------|-------|
| Base URL | `https://api.kimi.com/coding` |
| Messages endpoint | `https://api.kimi.com/coding/v1/messages` |
| Auth header | `x-api-key: sk-kimi-...` |
| Version header | `anthropic-version: 2023-06-01` |
| Model (request) | `kimi-k2.5` |
| Model (response) | `kimi-for-coding` |
| Protocol | Anthropic Messages API |
| Streaming | `"stream": true` → SSE |

## Raw Call Examples

### curl

```bash
curl -s https://api.kimi.com/coding/v1/messages \
  -H "x-api-key: sk-kimi-..." \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"kimi-k2.5","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'
```

### Python (no dependencies)

```python
import json, urllib.request

req = urllib.request.Request(
    "https://api.kimi.com/coding/v1/messages",
    data=json.dumps({
        "model": "kimi-k2.5",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Hello"}]
    }).encode(),
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk-kimi-...",
        "anthropic-version": "2023-06-01",
    },
)
with urllib.request.urlopen(req, timeout=120) as resp:
    print(json.loads(resp.read())["content"][0]["text"])
```

## Gotchas

- **Model name mismatch**: Request sends `kimi-k2.5`, response returns `kimi-for-coding`. Don't assert on the response model field.
- **Anthropic format only**: `/v1/messages` works. `/v1/chat/completions` (OpenAI format) returns 404.
- **`api.moonshot.cn` ≠ Kimi Code**: That's the general Moonshot API — different product, different auth.
- **Timeout**: Set ≥120s for complex prompts.
- **Provider type**: Always `"type": "anthropic"` in OpenClaw config — Kimi speaks Anthropic, not OpenAI.
