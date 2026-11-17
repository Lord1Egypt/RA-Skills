---
name: agent-evaluation
description: 评估 AI Agent / LLM Agent 的输出质量与行为：工具调用准确性、答案质量、成本与稳定性；用数据集+评分器+追踪做系统化评测。触发词："agent 评估、agent evaluation、LLM 评测、工具调用准确率、ragas、mlflow evaluate、llm-as-judge、评分器、评测数据集、agent 回归测试"。
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/agent-evaluation/SKILL.md
  url: https://skills.sh/mlflow/skills/agent-evaluation
  version: 1.0.0
  updated: 2026-10-08
metadata:
  author: hope
  category: ML
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-10-08
tags:
  - agent-evaluation
  - llm-eval
  - mlflow
  - ragas
  - llm-as-judge
  - tool-use
---

# Agent 评估 — 系统化评测你的 AI Agent

> 把"我觉得这个 Agent 变好了"变成可量化、可复现的评测结论：工具选得对不对、答案准不准、成本与稳定性如何。

衍生自社区技能 `mlflow/skills@agent-evaluation`（skills.sh 803 安装，MLflow 官方 GenAI 评测导向）。
本技能只做路由与能力索引，完整评测工作流、评分器约束、数据集构建命令见
[agent-evaluation playbook](../../references/agent-evaluation.md)。

## 能力

- **评测规划**：先问清 Agent 做什么、最该做对的 2–3 件事、已知失败模式，再定评测优先级
- **评分器（scorer）**：用内置评分器或 `@scorer` / `make_judge` 定义代码检查与 LLM 裁判，覆盖工具调用准确率、答案质量、安全/合规
- **数据集**：从真实语料或生产日志合成 50–200+ 条评测样本，先 5 条 sanity check 再放大
- **执行与回归**：用 `mlflow.genai.evaluate` 跑全流程，先 dry-run 3 条验证工具/评分器，再全量
- **结果分析**：按评分器出通过率、失败模式与改进建议，做版本/模型对比

## 何时用 / 何时不用

- **用**：Agent 上线前验收、提示词/模型/工具改动后的回归、想把"变好"用指标证明
- **不用**：纯一次性问答手调（直接试即可）；与 MLflow/LangSmith/RAGAS 等评测框架无关的纯业务验收，请结合人工判断

## 使用方式

```
/agent-evaluation 给这个 RAG Agent 做回归评测，重点看检索工具调用准不准
/agent-evaluation 这个 Agent 改了提示词，帮我跑 100 条对比新旧版本
/agent-evaluation 评分器分数为什么全是 0？帮我排查
```

## 工作流

1. **访谈定边界**：做什么 / 最该做对的 2–3 件事 / 已知失败模式 → 写 `agent_description`。
2. **注册评分器套件**：每条标准选最便宜的实现（代码检查 vs 内置 vs LLM 裁判）。
3. **数据集**：先发现已有数据集；没有就先造 5 条 sanity，再合成/采 50–200+ 条。
4. **Dry-run 3 条**：确认工具被调用、响应非空、评分器非零（否则停手修）。
5. **全量评测**：`mlflow.genai.evaluate` → 分析报告与改进项，做版本对比。

## 与其他技能协作

- 想评测"技能本身质量" → `skills-repo/skill-quality-inspector`
- 想做可复现实验基线 → [references/experiment-reproducibility.md](../../references/experiment-reproducibility.md)
- 模型指标与数据泄漏排查 → [references/model-evaluation.md](../../references/model-evaluation.md)
