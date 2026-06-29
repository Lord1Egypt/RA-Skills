---
name: poyo-deepseek-v4-chat
description: DeepSeek V4 chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions`; use for `deepseek-v4-flash`, `deepseek-v4-pro`, OpenAI-compatible chat payloads, system prompts, multi-turn messages, streaming chat, coding assistance, long-context analysis, and server-side chat integration.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/chat-series/chat-completions","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo DeepSeek V4 Chat

Use this skill for DeepSeek V4 chat completion requests on PoYo. It helps agents choose the Flash or Pro model id, prepare OpenAI-compatible chat payloads, choose synchronous or streaming response handling, and keep API keys server-side.

## Use When

- The user mentions DeepSeek V4, `deepseek-v4-flash`, `deepseek-v4-pro`, DeepSeek chat, OpenAI-compatible chat, system prompts, assistant messages, or streaming chat.
- The task is text generation, coding assistance, reasoning, summarization, structured assistant output, or long-context assistant workflow planning.
- The workflow needs a server-side curl example or a production chat payload for PoYo.

## Model Selection

- `deepseek-v4-flash`: use for DeepSeek V4 Flash chat requests.
- `deepseek-v4-pro`: use for DeepSeek V4 Pro chat requests.

## Key Inputs

- `model` is required and should be `deepseek-v4-flash` or `deepseek-v4-pro`.
- `messages` is required and should contain `role` and `content` pairs.
- `temperature`, `top_p`, `max_tokens`, penalties, `stop`, and `n` are optional chat controls.
- `stream: true` requests SSE streaming and requires streaming-aware client handling.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private user messages, system prompts, or raw authorization headers unless the user or product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_deepseek_v4_chat.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Chat completions are synchronous unless streaming is enabled.

## Output Expectations

When helping with DeepSeek V4 chat, include:

- chosen model id
- whether Flash or Pro is selected
- final payload or concise parameter summary
- synchronous or streaming handling
- any system prompt constraints
- response parsing notes if the user needs integration code
