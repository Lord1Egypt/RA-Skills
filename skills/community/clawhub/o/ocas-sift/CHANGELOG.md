# Changelog

All notable changes to ocas-sift are recorded in this file.

## [2.10.0] — 2026-09-16

### Added
- **Local SearXNG fallback cascade** — when a primary web-search API hits a rate limit / 429 (Brave, N2 MCP outage, etc.), escalate to the local SearXNG instance (`http://localhost:8888/search?q=...&format=json&limit=10`) before attempting paid/CSAPI tiers.

- **Concise/detailed output format** — `scripts/csapi_quota.py` and `scripts/wayback_fallback.py` support `--format=concise` (default, ~60–80% token savings, high-signal fields only or `--format=detailed` (full envelope/UUIDs/fields for chaining）。 Script failure paths return JSON envelopes with human-actionable `actionable_guidance`.
;- **Declarative eval suite** — `references/evals/eval.yaml` with deterministic + LLM-rubric tasks (fact-extraction precision, SearXNG fallback cascade, concise output format) per `spec-ocas-skill-improvements.md`.
- **Extraction tooling** — `get-md` documented as the default HTML-to-Markdown extraction engine (`sift.fetch` → Scrapling → Jina Reader → Wayback fallback → `get-md`)。

## [2.9.4] — 2026-08-27

### Added
- **DonSeTch integration** — `donsetch fetch` added as tier-3 anti-bot fallback (v3.2.3, AGPL, `/usr/local/bin/donsetch`). Real Chrome TLS, solve-and-bounce, headless escalation for CF/Akamai/DataDome/Imperva bot-walled pages.
- New reference: `references/donsetch-integration.md` — tier placement, exit codes (0/1/2/3), commands, caveats.
- New reference: `references/vps-search-cheat-sheet.md` — quick SearXNG + CSAPI + donsetch commands for VPS/cloud.
- New reference: `references/searxng-diagnostics.md` — engine health check + N2 MCP notes.
- CHANGELOG.md (this file).

### Changed
- Anti-bot escalation chain (pitfalls.md): added `donsetch fetch` as tier 3 between `sift.fetch` and `sift.webwright`. Renumbered webwright to tier 4. Clarified agent owns escalation (not auto-fallback).
- Commands table: added `donsetch fetch` entry with inline exit-code mapping.
- Support file map: added `donsetch-integration.md`, `fetch-behavior.md`, `vps-search-cheat-sheet.md`, `searxng-diagnostics.md`.
- Moved "Quick VPS Search Cheat Sheet" from SKILL.md to `references/vps-search-cheat-sheet.md` (15 lines removed).
- Moved N2 MCP engine-diagnostic bash block from SKILL.md to `references/searxng-diagnostics.md` (8 lines removed).
- Trimmed `user_relevance` repetition in ontology section (5 lines removed).
- SKILL.md: 283 → 260 lines. Code ratio: 8.8% → ~5%.

### Verified
- All 4 scripts (`csapi_quota.py`, `update.sh`, `wayback_fallback.py`, `webwright_runner.py`) have `--help` exiting 0.

## [2.9.3] — 2026-08-25

### Fixed
- Fail webwright runs that explored nothing; stop defaulting to a CAPTCHA'd URL.
- Fix webwright_runner crashing on every run + reporting success on failure.
- Reject unknown flags in `update.sh` (exit non-zero).

### Changed
- Sanitize: derive host paths instead of hardcoding them.
- Stop overstating search coverage; unpin the journal example.

## [2.9.2] — 2026-07-21

### Security
- Apply GitHub Deploy Security Protocol: generalize PII + system-specific paths.
- Security: env-resolve operator emails + system paths in code.

### Added
- Add recovery paths; mark deprecated ones.

## [2.9.1] — 2026-07-19

### Fixed
- 10khr: fix D1/D9 defects (category frontmatter, --help guards).

## [2.9.0] — 2026-07-15

### Added
- indigo-seam v3 banner support.
- Templated README structure.
