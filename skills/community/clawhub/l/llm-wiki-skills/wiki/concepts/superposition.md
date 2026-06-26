---
title: "Superposition"
aka: ["叠加"]
created: 2026-04-09
tags: [concept, theory, superposition]
---

## Overview

**叠加(Superposition)** 是一种现象，指神经网络表示比其维度更多的特征。这是通过将多个特征"涂抹"到相同的神经元上来实现的。

## 核心思想

### 问题
- 神经网络只有有限数量的神经元
- 但需要表示的概念（特征）可能比神经元多得多

### 解决方案
- 特征不一定要正交
- 可以通过线性组合表示多个特征
- 代价是"干扰(interference)"

## Toy Models 论文

[[wiki/toy-models-superposition]] 使用toy models研究这一现象：
- 稀疏特征可以通过叠加存储额外信息
- 模型可以在叠加中执行计算
- 这解释了为什么神经元通常不对应单个特征

## 与SAEs的关系

- SAEs是解决叠加问题的一种方法
- 通过稀疏编码将叠加的特征分解为可解释的单元

## Related Concepts
- [[wiki/sparse-autoencoder]]
- [[wiki/polysemanticity]]
- [[wiki/monosemanticity]]

## Further Reading
- [[wiki/toy-models-superposition]]
- [[wiki/scaling-monosemanticity]]