# llm-perf-estimator

A Claude Code skill that estimates LLM inference performance metrics based on model architecture, GPU specs, and quantization format.

## What it estimates

- **TTFT** — Time to First Token (prefill latency)
- **Decode speed** — tokens/second
- **VRAM usage** — weights + KV cache + activations + overhead

## Usage

```
/llm-perf-estimator [model] [gpu] [input_tokens] [output_tokens] [quant]
```

All arguments are optional — the skill will prompt for anything missing.

**Examples:**
```
/llm-perf-estimator Qwen3.5-4B RTX4090 2048 512 int4
/llm-perf-estimator config.json H100-SXM 4096 1024 fp8
/llm-perf-estimator
```

## Supported inputs

**Models (presets):**
- Qwen3.5-4B (Hybrid Dense, calibrated from official config)
- Qwen3.5-35B-A3B (Hybrid MoE, calibrated from official config)

For any other model, provide a `config.json` from ModelScope or HuggingFace — no need to download the full model weights.

**GPUs:** RTX 40/50 series, A100, H100, H200, L4, L40S, MI300X, Apple M4 series. Custom specs also accepted.

**Quantization:** `fp32`, `fp16`, `bf16`, `fp8`, `int8`, `int4`

## Architecture support

The skill handles:
- Standard dense transformers
- MoE (Mixture of Experts)
- Hybrid attention (linear + full attention layers, e.g. Qwen3.5 series)

For hybrid models, KV cache and O(n²) attention FLOPs are computed only for full attention layers. Linear attention layers use a fixed-size recurrent state that does not grow with sequence length.

## Methodology

| Phase | Bottleneck | Formula |
|---|---|---|
| Prefill (TTFT) | Compute-bound | FLOPs / (GPU TFLOPS × MFU) |
| Decode | Bandwidth-bound | Bytes per step / (HBM BW × utilization) |

MFU and bandwidth utilization coefficients are selected based on GPU type and prompt length.

## Installation

Copy `SKILL.md` to your Claude Code skills directory:

```bash
# Personal (all projects)
cp SKILL.md ~/.claude/skills/llm-perf-estimator.md

# Project-local
cp SKILL.md .claude/skills/llm-perf-estimator.md
```

## Contributing

Preset models are intentionally limited to architectures verified against official `config.json` files. To add a new preset, please include the source config in your PR.
