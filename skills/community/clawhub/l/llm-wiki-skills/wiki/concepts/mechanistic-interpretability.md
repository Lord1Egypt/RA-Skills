---
title: "Mechanistic Interpretability"
aka: ["机制解释性", "机械可解释性"]
created: 2026-04-09
tags: [concept, field, mechanistic-interpretability]
---

## Overview

**Mechanistic Interpretability** 机制解释性是AI可解释性研究的一个分支，目标是用人类可理解的语言描述神经网络的转换过程。

## 核心目标

1. 理解模型如何计算其输出
2. 识别可解释的构建块（特征）
3. 描述这些构建块如何相互作用（电路）

## 两步方法

### 1. 特征识别 (Feature Identification)
- 找到模型使用的可解释构建块
- 使用SAEs、Transcoders等方法

### 2. 电路发现 (Circuit Discovery)
- 描述特征如何相互作用
- 构建因果图
- 验证机制

## 在本Wiki中的论文

- [[wiki/circuit-tracing]]: Circuit Tracing方法
- [[wiki/biology-large-language-model]]: Claude 3.5 Haiku案例研究
- [[wiki/assistant-axis]]: 角色和人格的机制解释

## 相关技术
- [[wiki/sparse-autoencoder]]
- [[wiki/attribution-graphs]]
- [[wiki/feature-steering]]

## 挑战
- Polysemanticity（多义性）
- Superposition（叠加）
- 大规模模型的复杂度