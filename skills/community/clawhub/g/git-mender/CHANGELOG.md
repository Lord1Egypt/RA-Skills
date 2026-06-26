# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-08

### Added
- Interactive PR submission workflow (Phase 7 & 8)
- Auto commit, push, and PR creation with user confirmation
- Auto-fork support for repositories without write access
- PR creation verification and URL feedback

### Changed
- Split original Phase 7 into Phase 7 (Present Changes) and Phase 8 (Submit PR)
- Enhanced error handling for push/PR failures

## [1.0.0] - 2025-04-08

### Added
- Initial release
- 7-phase workflow: Parse URL → Fetch Issue → Locate Repo → Analyze → Fix → Verify → Summary
- GitHub CLI (gh) integration with fetch_content fallback
- Auto-detection of default branch
- Commit message and PR description templates
- Comprehensive error handling
