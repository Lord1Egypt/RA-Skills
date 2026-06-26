---
title: "Sparse Autoencoder (SAE)"
aka: ["稀疏自编码器"]
created: 2026-04-09
tags: [concept, technique, sae]
---

## Overview

**Sparse Autoencoder (SAE)** 稀疏自编码器是一种用于从神经网络激活中提取可解释特征的方法。其核心思想是将模型的高维激活分解为稀疏活跃的组件，这些组件通常对应于人类可理解的概念。

## How It Works

### 基本原理
1. 训练一个自编码器来重建模型激活
2. 施加稀疏性约束，使大部分特征为0
3. 得到的"字典"包含可解释的特征

### 与传统神经元的区别
- 传统神经元可能是**多义的(polysemantic)**，混合多个概念
- SAE特征通常是**单义的(monosemantic)**，对应单一概念

## 在本Wiki中的应用

### 关键论文
- [[wiki/scaling-monosemanticity]]: 展示了SAEs如何从Claude 3 Sonnet提取特征
- [[wiki/circuit-tracing]]: 使用SAEs识别特征来构建电路

### 特征类型
- 名人特征
- 地理位置特征
- 代码特征
- 安全相关特征（漏洞、偏见、欺骗等）

## 缩放定律

SAEs可以随模型规模扩展：
- 使用缩放定律指导训练
- 概念频率与字典大小的关系

## Related Concepts
- [[wiki/superposition]]
- [[wiki/transcoder]]
- [[wiki/attribution-graphs]]

## Further Reading
- [[wiki/toy-models-superposition]]: 理论基础