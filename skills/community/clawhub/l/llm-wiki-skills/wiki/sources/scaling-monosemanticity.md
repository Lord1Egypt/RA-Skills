---
title: "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet"
source: "https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html"
author: "Transformer Circuits Team"
created: 2026-04-09
tags: [source, paper, monosemanticity, sparse-autoencoder]
---

## Paper Overview

本文展示了如何将稀疏自编码器(Sparse Autoencoders, SAEs)扩展到**Claude 3 Sonnet**——Anthropic的中型生产模型。研究团队成功提取了高质量特征，证明了这一方法可以扩展到最先进的Transformer模型。

## Key Results

### 1. 高度抽象的特征
- 发现多样化的**高度抽象特征**
- 这些特征既对刺激做出反应，又在行为上导致抽象行为

### 2. 特征类型示例
- **名人特征**: 识别著名人物
- **国家和城市特征**: 地理位置相关
- **代码类型签名特征**: 编程相关

### 3. 多语言和多模态特性
- 许多特征是**多语言的**: 对不同语言中的相同概念做出反应
- 许多特征是**多模态的**: 对文本和图像中的相同概念做出反应
- 涵盖同一想法的具体和抽象实例

### 4. 安全相关特征
发现与以下安全相关的内容：
- **安全漏洞和后门代码**
- **偏见**（包括公开的 slurs 和更微妙的偏见）
- **撒谎、欺骗和权力寻求**（包括treacherous turns）
- **谄媚(Sycophancy)**
- **危险/犯罪内容**（如生物武器制造）

## Scaling Laws

- 发现可以使用**缩放定律(scaling laws)**来指导SAEs的训练
- 概念频率与解析特征所需的字典大小之间存在系统性关系

## Steering

- 特征可用于**引导(steer)大型模型**
- 这扩展了先前使用其他方法引导模型的工作

## Methodology

### Linear Representation Hypothesis
- 神经网络将意义概念（称为"特征"）表示为激活空间中的方向

### Superposition Hypothesis
- 神经网络利用高维空间中几乎正交方向的存在来表示比维度更多的特征

### Dictionary Learning
- 使用标准方法——字典学习——从模型激活中提取特征
- 稀疏自编码器是实现这一目标的有效方法

## Comparison with Prior Work

八个月前，团队展示了SAEs可以从小型单层Transformer中恢复 monosemantic特征。当时主要担心这种方法可能无法实际扩展到最先进的Transformer。

本文证明了这种担忧是错误的——SAEs可以成功扩展到像Claude 3 Sonnet这样的大型模型。

## Related Concepts
- [[wiki/toy-models-superposition]]: 理论基础
- [[wiki/sparse-autoencoder]]: 技术细节
- [[wiki/circuit-tracing]]: 因果电路分析

## Source Files
- Raw source: `D:\obsidian-notebook\raw\Scaling Monosemanticity Extracting Interpretable Features from Claude 3 Sonnet.md`