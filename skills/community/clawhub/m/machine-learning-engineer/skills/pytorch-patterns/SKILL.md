---
name: pytorch-patterns
description: PyTorch 工程最佳实践：训练管线、高效数据加载、模型架构设计、可复现实验
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/pytorch-patterns/SKILL.md
  url: https://skills.sh/affaan-m/everything-claude-code/pytorch-patterns
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 工程
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - pytorch
  - training-pipeline
  - data-loading
  - architecture
  - reproducibility
---

# PyTorch Patterns — 工程最佳实践

> 编写健壮、高效、可复现的 PyTorch 训练代码。不是「怎么写模型」，而是「怎么写好模型代码」。

## 能力

- **训练管线设计**：标准训练循环、混合精度、分布式训练接口
- **高效数据加载**：Dataset/DataLoader 优化、预取、内存映射
- **模型架构模式**：模块化设计、参数初始化、权重管理
- **可复现性保证**：随机种子、环境快照、超参记录
- **调试与诊断**：梯度检查、NaN 追踪、内存分析、bottleneck 定位

## 使用方式

在 Claude Code 中使用 `/pytorch-patterns` 调用。

```
/pytorch-patterns 审查我的训练代码，找出效率瓶颈
/pytorch-patterns 重构 DataLoader 以提高 GPU 利用率
/pytorch-patterns 帮我建立可复现的实验框架
```

## 工作流

1. **代码审查** — 检查模型定义、训练循环、数据处理的结构
2. **问题诊断** — 定位瓶颈（CPU/GPU、I/O、内存）
3. **模式应用** — 选择合适的工程模式并实现
4. **验证** — Benchmark 对比、确保精度不降、可复现检查
5. **文档化** — 记录关键决策和性能基线

## 关键模式

| 模式 | 场景 | 收益 |
|------|------|------|
| Lightning 训练器封装 | 标准化训练流程 | 减少样板代码 |
| 预取 + pinned memory | GPU 利用率低 | 提速 2-5x |
| 梯度累积 | 小 batch / 显存不足 | 等效大 batch |
| 混合精度 (AMP) | 大模型训练 | 提速 + 省显存 |
| Checkpoint 管理 | 长训练 / 可恢复 | 不丢进度 |

## 可复现清单

```
[ ] torch.manual_seed(seed) + cuda.manual_seed_all(seed)
[ ] torch.backends.cudnn.deterministic = True
[ ] torch.backends.cudnn.benchmark = False
[ ] DataLoader worker_init_fn 固定
[ ] 记录 PyTorch / CUDA / cuDNN 版本
[ ] wandb / TensorBoard 记录超参和指标
```

## 适用场景

- PyTorch 训练代码运行慢但不知道为什么
- 需要标准化团队/项目中的训练流程
- 从 Jupyter notebook 过渡到结构化训练代码
- GPU 利用率低，想优化数据管线

## 限制

- 不替代 PyTorch Lightning 等高层框架的设计决策
- 分布式训练假设单机多卡，多机场景需额外配置
- 不涉及模型压缩（量化、剪枝、蒸馏）

## 相关参考（Playbook）

- [ml-pipeline-design playbook](../../references/ml-pipeline-design.md) — 训练管线设计与效率优化
- [experiment-reproducibility playbook](../../references/experiment-reproducibility.md) — 可复现实验：种子 / 环境 / 超参记录
- [model-evaluation playbook](../../references/model-evaluation.md) — 可复现的评估实验设计
