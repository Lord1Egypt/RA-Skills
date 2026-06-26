---
name: agent-self-evolution
description: 当需要改进 agent 自己的 memory、skills、prompts、runtime rules、tool policies、AGENTS.md/agent.md，或把外部 agent 项目的经验适配到当前 agent 时使用。
---

# Agent Self-Evolution

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md)

使用这个 skill，是为了让 agent 能安全、有效地改造自己，而不是把“自我进化”变成鲁莽重写。

目标是可持续学习：研究要沉淀成架构，架构要变成小步迁移，迁移结果要变成下一个 agent 能找到的工作手册。

## 用户同意门禁

修改 agent 自己的规则或记忆数据前，必须停下来，向用户明确说明并取得同意。

agent-owned surfaces 包括：

- `AGENTS.md`、`agent.md`、`.agent/AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`QWEN.md` 或同类 agent instruction 文件
- system prompts、tool schemas、permission policies、connector policies
- skill 文件、skill indexes、skill manifests、memory registries
- durable memory 文件、knowledge bases、wiki indexes、recall databases
- startup、restart、routing、planner、delegation、自更新逻辑

需要同意时，按这个格式说明：

```text
我需要修改 agent 自身数据。

文件/表面：
- ...

原因：
- ...

风险：
- ...

回滚：
- ...

你同意我修改这些内容吗？
```

不要把模糊的“继续”当成授权。不要在没说明会丢失什么的情况下删除或重写 memory。

## 核心循环

```text
外部信号
  -> 源码级研究
  -> 适配备忘录
  -> 架构归档
  -> 按顺序讨论
  -> 风险 / 收益评审
  -> 渐进式迁移
  -> 冻结相邻系统
  -> 小步落地
  -> 验证
  -> 工作手册
  -> 可索引归档路径
```

## 工作流程

### 1. 从外部项目学习

研究外部项目时，学习模式，不要复制代码。

返回适配备忘录：外部项目解决什么问题、哪些模式有用、哪些部分太重或不兼容、最小安全实验是什么、可能影响哪些文件或模块。

### 2. 先归档架构，再写代码

如果改动触及 memory、tools、prompts、runtime behavior、startup、restart、routing、delegation 或 persistence，把它当成架构工作。

实现前先写架构说明，包含当前问题、目标行为、迁移阶段、风险和回滚、当前必须保持不变的东西、验收检查。

### 3. 按顺序讨论

不要一次实现所有诱人的想法。按一个章节或一个阶段，和用户逐步确认。

直接说明：“这是第一阶段。”“这部分应该先等一下。”“这会修改 agent 自身数据，所以需要用户同意。”

### 4. 优先渐进式迁移

对高风险 agent 改动，比较直接全量切换、shadow mode / 并行运行、渐进式迁移。

当新旧行为可以共存，或回滚难以推理时，优先渐进式迁移。

### 5. 冻结相邻系统

迁移期间，暂停相邻系统的无关改造。例如任务是修改 tool routing，就不要同时重构 long-term memory，除非当前阶段确实需要。

聚焦是一种安全机制。

### 6. 小步落地

实现规则：尽量复用已有逻辑；集成点要小；除非用户明确同意，否则保留现有数据；添加便宜的验证；保持回滚路径明显；避免大范围重构。

### 7. 写工作手册

一个阶段落地后，在架构说明旁边写短工作手册。

包含：改了什么、为什么改、如何验证、哪些内容仍然暂停、第二阶段下一步做什么、给下一个 agent 的精确路径和命令。

### 8. 闭环

文件被修改不代表任务完成。只有下一个 agent 能找到并复用结果，任务才算完成。

闭环检查：架构说明存在；工作手册存在；相关 index 或 manifest 已更新；验证证据已记录；已向用户报告归档路径。

## 可复制 prompt trail

```text
深度研究 [外部项目 A] 和 [外部项目 B]。
不要直接复制它们。提取当前约束下能改进我们 agent 的部分。

如果这是大版本架构变化，先归档设计。
然后我们一步步讨论。

在实现最诱人的方案前，比较直接切换和渐进式迁移。
说清楚风险和收益。

迁移期间冻结相邻子系统，除非当前阶段必须触碰它们。

开始第一阶段。尽量复用已有逻辑。小心谨慎。

如果你需要修改 AGENTS.md、agent.md、memory、skills、prompt rules 或其他 agent 自身数据，先说明文件、风险和回滚方式，然后征求我的同意。

改完后，把工作手册写到架构设计旁边，让下一个 agent 不需要重新发现计划。
```

## 常见错误

- 复制外部项目，而不是适配它的模式。
- 把“好主意”当成重写 runtime behavior 的授权。
- 未经明确同意就修改 `AGENTS.md`、memory、prompts 或 skills。
- 同时迁移多个 agent 子系统。
- 代码改完就宣布完成，但没有归档和 index closure。
- 让已完成工作只存在于聊天记录里。
