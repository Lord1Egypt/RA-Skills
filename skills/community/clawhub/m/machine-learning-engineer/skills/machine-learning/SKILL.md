---
name: machine-learning
description: ML 全流程开发：JAX、特征工程、模型选择、评估与调优，从数据到生产级模型
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/machine-learning/SKILL.md
  url: https://skills.sh/mindrally/skills/machine-learning
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: ML
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - machine-learning
  - jax
  - scikit-learn
  - feature-engineering
  - model-evaluation
---

# Machine Learning — 机器学习全流程

> 从原始数据到可部署模型，覆盖特征工程、模型选择、超参调优和评估的完整 ML 工作流。

## 能力

- **ML 全流程开发**：JAX 功能编程范式、高性能计算
- **特征工程**：数值/类别特征处理、特征交叉、降维
- **模型选择**：Scikit-learn 经典模型 → XGBoost → JAX 高阶模型
- **评估与调优**：交叉验证、超参搜索、模型可解释性分析
- **实验管理**：追踪实验参数、指标和产出，支持对比分析

## 使用方式

在 Claude Code 中使用 `/machine-learning` 调用。

```
/machine-learning 帮我设计一个二分类问题的特征工程方案
/machine-learning 比较 XGBoost 和 LightGBM 在这个数据集上的适用性
/machine-learning 对当前模型做超参调优和交叉验证
```

## 工作流

1. **数据理解** — 数据集概览：特征类型、缺失情况、目标分布
2. **特征工程** — 编码、缩放、特征构造、特征选择
3. **基线建模** — 建立简单基线（逻辑回归/决策树），评估基准指标
4. **模型提升** — 逐步尝试更复杂模型，记录每次提升幅度
5. **调优评估** — 交叉验证、超参搜索、最终模型评估报告

## 模型选择决策树

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 快速基线 | Logistic Regression | 简单可解释 |
| 表格数据 | XGBoost / LightGBM | 高精度，处理缺失值 |
| 高维稀疏 | Linear SVC | 适合文本/稀疏特征 |
| 需要可解释性 | Decision Tree / SHAP | 路径清晰 |
| 大规模数据 | JAX / Flax | 高性能数值计算 |

## 适用场景

- 从零开始构建 ML 项目，不确定技术选型
- 已有基线模型，需要系统性提升性能
- 需要建立标准化的 ML 实验流程
- 评估不同模型在同一数据集上的表现

## 限制

- 不覆盖强化学习和生成模型（参见 deep-learning-pytorch）
- 不直接处理非结构化数据（图像用 computer-vision-opencv）
- 大规模分布式训练需要额外的基础设施知识

## 相关参考（Playbook）

- [experiment-reproducibility playbook](../../references/experiment-reproducibility.md) — 实验可复现：种子 / 环境 / 数据版本化
- [ml-pipeline-design playbook](../../references/ml-pipeline-design.md) — 训练管线与工程化设计模式
- [model-evaluation playbook](../../references/model-evaluation.md) — 指标选择与防泄漏验证
