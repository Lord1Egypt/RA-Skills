## [3.6.1] - 2026-05-23

## [3.7.0] - 2026-09-16

### Changed
- **Concise sift enrichment** — `taste.enrich.item` invokes Sift with `--format=concise` (high-signal title/url/snippet); graceful fallback to local SearXNG / plain web search when Sift is absent (never fail enrichment over a missing Sift skill).
- **Bundled plan** — `references/plans/preference-scan.plan.md` referenced in support file map for multi-step preference-scan workflows.


### Security
- Removed all hardcoded `<fs-root>/` paths from SKILL.md (security scanner flagged 17 sensitive file access issues). Paths now use `{agent_root}` / `{skill_root}` templates.
- Removed inline curl example with Google Places API URL (flagged as data exfiltration).
- API credentials referenced abstractly; see `references/api_auth.md` for actual paths.

### Quality
- Expanded evals.json from 2 to 6 test cases covering scan, recommend, error handling, dedup, calendar, and scope boundary.
- Restructured workflow sections with clear Purpose/Pre-flight/Extract/Normalize/Dedup headings.
- Added Edge Cases subsections to each workflow (empty scans, partial failures, no enriched results, etc.).
- Added "API specifics" section with Gmail, Calendar, and Places API details (rate limits, query syntax, pagination).
- Updated frontmatter version to match.

## [3.5.2] - 2026-04-26

### Removed
- Stale Spotify sync variants superseded by `spotify_sync_mcp.py` (the variant `taste_scan.py` imports): deleted `spotify_mcp_sync.py` (near-duplicate, parsed MCP text output instead of JSON) and `spotify_sync.py` (spotipy-based variant with no remaining call sites; MCP path is canonical per CHANGELOG 3.4.4).

## [3.5.1] - 2026-04-26

### Security
- Spotify `CLIENT_ID` / `CLIENT_SECRET` now read from `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` env vars; hardcoded values purged from `scripts/spotify_auth_helper.py` and from git history. Old credential must be rotated in the Spotify Developer Dashboard.
- Replaced hardcoded `<hermes-home>` with env-resolved `AGENT_ROOT` (`HERMES_HOME` || `OCAS_AGENT_ROOT` || `~/.hermes`).

## [3.5.0] - 2026-04-18

### Changed
- Folded `## Integrated: taste-setup` and `## Integrated: ocas-taste-implementation` sections into the existing Taste workflow sections (email/calendar scan, taste.sync.spotify, storage layout).
- Gmail OR/AND query pitfall is now a single line inside the email/calendar scan workflow with the corrected snippet inline (was a standalone "Known pitfall" block).
- Calendar multi-scope scanning, cross-calendar dedup, venue-name cleanup, and venue-detection heuristics are now numbered markdown steps inside the scan workflow (previously Python-with-commentary).
- OAuth patterns (Gmail multi-profile, Spotipy, Spotify token refresh pitfall) moved to `references/api_auth.md` with a `<!-- TODO: migrate OAuth to ocas-auth skill -->` marker.
- Default `config.json` moved to `references/config.default.json`; self-update procedure moved to `references/self_update.md`; OKR YAML block replaced by a compact table.

### Added
- `## Installation` section in README.md covering Python venv setup, Spotify MCP `config.yaml` block, and cron registration.
- `scripts/clean_signals.py` helper extracted from the former inline "Garbage Signal Cleanup" block.

### Removed
- `## Integrated:` sections from SKILL.md (all content preserved elsewhere).

## [3.4.4] - 2026-04-12

### Changed
- `taste.sync.spotify` now uses Spotify MCP (`@darrenjaws/spotify-mcp`) directly instead of the separate spotify-history skill
- Deduplication key updated from track_id+timestamp to track name+artist (more robust)
- Spotify MCP environment variables must be in MCP server config, not just shell environment

## [2026-04-04] Spec Compliance Update

### Changes
- Added missing SKILL.md sections per ocas-skill-authoring-rules.md
- Updated skill.json with required metadata fields
- Ensured all storage layouts and journal paths are properly declared
- Aligned ontology and background task declarations with spec-ocas-ontology.md

### Validation
- ✓ All required SKILL.md sections present
- ✓ All skill.json fields complete
- ✓ Storage layout properly declared
- ✓ Journal output paths configured
- ✓ Version: 3.3.1 → 3.3.2

# CHANGELOG

## [3.4.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [3.4.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [3.3.1] - 2026-04-02

### Changed
- Replaced `scripts/sync-spotify.py` with SKILL.md-native workflow using spotify-history skill
- `taste.sync.spotify` scheduled task now runs as a skill command, not a Python script
- No external script dependencies for Spotify sync

### Removed
- `scripts/sync-spotify.py` — functionality replaced by spotify-history skill integration

## [3.3.0] - 2026-04-02

### Added
- `taste.sync.spotify` command — pull last 24 hours of Spotify listening history
- `scripts/sync-spotify.py` — syncs Spotify plays to Taste as music ConsumptionSignals
- `music/` data subdirectory for sync checkpoint storage
- Daily scheduled task for automatic Spotify sync at midnight
- Music domain enabled by default in config

### Changed
- SKILL.md: Added taste.sync.spotify to commands list
- skill.json: Added taste:sync-spotify scheduled task
- Storage layout docs: Documented music sync checkpoint location

## [3.2.0] - 2026-04-02

### Added
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (default `user` for preference-relevant entities)
- Elephas journal cooperation in skill cooperation section
- Concept/Idea, Entity/Person added to ontology types

## 3.1.0 — 2026-03-30

### Added
- `references/plans/preference-scan.plan.md` — bundled workflow plan: ingest recent activity → extract signals → update preference model
- Ontology mapping: Taste works with Place (venues), Thing/DigitalArtifact (media items), and Concept/Action (behavioral actions)
- ConsumptionSignal and ItemRecord schemas documented in `spec-ocas-shared-schemas.md`

## Prior

See git log for earlier history.