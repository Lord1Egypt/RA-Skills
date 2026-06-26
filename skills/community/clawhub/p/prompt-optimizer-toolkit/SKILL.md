---
name: prompt-optimizer-toolkit
description: LLM Prompt Engineering Toolkit - 提示词分析、优化、模板化与质量评分 | Analyze, optimize, template, and score your LLM prompts with built-in engineering strategies
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-deps
        kind: python
        requirements: "requirements.txt"
---

# Prompt Optimizer Toolkit

## 功能

- **Analyze** — 多维度分析提示词质量（清晰度、具体性、上下文、约束、示例、角色）
- **Optimize** — 自动检测最佳优化策略并应用
- **Template** — 内置5种经典提示词模板（CoT、Few-shot、Role-play、Structured、Constraints）
- **Library** — 本地提示词库管理，支持标签检索
- **Score** — 1-10分综合质量评分

## 使用

```python
from scripts.prompt_optimizer import PromptOptimizer, PromptLibrary

optimizer = PromptOptimizer()

# 分析提示词
analysis = optimizer.analyze("Write a story about a robot")
# → {'clarity_score': 7, 'specificity_score': 5, 'overall_score': 4, ...}

# 自动优化
better = optimizer.optimize("Write a story about a robot")
# → 添加角色、结构、约束

# 使用模板
prompt = optimizer.apply_template("role_playing", domain="creative writing", task="Write a sci-fi story")

# 提示词库
lib = PromptLibrary()
lib.save("coding-helper", "You are a senior Python developer...", tags=["coding", "python"])
```

## CLI

```bash
python3 scripts/prompt_optimizer.py
```
