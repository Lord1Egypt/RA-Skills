---
name: multi-agent-memory
description: 多 agent 共享记忆与项目协作架构。支持项目状态隔离、知识库共享、跨项目搜索、版本控制、里程碑跟踪、周报和交接文档。适用于多个 agent 协作开发多个项目的场景。
author: COMMANDER
version: 1.0.0
---

# Multi-Agent Memory & Collaboration Architecture

## 概述

本 skill 定义了一套完整的多 agent 共享记忆与项目协作架构，解决以下核心问题：

1. **项目状态隔离 vs 知识共享**：项目状态（todos/status）按项目隔离，知识库（decisions/patterns）跨项目共享
2. **跨时空知识链接**：支持跨项目、跨时间搜索关键词，形成"智慧涌现"和"结构洞创新"
3. **版本控制**：每个文件保留最近 3 个版本，支持回滚
4. **里程碑跟踪**：SMART 原则的里程碑管理，RACI 责任模型
5. **周报与交接**：结构化的周报和一页纸交接文档

## 何时使用

**必须使用的场景：**
- 多个 agent 协作开发多个项目
- 需要跨项目共享知识和经验
- 需要清晰的项目状态跟踪
- 需要定期汇报和交接

**触发词：**
- "初始化项目"
- "创建周报"
- "写交接文档"
- "更新里程碑"
- "搜索知识库"
- "项目协作"

## 目录结构

```
/root/.openclaw/
├── workspace-commander/     # 个人工作区（私有）
├── workspace-maker/
├── workspace-vibe/
├── workspace-killjoy/
├── workspace-main/
│
├── projects/                # 项目状态（隔离）
│   ├── <project-name>/
│   │   ├── status/          # 当前状态（每日更新）
│   │   │   ├── maker.md
│   │   │   ├── vibe.md
│   │   │   ├── commander.md
│   │   │   └── killjoy.md
│   │   │
│   │   ├── todos.md         # 待办事项（实时更新）
│   │   ├── context.md       # 项目背景/目标（初始化后很少改）
│   │   │
│   │   ├── weekly/          # 每周总结（每周一篇）
│   │   │   ├── 2026-W10.md
│   │   │   └── 2026-W11.md
│   │   │
│   │   ├── handoffs/        # 交接文档（重大节点更新）
│   │   │   ├── 2026-03-09-Phase1-交接.md
│   │   │   └── latest.md    # 符号链接，指向最新版本
│   │   │
│   │   ├── docs/            # 设计文档（按需创建）
│   │   │   ├── requirements/
│   │   │   │   └── YYYY-MM-DD-HH-mm-需求-{描述}.md
│   │   │   └── specs/
│   │   │       └── YYYY-MM-DD-HH-mm-设计-{描述}.md
│   │   │
│   │   ├── logs/            # 开发日志（每次完成任务后）
│   │   │   └── YYYY-MM-DD-HH-mm-开发日志-{任务名}.md
│   │   │
│   │   └── milestones/      # 里程碑跟踪（每周更新）
│   │       └── milestones.md
│   │
│   └── <another-project>/
│
├── knowledge/               # 共享知识库（跨项目）
│   ├── decisions/
│   │   └── decisions.md     # 关键决策（跨项目）
│   ├── patterns/
│   │   └── patterns.md      # 技术模式/经验（跨项目）
│   ├── glossary/
│   │   └── glossary.md      # 术语表/概念定义
│   └── index/
│       └── keywords.txt     # 关键词索引
│
└── archive/                 # 归档（完整历史）
    ├── <project-name>/
    │   └── YYYY-Wxx/
    │       ├── status-snapshot.tar.gz
    │       ├── weekly-YYYY-Wxx.md
    │       └── summary.md
    └── <another-project>/
```

## 核心原则

### 1. 分层共享

- **项目状态（隔离）**：`projects/<project>/status/`, `todos.md`, `context.md`
- **知识库（共享）**：`knowledge/decisions/`, `knowledge/patterns/`, `knowledge/glossary/`
- **归档（只读）**：`archive/`

### 2. 文档命名规范

**所有文档必须遵循时间戳命名：**
```
YYYY-MM-DD-HH-mm-{类型}-{描述}.md
```

**获取时间戳：**
```bash
date +'%Y-%m-%d-%H-%M'
```

**示例：**
- `2026-03-09-14-30-需求-内容工厂.md`
- `2026-03-09-15-20-设计-文章生成流程.md`
- `2026-03-09-16-10-开发日志-功能A.md`

### 3. RACI 责任模型

每个任务/决策都应该有明确的责任人：
- **Responsible（执行者）**：谁来做这件事
- **Accountable（负责人）**：谁对结果负责
- **Consulted（咨询者）**：需要咨询谁
- **Informed（知情者）**：需要通知谁

### 4. 版本控制

