# Changelog

All notable changes to `@hodl-dance/skill` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-05-27

### Added
- Full support for AI agent workflows and 8004 ecosystem integration
- New modern README with Problem/Solution structure and dedicated "AI Agents & 8004 Integration" section
- `CHANGELOG.md` for proper release tracking
- Basic address validation for all commands accepting Ethereum addresses (`get-token`, `get-trades`, `quote`, `buy-token`, `sell-token`)
- `stripMongoFields()` helper to consistently remove internal `_id` and `__v` fields from all public JSON output

### Changed
- **Breaking for output consumers**: `get-token`, `get-trades`, and nested trades now return clean objects without MongoDB internal fields (`_id`, `__v`)
- Improved Windows compatibility: replaced direct `process.exit()` calls with `process.exitCode` pattern to prevent libuv `UV_HANDLE_CLOSING` assertion crashes when output is captured
- Better error messages when invalid addresses are provided (now returns clear `INVALID_ARG` instead of downstream contract errors)
- Updated `get-tokens` to use the new sanitization helper for consistency

### Fixed
- Critical bug: CLI would crash with native assertion on Windows after every successful command when stdout was piped or captured (common in agent environments)
- Inconsistent presence of MongoDB metadata in JSON responses

### Technical
- Added `src/lib/validators.js` for reusable address validation
- Refactored output handling in `src/lib/output.js` and `src/index.js`

---

## [1.2.1] - Previous

- Documentation updates
- Minor fixes for `create-token` command

---

## [1.2.0]

- Added `create-token` command (token deployment + logo upload + optional initial buy)

---

## [1.1.0]

- Initial public release
- Commands: `get-tokens`, `get-token`, `get-trades`, `quote`, `buy-token`, `sell-token`

[1.3.0]: https://github.com/hodldance/agent-skill/compare/v1.2.1...v1.3.0