---
name: poyo-claude-opus-4-7
description: Claude Opus 4.7 Messages API on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use for `claude-opus-4-7`, Claude-compatible messages, system prompts, multi-turn conversations, tools, structured output, prompt cache settings, vision content blocks, streaming, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/claude-opus-4-7","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Claude Opus 4.7 Messages
## PoYo Links

- Model page: <https://poyo.ai/models/claude-opus-4-7>
- API docs: <https://docs.poyo.ai/api-manual/chat-series/claude-messages>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Claude Opus 4.7 requests on PoYo. It helps agents prepare Claude-compatible Messages API payloads, streaming calls, tool definitions, structured output settings, and server-side integration notes.

## Use When

- The user explicitly wants to use PoYo with Claude Opus 4.7, `claude-opus-4-7`, or the PoYo Claude Messages API.
- The user asks for a PoYo request payload, server-side curl command, integration notes, streaming setup, tool-use payload, structured-output payload, or response parsing for this model.
- The user has already chosen PoYo as the execution provider for a Claude Opus 4.7 workflow.

## Model Selection

- `claude-opus-4-7`: use for Claude Opus 4.7 Messages API requests on PoYo.

## Key Inputs

- `model` is required and should be `claude-opus-4-7` for this skill.
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
- Do not use this skill for generic reasoning, coding, summarization, or chat unless the user explicitly wants a PoYo Claude Opus 4.7 API workflow.
- Do not make live API calls unless the user explicitly asks, confirms the payload should be sent to PoYo, and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_claude_opus_4_7_messages.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Claude Messages calls are synchronous unless streaming is enabled.

## Output Expectations

When helping with Claude Opus 4.7, include:

- chosen model id
- final payload or concise parameter summary
- synchronous or streaming handling
- system prompt, tools, structured output, and cache settings when relevant
- response parsing notes if the user needs integration code
