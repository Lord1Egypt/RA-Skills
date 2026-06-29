---
name: model-watch
description: Benchmark AI API models over time and detect quality degradation. 7 standardized tests (reasoning, coding, writing, instruction-following, hallucination). Alerts when scores drop >10% vs historical average. Because models silently get dumber.
version: 1.2.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [LLM, Benchmark, Quality, Monitoring, Degradation, API, CLI]
    homepage: https://github.com/minirr890112-byte/model-watch
---

# model-watch

## Problem → Solution

**The problem**: AI companies silently degrade their models. "Opus 4.7 was hallucinating a lot today... shocking to see such degradation" — r/ClaudeAI (49↑). "Anthropic admits to have made hosted models more stupid" — r/LocalLLaMA (281↑). You're paying the same price for a dumber model and you don't even know it.

**The solution**: Standardized benchmark suite you run yourself. 7 tests across 5 categories. Scores stored locally. Alerts when recent scores drop >10% vs your historical average. Hard data, not vibes.

## Quick Start

```bash
pip install git+https://github.com/minirr890112-byte/model-watch.git

model-watch demo              # View benchmark questions
model-watch submit '{"reasoning_1":"...","coding_1":"...",...}'  # Submit outputs
model-watch history           # View score history
model-watch alert             # Check for degradation
```

## Benchmarks (7 tests)

| Category | Tests | What it measures |
|----------|-------|-----------------|
| Reasoning | 2 | Logic, multi-step deduction |
| Coding | 2 | Code generation, debugging |
| Writing | 1 | Quality, coherence |
| Instruction-following | 1 | Precision, constraint adherence |
| Hallucination detection | 2 | Factual accuracy |

## How It Works

1. Run the 7 benchmark questions through your AI model of choice
2. Feed the responses into `model-watch submit`
3. Scores are stored locally in `~/.hermes/model-watch-history.json`
4. Track trends with `model-watch history`
5. `model-watch alert` flags when recent scores drop >10% vs historical average

---
⭐ **Star this repo if you've noticed your favorite model getting dumber**: [github.com/minirr890112-byte/model-watch](https://github.com/minirr890112-byte/model-watch)
