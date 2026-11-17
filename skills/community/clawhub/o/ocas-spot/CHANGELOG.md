## [2.7.0] - 2026-09-16

### Added
- **Vesper intake brief emission** — confirmed appointments emit a confirmation brief to `ocas-vesper`'s intake directory (venue, provider, time, confirmation ref) for the daily briefing.

## [2.3.0] - 2026-04-12

### Added
- Travel Context: on confirmed booking, Spot checks active Voyage itineraries and appends a Travel Context entry when venue location matches a trip destination
- Square edge cases: wait for `market-loading-indicator` to clear before reading disabled state; check `aria-disabled` as fallback; query from host element not document root
- Filesystem write permission for `{agent_root}/commons/data/ocas-voyage/itineraries/` (needed for Travel Context writes)

### Changed
- SevenRooms, Resy, Tock, OpenTable: agent now handles these platforms directly via browser automation and REST API calls; no helper scripts required
- Voyage skill cooperation updated from read-only to read+write

### Removed
- `scripts/resy.py`, `scripts/sevenrooms.py`, `scripts/tock.py` (contained stale openclaw paths; direct agent handling is more reliable)
- `python3` from required binaries and `pip` from dependencies

## [2026-04-05] Yelp discovery layer

### Added
- `spot.discover [type] [location]` — parallel Yelp discovery workflow (API business search + delivery eligibility + page verification, top-3 reviews fetched in parallel). Returns ranked shortlist with decision signals. Flows into `spot.venue.add` → `spot.check` → `spot.book`.
- Yelp storage: `{agent_root}/commons/data/ocas-spot/yelp/` (alias-cache, shortlists, request-log)
- `spot.init` step 4: optional Yelp API key setup with public page fallback
- `yelp_api_key` optional credential in skill.json
- `discovery` and `yelp` tags added

### Changed
- `description` updated to include discovery trigger phrases
- `filesystem.write` extended to include `yelp/` subdirectory

### Validation
- ✓ Version: 2.0.2 → 2.1.0

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
- ✓ Version: 2.0.1 → 2.0.2

# Changelog

## [2.2.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.2.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [2.0.1] - 2026-04-03

### Fixed
- Resy: switch from browser-only to REST API with token auth for auth-gated restaurants (e.g. Copra)
- Resy: add credential-based token flow (RESY_API_KEY, RESY_EMAIL, RESY_PASSWORD env vars)
- Resy: 12-hour token cache in `{agent_root}/commons/data/ocas-spot/resy-token.json` — portable across machines
- Resy: browser automation retained as fallback for unauthenticated venues; warns when credentials not set

### Changed
- `references/platforms/resy.md` — updated status to ⚠️ Working (auth-dependent), documented env vars, token flow, API endpoints
- SKILL.md platform table — Resy row updated to reflect auth requirement
- Version 2.0.0 → 2.0.1

---

## [2.0.0] - 2026-04-04

### Added
- Watchlist monitoring: `spot.watch.add`, `spot.watch.list`, `spot.watch.remove`, `spot.watch.sweep`
- Background cron sweep every 15 minutes via `spot:watch-sweep`; writes InsightProposals to Vesper on new availability
- Restaurant platform support: SevenRooms (✅ Production), Resy (✅ Production), Tock (⚠️ Working)
- OpenTable session persistence workaround: `spot.opentable.login` saves session for subsequent headless checks
- NLP parsing guidance: party size, date, time window extraction from natural language
- `WatchRecord` schema in storage layout
- Dedicated `## Background tasks` section in SKILL.md per OCAS authoring rules v2.6.0
- `opentable-session.json` to `.gitignore`
- Voyage cooperative read documented in Optional Skill Cooperation

### Changed
- Package directory renamed from `spot` to `ocas-spot` (OCAS spec compliance)
- Platform table updated: SevenRooms ✅, Resy ✅, Tock ⚠️, OpenTable ⚠️ (session required)
- `self_update.source` updated to `<agent-handle>/ocas-spot`
- `skill.json` `requires` now lists `npm` and `pip` dependencies explicitly
- `filesystem.write` updated: `ocas-elephas` intake path corrected to `{agent_root}/commons/db/ocas-elephas/intake/`
- `filesystem.read` extended to include `ocas-voyage/itineraries/`
- Version 1.0.0 → 2.0.0

### Removed
- `logs/` directory (debug artifacts — not a valid OCAS support directory)
- `knowledge/` directory (research notes — not a valid OCAS support directory)
- `IMPLEMENTATION_SUMMARY.md` (session research document)
- `README.md` (not in OCAS build template)
- `scripts/__pycache__/` (committed bytecode)
- ~100 research-iteration scripts replaced by 5 clean platform implementations: `acuity.js`, `square.js`, `sevenrooms.py`, `resy.py`, `tock.py`

---

## [1.0.0] - 2026-03-30

### Added
- Initial OCAS skill release: `skill.json`, `SKILL.md`, `references/schemas.md`
- Full system skill structure: responsibility boundary, ontology types, commands, workflow, storage layout, OKRs, initialization
- `references/platforms/` — platform knowledge base (Acuity, Square, OpenTable, new platform guide)
- Commands: `spot.check`, `spot.book`, `spot.list`, `spot.venue.add`, `spot.venue.list`, `spot.platform.probe`, `spot.update`
- Elephas Signal emission for Place and Concept/Event entities
- Vesper InsightProposal emission for upcoming confirmed bookings
- Voyage cooperative read for travel plan association

### Changed
- `knowledge/scheduling/` restructured to `references/platforms/` per OCAS package patterns