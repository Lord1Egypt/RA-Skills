# Changelog

## Unreleased

## 0.3.2 - 2026-06-23

### Changed

- cleaned up stale `project_facts` single-file references in `adapter-map.md`, generic-host `README.md`, and `bootstrap.md` so they match the `directory` mapping introduced in 0.3.1


## 0.3.1 - 2026-06-23

### Changed

- generic-host example manifest now maps `project_facts` as `directory` (`docs/projects`) instead of a single global file, because `project_facts` is the only target class that is inherently multi-project
- `references/adapter-manifest.md` now documents that `project_facts` is special: it must not be pinned to a single workspace-root file, and multi-project hosts should use `directory` or `pattern`

### Removed

- `examples/generic-host/docs/project-facts.md` (replaced by `docs/projects/README.md` explaining the per-project layout)

## 0.3.0 - 2026-06-23

### Added

- `references/compiled-surfaces.md` as the canonical inventory of official OpenClaw runtime / compiled surfaces that are NOT memory target classes
- governance rules for imported content (Imported Insights / cross-platform imports): stage through `learning_candidates`, do not jump to canonical truth
- governance rules for entity memory: capture entity facts into `long_term_memory` / `project_facts` / `learning_candidates`, never directly into a `people/` surface or Person Card
- a scope / privacy boundary that complements Active Memory Filters (`allowedChatIds` / `deniedChatIds`): record scope at capture time so compiled surfaces cannot widen it
- a Multi-Agent Writer Rule covering coordinated agents on Workboard (2026.6.1+), extending the existing skill-level Multi-Writer Rule to agent-level
- Skill Workshop (2026.6.1+) versioning guidance: a skill's `Memory Contract` should version and roll back with the skill

### Changed

- README and SKILL positioning now align with the OpenClaw 2026.6.x memory stack instead of stopping at 4.5 / April 2026
- alignment sections now cover People Wiki (2026.4.29), Memory Wiki Claim/Evidence, Memory Palace, Imported Insights, and Provenance Views, not only Dreaming / Active Memory / Memory Wiki
- `read-order.md` now lists Memory Palace, Imported Insights, Obsidian Vault outputs, Person Cards, and Relationship Graphs as non-default-startup surfaces, and cites official stale-REM filtering and partial-recall-on-timeout as validation of the existing boundary
- `exclusions.md` now covers external imports and scoped-memory capture
- `dreaming-integration.md` now points to the broader compiled-surfaces boundary and notes the Active Memory Filters privacy interaction
- `host-profiles.md` OpenClaw profile now references People Wiki, Active Memory Filters, Imported Insights / Memory Palace, and Workboard multi-agent behavior
- `skill-integration.md` now forbids treating compiled surfaces as capture layers and adds Skill Workshop versioning rules

### Notes

- the 9 standard target classes are unchanged; no new target class was introduced, to avoid competing with official compiled surfaces
- this is a boundary expansion release, not a contract break

## 0.2.10 - 2026-05-28

### Changed

- README now explains how `memory-governor` should coexist with Active Memory and Memory Wiki in newer OpenClaw builds
- read-order guidance now distinguishes governance-time minimal reads from runtime recall handled by Active Memory
- installation guidance now calls out Memory Wiki as a compiled knowledge surface rather than a new target class
- OpenClaw integration notes now emphasize compact recovery state for session pruning / automatic memory flush environments
- OpenClaw profile validation now checks the `learning_candidates` adapter or fallback so explicit corrections do not bypass review
- candidate review tests now use a fixed clock to avoid date-driven failures

## 0.2.9 - 2026-04-07

### Added

- `references/dreaming-integration.md` to define how `memory-governor` should coexist with OpenClaw Dreaming

### Changed

- README positioning now explains that `memory-governor` complements Dreaming instead of replacing it
- promotion rules now separate Dreaming-preferred `daily_memory -> long_term_memory` from manual-only hardening paths
- read-order guidance now explicitly excludes `DREAMS.md` from normal startup and recovery reads
- adapter, host-profile, installation, and skill-integration docs now define `DREAMS.md` / `memory/.dreams/` as engine-owned artifacts and keep explicit correction staging out of Dreaming

