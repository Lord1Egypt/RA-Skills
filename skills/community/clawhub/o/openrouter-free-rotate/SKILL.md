---
name: openrouter-free-rotate
description: |
  Scan OpenRouter for available free models (zero cost), benchmark them,
  score by capability, and auto-update OpenClaw config with the best ones.
  Use when: "rotate OpenRouter free models", "find free models", "refresh free models",
  "auto-swap free models", "benchmark free models", "scan free models",
  or "openrouter free" are mentioned.
  NOT for: testing paid models or non-OpenRouter providers.
---

# OpenRouter Free Model Rotate v2.0

## Capabilities

- **Smart scoring** — ranks models by context window, multimodal support, reasoning ability, output length, and latency
- **Concurrent testing** — tests multiple models at once (configurable workers)
- **Quality benchmark** — PONG instruction-following test
- **Capability filter** — text-only / multimodal / image / reasoning / large context
- **Result caching** — 1-hour cache to avoid redundant API calls
- **JSON report** — export results for analysis
- **Auto config** — updates openclaw.json + models.json + optional gateway restart

## Quick Start

```bash
# Full flow: scan → bench → test → update → restart (recommended)
scripts/rotate_free_models.py --api-key "sk-or-xxx" --restart

# Quick rotate (no bench, just connectivity)
scripts/rotate_free_models.py --api-key "sk-or-xxx" --test 30 --keep 10 --restart

# Scan + show ranked by score (no changes)
scripts/rotate_free_models.py --api-key "sk-or-xxx" --scan --sort score

# Quality benchmark
scripts/rotate_free_models.py --api-key "sk-or-xxx" --bench --json report.json

# Filter: only multimodal models
scripts/rotate_free_models.py --api-key "sk-or-xxx" --filter multimodal --restart

# Use cached results (<1h old), skip retesting
scripts/rotate_free_models.py --api-key "sk-or-xxx" --use-cache --keep 10

# Save JSON report
scripts/rotate_free_models.py --api-key "sk-or-xxx" --json /tmp/report.json
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--api-key` | `$OPENROUTER_API_KEY` | OpenRouter API key |
| `--test N` | `0` (all) | Max models to test |
| `--keep N` | `10` | Working models to keep in config |
| `--workers N` | `5` | Concurrent test workers |
| `--timeout N` | `15` | Per-model timeout (seconds) |
| `--bench` | off | Enable quality benchmark |
| `--filter TYPE` | `all` | all/text/multimodal/image/reasoning/fast/large |
| `--sort BY` | `score` | score/latency/name |
| `--use-cache` | off | Use 1h cached results |
| `--json FILE` | none | Save JSON report |
| `--restart` | off | Restart gateway after update |
| `--no-update` | off | Don't change configs |
| `--scan` | off | Scan only, no testing |

## Scoring Algorithm

Models are ranked by a weighted composite:

| Factor | Weight | Effect |
|--------|--------|--------|
| Context window | +2 per 100K tokens | More context = higher score |
| Max output tokens | +0.5 per 1K | Longer output = higher |
| Image input | +5 | Multimodal bonus |
| Audio input | +5 | Multimodal bonus |
| Video input | +3 | Advanced capability |
| Reasoning support | +8 | Chain-of-thought bonus |
| Latency | -0.3 per 100ms | Faster = higher score |
| Brand quality | +2~5 | Qwen-Coder, Llama-70B, GPT, Gemini recognized |

## Scheduling

Run via cron every 6 hours for auto-rotation:

```
0 */6 * * *  python3 rotate_free_models.py --api-key "sk-or-xxx" --restart > /var/log/model-rotate.log 2>&1
```
