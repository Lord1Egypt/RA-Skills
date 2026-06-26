# Recipe — Chat Completion

## Goal

Produce a text answer from a prompt using the cheapest capable model.

## When

General Q&A, summarization, rewriting, classification, simple extraction.

## Inputs

- A system instruction (optional) and a user message.
- A model (default `gpt-4o-mini`).
- A token cap.

## Steps

1. If the input is untrusted, moderate it first (`openai_moderations`, free).
2. Choose the cheapest capable model (`gpt-4o-mini`).
3. Build `messages` with a clear system role.
4. Set `max_tokens` and a low `temperature` for consistency.
5. Call `openai_chat`.
6. Read `choices[0].message.content` and report `usage.total_tokens`.

## Output

`choices[0].message.content` (string) + `usage`.

## Example

```json
{
  "tool": "openai_chat",
  "arguments": {
    "model": "gpt-4o-mini",
    "messages": [
      { "role": "system", "content": "Answer in one sentence." },
      { "role": "user", "content": "Why is the ocean salty?" }
    ],
    "temperature": 0.2,
    "max_tokens": 60
  }
}
```

```json
{
  "choices": [{ "message": { "role": "assistant", "content": "Rivers carry dissolved mineral salts into the ocean, where they accumulate." }, "finish_reason": "stop" }],
  "usage": { "prompt_tokens": 24, "completion_tokens": 14, "total_tokens": 38 }
}
```

## Edge cases

- `finish_reason: "length"` → output truncated; raise `max_tokens`.
- Empty/garbled output → raise model tier or clarify the prompt.
- `400 context_length_exceeded` → trim input.

## Production notes

- **Cost:** every call is billed by token. Cap `max_tokens`, cache identical calls, prefer `gpt-4o-mini`.
- Escalate to `gpt-4.1`/`gpt-4o` only when quality is insufficient.

> Verification needed: confirm fields with <https://platform.openai.com/docs/api-reference>.
