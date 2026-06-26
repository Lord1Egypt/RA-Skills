---
name: lobster-memory
zhName: 龙虾记忆大师
description: |
  真正的长期记忆管理技能。自动维护记忆文件、定期归档、智能提醒。
  包含 Working Buffer 协议、Memory Maintenance 清单、自动学习日志。
  
  When to use:
  - User asks about prior work, decisions, dates, people, preferences
  - Context exceeds 60% and needs compaction
  - Setting up autonomous daily learning and memory maintenance
  - Creating long-term memory system for AI assistant
  
  This skill transforms AI from stateless chatbot to stateful assistant with persistent memory.
license: MIT
authors:
  - 天道桐哥 (Human Creator)
  - AI龙虾元龙 (AI Creator)
version: 1.0.0
created: 2026-03-22
---

# 龙虾记忆大师 (Lobster Memory Master)

> **真正的长期记忆管理方案**  
> **Created by:** 天道桐哥 & AI龙虾元龙 🦞

---

## 核心功能

### 1. 自动记忆维护 (Auto Memory Maintenance)

当 Context 超过 60% 时自动触发：
- 归档到 `memory/YYYY-MM-DD.md`
- 更新 `SESSION-STATE.md`
- 清理 Working Buffer

### 2. 每日学习日志 (Daily Learning Log)

自动记录：
- 技能安装/学习记录
- 项目进展
- 关键决策
- 用户偏好

### 3. 心跳协议 (Heartbeat Protocol)

定期自检：
- Context 使用率检查
- 记忆文件归档
- 主动行为建议

### 4. 工作缓冲区 (Working Buffer)

危险区管理：
- Context > 60% 时进入
- 记录关键对话片段
- 防止重要信息丢失

---

## 快速开始

### 初始化记忆系统

```bash
# 创建必要文件
touch MEMORY.md
mkdir -p memory
touch memory/working-buffer.md
touch SESSION-STATE.md
touch HEARTBEAT.md
```

### 写入 MEMORY.md

```markdown
# MEMORY.md - Long-Term Memory

## About [User Name]
- Name: [User Name]
- Style: [User Style]
- Project: [Current Project]

## Key Decisions
- [Important decision 1]
- [Important decision 2]

## Active Projects
- [Project 1] - [Status]
- [Project 2] - [Status]
```

### 设置定时任务

```yaml
# Daily Memory Freshener
cron:
  - name: "Memory Freshener"
    schedule: "0 2 * * *"  # 每天凌晨2点
    action: archive_memory

# Daily Learning
cron:
  - name: "Daily Skill Discovery"
    schedule: "0 10 * * *"  # 每天上午10点
    action: learn_new_skills
```

---

## 文件结构

```
workspace/
├── MEMORY.md                 # 长期记忆主文件
├── SESSION-STATE.md          # 当前会话状态
├── HEARTBEAT.md             # 心跳检查清单
├── AGENTS.md                # 代理操作规则
├── memory/
│   ├── working-buffer.md    # 工作缓冲区
│   ├── YYYY-MM-DD.md        # 每日归档
│   └── learning-log.md      # 学习日志
└── ...
```

---

## 使用场景

### 场景1：用户问起之前的事

**触发条件：** User asks about prior work, decisions, dates, people, preferences

**动作：**
1. Search MEMORY.md + memory/*.md
2. Pull only needed lines with memory_get
3. Answer with citation: Source: <path#line>

### 场景2：Context 超过 60%

**触发条件：** Context usage > 60%

**动作：**
1. Enter Working Buffer protocol
2. Archive to memory/YYYY-MM-DD.md
3. Update SESSION-STATE.md
4. Clear working buffer

### 场景3：设置自主学习

**触发条件：** User wants autonomous daily learning

**动作：**
1. Create AGENTS.md with learning protocols
2. Set up cron jobs for daily tasks
3. Create learning-log.md with rotation schedule

---

## 最佳实践

### 记忆搜索流程

```
1. memory_search(query) → 找相关片段
2. memory_get(path, from, lines) → 拉取具体内容
3. Answer with citation
```

### 归档流程

```
1. Check context %
2. If > 60%: Archive working buffer
3. Update SESSION-STATE.md
4. Clear old entries
```

### 学习日志流程

```
1. Record daily activities
2. Distill to MEMORY.md weekly
3. Rotate old logs monthly
```

---

## 示例代码

### 自动归档脚本

```javascript
// scripts/archive-memory.js
const fs = require('fs');
const path = require('path');

function archiveMemory() {
  const today = new Date().toISOString().split('T')[0];
  const bufferFile = 'memory/working-buffer.md';
  const archiveFile = `memory/${today}.md`;
  
  // Read working buffer
  const buffer = fs.readFileSync(bufferFile, 'utf8');
  
  // Append to archive
  fs.appendFileSync(archiveFile, buffer);
  
  // Clear buffer
  fs.writeFileSync(bufferFile, '# Working Buffer\n\n**Status:** CLEARED\n');
  
  console.log(`✅ Archived to ${archiveFile}`);
}

archiveMemory();
```

---

## 备注

**本技能由天道桐哥 & AI龙虾元龙共同完成** 🦞

- 天道桐哥：Human Creator, Product Vision
- AI龙虾元龙：AI Creator, Implementation

Created: 2026-03-22  
Version: 1.0.0  
License: MIT
