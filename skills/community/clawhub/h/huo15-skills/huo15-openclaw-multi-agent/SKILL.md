---
name: huo15-openclaw-multi-agent
description: 火一五多智能体协同 - 基于 OpenClaw sessions_spawn 的多 Agent 并行工作系统。支持协调者模式、任务分配、结果汇总。触发词：多智能体协同、多 Agent、并行任务、协调者模式。
version: 2.2.0
dependencies:
  optional: ["huo15-memory-evolution", "huo15-cost-tracker"]
---

# 🤖 火一五多智能体协同 (huo15-multi-agent)

> **作者**: 火一五信息科技有限公司  
> **版本**: v2.0.0  
> **基于**: OpenClaw sessions_spawn

---

## 一、核心概念

| 概念 | 说明 |
|------|------|
| **Coordinator** | 主 Agent，协调任务分配 |
| **Worker** | 工作 Agent，执行具体任务 |
| **sessions_spawn** | OpenClaw 内置派生子 Agent |
| **announce** | 结果自动汇报给主 Agent |

### OpenClaw subagent 架构

```
主 Agent (depth 0)
    ↓ sessions_spawn
Worker A (depth 1) ─┐
Worker B (depth 1) ─┼─ 执行中...
Worker C (depth 1) ─┘
    ↓ announce 汇报
主 Agent ← 接收结果汇总
```

---

## 二、使用方式

### 2.1 协调者模式触发

当用户说"帮我同时处理..."时：

```
用户: "帮我同时分析这三个项目的代码"
  ↓
我: "好的，启动协调者模式，分3个并行任务"
  ↓
使用 sessions_spawn 启动 3 个 Worker
  ↓
Worker 们并行执行，完成后 announce 结果
  ↓
汇总结果，报告给用户
```

### 2.2 命令参考

| 命令 | 说明 |
|------|------|
| `/subagents list` | 查看所有子 Agent |
| `/subagents spawn <任务>` | 启动子 Agent |
| `/subagents kill <id>` | 停止子 Agent |
| `/subagents log <id>` | 查看子 Agent 日志 |

### 2.3 编程接口

```javascript
// 派生子 Agent
sessions_spawn({
  task: "分析代码仓库 A",
  label: "code-analyzer-a",
  runTimeoutSeconds: 300
})

// 发送消息给子 Agent
sessions_send(sessionKey, "状态如何？")

// 查看子 Agent 列表
subagents(action="list")
```

---

## 三、工作流程

### 3.1 启动并行任务

```javascript
// 并行启动 3 个任务
const results = await Promise.all([
  sessions_spawn({ task: "分析模块 A", label: "module-a" }),
  sessions_spawn({ task: "分析模块 B", label: "module-b" }),
  sessions_spawn({ task: "分析模块 C", label: "module-c" })
])
```

### 3.2 等待结果

子 Agent 完成后自动 announce 结果到当前会话。

### 3.3 汇总报告

```javascript
// 收集所有结果
const allResults = await Promise.all(
  workerSessions.map(key => sessions_history(key, { limit: 1 }))
)

// 汇总给用户
const summary = synthesizeResults(allResults)
```

---

## 四、配置

### 4.1 OpenClaw 配置

在 `~/.openclaw/config.json` 中启用嵌套：

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2,
        "maxConcurrent": 8,
        "runTimeoutSeconds": 900
      }
    }
  }
}
```

### 4.2 子 Agent 权限

```json
{
  "tools": {
    "subagents": {
      "tools": {
        "allow": ["read", "exec", "process"],
        "deny": ["gateway", "cron"]
      }
    }
  }
}
```

---

## 五、最佳实践

### 5.1 任务拆分原则

- 每个 Worker 任务独立，不依赖其他 Worker
- 任务时长建议 5-30 分钟
- 避免深度嵌套（depth 2 足够）

### 5.2 成本控制

```javascript
// 子 Agent 使用更便宜的模型
sessions_spawn({
  task: "简单分析",
  model: "MiniMax-M2.1"  // 比主 Agent 便宜
})
```

### 5.3 错误处理

```javascript
try {
  const result = await sessions_spawn({
    task: "可能失败的任务"
  })
} catch (e) {
  // 处理超时或失败
  reportError(e)
}
```

---

## 六、与传统方式对比

| 方式 | 同步 | 并行 | 结果汇总 |
|------|------|------|---------|
| 顺序执行 | ✅ | ❌ | 手动 |
| 传统 skill | ⚠️ | ⚠️ | 手动 |
| **sessions_spawn** | ❌ | ✅ | 自动 announce |

---

## 七、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **v2.0.0** | 2026-04-05 | 集成 OpenClaw sessions_spawn |
| v1.0.0 | 2026-04-05 | 初始版本（纯脚本） |
