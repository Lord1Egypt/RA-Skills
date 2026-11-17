# Kimi K3 Code Subagent 架构学习笔记

> 学习来源: github.com/MoonshotAI/kimi-code (MIT协议, TypeScript)
> 核心包: packages/agent-core/src/session/subagent-host.ts, subagent-batch.ts
> 日期: 2026-07-29

---

## 架构全景

```
Session
  SessionSubagentHost
    spawn() / resume() / retry() / runQueued() / startBtw() / cancelAll()
  SubagentBatch<T>
    Normal Phase -> Rate Limit Phase -> Done
  AgentTool (单Agent) / AgentSwarmTool (批量)
```

## 1. SessionSubagentHost 核心调度器

### 核心方法
- spawn(): 创建新子Agent, 含profileName/prompt
- resume(): 恢复已有子Agent, 保留对话历史
- retry(): 重试失败子Agent, 重新启动turn
- runQueued(): 批量执行, 交给SubagentBatch
- startBtw(): 侧通道顺便问, 纯文本无工具
- cancelAll(): 取消所有前台子Agent

### 生命周期
spawn -> configureChild -> runPromptTurn -> waitForChildCompletion -> drainChildBackgroundTasks -> summary检查 -> 返回

### 关键设计
1. Summary min length: 子Agent结果<200字符时自动追加追问
2. Background draining: 子Agent完成前等待所有后台任务结束
3. Suppress terminal notifications: 后台任务完成时不触发新turn
4. Lifecycle hooks: SubagentStart / SubagentStop 钩子
5. Events: spawned / started / completed / failed / suspended

## 2. SubagentBatch 批量调度引擎

### 正常阶段
- 立即启动5个任务
- 之后每700ms启动1个
- 可选并发上限
- 优先级: 重试 > resume > spawn

### 限流阶段
- 触发: 第一个Provider RateLimit错误
- 容量: 初始=已成功启动数, 最小1
- 收缩: 每次限流-1, 最小1, 间隔>=2000ms
- 恢复: 3分钟无限流后容量+1
- 重试间隔: 3s/6s/12s/24s... 指数退避

### 结果状态
completed / failed / aborted + state: started / not_started

## 3. Agent Tool 单子Agent工具
输入: prompt / description / subagent_type / resume / run_in_background
前台模式: 等待完成返回结果
后台模式: 立即返回task_id+agent_id, 后续自动通知

## 4. AgentSwarm 批量子Agent工具
输入: description / subagent_type / prompt_template / items / resume_agent_ids
约束: 至少2个items, 最多128个, 重复prompt检测

## 5. 与现有系统对比

| 维度 | Kimi Code | 我们现有 | 差距 |
|------|-----------|---------|------|
| 子Agent创建 | spawn/resume/retry | sessions_spawn | 缺resume/retry |
| 批量调度 | 两阶段+指数退避 | Swarm调度器 | 限流策略 |
| 生命周期事件 | 6种事件+2种钩子 | AgentLifecycle | 可升级 |
| 超时控制 | 每任务独立, 默认2h | 5分钟硬熔断 | 更灵活 |
| 后台模式 | foreground/background | 仅有foreground | 可加 |
| 侧通道 | startBtw | 无 | 新增 |
| 结果摘要 | 200字符min | 无 | 好用 |
| Agent Profile | 工具/权限配置 | 无 | 新增 |

## 6. 整合方案

### P0 已完成
1. subagent_types.py - 类型定义+4种内置Profile
2. subagent_host.py - 生命周期管理
3. subagent_batch.py - 两阶段批量调度

### P1 待做
4. 集成到Swarm调度器
5. 结果摘要检查(200字符min)
6. 生命周期事件流

### P2 长期
7. Agent Profile配置系统
8. 后台模式
9. 侧通道顺便问模式

## 总结
最值得学习的3个设计:
1. SubagentBatch两阶段调度: 正常阶段快速启动+限流阶段优雅降级
2. 生命周期管理: spawn->resume->retry 三级操作
3. 后台模式+侧通道: 灵活的任务执行模式
