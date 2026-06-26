# Changelog

## [1.0.0] - 2026-03-06

### Added
- Initial release of Meme Risk Radar skill
- Multi-chain support (Base, BSC, Ethereum, Solana)
- Bilingual output (Chinese and English)
- Token scanning with risk assessment
- Token audit integration
- Proxy support for network requests
- SkillPay billing hooks (optional)
- Health check command
- Global `meme-risk` command

### Fixed
- API response structure compatibility (data vs tokens field)
- Proxy configuration for all network requests

### Changed
- N/A

### Security
- No hardcoded secrets
- Environment-based configuration
- Read-only by default (no trading keys)
