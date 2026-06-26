# Model Preferences & Ranking

## How the ranked fallback chain works

The user can provide an explicit ordered list of preferred model IDs. OpenClaw
tries them in order, skipping any that are not currently free. After exhausting
the user's list, it falls back to the auto-ranked pool.

### User preference list format

When writing code or asking the user for preferences, use this structure:

```python
PREFERRED_MODELS = [
    # ── Tier 1: Qwen (all free variants, largest first) ──
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "qwen/qwen-2-72b-instruct:free",

    # ── Tier 2: GLM (Zhipu AI) ──
    "thudm/glm-4-9b:free",
    "thudm/glm-z1-32b:free",

    # ── Tier 3: Nemotron (NVIDIA) ──
    "nvidia/llama-3.1-nemotron-70b-instruct:free",
    "nvidia/nemotron-4-340b-instruct:free",

    # ── Tier 4: auto-ranked pool (anything free that passes) ──
    # (handled automatically if all above are unavailable)
]
```

Store this in the user's `.env` as a comma-separated string if they want it
persisted across sessions:

```
OPENROUTER_PREFERRED_MODELS=qwen/qwen-2.5-72b-instruct:free,qwen/qwen-2.5-7b-instruct:free,thudm/glm-4-9b:free,thudm/glm-z1-32b:free,nvidia/llama-3.1-nemotron-70b-instruct:free,nvidia/nemotron-4-340b-instruct:free
```

---

## Auto-ranking algorithm (when no preference list given)

Score each free model out of 100:

| Factor | Weight | How measured |
|--------|--------|-------------|
| Context window | 40% | `log(context_length) / log(200000)` — normalised to 0–1 |
| Recency | 30% | Models created in last 90 days score 1.0; older score decreases linearly to 0 at 2 years |
| Provider reputation | 30% | Hardcoded tiers (see below) |

### Provider reputation tiers (default)

| Tier | Score | Providers |
|------|-------|-----------|
| A | 1.0 | google, meta-llama, mistralai, anthropic |
| B | 0.7 | qwen, nvidia, microsoft, cohere |
| C | 0.4 | all others |

### Customising the auto-rank

The user can override tiers in `.env`:

```
OPENROUTER_TIER_A=google,meta-llama,mistralai
OPENROUTER_TIER_B=qwen,deepseek
```

---

## Default well-known free models (as of early 2025)

These are known-good free models. The preferred tiers are marked.
Always re-check against the live API — this list may be stale.

```
── Tier 1: Qwen (preferred) ──────────────────────────────────────────────
qwen/qwen-2.5-72b-instruct:free          (128k ctx, strong reasoning, Alibaba)
qwen/qwen-2.5-7b-instruct:free           (128k ctx, fast + lightweight)
qwen/qwen-2-72b-instruct:free            (128k ctx, previous gen fallback)

── Tier 2: GLM / Zhipu AI (preferred) ───────────────────────────────────
thudm/glm-4-9b:free                      (128k ctx, multilingual)
thudm/glm-z1-32b:free                    (32k ctx, reasoning-focused)

── Tier 3: Nemotron / NVIDIA (preferred) ─────────────────────────────────
nvidia/llama-3.1-nemotron-70b-instruct:free  (128k ctx, strong RLHF alignment)
nvidia/nemotron-4-340b-instruct:free         (4k ctx, largest open NVIDIA model)

── Auto-ranked pool (fallback when tiers 1–3 unavailable) ────────────────
google/gemini-2.0-flash-exp:free          (1M ctx, very capable)
meta-llama/llama-3.3-70b-instruct:free    (128k ctx, strong reasoning)
mistralai/mistral-7b-instruct:free        (32k ctx, reliable)
deepseek/deepseek-r1:free                 (64k ctx, strong reasoning)
microsoft/phi-3-mini-128k-instruct:free   (128k ctx, tiny+fast)
```

---

## Presenting options to the user

When showing the discovered model list, format it like this:

```
Free models found (ranked):
  1. google/gemini-2.0-flash-exp:free     — 1M ctx  | Google  | ★★★
  2. meta-llama/llama-3.3-70b-instruct    — 128k ctx | Meta    | ★★★
  3. mistralai/mistral-7b-instruct:free   — 32k ctx  | Mistral | ★★☆
  ...
```

Ask: "Would you like to use #1, pick a different one, or give me a ranked list?"
