# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-03-17

### Changed
- 优化描述文案（基于 Claude 改进版本）
- "向量搜索"改为"支持搜索"（更通用）
- 统一中英文术语

---

## [1.0.1] - 2026-03-17

### Added
- 增加降级方案说明：未配置 Ollama 时自动降级为关键词匹配
- 优化 flushMode 配置说明
- 增加注意事项（并发写入、权限等）

---

## [1.0.0] - 2026-03-17

### Added
- 完整的记忆系统框架
- 文件系统存储（Markdown 格式）
- 向量语义搜索（Ollama + nomic-embed-text）
- 关键词搜索（降级方案）
- 自动加载机制
- Memory Flush 机制
- 群组隔离记忆

---

**首发版本**: 团宝 (openclaw)
