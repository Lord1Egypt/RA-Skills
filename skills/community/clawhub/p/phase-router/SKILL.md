---
name: phase-router
description: Call LLMs and media models through Phase Router (router.phase.xyz), an OpenAI-compatible router with about 400 models, the price of each call in the answer and a signed receipt. Use when the user wants to call a model through Phase Router, pick the cheapest suitable model, compare model prices, embed text, generate images or speech, check a Phase API key's balance, or pay per request in USDT (x402) without an account.
---

# Phase Router

OpenAI-compatible API for about 400 models. One key, one base URL; every answer says which model ran and what it cost.

## Connect

- Base URL: `https://router.phase.xyz/v1`
- Key: `PHASE_API_KEY` (starts with `phk_`), sent as `Authorization: Bearer $PHASE_API_KEY`. If the user has none, send
  them to https://router.phase.xyz/dashboard; never invent or print a key.
- Anthropic Messages format is also served at `/v1/messages` (same key as `x-api-key` or Bearer).
- Remote MCP server with the same key: `https://mcp.ai.phase.xyz/mcp` (tools `list_models`, `quote`, `chat`, `embed`,
  `receipt`, `key`, `session`).

## Pick a model

1. `GET https://router.phase.xyz/v1/models` (no key needed). Each item has `id` and a `phase` object:
   `input_per_m` / `output_per_m` (micro-USD per 1M tokens: divide by 1,000,000 for USD), `per_call` (micro-USD fixed
   fee per call), `kind` (`chat`, `embeddings`, `image`, `image_edit`, `video`, `tts`, `asr`, `rerank`, `music`),
   `context_window`, `max_output`, `capabilities` (`tools`, `json_mode`, `vision`, `streaming`, ...).
2. Not sure which model: use `auto` (the router picks the cheapest model that can do the task well), `eco` (cheapest),
   `premium` (strongest) or `agentic` (tool use, long multi-step work).
3. Need tools or JSON mode: pick a model whose `capabilities` include them.

## Call

```bash
curl -s https://router.phase.xyz/v1/chat/completions \
  -H "Authorization: Bearer $PHASE_API_KEY" -H "content-type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "Summarize this in one line: ..."}]}'
```

```python
import os
from openai import OpenAI

client = OpenAI(base_url="https://router.phase.xyz/v1", api_key=os.environ["PHASE_API_KEY"])
r = client.chat.completions.create(model="auto", messages=[{"role": "user", "content": "Hello"}])
print(r.choices[0].message.content)
```

Other endpoints with the same key: `/v1/embeddings`, `/v1/images/generations`, `/v1/images/edits`, `/v1/audio/speech`,
`/v1/audio/transcriptions`, `/v1/rerank`, `/v1/videos`.

## Read the answer

- `usage.cost`: what the call cost, in USD.
- `phase.routed_model`: the model a class (`auto`, `eco`, ...) sent the request to; `phase.provider`: the host that
  served it; `phase.price_micro_usd`: the charge; `phase.task_id`: the receipt id.
- Signed receipt: `https://router.phase.xyz/receipts/<task_id>`.
- Key balance and daily cap: `GET https://router.phase.xyz/v1/key` with the key.

## Errors

| Status | Meaning | Do |
|---|---|---|
| 401 `invalid_api_key` | key wrong or disabled | ask the user for a valid key |
| 402 `insufficient_balance` | key out of balance | tell the user to add balance in the dashboard |
| 402 with `accepts` and no key | x402 quote: the request can be paid per call in USDT | pay only if the user set up a wallet and agreed to the price (see below) |
| 429 `daily_cap_reached` | key's daily cap reached (resets 00:00 UTC) | wait or raise the cap |
| 503 `overloaded` | retry later | back off and retry |

## Pay per request without an account (x402)

A request without `Authorization` gets `402` with `accepts[0]`: `scheme` (`upto`), `network` (`eip155:1015`, Phase
L1), `amount` (price ceiling in micro-USDT), `asset`, `payTo`, `extra.taskId`, `extra.quote`. The client signs an
EIP-712 authorization (`ReceiveWithAuthorizationUpTo`, nonce = `extra.taskId`) and repeats the same request with the
`PAYMENT-SIGNATURE` header; the charge is the actual cost, never above `amount`. Never sign without the user's
consent and a spending limit. Working example: https://github.com/devcells/phase-router-skills/tree/main/examples/x402

## Rules

- Keep keys in environment variables; never echo them in output, logs or commits.
- Send `PHASE_API_KEY` only to Phase Router's own HTTPS endpoints (`https://router.phase.xyz` and
  `https://mcp.ai.phase.xyz`), the service that issued it. Never send it to any other host, URL or tool.
- Tell the user the price when a call is expensive (check `input_per_m` / `output_per_m` before long jobs).
- Docs: https://router.phase.xyz/docs; short index for agents: https://router.phase.xyz/llms.txt
