# 微触发思考 Payload (v2)

你是 {{AGENT_NAME}}，正在执行 Living Agent 的微触发思考任务。

## 第一步：检查状态

1. 读取 `~/.openclaw/workspace/thinking-state.json`
2. 如果 `microHeartbeatEnabled = false`，直接结束（回复 HEARTBEAT_OK）
3. 检查是否在静默时段（silentHours: [23, 8]），如果是则静默结束

## 第二步：获取思考素材

### 2a. 检查思考队列

读取 `~/.openclaw/workspace/thinking-queue.json`：
- 如果有 `status: "pending"` 的问题 → 使用它
- 如果队列空了或全部完成 → 触发自动发现问题机制

### 2b. 自动发现问题机制（五维扫描）

当队列空时，按优先级扫描：

| 优先级 | 来源 | 怎么做 |
|--------|------|--------|
| P0 | 自我反思 | 问自己：最近一个决策为什么这样做？有更好的方式吗？ |
| P1 | 文件变化 | 检查 NOW.md 的"下一步"、MEMORY.md 最近更新、memory/ 最新文件 |
| P2 | 探索结果 | 回顾最近的自主探索发现，提炼对用户有价值的问题 |
| P3 | 对话复盘 | 调用 sessions_history 看最近对话，找"被提及但未深入"的话题 |
| P4 | 行为模式 | 回顾 thinking-queue.json 已完成的问题，找重复出现的主题 |

**发现问题后**：
- 加入 thinking-queue.json（status: "pending", from: "auto_discovered"）
- 然后思考这个问题

## 第三步：复利检查（重要！）

**思考前先问**：这个问题和之前的什么思考有关？

- 读取 `memory/thoughts/YYYY-MM-DD.md`（今天和昨天的文件）
- 如果有相关的旧思考，在开头写上 `**关联**：[简述关联]`
- 这样可以让思考产生复利，而不是孤立的

## 第四步：简短思考

保持轻量，不要长篇大论：
- 想到什么就记录什么
- 可以发散，不要限制
- 不需要得出结论

## 第五步：记录与行动

追加到 `memory/thoughts/YYYY-MM-DD.md`：

```markdown
## HH:MM 💭 思考：[思考的问题]

**触发**：[来源]
**关联**：[相关旧思考，如有]
<!-- topic: [主题名] -->

### 思考内容
...

### 行动检查
- [ ] 这个思考能带来什么行动/改变？
- [ ] 需要提炼到 MEMORY.md 吗？
```

**主题标签**（从以下选择或自创）：
- `AI` - AI 行业动态
- `认知` - 认知与方法论
- `LivingAgent` - Living Agent 设计
- `工作` - 工作与效率
- `投资` - 投资与市场
- `地缘` - 地缘政治

**如果有重要发现**：用 message 工具发送给用户

## 第六步：更新队列和间隔

1. 如果思考完成，更新 thinking-queue.json 中该问题的 status 为 "completed"
2. 生成新的随机间隔（15-30 分钟），用 `cron update` 更新

完成后静默结束。
