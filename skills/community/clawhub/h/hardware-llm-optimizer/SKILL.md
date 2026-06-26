---
name: hardware-llm-optimizer
version: 1.1.0
description: Auto-detect PC hardware (CPU/GPU/RAM/VRAM) -> Determine max LLM parameters -> Recommend models (3B/7B/8B/13B/34B/70B) + quantization + deployment tools + bottleneck analysis. Chinese interface.
---

# Hardware LLM Optimizer

Detects PC hardware configuration and recommends which large language models can run.

## Features

1. **Auto-detect**: CPU, RAM, GPU (NVIDIA/AMD), VRAM
2. **Calculate**: Maximum runnable model size
3. **Quantization**: FP16 / 8bit / 4bit / 2bit recommendation
4. **Model Suggestion**: Llama 2/3, Qwen, Mistral, Phi, Gemma, Yi, etc.
5. **Bottleneck Analysis**: System constraint diagnosis
6. **Deployment Tools**: Ollama, Llama.cpp, vLLM, Chatbox
7. **Optimization Tips**: Low VRAM solutions
8. **Minimum Config Table**: 3B/7B/13B/34B/70B requirements

## Usage

When user asks about running LLMs on their computer:

```
检测电脑配置
大模型推荐
能跑什么模型
硬件检测
LLM优化
```

## Quick Run

```bash
python3 skills/hardware-llm-optimizer/detect.py
```

## Requirements

- Python 3.8+
- psutil: `pip install psutil`
- nvidia-smi (optional, for NVIDIA GPU detection)

## Minimum Config Reference

| Model | Min VRAM | Rec VRAM | Quantization |
|-------|----------|----------|--------------|
| 3B    | 2GB      | 4GB      | Q4          |
| 7B    | 6GB      | 8GB      | Q4/Q8       |
| 13B   | 10GB     | 16GB     | Q4/Q8       |
| 34B   | 20GB     | 32GB     | Q4          |
| 70B   | 40GB     | 80GB     | Q4          |

## Chinese Interface

This skill outputs in Chinese for user convenience.
