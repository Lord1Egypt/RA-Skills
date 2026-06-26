---
name: llm-perf-estimator
description: Estimate LLM inference performance metrics including TTFT, decode speed, and VRAM requirements based on model architecture, GPU specs, and quantization format.
argument-hint: "[model_name_or_config_path] [gpu_name] [input_tokens] [output_tokens] [quant]"
user-invocable: true
---

# LLM Inference Performance Estimator

Estimate **TTFT (Time To First Token)**, **decode speed (tokens/s)**, and **VRAM usage** for a given LLM on a specific GPU.

## How to Use

The user may invoke this skill in several ways:

1. **Named model**: `/llm-perf-estimator Qwen2.5-7B RTX4090 2048 512 fp16`
2. **With config file**: `/llm-perf-estimator config.json RTX4090 2048 512 int4`
3. **Interactive**: `/llm-perf-estimator` — ask the user step by step

Arguments (all optional, prompt for missing ones):
- `model` — model name from preset list, or path to a HuggingFace `config.json`
- `gpu` — GPU name from preset list, or custom specs
- `input_tokens` — prefill sequence length (default: 1024)
- `output_tokens` — number of tokens to generate (default: 256)
- `quant` — quantization format: `fp16`, `bf16`, `fp8`, `int8`, `int4` (default: `fp16`)

---

## Step 1 — Resolve Model Architecture

### Preset Models

If the user provides a known model name, use the following presets:

| Model | Type | Total Params | Activated Params | Layers | Hidden | Heads (Q) | Heads (KV) | FFN Type | Intermediate | Vocab |
|---|---|---|---|---|---|---|---|---|---|---|
| **Qwen3.5-4B** | Hybrid Dense | 4B | 4B | 32 (8 full+24 linear) | 2560 | 16 (full) / 16 (linear) | 4 (full) | SwiGLU | 9216 | 248320 |
| **Qwen3.5-35B-A3B** | Hybrid MoE | 35B | 3B | 40 (10 full+30 linear) | 2048 | 16 (full) / 16 (linear) | 2 (full) | SwiGLU+MoE | 8×512 per tok | 248320 |

If the model is not in the preset list and no config file is provided, ask the user to provide a `config.json`. They can get it without downloading the full model:

```
# ModelScope (browser)
https://modelscope.cn/models/{org}/{model}/file/view/master/config.json

# HuggingFace (browser)
https://huggingface.co/{org}/{model}/blob/main/config.json
```

Open the URL, copy the content, and paste it directly into the conversation. Alternatively, provide the local file path if the model is already downloaded.

If the user cannot provide a config, ask them to manually input:
- `num_hidden_layers`, `hidden_size`, `num_attention_heads`, `num_key_value_heads`
- `intermediate_size`, `vocab_size`
- For MoE: `num_experts`, `num_experts_per_tok`, `moe_intermediate_size`

### Parsing config.json

If the user provides a `config.json` path, read the file and extract:
```
num_hidden_layers, hidden_size, num_attention_heads, num_key_value_heads,
intermediate_size, vocab_size, model_type,
# MoE fields (if present):
num_experts / num_local_experts, num_experts_per_tok, moe_intermediate_size
# Hybrid attention (if present):
layer_types  ← list of strings, e.g. ["linear_attention", ..., "full_attention", ...]
head_dim     ← if explicitly provided, use it; otherwise head_dim = hidden_size / num_attention_heads
```

**Determine `num_full_attn_layers`**:
- If `layer_types` exists: `num_full_attn_layers = count of "full_attention" in layer_types`
- If `layer_types` is absent (standard transformer): `num_full_attn_layers = num_hidden_layers`

**Note on nested configs** (e.g. Qwen3.5-35B-A3B has a `text_config` wrapper):
- If the top-level JSON has a `text_config` key, read all text model fields from inside it.
- `head_dim` may be explicitly set (e.g. `256`); prefer that over computing from `hidden_size / num_attention_heads`.

**Note on `tie_word_embeddings`**: if `true`, the embedding table and lm_head share the same weights. Do not count them twice in VRAM — the embedding contributes `vocab_size × hidden_size × bytes_per_param` only once.

**Note on `attn_output_gate`**: recognized but ignored in calculations — its contribution to FLOPs and VRAM is <1% and within the MFU uncertainty margin.

---

## Step 2 — Resolve GPU Specs

### Preset GPUs

