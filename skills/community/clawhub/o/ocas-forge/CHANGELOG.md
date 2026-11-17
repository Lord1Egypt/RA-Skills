## [2.7.1] - 2026-04-26

## [3.8.0] - 2026-09-16

### Added
- **Pre-build quality linters** — frontmatter verification, incident-log shape detection, reference-sprawl check (max 60 files), and config-vs-env separation, embedded in the Validate step; a failing linter blocks promotion to production.


### Changed
- Version alignment: SKILL.md frontmatter, CHANGELOG.md, and GitHub release tag now in sync per spec-ocas-skill-publishing.md. No functional change in this release.

## [2.7.0] - 2026-04-18

### Changed
- Refactor: folded builder-domain helper skills into Forge's existing section structure instead of appending `## Integrated:` wrappers.
- SKILL.md shrunk from 833 → 343 lines (well under the 300-line system-skill ceiling + reference-depth allowance).

### Added
- `forge.consolidate`, `forge.sync`, and `forge.verify-update` commands (folded from helper skills `skill-consolidation`, `sync-local-skills-to-repo`, and `skill-update-verification`).
- `references/builder_workflows.md` — full command sequences and pitfalls for the three new sub-workflows.

### Removed (moved, not deleted)
- `running-ocas-skills` content (MCP toolset traps, delegate patterns, cron inheritance) → `deferred/running-ocas-skills.md`. This is runtime-harness guidance, out-of-scope for the skill builder.
- OAuth/MCP/Google setup content (deduplicated across three helper skills) → `deferred/mcp-oauth-setup.md`. Belongs in the forthcoming `ocas-auth` private repo.
- `ocas-implementation` and `ocas-skill-initialization` — split between the two `deferred/` files by concern (runtime vs. auth); architecture-compliance bullets dropped as redundant with `references/authoring_rules.md`.

### Notes
- All `## Integrated: <skill-name>` wrapper headers removed.
- No content was deleted outright; out-of-scope material is preserved in `deferred/` pending proper homes.

## [2.6.11] - 2026-04-16

### Changed
- Synced reference documentation with ocas-architecture updates (architecture coherence sync 2026-04-16)
- Updated authoring_rules.md: v2.7.2 → v2.8.0 (added ocas-relay as active skill, updated responsibility boundaries)
- Updated ontology.md: v2.0.1 → v2.1.0 (added ocas-relay to entity extraction and signal emission tables)
- All references now reflect 2-skill active ecosystem (ocas-forge, ocas-relay)

## [2.6.10] - 2026-04-15

### Changed
- Synced reference documentation with ocas-architecture updates (architecture coherence sync 2026-04-15)
- Updated authoring_rules.md: v2.7.1 → v2.7.2 (clarified README.md and CHANGELOG.md requirements)
- Updated ontology.md, interfaces.md, schemas.md, workflow_plans.md, storage_conventions.md to latest spec versions
- All references now synchronized with architecture baseline

## [2.6.9] - 2026-04-13

### Changed
- Synced reference documentation with ocas-architecture updates
- Updated authoring_rules.md: v2.7.1 → v2.7.2 (clarified README.md and CHANGELOG.md requirements)
- References now include complete spec requirements for skill package structure

## [2.6.8] - 2026-04-12

### Fixed
- Added `{agent_root}/skills/` to filesystem write paths (was missing, caused write failures when building skill packages)

## [2.6.7] - 2026-04-12

### Changed
- Synced reference documentation with 2026-04-12 architecture coherence audit
- Updated authoring_rules.md: v2.7.0 → v2.7.1 (reflects verified 1-skill active ecosystem)
- Updated ontology.md: v2.0.0 → v2.0.1 (ocas-triage moved to archived reference)
- References now accurately document only active OCAS skill (ocas-forge)
- Clarified that ocas-triage has no GitHub repository instantiation

## [2.6.6] - 2026-04-11

### Changed
- Synced reference documentation with 2026-04-11 architecture coherence audit
- Updated authoring_rules.md: v2.6.4 → v2.7.0 (reflects current 2-skill active ecosystem)
- Updated ontology.md: v1.5.4 → v2.0.0 (major version update for scope change)
- References now accurately document only active OCAS skills (forge, triage)
- Marked 22 previously-documented skills as archived/historical reference

## [2.6.5] - 2026-04-10

### Changed
- Synced all reference documentation with ocas-architecture spec updates
- Updated authoring_rules.md, ontology.md, interfaces.md, journal.md, schemas.md, storage_conventions.md, workflow_plans.md
- Ensures forge always reflects latest architecture specifications

## [2.6.4] - 2026-04-10

### Added
- skill.json configuration file for OCAS architecture coherence (architecture audit 2026-04-10)

## [2.6.1] - 2026-04-08

### Changed
- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory

## [2.6.0] - 2026-04-08

### Changed
- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent

## [2.5.5] - 2026-04-07

### Changed
- Synced authoring_rules.md and ontology.md from ocas-architecture after coherence audit

## [2.5.4] - 2026-04-07

### Fixed
- Patch version update after architecture coherence audit

### Changed
- Synced all reference files with updated ocas-architecture specs:
  - authoring_rules.md: v2.6.2
  - ontology.md: v1.5.2
  - interfaces.md: v1.5
  - storage_conventions.md: latest
  - journal.md: latest
  - schemas.md: latest
- All changes reflect completion of Ontology Types audit for 24 OCAS skills
- Forge now references finalized Skill Entity Extraction and Signal Emission tables

## [2.5.3] - 2026-04-05

### Changed
- Synced all reference files with updated ocas-architecture specs:
  - authoring_rules.md: v2.6.2
  - ontology.md: v1.5.2
  - interfaces.md: v1.5
  - storage_conventions.md: latest
  - journal.md: latest
  - schemas.md: latest
- All changes reflect completion of Ontology Types audit for 24 OCAS skills
- Forge now references finalized Skill Entity Extraction and Signal Emission tables
