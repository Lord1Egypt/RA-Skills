# Changelog

All notable changes to the layered-memory skill will be documented in this file.

## [1.2.0] - 2026-03-13

### Added
- **v2 generator**: incremental + concurrent processing
- `lib/config-loader.js` - 配置文件系统，支持 CLI 覆盖和环境变量
- 新增 CLI options: `--force`, `--concurrent`, `--config`, `--dry-run`, `--verbose`
- `estimateTokens()` 函数提供更准确的 Token 估算
- 性能统计：生成耗时、节省 tokens、跳过文件数
- Dry-run 模式预览而不写入
- 增量检查：跳过未修改的文件
- 并发生成：默认 4 并发，可配置

### Improved
- `generate-layers-simple.js` 完全重写为 v2 版本
- `index.js` generate() 和 autoMaintain() 支持新参数
- 配置文件更完善（maxConcurrent, dryRun, verbose 等）
- 错误处理增强（单个文件失败不影响整体）
- 进度显示优化（百分比 + ETA 预留）
- Token 节省统计更精确

### Fixed
- v1.0.0 缺失 `test.js` 的问题
- handler.js 权限已修复
- 所有测试通过率 100%

### Docs
- README 更新：新增 v2 用法、配置说明
- `UPGRADE_PLAN.md` - 详细的三阶段升级路线图
- 新增 `config.example.json` 作为配置模板

---

## [1.1.0] - 2026-03-13

### Added
- `test.js` - 完整的测试套件，验证核心功能
- `config.example.json` - 配置示例
- `benchmark.js` - Token 节省效果性能测试脚本
- `CONTRIBUTING.md` - 贡献指南
- 更详细的 FAQ 章节到 README

### Improved
- package.json 测试脚本完善
- Hooks 错误处理增强（预留配置接口）
- 文档完整性提升

### Fixed
- 修复 v1.0.0 缺失 test.js 的问题
- 确保所有必需文件在 publish 时包含

---

## [1.0.0] - 2026-03-13

### Added
- 初始版本发布
- L0/L1/L2 三层分层记忆管理
- 自动生成分层文件
- 智能按需加载
- OpenClaw hooks 集成
- 完整的用户文档（README, INTEGRATION, AUTO-*）

---
EOF