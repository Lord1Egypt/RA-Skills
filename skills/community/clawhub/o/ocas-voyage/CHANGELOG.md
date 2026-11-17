## [2.7.5] - 2026-04-12

## [3.0.0] - 2026-09-16

### Added
- **Vesper intake brief delivery** — confirmed travel schedule briefs delivered directly to `ocas-vesper`'s intake directory (`{agent_root}/commons/data/ocas-vesper/intake/`); documented in `references/vesper-intake-delivery.md`.
- **Bundled plan** — `references/plans/trip-planning.plan.md` (destination research → itinerary → accommodation hueco); added to support file map.


### Changed
- Replaced `agent-browser` binary requirement with `web-browsing` capability declaration for platform portability
- Google Hotels setup clarified: available automatically when web browsing capability is present

## [2026-04-05] Parallel lodging stack + GoPlaces cooperation

### Added
- Parallel lodging search: Expedia web + Marriott Strider MCP + Marriott AI/FlyAI + Google Hotels all fire simultaneously during `voyage.recommend.lodging`
- `voyage.init` steps 7–10: Marriott Strider MCP installation and Bonvoy OAuth setup, Google Hotels agent-browser check, FLYAI_API_KEY optional setup, GoPlaces availability check
- GoPlaces optional cooperation: location geocoding, distance checks, disambiguation (when `ocas-goplaces` is installed)
- Sift documented as delegation target for all open web research
- `references/lodging-sources.md` — per-source patterns and failure modes
- `references/total-cost.md` — cost breakdown methodology
- `references/booking-gates.md` — pre-booking checklist
- `itineraries/` subdirectory added to storage layout

### Changed
- `voyage.recommend.lodging` description updated to reflect parallel search
- Optional skill cooperation section expanded with GoPlaces and Sift delegation detail
- `filesystem.read` extended to include Taste and Weave data directories
- `filesystem.write` extended to include `itineraries/`

### Validation
- ✓ Version: 2.5.1 → 2.6.0

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
- ✓ Version: 2.5.0 → 2.5.1

# CHANGELOG

## [2.7.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.7.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [2.5.0] - 2026-04-02

### Added
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (default `user` for travel-related entities)
- Entity/Person (travel companions) added to ontology types
- Elephas journal cooperation in skill cooperation section

## 2.4.0 — 2026-03-30

### Added
- `references/plans/trip-planning.plan.md` — bundled workflow plan: destination research → itinerary → accommodation
- Ontology mapping: Voyage works with Place (venues/airports/hotels), Concept/Event (trips), and Concept/Action (bookings)

## Prior

See git log for earlier history.
