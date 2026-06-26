---
name: nvidia-free-api
slug: nvidia-free-api
version: 1.0.0
description: NVIDIA 免费 API 集成 — 133+ 主流模型，OpenAI 完全兼容
author: openclaw
tags: [nvidia, api, llm, openai-compatible, free]
---

# 🚀 NVIDIA 免费 API 集成

## 概述

基于 NVIDIA 免费 API 积分，提供 **133+ 个主流模型** 的 OpenAI 兼容接口。包括 Llama、DeepSeek、Qwen、Gemma、Mistral、Kimi 等顶级模型。

## 特点

| 特性 | 说明 |
|------|------|
| 🆓 **完全免费** | NVIDIA API 免费积分，无需付费 |
| 🔌 **OpenAI 兼容** | 直接替换 OpenAI API 的 base_url 即可 |
| 🤖 **133+ 模型** | Llama、DeepSeek、Qwen、Gemma、Mistral、Kimi 等 |
| 🔧 **CLI 工具** | 命令行调用、流式输出、嵌入向量 |
| 📦 **即装即用** | 安装即可调用，内置 API Key |

## 安装

```bash
clawhub install nvidia-free-api
```

## 使用

### CLI 命令

```bash
# 列出所有模型
nvidia-api list

# 搜索模型
nvidia-api models llama
nvidia-api models qwen

# 聊天补全
nvidia-api chat "你好" --model meta/llama-3.3-70b-instruct

# 流式输出
nvidia-api stream "写一首诗" --model qwen/qwen2.5-coder-32b-instruct

# 文本嵌入
nvidia-api embed "机器学习是..."
```

### Python SDK 用法

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]  # 从环境变量读取
)

# 聊天
resp = client.chat.completions.create(
    model="meta/llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

## 推荐模型

| 类别 | 模型 | 说明 |
|------|------|------|
| 💬 通用 | `meta/llama-3.3-70b-instruct` | 高性价比主力模型 |
| 🚀 最新 | `meta/llama-4-maverick-17b-128e-instruct` | Llama 4 |
| 🧠 推理 | `deepseek-ai/deepseek-v3.2` | DeepSeek V3 |
| 💻 编程 | `qwen/qwen2.5-coder-32b-instruct` | 代码专用 |
| 🌍 多模态 | `meta/llama-3.2-90b-vision-instruct` | 视觉理解 |
| 🇨🇳 中文 | `moonshotai/kimi-k2-instruct` | Kimi K2 |
| 🧪 轻量 | `microsoft/phi-4-mini-instruct` | 快速轻量 |

## 配置

**重要：使用前需要设置你自己的 API Key**

从 [build.nvidia.com](https://build.nvidia.com/) 注册免费账号获取 Key。

环境变量:


也支持写入 ~/.zshrc 永久生效：


## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-23 | 初始版本：CLI + 133模型 + OpenAI兼容 |
