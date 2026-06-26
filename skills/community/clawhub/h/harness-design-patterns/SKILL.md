---
name: harness-design-patterns
version: 1.0.0
description: Agent harness 架构设计模式知识库。当设计多阶段任务的上下文传递、选择多 agent 协调方式、或规划 hook 系统架构时使用。纯设计指南，无可执行代码。不用于安装 hook 脚本（用 agent-hooks）或运维监控（用 agent-ops）。
license: MIT
triggers:
  - harness design
  - agent architecture
  - handoff document
  - context survival
  - multi agent coordination
  - coordinator vs fork
  - hook architecture
  - 上下文存活
  - 多 agent 协调
  - harness pattern
---

# Harness Design Patterns

Agent harness 架构设计决策参考。蒸馏自 Claude Code 内部架构、OMC、Anthropic/OpenAI harness engineering 博客。

## When to Use

- 设计多阶段任务的上下文传递方案 → Handoff 文档 / Compaction 提取
- 选择多 agent 的协调模式 → Coordinator / Fork / Swarm 选型
- 设计 hook 系统架构 → Hook Pair Bracket / Component-Scoped / Profiles
- 评估任务复杂度以选择执行强度 → Adaptive Complexity

## When NOT to Use

- 需要可执行的 hook 脚本 → 用 `agent-hooks`
- 需要运维工具（限速恢复、session 监控） → 用 `agent-ops`
- 需要 prompt 硬化 → 用 `prompt-hardening`

---

## 10 个设计模式

| # | 模式 | 解决什么 | 详情 |
|---|------|---------|------|
| 1 | **Handoff 文档** | 跨阶段/跨压缩的上下文传递 | [详情](references/02-handoff.md) |
| 2 | **原子文件写入** | 并发状态文件安全 | [详情](references/06-atomic-write.md) |
| 3 | **Compaction 记忆提取** | 压缩前被动抢救知识（PreCompact hook） | [详情](references/08-compaction-extract.md) |
| 4 | **权限否决追踪** | 防止 agent 绕过拒绝 | [详情](references/09-denial-tracking.md) |
| 5 | **三门控记忆合并** | 跨 session 记忆碎片化 | [详情](references/10-memory-consolidation.md) |
| 6 | **Hook Pair Bracket** | 每轮 context/时间测量 | [详情](references/11-hook-bracket.md) |
| 7 | **Component-Scoped Hooks** | 任务级别的 hook 控制 | [详情](references/12-scoped-hooks.md) |
| 8 | **三种委托模式** | 多 agent 协调方式选型 | [详情](references/14-delegation-modes.md) |
| 9 | **Adaptive Complexity** | 任务复杂度自适应 | [详情](references/16-adaptive-complexity.md) |
| 10 | **Hook Runtime Profiles** | 环境级 hook 强度控制 | [详情](references/18-hook-profiles.md) |

> 注：reference 文件名保留原始编号（02/06/08/...）以兼容 monorepo 中的交叉引用。

## 常见场景选型

| 场景 | 推荐模式 |
|------|---------|
| 多阶段任务（plan → implement → verify） | Handoff 文档 + Compaction 提取 |
| 选择 Coordinator / Fork / Swarm | 三种委托模式选型指南 |
| Hook 太多互相干扰 | Component-Scoped Hooks + Hook Profiles |
| 不同环境需要不同保障级别 | Hook Runtime Profiles (minimal/standard/strict) |
| 简单任务 overhead 太高 | Adaptive Complexity (triage → 自动选执行模式) |

## 工作流程

### Step 1: 识别问题

当遇到 agent 可靠性问题时，判断属于哪一类：上下文丢失、协调混乱、hook 冲突、或执行强度不匹配。

### Step 2: 选型

根据「常见场景选型」表找到对应模式，MUST 先读 reference 详情再做决策，otherwise 可能误用模式。

### Step 3: 应用

如果需要可执行脚本 → 切换到 `agent-hooks` skill。如果需要运维工具 → 切换到 `agent-ops` skill。如果不确定 → 先从最简单的模式开始试验。

## Output

当被询问 harness 设计建议时，returns:
- 推荐的模式名称及原因
- 该模式的 tradeoff 说明
- 具体的实施步骤指引（指向 agent-hooks 或 agent-ops 中的脚本）

## 延伸阅读

- [蒸馏方法论](references/distillation-methodology.md) — PCA 降维类比、Review-Execution 分离
- [质量测评体系集成](references/quality-pipeline-integration.md) — 与 improvement-* skill family 的接入点
