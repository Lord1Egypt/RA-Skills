# Context Pruning Strategies

## Token Estimation

Rough heuristic: `1 token ≈ 4 characters` (English). For French, closer to `3.5 chars/token` due to accents and longer words.

```python
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
```

## Sliding Window

Keep only the last N messages (e.g., 10). Oldest are dropped entirely.

**Pros:** Simple, predictable token count.
**Cons:** Loses early context.

## Summarise-then-Prune

When context exceeds budget:
1. Take oldest messages (those being dropped).
2. Generate a 1-2 sentence summary (cheap model or heuristic).
3. Prepend summary as a single system message.

```python
def cheap_summarise(messages: list[dict]) -> str:
    parts = []
    for m in messages:
        snippet = m["content"][:30].replace("\n", " ")
        parts.append(f"{m['role']}: {snippet}...")
    return " ".join(parts)[:600]
```

## Delta-Only Context

Instead of re-sending full history, send only what changed since the last call. Maintain a server-side or client-side conversation ID and let the API handle state.

**When available:** Prefer Inception's conversation/memory features over manual context management.

## Prompt Compression Checklist

Before sending any prompt to Inception:

- [ ] Remove duplicate instructions
- [ ] Strip markdown/formatting not needed by the model
- [ ] Truncate examples to minimum viable demonstration
- [ ] Use abbreviations where unambiguous
- [ ] Set explicit `max_tokens` on output
- [ ] Check total context against budget
