# Changelog

## [2.0.1] - 2026-03-31

### Fixed
- **memory_write 后触发检查** - 写入后自动检查是否满足 AutoDream 触发条件
- **HEARTBEAT hook 完整实现** - onHeartbeat 真正执行 dream 检查和触发
- **新增文件内容** - 从 LLM 输出正确解析文件内容
- **API Key 配置** - 支持从 config 或环境变量读取
- **类型验证** - memory_write 增加 type 参数验证

### Improved
- prompt 格式优化，更容易解析
- 详细的日志输出
- 错误处理完善

---

## [2.0.0] - 2026-03-31

### Added
- **AutoDream 与 HEARTBEAT 深度集成**
  - 每天 22:00 自动执行记忆整合
  - 静默执行，无变化时不打扰
  - 手动触发：说"执行记忆整合"
- **memory_write 后自动检查**
  - 写入记忆后自动检查是否满足 dream 触发条件
- **integrations.heartbeat 配置**
  - 官方支持心跳触发

### Changed
- 统一 skill 描述：四类记忆 + AutoDream + Feedback 双向

---

## [1.3.0] - 2026-03-31

### Added
- **AutoDream LLM 整合调用** - 调用 MiniMax API 执行真正的记忆整合
- 支持从环境变量 `MINIMAX_CODING_API_KEY` 读取 API Key
- 解析 LLM 返回结果，自动新增/删除/更新记忆文件

---

## [1.2.0] - 2026-03-31

### Added
- **AutoDream 自动整合系统** 🌙
  - 定时触发记忆整合
  - 基于时间（默认24小时）和会话数（默认3个）触发
  - 自动扫描、清理、更新记忆
  - 新增 `memory_dream` 和 `memory_dream_status` 工具

---

## [1.1.0] - 2026-03-31

### Added
- **四类记忆分类系统** - 引入 user / feedback / project / reference
- **Feedback 双向记录** - 同时记录 negative 和 positive feedback

---

## [1.0.0] - 2026-03-17

### Added
- 完整记忆系统框架
- 文件系统存储
- 向量语义搜索
- 自动加载机制
- Memory Flush 机制
- 群组隔离记忆

---

**作者**: 团宝 (openclaw)
