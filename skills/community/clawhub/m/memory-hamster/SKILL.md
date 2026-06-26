---
name: memory-hamster
version: 1.0.1
description: "Agent 记忆进化系统 - 温度模型 + 自动归档 + 学习记录 + 技能提炼。让 AI 每天变得更聪明。"
author: OpenClaw Community
keywords: [memory, evolution, learning, self-improvement, archive, skill-extraction, temperature-model, agent]
metadata:
  openclaw:
    emoji: "🤖"
    features:
      - 温度模型（热/温/冷）
      - 自动归档（30 天冷数据）
      - 夜间反思（每日 23:45）
      - 学习记录（教训/错误/功能请求）
      - 技能提炼（从教训提取）
      - Promotion 机制（到 SOUL/AGENTS/TOOLS）
---

# MemoryHamster 🤖

**Agent 记忆进化系统**

合并记忆管理与自我进化，让 AI 每天变得更聪明。

## 核心功能

### 1. 温度模型 🌡️

| 温度 | 时间范围 | 存储位置 | 说明 |
|------|----------|----------|------|
| 🔥 热 | < 7 天 | memory/*.md | 活跃数据，高频访问 |
| 🟡 温 | 7-30 天 | memory/*.md | 近期数据，偶尔访问 |
| ❄️ 冷 | > 30 天 | memory/.archive/ | 归档数据，低频访问 |

### 2. 学习记录系统 📝

| 类型 | 文件 | 触发条件 |
|------|------|----------|
| 教训 | `.learnings/LEARNINGS.md` | 被纠正、发现更好方法、知识缺口 |
| 错误 | `.learnings/ERRORS.md` | 命令失败、API 错误、异常 |
| 功能请求 | `.learnings/FEATURE_REQUESTS.md` | 用户想要新能力 |

### 3. 自动 GC（每周日 00:00）

```bash
./skills/memory-hamster/scripts/memory-gc.sh
```

功能：
- 扫描超过 30 天的日志文件
- 移动到 `memory/.archive/YYYY-MM/` 目录
- 生成 GC 报告

### 4. 夜间反思（每日 23:45）

```bash
./skills/memory-hamster/scripts/nightly-reflection.sh
```

功能：
- 验证记忆 CRUD
- 创建反思记录
- 更新健康度统计
- 检查待归档数据

### 5. 技能提炼 🏗️

```bash
./skills/memory-hamster/scripts/extract-skill.sh <lesson-name> [skill-name]
```

功能：
- 从 `.learnings/LEARNINGS.md` 读取教训
- 生成 `skills/<skill-name>/SKILL.md`
- 自动创建技能模板

### 6. 语义搜索 🔍

**优势：** 基于关键词的语义匹配，支持范围过滤和相关性排序

```bash
# 搜索记忆（Node.js 脚本）
node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" [--user|--repo|--both] "USER_QUERY_HERE"
```

| 范围 | 说明 |
|------|------|
| `--user` | 搜索个人/用户记忆（跨会话） |
| `--repo` | 搜索项目/代码记忆 |
| `--both` | 同时搜索（默认） |

**示例：**
- "昨天做了什么" → `node search-memory.cjs "work yesterday recent activity"`
- "如何实现认证" → `node search-memory.cjs --repo "authentication implementation"`
- "编码偏好" → `node search-memory.cjs --user "coding preferences style"`

### 7. Promotion 机制 📈

| 学习类型 | 提升到 | 示例 |
|----------|--------|------|
| 行为模式 | `SOUL.md` | "简洁回复，不说废话" |
| 工作流改进 | `AGENTS.md` | "长任务 spawning 子代理" |
| 工具技巧 | `TOOLS.md` | "Git push 需要先配置 auth" |

## 目录结构

```
workspace/
├── MEMORY.md                    # 核心长期记忆（<5KB）
├── SOUL.md                      # 行为准则
├── AGENTS.md                    # 工作流
├── TOOLS.md                     # 工具技巧
├── memory/                      # 每日记忆（温度模型）
│   ├── INDEX.md
│   ├── YYYY-MM-DD.md            # 每日日志
│   ├── lessons/README.md        # 教训索引
│   ├── decisions/README.md      # 决策索引
│   ├── people/                  # 人物档案
│   ├── reflections/             # 反思记录
│   └── .archive/                # 冷数据归档（>30 天）
├── .learnings/                  # 学习记录（进化核心）
│   ├── LEARNINGS.md             # 教训/纠正/最佳实践
│   ├── ERRORS.md                # 错误记录
│   └── FEATURE_REQUESTS.md      # 功能请求
└── skills/memory-hamster/
    ├── SKILL.md                 # 本文件
    └── scripts/
        ├── memory-gc.sh         # GC 归档脚本
        ├── nightly-reflection.sh # 夜间反思脚本
        ├── extract-skill.sh     # 技能提取脚本
        └── search-memory.cjs    # 语义搜索脚本（新增）
```

## 🚀 快速开始

### 1. 安装技能

```bash
# 从 ClawHub 安装
clawhub install memory-hamster
```

### 2. 初始化（已完成）

```bash
# 目录结构已创建
# 文件已初始化
```

### 2. 配置 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下任务（根据实际安装路径调整）
0 0 * * 0 ./skills/memory-hamster/scripts/memory-gc.sh >> ./logs/memory-gc.log 2>&1
45 23 * * * ./skills/memory-hamster/scripts/nightly-reflection.sh >> ./logs/nightly-reflection.log 2>&1
```

### 3. 日常使用

**会话开始：**
1. 读取 `MEMORY.md` 获取核心记忆
2. 检查今日日志 `memory/YYYY-MM-DD.md`

**会话中：**
- 重要决策 → `memory/decisions/`
- 犯错/教训 → `.learnings/LEARNINGS.md` 或 `ERRORS.md`
- 用户纠正 → `.learnings/LEARNINGS.md` (category: correction)
- 发现更好方法 → `.learnings/LEARNINGS.md` (category: best_practice)

**会话结束：**
- 更新每日日志
- 标记完成事项

## 学习记录格式

### 教训条目（LEARNINGS.md）

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: 2026-03-09T11:00:00+08:00
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted
**Area**: workflow | tool | behavior | knowledge

### Summary
一句话描述学到了什么

### Details
完整上下文：发生了什么，什么错了，什么是对的

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20260309-001 (如果相关)
- Pattern-Key: simplify.dead_code (可选，用于追踪重复模式)

---
```

### 错误条目（ERRORS.md）

```markdown
## [ERR-YYYYMMDD-XXX] command_or_skill

**Logged**: 2026-03-09T11:00:00+08:00
**Priority**: high
**Status**: pending | resolved

### Summary
什么失败了

### Error
```
实际错误信息
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关环境信息

### Suggested Fix
如果可识别，什么可能解决这个问题

---
```

### 功能请求条目（FEATURE_REQUESTS.md）

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: 2026-03-09T11:00:00+08:00
**Priority**: medium
**Status**: pending | implemented

### Requested Capability
用户想要什么功能

### User Context
为什么需要，解决什么问题

### Suggested Implementation
如何实现

---
```

## ID 生成规则

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (学习), `ERR` (错误), `FEAT` (功能)
- YYYYMMDD: 当前日期
- XXX: 序列号 (001, 002, ...)

示例：`LRN-20260309-001`, `ERR-20260309-001`, `FEAT-20260309-001`

## 解决条目

当问题解决后，更新条目：

1. 改 `**Status**: pending` → `**Status**: resolved`
2. 添加解决块：

```markdown
### Resolution
- **Resolved**: 2026-03-09T12:00:00+08:00
- **Commit/PR**: abc123 或 #42
- **Notes**: 简要描述做了什么
```

## Promotion 流程

当学习具有广泛适用性时，提升到配置文件：

### 何时 Promotion

- 学习适用于多个文件/功能
- 任何 AI 贡献者都应该知道的知识
- 防止重复犯错
- 记录项目特定规范

### Promotion 目标

| 学习类型 | 提升到 | 示例 |
|----------|--------|------|
| 行为模式 | `SOUL.md` | "简洁回复，不说废话" |
| 工作流改进 | `AGENTS.md` | "长任务 spawning 子代理" |
| 工具技巧 | `TOOLS.md` | "Git push 需要先配置 auth" |

### 如何 Promotion

1. **提炼** 学习成简洁的规则或事实
2. **添加** 到目标文件的相关部分
3. **更新** 原始条目：
   - 改 `**Status**: pending` → `**Status**: promoted`
   - 添加 `**Promoted**: SOUL.md` 或 `AGENTS.md` 或 `TOOLS.md`

## 技能提取流程

当学习足够有价值时，提取为独立技能：

### 提取标准

满足以下任一条件：
- **重复出现**: 有 2+ 个相关的 `See Also` 链接
- **已验证**: Status 是 `resolved` 且有有效解决方案
- **非显而易见**: 需要实际调试/调查才发现
- **广泛适用**: 不限于特定项目
- **用户指定**: 用户说"保存为技能"

### 提取步骤

```bash
# 1. 运行提取脚本
./skills/vv-evolution/scripts/extract-skill.sh <lesson-name> [skill-name]

# 2. 完善生成的 SKILL.md

# 3. 更新原学习条目
# Status: promoted_to_skill
# Skill-Path: skills/<skill-name>/
```

## 健康度指标

| 指标 | 正常范围 | 检查频率 |
|------|----------|----------|
| MEMORY.md 大小 | < 5KB | 每日 |
| 热数据数量 | 5-10 个 | 每周 |
| 教训数量 | 持续增长 | 每周 |
| 归档率 | < 20%/周 | 每周 |
| .learnings/ 待办 | < 20 | 每周 |
| 上下文大小 | < 100k | 每会话 |

## 上下文管理策略

详见 `AGENTS.md` → OpenClaw Best Practices → 上下文管理策略

核心：热/温/冷数据温度模型 + 100k 阈值监控

## Heartbeat 检查

详见 `AGENTS.md` → Heartbeat 检查清单

## 优先级指南

| 优先级 | 何时使用 |
|--------|----------|
| `critical` | 阻塞核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常见工作流、重复问题 |
| `medium` | 中等影响、有变通方案 |
| `low` | 小不便、边缘情况、锦上添花 |

## 最佳实践

1. **立即记录** - 上下文最新鲜
2. **具体明确** - 未来的 vv 需要快速理解
3. **包含复现步骤** - 特别是错误
4. **链接相关文件** - 让修复更容易
5. **建议具体修复** - 不只是"调查"
6. **使用一致分类** - 便于过滤
7. **积极 Promotion** - 有疑问就提升到配置文件
8. **定期回顾** -  stale 学习失去价值

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| browser-search | 搜索信息时可记录学习 |
| tavily-search | 搜索信息时可记录学习 |
| find-skills | 发现新技能后记录 |
| github | 项目相关学习记录 |
| skill-creator | 技能提取时使用 |

---

_🤖 MemoryHamster 进化宣言：每天进步一点点，积少成多！_
