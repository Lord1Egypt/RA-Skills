---
name: kinema-task-management
displayName: "Kinema's Task Management (daily report, active push, traceback)"
version: 1.1.0
description: |
  Kinema personal task tracking system. AI Agent maintains tasks as markdown files in workspace.
  Trigger: User describes tasks, mentions "任务", "task", asks to create/update/archive/check tasks, uses `/mytask`, or receives task-related cron heartbeat.
---

# Kinema's Task Management | Kinema 个人任务追踪系统

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/kinema-task-management

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [ONBOARDING.md](ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 ONBOARDING.md 完成全部步骤
- **环境不可用**（目录缺失、cron 未配置）→ 读取 ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方操作指南

---

## Core Principles | 核心原则

1. **你说我存** — 用户用自然语言描述任务，Agent 提问补全后结构化存储
2. **不可擅动** — 未经用户明确同意，不修改任何任务的状态
3. **主动确认** — Agent 发现某个任务可能已完成时，向用户确认后才标记
4. **每日推送** — 每天固定时间推送任务报告

---

## Data Structure | 数据结构

### 目录路径

```
TASK_DIR=~/.openclaw/workspace/kinema-tasks
```

### 文件夹结构

```
kinema-tasks/
├── active/      ← 活跃任务（Pending / In Progress / Snoozed）
├── archived/    ← 终结任务（Done / Cancelled）
└── snapshots/   ← 每日快照，按日期保存 YYYY-MM-DD.md
```

### 序号管理

- 序号 5 位递增：`TASK-00001` → `TASK-00002` → ...
- 创建新任务时，使用 `scripts/next-id.sh` 获取下一个可用序号
- 序号全局唯一，`active/` 和 `archived/` 共享同一序号空间
- 序号不可复用：已使用的序号永久保留

---

## Task File Format | 任务文件格式

每个任务一个独立 Markdown 文件：`TASK-XXXXX.md`

```markdown
# TASK-00001: {标题}

## Metadata

| 字段 | 值 |
|------|-----|
| 状态 | Pending |
| 优先级 | urgent |
| 领域 | OpenClaw生态 |
| 截止日期 | 2026-04-10 |
| 创建时间 | 2026-04-07 |
| 最后更新 | 2026-04-07 |

## 描述

{任务的详细描述，自由格式纯文本}

## Changelog

| 时间 | 变更 |
|------|------|
| 2026-04-07 | 创建任务，状态: Pending |
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| 状态 | 是 | `Pending` / `In Progress` / `Done` / `Snoozed` / `Cancelled` |
| 优先级 | 是 | `urgent` / `normal` / `low` |
| 领域 | 是 | 预设：`OpenClaw生态` / `其他项目` / `生活`，可扩展 |
| 截止日期 | 否 | `YYYY-MM-DD`，无截止日期填 `—` |
| 创建时间 | 是 | `YYYY-MM-DD` |
| 最后更新 | 是 | `YYYY-MM-DD`，每次变更时更新 |
| 描述 | 否 | 自由格式纯文本 |
| Changelog | 是 | 按时间正序追加，不修改已有记录 |

---

## Status Flow | 状态流转

```
┌──────────┐
│ Pending  │
└────┬─────┘
     │ 开始执行
     ▼
┌──────────────┐     完成（需用户确认）
│ In Progress  │────────→ Done → archived/
└──────┬───────┘
       │ 暂停
       ▼
┌──────────┐
│ Snoozed  │
└──────────┘

任意状态 ──→ Cancelled（需用户确认）→ archived/
```

### 转换规则

| 变更 | 触发方式 | 需要确认 |
|------|---------|---------|
| Pending → In Progress | 用户指令 | 否 |
| In Progress → Pending | 用户指令 | 否 |
| ↔ Snoozed | 用户指令 | 否 |
| → Done | Agent 主动或用户指令 | **是** |
| → Cancelled | 用户指令 | **是（二次确认）** |
| Done / Cancelled | 状态变更后 | 自动移入 `archived/` |

---

## Operations | 五种操作

### 1. 创建任务

**触发**：用户描述新任务

**流程**：
1. 接收自然语言描述
2. 提问补全缺失必填信息（优先级、领域、截止日期）
3. 用户确认后，使用 `scripts/create-task.sh` 创建文件
4. 返回任务摘要确认

```
用户: "ClawHub publish 命令在遇到同名版本时报错没有清晰提示"
Agent: "收到，确认几个信息：
 1. 优先级？urgent / normal / low
 2. 属于哪个领域？OpenClaw生态 / 其他项目 / 生活
 3. 截止日期？
 4. 补充描述？还是就按你说的来？"
```

### 2. 更新任务

**触发**：用户明确指令

**流程**：
1. 直接修改对应的 `.md` 文件
2. 更新 Metadata 表中相关字段和最后更新时间
3. 在 Changelog 中追加变更记录
4. 状态变为 Done/Cancelled → 使用 `scripts/archive-task.sh` 移入 `archived/`

```
用户: "TASK-00003 标记为 In Progress"
用户: "TASK-00001 的截止日期改到 4月20日"
```

### 3. 批量操作

**触发**：用户指令涉及多个任务

**流程**：
1. 解析意图，确定受影响任务列表
2. 向用户展示将要修改的任务清单，请求确认
3. 逐个修改文件（每个文件独立更新 Metadata + Changelog）
4. 返回操作摘要

```
用户: "把所有 normal 的任务截止日期都推迟一天"
Agent: "以下任务将被修改：
 - TASK-00002（截止 04/10 → 04/11）
 - TASK-00005（截止 04/20 → 04/21）
 确认执行？"
```

### 4. 取消任务

**触发**：用户明确说"取消"或"删除"某个任务

**流程**：
1. Agent 向用户确认（**取消不可逆**）
2. 用户同意 → 状态改为 `Cancelled`，Changelog 追加记录，移入 `archived/`
3. 返回确认

### 5. 主动询问

**触发条件**：
- 对话中明显完成了某个任务的工作
- 任务描述与最近对话内容高度匹配
- Agent 有合理依据认为任务已达成

**流程**：
1. 向用户提出确认
2. 同意 → 标记 Done，移入 `archived/`
3. 拒绝 → 不修改

---

## Daily Report | 每日推送

### 推送时间

北京时间 09:00（UTC 01:00），每天一次

### 推送格式

```
📋 KinemaTasks Daily Report — {M月D日}

{2-3句话状况摘要，由模型根据下方 section 内容生成，非固定模板}

Status: ▶ in_progress ○ pending ✓ done

● URGENT ────────────────────────────────────────────────────────────
▶ TASK-XXXXX Apr 09 2d left 标题 #领域
○ TASK-XXXXX Apr 10 3d left 标题 #领域

● NORMAL ────────────────────────────────────────────────────────────
○ TASK-XXXXX Apr 11 4d left 标题 #领域
✓ TASK-XXXXX Apr 06 done 标题 #领域

● LOW ────────────────────────────────────────────────────────────────
○ TASK-XXXXX — 标题 #领域

● SNOOZED ────────────────────────────────────────────────────────────
○ TASK-XXXXX Apr 12 5d left 标题 #领域

● EXPIRED ────────────────────────────────────────────────────────────
○ TASK-XXXXX Apr 01 6d overdue 标题 #领域

───────────────────────────────────────────────────────────────────────

● RECENTLY DONE ───────────────────────────────────────────────────────
✓ TASK-XXXXX Apr 06 done 标题 #领域

───────────────────────────────────────────────────────────────────────

新增 (N)
 TASK-XXXXX 标题 | 优先级 | 领域

状态变更 (N)
 TASK-XXXXX 旧状态 → 新状态

字段变更 (N)
 TASK-XXXXX 字段 旧值 → 新值

取消 (N)
 TASK-XXXXX 标题
```

### 状态图例

| 符号 | 状态 |
|------|------|
| ▶ | In Progress |
| ○ | Pending / Snoozed |
| ✓ | Done |

### 条目格式

每行格式：`{符号} TASK-XXXXX {日期} {时间提示} {标题} #{领域}`

- 日期：`Apr 09` 格式，无截止日期显示 `—`
- 时间提示：`Nd left` / `due today` / `Nd overdue` / `done`（仅已完成任务）/ 无（无截止日期）
- 领域：`#领域` 格式

> 最近完成的 Done 任务单独列出在「RECENTLY DONE」section，最近 5 条，按完成时间倒序，Cancelled 不展示。

### 触发方式

报告有两种触发方式：

| 方式 | 触发者 | 执行者 | 说明 |
|------|--------|--------|------|
| **定时推送** | Cron（每天 09:00/09:01/09:02 BJT） | Isolated session agent | cron 依次执行归档→报告→快照，推送结果 |
| **手动查询** | 用户在对话中询问 | 当前 session agent | Agent 直接在对话中执行，不走 cron |

#### 定时推送流程（Cron）

1. 归档检查 cron 扫描 active/，移入 archived/
2. 报告 cron 读取 SKILL.md 规范，扫描任务文件，调用 `report.sh` 生成结构化内容，**由模型撰写 2-3 句摘要**，组装完整报告并推送
3. 快照 cron 调用 `snapshot.sh` 写入当日快照

#### 手动查询流程

触发：用户输入 `/mytask`、询问"看看任务"、"任务列表"、"任务报告"等

1. Agent 扫描 `active/` 和 `archived/` 中所有任务文件
2. 按 SKILL.md 中的推送格式生成完整报告
3. **由模型撰写 2-3 句摘要**（基于各 section 统计）
4. 直接在对话中返回报告，无需调用 cron

> `/mytask` 可直接触发手动查询，无需额外参数。

> `report.sh` 输出的是不含摘要的结构化部分（当前任务状况 + 昨日变动）。摘要由 Agent 模型根据 `report.sh` 的输出内容自行撰写。

### Diff 计算规则

对比**最近一次快照**与当前 `active/` 状态：

| 变动类型 | 判断依据 |
|---------|---------|
| 新增 | 任务 ID 在上次快照中不存在 |
| 状态变更 | 状态字段值不同（Cancelled 单独归入"取消"） |
| 字段变更 | 优先级 / 领域 / 截止日期字段值不同 |
| 取消 | 上次快照中存在、当前 `archived/` 中状态为 Cancelled |

> 无上次快照 → 跳过 diff 部分，只输出当日任务状况
> 无变动 → diff 部分显示"无变动"

### 当日任务状况分组

| Section | 包含 | 排除 | 排序 |
|---------|------|------|------|
| ● URGENT | 优先级 = urgent，未过期 | Snoozed 状态 | 剩余时间升序，无截止日期排末尾 |
| ● NORMAL | 优先级 = normal，未过期 | Snoozed 状态 | 同上 |
| ● LOW | 优先级 = low，未过期 | Snoozed 状态 | 同上 |
| ● SNOOZED | 状态 = Snoozed（无论是否过期） | 无 | 剩余时间升序，无截止日期排末尾 |
| ● EXPIRED | Pending/InProgress + 已过期 | Snoozed 状态 | 过期天数降序（过期最久排前） |
| ● RECENTLY DONE | archived/ 中最近 5 条 Done 任务 | Cancelled | 完成时间倒序 |

最近完成的 Done 任务单独列出在「RECENTLY DONE」section，最近 5 条，按完成时间倒序，Cancelled 不展示。

**时间提示格式**：
- 未过期有截止日期：`Nd left`（如 `2d left`）
- 今天截止：`due today`
- 已过期：`Nd overdue`（不再追加 ⚠️）
- 已完成：`done`
- 无截止日期：不显示时间提示

**核心规则**：Snoozed 状态优先，即使过期也不出现在「EXPIRED」中。

---

## Snapshot | 每日快照

### 格式

```markdown
# Snapshot — {YYYY-MM-DD}

> 生成时间：{YYYY-MM-DD} 09:00 BJT

## 任务列表

| 任务 | 标题 | 状态 | 优先级 | 领域 | 截止日期 |
|------|------|------|--------|------|---------|
| TASK-XXXXX | 标题 | 状态 | 优先级 | 领域 | 截止日期 |

## 摘要

共 N 个活跃任务 | N In Progress · N Pending · N Snoozed
```

快照文件由 cron 写入，不应手动修改。

---

## Cron Jobs | 定时任务

| 任务 | 时间（BJT） | Cron Name | 说明 |
|------|------------|-----------|------|
| 归档检查 | 09:00 | `kinema-tasks-archive-check` | 扫描 active/ 中 Done/Cancelled 文件，更新 Changelog 并移入 archived/ |
| 每日早报 | 09:01 | `kinema-tasks-daily-report` | 读取最近快照 + 当前 active 生成 diff + 报告，推送到对话 |
| 写入快照 | 09:02 | `kinema-tasks-write-snapshot` | 扫描 active/ 生成快照写入 snapshots/YYYY-MM-DD.md |

> 三个 cron 使用 `--session isolated` + `--channel` + `--to` + `--announce`，配置步骤详见 ONBOARDING.md Step 2（确定推送通道）和 Step 4（创建 cron 任务）。
> 严格按顺序执行：归档检查 → 早报推送 → 写入快照

---

## Helper Scripts | 辅助脚本

所有脚本位于 `scripts/` 目录，通过 `TASK_DIR` 环境变量控制路径，默认 `~/.openclaw/workspace/kinema-tasks`。

| 脚本 | 用途 |
|------|------|
| `next-id.sh` | 获取下一个可用任务序号 |
| `create-task.sh` | 创建任务文件（模板填充） |
| `archive-task.sh` | 将任务移入 archived/ |
| `snapshot.sh` | 生成并写入当日快照 |
| `report.sh` | 生成每日报告（输出到 stdout） |

---

## Domain Tags | 领域标签

| 领域 | 说明 |
|------|------|
| OpenClaw生态 | Skill 开发、生态调研、社区贡献 |
| 其他项目 | 非 OpenClaw 的技术项目 |
| 生活 | 非技术类事务 |

可自由扩展，创建任务时由用户指定或 Agent 提议。

---

## Rules | 注意事项

- **禁止自动完成**：未经确认不将任务标记为 Done 或 Cancelled
- **取消不可逆**：Cancelled 执行前必须二次确认
- **文件原子性**：状态变更和文件移动在同一操作中完成
- **Changelog 只追加**：不修改已有记录
- **序号不可复用**：已使用序号永久保留
- **描述为纯文本**：不做结构化拆分
- **快照只读**：仅由 cron 写入
- **Cron 顺序固定**：归档 → 报告 → 快照
