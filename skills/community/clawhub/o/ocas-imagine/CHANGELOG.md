# Changelog

## [1.1.0] - 2026-09-16

### Changed
- **Concise art-direction output schema** — art-direction output formatted as structured JSON (prompt text, normalized style_weights per section, negative_prompt, content_summary) for programmatic consumption.


## [1.0.4] - 2026-04-14

### Changed
- Storage paths migrated from `~/openclaw/...` to `{agent_root}/commons/...` per updated `spec-ocas-storage-conventions.md` (`{agent_root}` makes skills deployable across hosts; `/commons/` matches the Hermes runtime layout).
- All path references updated across `SKILL.md` (frontmatter `filesystem.read|write`, Storage Layout, Validation Rules, Flow steps), `README.md` (Setup), and `references/journal.md` (Location).

## [1.0.3] - 2026-04-14

### Changed
- Split `references/default_styles.md` into one file per style: `soma.md`, `noir.md`, `hiro.md`, `comic.md`, `candy.md`, `vaporware.md`. `default_styles.md` is now a thin index pointing to each file.
- Updated Support File Map in SKILL.md to list each style file individually.

### Added
- Guidance in `default_styles.md` for adding a new default style (file naming, section shape, index entry).

## [1.0.2] - 2026-04-14

### Added
- `README.md` and `CHANGELOG.md` per `spec-ocas-skill-publishing.md`.
- `references/journal.md` defining the Imagine journal record schema.
- System-skill sections in SKILL.md: Responsibility Boundary, Optional Skill Cooperation, Ontology Mapping, Journal Outputs, Visibility, Background Tasks, Validation Rules.
- Storage Layout section referencing `{agent_root}/commons/` paths.

### Changed
- Storage paths migrated from `{agent_root}/commons/data|journals/ocas-imagine/` to `~/openclaw/data/ocas-imagine/` and `~/openclaw/journals/ocas-imagine/` to match the then-current `spec-ocas-storage-conventions.md` (later superseded; see 1.0.4).
- Frontmatter `filesystem.read` and `filesystem.write` entries updated to the `~/openclaw/` root.
- Description refined for routing (explicit trigger / non-trigger language differentiating Imagine from `ocas-look`).

### Fixed
- Support File Map previously referenced `references/journal.md`, which did not exist in the package. File now added.

## [1.0.1] - Prior

### Added
- Initial release of the Style/Content separation methodology.
- `imagine.generate`, `imagine.extract`, `imagine.library.list`, `imagine.style.save`, `imagine.journal` commands.
- `references/style_prompt_guide.md`, `references/default_styles.md`, `references/api_reference.md`.
