# Model Database — Pricing, Benchmarks & Capability Tiers

Provider-agnostic model reference for Model Pilot routing decisions.

> ⚠️ Prices change. Update this file when providers announce changes. Last verified: 2026-03-31.

---

## Z.ai / GLM Models

| Model | Slug | Tier | Input ($/1M) | Output ($/1M) | Context | Key Strengths |
|-------|------|------|-------------|---------------|---------|---------------|
| GLM-4.5 | `zai/glm-4.5` | 🟢 Routine | ~$0.20 | ~$0.60 | 128K | General tasks, good baseline |
| GLM-4.6 | `zai/glm-4.6` | 🟢 Routine | ~$0.30 | ~$0.80 | 128K | Improved reasoning over 4.5 |
| GLM-4.6V | `zai/glm-4.6v` | 🟡 Vision | ~$0.40 | ~$1.00 | 128K | **Image understanding** — use for any vision task |
| GLM-4.7 | `zai/glm-4.7` | 🟢 Routine | ~$0.20 | ~$0.60 | 128K | Latest routine model, low hallucination |
| GLM-5 Turbo | `zai/glm-5-turbo` | 🟡 Intermediate | ~$1.00 | ~$3.20 | 200K | Fast, strong coding, good balance |
| GLM-5 | `zai/glm-5` | 🔴 Complex | ~$1.00 | ~$3.20 | 200K | Flagship, MoE 744B (40B active), SWE-bench 77.8% |
| GLM-5.1 | `zai/glm-5.1` | 🔴 Complex | TBD (likely ~$1.50) | TBD (likely ~$5.00) | 200K | Best coding (45.3 vs 47.9 Claude Opus 4.6), newest |

**Z.ai Notes:**
- All models are open source (MIT license)
- GLM-5.1 uses 3x quota during peak, 2x off-peak (1x promo until end of April 2026)
- GLM-5 has industry-lowest hallucination rate (34%)
- Trained on Huawei Ascend 910B chips

### Z.ai Cost Ratios (approximate, relative to GLM-4.7)

```
GLM-4.7:    1.0x  (baseline)
GLM-5 Turbo: ~5x
GLM-5:      ~5x
GLM-5.1:    ~8x  (estimated)
```

---

## OpenAI Models

| Model | Slug | Tier | Input ($/1M) | Output ($/1M) | Context | Key Strengths |
|-------|------|------|-------------|---------------|---------|---------------|
| GPT-4o-mini | `openai/gpt-4o-mini` | 🟢 Routine | $0.15 | $0.60 | 128K | Fast, cheap, solid quality |
| GPT-4o | `openai/gpt-4o` | 🟡 Intermediate | $2.50 | $10.00 | 128K | Strong generalist, multimodal |
| o1 | `openai/o1` | 🔴 Complex | $15.00 | $60.00 | 200K | Deep reasoning, math, science |
| o3 | `openai/o3` | 🔴 Complex | $10.00 | $40.00 | 200K | Latest reasoning model |
| o4-mini | `openai/o4-mini` | 🟡 Intermediate | $1.10 | $4.40 | 200K | Reasoning at lower cost |

**OpenAI Notes:**
- o1/o3 are thinking models — slower but more accurate for complex tasks
- GPT-4o-mini is ~17x cheaper than GPT-4o with 80-90% quality for most tasks

### OpenAI Cost Ratios

```
GPT-4o-mini: 1.0x  (baseline)
o4-mini:       ~7x
GPT-4o:       ~17x
o3:          ~100x
o1:          ~150x
```

---

## Anthropic Models

| Model | Slug | Tier | Input ($/1M) | Output ($/1M) | Context | Key Strengths |
|-------|------|------|-------------|---------------|---------|---------------|
| Claude Haiku 3.5 | `anthropic/claude-3.5-haiku` | 🟢 Routine | $0.80 | $4.00 | 200K | Fast, efficient, good for tools |
| Claude Sonnet 4 | `anthropic/claude-sonnet-4` | 🟡 Intermediate | $3.00 | $15.00 | 200K | Best balance of speed and quality |
| Claude Opus 4 | `anthropic/claude-opus-4` | 🔴 Complex | $15.00 | $75.00 | 200K | Peak quality, complex tasks |
| Claude Opus 4.6 | `anthropic/claude-opus-4.6` | 🔴 Complex | $5.00 | $25.00 | 200K | Best coding (SWE-bench 80.9%), improved pricing |

