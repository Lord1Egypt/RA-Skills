---
name: hardware-llm-optimizer
version: 2.0.0
description: AI硬件LLM推荐工具 - 基于llmfit内核。自动检测CPU/GPU/RAM/VRAM → 智能推荐最适合的大模型 + 量化方案 + 速度估算。支持100+模型库，内置TUI界面和硬件模拟。
keywords: [hardware,llm,ai,nvidia,gpu,optimization,quantization,llmfit,ollama]
---

# Hardware LLM Optimizer v2.0
基于 llmfit 的智能硬件LLM推荐工具

## 安装状态

llmfit 已安装在: `/usr/local/bin/llmfit`

## 快速使用

当用户问"能跑什么大模型"、"推荐LLM"、"硬件检测"时使用：

### 1. 查看推荐模型
```bash
llmfit recommend
```

### 2. 查看所有推荐（JSON格式，便于解析）
```bash
llmfit recommend --json
```

### 3. 按用途筛选
```bash
llmfit recommend --use-case coding
llmfit recommend --use-case chat
llmfit recommend --use-case general
llmfit recommend --use-case embedding
```

### 4. 硬件模拟（模拟不同配置）
```bash
# 模拟 16GB 显存
llmfit recommend --memory 16G

# 模拟 32GB 显存 + 64GB RAM
llmfit recommend --memory 32G --ram 64G
```

### 5. 交互式TUI（需要终端）
```bash
llmfit
```

## 输出字段说明

| 字段 | 含义 |
|------|------|
| `name` | 模型名称 |
| `parameter_count` | 参数量 |
| `best_quant` | 推荐量化方案 |
| `score` | 综合评分（越高越好）|
| `estimated_tps` | 预估速度（tok/s）|
| `memory_required_gb` | 所需显存 |
| `run_mode` | 运行模式（GPU/CPU/MoE）|
| `fit_level` | 匹配度（Perfect/Good/Marginal）|

## 量化方案参考

| 量化 | 质量 | 速度 | 适用场景 |
|------|------|------|---------|
| FP16 | 最高 | 最慢 | 大显存GPU |
| Q8_0 | 很高 | 较快 | 中等显存 |
| Q6_K | 高 | 快 | 6-8GB显存 |
| Q4_K_M | 中高 | 最快 | 4-6GB显存 |
| Q2_K | 中 | 最快 | <4GB显存 |

## 本地运行命令

### 安装Ollama模型
```bash
ollama run <model-name>
```

### 使用llama.cpp
```bash
# 下载GGUF后
./llama.cpp -m <model.gguf> --rompt <prompt>
```

## 最低配置参考（来自llmfit）

| 显存 | 推荐模型 | 量化 |
|------|---------|------|
| 2GB | Phi-3-mini, Gemma-2B | Q4 |
| 4GB | Llama3-8B, Qwen-7B | Q4 |
| 6GB | Llama2-13B, Mistral-7B | Q4/Q6 |
| 8GB | Llama2-13B, Yi-9B | Q5/Q6 |
| 12GB | Llama2-34B | Q4 |
| 16GB | Llama2-34B, Qwen-72B | Q4 |
| 24GB+ | 70B大模型 | Q4/Q8 |

## 安装llmfit（如需）

```bash
curl -fsSL https://llmfit.axjns.dev/install.sh | sh
```

## 优势对比

| 功能 | v1.0 | v2.0 (llmfit) |
|------|-------|----------------|
| 模型库 | 手动查表 | 100+自动匹配 |
| 量化推荐 | 简单估算 | 智能最优 |
| 速度估算 | ❌ | ✅ |
| 下载源 | ❌ | ✅ GGUF |
| 硬件模拟 | ❌ | ✅ |
| TUI界面 | ❌ | ✅ |
| 多GPU | ❌ | ✅ |
| MoE支持 | ❌ | ✅ |

*Powered by llmfit | Updated: 2026-04-17*
