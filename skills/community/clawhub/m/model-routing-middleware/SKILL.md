---
name: model-routing-middleware
version: 1.0.0
description: "Intelligent model selection middleware for AI agents. Route tasks to the best model, manage context, and cut API costs 40-70%."
license: MIT
tags: [model-routing, llm, cost-optimization, middleware, agent, context-management, escalation]
source: el-rudo-larios/model-routing
trigger: "model routing LLM selection cost optimization middleware agent"
metadata:
  openclaw:
    emoji: "🧭"
---

# Model Routing — Intelligent Model Selection Middleware

Automatically select the best LLM model and think mode based on task type, context size, and response confidence. Cut API costs 40-70% by routing simple tasks to fast models and complex tasks to capable ones.

## How It Works

```
User message → Task Classifier → Model Router → Best Model → Response
                                     ↓
                          Low confidence? → Escalate to stronger model
```

## Quick Start

```yaml
# config.yaml
models:
  casual_chat:
    model: qwen3-14b
    think: false
  coding:
    model: qwen-coder
    think: true
  reasoning:
    model: deepseek-r1
    think: true
  long_context:
    model: glm-5.1
    think: false
```

```python
from router import get_router

router = get_router()
result = await router.route("Write a Python web scraper")
# → Routes to qwen-coder with think=True
```

## Features

- Task-type classification (coding, reasoning, chat, summarization)
- Per-model think mode configuration
- Confidence-based escalation (retry with stronger model)
- Context management and compaction at 55% threshold
- Hot-reload configuration (no restart needed)
- 83 tests passing

## Cost Savings

| Task Type | Without Routing | With Routing | Savings |
|-----------|----------------|--------------|---------|
| Casual chat | GPT-4 ($0.03/1K) | Qwen3-14B (local) | ~100% |
| Coding | GPT-4 ($0.03/1K) | Qwen-Coder (local) | ~95% |
| Hard reasoning | GPT-4 ($0.03/1K) | DeepSeek-R1 (local) | ~90% |

## License

MIT
