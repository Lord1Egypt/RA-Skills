# Changelog

All notable changes to the Knowfun.io Claude Code Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.15] - 2026-03-12

### Fixed
- Added `agentSkill` field to package.json for ClawHub recognition
- Added ClawHub-specific keywords: `agent-skill`, `claude-skill`, `clawhub`
- Improved ClawHub indexing and searchability

### Changed
- Enhanced package.json metadata for better skill discovery

## [1.0.14] - 2026-03-09

### Added
- Added metadata.keywords field with 25 accurate keywords
- Keywords based on actual CLI capabilities (course, poster, game, film)
- Improved ClawHub discoverability

### Changed
- Enhanced description for better clarity
- All keywords now reflect real features only

## [1.0.13] - 2026-03-09

### Security
- Removed check-clawhub.sh and watch-clawhub.sh scripts that triggered security scanners
- Enhanced SECURITY.md with comprehensive security analysis and verification steps
- Added ClawHub security compliance documentation
- Clarified legitimate use cases and architecture for security review

### Changed
- Updated security documentation to explain why automated scanners may flag this code
- Added verification instructions for security auditors
- Improved transparency around bash script usage and API calls

### Documentation
- Added CLAWHUB_VERIFICATION.md for security review process
- Enhanced README with security compliance badges
- Documented all security guarantees and safe coding practices

## [1.0.12] - 2026-03-08

### Changed
- Improved package description for better npm searchability
- Enhanced SEO keywords with KnowFun main site terminology

## [1.0.2] - 2026-03-05

### Fixed
- Updated all documentation to use correct npm package name `knowfun-skills` instead of `knowfun-cli`
- Fixed GitHub repository URLs from placeholder `yourusername` to `MindStarAI`
- Corrected API Base URL in SKILL.md from `https://knowfun.io/openapi/v1` to `https://api.knowfun.io`
- Unified version numbers across all documentation files
- Updated OpenClaw integration documentation with correct repository links
- Fixed Cline integration configuration file links

### Changed
- Updated installation instructions across all platforms (Claude Code, Cursor, Cline, OpenClaw)
- Improved OpenClaw README with npm installation as recommended method

## [1.0.1] - 2026-03-04

### Added
- Initial npm package publication
- CLI binary wrapper for multi-platform support

## [1.0.0] - 2026-03-01

### Added
- Initial release of Knowfun.io Claude Code Skill
- Support for creating tasks (course, poster, game, film)
- Task status checking and monitoring
- Detailed task information retrieval
- Task listing with pagination
- Credit balance checking
- Credit pricing information
- Configuration schema retrieval
- Usage statistics tracking
- Comprehensive API reference documentation
- Usage examples for all features
- Standalone CLI helper script
- Environment configuration support
- Error handling and troubleshooting guides

### Features
- **Task Types**:
  - Course generation with customizable styles and languages
  - Poster generation with multiple usage types and styles
  - Game generation with 11+ game types
  - Film generation with 9+ film styles

- **API Operations**:
  - Create and manage content generation tasks
  - Monitor task progress in real-time
  - Retrieve detailed results including URLs and metadata
  - Check credit balance and pricing
  - View usage history and statistics

- **Developer Tools**:
  - Shell script for command-line usage
  - Comprehensive documentation
  - Multiple usage examples
  - Error handling patterns

### Documentation
- README.md with quick start guide
- SKILL.md with complete skill instructions
- api-reference.md with full API documentation
- examples.md with 20+ usage examples
- .env.example for easy configuration

### Scripts
- knowfun-cli.sh: Standalone CLI tool for API interaction

### Configuration
- Support for environment variables
- Configurable API key management
- Optional custom base URL and timeouts
