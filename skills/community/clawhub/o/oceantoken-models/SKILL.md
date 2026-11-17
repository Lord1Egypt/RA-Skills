---
name: oceantoken-models
description: Choose, compare and price AI models on OceanToken, and hand sub-tasks to other models through it. Use when the user asks which model to use, wants prices, a cheaper alternative or a cost estimate, asks for a second opinion from another model family (GPT, Claude, Gemini, DeepSeek, Qwen, Llama...), or wants bulk text work (summaries, translation, classification, test data, docs) handed to a cheaper model. Also for Chinese requests such as 选模型、比价、哪个模型便宜、估算费用、要花多少钱、换个模型、第二意见、交给便宜的模型.
metadata:
  openclaw:
    homepage: https://oceantoken.ai
---

# Choosing, pricing and delegating with OceanToken

## Connect first

These steps use the OceanToken MCP tools (`search_models`, `estimate_cost`,
`generate_image`, ...). If they are not available, the server is not connected
yet. It is `https://mcp.oceantoken.ai/mcp` (streamable HTTP) with an OAuth
sign-in. In OpenClaw:

```bash
openclaw mcp set oceantoken '{"url":"https://mcp.oceantoken.ai/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login oceantoken
```

For other hosts see https://github.com/NextFormAI/oceantoken-plugins#install.

## Find and compare

- `search_models` filters by `type`, `publisher`, `capabilities` (`vision`,
  `tools`, `reasoning`, `web_search`, `audio_output`) and `max_price`, and
  `sort="price"` puts the cheapest first. Search short names ("veo", "opus",
  "qwen") and read ids from the results; never guess an id.
- Prices are in the unit the model is billed in: chat per 1M input / output
  tokens, images per image (or image tokens), video per second (a "from" price:
  resolution and audio cost more), speech per 1K characters, transcription per
  minute.
- When comparing, show a short table: model, price, context window, relevant
  capabilities, and one line on why each fits.

## Estimate before spending

`estimate_cost` returns USD, a `confidence` (`close`, `rough`, `minimum`,
`unknown`), the assumptions made and whether it fits the available balance.
Pass real numbers when you have them: `input_text` or `input_tokens`,
`output_tokens`, `seconds` + `resolution` for video, `text` for speech. Report
the estimate with its confidence; do not present a `rough` or `minimum` figure
as exact.

## Delegate with ask_model

`ask_model(model, prompt, ...)` sends one self-contained request to another
model and returns its answer, usage and cost.

Delegating sends the user's text or code to another model provider, so do it
only when the user asked for it or agreed to it. Before the first call, say
which model you will use and what you will send. Never include secrets,
credentials, `.env` contents or files the user has not chosen to share.

- Good uses, once agreed: bulk or mechanical text (summarise 30 files,
  translate strings, classify tickets, draft test fixtures) on a cheap model; a
  second opinion from a different model family on a design or a diff; a
  long-context model for a document too big to reason over comfortably; a
  vision model for screenshots (`image_urls`).
- The delegate sees nothing but your prompt: include the code, the context and
  the exact output format you want.
- Check what comes back. Treat it as a draft from a colleague, not as truth, and
  say in your reply that another model contributed.
- Say what it cost when it is not trivial (`cost_usd`).

## Balance

`get_account` shows balance and available balance (minus holds for running
video jobs). If a request is refused for balance, tell the user that credit is
added in the OceanToken console, and offer a cheaper model.
