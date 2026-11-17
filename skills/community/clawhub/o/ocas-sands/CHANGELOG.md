## [2.1.4] - 2026-04-12

## [2.3.0] - 2026-09-16

### Changed
- **Activation & fallback declarations** — added `metadata.activation.requires_tools: ["workspace_mcp"]` and `fallback_for_tools: ["google_api_fallback"]` to SKILL.md frontmatter per `spec-ocas-skill-improvements.md`.


### Added
- Briefing time window definitions: morning scope = today, evening scope = tomorrow (timeMin/timeMax)
- OAuth staleness note: re-authenticate on auth error rather than suppressing

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
- ✓ Version: 2.0.0 → 2.0.1

# CHANGELOG

## [2.1.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.1.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [2.0.0] - 2026-04-02

### Changed
- SKILL.md rewritten to comply with OCAS architecture standards (528 → ~280 lines)
- Commands renamed to hierarchical dot-notation: sands.calendar.query, sands.event.create, sands.event.modify, sands.event.delete, sands.event.undo, sands.schedule.free, sands.schedule.conflicts, sands.logistics.travel, sands.briefing.generate
- Cron registration updated to use correct openclaw cron CLI syntax (--cron, --session isolated, --message, --light-context, --tz)
- Background task commands updated to match new hierarchical names
- Section ordering aligned with build template

### Added
- Frontmatter fields: source, install (were missing)
- Run completion, Hard boundaries, Self-update, Support file map sections
- sands.journal command
- requires.credentials in skill.json for GOOGLE_PLACES_API_KEY
- New reference files: calendar_config.md, recurring_events.md, conflict_detection.md

### Removed
- Inline detail sections from SKILL.md moved to references/

## [1.2.0] - 2026-04-02

### Added
- Background tasks: sands:morning-brief, sands:evening-brief, sands:conflict-scan, sands:travel-check, sands:update
- sands.init command for directory/config/cron setup on first run
- sands.update command for self-update from GitHub

### Fixed
- Missing scheduled_tasks in skill.json

## [1.1.1] - 2026-04-02

### Changed
- Fixed missing skill_type and filesystem fields in skill.json

## [1.1.0] - 2026-04-02

### Added
- sands.delete, sands.free, sands.undo commands
- Timezone awareness, recurring event handling, multi-mode travel
- Smart duration defaults, attendee management, morning brief day-at-a-glance

## [1.0.0] - 2026-03-31

### Added
- Initial release: query, create, modify, conflicts, travel, brief, status
- Work calendar busy overlay, Google Places integration, conflict classification