**Anthropic Notes:**
- Opus 4.6 is dramatically cheaper than Opus 4 with better coding performance
- Sonnet 4 is the sweet spot for most tasks
- Haiku 3.5 is ~19x cheaper than Sonnet 4

### Anthropic Cost Ratios

```
Haiku 3.5: 1.0x  (baseline)
Sonnet 4:  ~4x
Opus 4.6:  ~6x
Opus 4:   ~19x
```

---

## Google Models

| Model | Slug | Tier | Input ($/1M) | Output ($/1M) | Context | Key Strengths |
|-------|------|------|-------------|---------------|---------|---------------|
| Gemini Flash 2.0 | `google/gemini-flash` | 🟢 Routine | $0.075 | $0.30 | 1M | Ultra-cheap, massive context |
| Gemini Pro 2.5 | `google/gemini-pro` | 🟡 Intermediate | $1.25 | $10.00 | 1M | Strong reasoning, multimodal |
| Gemini Ultra 2.0 | `google/gemini-ultra` | 🔴 Complex | $2.50 | $15.00 | 1M | Best overall, massive context |

**Google Notes:**
- Flash is the cheapest option across all providers (~2x cheaper than GPT-4o-mini)
- All models support 1M token context — unique advantage for long documents
- Flash handles most routine tasks surprisingly well

### Google Cost Ratios

```
Flash:    1.0x  (baseline)
Pro:     ~33x
Ultra:   ~50x
```

---

## Cross-Provider Comparison (Intermediate Tier)

| Provider | Model | Input ($/1M) | Output ($/1M) | SWE-bench | Relative Cost |
|----------|-------|-------------|---------------|-----------|---------------|
| Google | Gemini Flash 2.0 | $0.075 | $0.30 | — | 1.0x (cheapest) |
| Z.ai | GLM-4.7 | ~$0.20 | ~$0.60 | — | ~2x |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 | — | ~2x |
| Z.ai | GLM-5 Turbo | $1.00 | $3.20 | ~77% | ~10x |
| Anthropic | Claude Haiku 3.5 | $0.80 | $4.00 | — | ~13x |
| OpenAI | o4-mini | $1.10 | $4.40 | — | ~15x |
| Anthropic | Claude Sonnet 4 | $3.00 | $15.00 | — | ~50x |

---

## When to Use Each Tier

| Situation | Use This | Why |
|-----------|----------|-----|
| Quick question, formatting | 🟢 Routine tier | Quality ceiling irrelevant |
| Code scaffolding, email, analysis | 🟡 Intermediate | Good quality, reasonable cost |
| Architecture, creative writing, deep debugging | 🔴 Complex | Quality ceiling matters |
| Processing images | Vision model (any tier) | Non-negotiable requirement |
| Processing 100K+ token documents | Google Flash (1M context) | Other models can't handle it |
| Budget is priority | 🟢 Routine tier always | Maximize savings |
| Accuracy is priority | 🔴 Complex tier always | Minimize errors |
| Batch processing (100+ tasks) | 🟢 Routine tier | Savings compound |

---

## Model Aliases in OpenClaw

OpenClaw uses model aliases for quick switching. Check the user's config for available aliases.

Example Z.ai aliases (may vary):
```
GLM         → zai/glm-4.7
GLM-4.5     → zai/glm-4.5
GLM-4.6     → zai/glm-4.6
GLM-4.6V    → zai/glm-4.6v
GLM-5-Turbo → zai/glm-5-turbo
GLM-5       → zai/glm-5 (may need explicit config)
GLM-5.1     → zai/glm-5.1 (may need explicit config)
```

Model Pilot uses these aliases when suggesting switches via `session_status(model=...)`.

---

*Prices are approximate and may not reflect latest updates. Always verify with provider documentation.*
