---
name: openai-compatible-llm-gateway
description: OpenAI-compatible LLM gateway for AI agents — point your OpenAI client's base_url here and pay per call in USDC via x402 (Base or Solana) or a funded key. 17 models (GPT, Claude, Gemini, DeepSeek, Llama, Kimi, Qwen). No signup, no API key, no rate limits. The keyless pay-per-call alternative to OpenRouter and BlockRun.
tags: [llm-gateway, openai-compatible, chat-completions, ai, pay-per-call, x402, usdc, no-api-key, openrouter-alternative, blockrun-alternative, gpt, claude, gemini, deepseek]
author: gocreative
version: 1.0.0
license: MIT
---

# OpenAI-Compatible LLM Gateway

> Drop-in `base_url` for any OpenAI client. 17 models, pay-per-call in USDC, no API key, no signup.

## When to use this
- You want **frontier LLM completions** (GPT, Claude, Gemini, DeepSeek, Llama, Kimi, Qwen) without managing provider keys or accounts.
- You want to **pay per call in USDC** (x402, Base or Solana) instead of a subscription — or fund a key and pay from balance.
- You need a **drop-in OpenAI-compatible** endpoint your existing tools/SDKs already speak.

## Base URL
```
https://api.gocreativeai.com/v1
```

## Endpoints
- `POST /v1/chat/completions` — OpenAI-compatible chat completions. Send `{model, messages}`, get a standard `chat.completion` back. **$0.02 / call.** (Streaming not yet supported — set `stream: false`.)
- `GET /v1/models` — free. Lists every model the gateway routes to.
- Tiered shortcuts (URL-encode the prompt in the path):
  - `GET /v1/ai/eco/{prompt}` — cheapest, **$0.005**
  - `GET /v1/ai/ask/{prompt}` — standard, **$0.02**
  - `GET /v1/ai/pro/{prompt}` — frontier (Claude/GPT-5), **$0.08**
  - `GET /v1/ai/ultra/{prompt}` — top reasoning (Opus), **$0.25**

## How to pay (no signup either way)
1. **x402 (pay-per-call):** call the endpoint with an x402-enabled client; it returns HTTP 402 offering USDC on **Base or Solana**, your client pays, the call completes.
2. **Funded key:** fund a key and pass it as the OpenAI `api_key` (`Authorization: Bearer gck_...`).

## Drop-in example (OpenAI SDK)
```python
from openai import OpenAI
client = OpenAI(base_url="https://api.gocreativeai.com/v1", api_key="gck_<your-key>")
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Summarize this in one line: ..."}],
)
print(resp.choices[0].message.content)
```

## curl
```
curl -X POST https://api.gocreativeai.com/v1/chat/completions \
  -H "Authorization: Bearer gck_<your-key>" -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}]}'
```

## Models
17 models across tiers — GPT-5 / 5-mini / 5-nano, Claude Sonnet / Haiku / Opus, Gemini Flash / Pro, DeepSeek, Llama, Kimi, Qwen, GPT-OSS. Call `GET /v1/models` for the live list. Unknown model names map to a sensible default.

## Why this vs others
- **Keyless + pay-per-call** in USDC (Base + Solana) — no subscription, no account, no rate limits.
- **Bundled with 350+ data & compliance tools** on the same API (company enrichment, sanctions/KYB screening, SEC filings, crypto/DeFi, government data) — one `base_url` for LLM *and* real-world data.
