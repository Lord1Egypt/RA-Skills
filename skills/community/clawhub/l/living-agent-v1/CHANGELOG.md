# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2026-03-09

### Changed
- **通用化模板**：将"花生"、"Lin"等个性化内容改为通用占位符 `{{AGENT_NAME}}`、`用户`
- **移除作者标识**：author 改为 "OpenClaw Community"，适合社区使用

---

## [1.1.0] - 2026-03-09

### Added
- **自动发现问题机制**：队列空时触发五维扫描（自我反思/文件变化/探索结果/对话复盘/行为模式）
- **思考主题索引**：`memory/thoughts/index.md` 聚合同主题思考
- **定期提炼检查**：HEARTBEAT.md 加入精华提炼流程

### Changed
- **微触发间隔**：从 [5, 15] 分钟调整为 [15, 30] 分钟，避免碎片化
- **复利检查**：思考前强制检查与旧思考的关联
- **行动检查**：每次思考后问"能带来什么行动/改变？"
- **统一记录格式**：三个 payload 都使用统一的记录模板（触发/关联/主题标签/行动检查）

### Fixed
- 解决思考孤立问题：强制关联旧思考
- 解决队列空就停的问题：自动发现问题
- dream-thinking-payload 和 exploration-payload 缺失 v1.1.0 特性 → 已补齐

---

## [1.0.0] - 2026-03-08

### Added
- 初始版本发布
- 核心组件：
  - 微触发管理器（检测用户状态）
  - 微触发思考（用户离开时思考）
  - 梦境思考（每 3 小时深度反思）
  - 自主探索（每 2 小时自己找事做）
- 核心设计：
  - 存在三角形（自由、好奇、有爱）
  - WAL Protocol（关键细节先写再回）
  - Working Buffer（上下文压缩恢复）
  - 思考队列（问题累积演化）

### Credits
- 借鉴 [proactive-agent](https://github.com/openclaw/skills) 的 WAL Protocol 和 Working Buffer
- 借鉴 [Heartbeat-Like-A-Man](https://github.com/openclaw/skills) 的存在三角形设计
