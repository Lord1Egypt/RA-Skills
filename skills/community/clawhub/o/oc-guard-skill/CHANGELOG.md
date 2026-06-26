# Changelog

All notable changes to this project are documented here.

## [1.1.2] - 2026-03-06

### Fixed
- Added `scripts/oc-guard.py` so ClawHub package includes a concrete executable CLI file
- Updated skill command examples to use `{baseDir}/scripts/oc-guard.py` for package consistency checks

### Docs
- Updated publish verification checklist to assert `scripts/oc-guard.py` is present in ClawHub package files

## [1.1.1] - 2026-03-06

### Changed
- Refreshed `README.md` with a navigation table of contents and release/tag guidance

### Docs
- Added release checklist details covering changelog, tag, GitHub Release, and ClawHub verification order

## [1.1.0] - 2026-03-06

### Added
- Added official `openclaw config validate` checks in both `plan` and `apply` flows
- Added enum guardrails for high-risk fields (including `tools.exec.ask`)
- Added drift detection between global provider settings and `~/.openclaw/agents/*/agent/models.json`
- Added post-apply canary checks using local agent turns (prefer `main` and `bro`)

### Fixed
- Updated skill metadata with `metadata.openclaw.requires` so runtime prerequisites are explicit
- Updated skill instructions to invoke bundled CLI via `{baseDir}/scripts/oc-guard`
- Added publish verification guidance to ensure ClawHub package includes `scripts/oc-guard`

### Security
- Treat "gateway running" as insufficient success signal; rollback now triggers when canary response validation fails

## [1.0.3] - 2026-03-05

### Fixed
- Added local diagnostics for `plan` proposal failures by persisting raw `opencode` output to `/tmp/oc-guard-last-opencode-output.txt`
- Improved failure messaging when proposal JSON extraction/parsing fails, including debug file location

### Security
- Documented and enforced no-bypass rule: do not directly edit config when `oc-guard` returns failed/blocked
- Preserved execution receipt contract, high-risk confirmation gate, and backup/rollback flow

## [1.0.2] - 2026-03-05

### Fixed
- Added `【模型说明-未执行】` marker for blocked (`status=阻断`) non-executed paths in receipt details
- Preserved existing execution receipt contract and apply backup/rollback behavior

## [1.0.1] - 2026-03-05

### Changed
- Updated README with bilingual (Chinese + English) content
- Added release announcement section at README top for public sharing

## [1.0.0] - 2026-03-05

### Added
- Initial `oc-guard-skill` release with `plan` and `apply` workflow
- High-risk gating with `--confirm`
- Validation for channels, bindings, agents, and models references
- Auto backup before apply and rollback on failure
- Unified bilingual execution receipt with 12-char signature

### Security
- Path allowlist for guarded mutations
- Secret masking in receipt details
- Public package boundary guidance
