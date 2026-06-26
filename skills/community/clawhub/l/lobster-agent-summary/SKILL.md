---
name: lobster-agent-summary
description: Agent进度摘要系统，定期检查子Agent状态并生成简短进度报告。参考Claude Code的AgentSummary机制，每30秒对子Agent生成3-5词状态摘要。
metadata: {"openclaw":{"requires":["subagents","sessions_history"]}}
---

# Agent Summary — 进度摘要系统

参考 Claude Code 的 AgentSummary 机制，用于监控子Agent工作状态。

## 核心机制

### 摘要生成
Claude Code 每30秒对子Agent的对话历史运行一次轻量查询，生成进度摘要：
- 原文要求 Claude 用 3-5 个词描述当前正在做什么
- ✅ "Reading runAgent.ts" — 具体
- ✅ "Fixing null check in validate.ts" — 具体
- ❌ "Investigating the issue" — 太模糊

### 优化策略
- 复用父Agent的上下文，最大化缓存命中率
- 摘要请求使用相同系统提示和工具列表
- 使摘要生成的 token 成本极低

## 使用方式

### 1. 手动检查
```
subagents list → 获取所有Worker状态
对每个活跃Worker:
  sessions_history(sessionKey, limit=2) → 获取最新消息
  → 生成摘要
```

### 2. 在心跳中集成
在 HEARTBEAT.md 中加入 Agent Summary 检查：
```
## Agent Summary Check
- 检查是否有活跃的子Agent
- 如有，生成进度摘要
- 只在有变化时通知用户
```

### 3. Coordinator集成
在协调器模式下，定期检查Worker进度：
```
每30秒:
  1. subagents list → 获取活跃Workers
  2. 对每个Worker获取最新2条消息
  3. 生成3-5词进度摘要
  4. 汇总报告给用户（仅在变化时）
```

## 摘要格式
```
📊 Agent Status:
  ├─ 🟢 researcher: "Searching Rust async docs"
  ├─ 🟢 coder: "Writing unit tests for auth module"
  └─ ⚪ devops: completed ✓
```

## 注意
- 不要频繁轮询，最多每30秒一次
- 只在有变化时通知用户
- 完成/失败的Agent立即报告
- 深夜（23:00-08:00）不打扰用户
