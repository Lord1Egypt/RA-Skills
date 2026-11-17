## [1.5.0] - 2026-09-16

### Changed
- **Workspace MCP fallback** — Drive operations fall back gracefully to `google_api.py` (direct Google API client) when the Workspace MCP toolset is absent; same operations, no delete, backend logged in journal.

## [1.4.5] - 2026-04-26

### Changed
- Version alignment: SKILL.md frontmatter, CHANGELOG.md, and GitHub release tag now in sync per spec-ocas-skill-publishing.md. No functional change in this release.

## [1.4.3] - 2026-04-12

### Changed
- Generalized Google Drive MCP reference to platform-agnostic capability description

## [1.4.0] - 2026-04-09

### Added
- Drive digest (`drive_digest.json`) — lightweight holistic Drive summary updated incrementally after each folder scan
- Per-folder statistics (naming patterns, domain detection, sacred flags) feed Drive-wide aggregates
- Analysis uses digest for cross-folder reasoning, scan files for per-file proposals
- Partial digest works with incomplete scans (scan_coverage < 1.0)

## [1.3.0] - 2026-04-09

### Changed
- Replaced monolithic `structural_model.json` with folder-by-folder scan files (`scans/{folder_id}.json`)
- Founding scan now spans multiple sessions with automatic resume via `scan_progress.json`
- Added `--analyze-now` flag for early results before full scan completes
- Phase 1 (tree discovery) writes `folder_index.json` — folder tree only, fast for any Drive size
- Phase 2 (folder scanning) processes one top-level folder at a time, checkpoints after each
- No timeouts or memory issues for 100k+ file Drives

### Removed
- `structural_model.json` (replaced by `scans/` directory + `drive_digest.json`)
- `staging/scan_checkpoint.json` (replaced by `scan_progress.json`)

## [1.2.2] - 2026-04-08

### Fixed
- Replaced skill.json references with SKILL.md frontmatter for agentskills.io compatibility

## [1.2.1] - 2026-04-08

### Fixed
- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Removed hardcoded OpenClaw references for platform portability

## [1.2.0] - 2026-04-08

### Changed
- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with $OCAS_DATA_ROOT/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points

## [1.1.2] - 2026-04-06

### Added
- OKRs section in SKILL.md with formal OKR definitions for skill evaluation
- YAML-formatted skill_okrs with metrics, targets, and evaluation windows

### Fixed
- Renamed "## OKR targets" to "## OKRs" for consistency with spec-ocas-skill-authoring-rules.md

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
- ✓ Version: 1.1.0 → 1.1.1

## [1.3.2] - 2026-03-31

### Added
- Required SKILL.md sections for OCAS specification compliance
- Filesystem field in skill.json

### Changed
- Documentation improvements for better maintainability

# Changelog

## [1.2.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [1.2.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [1.1.0] - 2026-04-02

### Added
- Full signal emission to See references/integration-notes.md for current backend architecture. for Drive artifacts (Thing/DigitalArtifact, Entity/Person, Place, Concept/Event, Concept/Idea)
- All emitted signals carry `user_relevance: "user"` — Drive content is inherently user-owned
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- Filesystem write permission for See references/integration-notes.md for current backend architecture. intake directory
- See references/integration-notes.md for current backend architecture. signal cooperation documented in skill cooperation section

## [1.0.1] - 2026-03-30

### Added
- `## Ontology types` section per authoring rules v2.4.0 (Thing/DigitalArtifact declared)


## [1.0.0] - 2026-03-30

### Added
- Initial release of Bower
- Deep scan (`bower.scan.deep`) with content reading, description generation, and checkpoint/resume
- Light scan (`bower.scan.light`) with drift detection and arrival detection
- Analysis engine (`bower.analyze`) with domain-specific and generic outlier logic
- Simulation mode (`bower.simulate`) for read-only previews
- Proposal lifecycle: generate, review, approve, apply, undo
- Founding run (`--founding` flag) for one-time batch bootstrap with immediate pattern promotion
- Domain support: Taxes, Projects, Home, Finance, Legal, Medical, Archive, Education
- Prescriptive and descriptive mode selection per domain
- Preference profile inference: naming conventions, depth preference, sacred folders, domain detection
- Pattern promotion and auto-approval with demotion on undo/reject
- Feedback learning and proposal suppression
- Confidence recalibration per outlier class
- Permission safety: O(1) folder_index comparison blocks permission-changing moves
- Description auto-writes for empty fields; overwrite proposals for existing descriptions
- Rename proposals (high confidence only, five required conditions)
- Quiet mode for silent apply runs
- Apply cap (25 proposals) and describe_auto_cap (50 auto-writes) per run
- Proposal expiry (14-day default)
- Pre-apply staleness gate per proposal
- Weekly Drive health signal to Vesper intake
- Full audit trail: move_log, undo_log, feedback_log, scan_events, analysis_events
- Background tasks: daily light scan (2am PT), weekly deep scan (Sunday 1am PT)
