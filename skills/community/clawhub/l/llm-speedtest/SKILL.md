---
name: llm-speedtest
version: 1.0.0
description: "Ping major LLM providers in parallel and compare real API latency. Run with /ping"
metadata:
  category: utility
  capabilities:
    - api
  dependencies: []
  interface: shell
openclaw:
  emoji: "⚡"
  requires:
    env:
      - ANTHROPIC_API_KEY (optional)
      - OPENAI_API_KEY (optional)
      - GEMINI_API_KEY (optional)
      - MINIMAX_API_KEY (optional)
      - XAI_API_KEY (optional)
author:
  name: chapati23
---

# LLM Speedtest

Ping major LLM providers in parallel and compare real API latency (TTFT).

## When to Use

- User types `/ping` or asks about model latency/speed
- Comparing provider response times
- Checking if a specific provider is slow or down

## How It Works

Runs `scripts/ping.sh` which:

1. Retrieves API keys from `pass shared/` (users may need to adapt key sourcing for their setup)
2. Fires parallel `curl` requests to each provider with a minimal prompt ("hi", `max_tokens=1`)
3. Measures total round-trip time per provider
4. Sorts results by latency and displays with color badges

## Output Format

Results are sorted fastest-to-slowest with color badges:

- 🟢 **< 2s** — Fast
- 🟡 **2–5s** — Normal
- 🔴 **5–30s** — Slow
- ⚫ **30s** — Timeout

Example:
```
⚡ Model Latency — 14:32

🟢 `Gemini       412ms`
🟢 `GPT-4o       623ms`
🟢 `Sonnet       891ms`
🟡 `Grok        2104ms`
🟡 `MiniMax     3210ms`
🟡 `Opus        4102ms`

_real API latency (TTFT)_
```

## Models Tested

| Provider | Model |
|----------|-------|
| Anthropic | Claude Sonnet 4 |
| Anthropic | Claude Opus 4 |
| OpenAI | GPT-4o-mini |
| Google | Gemini 2.5 Flash |
| MiniMax | MiniMax-M1 |
| xAI | Grok 3 Mini Fast |

## Cost

~$0.0001 per run (1 token per model, cheapest tiers).

## Note

This skill uses `pass shared/` for API key retrieval. If you don't use `pass`, you'll need to adapt `scripts/ping.sh` to source keys from environment variables or another secret manager.
