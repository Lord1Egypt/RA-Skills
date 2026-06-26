# Changelog

All notable changes to the G-Prophet API skill will be documented in this file.

## [1.0.6] - 2026-03-16

### Changed

- Removed noise documentation files (IMPROVEMENTS*.md, FINAL_REPORT.md, RELEASE_NOTES.md, etc.) to reduce context pollution
- Simplified README.md to essential information only
- Added explicit warning to `gprophet_predict` MCP tool description: always use the `name` field from response, never fabricate stock names
- Updated api-docs page example responses to include `name` and `market` fields



### ⚡ New Features

- **Rate Limiting**: Per-key minute-level rate limiting via Redis (fixed window). Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Quota Management**: Daily/monthly quota enforcement with automatic reset. Quota=0 means unlimited
- **Batch Quote**: `POST /market-data/batch-quote` — get quotes for up to 20 symbols in one call (5 pts × count)
- **AI Stock Analysis**: `POST /analysis/stock` — single-stock AI analysis report (58 pts, async)
- **Webhook Callbacks**: Analysis endpoints accept `callback_url` parameter; results are POSTed on completion
- **Account Balance**: `GET /account/balance` — check points balance, quota usage (free)
- **Usage Statistics**: `GET /account/usage` — per-day and per-endpoint call history (free)
- **API Info**: `GET /info` — metadata: supported markets, algorithms, pricing table, auth info (free)
- **Python SDK**: Official `gprophet` Python package with auto-retry, async task polling, typed exceptions
- **MCP Server**: Standalone MCP server exposing all 13 tools for AI agent integration

### 🔧 Improvements

- **HTTP Status Codes**: All errors now return proper HTTP status codes (401/402/403/404/429/500/503) instead of HTTP 200 with `success: false`
- **Unified Guards**: Consolidated scope check + rate limit + quota + user lookup into single dependency
- **Middleware Simplification**: Logging middleware no longer parses response body to guess status codes
- **Rate Limit Headers**: All responses include `X-RateLimit-*` headers for client-side throttling

### 📝 New Error Codes

- `RATE_LIMITED` (429) — Request frequency exceeded per-minute limit
- `QUOTA_EXCEEDED` (429) — Daily or monthly call quota exhausted
- `UNSUPPORTED_MARKET` (400) — Market not supported for this endpoint

### 📖 Documentation

- Updated SKILL.md with all new endpoints, error codes, and MCP tool definitions
- Updated frontend API docs page with new endpoints and error codes
- Added Python SDK README with usage examples
- Added MCP Server README with configuration guide
## [1.0.3] - 2026-03-04

### Fixed

- Added proper SKILL.md and README.md frontmatter with clawdbot metadata
- Declared GPROPHET_API_KEY environment variable requirement in frontmatter
- Resolved ClawHub security scan warning about missing credential declaration

### Changed

- Updated version from 1.0.2 to 1.0.3
- Added metadata.clawdbot section to SKILL.md and README.md frontmatter

## [1.0.2] - 2026-03-04

### Documentation Enhancements

- Added TROUBLESHOOTING.md with comprehensive troubleshooting guide
- Added COST_MANAGEMENT.md with pricing, budget planning, and cost optimization strategies
- Enhanced README with links to all documentation
- Added FAQ section to troubleshooting guide
- Added cost estimation examples for common scenarios

### New Features in Documentation

- Error handling best practices
- Rate limiting and quota management information
- Monthly budget scenarios for different user types
- Cost optimization strategies
- ROI calculation examples
- Billing alert setup instructions

## [1.0.1] - 2026-03-04

### Security Improvements

- Added explicit credential requirements to package metadata
- Added homepage URL to package metadata
- Removed recommendation to store API keys in agent configuration files
- Added comprehensive security guidelines in SECURITY.md
- Enhanced README with security best practices
- Added warnings about API key management and rotation

### Documentation

- Added SECURITY.md with detailed security guidelines
- Added privacy and data handling information
- Added incident response procedures
- Added testing and evaluation guidelines
- Enhanced authentication section in SKILL.md with security recommendations

### Changed

- Updated version from 1.0.0 to 1.0.1
- Improved README structure with clearer security sections
- Recommended environment variables as primary credential storage method

## [1.0.0] - 2026-02-18

### Added

- Initial release
- Stock price prediction (1-30 days)
- Multi-market support (US, CN, HK, Crypto)
- Multiple AI algorithms (G-Prophet2026V1, LSTM, Transformer, etc.)
- Technical analysis (RSI, MACD, Bollinger Bands, KDJ)
- Market sentiment analysis
- Deep multi-agent analysis
- MCP tool definitions for agent integration

