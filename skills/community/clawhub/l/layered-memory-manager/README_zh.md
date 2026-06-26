# 分层记忆管理器 (Layered Memory Manager)

一种专为持久化 AI Agent 设计的专业多层级记忆管理系统。它通过自动晋升（Promotion）和降级（Demotion）逻辑，实现缓存一致性架构。

## 安全与数据完整性 (Security & Data Integrity)

- **关于 `grep` 依赖**: 本技能建议系统预装 `grep`。它仅用于在“Secondary: Layer Awareness”阶段对 `memory/*.md` 文件进行只读扫描。这比让 AI 读取成百上千个小文件更安全、更快速、更节省 Token。
- **关于“数据清理”逻辑**: 
  - **晋升清理**: 当条目从 L2 晋升至 L1 时，我们会从 `accessLog` 中移除该条目，因为 L1 条目将通过 `L1accessLog` 进行独立的高频追踪，避免重复计次。
  - **自动归档**: 30 天无活动条目会被**移动**至 `memory/archive/` 而非物理删除。这是为了确保 Agent 的核心上下文始终保持精简，防止无关的历史噪音干扰当前决策。
- **数据透明**: 所有操作均会在 `hygiene.json` 中留痕，用户可以随时通过 `[[restore]]` 指令撤销归档。

## 使用方法

在消息中嵌入以下标签可手动触发记忆操作：

- `[[pin:<layer>:<slug>]]`: 永久保留某条目在 L1。
- `[[promote:<layer>:<slug>]]`: 强制将 L2 条目晋升至 L1。
- `[[forget:<layer>:<slug>]]`: 立即将某 L1 条目降级。
- `[[restore:<layer>:<slug>]]`: 从归档中恢复条目至活动存储。
- `[[memory_health]]`: 获取记忆系统状态快照。

## 设计哲学

该技能遵循“分层智能”原则——将高频操作事实 (L1) 与深层历史背景 (L2) 分离，在保持高效性能的同时，最大限度降低 Token 消耗。
