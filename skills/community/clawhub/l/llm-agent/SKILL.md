---
name: llm-agent
description: >
  Build a chat, reasoning, or tool-calling agent on top of Runware-hosted LLMs.
  Use when the user says "make an agent that can call my functions", "let the
  model use these tools", "wire up an LLM over my API", "chat assistant with
  function calling", "give the model access to my database/search", or wants
  multi-step reasoning that runs the user's own code. Covers the OpenAI-compatible
  chat-completions + tool-calling loop, not the imageInference task shape.
---

# LLM agent

Build a conversational or agentic LLM over your own functions using Runware-hosted models. The model reasons, decides when to call the tools you define, reads what they return, and answers with that data in hand. Runware exposes an **OpenAI-compatible** endpoint, so this is the standard chat-completions + tool-calling format, not the `imageInference` task shape the image skills use.

## Inputs to collect

- **The job:** plain chat/reasoning, or tool-calling over the user's own functions.
- **The tools** (if agentic): each function's name, what it does, its arguments, and how the user runs it. The model never touches the systems directly. It only sees the schemas you hand it and the JSON they return.
- **The system prompt:** the agent's role and how eagerly it should act ("gather context before acting" vs "act immediately").
- **Constraints:** latency/cost target, context-window needs, whether reasoning depth matters.

## Models

Address by **AIR**. Confirm each is `live` and inspect its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale pick.

- **Default flagship: Gemini 3.1 Pro** (`google:gemini@3.1-pro`). Strongest reasoning and instruction-following, ~1M-token context. Best general agent brain.
- **Claude Opus 4.8** (`anthropic:claude@opus-4.8`). Premium reasoning and long-horizon tool use.
- **Claude Sonnet 4.6** (`anthropic:claude@sonnet-4.6`). Fast, cheaper Claude tier for high-volume or latency-sensitive agents.
- **Kimi K2.6** (slug `moonshotai-kimi-k2-6`, AIR `moonshotai:kimi@k2.6`). Open frontier model built for long-horizon, tool-rich agentic workflows. The tool-calling guide is grounded on it.
- **Qwen3.5-397B** (`alibaba:qwen@3.5-397b`). Large MoE reasoner with ultra-long context, strong on coding and agent tasks.

Route by sub-task, not by brand: pick reasoning depth and context window for the job, then drop to a faster tier for cheap or high-volume calls. All five carry `io:text-to-text`.

## Workflow

This is text, not media, so it runs over the OpenAI-compatible endpoint, **not** `imageInference`.

1. **Point an OpenAI client at Runware.** Base URL `https://api.runware.ai/v1`, your Runware API key, and set `model` to the AIR (or slug). Existing OpenAI agent code and frameworks work unchanged. See the platform endpoint docs at `/docs/platform/openai`.
2. **Describe each tool as a JSON schema** under `tools`: `{ "type": "function", "function": { name, description, parameters } }`. Constrain arguments tightly (`enum`, `required`).
3. **Send the conversation** (`messages` with `system` + `user`) plus `tools`. Set `tool_choice` (default `auto`).
4. **Run the loop.** Read `response.choices[0].message`. If `finish_reason` is `tool_calls`, the assistant `content` is null and calls live in `message.tool_calls`. For each call: parse `function.arguments` (a JSON **string**, not an object), run the function, and append one `tool` message whose `tool_call_id` matches the call's `id`. Append the assistant message too. Repeat until the model returns no tool calls (`finish_reason: "stop"`).
5. **Bound the loop.** Cap iterations and stop with a clear error at the cap. Do not rely on the model to always finish on its own.

See `references/examples.md` for worked request/response recipes: a basic chat completion, a single tool-call loop, and parallel tool calls in OpenAI chat-completions format.

## Technique

- **One call answers one question. A loop answers a task.** The model often calls more tools after seeing the first results. The whole protocol is: send the conversation, append whatever comes back, repeat until no more tool calls. The round that a single call can't reach is the model reading earlier results and choosing a new action from them.
- **Three details carry the round-trip.** A `tool_calls` finish means there is no text to show yet. `arguments` is a JSON-encoded string you must parse. Your `tool` reply's `tool_call_id` must equal the call's `id`, and that pairing is how the model matches your result to its request.
- **Echo every tool call back into history.** Append both the assistant message that requested the call and your `tool` reply. Dropping the assistant message breaks the `tool_call_id` pairing and the next request errors.
- **Return errors as tool results, not exceptions.** On a tool failure send `{ "error": "..." }` back as the `tool` message so the model can read it and adjust. A thrown exception just ends the loop.
- **Parallel tool calls come back in one message.** When the model needs several independent pieces of information, it returns multiple entries in one `tool_calls` array instead of one round at a time. The loop already handles this: iterate every entry, append one `tool` message per call. Because each result is matched by its own `tool_call_id`, you can run independent calls concurrently and append results in any order.
- **Set the action threshold in the system prompt.** Whether the model gathers context before acting or acts immediately is shaped by lines like "inspect health and logs before taking action." Tighten or loosen that to match the autonomy you want.
- **Design tools the model can use well.** Name and description are a tool's entire interface. Name functions like API endpoints (`get_service_health`, `search_logs`), not `handler` or `doStuff`. Treat the description as instructions for choosing between tools mid-conversation. Return compact JSON objects with named fields, not prose or large blobs. Keep the set small: a handful of well-scoped tools beats a large overlapping catalog.

## Parameters that matter

- `model`: the AIR (or slug). Confirm it's `live` first.
- `messages`: the conversation. Keep stable parts (system prompt + tool defs) as a fixed prefix to maximize Runware's prompt cache. Watch `usage.prompt_tokens_details.cached_tokens` climb across rounds on long conversations.
- `tools`: array of function schemas. `enum` and `required` are the difference between a clean call and a malformed one.
- `tool_choice`: `"auto"` (default, model decides), `"none"` (text only, no tools), `"required"` (must call at least one tool), or `{ "type": "function", "function": { "name": "..." } }` (must call the named one, useful when the action is decided and you only need arguments filled). Naming a function guarantees that call but the model may still issue others it judges necessary. Expose only that one tool if you need exactly one call.
- `temperature`, `max_completion_tokens`: standard OpenAI knobs. Lower temperature for decisive tool-use agents.
- Confirm the exact supported fields against the live model schema via `runware-run`. Never guess.

## Quality bar

- The loop is bounded (iteration cap with a clear error), not open-ended.
- Every assistant tool-call message and its matching `tool` reply are both in history, with `tool_call_id`s paired correctly.
- `arguments` is parsed (and ideally validated) before the function runs. Tool failures return `{ "error": ... }`, not exceptions.
- Tools are tightly scoped: clear names, `enum`/`required` on arguments, compact JSON results.
- The model is `live` and supports `io:text-to-text` (verified against its card, not assumed).

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `vision-understanding` (image/video understanding with the same LLMs over the same endpoint).
