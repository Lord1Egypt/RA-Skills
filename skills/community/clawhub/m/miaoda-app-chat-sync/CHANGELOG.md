# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.1] - 2026-04-30

### Security
- Added security considerations documentation for generated JSON instructions
- Clarified token scope and credential handling in metadata
- Added warnings about downstream AI agent interpretation of rules
- Improved safety documentation in README.md and SKILL.md

### Fixed
- Fixed version mismatch in _meta.json (3.0.0 → 3.2.0)
- Added environment variable declarations to metadata

### Changed
- Updated rules description to emphasize review before applying changes
- Adjusted security claims from "安全可靠" to "安全特性" for accuracy
- Added note to rules that they are suggestions, not absolute commands

## [3.2.0] - 2026-04-30

### Added
- Modular architecture for better maintainability
- `info` command now includes complete file content in JSON output
- Unified `--no-instructions` parameter across all commands
- Consistent terminal output - always shows summary information
- Flexible file output - full formatted or pure JSON format
- `info` command supports `--filter` and `--exclude` parameters

### Removed
- Removed streaming.py module (unused)
- Simplified dependencies and cleaned up dead code (~320 lines)

## [1.0.1] - 2026-04-28

### Fixed
- 修复已知问题，提升系统稳定性

### Changed
- 优化代码同步逻辑
- 改进错误处理机制

## [1.0.0] - 2026-04-27

### Added
- Initial release of `generator`
- **Core functionality**: Convert Git repository code to structured JSON instructions
- **CLI commands**:
  - `sync`: Generate JSON instructions for code synchronization
  - `info`: Get commit information and changed files
- **File filtering**: Support for `--filter` and `--exclude` patterns
- **Batch processing**: Automatic splitting for large projects (>50 files)
- **Structured JSON output**: AI-agent-friendly format with strict execution rules
- **GitHub integration**: Support for public and private repositories
- **Commit-based sync**: Pin to specific commit for reproducibility
- **Comprehensive documentation**: SKILL.md with integration guides and examples
