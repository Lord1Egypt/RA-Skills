---
name: hermes-smart-router
description: Use when switching models, saving costs, or routing queries. Automatically picks the cheapest model that can handle the job — "translate hello" routes to $0/M local, "design a database" routes to $3/M pro. 100% local classification, zero API calls for routing.
version: 0.2.2
author: raydatalab
license: MIT
platforms: [linux, macos, wsl]
triggers:
  - model switch
  - change model
  - /model
  - /tier
  - switch to
  - use local
  - use flash
  - use pro
  - too slow
  - wasting tokens
  - cheaper model
  - downgrade
  - upgrade model
  - routing
  - tier selection
  - local model
  - what model
  - which model
  - speed up
  - save cost
  - 切换模型
  - 太慢了
  - 换模型
  - 用什么模型
metadata:
  hermes:
    tags: [routing, model, cost-optimization, ollama]
    homepage: https://github.com/raydatalab/hermes-smart-router
    related_skills: [hermes-cost-optimization]
---

# Smart Router

## Overview

```
"Translate hello to German"       → local   $0/M tok
"Explain how DNS works"           → flash   $0.15/M tok  (GPT-4o-mini)
"Design a distributed database"   → pro     $3/M tok  (Claude Sonnet)
```

Smart Router classifies every query locally (Ollama embeddings + semantic-router)
and picks the cheapest tier that can handle it. Simple queries route to free local
models. Complex reasoning routes to frontier models. You pay for what you need —
not what your config happens to be set to.

Classification runs entirely on your machine. Zero API calls for routing decisions.
Zero keys needed. ~3s on first call, <1ms after.

## When to Use

Load this skill when:
- The user is toggling between models manually (wasting tokens on simple queries)
- The user asks about cost saving, model switching, or routing
- The user mentions `/model`, `/tier`, or switches models mid-session
- The agent is about to answer a complex question and should verify the current tier

Do NOT load for: greetings, one-liners, translations, queries under 20 characters.

## CRITICAL — Agent Instructions

**Call `router.resolve()` before answering any non-trivial query.**

```python
from smart_router.router import get_router

router = get_router()
decision = router.resolve(user_message, current_tier=ACTIVE_TIER)
# → {"tier": "pro", "model": {...}, "needs_switch": true,
#    "reason": "Upgrade from flash to pro — Complex code...",
#    "recommendation": "💡 Switch to pro: `/model anthropic claude-sonnet-4` — ..."}
```

**If `decision["recommendation"]` is not None**, paste it at the top of your
response — it's ready to use, no formatting needed.

**If `decision["recommendation"]` is None**, just answer normally.
**If the call errors or times out**, skip it and answer — never retry.

`ACTIVE_TIER` is your current tier (local/flash/pro). Check with `/tier` or ask.

### When to Skip

Skip routing for: greetings ("hello", "thanks"), translations, one-liner facts,
queries under 20 characters. Everything else — route.

### When to Route

- **Complex:** 3+ tool calls, reasoning, architecture, multi-step code, debugging → route
- **Unsure:** If it takes more than a sentence to answer → route
- **Default:** If in doubt, route. Routing cost (~3s first call, <1ms after) is always
  less than answering from the wrong tier.

## Tier Reference

| Tier | Example Model | Input Price/1M tok | Use When |
|------|-------------|-------------------|----------|
| `local` | Ollama (llama3, qwen, etc.) | $0 | Simple Q&A, translations, offline |
| `flash` | GPT-4o-mini, Gemini Flash, Claude Haiku | ~$0.15–0.80 | General knowledge, casual coding |
| `pro` | Claude Sonnet, GPT-4o, Gemini Pro | ~$2.50–3 | Complex reasoning, architecture |

Pricing per official API pages (OpenAI, Anthropic, Google). See individual provider
docs for exact rates. Per-token pricing means a single 1K-token question costs
$0.003 on flash vs $0.003 on pro — but over thousands of queries per month, the
difference compounds.

## Prerequisites

- Hermes Agent v0.17+
- Ollama installed
- `semantic-router[ollama]` and `smart_router`

## Configuration

```yaml
smart_router:
  enabled: true
  default_tier: flash
  encoder_model: nomic-embed-text
  tiers:
    local:
      provider: custom
      model: llama3.2:3b
      base_url: http://localhost:11434/v1
    flash:
      provider: openai
      model: gpt-4o-mini
    pro:
      provider: anthropic
      model: claude-sonnet-4
  ollama:
    auto_start: true
    idle_timeout: 300
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/route <query>` | Show tier selection (dry run) |
| `/route-stats` | Session routing statistics |
| `/ollama start / stop / status` | Ollama lifecycle |
| `/tier` | Show current tier and model |

## Common Pitfalls

1. **Agent forgets to call `router.resolve()`.** The most common failure mode.
   If the agent answers without routing, manually trigger with `/route <query>`.
2. **Ollama not running.** If `decision["ollama_ready"]` is false, start Ollama
   first (`/ollama start`) or skip routing for this query.
3. **Slow first call.** First `router.resolve()` pulls `nomic-embed-text` (~274MB).
   Subsequent calls are instant. Warm up with `python3 -m smart_router route "test"`
   before heavy sessions.
4. **Fast-path false negatives.** Queries under 20 chars skip embedding. If a short
   query needs pro-level reasoning, the router won't catch it — use `/model` manually.

## Testing

```bash
bash scripts/install.sh
python3 -m smart_router route "What is the capital of France?"
python3 -m smart_router chat
python3 -m pytest tests/
```
