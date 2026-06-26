---
name: multi-thread-dialogue
description: "多线程对话架构：主代理前台响应，子代理后台处理任务，支持打断、状态处理、两阶段审查和任务监控 / Multi-thread dialogue architecture: main agent responds in foreground, sub-agents handle tasks in background, supporting interruption, state handling, two-phase review and task monitoring"
metadata:
  openclaw:
    emoji: "🧵"
    events: []
    requires: {}
---

# Multi-Thread Dialogue / 多线程对话架构

多线程对话架构，让 AI 能够同时处理多个任务，支持打断和任务监控。

Multi-thread dialogue architecture enabling AI to handle multiple tasks simultaneously with interruption support.

## ⚠️ 实现方式 / Implementation

**本 Skill 主要提供文档和辅助工具。核心逻辑通过 AGENTS.md 实现。**

**This Skill primarily provides documentation and auxiliary tools. Core logic is implemented through AGENTS.md.**

原因 / Reason：AGENTS.md 定义了我的行为规则，可以直接实现：
- 任务类型判断 + 触发规则
- 子代理 spawn + 模型选择
- 状态处理（DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED）
- 打断机制 + 状态监控

AGENTS.md defines my behavior rules and directly implements:
- Task type judgment + trigger rules
- Sub-agent spawn + model selection
- State handling (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED)
- Interruption mechanism + state monitoring

无需额外的 Hook。No additional hooks needed.

---

## 功能特性 / Features

### 1. 智能任务分流 / Intelligent Task Routing

| 条件 / Condition | 阈值 / Threshold | 行为 / Behavior |
|------|------|------|
| 简单任务 / Simple task | ≤3 tool calls | 前台处理 / Foreground |
| 长任务 / Long task | >3 tool calls | 后台 spawn 子代理 / Spawn sub-agent |
| 上下文膨胀 / Context bloat | >3000 tokens | spawn 子代理 / Spawn sub-agent |
| 独立任务 / Independent tasks | 多步骤 / Multi-step | 可并行（最多5个）/ Parallel (max 5) |

### 2. 模型选择 / Model Selection

| 复杂度 / Complexity | 模型 / Model | 示例 / Example |
|--------|------|------|
| 机械 / Mechanical | mini/fast | 简单重构 / Simple refactor |
| 标准 / Standard | 继承父模型 / Inherit parent | 功能实现 / Feature implementation |
| 判断 / Judgment | 最强模型 / Strongest | 架构/审查 / Architecture/Review |

### 3. 状态处理 / State Handling

| 状态 / State | 含义 / Meaning | 行为 / Behavior |
|------|------|------|
| `DONE` | 任务完成 / Task complete | 展示结果或进入审查 / Show result or enter review |
| `DONE_WITH_CONCERNS` | 完成但有疑虑 / Complete with concerns | 读取疑虑后决定 / Read concerns then decide |
| `NEEDS_CONTEXT` | 需要更多信息 / Need more info | 提供信息后重新 dispatch / Provide info then redispatch |
| `BLOCKED` | 无法完成 / Cannot complete | 评估原因并处理 / Evaluate cause and handle |

### 4. 质量保障（可选）/ Quality Assurance (Optional)

两阶段审查机制 / Two-phase review mechanism:
```
[实现子代理] → [Spec 审查] → [代码质量审查] → [展示结果]
[Implement Sub-agent] → [Spec Review] → [Code Quality Review] → [Show Result]
```

### 5. 交互模式 / Interaction Mode

- **任务编号 / Task ID**：递增编号 (1, 2, 3...) / Incremental numbering
- **即时介入 / Immediate intervention**：子代理暂停等你操作 / Sub-agent pauses for your input
- **阶段决策 / Phase decision**：完成后汇总让你选 / Summarize after completion for your choice
- **打断 / Interruption**：说"停"或"打断"停止最近任务 / Say "stop" or "interrupt" to halt recent task

### 6. 监控提醒 / Monitoring & Alerts

- 30分钟超时自动提醒 / 30-min timeout auto-alert
- 1天超时自动删除释放资源 / 1-day timeout auto-delete to free resources
- 用户用任务号指定回复 / User can reply by task number

---

## 安装 / Installation

### 1. 安装 Skill / Install Skill

```bash
npx skills add multi-thread-dialogue
# 或 / or
npx skills add multi-thread-dialogue -g
```

### 2. 配置 AGENTS.md（关键步骤）/ Configure AGENTS.md (Key Step)

打开你的 `AGENTS.md` 文件，确保包含"Multi-Thread Dialogue Mode"章节。如果没有，手动添加：

