## [0.3.4] - 2026-03-03
### Added
- Simplified installation instructions (Ask OpenClaw / CLI) to SKILL.md for better ClawHub visibility.
- Zero-Secret Logging and Redaction Protocol (v0.3.2/v0.3.3).
### Security
- Removed all API key / credential handling (no curl, no env vars, no non-LLM checks)
- Phase 2 now exclusively uses `sessions_spawn` — zero credential access
- `credentials: none` declared in metadata
- Removed contradictory stale references in CHANGELOG and verify script
- Added dry-run mode, 3-field auto-fix pause, before/after logging

## [0.1.0] - 2026-03-02

### Initial Release
- 5-phase post-upgrade verification system
- MODEL_GROUND_TRUTH.md template with YAML-formatted config/cron/model declarations
- Auto-repair for config drift (Phase 1) and cron drift (Phase 3)
- LLM provider liveness via `sessions_spawn` (tests real routing path)
- Non-LLM provider liveness: removed in v0.3.0 (was env-injected curl, now out of scope)
- Channel liveness with cross-context WhatsApp workaround
- UPGRADE_SOP.md for standardized upgrade procedure
- AGENTS.md GROUND_TRUTH sync rule snippet
