---
title: "Circuit Tracing: Revealing Computational Graphs in Language Models"
source: "https://transformer-circuits.pub/2025/attribution-graphs/methods.html"
author: "Transformer Circuits Team"
created: 2026-04-09
tags: [source, paper, circuit-tracing]
---

## Paper Overview

本文介绍了一种名为**Circuit Tracing**的方法，用于揭示语言模型在处理单个提示时的"逐步"计算过程。该方法通过在"替换模型"(replacement model)中追踪单个计算步骤，生成模型计算的图描述。

## Key Concepts

### Replacement Model
- 使用更可解释的组件（这里是"跨层转码器" cross-layer transcoder）来替代底层模型的部分（这里是MLP）
- 转码器经过训练来近似底层模型

### Attribution Graphs
- 生成关于模型使用机制的假设
- 通过后续扰动实验测试和精炼假设

## Key Findings

### Two-Step Approach to Mechanistic Interpretability
1. **识别特征(Features)**: 找到模型计算中使用的可解释构建块
2. **描述过程(Processes/Circuits)**: 描述这些特征如何相互作用以产生模型输出

### The Problem of Polysemanticity
- 模型神经元通常是**多义的(polysemantic)**，表示许多不相关的概念混合
- 原因之一是**叠加(Superposition)**现象
- 模型必须表示比神经元更多的概念，因此必须将概念"涂抹"到许多神经元上

### Solutions: Sparse Coding Methods
- **Sparse Autoencoders (SAEs)**: 将模型激活分解为稀疏活跃组件（"特征"）
- **Transcoders**: 寻找可解释的LLM特征电路
- **Crosscoders**: 跨层特征和模型差异

## Methodology

1. 使用稀疏编码方法识别特征
2. 构建由这些特征组成的电路
3. 使用可视化工具调查attribution graphs
4. 对18层语言模型进行验证

## Related Work
- [[wiki/toy-models-superposition]]: 叠加理论的基础
- [[wiki/scaling-monosemanticity]]: SAEs在大规模模型上的应用
- [[wiki/circuit-tracing-biology]]: 将这些方法应用于Claude 3.5 Haiku

## Significance

本文为机制解释提供了重要的方法论基础，使得研究人员能够：
- 追踪模型的逐步计算过程
- 识别和验证特征交互电路
- 为理解更复杂的模型（如Claude 3.5 Haiku）奠定基础

## Source Files
- Raw source: `D:\obsidian-notebook\raw\Circuit Tracing Revealing Computational Graphs in Language Models.md`