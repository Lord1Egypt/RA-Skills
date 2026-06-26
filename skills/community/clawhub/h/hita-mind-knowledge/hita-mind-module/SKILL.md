---
name: hita-mind-module
description: hita 开发的 AI Agent 记忆模块，是 Hita-Mind & Knowledge 的一部分。基于8大分类体系（decisions/preferences/patterns/causality/contacts/feedback/projects/daily）。适用于 AI Agent 的长期记忆管理，支持对话记录、偏好、决策、教训等信息的积累与检索。触发关键词："查一下记忆"、"我的记忆"、"记得什么"。
---

# hita Mind Module - AI 个人记忆系统

hita 开发的记忆模块，是 **Hita-Mind & Knowledge** 知识体系的一部分。

## 定位

| 模块 | 作用 |
|------|------|
| **Mind**（本模块） | AI 的记忆 — 偏好、决策、教训 |
| **Knowledge** | AI 的知识 — 技巧、方法、规则 |

## 8 大分类

| 分类 | 存什么 |
|------|--------|
| decisions | 技术选型、重要决定及原因 |
| preferences | 沟通风格、工作习惯、说话偏好 |
| patterns | 工作模板、分析流程、最佳实践 |
| causality | 问题根因、失败教训、经验总结 |
| contacts | 人名、业务联系人 |
| feedback | 用户纠正、好评、工作反馈 |
| projects | 具体任务、项目事实、客观数据 |
| daily | 当天工作日志、对话记录 |

## CLI 用法

```bash
# 列出某分类的记忆
node index.js list patterns
node index.js list preferences

# 搜索记忆
node index.js search PPT
node index.js search 开会

# 查看统计
node index.js stats

# 构建上下文（默认5条）
node index.js context patterns
node index.js context preferences

# 添加记忆
node index.js add preferences "叫用户" "叫老板，说话轻松一点"
node index.js add causality "教训" "做事前先查记忆，不要直接开始"
```

## 数据文件

记忆数据存储在 `memory-store.json`，首次运行自动创建。

## 关于

由 **hita** 开发，作为 **Hita-Mind & Knowledge** 的一部分。
