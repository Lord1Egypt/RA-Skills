# Model Matrix — Local Model Optimizer

## Model Comparison by Hardware Tier

### Tiny Tier (≤4GB VRAM)

| Model | Size | VRAM | Quality | Speed | Tool Calling | Multilingual | Best For |
|-------|------|------|---------|-------|-------------|-------------|----------|
| Gemma 3 4B | 2.5GB | 2.5GB | 5/10 | 60 t/s | ✅ Basic | ✅ 30+ langs | Edge/mobile deployment |
| Phi-3.5 Mini | 2.5GB | 2.5GB | 5/10 | 55 t/s | ✅ Basic | ⚠️ EN-focus | Reasoning on tiny hardware |
| Qwen 2.5 3B | 2.0GB | 2.0GB | 4/10 | 70 t/s | ❌ | ✅ CJK+EN | Fast multilingual tasks |

### Small Tier (4-8GB VRAM)

| Model | Size | VRAM | Quality | Speed | Tool Calling | Multilingual | Best For |
|-------|------|------|---------|-------|-------------|-------------|----------|
| Gemma 3 12B Q4 | 5.0GB | 5.0GB | 7/10 | 35 t/s | ✅ Strong | ✅ 30+ langs | Best quality/size ratio |
| Llama 3.1 8B | 4.5GB | 4.5GB | 7/10 | 40 t/s | ✅ Good | ✅ 8 langs | General purpose workhorse |
| Mistral 7B | 4.0GB | 4.0GB | 6/10 | 45 t/s | ✅ Basic | ✅ EU langs | Fast European language tasks |

### Medium Tier (8-16GB VRAM)

| Model | Size | VRAM | Quality | Speed | Tool Calling | Multilingual | Best For |
|-------|------|------|---------|-------|-------------|-------------|----------|
| Gemma 3 12B | 8.0GB | 8.0GB | 8/10 | 30 t/s | ✅ Perfect | ✅ 30+ langs | Tool-calling & agent tasks |
| Llama 3.1 8B Q8 | 8.5GB | 8.5GB | 8/10 | 25 t/s | ✅ Strong | ✅ 8 langs | Maximum 8B model quality |
| CodeGemma 7B | 7.0GB | 7.0GB | 7/10 | 35 t/s | ✅ Good | ⚠️ Code-focus | Coding and code review |

### Large Tier (16-32GB VRAM)

| Model | Size | VRAM | Quality | Speed | Tool Calling | Multilingual | Best For |
|-------|------|------|---------|-------|-------------|-------------|----------|
| Gemma 3 27B Q4 | 16GB | 16GB | 9/10 | 15 t/s | ✅ Perfect | ✅ 30+ langs | Near-cloud quality locally |
| Llama 3.1 70B Q4 | 24GB | 24GB | 9/10 | 8 t/s | ✅ Strong | ✅ 8 langs | Maximum open-model capability |
| Mixtral 8x7B | 20GB | 20GB | 8/10 | 12 t/s | ✅ Good | ✅ EU langs | High throughput MoE |

### XL Tier (32GB+ VRAM)

| Model | Size | VRAM | Quality | Speed | Tool Calling | Multilingual | Best For |
|-------|------|------|---------|-------|-------------|-------------|----------|
| Gemma 3 27B | 28GB | 28GB | 10/10 | 12 t/s | ✅ Perfect | ✅ 30+ langs | Top-3 global open model |
| Llama 3.1 70B Q8 | 48GB | 48GB | 10/10 | 5 t/s | ✅ Strong | ✅ 8 langs | Rivals cloud models |
| DeepSeek V2 16B | 32GB | 32GB | 9/10 | 10 t/s | ✅ Strong | ✅ Multi | Reasoning & math |

## Quantization Guide

| Format | Quality Loss | Size Reduction | When to Use |
|--------|-------------|----------------|-------------|
| F16 (full) | 0% | 0% | Max quality, unlimited VRAM |
| Q8_0 | ~1% | 50% | High quality, enough VRAM |
| Q6_K | ~2% | 58% | Good balance |
| Q5_K_M | ~3% | 64% | Recommended default |
| Q4_K_M | ~5% | 71% | Best size/quality ratio |
| Q4_0 | ~8% | 75% | Max compression |
| Q3_K_M | ~12% | 78% | Extreme compression |
| Q2_K | ~20% | 85% | Last resort |

## Apple Silicon Notes

- M1/M2/M3/M4 use unified memory — 75% of total RAM is usable as VRAM
- Metal acceleration provides good performance
- M1 Pro (16GB): Medium tier → Gemma 3 12B recommended
- M1 Max (32GB): Large tier → Gemma 3 27B Q4 recommended
- M2 Ultra (64-192GB): XL tier → Any model including 70B+ full precision