## 0.2.8 - 2026-04-05

### Added

- `learning_candidates` as a low-commitment target class for corrections and emerging lessons
- `references/correction-pipeline.md` describing the staged correction flow
- fallback template for candidate-layer capture
- checker, validator, and generic host example support for `learning_candidates`
- candidate review workflow documentation and `review-learning-candidates.py` helper
- stronger candidate entry lifecycle guidance, including `lifecycle_stage` and `evidence_count`
- machine-checkable integration checks for host entry files and writer skill contracts
- OpenClaw-style simulated tests covering fallback-only, external-adapter, partial-adapter, and invalid-schema scenarios

### Changed

- explicit corrections now route to `learning_candidates` by default instead of hardening immediately
- promotion rules now describe minimal candidate-to-lesson thresholds
- skill integration docs now explain correction staging and sampling boundaries
- host validation now checks for real `memory-governor` / `Memory Contract` markers instead of file existence only

## 0.2.7 - 2026-04-05

### Added

- maintainer-facing `tests/` with validator, host-checker, and bootstrap coverage
- more complex host fixtures covering split, directory/pattern, unknown target, and missing fallback cases
- `dev/` area for plans and evaluation materials
- `releases/` directory for versioned release notes

### Changed

- repository layout is now clearer about runtime package vs maintainer-only material
- maintainer entry docs are now bilingual in `dev/` and `releases/`

## 0.2.5-beta - 2026-03-31

### Changed

- public README now states more clearly that `memory-governor` is a governance kernel, not an execution-first skill
- public positioning now explains who should use it and when it may feel too heavy

## 0.2.4-beta - 2026-03-31

### Fixed

- `check-memory-host.py` and `validate-memory-frontmatter.py` now support Python 3.9 / 3.10 via `tomli` fallback

### Changed

- installation docs now call out Python version compatibility explicitly

## 0.2.3-beta - 2026-03-31

### Added

- migration guide for hosts that already have a messy memory setup
- manifest examples for `reusable_lessons` as `directory` or `pattern`

### Changed

- host checker and manifest contract now support `fallback_paths`
- installation and integration docs now point legacy hosts to the migration path
- integration checklist now calls out non-single `reusable_lessons` modes explicitly

## 0.2.2-beta - 2026-03-31

### Added

- bilingual public-facing intro sections in `README.md`
- bilingual opening guidance in `SKILL.md`

### Changed

- public packaging now reads more clearly for both English and Chinese readers

## 0.2.1-beta - 2026-03-31

### Added

- clearer English public-facing summary in `README.md`
- bilingual skill description in `SKILL.md` for ClawHub-facing metadata

### Changed

- public packaging now explains the `Installed / Integrated / Validated` model more clearly for external readers

## 0.2.0-beta - 2026-03-31

This is the first distributable beta shape of `memory-governor`.

### Added

- generic core + host profiles packaging model
- packaged fallback templates in `assets/fallbacks/`
- installation and integration guide
- host profile reference for `Generic` and `OpenClaw`
- snippets for host-level and skill-level integration
- before / after comparison page
- generic host validation record
- standalone `examples/generic-host/` example directory
- lightweight bootstrap script for generic hosts
- adapter manifest contract via `memory-governor-host.toml`
- manifest-driven host checker flow for generic and OpenClaw hosts

### Changed

- path-centric design language was tightened into `memory type -> target class -> adapter`
- optional skills such as `self-improving` and `proactivity` are now treated as adapters, not core dependencies
- OpenClaw is now framed as a reference host profile rather than the universal default
- OpenClaw host can now declare its adapter map explicitly instead of relying only on reference-profile inference

### Fixed

- machine-local absolute links were removed from package-facing docs
- fallback assets are now packaged inside the skill
- adapter resolution order is documented explicitly
- host checking can now prefer explicit manifest contracts over directory guessing

### Current Scope

`memory-governor` remains a governance kernel.

It does not attempt to become:

- a second-brain platform
- a universal sync bus
- a forced workspace migration tool

### Known Gaps

- no polished public landing page yet
- no richer installer beyond the lightweight bootstrap
- no versioned release automation
