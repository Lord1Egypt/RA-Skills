---
name: metrillm
description: Find the best local LLM for your machine. Tests speed, quality and RAM fit, then tells you if a model is worth running on your hardware.
argument-hint: "[model-name]"
author: MetriLLM
source: https://github.com/MetriLLM/metrillm
license: Apache-2.0
allowed-tools: Bash, Read
install: npm install -g metrillm
---

# MetriLLM — Find the Best LLM for Your Hardware

Test any local model and get a clear verdict: is it worth running on your machine?

## Prerequisites

1. **Node.js 20+** — check with `node -v`
2. **Ollama** or **LM Studio** installed and running
   - Ollama: [ollama.com](https://ollama.com), then `ollama serve`
   - LM Studio: [lmstudio.ai](https://lmstudio.ai), load a model and start the server
3. **MetriLLM CLI** — install globally:

```bash
npm install -g metrillm
```

## Usage

### List available models

```bash
ollama list
```

### Run a full benchmark

```bash
metrillm bench --model $ARGUMENTS --json
```

This measures:
- **Performance**: tokens/second, time to first token, memory usage
- **Quality**: reasoning, math, coding, instruction following, structured output, multilingual
- **Fitness verdict**: EXCELLENT / GOOD / MARGINAL / NOT RECOMMENDED

### Performance-only benchmark (faster)

```bash
metrillm bench --model $ARGUMENTS --perf-only --json
```

Skips quality evaluation — measures speed and memory only.

### View previous results

```bash
ls ~/.metrillm/results/
```

Read any JSON file to see full benchmark details.

### Share to the public leaderboard

```bash
metrillm bench --model $ARGUMENTS --share
```

Uploads your result to the [MetriLLM community leaderboard](https://metrillm.dev) — an open, community-driven ranking of local LLM performance across real hardware. Compare your results with others and help the community find the best models for every setup. Shared data includes: model name, scores, hardware specs (CPU, RAM, GPU). No personal data is sent.

## Interpreting Results

| Verdict | Score | Meaning |
|---|---|---|
| EXCELLENT | >= 80 | Fast and accurate — great fit |
| GOOD | >= 60 | Solid — suitable for most tasks |
| MARGINAL | >= 40 | Usable but with tradeoffs |
| NOT RECOMMENDED | < 40 | Too slow or inaccurate |

Key metrics to highlight:
- `tokensPerSecond` > 30 = good for interactive use
- `ttft` < 500ms = responsive
- `memoryUsedGB` vs available RAM = will it fit?

## Tips

- Use `--perf-only` for quick tests
- Close GPU-intensive apps before benchmarking
- Benchmark duration varies depending on model speed and response length

## Open Source

MetriLLM is free and open source (Apache 2.0). Contributions, issues, and feedback are welcome: [github.com/MetriLLM/metrillm](https://github.com/MetriLLM/metrillm)
