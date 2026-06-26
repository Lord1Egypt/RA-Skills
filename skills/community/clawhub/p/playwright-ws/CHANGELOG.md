# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-05-01

### Fixed
- Security: redact `PLAYWRIGHT_WS` endpoint value from log output in `test-runner.js` to prevent credential/URL leakage in CI logs and agent context
- Security: redact `PLAYWRIGHT_WS` value from confirmation echo in `test.sh`

### Added
- Provenance metadata: added `repository` and `homepage` fields to `package.json` and `source` to `_meta.json`
- Privacy notice in `SKILL.md` warning that the configured WebSocket server can observe all URLs, page contents, and interactions

## [1.0.2] - 2026-03-13

### Fixed
- Standardize on `PLAYWRIGHT_WS` env var across all scripts — `test-runner.js` was inconsistently using `PLAYWRIGHT_SERVER`; `PW_TEST_CONNECT_WS_ENDPOINT` is now set directly to the WebSocket URL
- Fix `README.md` requirements section to reference `PLAYWRIGHT_WS`

## [1.0.1] - 2026-03-13

### Fixed
- Security: replace `execSync` string concatenation with `spawnSync` array args in `test-runner.js`, `package-skill.js`, and `package-for-clawhub.js` to prevent shell injection (RCE)

## [1.0.0] - 2026-03-11

### Fixed
- Security: replace `execSync` string concatenation with `spawnSync` array args in `test-runner.js`, `package-skill.js`, and `package-for-clawhub.js` to prevent shell injection (RCE)

## [1.0.0] - 2026-03-08

### Added
- Initial release with WebSocket server support
- Screenshot generation via remote Playwright server
- PDF export functionality
- Test runner for remote browser execution
- Complete Playwright selector documentation
- API reference documentation
- Jest test suite with 16 tests
- GitHub Actions CI/CD pipeline
- Renovate configuration for automated dependency updates

### Features
- `screenshot.js` - Capture screenshots with options (fullPage, viewport, waitForSelector)
- `pdf-export.js` - Generate PDFs from URLs with customizable format
- `test-runner.js` - Execute Playwright tests on remote server
- WebSocket connection support via `PLAYWRIGHT_WS` environment variable

[Unreleased]: https://github.com/first-it-consulting/playwright-skill/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/first-it-consulting/playwright-skill/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/first-it-consulting/playwright-skill/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/first-it-consulting/playwright-skill/releases/tag/v1.0.0