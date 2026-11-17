# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-17

### Added

- Added the `.github/` platform configuration: issue forms, pull request template, CI workflow, `CODEOWNERS`, and Dependabot.
- Added `SUPPORT.md`, `.gitattributes`, and a `Makefile` with `validate`, `syntax`, and `clean` targets.

### Changed

- `SECURITY.md` now specifies the private reporting channel and the response timeline.
- `CONTRIBUTING.md` no longer references a nonexistent `requirements.txt`; the project is standard-library only.
- `LICENSE` now carries the project copyright notice.
- Updated the file trees in `README.md` and `README FOR AI.md`.

### Fixed

- `scripts/validate-project.py` no longer crashes on binary files such as `__pycache__` bytecode.

## [0.1.0] - 2026-09-12

### Added

- Added the repository contract validator at `scripts/validate-project.py`.
- Added GitHub-standard governance and editor configuration files.

### Changed

- Standardized `SKILL.md` and `CHANGELOG.md` filename casing.
- Clarified the separation between runtime references and user-facing prompts.
- Added `argparse` command-line interfaces to the executable scripts.