| GPU | VRAM (GB) | BF16 TFLOPS | FP8 TFLOPS | INT8 TOPS | HBM BW (GB/s) |
|---|---|---|---|---|---|
| RTX 4060 | 8 | 15.1 | — | 30.2 | 272 |
| RTX 4060 Ti | 16 | 22.1 | — | 44.2 | 288 |
| RTX 4070 | 12 | 29.1 | — | 58.2 | 504 |
| RTX 4070 Ti | 12 | 40.1 | — | 80.2 | 504 |
| RTX 4070 Ti Super | 16 | 40.1 | — | 80.2 | 672 |
| RTX 4080 | 16 | 48.7 | — | 97.4 | 717 |
| RTX 4080 Super | 16 | 52.2 | — | 104.4 | 736 |
| RTX 4090 | 24 | 82.6 | — | 165.2 | 1008 |
| RTX 5070 Ti | 16 | 176.0 | 352.0 | 352.0 | 896 |
| RTX 5080 | 16 | 225.0 | 450.0 | 450.0 | 960 |
| RTX 5090 | 32 | 419.0 | 838.0 | 838.0 | 1792 |
| A10G | 24 | 31.2 | — | 62.5 | 600 |
| A100-40G | 40 | 77.97 | — | 311.9 | 1555 |
| A100-80G | 80 | 77.97 | — | 311.9 | 2000 |
| H100-SXM | 80 | 989.4 | 1978.9 | 3958.0 | 3350 |
| H100-PCIe | 80 | 756.0 | 1513.0 | 3026.0 | 2000 |
| H200-SXM | 141 | 989.4 | 1978.9 | 3958.0 | 4800 |
| L4 | 24 | 30.3 | 60.6 | 121.2 | 300 |
| L40S | 48 | 91.6 | 183.2 | 366.4 | 864 |
| MI300X | 192 | 1307.4 | 2614.9 | 5229.8 | 5300 |
| Apple M4 (16GB) | 16 | 4.6 | — | — | 120 |
| Apple M4 Pro (48GB) | 48 | 9.2 | — | — | 273 |
| Apple M4 Max (128GB) | 128 | 18.4 | — | — | 546 |

If the GPU is not listed, ask the user to provide:
- VRAM (GB)
- BF16/FP16 TFLOPS
- HBM bandwidth (GB/s)

---

## Step 3 — Quantization Bytes Per Parameter

| Format | Bytes/param | Compute dtype | Notes |
|---|---|---|---|
| fp32 | 4.0 | fp32 | Rarely used for inference |
| bf16 / fp16 | 2.0 | bf16/fp16 | Baseline |
| fp8 | 1.0 | fp8 | Requires H100/H200/RTX50xx |
| int8 | 1.0 | int8 | W8A8 or W8A16 |
| int4 | 0.5 | int4/fp16 | GPTQ/AWQ/bitsandbytes |

Select the GPU TFLOPS column matching the compute dtype:
- fp16/bf16 → BF16 TFLOPS
- fp8 → FP8 TFLOPS (fall back to BF16 if not supported, with a warning)
- int8 → INT8 TOPS
- int4 → BF16 TFLOPS (dequant to fp16 for matmul in most frameworks)

---

## Step 4 — Compute VRAM Requirements

### 4.1 Weight Memory

```
weight_bytes = total_params × bytes_per_param
weight_GB = weight_bytes / 1e9
```

For MoE models, `total_params` includes all expert weights (not just activated).

### 4.2 KV Cache Memory

Only **full attention layers** maintain a KV cache. Linear attention layers use a fixed-size recurrent state (negligible, ~tens of MB) that does not grow with sequence length.

```
kv_heads = num_key_value_heads          # from full attention config
kv_bytes_per_token = 2 × num_full_attn_layers × kv_heads × head_dim × bytes_per_param
kv_cache_GB = kv_bytes_per_token × (input_tokens + output_tokens) / 1e9
```

If `num_full_attn_layers = num_hidden_layers` (standard transformer), this reduces to the standard formula.

### 4.3 Activation Memory (prefill peak)

```
activation_GB ≈ num_layers × hidden_size × input_tokens × bytes_per_param × 2 / 1e9
```

This is an approximation; actual peak depends on framework and attention implementation.

### 4.4 Total VRAM

```
total_VRAM_GB = weight_GB + kv_cache_GB + activation_GB
```

Add a **15% overhead** for framework buffers, CUDA context, etc.:
```
total_VRAM_GB_with_overhead = total_VRAM_GB × 1.15
```

---

## Step 5 — Estimate TTFT (Prefill Latency)

Prefill is **compute-bound** for long sequences.

### 5.1 Attention FLOPs (prefill)

Only **full attention layers** have O(n²) attention compute. Linear attention layers are O(n) and their attention FLOPs are already captured in the projection FLOPs (Step 5.3).

```
attn_flops = 4 × num_full_attn_layers × input_tokens² × hidden_size
```
(factor of 4 = QK matmul + softmax + AV matmul, forward pass)

If `num_full_attn_layers = num_hidden_layers`, this is the standard transformer formula.

### 5.2 FFN FLOPs (prefill)

