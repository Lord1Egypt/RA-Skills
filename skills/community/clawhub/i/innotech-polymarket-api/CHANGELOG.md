# Changelog

All notable changes to the polymarket-api skill.

## [2.0.0] - 2026-03-23

### Added
- **CLOB SDK Trading Section** — limit orders, market orders, decimal precision rules
- **5-Minute Market Mechanics** — timing lifecycle, winner determination, resolution timing
- **Data Reliability Guide** — what to trust, what not to trust, with explanations
- **Known Pitfalls** — 7 critical lessons learned from real bot development
- **Winner Verification Timing** — poll Gamma API until outcomePrices resolves to 1.0/0.0
- **Market Rotation** — interval-based vs time-based, with correct implementation
- **WebSocket event reliability matrix** — with clear DO USE / DO NOT USE labels
- **CLOB Auth API** — authentication flow for trading

### Changed
- **SKILL.md** — restructured from tutorial format to reference format
- **API_REFERENCE.md** — added CLOB API, CLOB Auth API, outcomePrices timing
- **WEBSOCKET_GUIDE.md** — rewrote with correct CLOB endpoint, event reliability data
- Removed arbitrage scanner examples (not applicable to 5-min markets)
- Updated version from v1.2.0 to v2.0.0

### Knowledge Sources
All new content derived from 3 weeks of bot development (V6 → V7.20) and 3 years of data analysis.

## [1.2.0] - 2026-03-05

### Fixed
- **CRITICAL**: WebSocket book event structure (bids/asks at top level, not under 'book' key)

### Added
- Real-time liquidity tracking with sizes
- Multi-cryptocurrency monitoring (BTC, ETH, SOL, XRP)
- Clean output display patterns

## [1.1.0] - 2026-03-05

### Added
- Time-based market discovery (5-minute pattern)
- WebSocket real-time data guide
- Order book and liquidity tracking
- clobTokenIds field documentation
- Market rotation examples

## [1.0.0] - 2026-03-03

### Added
- Initial release
- Basic API connectivity
- Market search and discovery
- WebSocket basics
