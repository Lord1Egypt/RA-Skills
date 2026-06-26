# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-02

### Added
- README generation functionality
- Changelog generation with Git Commit parsing
- Semantic version calculation (fix/feat/BREAKING)
- Commit auto-classification (feat/fix/docs/refactor/perf/test/chore)
- Command-line interface for local execution
- Python module import support

### Changed
- Refactored from Coze Skill to pure Python tool
- Removed all platform dependencies
- Simplified project structure

### Removed
- Coze platform specific files
- FastAPI web service (moved to standalone version if needed)

## [1.0.0] - 2026-03-01

### Added
- Initial release
- Basic Changelog generation
- Git Commit parsing support
- Version calculation
