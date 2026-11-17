# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffold and validation workflow.
- `SUPPORT.md` and `GOVERNANCE.md` for support channels, roles, and decision process.
- `.gitattributes` for line-ending normalization and binary-file marking.
- `.github/` platform configuration: issue forms (bug report, feature request, config), pull request template, CI workflow (structure validation, ShellCheck, PR title lint), CODEOWNERS, dependabot, and funding options.

### Changed
- Updated project structure and documentation to align with the build specification in README_FOR_AI.md.
- README.md: corrected the clone URL and refreshed the file structure overview.
- SECURITY.md: switched the preferred reporting channel to GitHub private vulnerability reporting and quantified the 90-day coordinated disclosure window.
- CODE_OF_CONDUCT.md: quantified the 5-business-day complaint review target.
- LICENSE: added the project copyright line above the canonical GPLv3 text.
- `.gitignore`: excluded the local `.workbuddy/` tooling directory.
- `scripts/validate-structure.sh`: registered `.gitattributes`, `SUPPORT.md`, `GOVERNANCE.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS`, and `.github/dependabot.yml` as optional files.

### Fixed
- Added the required root documentation and update script to satisfy project quality gates.

## [1.0.0] - 2026-09-12

### Added
- Initial K-12 teaching skill scaffold with project metadata, skill index, and prompt deliverables.
- Syllabus registry and grade crosswalk skeleton for curriculum mapping.
- Validation script for structural and quality-gate checks.
- Shared instructional methodology and reusable teaching patterns.

### Changed
- Established the canonical English-language project documentation and repository structure.

### Fixed
- Corrected file naming and required project assets to match the build specification.

### Security
- Documented the security reporting process.
