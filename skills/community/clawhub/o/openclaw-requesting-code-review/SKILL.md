---
name: superpowers-requesting-code-review
description: Use when completing tasks, implementing major features, or before merging - dispatches code review subagent to catch issues before they cascade, adapted for OpenClaw sessions_spawn model
---

# Superpowers Requesting Code Review（OpenClaw 适配版）

## 概述

在问题级联前派发代码审查 subagent 捕获问题。审查者获得精确构造的上下文做评估——永远不是你 session 的历史。这保持审查者专注在工作产出上，而非你的思维过程。

**核心原则：** 尽早审查，经常审查。

## OpenClaw 适配

Superpowers 原版使用 `Task` 工具派发 code-reviewer subagent。OpenClaw 用 `sessions_spawn`：
- 派发前准备审查上下文（git diff、变更摘要、规格引用）
- 用 `sessions_spawn(mode="run")` 派发一次性审查 session
- 审查结果通过 session 历史或文件系统返回

## 何时请求审查

**强制：**
- subagent-dev 中每个任务完成后
- 完成重大功能后
- Merge 到 main 前

**可选但有价值：**
- 卡住时（新鲜视角）
- 重构前（基线检查）
- 修复复杂 bug 后

## 如何请求

### 1. 收集上下文

```bash
# 获取 git diff
git diff BASE_SHA HEAD > /tmp/review-diff.patch
git log --oneline BASE_SHA..HEAD

# 获取变更统计
git diff --stat BASE_SHA HEAD
```

### 2. 准备审查 prompt

审查 prompt 应包含：
- **实现了什么** — 刚刚构建的内容
- **计划/需求** — 应该做什么
- **基准 SHA** — 起始 commit
- **头部 SHA** — 结束 commit
- **变更描述** — 简要总结

### 3. 派发审查 subagent

```javascript
sessions_spawn({
  task: `代码审查请求

实现了什么：
[具体描述刚完成的工作]

规格/需求：
[任务来自哪个计划，相关规格要求]

变更：
[git diff 关键内容或指向 diff 文件的路径]

请审查：
1. 规格合规——实现是否满足需求？
2. 代码质量——DRY、命名、测试设计
3. 潜在问题——bug、边界情况、安全

返回：strengths、issues（按 severity 分类）、assessment`,
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
```

### 4. 处理反馈

- 立即修复 Critical 问题
- 继续前修复 Important 问题
- 记录 Minor 问题供以后
- 如果审查者错了——用技术理由反驳

## 审查关注点

### 规格合规
- 每个计划需求有对应实现吗？
- 没有做多余的东西？
- 边界情况覆盖了吗？

### 代码质量
- DRY（不要重复自己）？
- 命名清晰有意义？
- 测试覆盖好？
- 没有明显的性能问题？

### 问题严重度

| 级别 | 含义 | 行动 |
|------|------|------|
| **Critical** | 破坏功能或安全 | 立即修复 |
| **Important** | 重要但非破坏 | 继续前修复 |
| **Minor** | 风格/改进建议 | 记录可选做 |

## Red Flags

**永远不要：**
- 因为"简单"就跳过审查
- 忽略 Critical 问题
- 有未修复 Important 问题时继续
- 用合理技术反驳有效反馈

**如果审查者错了：**
- 用技术理由反驳
- 展示证明它工作的代码/测试
- 请求澄清

## 与工作流集成

**Subagent 驱动开发：**
- 每个任务**后**审查
- 在问题级联前捕获
- 继续前修复

**顺序执行：**
- 每个批次（3 个任务）后审查
- 获得反馈，应用，继续

**临时开发：**
- Merge 前审查
- 卡住时审查
