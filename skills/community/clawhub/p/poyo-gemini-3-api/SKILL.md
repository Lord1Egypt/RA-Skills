---
name: poyo-gemini-3-api
description: Gemini 3 Series chat on PoYo / poyo.ai via `https://api.poyo.ai/v1/chat/completions` and Gemini Native Format; use for `gemini-3-flash-preview`, `gemini-3-pro-preview`, `gemini-3.1-pro-preview`, chat completions, native generateContent, streaming, multimodal prompt structure, generation config, and server-side integration.
metadata: {"openclaw":{"homepage":"https://poyo.ai/models/gemini-3-api","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---

# PoYo Gemini 3 Series Chat
## PoYo Links

- Model page: <https://poyo.ai/models/gemini-3-api>
- API docs: <https://docs.poyo.ai/api-manual/chat-series/gemini-native-format>
- API key page: <https://poyo.ai/dashboard/api-key>


Use this skill for Gemini 3 Series chat requests on PoYo. It helps agents prepare OpenAI-compatible chat payloads, Gemini Native Format payloads, streaming calls, multimodal prompt structures, and server-side integration notes.

## Use When

- The user mentions Gemini 3, Gemini 3 Series, `gemini-3-flash-preview`, `gemini-3-pro-preview`, `gemini-3.1-pro-preview`, Gemini Native Format, `generateContent`, or Gemini streaming.
- The task is text generation, coding assistance, summarization, structured responses, multimodal prompt planning, or chat integration.
- The workflow needs a server-side curl example or a production request payload for PoYo.

## Model Selection

- `gemini-3-flash-preview`: use for faster Gemini 3 chat and coding requests.
- `gemini-3-pro-preview`: use for harder reasoning, analysis, or planning requests.
- `gemini-3.1-pro-preview`: use when the user explicitly asks for Gemini 3.1 Pro Preview.

## Key Inputs

- For `/v1/chat/completions`, `model` and `messages` are required.
- For Gemini Native Format, `contents` is required and contains `role` plus `parts`.
- Use `generationConfig` for Gemini Native Format controls such as temperature, topP, maxOutputTokens, and stopSequences.
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
- Use `scripts/submit_gemini_3_api_chat.sh` only when the user wants to submit an OpenAI-compatible chat payload from a trusted shell.
- If the user needs Gemini Native Format, adapt the native example from `references/api.md`.
- Chat completions and native generateContent calls are synchronous unless streaming is enabled.

## Output Expectations

When helping with Gemini 3 Series, include:

- chosen model id
- chosen endpoint style: OpenAI-compatible chat or Gemini Native Format
- final payload or concise parameter summary
- synchronous or streaming handling
- generation config and safety settings when relevant
- response parsing notes if the user needs integration code
