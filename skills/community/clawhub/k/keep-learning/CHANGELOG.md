# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-03-23

### Fixed
- First-time user interaction now requires explicit knowledge base path confirmation before learning
- Incremental learning now detects both committed and uncommitted changes (using `git diff` + `git status`)

### Added
- Skills CLI installation method: `npx skills add nileader/keep-learning`
- Support for local file modifications even when remote has no updates

## [0.0.1] - 2026-03-22

### Added
- Initial release
- Support for Markdown and code files
- Three-layer knowledge architecture (L1 Core Memory, L2 Index, L3 Source Files)
- Git integration with auto-pull before learning
- Incremental learning based on git diff
- Learning report generation
- Chinese and English trigger words support

### Not Included
- PDF, Word, Excel, PowerPoint support (planned for future versions)
- Audio/video file support
- Scheduled automatic learning
