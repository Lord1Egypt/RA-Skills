---
name: poyo-claude-fable-5
description: Claude Fable 5 Messages API integration on PoYo / poyo.ai via `https://api.poyo.ai/v1/messages`; use when the user explicitly requests PoYo, `claude-fable-5`, or PoYo Messages API payloads involving content blocks, system prompts, tools, structured output, prompt caching controls, streaming, or server-side agent workflows.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/claude-fable-5","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Claude Fable 5 Messages

## PoYo Links

- Model page: <https://poyo.ai/models/claude-fable-5>
- API docs: <https://docs.poyo.ai/api-manual/chat-series/claude-messages>
- API key page: <https://poyo.ai/dashboard/api-key>

Use this skill for Claude Fable 5 requests through PoYo's Claude-compatible Messages API. It helps agents prepare messages, system instructions, content blocks, tool definitions, structured output settings, streaming calls, and server-side integration notes.

## Use When

- The user explicitly asks for PoYo, `claude-fable-5`, the PoYo Claude Messages API, or a PoYo `/v1/messages` integration.
- The user wants to use that PoYo integration for code assistance, research synthesis, document analysis, knowledge work, multi-turn chat, vision input, or agent tool planning.
- The workflow needs a server-side PoYo curl example, request payload, streaming handler, tool schema, or response parser.

## Model Selection

- `claude-fable-5`: use for Claude Fable 5 Messages API requests on PoYo.

## Key Inputs

- `model` is required and should be `claude-fable-5`.
- `messages` is required and should contain `role` and `content`.
- `max_tokens` controls the maximum response length.
- `system` sets assistant behavior and can use a string or documented content blocks.
- `tools` and `tool_choice` configure tool use when the application can safely execute tools.
- `output_config` can request structured output when supported.
- `cache_control` can mark reusable content when supported by the current API.
- `stream: true` requires streaming-aware client handling.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private messages, system prompts, image content, tool inputs, raw request bodies, or API key headers unless product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Execute returned tool calls only through an application-controlled allowlist with validated arguments.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_claude_fable_5_messages.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Messages calls are synchronous unless streaming is enabled.

## Output Expectations

When helping with Claude Fable 5, include:

- chosen model id
- final payload or concise parameter summary
- synchronous or streaming handling
- system prompt, content blocks, tools, structured output, and cache settings when relevant
- response parsing notes if the user needs integration code
