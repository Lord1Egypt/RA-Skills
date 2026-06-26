---
name: huo15-openclaw-multi-agent
displayName: 火一五多智能体技能
description: 火一五多智能体协同 - 基于 OpenClaw sessions_spawn 的多 Agent 并行工作系统。支持协调者模式、任务分配、结果汇总。触发词：多智能体协同、多 Agent、并行任务、协调者模式。
version: 2.3.0
dependencies:
  optional: ["huo15-memory-evolution", "huo15-cost-tracker"]
aliases:
  - 火一五多智能体技能
  - 火一五多Agent技能
  - 火一五协调者技能
  - 火一五并行任务技能
  - 火一五Agent协同技能
  - 多智能体
  - multi agent
  - sessions_spawn
---

# 🤖 火一五多智能体协同 (huo15-multi-agent)

> **作者**: 火一五信息科技有限公司  
> **版本**: v2.3.0  
> **基于**: OpenClaw `sessions_spawn`(对齐 2026.6.8 官方 `docs/tools/subagents.md`)

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
| `/subagents list` | 查看当前会话的子 Agent |
| `/subagents log <id 或 #> [limit] [tools]` | 查看子 Agent 日志 |
| `/subagents info <id 或 #>` | 运行元信息(状态/时间/会话id/transcript) |

> ⚠️ 没有 `/subagents spawn` 或 `kill`:派生用工具 `sessions_spawn`;停止/清理由运行超时 + 自动归档(`archiveAfterMinutes`,默认 60 分钟)管理。线程绑定另有 `/focus` `/unfocus` `/agents`。

### 2.3 编程接口

```javascript
// 派生子 Agent(非阻塞,立刻返回 run id;完成时自动 announce 回来)
sessions_spawn({
  task: "分析代码仓库 A",       // 必填
  label: "code-analyzer-a",    // 可选,人类可读标签
  taskName: "analyze_repo_a",  // 可选,稳定句柄(供后续定位/嵌套编排)
  context: "isolated"          // 默认 isolated;需继承当前对话上下文才用 "fork"
})
// 注:sessions_spawn 不接受 per-call 超时;超时在配置 agents.defaults.subagents.runTimeoutSeconds

// 派生后若本轮必须等子结果 → 用 sessions_yield 结束本轮,完成事件作为下一条消息到达
sessions_yield()

// 按需查看子 Agent 状态(调试用,切勿轮询)
subagents()
```

---

## 三、工作流程(push 完成模型,**非轮询**)

> openclaw 官方铁律:`sessions_spawn` 非阻塞,**完成是 push 的**。派生后**不要**用 `Promise.all` / `sessions_history` / `sessions_list` / `sleep` 轮询等结果——用 `sessions_yield`。

### 3.1 派生并行任务

```javascript
// 依次派生 3 个 Worker,每个调用立刻返回 run id(不阻塞、不 await)
sessions_spawn({ task: "分析模块 A", taskName: "module_a" })
sessions_spawn({ task: "分析模块 B", taskName: "module_b" })
sessions_spawn({ task: "分析模块 C", taskName: "module_c" })
```

### 3.2 让出本轮,等完成事件

```javascript
// 结束当前回合;子 Agent 完成事件会作为下一条消息送回(前提:工具列表含 sessions_yield)
sessions_yield()
```

完成后 openclaw 把每个子 Agent 结果以 `agent` 回合 **announce** 回当前会话;活动期间还会注入 `Active Subagents` 块让你看到状态,无需轮询。

### 3.3 汇总报告

子结果到达后,协调者(主 Agent)综合各 Worker 的 announce 内容,核对后再决定是否给用户最终答复。需回看某子 Agent 历史时用 `sessions_history`(有界、安全过滤)——**仅按需调用,不要循环**。

---

## 四、配置

### 4.1 OpenClaw 配置

在 `~/.openclaw/openclaw.json`(键路径 `agents.defaults.subagents`):

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,        // 默认 1(子 Agent 不能再派生);设 2 开启一层嵌套(orchestrator)
        maxChildrenPerAgent: 5,  // 每 Agent 同时活动子数上限(默认 5)
        maxConcurrent: 8,        // 全局并发上限(默认 8)
        runTimeoutSeconds: 900,  // sessions_spawn 默认超时秒(0=不超时)
        model: "MiniMax-M2.1",   // 子 Agent 默认模型(省钱;留空=继承主 Agent)
      },
    },
  },
}
```

### 4.2 开启 sessions_spawn 工具

`coding` / `full` 工具档默认暴露 `sessions_spawn`;`messaging` 档不暴露。要让某 Agent 能派生:

```json5
{
  agents: {
    list: [{
      id: "coordinator",
      tools: {
        // 二选一:整档切 coding,或在现档基础上追加这几个工具
        profile: "coding",
        alsoAllow: ["sessions_spawn", "sessions_yield", "subagents"],
      },
    }],
  },
}
```

> 用 `/tools` 查当前会话生效的工具列表确认。

---

## 五、最佳实践

### 5.1 任务拆分原则

- 每个 Worker 任务独立，不依赖其他 Worker
- 任务时长建议 5-30 分钟
- 嵌套上限 depth 2:主(0)→ 编排子(1)→ leaf worker(2),leaf 不能再派生;默认 `maxSpawnDepth: 1` 即不嵌套

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
| **v2.3.0** | 2026-06-20 | 按 2026.6.8 官方 `docs/tools/subagents.md` 校正:`/subagents` 子命令(list/log/info)、push 完成模型 + `sessions_yield`(替代轮询)、移除非法 per-call `runTimeoutSeconds`、配置文件改 `openclaw.json` + 工具档 `tools.profile/alsoAllow`、嵌套 depth 语义 |
| v2.0.0 | 2026-04-05 | 集成 OpenClaw sessions_spawn |
| v1.0.0 | 2026-04-05 | 初始版本（纯脚本） |
