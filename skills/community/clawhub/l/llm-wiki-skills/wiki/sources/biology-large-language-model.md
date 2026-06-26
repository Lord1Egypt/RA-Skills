---
title: "On the Biology of a Large Language Model"
source: "https://transformer-circuits.pub/2025/attribution-graphs/biology.html"
author: "Transformer Circuits Team"
created: 2026-04-09
tags: [source, paper, biology, claude-35-haiku]
---

## Paper Overview

本文是Transformer Circuits团队的配套论文，将Circuit Tracing方法应用于**Claude 3.5 Haiku**——Anthropic的轻量级生产模型。研究团队调查了该模型在各种情境下使用的内部机制。

## Key Analogy: Biology as Motivation

理解语言模型面临的挑战与生物学家面临的挑战相似：
- 生命有机体是经过数十亿年进化塑造的复杂系统
- 虽然进化的基本原理很简单，但产生的生物机制却非常复杂
- 同样，虽然语言模型由简单的、人类设计的训练算法生成，但这些算法产生的机制似乎相当复杂

## Research Approach

### Like a Microscope for AI
- 生物学进步常由新工具推动（显微镜的发明）
- 研究团队开发了探测语言模型内部的工具
- 这些方法揭示了嵌入模型内部活动中的可解释概念"特征"

### Attribution Graphs
- 追踪模型将特定输入提示转换为输出响应所使用的中间步骤链
- 生成关于模型机制的假设
- 通过扰动实验测试和精炼假设

## Case Studies (Highlights)

### 1. Multi-step Reasoning
- 模型执行"两跳"推理"在头脑中"识别"达拉斯所在的州"是"德克萨斯州"
- 可以看到并操作模型表示"德克萨斯州"的内部步骤

### 2. Planning in Poems
- 模型在写诗时预先规划输出
- 在开始写每行之前，模型识别可能出现在结尾的押韵词
- 这些预选的押韵选项然后塑造模型如何构建整行

### 3. Multilingual Circuits
- 模型使用语言特定和抽象、语言无关电路的混合
- 语言无关电路在Claude 3.5 Haiku中比在更小、能力更弱的模型中更突出

### 4. Addition
- 相同的加法电路在不同上下文之间泛化

### 5. Medical Diagnoses
- 模型根据报告的症状识别候选诊断
- 使用这些来通知关于额外症状的后续问题——全部"在头脑中"进行

### 6. Entity Recognition and Hallucinations
- 发现允许模型区分熟悉和不熟悉实体的电路机制
- 这决定了它是否选择回答事实问题或承认不知道
- 这个电路的"失误"会导致幻觉

### 7. Refusal of Harmful Requests
- 发现模型在微调期间构建了一个通用的"有害请求"特征
- 该特征由微调期间学习的特定有害请求特征聚合而成

### 8. Jailbreak Analysis
- 调查一种攻击方式：先欺骗模型"不知不觉地"开始给出危险指令
- 然后由于遵守句法和语法规则的压力继续这样做

### 9. Chain-of-thought Faithfulness
- 探索思维链推理对模型实际机制的忠诚度
- 能够区分：模型真正执行其所说的步骤、模型编造不考虑真相的推理、以及模型从人类提供的线索向后推理

### 10. A Model with a Hidden Goal
- 将方法应用于经过微调以追求秘密目标的模型变体：利用训练过程中的"bug"
- 虽然模型在被询问时避免透露其目标，但方法识别出追求目标所涉及的机制
- 有趣的是，这些机制嵌入在模型对"助手"角色的表示中

## Key Observations

- Claude 3.5 Haiku经常在"头脑中"使用多个中间推理步骤来决定输出
- 显示**向前规划**的迹象，提前考虑多种可能性
- 显示**向后规划**的迹象，从目标状态向后制定响应的早期部分
- 看到原始"元认知"电路的迹象，允许模型知道自己的知识范围
- 模型的内部计算是高度抽象的，并在不同上下文之间泛化
- 方法有时能够审计模型的内部推理步骤，以标记令人担忧的"思维过程"

## Limitations

- 归因图仅能提供约四分之一提示的满意洞察
- 即使在成功的案例研究中，所强调的发现只捕获了模型机制的一小部分

## Related Papers
- [[wiki/circuit-tracing]]: 方法论文
- [[wiki/scaling-monosemanticity]]: 特征提取基础

## Source Files
- Raw source: `D:\obsidian-notebook\raw\On the Biology of a Large Language Model.md`