Open your `AGENTS.md`, ensure it contains "Multi-Thread Dialogue Mode" section. Add manually if missing:

```markdown
## 🧵 Multi-Thread Dialogue Mode

### 触发规则 / Trigger Rules
| 条件 / Condition | 阈值 / Threshold | 行为 / Behavior |
|------|------|------|
| 简单任务 / Simple task | ≤3 tool calls | 前台处理 / Foreground |
| 长任务 / Long task | >3 tool calls | spawn 子代理 / Spawn sub-agent |
| 上下文膨胀 / Context bloat | >3000 tokens | spawn 子代理 / Spawn sub-agent |
| 独立任务 / Independent tasks | 多步骤 / Multi-step | 可并行 / Parallel |

### 模型选择 / Model Selection
| 复杂度 | 模型 | 示例 |
|--------|------|------|
| 机械 | mini/fast | 简单重构 |
| 标准 | 继承父模型 | 功能实现 |
| 判断 | 最强模型 | 架构/审查 |

### 状态处理 / State Handling
- DONE: 进入审查或展示结果
- DONE_WITH_CONCERNS: 读取疑虑再决定
- NEEDS_CONTEXT: 提供信息后重新 dispatch
- BLOCKED: 评估原因处理

### 交互 / Interaction
- 任务编号：每个子代理递增编号
- 打断："停"或"打断"停止最近任务
- 指定回复："X号任务..."精准定位

### 监控 / Monitoring
- 等待超30分钟提醒
- 1天超时删除释放资源
```

### 3. 创建任务状态文件 / Create Task State File

```bash
mkdir -p memory
echo '{"nextTaskId": 1, "tasks": []}' > memory/multi-thread-tasks.json
```

---

## 使用方法 / Usage

### Spawn 子代理时使用 Prompt 模板 / Prompt Template for Spawning Sub-agents

```markdown
[任务背景 / Task Background]
你在处理 [项目/领域] 的 [具体任务]。
You are handling [specific task] for [project/domain].

[目标 / Goals]
1. [具体目标1 / Specific goal 1]
2. [具体目标2 / Specific goal 2]

[约束 / Constraints]
- 关注 / Focus on：[具体范围 / Specific scope]
- 优先 / Priority：[重要事项 / Important item]
- 跳过 / Skip：[不需要的 / Not needed]

[输出格式 / Output Format]
返回 / Return：[具体格式 / Specific format]

[完成条件 / Completion Criteria]
完成当 / Complete when：[具体判定标准 / Specific criteria]
```

### 状态标记 / State Markers

子代理完成任务时，在返回结果前明确标记状态：

When sub-agent completes, clearly mark state before returning:

- `DONE` - 任务完成 / Task complete
- `DONE_WITH_CONCERNS: [疑虑内容]` - 完成但有疑虑 / Complete but has concerns
- `NEEDS_CONTEXT: [缺失信息]` - 需要更多信息 / Need more info
- `BLOCKED: [阻塞原因]` - 无法完成 / Cannot complete

### 查看任务状态 / Check Task Status

```
你：任务列表 / 有哪些在跑
→ 显示所有活跃子代理
→ Show all active sub-agents
```

---

## 配置参数 / Configuration Parameters

| 参数 / Parameter | 默认值 / Default | 说明 / Description |
|-----|-------|------|
| 短任务阈值 / Short task threshold | ≤3 次工具调用 / ≤3 tool calls | 判断短任务 / Judge short tasks |
| 卡住阈值 / Stuck threshold | 30 分钟 / 30 min | 等待多久算卡住 / Wait time before stuck |
| 超时删除 / Timeout delete | 1 天 / 1 day | 任务超时后释放资源 / Free resources after timeout |
| 最大并行 / Max parallel | 5 | 最多并行子代理数 / Max parallel sub-agents |

---

## 文件结构 / File Structure

```
multi-thread-dialogue/
├── SKILL.md                    # 本文件 / This file
├── _meta.json                  # 元数据 / Metadata
├── skill.yaml                  # Skill 配置 / Skill config
├── README.md                   # 英文版说明 / English version
└── docs/
    └── multi-thread-dialogue-plan.md  # 完整方案文档 / Complete plan doc
```

---

## 类似技能 / Similar Skills

- `skill-creator`: 技能创建工具 / Skill creation tool
- `subagent-creator`: 子代理创建器 / Sub-agent creator (tech-leads-club)
- `codex-subagent`: Codex 子代理 / Codex sub-agent (am-will)
- `superpowers`: Subagent 驱动开发 / Subagent-driven development (obra)
