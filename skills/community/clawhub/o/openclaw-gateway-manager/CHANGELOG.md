# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-03-23

### Added

- Added a Chinese project README.
- Added `scripts/common.sh` to centralize OS detection, instance resolution, port lookup, and service control helpers.
- Added `SECURITY_RESPONSE.md`.

### Changed

- Clarified installation guidance: normal installation should use the skill system/runtime chosen location; manual cloning is only for local development or debugging.
- Updated `README.md`, `README.en.md`, `SKILL.md`, `README_发布指南.md`, and `ClawHub_上传说明.txt` to distinguish repository location from OpenClaw instance config directories.
- Updated package and metadata versions to `1.0.2`.
- Expanded platform support docs to match current behavior on macOS, Linux, and Windows manual mode.

### Fixed

- Fixed hardcoded installation examples that incorrectly suggested using `~/.jvs/.openclaw/...` as the repository location.
- Fixed script executability by ensuring shell scripts are runnable.
- Fixed macOS Bash 3 compatibility issues in the port scan flow.
- Unified service handling for macOS `LaunchAgent`, Linux `systemd --user`, and manual fallback mode.

