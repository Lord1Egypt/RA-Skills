---
name: poyo-gpt-5-2-chat
description: GPT-5.2 chat completions on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions`; use for `gpt-5.2`, OpenAI-compatible chat payloads, system prompts, multi-turn messages, streaming chat, max_tokens, and server-side chat integration.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/chat-series/chat-completions","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo GPT-5.2 Chat Completions

Use this skill for `gpt-5.2` chat completion jobs on PoYo. It helps agents prepare OpenAI-compatible chat payloads, choose synchronous or streaming response handling, and keep API keys server-side.

## Use When

- The user mentions PoYo chat, `gpt-5.2`, chat completions, OpenAI-compatible chat, system prompts, assistant messages, or streaming chat.
- The task is text generation, planning, copy, summarization, structured assistant output, or agent workflow text.
- The workflow needs a server-side curl example or a production chat payload for PoYo.

## Model Selection

- `gpt-5.2`: use for PoYo chat completion requests through `/v1/chat/completions`.

## Key Inputs

- `model` is required and should be `gpt-5.2` for this skill.
- `messages` is required and should contain `role` and `content` pairs.
- `temperature`, `top_p`, `max_tokens`, penalties, `stop`, and `n` are optional chat controls.
- `stream: true` requests SSE streaming and requires streaming-aware client handling.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private user messages unless the user or product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_gpt_5_2_chat.sh` only when the user wants to submit a prepared JSON payload from a trusted shell.
- If the user only needs a curl example, adapt one from `references/api.md`.
- Unlike PoYo media tasks, chat completions are synchronous unless streaming is enabled.

## Output Expectations

When helping with GPT-5.2 chat, include:

- chosen model id
- final payload or concise parameter summary
- synchronous or streaming handling
- any system prompt constraints
- response parsing notes if the user needs integration code
