# Recipe — Find and Run a Model

## Goal

Discover a suitable open-source model on the Hub, confirm it is runnable via the router, and run a chat completion.

## When

The user asks an open-ended question best answered by an open-source LLM, or explicitly wants to use a Hugging Face model.

## Inputs

- A task description (what the model should do).
- Optional constraints: size, language, license, author.

## Steps

1. **Search (free).** `hf_search_models` with `filter: "text-generation"`, `sort: "downloads"`, and a `search` term. Limit to a few results.
2. **Inspect (free).** `hf_model_info` on the top candidate — check `pipeline_tag: text-generation` and `cardData.license`.
3. **Confirm support (free).** `hf_list_inference_models`; ensure the candidate id is present. If not, pick one that is.
4. **Run (billed).** `hf_chat` with the confirmed model, OpenAI-style `messages`, and a bounded `max_tokens`.
5. **Report.** Cite the exact model id and the returned `usage`.

## Output

A chat completion answer plus the model id and token usage.

## Example

```json
{ "tool": "hf_search_models", "arguments": { "search": "qwen", "filter": "text-generation", "sort": "downloads", "limit": 3 } }
```

```json
{ "tool": "hf_list_inference_models", "arguments": {} }
```

```json
{
  "tool": "hf_chat",
  "arguments": {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [{ "role": "user", "content": "Give three uses of embeddings." }],
    "max_tokens": 120
  }
}
```

> Answer generated with `Qwen/Qwen2.5-7B-Instruct` (report the `usage` from the response).

## Edge cases

- **`model_not_supported`**: the candidate isn't runnable → pick a model from `hf_list_inference_models`.
- **Gated license**: the model card may require accepting terms / access — choose another model or obtain access.
- **`401`/`402`**: fix the token / add credits; do not retry blindly.

## Production notes

- Pin the model id; do not switch models silently between runs.
- Always set `max_tokens`; prefer smaller models when adequate.
- Cache deterministic (temperature 0) completions if the same prompt recurs.
