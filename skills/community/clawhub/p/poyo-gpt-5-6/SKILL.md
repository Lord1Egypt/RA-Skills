---
name: poyo-gpt-5-6
description: GPT-5.6 Responses API integration on PoYo / poyo.ai via `https://api.poyo.ai/v1/responses`; use for `gpt-5-6-sol`, `gpt-5-6-terra`, `gpt-5-6-luna`, text and structured input, tools, reasoning settings, streaming, previous response continuation, and server-side agent workflows.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/gpt-5-6","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo GPT-5.6 Responses API

## PoYo Links

- Model page: <https://poyo.ai/models/gpt-5-6>
- API docs: <https://docs.poyo.ai/api-manual/chat-series/responses>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for GPT-5.6 requests through PoYo's OpenAI-compatible Responses API. It helps agents select an exact GPT-5.6 model id, prepare text or structured input, configure tools and reasoning, handle complete or streaming responses, and keep API keys server-side.

## Use When

- The user mentions GPT-5.6, `gpt-5-6-sol`, `gpt-5-6-terra`, `gpt-5-6-luna`, PoYo Responses API, tool use, reasoning controls, or streaming responses.
- The task is coding assistance, research, text generation, structured input, multimodal input, tool-assisted work, or a multi-turn response workflow.
- The workflow needs a server-side curl example or a production `/v1/responses` payload for PoYo.

## Model Selection

- `gpt-5-6-sol`: use when the user explicitly selects the Sol variant.
- `gpt-5-6-terra`: use when the user explicitly selects the Terra variant.
- `gpt-5-6-luna`: use when the user explicitly selects the Luna variant.
- If the user does not select a variant, show the three ids and ask which current PoYo option matches the workload instead of silently substituting one.

## Key Inputs

- `model` is required and must be one of the documented GPT-5.6 ids above.
- `input` is required and can be plain text or documented structured input items.
- `instructions` can set high-level behavior when supported.
- `tools` and `tool_choice` configure tool use when the application can safely execute tool calls.
- `reasoning`, `text`, and `max_output_tokens` configure supported reasoning and output behavior.
- `previous_response_id` can continue a supported response chain.
- `stream: true` requests SSE output and requires streaming-aware client handling.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private input, tool arguments, uploaded media, raw request bodies, or authorization headers unless product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Execute returned tool calls only through an application-controlled allowlist with validated arguments.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response parsing notes.
- Use `scripts/submit_gpt_5_6_responses.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Responses are synchronous unless streaming or another documented asynchronous behavior is enabled.

## Output Expectations

When helping with GPT-5.6, include:

- chosen exact model id
- final payload or concise parameter summary
- complete or streaming response handling
- tool, reasoning, structured-output, and continuation settings when relevant
- response parsing notes if the user needs integration code
