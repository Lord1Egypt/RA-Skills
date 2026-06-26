# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-04-08

### Improved
- Simplified PR submission flow: merged Phase 7/8 dual confirmation into a single step
- Early push permission detection and automatic fork preparation in Phase 3
- Streamlined fork workflow from 5 steps to direct remote selection
- Extended issue input formats: supports `owner/repo#123`, `#123`, and plain issue numbers
- Optimized repository location logic: removed hardcoded path scanning
- Enhanced default branch detection with GitHub API priority
- Added repository PR template detection and Draft PR support
- Added structured analysis output template in Phase 4

### Added
- Scope assessment section for multi-problem issues and monorepo detection
- Handling for missing test frameworks with static analysis fallback
- Branch conflict detection before creating fix branches
- New error handling scenarios in the error table

### Removed
- Redundant "Model Invocation" section (duplicated Progress Checklist)
- Merged "Security and Privacy", "Trust Statement", and "External Endpoints" into concise "Notes" section

## [1.2.0] - 2026-04-08

### Added
- PR body template now includes a promotional footer linking back to the issue-to-pr skill repository

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
