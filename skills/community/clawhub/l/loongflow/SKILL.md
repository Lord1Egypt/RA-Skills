---
name: loongflow
description: "LoongFlow brings evolutionary multi-agent optimization to your coding agent harness. Drop it into Codex, Claude Code, Cursor or any OpenClaw agent — then watch PEES (Plan-Execute-Evaluate-Summary) iterate your code, algorithms, or prompts toward a target score, just like a harness-native eval loop but without writing a single test fixture. Two modes: Native PEES (async subagent, zero config, fires-and-forgets into the background) and LoongFlow Engine (full evolutionary search with islands, Boltzmann selection, MAP-Elites diversity, 50+ iterations, checkpoint/resume). Pairs perfectly with any task where 'run it once' isn't good enough. Use when tasks need structured iteration, optimization, evolution, or when user mentions loongflow/PEES."
---

# LoongFlow — PEES 迭代问题求解

当用户希望通过多轮迭代来优化方案时使用此 Skill——代码优化、算法进化、结构化重试与学习，或任何"一次生成质量不够、需要反复打磨"的任务。

## 第一步：分析任务，推荐模式

收到任务后，先分析复杂度，向用户介绍两种模式并给出推荐：

**Native PEES（推荐中小型任务）：**
- 适合：单文件修复、小功能、bug fix、聚焦的质量提升
- 工作方式：**异步 subagent**——任务丢给独立 subagent 跑 PEES 迭代，主 session 立刻释放，不阻塞对话
- 优点：无需额外配置，透明工作区，完成时直接通知用户
- 限制：最多 5 轮迭代，单线程，无种群进化
- 进度：每轮迭代完成后写入 `.loongflow/tasks.json`，统一监控

**LoongFlow Engine（推荐复杂优化任务）：**
- 适合：优化问题、多文件项目、需要 50+ 轮迭代、种群进化
- 工作方式：下载 LoongFlow 框架，后台运行进化引擎，cron 定时汇报进度
- 优点：多岛模型、Boltzmann 选择、MAP-Elites 多样性、断点续跑、成本追踪
- 限制：需要 `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`，有安装步骤
- 源码：https://github.com/baidu-baige/LoongFlow

**先询问用户选择哪种模式，再执行。**

## 第二步：按模式执行

用户确认模式后，读取对应的参考文件并严格按其指令操作：

- **Native PEES** → 读取并遵循 `references/native-pees.md`
- **LoongFlow Engine** → 读取并遵循 `references/engine-mode.md`

## 任务监控（两种模式通用）

所有 LoongFlow 任务（无论 native 还是 engine）都通过统一的任务注册表管理：

- **注册表**：`<agentWorkspace>/.loongflow/tasks.json`
- **监控 cron**：所有任务共用一个 `openclaw cron`，每 10 分钟触发一次。每次向用户推送**有实质内容的进度摘要**：分数趋势（0.XX → 0.XX → 0.XX）、本轮策略（从 plan.md/log 提取）、关键发现（从 summary.md/log 提取）。
- **任务完成**：subagent / engine 直接 `infoflow_send` 最终结果，并将任务标记为 `done`

cron 创建命令详见 `references/monitoring.md`（两种模式共用，不要在各模式文件里单独维护，也不要内联 cron 命令）。

## 架构参考：任务复杂度分级

LoongFlow 将 Agent 任务分为三个层级：

| 层级 | 说明 | 适合场景 |
|------|------|---------|
| **Simple（简单）** | ReAct 循环 + 持久化记忆 | 聊天机器人、工具调用、格式转换 |
| **Standard（标准）** | ReAct + 自我评估 + 迭代改进 | 代码审查、文档生成、数据分析 |
| **Advanced（高级）** | PEES 进化循环 + loongflow-memory | 数学优化、算法设计、NP-hard 问题 |

### 复杂度判断流程

```
任务分析
├── 只需对话 + 简单工具？→ SIMPLE
├── 需要文件操作或代码生成？
│   ├── 有数值评估指标？→ ADVANCED
│   └── 无数值指标？→ STANDARD
└── 需要迭代优化？
    ├── 有明确打分函数？→ ADVANCED
    └── 定性改进？→ STANDARD
```
