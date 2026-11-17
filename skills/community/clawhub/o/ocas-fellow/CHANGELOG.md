## [2.6.5] - 2026-04-26

## [2.7.0] - 2026-09-16

### Changed
- **Skillgrade evaluation engine** — Fellow natively executes declarative `eval.yaml` suites in isolated `ocas-inception` containers, returning `CycleResult` with trial pass rates, token metrics, and per-grader breakdowns to Mentor (feeding the ≥0.85 / N≥5, N≥15 promotion thresholds).


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
- ✓ Version: 2.5.0 → 2.5.1

# Changelog

## [2.6.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.6.0] - 2026-04-08

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
- `user_relevance` tagging on journal observations (default `agent_only` for experiment entities, `user` for user-preference experiments)
- Elephas journal cooperation in skill cooperation section

## 2.3.2

- Add skill_type field to skill.json for spec compliance
- Complete required SKILL.md sections per ocas-skill-authoring-rules.md

