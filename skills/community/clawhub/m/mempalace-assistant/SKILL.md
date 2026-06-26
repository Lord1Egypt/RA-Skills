---
name: mempalace-assistant
description: MemPalace记忆系统助手 - 基于老四的AI记忆系统。提供结构化记忆存储、快速检索、记忆组织等功能。适用于需要持久化知识、跨会话记忆、语义搜索等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [memory, knowledge-base, search, ai-memory, retrieval]
version: 1.0.0
author: laosi
source: local
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

发布前必须验证：

- [x] 功能完整性：所有描述的功能都能正常工作
- [x] 语法正确性：Markdown格式正确，无错误
- [x] 激活词有效性：激活词能正确触发
- [x] 场景覆盖：主要使用场景已测试
- [x] 无副作用：不会破坏已有功能

---

# MemPalace Assistant - 记忆系统助手

> 基于老四(laosi)的AI记忆系统
> 激活词: 搜索记忆 / 记住 / 记忆搜索

## 概述

MemPalace是一个结构化记忆系统，用于AI Agent的持久化知识存储和快速检索。

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 搜索记忆 | `mempalace search <关键词>` | 语义搜索记忆 |
| 写入记忆 | 存储对话知识 | 跨会话知识传承 |
| 读取记忆 | 查看记忆内容 | 按时间/标签检索 |
| 组织记忆 | 分类标签 | 知识图谱构建 |

## 使用方法

### 搜索记忆

```bash
py -3.13 -m mempalace search "关键词"
```

### 写入记忆

```bash
py -3.13 -m mempalace add "记忆内容"
```

### 查看所有记忆

```bash
py -3.13 -m mempalace list
```

### 导出记忆

```bash
py -3.13 -m mempalace export
```

## 记忆结构

```json
{
  "content": "记忆内容",
  "timestamp": "2026-04-28T00:00:00.000Z",
  "tokens": "分词后的关键词"
}
```

## 应用场景

1. **跨会话学习** - 将一次学到的知识存储，供下次使用
2. **知识积累** - 持续构建个人知识库
3. **快速检索** - 用自然语言搜索记忆
4. **记忆巩固** - 强化重要信息的记忆

## 来源

- 老四MemPalace系统: `D:\coze-local\simple-agent\skills_learned\mempalace.md`