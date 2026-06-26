# Prompt Optimizer Toolkit

> 中英文双语 | Bilingual Documentation

---

## English

A comprehensive toolkit for LLM prompt engineering. Analyze, optimize, template, and score your prompts to get better results from any language model.

### Features

- **Multi-dimensional Analysis** — clarity, specificity, context, constraints, examples, role, structure
- **Auto-Optimization** — detects the best strategy and applies it automatically
- **Template Library** — Chain-of-Thought, Few-shot, Role-playing, Structured Output, Constraints
- **Prompt Library** — local storage with tag-based search
- **Quality Scoring** — 1-10 overall score with actionable improvement suggestions

### Quick Start

```python
from scripts.prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()
analysis = optimizer.analyze("Your prompt here")
optimized = optimizer.optimize("Your prompt here")
suggestions = optimizer.suggest_improvements("Your prompt here")
```

## 中文

LLM提示词工程综合工具包。分析、优化、模板化和评分你的提示词，从任何语言模型获得更好的结果。

### 功能特性

- **多维度分析** — 清晰度、具体性、上下文、约束条件、示例、角色、结构
- **自动优化** — 检测最佳策略并自动应用
- **模板库** — 思维链、少样本、角色扮演、结构化输出、约束模板
- **提示词库** — 本地存储，支持标签搜索
- **质量评分** — 1-10分综合评分，附带可操作的改进建议

### 快速开始

```python
from scripts.prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()
analysis = optimizer.analyze("你的提示词")
optimized = optimizer.optimize("你的提示词")
suggestions = optimizer.suggest_improvements("你的提示词")
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
python3 -m pytest tests/ -v
```
