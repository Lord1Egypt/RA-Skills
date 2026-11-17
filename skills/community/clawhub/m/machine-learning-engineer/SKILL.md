---
name: machine-learning-engineer
description: >-
  机器学习工程师技能库：ML 全流程、深度学习（PyTorch）、计算机视觉、PyTorch 工程实践。
  覆盖可复现实验、模型评估防泄漏、训练管线设计，以及数据集泄漏检测。
  触发词："machine-learning、deep-learning-pytorch、computer-vision-opencv、pytorch-patterns、claude-agent-sdk、claude-api、agent-sdk、工具调用、构建 Agent、可复现、模型评估、训练管线、数据泄漏"。
agent_created: true
metadata:
  version: 1.0.0
  category: 机器学习
  difficulty: 进阶
  architecture: superpower
---

# 机器学习工程师

> 把 AI 助手变成一名 ML 工程搭档：从简单基线到深度学习，从训练循环到可复现实验。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中
**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 设计可复现的 ML 实验（种子/版本/配置/数据版本）
- 选择评估指标、搭建验证、排查数据泄漏
- 设计高效训练管线、数据加载与检查点策略
- 检查数据集切分是否泄漏、类别是否漂移

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列
`references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 实验可复现性（种子/版本/配置/数据版本） | [references/experiment-reproducibility.md](references/experiment-reproducibility.md) | 可复现 随机种子 环境版本 配置管理 数据版本 实验追踪 |
| 模型评估框架（指标/验证/基线/泄漏） | [references/model-evaluation.md](references/model-evaluation.md) | 模型评估 指标 验证 基线 数据泄漏 校准 |
| ML 管线设计（训练循环/数据加载/检查点） | [references/ml-pipeline-design.md](references/ml-pipeline-design.md) | ml 管线 训练循环 数据加载 检查点 分布式 训练 |
| 计算机视觉：OpenCV+PyTorch 图像/视频处理、检测、分割 | [skills/computer-vision-opencv/SKILL.md](skills/computer-vision-opencv/SKILL.md) | 计算机视觉 opencv 图像 视频 目标检测 分割 特征提取 |
| PyTorch 深度学习：Transformers、扩散模型、LLM 开发 | [skills/deep-learning-pytorch/SKILL.md](skills/deep-learning-pytorch/SKILL.md) | pytorch 深度学习 transformer 扩散模型 llm gradio 部署 |
| ML 全流程：JAX、特征工程、模型选择与评估 | [skills/machine-learning/SKILL.md](skills/machine-learning/SKILL.md) | 机器学习 jax scikit-learn 特征工程 模型选择 评估 调优 |
| PyTorch 工程实践：训练管线、数据加载、架构设计 | [skills/pytorch-patterns/SKILL.md](skills/pytorch-patterns/SKILL.md) | pytorch 工程 训练管线 数据加载 模型架构 可复现 |
| 用 Claude API / Agent SDK 构建 AI 应用与 Agent：Messages API、流式、工具调用、Agent 编排（代码骨架/决策树/踩坑见 playbook） | [skills/claude-agent-sdk/SKILL.md](skills/claude-agent-sdk/SKILL.md) [references/claude-api-playbook.md](references/claude-api-playbook.md) | claude-api anthropic agent-sdk 工具调用 构建agent 流式 llm 应用 playbook 踩坑 |
| 生成 MCP Server（让 Agent 调用你的工具/数据）：stdio/streamable-http 脚手架、tool/resource/prompt 定义、MCP Inspector 调试 | [skills/mcp-server-generation/SKILL.md](skills/mcp-server-generation/SKILL.md) [references/mcp-server-generation.md](references/mcp-server-generation.md) | mcp server 生成 工具 协议 stdio streamable-http fastmcp 脚手架 agent 上下文 调试 |
| 评估 AI Agent 输出质量与行为（工具调用准确率/答案质量/回归）：数据集+评分器+追踪系统化评测 | [skills/agent-evaluation/SKILL.md](skills/agent-evaluation/SKILL.md) [references/agent-evaluation.md](references/agent-evaluation.md) | agent 评估 llm 评测 工具调用准确率 ragas mlflow evaluate llm-as-judge 评分器 回归测试 |

> 路由规则：方法论 / 评估类任务读 `references/`；要落地具体动作（训 CV、写 PyTorch、做 ML、查泄漏）直接调 `skills/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/dataset_split_check.py train.csv test.csv [--target 列] [--json] [--strict]` — 检测训练/测试集行重叠（泄漏）、类别分布漂移、缺失值。

运行示例：

```bash
python3 scripts/dataset_split_check.py data/train.csv data/test.csv --target label --strict
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/ml-experiment-template.md](assets/ml-experiment-template.md) — 实验记录模板（元信息/配置/数据/指标/结论）。

## 核心原则（始终遵循）

1. **从简单基线开始**：先规则/线性，再上深度模型。
2. **可复现优先**：固定种子、锁版本、版本化数据。
3. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜 API。
4. **关注数据质量**：数据决定上限，模型决定逼近速度。
5. **明确边界**：只出评估与建议，不替用户拍板上线。

## 与其他技能协作

- 需要把模型做成服务/产品 → 调用 `skills-repo/ai-fullstack-engineer`
- 需要数据工程基础设施 → 调用 `skills-repo/infrastructure-engineer`
