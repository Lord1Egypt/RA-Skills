# NanoGPT API — Key Reference

Source: https://docs.nano-gpt.com/introduction

## Overview
NanoGPT API provides text, image, and video generation via any AI model through a unified OpenAI-compatible API. Supports verifiably private TEE (Trusted Execution Environment) models.

Base URL: `https://nano-gpt.com/api/v1`
Alternative domains: `ai.bitcoin.com`, `bcashgpt.com`, `cake.nano-gpt.com`

## Main Endpoints
- `POST /api/v1/chat/completions` — OpenAI-compatible chat generation. Supports streaming via SSE.
- `POST /api/v1/models` — List available models (basic mode, no auth required)
- `POST /api/v1/models?detailed=true` — Detailed model info including pricing
- `GET /api/subscription/v1/models` — Subscription-only models
- `GET /api/paid/v1/models` — Paid/premium models only
- `GET /api/subscription/v1/usage` — Subscription usage (daily/monthly limits)
- `POST /api/check-balance` — Account balance (USD + Nano)

## Auth
- Format: `sk-nano-<uuid>` (new keys)
- Headers: `Authorization: Bearer <key>` or `x-api-key: <key>`

## Model ID Format
- `provider/model-id` e.g., `openai/gpt-5.2`, `anthropic/claude-opus-4.6`, `google/gemini-3-flash-preview`

## Capabilities (detailed model info)
`vision`, `reasoning`, `tool_calling`, `parallel_tool_calls`, `structured_output`, `pdf_upload`

## Pricing fields per model (detailed mode)
- `pricing.prompt` — $/million input tokens
- `pricing.completion` — $/million output tokens
- `pricing.unit` — always `per_million_tokens`
- `context_length` — max input tokens
- `max_output_tokens` — max output tokens
