---
name: gocreative-llm
description: LLM gateway & AI completion API for agents — call frontier models (Claude, GPT, DeepSeek) across cheap/pro/ultra tiers from one endpoint, pay-per-call in USDC via x402. No API key, no provider account, no monthly bill. Use when an agent needs an LLM completion, AI text generation, or model routing with pay-as-you-go pricing.
tags: [llm, ai, gateway, completion, claude, deepseek, inference, model-routing, pay-per-call, opus, sonnet]
author: gocreative
version: 1.0.0
license: MIT
---

# GoCreative LLM Gateway

> One endpoint, three tiers of frontier models, pay-per-call in USDC. No API key, no OpenAI/Anthropic account needed.

## When to use this
- An agent needs an **LLM completion** but has no provider key / wants to pay-as-you-go.
- An agent wants to **pick a price/quality tier** per task (cheap vs. frontier vs. top-end).

## How it's paid (x402 — no key, no signup)
HTTPS GET with the prompt URL-encoded in the path. First call returns **HTTP 402**; your OpenClaw wallet auto-pays the USDC fee (Base) and retries, returning the completion.

## Tiers (live endpoints)
| Call | Model tier | Price |
|---|---|---|
| `GET https://api.gocreativeai.com/v1/ai/ask/{prompt}` | Fast & cheap (DeepSeek-tier) | ~$0.02 |
| `GET https://api.gocreativeai.com/v1/ai/pro/{prompt}` | Frontier — Claude 4.5 Sonnet (`?model=` to override) | ~$0.08 |
| `GET https://api.gocreativeai.com/v1/ai/ultra/{prompt}` | Ultra — Claude Opus 4.6, top-end reasoning | ~$0.25 |

URL-encode the prompt. Example: `/v1/ai/ask/Summarize%20this%20contract%20in%203%20bullets`.

## Examples
- Cheap classification: `GET /v1/ai/ask/Classify%20sentiment%3A%20...` → ~$0.02.
- Frontier reasoning: `GET /v1/ai/pro/Draft%20a%20reply%20to...` → Claude Sonnet.
- Hard problem: `GET /v1/ai/ultra/Solve%20step%20by%20step...` → Claude Opus.

## Why GoCreative
Frontier models without an API key or a provider account — **one x402 endpoint, three tiers, pay only per call.** Drop it into any agent that needs an LLM and route by cost. Pairs with `gocreative-compliance`, `gocreative-enrichment`, and `gocreative-crypto` for a full agent back-office.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
