# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-11-24

Reworks the skill around evidence and safety instead of a single linear pass.

### Added

- Phase 0 preflight: reads `AGENTS.md` / `CONTRIBUTING.md`, detects the package manager and monorepo task graph, and checks issue state, assignees, and existing PRs before writing code.
- Phase 1 reproduce: records a pre-change baseline and requires a failing test or a minimal reproduction script that fails for the reported reason.
- State file `.issue-to-pr/state.json` with a JSON schema, so interrupted or reset runs can resume instead of restarting.
- Red-green proof in Phase 4: temporarily removing the source change must make the new test fail.
- Self-review phase covering boundary cases, error paths, test validity, secrets, docs, and translations.
- CI loop after PR creation: watch checks, read failing logs, iterate at most twice, and report "no checks" instead of claiming green.
- `references/state.schema.json` and `references/pr-evidence.md`.
- Installer support for multiple harnesses: `--target`, `--project`, `--list-targets`, `--force`, and `--uninstall`.

### Changed

- Repository conventions (commitlint scopes, DCO sign-off, changesets, PR templates) are detected instead of assumed.
- PR body now carries reproduction evidence, verification results, risk, rollback, and explicit "not covered" items.
- Test selection prefers the narrowest target (`nx affected`, filtered package tests) and compares failures against the baseline.
- Tool references are capability-based, so the skill works across harnesses rather than assuming IDE-specific tools.

### Fixed

- Untrusted issue text is treated as data, with explicit rules against executing issue-supplied commands and reading credential paths.
- Fork, remote, branch, and PR handling are idempotent; a missing fork remote or an existing fork no longer breaks the run.
- Missing build artifacts are classified as environment problems instead of code regressions.
- `gh` capabilities are checked before using optional flags.

### Removed

- The 8-phase linear flow with no baseline, no state, and no post-PR follow-up.

## [1.3.0] - 2025-04-08

### Improved
- Simplified PR submission flow: merged Phase 7/8 dual confirmation into a single step
- Early push permission detection and automatic fork preparation in Phase 3
- Streamlined fork workflow from 5 steps to direct remote selection
- Extended issue input formats: supports `owner/repo#123`, `#123`, and plain issue numbers
- Optimized repository location logic: removed hardcoded path scanning
- Enhanced default branch detection with GitHub API priority
- Added repository PR template detection and Draft PR support
- Added structured analysis output template in Phase 4

### Added
- Scope assessment section for multi-problem issues and monorepo detection
- Handling for missing test frameworks with static analysis fallback
- Branch conflict detection before creating fix branches
- New error handling scenarios in the error table

### Removed
- Redundant "Model Invocation" section (duplicated Progress Checklist)
- Merged "Security and Privacy", "Trust Statement", and "External Endpoints" into concise "Notes" section

## [1.2.0] - 2026-04-08

### Added
- PR body template now includes a promotional footer linking back to the issue-to-pr skill repository

## [1.1.0] - 2026-04-08

### Added
- Interactive PR submission workflow (Phase 7 & 8)
- Auto commit, push, and PR creation with user confirmation
- Auto-fork support for repositories without write access
- PR creation verification and URL feedback

### Changed
- Split original Phase 7 into Phase 7 (Present Changes) and Phase 8 (Submit PR)
- Enhanced error handling for push/PR failures

## [1.0.0] - 2025-04-08

### Added
- Initial release
- 7-phase workflow: Parse URL → Fetch Issue → Locate Repo → Analyze → Fix → Verify → Summary
- GitHub CLI (gh) integration with fetch_content fallback
- Auto-detection of default branch
- Commit message and PR description templates
- Comprehensive error handling
