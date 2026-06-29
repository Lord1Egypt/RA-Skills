---
name: poyo-gemini-3-5-flash
description: Gemini 3.5 Flash chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions` and Gemini Native Format; use for `gemini-3.5-flash`, chat completions, native generateContent, streaming, system prompts, multimodal prompt structure, generation config, and server-side integration.
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/chat-series/gemini-native-format","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Gemini 3.5 Flash Chat

Use this skill for Gemini 3.5 Flash chat requests on PoYo. It helps agents prepare OpenAI-compatible chat payloads, Gemini Native Format payloads, streaming calls, and server-side integration notes.

## Use When

- The user mentions Gemini 3.5 Flash, `gemini-3.5-flash`, Gemini chat, Gemini Native Format, `generateContent`, or Gemini streaming.
- The task is text generation, coding assistance, summarization, structured responses, multimodal prompt planning, or chat integration.
- The workflow needs a server-side curl example or a production request payload for PoYo.

## Model Selection

- `gemini-3.5-flash`: use for Gemini 3.5 Flash requests on PoYo.

## Key Inputs

- For `/v1/chat/completions`, `model` and `messages` are required.
- For Gemini Native Format, `contents` is required and contains `role` plus `parts`.
- Use `generationConfig` for Gemini Native Format controls such as temperature, topP, topK, maxOutputTokens, and stopSequences.
- Use `safetySettings` only when the workflow explicitly needs Gemini safety threshold configuration.
- Use `stream: true` or `streamGenerateContent` only when the client can consume streaming responses.

## Security Rules

- Treat `POYO_API_KEY` as a secret.
- Keep PoYo API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repositories, logs, screenshots, or chat output.
- Do not log private user messages, system prompts, inline media data, or raw authorization headers unless the user or product policy explicitly allows it.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.

## Execution

- Read `references/api.md` for endpoint details, request fields, examples, and response notes.
- Use `scripts/submit_gemini_3_5_flash_chat.sh` only when the user wants to submit an OpenAI-compatible chat payload from a trusted shell.
- If the user needs Gemini Native Format, adapt the native example from `references/api.md`.
- Chat completions and native generateContent calls are synchronous unless streaming is enabled.

## Output Expectations

When helping with Gemini 3.5 Flash, include:

- chosen model id
- chosen endpoint style: OpenAI-compatible chat or Gemini Native Format
- final payload or concise parameter summary
- synchronous or streaming handling
- generation config and safety settings when relevant
- response parsing notes if the user needs integration code
