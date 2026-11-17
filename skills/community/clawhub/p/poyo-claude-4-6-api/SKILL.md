---
name: poyo-claude-4-6-api
description: Claude 4.6 Series Messages API on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use for `claude-sonnet-4-6`, `claude-opus-4-6`, Claude-compatible messages, tools, structured output, prompt cache settings, vision content blocks, streaming, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/claude-4-6-api","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Claude 4.6 Series Messages
## PoYo Links

- Model page: <https://poyo.ai/models/claude-4-6-api>
- API docs: <https://docs.poyo.ai/api-manual/chat-series/claude-messages>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Claude 4.6 Series requests on PoYo. It helps agents prepare Claude-compatible Messages API payloads, streaming calls, tool definitions, structured output settings, and server-side integration notes.

## Use When

- The user explicitly wants to use PoYo with Claude 4.6, `claude-sonnet-4-6`, `claude-opus-4-6`, or the PoYo Claude Messages API.
- The user asks for a PoYo request payload, server-side curl command, integration notes, streaming setup, tool-use payload, structured-output payload, or response parsing for this model family.
- The user has already chosen PoYo as the execution provider for a Claude 4.6 workflow.

## Model Selection

- `claude-sonnet-4-6`: use for Claude Sonnet 4.6 Messages API requests on PoYo.
- `claude-opus-4-6`: use when the user explicitly selects the Opus 4.6 variant.

## Key Inputs

- `model` is required and should be one of the supported Claude 4.6 model ids.
- `messages` is required and should contain `role` and `content`.
- `max_tokens` controls response length.
- `system` sets assistant behavior and can be a string or supported content blocks.
- `tools` and `tool_choice` configure tool use when the application can execute tools.
- `output_config` can request structured output when supported.
- `cache_control` can mark reusable prompt content when supported.
- `stream: true` requires streaming-aware client handling.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private user messages, system prompts, image content, tool inputs, or raw API key headers unless the user or product policy explicitly allows it.
- Do not use this skill for generic reasoning, coding, summarization, or chat unless the user explicitly wants a PoYo Claude 4.6 API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_claude_4_6_messages.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Claude Messages calls are synchronous unless streaming is enabled.

## Output Expectations

When helping with Claude 4.6 Series, include:

- chosen model id
- final payload or concise parameter summary
- synchronous or streaming handling
- system prompt, tools, structured output, and cache settings when relevant
- response parsing notes if the user needs integration code
