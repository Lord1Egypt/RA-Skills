---
title: "Activation Oracles: Training and Evaluating LLMs as General-Purpose Activation Explainer"
source: "https://arxiv.org/pdf/2512.15674"
author: "Adam Karvonen, James Chua, Clément Dumas, Kit Fraser-Taliente, Julian Minder, Euan Ong, Arnab Sen Sharma, Daniel Wen, Owain Evans, Samuel Marks"
created: 2026-04-09
tags: [source, paper, activation-oracles]
---

## Paper Overview

本文提出了一种名为**Activation Oracles (AOs)**的新方法，用于解释大型语言模型(LLM)的激活。与传统使用复杂专业方法解释激活不同，Activation Oracles采用更简单的方法：**训练LLM直接接受LLM激活作为输入，并用自然语言回答关于激活的任意问题**。

这种方法基于**LatentQA**框架，但之前的工作主要关注狭窄的任务设置。本文采取更通用的视角，在远离训练分布的设置中评估LatentQA训练的模型，并研究性能如何随训练数据多样性扩展。

## Key Findings

### 1. 可以恢复未在输入文本中出现的微调信息
- AOs可以恢复** biographical knowledge**（传记知识）或**malign propensities**（恶意倾向）
- 这些信息是通过微调注入模型的，但从未在输入文本中出现
- 即使从未使用过来自微调模型的激活进行训练，AOs也能恢复这些信息

### 2. 训练数据多样性的重要性
- 即使是**narrowly trained**（窄范围训练）的LatentQA模型也能很好地泛化
- 添加额外的训练数据集（如分类任务和自监督上下文预测任务）可以持续进一步改进
- 多样化训练赋予回答自然语言查询的一般能力

### 3. 性能评估
- 在四个下游任务中进行评估，可与之前的白盒和黑盒技术比较
- 即使是窄范围训练的模型也表现良好
- 最佳AOs在4个任务中的**3个**匹配或超过最佳总体基线

## Method

### LatentQA框架
- 训练模型直接接受LLM激活作为输入
- 用自然语言回答关于激活的问题
- 不需要复杂的专门解释方法

### 训练策略
1. **Narrow training**: 专注于特定任务
2. **Diversified training**: 添加多种训练数据集
   - 分类任务
   - 自监督上下文预测任务

## Significance

这项研究表明：
- 训练LLM用自然语言回答关于激活的问题可以赋予**通用能力**
- 这种方法比复杂的专业方法更简单但同样有效
- 为AI可解释性和安全评估提供了新工具

## Related Concepts
- [[wiki/sparse-autoencoder]]
- [[wiki/feature-steering]]
- [[wiki/mechanistic-interpretability]]
- [[wiki/attribution-graphs]]

## Source Files
- Raw source: `D:\obsidian-notebook\raw\ACTIVATION ORACLES= TRAINING AND EVALUATING LLMS AS GENERAL-PURPOSE ACTIVATION EXPLAINERS.md`