---
title: "Toy Models of Superposition"
source: "https://transformer-circuits.pub/2022/toy_model/index.html"
author: "Transformer Circuits Team"
created: 2026-04-09
tags: [source, paper, superposition, toy-models]
---

## Paper Overview

本文使用**toy models**——在合成数据上训练的小型ReLU网络——来研究模型如何表示比其维度更多的特征。这一现象被称为**叠加(Superposition)**。

## Key Motivation

### The Ideal vs Reality
- 理想情况：每个神经元对应一个清晰可解释的输入特征
- 实际情况：在大型语言模型中，神经元对应清晰特征的情况很少见

### Questions Explored
1. 为什么神经元有时与特征对齐，有时不对齐？
2. 为什么一些模型和任务有很多干净的神经元，而在其他模型中却很少？

## Key Findings

### Superposition
当特征稀疏时，叠加允许超越线性模型的压缩，代价是需要非线性过滤的"干扰"。

### Key Insights

1. **Dense Features**: 模型学习表示最重要的两个特征的正交基（类似PCA）
2. **Sparse Features**: 模型可以存储额外的特征，通过容忍一些干扰

### Computation in Superposition
- 模型不仅可以在叠加中存储额外特征
- 还可以执行计算
- 例如：模型可以在叠加中放置计算绝对值函数的简单电路

### Hypothesis
- 我们训练的模型可以被认为是"做同样的事情"一个假想的更大的模型
- 表示完全相同的特征，但没有干扰

## Relationship to Prior Work

Superposition并非新想法，与以下领域密切相关：
1. **Compressed Sensing** (数学)
2. **Distributed/Dense/Population Codes** (神经科学)
3. **Representation Learning** (深度学习)

## Key Concepts

### Polysemanticity
- 神经元表示多个不相关概念的混合
- 原因之一是叠加现象
- 特征被"涂抹"到多个神经元上

### Feature Representation
- 特征在激活空间中表示为方向
- 使用稀疏编码可以提取这些特征
- 稀疏自编码器(SAEs)是实现这一目标的方法

## Significance

本文奠定了机制解释的理论基础：
1. 解释了为什么神经元不一定对应特征
2. 提出了叠加假说
3. 为后续SAE和特征提取工作提供理论基础

## Related Papers
- [[wiki/scaling-monosemanticity]]: 基于叠加理论的特征提取
- [[wiki/circuit-tracing]]: 使用特征构建电路
- [[wiki/sparse-autoencoder]]: 技术实现

## Source Files
- Raw source: `D:\obsidian-notebook\raw\Toy Models of Superposition.md`