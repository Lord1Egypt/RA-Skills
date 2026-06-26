# Micro Memory V4 — Your Second Brain

> 🧠 **Not just a note-taking tool, but your external brain that truly remembers.**
> 
> 不只是笔记工具，而是真正会"记忆"的外部大脑。

## What is Micro Memory? | 什么是 Micro Memory？

Micro Memory is an **intelligent memory system** inspired by how the human brain works:

- 🧠 **Like your brain**, memories fade over time without reinforcement
- 🔗 **Like your brain**, related concepts form neural networks  
- 📅 **Like your brain**, spaced repetition strengthens retention
- 🏥 **Unlike your brain**, it gives you health reports and analytics

Micro Memory 是一个**智能记忆系统**，灵感来自人脑的工作方式：

- 🧠 **像大脑一样**，记忆会随时间衰减，需要强化巩固
- 🔗 **像大脑一样**，相关概念形成神经网络关联
- 📅 **像大脑一样**，间隔重复加强记忆留存
- 🏥 ** unlike大脑**，它能给你健康报告和分析

---

## Why Micro Memory? | 为什么选择 Micro Memory？

| Feature | Traditional Notes | Micro Memory |
|---------|------------------|--------------|
| Storage | Static files | Living memories with strength |
| Search | Simple text | Multi-keyword + Regex + Fuzzy |
| Organization | Folders/tags | Semantic networks |
| Retention | Manual review | Spaced repetition scheduling |
| Health | No insight | Memory health reports |
| Compression | None | TF-IDF smart compression |

| 特性 | 传统笔记 | Micro Memory |
|---------|------------------|--------------|
| 存储 | 静态文件 | 有强度的活记忆 |
| 搜索 | 简单文本 | 多关键词 + 正则 + 模糊 |
| 组织 | 文件夹/标签 | 语义网络 |
| 留存 | 手动复习 | 间隔重复调度 |
| 健康 | 无洞察 | 记忆健康报告 |
| 压缩 | 无 | TF-IDF 智能压缩 |

---

## Core Features | 核心功能

### 📝 Smart Memory Creation | 智能记忆创建
```bash
memory add "Learned about TypeScript decorators"
memory add "Important meeting with client" --tag=work --type=longterm --importance=5
memory add "Related concept" --tag=study --link=1,2
```

### 🔍 Advanced Search | 高级搜索
```bash
memory search "TypeScript"                    # Multi-keyword
memory search "Type.*script" --regex          # Regex pattern
memory search "Typscript" --fuzzy             # Fuzzy matching
memory search "meeting client" --tag=work     # Filtered search
```

### 🔗 Memory Networks | 记忆网络
```bash
memory link --from=1 --to=2,3    # Connect memories
memory graph --id=1              # Visualize connections
memory graph                     # Full network view
```

### 📊 Strength System | 强度系统
Memories have 5 strength levels that decay over time:

| Level | Score | Icon | Description |
|-------|-------|------|-------------|
| 💎 Permanent | 80-100 | 💎 | Permanent memory |
| 💪 Strong | 60-79 | 💪 | Strong memory |
| 📊 Stable | 40-59 | 📊 | Stable memory |
| ⚠️ Weak | 20-39 | ⚠️ | Weak memory - needs review |
| 🔴 Critical | 0-19 | 🔴 | Critical - about to be forgotten |

### 🔄 Spaced Repetition | 间隔重复
Based on SM-2 algorithm:
- Level 0 → 1 day
- Level 1 → 3 days
- Level 2 → 7 days
- Level 3 → 14 days
- Level 4 → 30 days
- Level 5+ → 60-90 days

### 🏥 Health Reports | 健康报告
```bash
memory health    # Overall system health
memory stats     # Detailed statistics
memory strength  # Strength distribution
```

### 📦 Compression & Archiving | 压缩与归档
```bash
memory compress --auto           # Auto-compress weak memories
memory compress --id=1           # Compress specific memory
memory archive --older_than=30   # Archive old memories
memory archive --restore=1       # Restore from archive
```

---

## Quick Start | 快速开始

### Installation | 安装
```bash
npm install
npm run build
```

### Basic Usage | 基本用法
```bash
# Add a memory
memory add "Learned about neural networks"

# List all memories
memory list

# Search memories
memory search "neural"

# Check health
memory health

# Review due memories
memory review --today
```

---

## Clawdbot Integration | Clawdbot 集成

As a native skill, Micro Memory auto-triggers on:

| Trigger | Action |
|---------|--------|
| "记住..." / "记录..." | Auto-add memory |
| "搜索记忆..." / "找找之前..." | Auto-search |
| "列出记忆" / "我的记忆" | Auto-list |
| "记忆健康" | Show health report |
| "复习记忆" | Show today's reviews |

---

## Data Storage | 数据存储

```
store/
├── index.json      # Main memory index
├── links.json      # Association networks
├── reviews.json    # Review schedules
├── store.md        # Markdown backup
└── archive/        # Archived memories
```

---

## Version | 版本

- **Current | 当前**: 4.0.1
- **Implementation | 实现**: TypeScript (Native Clawdbot Skill)

---

## Architecture | 架构

```
micro-memory/
├── src/
│   ├── index.ts      # CLI entry
│   ├── memory.ts     # Core memory management
│   ├── strength.ts   # Strength decay system
│   ├── links.ts      # Network associations
│   ├── review.ts     # Spaced repetition
│   ├── health.ts     # Health analytics
│   ├── archive.ts    # Compression & archiving
│   └── utils.ts      # Utilities
└── dist/             # Compiled JavaScript
```

---

**Your thoughts deserve to be remembered. Not just stored.**

**你的想法值得被记住，而不只是被存储。**
