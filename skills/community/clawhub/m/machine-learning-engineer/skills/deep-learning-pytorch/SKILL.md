---
name: deep-learning-pytorch
description: PyTorch 深度学习：Transformers、扩散模型、LLM 开发，含 HuggingFace 生态和 Gradio 部署
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/deep-learning-pytorch/SKILL.md
  url: https://skills.sh/mindrally/skills/deep-learning-pytorch
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 深度学习
  platform: 通用
  difficulty: 专家
  version: 1.0.0
  created: 2026-07-30
tags:
  - deep-learning
  - pytorch
  - transformers
  - diffusion
  - llm
---

# Deep Learning PyTorch — 深度学习

> 使用 PyTorch、HuggingFace Transformers、Diffusers 和 Gradio 构建现代深度学习应用，覆盖 Transformer、扩散模型和 LLM。

## 能力

- **PyTorch 开发**：自定义模型、训练循环、梯度管理、混合精度
- **Transformers 微调**：HuggingFace 模型加载、微调策略、序列分类
- **扩散模型**：Stable Diffusion 推理与微调、图像生成管线
- **LLM 应用开发**：推理优化、Prompt 工程集成、量化部署
- **Gradio 部署**：快速构建 ML 应用 UI，模型演示和分享

## 使用方式

在 Claude Code 中使用 `/deep-learning-pytorch` 调用。

```
/deep-learning-pytorch 帮我微调一个文本分类模型（BERT/RoBERTa）
/deep-learning-pytorch 用 Stable Diffusion 构建一个图像生成流水线
/deep-learning-pytorch 将模型导出为 ONNX 并部署到生产环境
```

## 工作流

1. **模型选择** — 根据任务选基线模型（BERT/ResNet/SD/GPT）
2. **数据准备** — Dataset + DataLoader，预处理和增强
3. **训练配置** — 优化器、学习率调度、early stopping、混合精度
4. **训练监控** — Loss 曲线、验证指标、梯度检查、TensorBoard
5. **推理部署** — 模型导出（ONNX/TorchScript）、Gradio 演示

## PyTorch 训练模板

```python
# 标准训练循环骨架
model.train()
for epoch in range(epochs):
    for batch in train_loader:
        optimizer.zero_grad()
        loss = model(batch).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
```

## 适用场景

- 从 PyTorch 开始第一个深度学习项目
- 微调预训练模型（BERT、GPT、ViT 等）到自己的数据
- 构建图像生成或文本生成应用
- 需要快速搭建模型演示（Gradio）

## 限制

- 不覆盖 JAX/TensorFlow/Keras 等其他框架
- 大模型训练（>7B 参数）需要分布式训练基础设施
- Transformer 推理优化建议结合 vLLM 等专用工具

## 相关参考（Playbook）

- [ml-pipeline-design playbook](../../references/ml-pipeline-design.md) — 训练管线、分布式扩容与工程化
- [model-evaluation playbook](../../references/model-evaluation.md) — 模型验证与防泄漏评估
- [experiment-reproducibility playbook](../../references/experiment-reproducibility.md) — 训练可复现：种子 / 环境 / 数据版本
