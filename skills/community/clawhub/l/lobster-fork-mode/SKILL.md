---
name: lobster-fork-mode
description: "Fork子Agent模式 — 子Agent继承父上下文。当需要子Agent了解父会话的关键上下文时自动激活。"
metadata: {"openclaw":{"requires":["sessions_spawn","read","memory_search"]}}
---

# Fork Mode — 子Agent上下文继承

参考 Claude Code 的 `forkSubagent.ts` 和 `runForkedAgent()`。

## 问题
`sessions_spawn` 创建的子Agent是全新会话，没有父会话的上下文。这导致子Agent缺少关键信息。

## 解决方案
在spawn子Agent时，手动注入父上下文。

## Fork 模板

### Step 1: 收集父上下文
```
需要注入的上下文：
1. 当前任务的目标和约束
2. 相关文件路径和关键代码片段
3. 已做出的决策和原因
4. 用户偏好（从MEMORY.md提取）
5. 项目结构概要
```

### Step 2: 构建Fork Prompt
```
你是一个子Agent，从父会话 fork 出来。以下是你的继承上下文：

## 父会话上下文
{从Step 1收集的信息}

## 你的任务
{具体任务描述}

## 约束
- 工具白名单：{从Agent定义读取}
- 不要修改父会话的文件（除非明确要求）
- 完成后返回：{期望的输出格式}
```

### Step 3: Spawn
```
sessions_spawn:
  runtime: "subagent"
  mode: "run"
  task: "{Fork Prompt}"
  streamTo: "parent"
```

## 上下文大小控制

| 上下文类型 | 最大长度 | 截断策略 |
|-----------|---------|---------|
| 任务目标 | 500字 | 保留核心需求 |
| 文件路径 | 10个文件 | 保留最相关的 |
| 代码片段 | 2000字 | 保留签名+关键逻辑 |
| 决策记录 | 5条 | 保留最新的 |
| 用户偏好 | 3条 | 保留最相关的 |

## 缓存共享（模拟Claude Code的CacheSafeParams）

OpenClaw没有prompt cache共享机制，但可以通过以下方式减少重复：
1. 子Agent使用相同模型（model: zai/glm-5.1）
2. system prompt结构一致
3. 避免在task中重复注入完整的SKILL.md内容

## 适用场景

| 场景 | Fork模式 | 普通spawn |
|------|---------|----------|
| 需要了解项目背景 | ✅ | ❌ |
| 需要知道已做决策 | ✅ | ❌ |
| 纯机械任务（格式化、搜索） | ❌ | ✅ |
| 需要用户偏好 | ✅ | ❌ |
| 独立的新项目 | ❌ | ✅ |
