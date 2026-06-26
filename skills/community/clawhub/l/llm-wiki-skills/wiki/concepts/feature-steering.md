---
title: "Feature Steering"
aka: ["特征引导", "特征控制"]
created: 2026-04-09
tags: [concept, technique, steering]
---

## Overview

**Feature Steering** 特征引导是一种通过调整模型内部特征激活来控制模型行为的技术。

## 工作原理

1. 识别模型中的特定特征（使用SAEs等方法）
2. 调整该特征的激活强度
3. 观察模型行为的变化

## 应用场景

### 行为控制
- 引导模型更倾向于特定类型的响应
- 减少有害输出

### 案例
- [[wiki/assistant-axis]]: 通过助手轴引导控制角色漂移
- [[wiki/activation-oracles]]: 使用Activation Oracles理解和引导激活

## Activation Capping

一种轻触干预方法：
- 识别助手行为期间激活的正常范围
- 当激活超出范围时进行限制
- 既减少有害响应，又保留模型能力

## 相关概念
- [[wiki/sparse-autoencoder]]
- [[wiki/feature]]
- [[wiki/activation-oracles]]

## 安全性考虑
- 特征引导可能产生意外副作用
- 需要仔细验证和测试