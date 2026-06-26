---
name: hita-mind-and-knowledge
description: hita 开发的 AI Agent 记忆与知识管理系统。包含 Mind Module（8大分类记忆）和 Knowledge Manager（3层知识库）两个互补模块。Mind Module 存储偏好、决策、教训；Knowledge Manager 存储技巧、方法、规则。适用于 AI Agent 的长期知识积累。触发关键词："查一下记忆"、"我的记忆"、"记得什么"、"知识库"、"添加知识"。
---

# Hita-Mind & Knowledge

AI Agent 记忆与知识管理系统，让 AI 拥有"记忆"和"知识"。

## 组成

| 模块 | 作用 | 存储 |
|------|------|------|
| **hita-mind-module** | AI 的记忆 | 偏好、决策、教训、习惯 |
| **hita-knowledge-manager** | AI 的知识 | 技巧、方法、规则、经验 |

## 模块说明

### hita-mind-module（记忆模块）

基于 8 大分类体系的记忆系统。

- decisions / preferences / patterns / causality
- contacts / feedback / projects / daily

### hita-knowledge-manager（知识模块）

三层知识库系统（L1/L2/L3），智能分层存储。

- L1 热数据：完整内容，50条上限
- L2 温数据：摘要+标签，200条上限
- L3 冷数据：元数据索引，无上限

## 使用方式

```bash
# 记忆模块
cd hita-mind-module && node index.js list

# 知识模块
cd hita-knowledge-manager && node index.js list
```

## 关于

由 **hita** 开发。
