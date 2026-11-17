# Changelog

## [0.2.5] - 2026-08-04

### Fixed
- The `version:` field in SKILL.md's frontmatter had drifted (stuck at 0.2.0
  since the 0.2.1–0.2.4 releases were versioned only via the publish CLI).
  Frontmatter now matches the registry version and will be bumped with every
  release going forward.

## [0.2.4] - 2026-08-04

### Changed
- Clarity: the scoring-rubric heading now names the job it serves ("for job
  7 — joke doctor & scorer") instead of the bare cross-reference "(job 7)".
  Docs only; no behavioral change.

## [0.2.3] - 2026-08-04

### Changed
- Language-separation sweep across all files: English sections are now purely
  English (no interleaved Chinese words or section names); each file opens
  with a one-line bilingual pointer to the Chinese section. Chinese sections
  unchanged. Docs only; no change to the skill's behavior.

## [0.2.2] - 2026-08-04

### Changed
- Release now carries GitHub source provenance (source repo/ref/commit) so
  the ClawHub page links back to the repository.
- README: explicit "Feedback & issues" section (in both languages) pointing
  to github.com/KimmyPlusLi/HumorUp/issues. Docs/metadata only; no change to
  the skill itself.

## [0.2.1] - 2026-08-04

### Changed
- README.md is now fully bilingual: complete English version first, complete
  Chinese version second (install, jobs table, safety, files — everything in
  both languages). Docs only; no change to the skill itself.

## [0.2.0] - 2026-08-04

### Changed
- Restructured SKILL.md and patterns.md for bilingual transparency: English
  content now comes first, followed by a self-contained Chinese section, so
  readers of either language get a coherent read without interleaved
  fragments of the other.
- SKILL.md's Chinese guide now carries the five laws in full Chinese,
  Chinese-specific rules (homophone puns, two-part allegorical sayings), a
  pattern-name mapping, and the Chinese calibration examples.
- patterns.md's Chinese section now carries Chinese build notes for all
  universal patterns plus the three Chinese-only patterns (homophone pun,
  two-part allegorical saying, parallel deflation).
- No behavioral change: the seven jobs, five laws, anti-cringe contract, and
  scoring rubric are unchanged.

## [0.1.0] - 2026-08-02

### Added
- Initial release: 7 humor jobs (punch-up, occasion writer, witty daily brief,
  joke on demand, icebreakers, caption-this, joke doctor & scorer).
- Five craft laws for every humorous line, in English and Chinese.
- 14-pattern bilingual pattern library (`patterns.md`) with build steps and
  failure modes per pattern.
- 4-dimension scoring rubric with calibration examples.
- Anti-cringe contract: explicit rules for when NOT to be funny.

### Security
- Pure-prompt skill: no scripts, no environment variables, no CLI dependencies,
  no network access. Nothing to declare in `metadata.openclaw.requires` — and
  that's the honest declaration.
