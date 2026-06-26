---
name: local-model-optimizer
description: Auto-detect hardware (GPU VRAM, system RAM, CPU), recommend optimal local models from Ollama registry, configure Ollama with tuned parameters, and set up hybrid cloud/local routing in OpenClaw. Supports Gemma 4, Llama, Mistral, Qwen, Phi, and other Ollama-compatible models. Calculates cost savings vs cloud API. Use when asked to "set up local model", "optimize local AI", "reduce API costs", "configure Ollama", "hardware check for AI", "hybrid routing", "cloud local routing", "run AI locally", "free AI", "zero cost model", "which model fits my hardware", "auto-config Ollama", or when users mention high API costs and want a local alternative.
---

# Local Model Optimizer

Auto-detect hardware → recommend models → configure Ollama → set up hybrid cloud/local routing.

## Quick Start

```bash
# Full auto-setup: detect hardware, install Ollama, recommend + pull model, configure routing
python3 scripts/local-model-optimizer.py auto

# Hardware detection only
python3 scripts/local-model-optimizer.py detect

# Recommend models for your hardware (no install)
python3 scripts/local-model-optimizer.py recommend

# Set up hybrid routing (cloud for complex tasks, local for simple ones)
python3 scripts/local-model-optimizer.py routing

# Cost comparison: local vs cloud
python3 scripts/local-model-optimizer.py cost
```

## Commands

### `auto` — Full Automated Setup
1. Detects GPU (NVIDIA/AMD/Apple Silicon), VRAM, RAM, CPU cores
2. Queries Ollama model registry for compatible models
3. Recommends top 3 models ranked by benchmark/size ratio
4. Installs Ollama if not present
5. Pulls recommended model
6. Configures OpenClaw provider entry
7. Sets up hybrid routing rules
8. Runs verification test

### `detect` — Hardware Detection
Reports:
- GPU model, VRAM, driver version (NVIDIA/AMD/Apple)
- System RAM (total/available)
- CPU model, core count, architecture
- Estimated model size capacity
- Compatibility tier: Tiny (≤4GB) / Small (4-8GB) / Medium (8-16GB) / Large (16-32GB) / XL (32GB+)

### `recommend` — Model Recommendations
Based on hardware tier, recommends from:

| Tier | VRAM | Models |
|------|------|--------|
| Tiny | ≤4GB | Gemma 4 E2B, Phi-3.5 Mini, Qwen2.5-3B |
| Small | 4-8GB | Gemma 4 E4B, Llama 3.1 8B, Mistral 7B |
| Medium | 8-16GB | Gemma 4 12B, Llama 3.1 8B Q8, CodeGemma |
| Large | 16-32GB | Gemma 4 27B, Llama 3.1 70B Q4, Mixtral 8x7B |
| XL | 32GB+ | Gemma 4 27B Q8, Llama 3.1 70B Q8, DeepSeek V2 |

See `references/model-matrix.md` for full benchmark comparisons.

### `routing` — Hybrid Cloud/Local Routing
Configures OpenClaw to route requests intelligently:
- **Local:** Simple Q&A, summarization, code completion, memory operations
- **Cloud:** Complex reasoning, multi-step planning, code generation, creative writing

Options:
- `--strategy cost` — minimize API spend (prefer local)
- `--strategy quality` — maximize output quality (prefer cloud)
- `--strategy balanced` — default, smart routing based on task complexity
- `--cloud-provider <name>` — which cloud provider for fallback (default: anthropic)

### `cost` — Cost Analysis
Calculates monthly savings based on:
- Current API usage pattern (reads from OpenClaw logs if available)
- Estimated electricity cost for local inference
- Token throughput comparison
- Break-even analysis for hardware investment

## Configuration

The optimizer writes to `~/.openclaw/local-model-config.json`:
```json
{
  "hardware": { "gpu": "...", "vram_gb": 16, "ram_gb": 32, "tier": "Large" },
  "model": { "name": "gemma4:27b", "quantization": "Q4_K_M", "size_gb": 15.2 },
  "routing": { "strategy": "balanced", "local_tasks": [...], "cloud_tasks": [...] },
  "performance": { "tokens_per_sec": 42, "first_token_ms": 180 }
}
```
