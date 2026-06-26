# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.8.5] - 2026-04-08

### Fixed
- **Bug 2: CLI 参数解析修复**: `bin/memory-palace.js` 正确解析 `--db-path` 参数
- **Bug 5: vector-search ESM __dirname 修复**: `dist/src/background/vector-search.js` 使用 `fileURLToPath(import.meta.url)` 替代 CommonJS `__dirname`，兼容 ES Module 环境
- **Bug 5: Python 模型路径修复**: `scripts/vector-service.py` 改进 `get_model_path()` 默认路径解析逻辑

---

## [1.7.0] - 2026-03-21

### Added
- **P1-1: CLI 参数解析增强**: CLI 现在支持 key=value 格式的参数（如 `id=xxx content=test`），同时保持 JSON 格式兼容
- **P1-2: 批量删除 deleteBatch**: 新增 `deleteBatch(ids, permanent)` 方法，支持批量删除记忆，返回删除结果和失败详情
- **P1-3: storeBatch 原子性优化**: `storeBatch` 向量索引改为 `Promise.all` 并行执行，提升批量写入性能

### Changed
- `storeBatch` 保持串行创建记忆（避免 ID 冲突），向量索引阶段并行执行

---

## [1.6.1] - 2026-03-21

### Fixed
- **P0: ES Module __dirname 兼容性**: `LocalVectorSearchProvider` 构造函数中使用 `__dirname` 在 ES Module 环境下不存在，改为使用 `fileURLToPath(import.meta.url)` 兼容
- **P0: get() 返回值语义优化**: 新增 `getOrThrow()` 方法，区分「ID不存在」与「系统错误」两种场景，原有 `get()` 方法保持向后兼容

---

## [1.4.1] - 2026-03-20

### Changed
- SKILL.md 移除冗余 version 字段

### Fixed
- 修复版本号与发布状态同步

---

## [1.4.0] - 2026-03-20

### Changed
- **LLM 工具降级为规则引擎**: `parse_time` 从 LLM 调用降级为规则引擎实现，提升响应速度并避免 API 依赖
- **精简 LLM 依赖**: 移除以下 LLM 工具（功能已整合或降级为规则引擎）：
  - `extract_experience` - 经验提取
  - `parse_time_llm` - LLM 时间解析
  - `expand_concepts_llm` - 概念扩展
  - `compress` - 记忆压缩
- 保留 `summarize` LLM 智能总结功能

### Technical Details
- `summarize` 仍使用 LLM 增强，提供智能总结服务
- `parse_time` 改用规则引擎，解析常见时间表达式（明天、下周三、上周五等）
- 向量搜索功能保持不变

---

## [1.4.0-beta.1] - 2026-03-20

### Added
- **统一 API 参数风格**: 所有方法支持 `{ param, options? }` 对象风格，同时保持向后兼容
  - `get(id)` → `get({ id })` 
  - `recall(query, options)` → `recall({ query, ...options })`
  - `update(id, content, ...)` → `update({ id, content, ... })`
  - `getRelevantExperiences(context, limit)` → `getRelevantExperiences({ context, limit })`
- **verifyExperience 快捷字段**: 返回值增加 `verified`, `verifiedCount`, `verifiedAt` 快捷字段
- **新增 VerifiedExperienceResult 类型**: 用于验证结果的类型定义
- **新增 GetParams, RecallParams, GetRelevantParams 类型**: 统一对象风格的参数类型
- **CLI 新增命令**:
  - `get_relevant_experiences` - 获取相关经验
  - `experience_stats` - 经验统计
  - `summarize` - 智能总结记忆
  - `parse_time` - 规则时间解析
  - `get` 命令支持对象风格参数

### Changed
- SKILL.md 文档更新以反映新 API 风格
- 简化 CLI 代码，使用更清晰的 API 调用方式

### Fixed
- API 类型定义与实际实现对齐
- **CLI --db-path 参数**: 添加全局 `--db-path` 参数支持，将路径传递给 LocalVectorSearchProvider
- **向量服务权限检查**: 添加 `check_db_path_writable()` 函数，初始化时检查数据库路径可写性
- **SKILL.md 版本号**: 更新为 v1.4.0-beta.1

---

## [1.3.4] - 2026-03-20

### Fixed
- **CLI API 调用错误**: 修复 `MemoryPalaceManager` 构造函数调用方式，使用 `{ workspaceDir: path }` 格式
- **CLI ExperienceManager**: 移除错误的 ExperienceManager 直接实例化，改用 manager 的方法
- **参数映射**: 修复 `top_k` 到 `topK` 的参数映射问题
- **经验分类筛选**: 修复严格相等 `===` 导致 category 筛选失效的问题，改用字符串宽松比较
- **向量搜索降级**: SearchResult 增加 `isFallback` 字段，降级时输出 console.warn
- **Stats 增强**: stats() 方法返回 `vectorSearch` 状态信息
- **向量服务数据库错误处理**: 
  - 添加 `--db-path` 参数支持自定义数据库路径
  - 启动时检查数据库路径可写性
  - 添加明确的权限错误提示
- **SKILL.md 文档**: 更新示例代码与实际 API 对齐

### Changed
- CLI 工具使用 manager 暴露的方法替代直接操作 ExperienceManager

---

## [1.2.1] - 2026-03-19

### Added
- Optimized vector model storage path - now supports dynamic skill directory
- Multi-language README support (EN, ZH, JA, ES)
- Improved model download path resolution

### Changed
- Vector model download path changed to skill directory for better integration
- Enhanced documentation with multi-language support

---

## [1.0.0] - 2026-03-18

### Added
- Initial release of Memory Palace
- Core memory management with CRUD operations
- Persistent file-based storage (Markdown format)
- Semantic search with vector search integration
- Text-based search fallback when vector search unavailable
- Time reasoning engine for temporal expressions (明天, 下周, 本月, etc.)
- Concept expansion for query enhancement
- Tagging system for flexible categorization
- Location-based memory organization
- Importance scoring for memory prioritization
- Soft delete with trash and restore functionality
- Background tasks support (conflict detection, memory compression)
- Knowledge graph builder for memory relationships
- Entity tracking and co-occurrence analysis
- Topic clustering for memory organization
- OpenClaw MemoryIndexManager integration support
- TypeScript type definitions
- Comprehensive test suite

### Technical Details
- No MCP protocol dependency - direct function calls
- Interface isolation - vector search is optional
- Graceful degradation - works without advanced features
- File-based storage - simple, portable, human-readable

---

## Future Plans

- [ ] Cloud sync support
- [ ] Memory encryption
- [ ] Advanced visualization
- [ ] Multi-agent memory sharing
- [ ] Natural language queries

---

🔥 Built with passion by the Chaos Team