---
name: local-model-quantization-router
description: Recommend local LLM model routes and quantization levels using hardware, privacy, task complexity, context size, and budget constraints. Use for Qwen/Ollama/local endpoint cost-performance decisions.
---

# Local Model Quantization Router

Use this skill to choose between local quantized models and cloud fallback before running OpenClaw workloads.

## Workflow

1. Describe available hardware and task requirements.
2. Run `scripts/local_model_quantization_router.py` with CLI flags or JSON input.
3. Review the recommended model family, quantization level, endpoint, fallback, and risk notes.
4. Use the output as routing evidence for local-first or privacy-first deployments.

## Parameters

- `--task TEXT`: Task summary.
- `--complexity {simple,standard,complex,critical}`.
- `--privacy {low,normal,high,regulated}`.
- `--vram-gb FLOAT`: GPU memory available.
- `--ram-gb FLOAT`: System memory available.
- `--context-tokens INT`: Required context window.
- `--hardware PATH`: Optional JSON with `vram_gb`, `ram_gb`, `cpu_only`.
- `--output PATH`: Optional JSON output path.

## Outputs

- `route`: `local-only`, `local-first`, `hybrid`, or `cloud-required`.
- `model`: Recommended model family.
- `quantization`: Suggested quant level.
- `endpoint`: Suggested local endpoint type.
- `fallback`: Safer fallback when quality or context is insufficient.
- `reasons`: Evidence for the decision.

No model is downloaded and no config file is changed.
