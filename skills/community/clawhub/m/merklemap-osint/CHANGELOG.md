# Changelog

## [3.0.0] - 2026-04-05

### Added
- **Risk Scoring** — automatic 0–100 risk score based on scan findings
- **Subdomain Categorization** — auto-classify hosts into mail, api, admin, dev, cdn, auth, internal, docs
- **CA Trust Analysis** — detect unusual CAs, self-signed certs, CA diversity issues
- **Temporal Anomaly Detection** — spot bursts of new subdomains and dormant domain revival
- **Change Detection (Diff Mode)** — compare current scan vs previous report
- **Wildcard Certificate Mapping** — map coverage and find dedicated-cert subdomains
- **Multi-Domain Batch Scanning** — scan multiple domains with comparison table
- **Executive Summary Mode** — non-technical paragraph for management
- **JSON Export** — machine-readable output for SIEMs and automation
- **Auto-Pagination** — deep scans automatically fetch all pages
- Risk score banner in HTML reports
- Executive summary section in HTML reports
- Category breakdown pills in HTML reports
- CA analysis section in HTML reports
- Wildcard coverage map in HTML reports
- Discovery timeline in HTML reports
- Change detection diff view in HTML reports
- `.gitignore` for generated reports and env files
- `CHANGELOG.md`

### Changed
- HTML report template expanded with new sections and improved styling
- Smart workflows updated to incorporate all intelligence features
- Version bumped to 3.0.0

## [2.1.0] - 2026-04-05

### Added
- HTML report generation with dark-themed dashboard layout
- Self-contained HTML with inline CSS, no external dependencies
- Summary cards, severity-ranked findings, data tables with status badges
- Print-ready `@media print` styles
- Light theme option

## [2.0.0] - 2026-04-05

### Added
- Get Certificate endpoint (`/v1/certificates/hash/{sha256}`) — full X.509 deep dive
- Live Tail endpoint (`/v1/live-tail`) — real-time SSE stream
- Typosquatting detection via Levenshtein distance search
- Pagination support for all endpoints
- Smart chained workflows (full recon, typosquat check, cert audit, monitor)
- Comprehensive error handling table

### Changed
- Search endpoint now documents `type=distance` parameter
- List Certificates endpoint now documents all response fields

## [1.0.0] - 2026-04-05

### Added
- Initial release
- Subdomain search via MerkleMap API
- Certificate listing by hostname
- Basic Markdown output formatting
