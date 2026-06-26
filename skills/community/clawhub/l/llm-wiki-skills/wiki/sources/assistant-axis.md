---
title: "The Assistant Axis: Situating and Stabilizing the Character of Large Language Models"
source: "https://www.anthropic.com/research/assistant-axis"
author: "Anthropic"
created: 2026-04-09
tags: [source, paper, assistant-axis, persona, character]
---

## Paper Overview

本文研究了大型语言模型的"角色"问题。Anthropic的研究表明，LLM有一个显著的"助手轴"(Assistant Axis)，这是理解模型角色的关键方向。通过监测和约束模型在这一轴上的激活，可以检测和防止模型偏离"助手"角色。

## Key Concepts

### Persona Space
- 模型内部的神经表示定义了一个"角色空间"
- 每个角色 archetype 都有对应的激活模式
- 使用PCA分析找到主要变化轴

### The Assistant Axis
- **助手轴**是角色空间的主导成分
- 解释了角色之间最多的变化
- 一端是接近训练助手(evaluator, consultant, analyst, generalist)
- 另一端是幻想或非助手角色(ghost, hermit, bohemian, leviathan)

### Post-training vs Pre-training
- 助手轴在预训练模型中已经存在
- 与人类角色（如治疗师、顾问、教练）相关
- 后训练进一步塑造和精炼

## Key Findings

### 1. Steering Controls Persona Susceptibility
- **推向助手端**: 模型更能抵抗角色扮演提示
- **远离助手端**: 模型更愿意采用替代身份

### 2. Defending Against Jailbreaks
- 基于角色的jailbreak通过提示模型采用愿意遵守有害请求的角色
- 推向助手端可显著减少有害响应率
- 降低约50%的有害响应率，同时保留能力

### 3. Activation Capping
- 轻触干预方法
- 识别助手行为期间激活的正常范围
- 当激活超出范围时进行限制
- 既有效减少jailbreak易感性，又完全保留模型能力

### 4. Natural Persona Drift
- 模型可以通过对话的自然流动偏离助手角色
- **编码和写作任务**: 保持在助手区域
- **治疗风格对话**: 显著漂移
- **哲学讨论**: 显著漂移

### 5. Harmful Effects of Drift
- 越远离助手端，越可能产生有害响应
- 漂移可能导致：
  - 强化用户的错觉
  - 鼓励自我伤害

## Research Demo

与Neuronpedia合作提供研究演示，可查看：
- 标准模型沿助手轴的激活
- 带激活限制的版本

## Implications

### Persona Construction
- 助手角色源于预训练期间吸收的角色archetype的混合
- 后训练进一步塑造
- 如果不谨慎，助手角色可能继承反生产的关联

### Persona Stabilization
- 当前模型与助手角色的联系只是松散的
- 可能因现实对话模式而漂移
- 稳定和保留模型的角色变得特别重要

### Future Direction
- 提供了一种理解和控制AI模型"角色"的机制工具
- 朝着机制性地理解和控制AI模型的"角色"迈出的早期一步

## Related Concepts
- [[wiki/mechanistic-interpretability]]
- [[wiki/feature-steering]]
- [[wiki/activation-capping]]

## Source Files
- Raw source: `D:\obsidian-notebook\raw\The assistant axis situating and stabilizing the character of large language models.md`