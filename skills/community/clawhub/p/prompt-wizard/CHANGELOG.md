# Changelog

All notable changes to Prompt Wizard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.5] — 2026-05-02

### Changed
- `/wizard update-library`: hardened fence — MUST execute script, anti-bypass language added, honesty rule for no-permission case

### Added
- Common Violations: added "short-circuiting update-library" and "fabricating script output" anti-pattern rows

## [1.0.4] — 2026-05-02

### Fixed
- CHANGELOG: restored correct 1.0.1 and 1.0.2 content after a version split edit error corrupted the heading structure

## [1.0.3] — 2026-05-02

### Fixed
- **update-prompts.sh**: light install (ClawHub without images) now detected and forces full download even when version matches
- **Output Format**: added explicit image-file-existence check before displaying fallback message
- **≥4 GATE**: added explicit "FULL Output Format" requirement to prevent agent using shortened confirmation format
- Display step clarified as per-prompt (not end-of-session summary)
- Second case entry template in Output Format aligned with conditional image check

### Added
- `/wizard version`: add update check hint (`git pull` / `clawhub search`)
- Common Violations: added "shortened format for confirmation" anti-pattern row

### Docs
- **GOVERNANCE.md**: release checklist, file dependency map, fence design principles

## [1.0.2] — 2026-05-02

### Added
- `/wizard version` command — displays skill and library version info
- Workflow Compliance section with mandatory case grounding requirements
- Common Violations (Anti-Patterns) reference table to prevent known failure modes
- ⛔ GATE markers at critical confirmation points in multi-prompt ≥4 strategy
- Silent case library search requirement in multi and pro modes
- Round budget for multi mode

### Changed
- **Breaking:** Case grounding is now MANDATORY — every prompt must reference at least one case library entry
- Style Anchor step no longer skippable (user must explicitly opt out)
- Prompt Generation Rule 6 changed from "Case-anchored (if chosen)" to "Case-grounded (MANDATORY)"
- Multi mode ≥4 strategy now requires first-prompt confirmation before generating remaining prompts
- Output Format: Related Cases section now mandatory

## [1.0.1] — 2026-05-01

### Added
- `/wizard multi` multi-prompt generation (batch, variations, series)
- Text/copy proactive inquiry before prompt generation
- Logo silent removal from prompts (add logo to generated images separately)
- Lightweight ClawHub distribution (case images downloadable on demand)

### Changed
- `/wizard pro` extended to 8 steps with Text/Copy step
- Case images gracefully degrade when not installed
- `.clawhubignore` excludes non-essential files from ClawHub publish

## [1.0.0] — 2026-05-01

### Added
- `/wizard` conversational prompt generation with 6-dimension coverage
- `/wizard pro` structured 7-step guided mode with `/back` and `/skip`
- Market/audience dimension for regional aesthetic alignment
- Style anchoring: pre-generation case pattern matching from the library
- `/examples` command with 6 curated highlight cases
- `/templates` command to browse 175+ community-verified prompts
- `/lang` command for multi-language conversation support
- `/update` command to fetch the latest case library
- Quick refine after generation (darker, brighter, more minimalist, etc.)
- Bundled case library with local image references
- OpenClaw platform compatibility
- Bilingual documentation (English + Chinese)

### Deprecated
- `setup.sh` removed — data is now bundled directly in the repository

[1.0.1]: https://github.com/EricArcha/prompt-wizard/releases/tag/v1.0.1
[1.0.0]: https://github.com/EricArcha/prompt-wizard/releases/tag/v1.0.0

Repository: https://github.com/EricArcha/prompt-wizard
