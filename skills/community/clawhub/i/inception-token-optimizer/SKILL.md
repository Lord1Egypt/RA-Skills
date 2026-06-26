---
name: inception-token-optimizer
description: "Optimize Inception Labs token usage to minimize costs. Use when choosing Inception models (Mercury, etc.), crafting prompts for Inception, analyzing token consumption, or when the user wants to reduce API costs. Covers caching strategies, context pruning, prompt compression, model selection tips, and free-tier budget management."
---

# Inception Token Optimizer

Reduce Inception API token consumption through prompt engineering, context management, and budget enforcement.

## Free-Tier Limits (Inception Labs)

| Metric | Cap |
|---|---|
| Requests/min | 100 |
| Input tokens/min | 100,000 |
| Output tokens/min | 10,000 |

## Core Strategies

### 1. Prompt Compression

- Remove redundant instructions, filler words, and repeated context.
- Use short system prompts: "Concise answers. French." beats a 200-word persona block.
- Avoid re-sending unchanged context — only send deltas.
- Ask for short replies: "Réponds en < 100 mots."

### 2. Context Pruning

- Before sending, estimate tokens: `len(text) // 4` (rough heuristic).
- If total context > target budget, drop oldest messages and replace with a 1-2 sentence summary.
- Use `references/pruning-strategies.md` for detailed patterns.

### 3. Caching

- Identical prompts → reuse previous response. Do not re-call.
- Hash the prompt; if seen recently (within session), return cached reply.
- `scripts/lru_cache.py` provides a drop-in LRU cache (256 items default).

### 4. Model Selection

- Use cheaper/faster models for simple tasks (summarisation, classification).
- Reserve Mercury (or flagship) for complex reasoning only.
- Batch trivial queries into a single prompt instead of multiple calls.

### 5. Output Budgeting

- Set `max_tokens` explicitly — never leave it open-ended.
- Target 150-200 output tokens for conversational replies.
- Use `temperature=0.7` to reduce verbose wandering.

## Token Budget Guard

`scripts/token_bucket.py` enforces per-minute caps using a sliding window:

```python
from scripts.token_bucket import TokenBucket

bucket = TokenBucket(req_per_min=100, in_tok_per_min=100_000, out_tok_per_min=10_000)
bucket.wait_for_slot(in_tokens=500, out_tokens=200)
# proceed with API call
```

Blocks until a slot is available. Use before every Inception API call.

## When to Use This Skill

- Before sending a prompt to Inception → compress & prune first.
- When monitoring costs → check token estimates.
- When near free-tier limits → activate budget guard.
- When building automation → integrate caching + bucket guard.
