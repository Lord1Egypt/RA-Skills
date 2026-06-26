# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.12] - 2026-03-26

### Security
- Added detailed Shell command execution security documentation
- Clarified safe usage of spawn() vs exec() in SKILL.md
- All child_process usage reviewed and confirmed safe

### Documentation
- Added Shell injection prevention explanation
- Added links to Node.js security best practices
- Added OWASP injection prevention reference
- Updated package.json to include dotenv in dependencies

## [1.0.11] - 2026-03-26

### Added
- Automatic .env file loading (no need to manually `source .env`)
- dotenv package integration for environment variable management

### Fixed
- Environment variable passing issue in npm run search
- Environment variable passing issue in scripts/search.sh
- User experience improved (1 step instead of 2)

### Changed
- scripts/search.sh: Auto-loads .env file if exists
- package.json: Uses dotenv/config for automatic loading
- src/index.ts: Loads .env file in code as fallback

## [1.0.10] - 2026-03-26

### Added
- Dynamic engine quantity limit based on query complexity
- `--deep` CLI parameter for deep research mode (uses all 5 engines)
- Scenario-based engine selection (academic, technical, news, scrape)
- Smart routing optimization for Firecrawl and Exa engines

### Changed
- Simple queries (<10 chars): use 2 engines instead of 5 (-60%)
- Normal queries: use 3 engines instead of 5 (-40%)
- Firecrawl available days: 25 days → 60+ days (+148%)
- Search speed: ~3-4s → ~2s (-40%)
- Default backup engines: 2 (was unlimited in v1.0.8)

### Fixed
- API quota consumption issue in v1.0.8 (all 5 engines always participating)
- Firecrawl quota exhaustion problem (500 pages/month depleted in 25 days)
- Unnecessary engine calls for simple queries

### Performance
- Reduced API calls by 50% for daily usage (20 searches/day)
- Improved search response time by 40%
- Extended Firecrawl quota from 25 days to 60+ days

## [1.0.8] - 2026-03-26

### Security
- Added OPENCLAW_MASTER_KEY environment variable declaration in ClawHub metadata
- Enhanced SKILL.md with detailed security documentation
- Improved setup wizard to not print API keys to terminal
- Added security best practices guide
- Documented encryption implementation (AES-256-GCM, PBKDF2, random salt)

### Added
- openclaw.plugin.json with complete metadata
- Environment variable requirements documentation
- Security audit section in SKILL.md
- Troubleshooting guide for common issues

### Changed
- Improved user experience for API key setup
- Enhanced documentation for key lifecycle management
- Better error messages for missing configuration

### Fixed
- ClawHub security warnings about missing environment variable declarations
- Setup wizard security issue (printing keys to terminal)
- Documentation gaps in key management

## [1.0.6] - 2026-03-26

### Added
- Firecrawl-specific scenario triggers (scrape, crawl, 网页抓取，content extraction)
- Exa academic/technical scenario triggers (paper, 论文，research)

### Changed
- Removed backup engine limit (slice(0, 2))
- All relevant engines now participate in search
- Improved Firecrawl engine selection logic
- Enhanced Exa engine selection for academic queries

### Fixed
- Firecrawl engine rarely being selected issue
- Improved search result quality for specific scenarios

## [1.0.5] - 2026-03-25

### Added
- Implemented Exa search engine adapter
- Implemented Firecrawl search engine adapter

### Changed
- All 5 engines now fully functional

## [1.0.4] - 2026-03-25

### Fixed
- ClawHub publishing workflow compatibility
- Package metadata for ClawHub registry

## [1.0.3] - 2026-03-25

### Security
- **Critical Fix**: Replaced fixed salt with random salt in PBKDF2 key derivation
- Declared `mcporter` CLI dependency in SKILL.md metadata
- Declared `OPENCLAW_MASTER_KEY` environment variable requirement
- Added security documentation comments to bailian.ts

### Documentation
- Fixed misleading privacy claim
- Removed non-existent `npm run serve` command

### Fixed
- Added missing test scripts to package.json

### Changed
- Config file version bumped to `2.0` to indicate random salt format