For SwiGLU/GeGLU (3 projections: gate, up, down):
```
ffn_flops = 3 × 2 × num_layers × input_tokens × hidden_size × intermediate_size
```

For MoE, replace `intermediate_size` with `num_experts_per_tok × moe_intermediate_size`.

### 5.3 QKV + Output Projection FLOPs

For **full attention layers** (standard QKV projections):
```
full_proj_flops = 2 × num_full_attn_layers × input_tokens × hidden_size
                  × (num_attention_heads × head_dim + 2 × kv_heads × head_dim + hidden_size)
```

For **linear attention layers** (also have Q/K/V-equivalent projections, but different dims):
```
linear_proj_flops = 2 × num_linear_attn_layers × input_tokens × hidden_size
                    × (linear_num_key_heads × linear_key_head_dim
                       + linear_num_key_heads × linear_key_head_dim
                       + linear_num_value_heads × linear_value_head_dim
                       + hidden_size)
```

If `layer_types` is absent (standard transformer), only `full_proj_flops` applies and `num_linear_attn_layers = 0`.

### 5.4 Total Prefill FLOPs

```
total_prefill_flops = attn_flops + ffn_flops + full_proj_flops + linear_proj_flops
```

### 5.5 TTFT

Apply **MFU (Model FLOP Utilization)** efficiency factor:

| Scenario | MFU |
|---|---|
| Long prompt (>512 tokens), data center GPU | 0.45 |
| Long prompt, consumer GPU | 0.35 |
| Short prompt (<128 tokens) | 0.25 |

```
effective_tflops = gpu_tflops × MFU
TTFT_seconds = total_prefill_flops / (effective_tflops × 1e12)
```

---

## Step 6 — Estimate Decode Speed

Decode is **memory-bandwidth-bound** at batch=1.

### 6.1 Bytes Read Per Decode Step

Each decode step reads:
- All activated model weights once
- KV cache for all previous tokens (full attention layers only; linear attention state is fixed-size and already loaded with weights)

```
activated_weight_bytes = activated_params × bytes_per_param
kv_cache_bytes_at_step = kv_bytes_per_token × (input_tokens + current_output_tokens)
bytes_per_step = activated_weight_bytes + kv_cache_bytes_at_step
```

For the average decode step, use `current_output_tokens ≈ output_tokens / 2`.

### 6.2 Decode Speed

Apply **bandwidth utilization** efficiency factor:

| Scenario | BW Utilization |
|---|---|
| Data center GPU (HBM2e/HBM3) | 0.85 |
| Consumer GPU (GDDR6X) | 0.75 |
| Apple Silicon (unified memory) | 0.80 |

```
effective_bandwidth = gpu_bandwidth_GBs × bw_utilization
decode_speed_tps = effective_bandwidth × 1e9 / bytes_per_step
```

---

## Step 7 — Output Report

Present results as a Markdown report with the following sections:

### Section 1: Configuration Summary

| Parameter | Value |
|---|---|
| Model | {model_name} |
| Type | Dense / MoE / Hybrid MoE |
| Total Params | {X}B |
| Activated Params | {X}B |
| Total Layers | {N} |
| Full Attention Layers | {N} ({N} linear attention) |
| GPU | {gpu_name} |
| VRAM Available | {X} GB |
| Quantization | {quant} |
| Input Tokens | {N} |
| Output Tokens | {N} |

### Section 2: VRAM Breakdown

| Component | Size (GB) |
|---|---|
| Model Weights | {X} |
| KV Cache | {X} |
| Activations (peak) | {X} |
| Framework Overhead (15%) | {X} |
| **Total Required** | **{X}** |
| GPU Available | {X} |
| **Fits in VRAM?** | ✅ Yes / ❌ No |

If it doesn't fit, suggest:
- A lower quantization format
- Offloading options (CPU offload, disk offload)

### Section 3: Performance Estimates

| Metric | Estimate |
|---|---|
| TTFT (Time to First Token) | {X} ms |
| Decode Speed | {X} tokens/s |
| Time to Generate {N} tokens | {X} s |
| Total End-to-End Latency | {X} s |

### Section 4: Assumptions & Caveats

List the MFU and bandwidth utilization values used, and note:
- Estimates assume batch_size=1, single GPU
- Actual performance varies by framework (vLLM, llama.cpp, Ollama, etc.)
- FlashAttention / FlashAttention-2 is assumed for prefill
- KV cache quantization not considered
- Speculative decoding not considered

---

## Notes for the Agent

- Always show intermediate calculations in a collapsible section or footnote if the user asks "how did you calculate this"
- If VRAM is insufficient, proactively suggest the minimum quantization that would fit
- If the user provides a `config.json`, confirm the parsed values before computing
- Round all results to 2 significant figures for readability
- For MoE models, clearly distinguish total vs activated parameters in all calculations
