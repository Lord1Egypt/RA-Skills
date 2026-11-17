## [4.2.0] - 2026-09-16

### Changed
- **Token storage discipline** — standardized service credentials at `~/.hermes/{service}_token.json` with freshness validation (expiry + 5min buffer), shape validation (`access_token`/`token_type`/`expires_at` fields), and atomic refresh cleanup before every multiplexed request.

## [4.1.3] - 2026-04-26

### Changed
- Version alignment: SKILL.md frontmatter, CHANGELOG.md, and GitHub release tag now in sync per spec-ocas-skill-publishing.md. No functional change in this release.

## [4.0.3] - 2026-04-06

### Added
- OKRs section in SKILL.md with formal OKR definitions for skill evaluation
- YAML-formatted skill_okrs with metrics (tool_invocation_success_rate, spawn_depth_efficiency, isolation_violation_rate) and evaluation windows

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
- ✓ Version: 4.0.0 → 4.0.1

# Changelog

## [4.1.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [4.1.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [4.0.0] - 2026-04-04

### Added
- README.md: user-facing overview with commands, setup, dependencies, and storage layout
- CHANGELOG.md: version history
- references/journal.md: Action Journal and Research Journal specification per spec-ocas-journal.md v1.3
- skill.json: skill_type, filesystem read/write permissions, self_update configuration

## [3.0.0] - 2026-04-04

### Added
- Initial release: four-phase autonomous workflow (Plan, Fill gaps, Execute, Report)
- Adaptive complexity -- inline search for simple tasks, parallel workers for complex
- Circuit breakers and loop prevention (references/resilience.md)
- Disposable identity cascade: BotEmail, Mail.tm, 1secmail, Guerrilla Mail
- Candidate scoring rubric: relevance, trust, cost, effort axes (references/scoring.md)
- Discovery surfaces: MCP Registry, ClawHub, Skills.sh, GitHub, public APIs (references/surfaces.md)
- Orchestrator/worker checkpoint architecture with recovery paths (references/orchestration.md)
- Commands: multipass.run, multipass.search, multipass.sessions, multipass.replay, multipass.status
