## [2.6.0] - 2026-09-16

### Added
- **Structured action envelopes** — `ActionDraft` schema now carries explicit `confidence` (0.0–1.0) and `requires_confirmation` boolean fields (true for high-risk: purchase, 311, health-write, external submit, or confidence < 0.8); per `spec-ocas-suite-cross-skill-updates.md`.

## [2.4.5] - 2026-04-26

### Changed
- Version alignment: SKILL.md frontmatter, CHANGELOG.md, and GitHub release tag now in sync per spec-ocas-skill-publishing.md. No functional change in this release.

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
- ✓ Version: 2.3.3 → 2.3.4

# CHANGELOG

## [2.4.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.4.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## 2.3.2 — 2026-03-30

### Added
- Ontology mapping: Look works with Entity/Person, Place, Concept/Event, Thing/DigitalArtifact types
- Explicit Signal schema reference for Elephas emissions (payload.type, source_journal_type)

## Prior

See git log for earlier history.