每个文件保留最近 3 个版本：
```
file.md       # 当前版本
file.md.1     # 上一个版本
file.md.2     # 上上个版本
```

**备份脚本：**
```bash
if [ -f file.md ]; then
  cp file.md.1 file.md.2
  cp file.md file.md.1
fi
echo "新内容" > file.md
```

## 文档模板

所有模板文件位于：`~/.openclaw/skills/multi-agent-memory/templates/`

### 1. context.md（项目背景）
### 2. todos.md（待办事项）
### 3. status/<agent>.md（agent 状态）
### 4. weekly/YYYY-Wxx.md（每周总结）
### 5. handoffs/YYYY-MM-DD-{阶段}-交接.md（交接文档）
### 6. milestones/milestones.md（里程碑跟踪）
### 7. logs/YYYY-MM-DD-HH-mm-开发日志-{任务名}.md（开发日志）

详细模板内容见 templates/ 目录。

## 工作流程

### 每天开始时（每个 agent）

```bash
# 1. 确定当前项目
PROJECT=$(cat ~/workspace-<agent>/current-project.txt)

# 2. 读取项目核心文件
read /root/.openclaw/projects/$PROJECT/context.md
read /root/.openclaw/projects/$PROJECT/todos.md
read /root/.openclaw/projects/$PROJECT/status/*.md

# 3. 读取最新周报和里程碑
LATEST_WEEKLY=$(ls -t /root/.openclaw/projects/$PROJECT/weekly/ 2>/dev/null | head -1)
if [ -n "$LATEST_WEEKLY" ]; then
  read /root/.openclaw/projects/$PROJECT/weekly/$LATEST_WEEKLY
fi
read /root/.openclaw/projects/$PROJECT/milestones/milestones.md

# 4. 如果需要跨项目知识，搜索知识库
grep -rn "关键词" /root/.openclaw/knowledge/
```

### 完成任务后（每个 agent）

```bash
PROJECT=$(cat ~/workspace-<agent>/current-project.txt)
TIMESTAMP=$(date +'%Y-%m-%d-%H-%M')

# 1. 备份并更新 status
STATUS_FILE="/root/.openclaw/projects/$PROJECT/status/<agent>.md"
if [ -f "$STATUS_FILE" ]; then
  cp "$STATUS_FILE.1" "$STATUS_FILE.2" 2>/dev/null
  cp "$STATUS_FILE" "$STATUS_FILE.1"
fi

# 2. 写入开发日志
cat > /root/.openclaw/projects/$PROJECT/logs/$TIMESTAMP-开发日志-{任务名}.md <<EOF
# 开发日志 - {任务名}

**时间：** $(date +'%Y-%m-%d %H:%M')
**负责人：** <AGENT>
**项目：** $PROJECT

## 完成的工作
- ...

## 遇到的问题
- ...

## 解决方案
- ...

## 下一步
- ...
EOF

# 3. 更新 todos.md 和 status
# 4. 如果有新知识，追加到 knowledge/
```

### 每周结束时（COMMANDER）

```bash
PROJECT="<project-name>"
WEEK=$(date +'%Y-W%V')

# 1. 写入周报（使用模板）
# 2. 更新里程碑
# 3. 归档本周数据
mkdir -p /root/.openclaw/archive/$PROJECT/$WEEK/
tar -czf /root/.openclaw/archive/$PROJECT/$WEEK/status-snapshot.tar.gz \
  /root/.openclaw/projects/$PROJECT/status/
```

## 实施步骤

### Step 1: 初始化项目

```bash
~/.openclaw/skills/multi-agent-memory/scripts/init-project.sh <project-name>
```

### Step 2: 设置当前项目

```bash
echo "<project-name>" > ~/workspace-<agent>/current-project.txt
```

### Step 3: 每日检查

```bash
~/.openclaw/skills/multi-agent-memory/scripts/daily-check.sh <project-name>
```

## 搜索机制

### 关键词搜索

```bash
# 搜索知识库
grep -rn "PostgreSQL" /root/.openclaw/knowledge/

# 搜索项目文档
grep -rn "PostgreSQL" /root/.openclaw/projects/<project>/docs/

# 跨项目搜索
grep -rn "PostgreSQL" /root/.openclaw/projects/
```

## 最佳实践

1. **信任文档**：context.md 是项目的"事实之源"
2. **区分全局与项目**：全局知识库 vs 项目状态
3. **遵循命名规范**：所有文档使用时间戳前缀
4. **定期更新**：status 每日，weekly 每周
5. **版本控制**：每次写入前自动备份
6. **知识沉淀**：每周汇总关键决策和经验
7. **责任明确**：每个任务都有 RACI

## 相关 Skills

- `project-management` - 项目结构和工作流管理
- `doc-todo-log-loop` - 基于日志记录驱动的轻量级项目开发和管理方案
- `milestone-tracker` - 里程碑跟踪

## 版本历史

- **1.0.0** (2026-03-09): 初始版本
