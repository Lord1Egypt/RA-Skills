# Changelog

## v1.1.3 - 2026-03-25

### Changed
- Updated README examples to prefer `QWEN_API_KEY` instead of `HF_TOKEN`
- Synced quick-start, env vars, and shell examples with the Qwen-first setup

## v1.1.2 - 2026-03-25

### Changed
- Unified SKILL.md and script headers to the Qwen-first backend order
- Removed remaining outdated persona suffix wording from the official-face prompt tail
- Synced README badge version for the new release

## v1.1.1 - 2026-03-25

### Changed
- Cleaned up remaining Hugging Face-first wording in README
- Synced README backend strategy text with the real runtime order
- Clarified FAQ / limitations / current status sections around Qwen-first routing

## v1.1.0 - 2026-03-25

### Added
- Qwen (`qwen-image-plus`) image generation backend via DashScope async API
- Qwen-first routing with Hugging Face fallback and optional Gemini compatibility path
- Expanded README showcase to a 4-image two-row layout
- Updated official face asset and latest generated showcase materials

### Changed
- README hero image now uses the current official face
- README backend description now reflects `Qwen -> Gemini(optional) -> Hugging Face fallback`
- Project showcase order updated to: official face / beach / Everest / swimming pool

### Notes
- Qwen is now the preferred backend for day-to-day generation in this project.
- Hugging Face remains the fallback free backend.
- Face consistency is still soft consistency, not hard face lock.

## v1.0.0 - 2026-03-25

First public release.

### Added
- Hugging Face default image generation flow
- Official face soft-anchor mechanism
- Direct / mirror generation modes
- Gemini probe path (disabled by default)
- TypeScript wrapper script
- Public Chinese README landing page
- Install script: `scripts/install.sh`
- ClawHub distribution: `nasplycc-clawra-selfie`
- CONTRIBUTING / SECURITY docs
- GitHub public release: `v1.0.0`

### Notes
- Gemini image generation is currently disabled by default due to free-tier quota limitations.
- Hugging Face remains the active free fallback backend.
- Current face consistency is still soft consistency, not hard face lock.
