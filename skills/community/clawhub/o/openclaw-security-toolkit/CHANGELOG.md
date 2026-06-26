# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-11

### Added
- Initial release
- Security audit module with comprehensive checks
- Secret scanner with pattern detection (API keys, tokens, passwords)
- Access control management (devices, users, channels)
- Token management (status, rotation, validation)
- Security report generation (JSON, Markdown, Table formats)
- Auto-fix capabilities for supported issues
- Internationalization support (English, Chinese)
- Deep scan mode for thorough analysis
- Security scoring system

### Security
- Detection for OpenAI API keys (`sk-*`)
- Detection for Feishu app secrets
- Detection for generic API keys and tokens
- Detection for private keys
- Gateway bind address check
- Token strength validation
- Public IP exposure check

## [0.1.0] - 2026-03-10

### Added
- Project initialization
- Basic design documentation