# Changelog

## 1.1.2 (2026-03)

### Fixed
- Excluded `backend/` and `frontend/` from ClawHub package to resolve all 5 safety review flags (dynamic code execution, trust_remote_code, runtime downloads, undocumented env vars — all in the optional backend, not in the skill itself)
- Removed hardcoded backend API URL from skill.yaml prompt; replaced with generic persistence fallback
- Clarified `shell` permission is exclusively for ffmpeg audio conversion, not for running scripts or downloading models

### Updated
- Documentation updated to clearly separate ClawHub skill (LLM-only) from optional self-hosted backend (GitHub only)
- Added publish-clean.sh script for guaranteed clean ClawHub publish

## 1.1.0 (2026-03)

### Added
- **Audio pronunciation scoring**: ffmpeg + ASR integration for real PR band scores from audio input (requires `shell` permission)
- **Mock exam mode** (Menu 7): Full Part 1→2→3 simulation with timed flow and comprehensive final report
- **ZPD learning paths** (Menu 6): Personalized vocabulary and grammar progression based on Zone of Proximal Development theory
- **Adaptive difficulty**: Question difficulty auto-adjusts based on user's band level
- **Pronunciation guide**: Dedicated `pronunciation-guide.md` with Chinese speaker-specific diagnostics and exercises
- **42 difficulty-tagged cue cards**: Expanded from 10 to 42 cards across 7 categories with [Easy]/[Medium]/[Hard] tags
- **Learning path reference**: `learning-path.md` with band-stratified vocabulary ladders, grammar milestones, and daily practice templates
- **Backend API integration**: Optional backend endpoints for persistent scoring, learning state, and trajectory planning

### Updated
- Prompt compressed for token efficiency while retaining all features
- Scoring template now includes "下一步学习方向" (ZPD recommendations)
- PR estimation improved: uses median of FC/LR/GRA for text-only, ASR confidence mapping for audio
- Trigger keywords expanded to cover mock exam and learning path entry points

## 1.0.2 (2026-03)

### Updated
- Reduced public release permissions to `network` only for easier ClawHub review
- Removed local-model, shell, and persistence requirements from the published skill package
- Simplified public documentation to focus on menu-driven IELTS practice and bundled cue cards

## 1.0.1 (2026-03)

### Updated
- Added fixed-entry IELTS speaking mode with explicit enter/exit phrases
- Added menu-driven workflows for Part 1, Part 2, Part 3, scoring, and grammar correction
- Standardized scoring and correction outputs with fixed Chinese templates
- Prioritized Part 2 cue cards from `cue-cards-2025-may-aug.md`, then `cue-cards.md`
- Added fixed topic rotation for Part 1 and Part 3 follow-up generation based on Part 2 themes

## 1.0.0 (2025-03)

### Added
- Four-criterion IELTS scoring (FC, LR, GRA, PR) with Band 1-9 descriptors
- CHAI calibration for Part-specific score adjustment
- Grammar corrections (genuine errors only, no punctuation/style)
- Context-aware vocabulary upgrades via vocab-map.json
- Spoken-register model answers (LLM or local Qwen3-0.6B)
- Part 1/2/3 support with Part-specific expectations
- 15 cue cards from 2025 May–August IELTS question bank
- Optional persistence (load_trajectory, update_trajectory) for learning path tracking
- 24 trigger keywords (English + Chinese)
