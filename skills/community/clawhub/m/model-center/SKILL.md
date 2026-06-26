---
name: model-center
description: Unified interface to 42+ NVIDIA NIM API models — LLM chat, vision, embeddings, image generation, with price comparison and model recommendation.
version: 1.0.0
tags:
  - nvidia
  - ai
  - llm
  - api
  - models
  - nim
category: "Data & APIs"
metadata:
  openclaw:
    requires:
      env:
        - NVIDIA_API_KEY
      bins:
        - python
    primaryEnv: NVIDIA_API_KEY
    envVars:
      - name: NVIDIA_API_KEY
        required: true
        description: NVIDIA NIM API key from https://build.nvidia.com
    emoji: 🤖
    homepage: https://build.nvidia.com
---

# NVIDIA AI Model Center

A Python skill that provides a unified interface to **42+ NVIDIA NIM API models** — LLM chat, vision analysis, text embeddings, image generation, and more.

## Quick Start

```python
from model_center import ModelCenter

center = ModelCenter()

# List all models
models = center.list_models()
print("Available categories:", list(models.keys()))

# Get model info
info = center.get_model_info('nemotron-3-super-8b')
print(f"Model: {info['name']}, Provider: {info['provider']}")

# Compare pricing
comparisons = center.compare_pricing(['nemotron-3-super-8b', 'llama-3.1-70b-instruct'])
for c in comparisons:
    print(f"{c['name']}: ${c['input_price']}/M in, ${c['output_price']}/M out")

# Get recommendations
rec = center.recommend_model('code generation', 'low', False)
print(f"Recommended: {rec}")

# Estimate cost
cost = center.estimate_cost('nemotron-3-super-8b', 1000, 500)
print(f"Estimated cost: ${cost['total_cost']}")

# Chat with a model (requires NVIDIA_API_KEY env var)
# response = center.chat_completion(
#     model='nemotron-3-super-8b',
#     messages=[{'role': 'user', 'content': 'Hello'}],
#     temperature=0.7,
#     max_tokens=100
# )
```

## Setup

1. Get an API key from [build.nvidia.com](https://build.nvidia.com)
2. Set the `NVIDIA_API_KEY` environment variable:
   ```powershell
   $env:NVIDIA_API_KEY = "nvapi-..."
   ```
3. Install dependency: `pip install requests`
4. Import and use `ModelCenter` or `NVIDIAAPIClient` from `model_center.py`

## API

### ModelCenter

| Method | Description |
|--------|-------------|
| `list_models(category)` | List all models or by category |
| `get_model_info(model_id)` | Get detailed model information |
| `compare_pricing(model_ids)` | Compare pricing across models |
| `recommend_model(use_case, budget, need_vision)` | AI-powered model recommendation |
| `estimate_cost(model, input_tokens, output_tokens)` | Estimate API call cost |
| `chat_completion(model, messages, ...)` | Chat completion API call |
| `generate_image(model, prompt, ...)` | Image generation API call |
| `get_embedding(model, input_text)` | Embedding API call |
| `chat(model, message, system_prompt)` | Simple chat interface |

### Categories

- **llm**: Chat completion models (Nemotron, Llama, Mixtral, etc.)
- **vision**: Image understanding models
- **embedding**: Text embedding models
- **image**: Image generation models
- **moderation**: Content moderation models

## Source

The implementation lives in `model_center.py` (548 lines) in this skill directory.

## 触发场景
- 用户说"模型中心"、"NVIDIA NIM"、"API模型"
- 用户说"LLM API"、"模型对比"、"选择模型"
- 用户说"模型推荐"、"价格对比"


## B站学习
> 学习时间: 2026-06-01 20:57

- **u-blox**: u-center 2系列视频1：如何下载、安装以及首次运行u-center 2
  - 关键词: center, 2系列视频1, 如何下载, 安装以及首次运行u, center
- **大虾试车真香**: 【大虾沉浸式试驾】Model 3长续航全轮驱动版 👉百公里加速·隔音·电耗全知道！
  - 关键词: 大虾沉浸式试驾, Model, 3长续航全轮驱动版, 百公里加速, 隔音

## B站学习
> 学习时间: 2026-06-01 21:02

- **u-blox**: u-center 2系列视频1：如何下载、安装以及首次运行u-center 2
- **大虾试车真香**: 【大虾沉浸式试驾】Model 3长续航全轮驱动版 👉百公里加速·隔音·电耗全知道！
- **星之许愿树**: 无人机gps参数修改 u-center下修改gnss等其他参数 最近比较忙 下面闲了 会承诺出ardupilot的直升机固件

## 融合来源: model-center-e9fd16
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:08
- **sodoi7788**: a702a8e4361a57f9fd182c7231ce9600
- **user_87735434675**: 7e815722-c5d8-45fd-9c19-a1d6870e3df2
- **东莞小学生朗读大赛**: 3402_trim.5E7DA9DE-FD16-44E0-9D35-F008CEF6839C

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:21

- **u-blox**: u-center 2系列视频1：如何下载、安装以及首次运行u-center 2
  https://www.bilibili.com/video/BV1yCeKeqEXu
- **大虾试车真香**: 【大虾沉浸式试驾】Model 3长续航全轮驱动版 👉百公里加速·隔音·电耗全知道！
  https://www.bilibili.com/video/BV1ox421Z7im
- **星之许愿树**: 无人机gps参数修改 u-center下修改gnss等其他参数 最近比较忙 下面闲了 会承诺出ardupilot的直升机固件
  https://www.bilibili.com/video/BV1BB4y1q7KT

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:34

- **u-blox**: u-center 2系列视频1：如何下载、安装以及首次运行u-center 2
  https://www.bilibili.com/video/BV1yCeKeqEXu
- **大虾试车真香**: 【大虾沉浸式试驾】Model 3长续航全轮驱动版 👉百公里加速·隔音·电耗全知道！
  https://www.bilibili.com/video/BV1ox421Z7im
- **星之许愿树**: 无人机gps参数修改 u-center下修改gnss等其他参数 最近比较忙 下面闲了 会承诺出ardupilot的直升机固件
  https://www.bilibili.com/video/BV1BB4y1q7KT
