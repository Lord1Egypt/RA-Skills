---
name: marl-middleware
description: Multi-stage multi-agent reasoning middleware that reduces LLM hallucination by 70%+. 9 specialized emergence engines for invention, creative, pharma, genomics, chemistry, ecology, law, recipe, and document generation.
tags: [reasoning, hallucination, multi-agent, metacognition, emergence, middleware]
metadata:
  clawdbot:
    config:
      requiredEnv: []
      example: |
        llm:
          baseURL: "http://localhost:8080/v1"
          model: "gpt-5.4::create"
---

# MARL Enhance — Brain Upgrade for Your Agent

**The 3rd approach after fine-tuning & RAG.** MARL restructures how LLMs reason at runtime — not their weights. One line to integrate, 70%+ hallucination reduction, 9 domain-specific emergence engines.

[![PyPI](https://img.shields.io/pypi/v/marl-middleware?color=6366f1&label=PyPI)](https://pypi.org/project/marl-middleware/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-24292e?logo=github)](https://github.com/Vidraft/MARL)
[![Demo](https://img.shields.io/badge/🤗%20Demo-HuggingFace-ff9d00)](https://huggingface.co/spaces/VIDraft/MARL)
[![FINAL Bench](https://img.shields.io/badge/🏆%20FINAL%20Bench-Global%20%235-16a34a)](https://huggingface.co/spaces/FINAL-Bench/Leaderboard)

## What It Does

Before MARL: Your agent calls the LLM once → gets an answer (might hallucinate).

After MARL: Your agent calls MARL → MARL runs a multi-stage expert pipeline → hypothesis, solving, auditing, adversarial verification, synthesis → returns a deeply verified answer.

```
Your Agent → MARL → Multi-stage Pipeline → Any LLM → Verified Answer
```

**Results:** 70%+ hallucination reduction · 94.8% of improvement from self-correction · Verified on FINAL Bench (HuggingFace Global Top 5 dataset).

## Setup

### Option A: Docker (Recommended — all platforms)

```bash
docker run -p 8080:8080 vidraft/marl
```

### Option B: pip (Linux x86_64)

```bash
pip install marl-middleware
python -m marl serve --port 8080
```

### Option C: HuggingFace Space (No install — try instantly)

Use `https://huggingface.co/spaces/VIDraft/MARL` directly in your browser.

## Connect to OpenClaw

Set your `config.json`:

```json
{
  "llm": {
    "baseURL": "http://localhost:8080/v1",
    "model": "gpt-5.4"
  }
}
```

That's it. Every LLM call now passes through MARL's multi-stage reasoning pipeline.

## 9 Emergence Modes

Switch modes by appending `::mode` to any model name:

| model value | Engine | What it does |
|-------------|--------|-------------|
| `gpt-5.4` | 🔬 Insight | Default — fact-check, strategy, deep analysis |
| `gpt-5.4::invent` | 🔧 Invent | Patent-level invention via TRIZ + bio-inspired + contradiction resolution |
| `gpt-5.4::create` | ✨ Create | Cliché inversion, paradox, genre fusion, sensory collision |
| `gpt-5.4::recipe` | 🍳 Recipe | Culinary emergence with taste chemistry validation |
| `gpt-5.4::pharma` | 💊 Pharma | Drug repositioning, mechanism crossing, multi-target design |
| `gpt-5.4::genomics` | 🧬 Genomics | Pathway crosstalk, synthetic lethality, phenotype bridging |
| `gpt-5.4::chemistry` | 🧪 Chemistry | Contradictory properties, biomimicry, waste-to-value |
| `gpt-5.4::ecology` | 🌍 Ecology | Conservation transfer, threat inversion, service stacking |
| `gpt-5.4::law` | ⚖️ Law | Cross-jurisdiction transplant, tech-law collision resolution |
| `gpt-5.4::document` | 📄 Document | Metacognitive report and document generation |

Replace `gpt-5.4` with any model — Claude, Gemini, DeepSeek, Llama, etc.

### Example: Switch to Pharma mode

```json
{
  "llm": {
    "baseURL": "http://localhost:8080/v1",
    "model": "gpt-5.4::pharma"
  }
}
```

Then chat: *"Find drug repositioning candidates for Alzheimer's using immune checkpoint mechanisms"*

### Example: Creative ideation

```json
{
  "llm": {
    "model": "claude-sonnet::create"
  }
}
```

Then chat: *"Generate 10 movie loglines that have never existed before"*

## How It Works

```
┌─ OpenClaw ────────────────────────────────────┐
│  "Analyze this complex question"               │
└──────────────┬─────────────────────────────────┘
               │ HTTP (OpenAI API format)
               ▼
┌─ MARL Middleware ─────────────────────────────┐
│  Multi-stage Multi-agent Reasoning Pipeline    │
│  9 Emergence Engines · 70%+ Hallucination ↓   │
└──────────────┬─────────────────────────────────┘
               │ API calls to your chosen LLM
               ▼
┌─ Any LLM ─────────────────────────────────────┐
│  GPT-5.4 · Claude · Gemini · DeepSeek · Llama │
└────────────────────────────────────────────────┘
```

MARL works with **every LLM** that supports OpenAI API format. It runs locally on your machine — your data never leaves your infrastructure.

## Works With Any LLM

- OpenAI (GPT-5.4, GPT-5.2, GPT-4.1, o4-mini)
- Anthropic (Claude Opus 4.6, Sonnet 4.6)
- Google (Gemini 3.1 Pro, Gemini 3 Flash)
- DeepSeek (V3, R1, R2)
- xAI (Grok-4, Grok-3)
- Groq (gpt-oss-120b, Llama 4 — free)
- Ollama (any local model)
- Any OpenAI-compatible endpoint

## Links

- **PyPI:** [pip install marl-middleware](https://pypi.org/project/marl-middleware/)
- **GitHub:** [github.com/Vidraft/MARL](https://github.com/Vidraft/MARL)
- **Demo:** [HuggingFace Space](https://huggingface.co/spaces/VIDraft/MARL)
- **FINAL Bench:** [Leaderboard](https://huggingface.co/spaces/FINAL-Bench/Leaderboard)
- **Website:** [vidraft.net](https://vidraft.net)

## About

Built by **VIDRAFT** (Seoul AI Hub). MARL's core engine is delivered as compiled binaries to protect proprietary technology. Interface code is open for integration.

Apache 2.0 · Contact: arxivgpt@gmail.com
