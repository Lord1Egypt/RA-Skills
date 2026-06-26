# MULTI-INSTANCE.md - 多实例运行

> 并行工作，提高效率

---

## 多实例架构

```
Main Agent (Odin)
  │
  ├── Atlas (协调)
  │     └── 任务分发
  │
  ├── Buffett (投资)
  │     └── 并行研究多个标的
  │
  ├── Jobs (内容)
  │     └── 多平台发布
  │
  └── Byte (工程)
        └── 多任务处理
```

---

## 运行模式

### 1. 子Agent委派
```
sessions_spawn(
  agentId: "elliott",
  task: "分析 BTC 走势"
)
```

### 2. 并行任务
```
同时运行多个 subagent
- Agent A: 研究项目X
- Agent B: 研究项目Y
- Agent C: 研究项目Z
```

### 3. 多实例部署
- 不同端口运行多个 Gateway
- 支持不同配置
- 隔离运行环境

---

## 实例管理

### 查看实例
```bash
openclaw status
```

### 启动新实例
```bash
openclaw gateway start --port 18790
```

### 实例间通信
```
sessions_send(sessionKey, message)
```

---

## 使用场景

| 场景 | 方案 |
|------|------|
| 复杂任务分解 | subagent 委派 |
| 并行研究 | 多 subagent |
| 多环境隔离 | 多实例 |
| 负载均衡 | 轮询分配 |

---

*更新: 2026-03-07*
