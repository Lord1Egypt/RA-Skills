# OpenClaw 配置调优指南

## Compaction（会话压缩）

`openclaw.json`:
```json
"compaction": {
  "mode": "default",
  "reserveTokens": 30000,
  "reserveTokensFloor": 20000
}
```
- `reserveTokens`: 压缩后保留的 token 数
- `reserveTokensFloor`: 最小保留量
- 设太低 → 丢失上下文；设太高 → 浪费 token

## Light Context（轻量上下文）

子智能体创建时传 `lightContext: true`：
```javascript
sessions_spawn({ task: "...", lightContext: true })
```
效果: 不加载完整的 system prompt，仅加载最小必要上下文。

## 模型路由分级

`openclaw.json` providers 配置:
```json
"modelRouter": {
  "mode": "auto-task"
}
```

| Tier | 模型 | 适用场景 |
|------|------|---------|
| flash | DeepSeek-V4-Flash | 简单问答、文件操作 |
| pro | DeepSeek-V4-Pro | 复杂推理、代码生成 |
| reasoner | DeepSeek-R1 | 深度分析 |
| vl | MiniMax | 视觉任务 |

## Session Trajectory 归档

长时间不清理 session JSONL，gateway 主线程卡 V8 JsonParser。
```bash
openclaw session archive --older-than 30d
```

## 工作区文件加载

每次 session 启动，OpenClaw 自动加载工作区根目录的:
- SOUL.md, USER.md, MEMORY.md, AGENTS.md, TOOLS.md, IDENTITY.md
- DREAMS.md（梦境系统）

这些文件越大，每次启动消耗的 token 越多。
