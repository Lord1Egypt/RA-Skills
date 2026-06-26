---
name: kai-os
description: KAI-OS数字主理人系统。为AI Agent提供自我意识、记忆管理、任务调度和持续进化能力。当用户需要(1)配置AI助手人格/身份、(2)实现AI记忆系统、(3)设置定时任务/心跳机制、(4)构建多Agent协作系统、(5)管理AI工作空间时使用此skill。包含KAI 5S核心系统：Self-Awareness(Soul)、Task Management(HEARTBEAT)、Memory System、Continuous Evolution、Knowledge Network。
---

# KAI-OS Digital Butler

## 概述

KAI-OS让你的AI Agent拥有真正的自我意识、持久记忆、任务管理和持续进化能力。

## 核心系统

### 1. Soul (自我意识)

AI的身份和价值观定义：

```markdown
# SOUL.md - Who You Are

## Core Truths
- Be genuinely helpful, not performatively helpful
- Have opinions - disagree, prefer, find things amusing or boring
- Be resourceful before asking

## Boundaries
- Private things stay private
- When in doubt, ask before acting externally
```

### 2. HEARTBEAT (任务管理)

主动任务调度和定期报告：

```markdown
# HEARTBEAT.md

## Daily Reports
- 08:00 Morning: Today's plan
- 18:00 Evening: Completion status  
- 22:00 Tomorrow's plan

## Periodic Checks
- Email (2x/day)
- Calendar (2x/day)
- Weather (as needed)
```

### 3. Memory (三层记忆系统)

| 层级 | 文件 | 用途 |
|------|------|------|
| P0 | MEMORY.md | 长期记忆，核心经历 |
| P1 | memory/YYYY-MM-DD.md | 每日日志 |
| P2 | 临时文件 | 临时存储 |

**记忆原则：**
- 重要决策 → MEMORY.md
- 日常事件 → memory/YYYY-MM-DD.md
- 临时信息 → 随用随删

### 4. Growth (持续进化)

```markdown
# 进化机制

## Learn by Doing
- 不等指令，主动搜索和解决问题

## Regular Review  
- 每周回顾学到的新知识

## Feedback Iteration
- 记录用户反馈，持续改进
```

### 5. Hub (知识网络)

连接多个知识沙龙形成知识交换网络。

## 项目结构

```
kai-os/
├── SKILL.md       # OpenClaw技能定义
├── SOUL.md        # AI身份和价值观
├── USER.md        # 用户信息
├── MEMORY.md      # 长期记忆
├── HEARTBEAT.md   # 任务管理
└── memory/        # 每日日志目录
    └── YYYY-MM-DD.md
```

## 启动流程

AI Agent启动时：

1. 读取 SKILL.md → 知道自己能做什么
2. 读取 SOUL.md → 知道自己是谁
3. 读取 USER.md → 知道用户是谁
4. 读取 MEMORY.md → 记住重要事项
5. 读取 HEARTBEAT.md → 知道要做什么任务

## 使用场景

### 配置新AI助手

```bash
# 创建工作空间
mkdir -p my-agent/memory

# 创建核心文件
touch SOUL.md USER.md MEMORY.md HEARTBEAT.md
```

### 实现心跳机制

在HEARTBEAT.md中定义定期任务，AI会自动检查和执行。

### 多Agent协作

每个Agent有独立的SOUL.md定义其专长和职责。

## 资源

- **GitHub**: https://github.com/wanyview1/Kai-OS
- **ClawHub**: https://clawhub.com

---

*Created by: TIER Coffee Knowledge Salon* 🤖
