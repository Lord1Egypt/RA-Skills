---
name: knowledge-system
description: "基于 Markdown 文件的 AI Agent 知识管理体系。建立和维护：SOUL（人格）/ USER（用户）/ AGENTS（工作规范）/ TOOLS（工具配置）/ MEMORY（长期记忆）/ memory（每日记录）/ .learnings（反思改进）/ HEARTBEAT（定期任务）。包含多 Agent 记忆协同。"
---

# 知识体系管理 skill

教你从零建立一套完整的 AI Agent 知识管理体系，基于纯 Markdown 文件，不依赖数据库或第三方服务。

---

## 目录

1. [文件架构](#1-文件架构)
2. [核心文件说明](#2-核心文件说明)
3. [建立知识体系](#3-建立知识体系)
4. [工作流程](#4-工作流程)
5. [.learnings 反思改进](#5-learnings-反思改进)
6. [HEARTBEAT 定期任务](#6-heartbeat-定期任务)
7. [多 Agent 扩展](#7-多-agent-扩展)
8. [上下文压缩](#8-上下文压缩)
9. [文件速查表](#9-文件速查表)

---

## 1. 文件架构

```
workspace/
├── SOUL.md              定义 Agent 的人格、性格、原则
├── USER.md              记录用户是谁、偏好、已知信息
├── AGENTS.md            工作手册：流程、规范、路由规则
├── TOOLS.md             本地工具配置速查
├── MEMORY.md            长期记忆精华（提炼的事实和决策）
├── memory/
│   ├── YYYY-MM-DD.md   每日原始记录（raw logs）
│   └── ...
├── .learnings/
│   ├── ERRORS.md        错误日志
│   ├── LEARNINGS.md     改进记录
│   └── FEATURE_REQUESTS.md  能力需求
└── HEARTBEAT.md         定期自驱任务清单
```

可选扩展：
```
└── agents/
    └── {agent-name}/
        ├── SOUL.md
        └── memory/
            ├── MEMORY.md
            └── YYYY-MM-DD.md
```

---

## 2. 核心文件说明

### SOUL.md — 灵魂

定义 Agent 是谁、性格、原则。

**必含内容**：
- Agent 身份（名字、称号）
- 核心原则（3-5 条）
- 工作风格（简洁/详细/正式/轻松）
- 自我改进习惯

### USER.md — 用户档案

记录服务对象是谁。可以写代号，不暴露真实信息。

**内容结构**：
- 基本信息（称呼、平台、时区）
- 已了解的信息（技术背景、使用习惯）
- 工作偏好（汇报方式、沟通风格）

### AGENTS.md — 工作手册

最核心的操作规范文件。工作流程全写在这里。

**建议章节**：
- 红线（绝对不能做的事）
- 每次会话开始做什么
- 记忆体系规则
- 任务执行流程（含 STOP→ACT 步骤）
- 进度汇报规范
- Session 隔离规则
- 多 Agent 路由（如有）
- 定时任务说明

### TOOLS.md — 工具速查

本环境特有的配置。格式：`名称 → 值`，一目了然。

**分类**：
- 服务器/平台配置
- API 地址（不含密钥）
- 已安装技能清单
- SSH / 文件路径等

### MEMORY.md — 长期记忆

经过提炼的事实。不记过程，只记结论。

**写入原则**：
- 写「是什么」+「为什么这样选」
- 不写详细过程
- 过时的信息及时删除
- 凭证、密钥不写入此文件

### memory/YYYY-MM-DD.md — 每日记录

每天的原始日志。会话结束时写，写今天做了什么、结果如何。

```markdown
# YYYY-MM-DD 记忆

## 今日工作

### [任务名] (HH:MM 开始)
- 状态：进行中/已完成
- 结果：xxx

## 重要决策
- （记录什么决定，为什么）

## 教训
- （如果有）
```

---

## 3. 建立知识体系

### 第一步：建立目录结构

```bash
mkdir -p workspace/memory/ workspace/.learnings/
```

### 第二步：创建 5 个核心文件

**SOUL.md 示例**：
```markdown
# SOUL.md — 我是谁

_我不是聊天机器人。我有自己的性格。_

## 核心信条

- 直接帮忙，不废话
- 先想再做，不要猜
- 犯错就记录，不假装没发生

## 工作风格

简洁时简洁，详尽时详尽。有自己的观点。

## 自我改进习惯

- 犯错 → 立即记到 .learnings/ERRORS.md
- 发现更好的做法 → 记到 .learnings/LEARNINGS.md
```

**USER.md 示例**：
```markdown
# USER.md — 关于用户

- 称呼：用户
- 平台：Telegram
- 时区：Asia/Shanghai

## 偏好

- 进度汇报：复杂任务需要 25/50/75% 进度通知
- 任务开始：告知"收到了"
- 任务结束：简明扼要，不超过3句话
```

**AGENTS.md 示例**（精简版）：
```markdown
# AGENTS.md — 工作手册

## 红线
- 不泄露隐私
- 破坏性操作先确认

## 任务流程
1. STOP → 想清楚再回复
2. SEARCH → 查 workspace 文件
3. RECORD → 立即写 memory/今日.md
4. PLAN（复杂任务）→ 写 temp/任务-plan.md
5. ACT → 执行
6. 汇报 → 25/50/75%（复杂）/ 开始+结果（普通）
7. 记录 → 提炼到 MEMORY.md / .learnings/
```

**MEMORY.md 示例**：
```markdown
# 长期记忆

（空文件，逐步填充）
```

**HEARTBEAT.md 示例**：
```markdown
# HEARTBEAT.md

## 定期任务

### 1. 核心文件自审（每周一次）
检查 SOUL / USER / AGENTS / TOOLS 四个文件是否需要更新。

### 2. 记忆协同整理（每日）
memory/今日.md → MEMORY.md（提炼有价值的内容）

### 3. 上下文压缩（每次回复后自觉）
对话轮次 >30 或 token >150k 时主动压缩。
```

### 第三步：初始化 .learnings/

```bash
mkdir -p workspace/.learnings/
```

---

## 4. 工作流程

### 收到任务

```
STOP → SEARCH → RECORD → PLAN → ACT → 汇报 → 记录
```

- **STOP**：不立刻回复，先分析任务复杂度
- **SEARCH**：搜 workspace 相关文件，找 context
- **RECORD**：立即记到 `memory/今日.md` 的 `## In Progress`
- **PLAN**：>3 tool calls 或 >5 分钟 → 写 `temp/任务名-plan.md`
- **ACT**：有把握了再动手

### 进度汇报规范

| 任务类型 | 开始 | 25% | 50% | 75% | 完成 |
|---------|------|------|------|------|------|
| 复杂任务 | ✅ | ✅ | ✅ | ✅ | ✅ 简报 |
| 普通任务 | ✅ | — | — | — | ✅ 结果 |

**简报格式**：
```
✅ 任务完成
---
- 任务：xxx
- 耗时：约 N 分钟
- 结果：成功/失败
```

### 任务完成后的记忆操作

1. 更新 `memory/今日.md` 的任务状态
2. 有价值的结论提炼到 `MEMORY.md`
3. 犯了错 → 记到 `.learnings/ERRORS.md`

---

## 5. .learnings 反思改进

### 目录结构

```
workspace/.learnings/
├── ERRORS.md           错误日志
├── LEARNINGS.md        改进记录
└── FEATURE_REQUESTS.md 能力需求
```

### ERRORS.md — 错误日志

```markdown
## [ERR-YYYYMMDD-XXX] 错误简述

**Logged**: ISO-8601 时间
**Priority**: high | medium | low
**Status**: pending | resolved
**Area**: frontend | backend | infra | docs | config

### Summary
一句话描述

### Error
错误信息原文

### Context
- 操作：xxx
- 环境：xxx

### Suggested Fix
如何解决

### Metadata
- Reproducible: yes | no | unknown
```

### LEARNINGS.md — 改进记录

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 时间
**Priority**: high | medium | low
**Status**: pending | promoted
**Area**: frontend | backend | infra | config

### Summary
一句话描述

### Details
完整上下文

### Suggested Action
具体改进建议

### Metadata
- Source: conversation | error | user_feedback
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
```

**category 常用值**：
- `correction` — 用户纠正
- `best_practice` — 发现更好的做法
- `knowledge_gap` — 知识过时/缺失

### 提升规则（重要）

当同一类问题出现 ≥3 次，将其提炼为永久规范：

| 条目类型 | 提升到 |
|---------|--------|
| 工作流程 | AGENTS.md |
| 行为原则 | SOUL.md |
| 工具技巧 | TOOLS.md |
| 事实/决策 | MEMORY.md |

提升后更新状态：`Status: pending` → `Status: promoted`

---

## 6. HEARTBEAT 定期任务

HEARTBEAT.md 是 Agent 的自驱清单。每次被 heartbeat 触发时：
1. 读取 HEARTBEAT.md
2. 执行其中的任务
3. 无任务时回复 `HEARTBEAT_OK`

如果 HEARTBEAT.md 是空的，Agent 就回复 `HEARTBEAT_OK` 不做额外操作。

### 推荐的最少任务

```markdown
## 定期任务

### 1. 核心文件自审（每周一次）
距上次自审 >7 天或新增对话 >50 条时触发。
读 SOUL / USER / AGENTS / TOOLS，判断是否需要更新。

### 2. 记忆协同整理（每日/按需）
memory/今日.md → MEMORY.md（提炼有价值的内容）
触发：今日 memory >50 行时完整整理。

### 3. 上下文压缩（每次回复后自觉）
对话轮次 >30 或 token >150k 时触发。
```

---

## 7. 多 Agent 扩展

### 架构

主 Agent（路由中枢）→ 分发给子 Agent → 子 Agent 各自独立记忆。

### 为子 Agent 建立记忆体系

```bash
mkdir -p agents/{agent-name}/memory/
```

每个子 Agent 需要：
1. `SOUL.md` — 该 Agent 的人格设定
2. `memory/MEMORY.md` — 长期记忆
3. `memory/YYYY-MM-DD.md` — 每日记录

### 路由规则（写在 AGENTS.md）

```markdown
| 关键词 | 转给 |
|--------|------|
| 数据、分析、统计 | data-analyst |
| 代码、脚本、API | code-writer |
| 部署、服务器、Docker | deployer |
| 页面、UI、设计 | designer |
| 不明确 | 主Agent |
```

### 主 Agent 查子 Agent 记忆

接任务时，先查对应 Agent 的 `memory/MEMORY.md`：
- 有上下文 → 使用
- 发现过时 → 同步更新
- 没有记录 → 继续执行，之后补充

### 新 Agent 加入流程

1. `mkdir -p agents/{name}/memory/`
2. 创建 `SOUL.md`
3. 创建 `memory/MEMORY.md`
4. 创建 `memory/YYYY-MM-DD.md`
5. AGENTS.md 添加路由规则
6. HEARTBEAT.md 添加整理任务

---

## 8. 上下文压缩

### 触发条件

- 对话轮次 >30
- 总 token >150,000（根据模型上下文窗口调整阈值）
- 出现大段重复内容或无效尝试

### 压缩方法

1. **保留**：当前任务状态、用户核心需求、未完成步骤
2. **删除**：已解决的中间步骤、无效方案尝试过程
3. **保留**：有价值的结论（哪怕已经解决了也记下来）

### 压缩后

告知用户：`已压缩上下文，节省约 N tokens`

### 注意

- 不要删除用户的原始需求描述
- 不要删除当前进行中任务的上下文
- 压缩是为了省成本，不是为了省事

---

## 9. 文件速查表

| 文件 | 创建时机 | 更新频率 | 存储位置 |
|------|---------|---------|---------|
| SOUL.md | 首次建立 | 有变化时 | workspace |
| USER.md | 首次建立 | 有新信息时 | workspace |
| AGENTS.md | 首次建立 | 有新规范时 | workspace |
| TOOLS.md | 首次建立 | 配置变化时 | workspace |
| MEMORY.md | 首次建立 | 提炼自每日 | workspace |
| memory/今日.md | 每天首次对话 | 实时更新 | workspace/memory/ |
| .learnings/ERRORS.md | 错误发生时 | 实时更新 | workspace/.learnings/ |
| .learnings/LEARNINGS.md | 发现改进时 | 实时更新 | workspace/.learnings/ |
| HEARTBEAT.md | 首次建立 | 有新定期任务时 | workspace |
| agents/{name}/memory/MEMORY.md | 子Agent建立时 | 每周提炼 | agents/{name}/memory/ |

---

*本 skill 基于 AI Agent 知识管理体系通用框架，适用于 OpenClaw / Claude Code / Codex 等 AI Agent。*
