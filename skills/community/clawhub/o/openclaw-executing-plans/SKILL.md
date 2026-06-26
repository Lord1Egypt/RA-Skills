---
name: superpowers-executing-plans
description: Use when executing a written implementation plan in the current session with sequential task execution and review checkpoints - for when subagent-driven mode is not available
---

# Superpowers Executing Plans（OpenClaw 顺序执行版）

## 概述

加载计划，批判性审查，按顺序执行所有任务，有审查检查点。

**开始时宣布：** "我正在用 executing-plans 技能实现这个计划。"

**注意：** Superpowers 在有 subagent 支持的平台（Claude Code、Codex）工作质量高得多。如果 subagent 可用，用 `superpowers-subagent-dev` 而不是这个技能。

## OpenClaw 适配

OpenClaw 的 `sessions_spawn` 支持 subagent，可以用 `superpowers-subagent-dev` 获得更好质量。这个技能用于：
- subagent 不可用的环境
- 简单任务不需要 subagent 开销
- 学习和测试计划质量

## 流程

### 步骤 1：加载和审查计划

1. 读计划文件
2. 批判性审查——识别任何问题或顾虑
3. 如果有顾虑：开始前向主人提出
4. 如果无顾虑：创建任务列表并继续

### 步骤 2：执行任务

每个任务：
1. 标记为进行中
2. 按计划精确执行每步（计划有小的粒度步骤）
3. 按指定运行验证
4. 标记为完成

### 步骤 3：完成开发

所有任务完成并验证后：
- 宣布："我正在用 finishing-a-development-branch 技能完成这项工作。"
- 使用 `superpowers-finishing-branch` 技能
- 按该技能验证测试、展示选项、执行选择

## 何时停止并求助

**立即停止执行当：**
- 遇到阻塞（缺失依赖、测试失败、指令不清）
- 计划有阻止开始的重大缺口
- 不理解某个指令
- 验证反复失败

**宁可提问，不要猜测。**

## 何时回顾早期步骤

**回到审查（步骤 1）当：**
- 主人根据反馈更新了计划
- 基本方法需要重新思考

**不要强行突破阻塞** — 停止并提问。

## 批次执行（推荐）

对于长计划，按批次执行：

```
每完成 3 个任务：
  → 运行审查（请求 code review）
  → 获得反馈，应用，继续
```

批次审查防止问题级联。

## 计划质量信号

如果计划质量差（步骤模糊、缺少验证、占位符多）：
- 在开始前指出问题
- 与主人讨论解决方案
- 不要强行按坏计划执行

## 记住

- 先批判性审查计划
- 精确按计划步骤执行
- 不要跳过验证
- 引用计划说到的技能
- 阻塞时停止，不要猜
- 未获主人明确同意不要在 main/master 分支上开始实现

## 集成

**必需的工作流技能：**
- `superpowers-isolated-workspace` — 开始前 REQUIRED：建立隔离工作区
- `superpowers-writing-plans` — 创建这个技能执行的计划
- `superpowers-finishing-branch` — 所有任务完成后的收尾
- `superpowers-verification` — 每个步骤验证
- `superpowers-tdd` — 每个任务遵循 TDD
