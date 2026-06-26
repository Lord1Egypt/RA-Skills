---
name: model_router
description: "Model Router - Parallel multi-LLM invocation with result merging. Use when: need better answers, compare model outputs, or get best result from multiple LLMs. / 并行调用多模型 - 并行调用多个大模型，结果智能合并。"
metadata:
  author: "WaaiOn"
  version: "1.0"
  openclaw:
    emoji: "🔀"
    requires:
      bins: ["python3"]
---

# 🔀 Model Router / 模型路由器

Parallel multi-LLM invocation with intelligent result merging. Get the best from multiple models.

## When to Use / 使用场景

| EN | CN |
|----|----|
| Need better answers than single model | 需要比单一模型更好的答案 |
| Compare outputs from different LLMs | 对比不同模型输出 |
| Get best result through ensemble | 通过集成获取最佳结果 |
| Critical tasks requiring reliability | 需要可靠性的关键任务 |

## Workflow / 工作流

```
User Task / 用户任务
       │
       ▼
┌──────────────────┐
│  Parallel Invoke  │  / 并行调用
│  ┌────┬────┬────┐│
│  │GPT4│Claude│Kimi││
│  └────┴────┴────┘│
└──────────────────┘
       │
       ▼
┌──────────────────┐
│   Target Merge    │  / 目标模型合并
│   Target LLM     │
└──────────────────┘
       │
       ▼
   Final Result / 最终结果
```

## Features / 功能

| Feature | EN | CN |
|---------|----|----|
| Parallel invocation | 并行调用多模型 |
| Auto-routing | 自动路由 |
| Result merging | 结果智能合并 |
| Quality assessment | 质量评估 |

## Supported Models / 支持模型

| Model | Provider |
|-------|----------|
| gpt4 | OpenAI |
| claude | Anthropic |
| kimi | 月之暗面 |
| deepseek | 深度求索 |
| qwen | 阿里 |
| ernie | 百度 |
| gemini | Google |

## Usage / 使用

```python
from model_router import Router

# Simple / 简单
result = await Router().run(
    task="写一首关于春天的诗",
    models=["gpt4", "claude", "kimi"],
    merge_model="gpt4"
)

# Advanced / 高级
result = await Router().run(
    task="分析这段代码",
    models=["cursor", "windsurf", "codeium"],
    merge_model="claude",
    timeout=30,
    merge_prompt="合并以下代码审查结果，给出最佳建议"
)
```

## Response / 返回结果

```python
{
    "final": "...",           # 合并后的最终结果
    "sources": [...],         # 各模型原始结果
    "merge_model": "claude",  # 合并用的模型
    "total_time": 2.5         # 总耗时(秒)
}
```

## Installation / 安装

```bash
npx clawhub install model-router-waai
```

## Author / 作者

- WaaiOn
