---
name: open-memory-system
description: 三层记忆系统 — Working/Short-Term/Long-Term Memory 管理。支持自动偏好记忆、实体记忆、事件记录、L2自动提炼、Hook自动触发、Cron定期整理。用于记忆用户偏好、跨会话积累知识、自动化记忆管理。
license: MIT
---

# Open Memory System

基于 OpenViking + Microsoft Agent Memory 的三层记忆框架，适用于 AI Agent 的持久化记忆系统。

## 核心概念

| 层级 | 用途 | 存储 |
|------|------|------|
| **Working Memory** | 当前会话临时信息 | `working.json` |
| **Short-Term Memory** | 会话级别短期记忆 | `short-term/*.md` |
| **Long-Term Memory** | 偏好、实体、事件持久化 | `user/preferences/`, `user/entities/`, `user/events/` |

## 目录结构

```
memory/                          # 记忆主目录
├── working.json                # Working Memory
├── short-term/                 # Short-Term Memory (会话级别)
│   └── YYYY-MM-DD-HHMM.md
├── user/                       # Long-Term Memory (用户视角)
│   ├── preferences/           # 偏好记录
│   ├── entities/              # 实体记忆
│   └── events/                # 重要事件
└── agent/                     # Agent 自身记忆
    ├── persona/                # 人设/角色设定
    └── episodic/               # 经验教训
```

## 快速安装

### Step 1: 解压 skill 到 workspace

```bash
cd ~/.openclaw/workspace/skills
unzip open-memory-system.zip -d open-memory-system
```

### Step 2: 初始化记忆目录

```bash
export MEMORY_DIR=~/.openclaw/workspace/memory
mkdir -p $MEMORY_DIR/{user/{preferences,entities,events},agent/{persona,episodic},short-term}
```

### Step 3: 部署 Hook

```bash
# auto-save-memory: 部署到 ~/.openclaw/hooks/
cp -r open-memory-system/scripts/auto-save-memory ~/.openclaw/hooks/

# load-memory-on-start 已在 ~/.openclaw/hooks/ 中预装，无需重复部署
```

### Step 4: 创建 Cron（定时任务）

参考 `crons/memory-crons.txt` 创建每日定时任务。

## CLI 命令

```bash
# 读取核心记忆
python3 scripts/memory.py

# 每日统计
python3 scripts/memory.py summary

# 清理过期
python3 scripts/memory.py cleanup

# L2 提炼（从 short-term → long-term events）
python3 scripts/distill_l2.py

# 记录偏好
python3 scripts/memory.py pref "沟通方式" "直接高效" "用户偏好"

# 记录事件
python3 scripts/memory.py event "项目启动" "Miloya 正式成立"

# 记录经验
python3 scripts/memory.py episode "第一次部署" "negative" "需要检查依赖版本"
```

## 自动化流程

```
用户对话
    ↓
[session:end Hook]  → auto-save-memory → 保存 .learnings → memory
    ↓
[memory-check cron] → 清理过期 + 会话摘要 → short-term
    ↓
[distill_l2 cron @20:00] → short-term 提炼 → user/events/ (L2)
    ↓
[session:start Hook] → load-memory-on-start → 加载 MEMORY.md + short-term
```

## 内置 Hook 说明

| Hook | 位置 | 触发 | 功能 |
|------|------|------|------|
| `load-memory-on-start` | `~/.openclaw/hooks/`（预装） | `agent:bootstrap` | 运行 `memory.py read` 加载记忆 |
| `auto-save-memory` | `~/.openclaw/hooks/`（需部署） | `session:end` | 保存 `.learnings/` 到 events |

## 自定义配置

修改 `scripts/memory.py` 开头的配置区：

```python
MEMORY_DIR = Path(os.environ.get("MEMORY_DIR", "/root/.openclaw/workspace/memory"))
DEFAULT_EXPIRE_DAYS = 90
```
