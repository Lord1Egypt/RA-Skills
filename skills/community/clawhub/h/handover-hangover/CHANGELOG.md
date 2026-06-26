# Changelog

## [Unreleased]

## [1.2.1] — 2026-05-10

### Changed
- Managed hook now executes `handoff.sh` directly via its shebang instead of launching `bash` explicitly from `child_process`.
- Hook performs a best-effort executable-bit repair before launch so updated installs continue working even if older copies of `handoff.sh` lost `+x`.

### Fixed
- Reduced ClawHub scanner exposure around explicit shell execution in `hooks/handover-hangover/handler.js` without changing runtime behavior.

## [1.2.0] — 2026-05-09

### Added
- Managed OpenClaw hook pack under `hooks/handover-hangover/` (`HOOK.md` + `handler.js`).
- `scripts/install-integration.sh` to install/enable the managed hook and print fallback snippets.
- `scripts/status.sh` to diagnose watchdog executable state, managed hook install state, hook config, and memory baton files.
- Next-turn lifecycle coverage via `message:received`, plus `/new`, `/reset`, and `gateway:startup` boundaries.

### Changed
- README integration now targets the current OpenClaw hook system first, with boot/heartbeat as version-tolerant fallbacks.
- SKILL.md now explicitly treats hook/API drift as expected and tells agents how to diagnose/install integration.
- Integration language is model/provider agnostic; Codex, Anthropic, Gemini, local models, and manual model switches are all treated as interpreter handoffs over the same filesystem baton.

### Fixed
- ClawHub users no longer have to infer obsolete `afterTurn` wiring from README examples.
- Watchdog automation no longer depends on undocumented ad-hoc hook directories.

## [1.1.3] — 2026-04-07

### Changed
- License: MIT → MIT-0 (ClawHub publishing requirement — uniform licensing)
- `.clawhubignore`: exclude CLAUDE.md and `.claude/` from published bundle
- Added `homepage` metadata to SKILL.md frontmatter

## [1.1.2] — 2026-04-07

### Changed
- INIT bootstrap note no longer includes noisy workspace-wide file list and git status (Ronin live-test feedback)

## [1.1.1] — 2026-04-07

### Changed
- WORKSPACE path resolution: added comment and dev-copy warning (Ronin review)
- README: softened "guarantee" to "ensure", afterTurn hook to neutral tone (Ronin review)

## [1.1.0] — 2026-04-06

### Changed
- Watchdog refactored to idempotent semantics — safe for frequent execution (heartbeat, cron, afterTurn hooks)
- Four-scenario logic: CONFIRMED / NO-OP / DIRTY SWITCH / INIT
- Integration section rewritten: `afterTurn` hook (primary) + boot (baseline) + heartbeat (safety net)

### Added
- Sealed marker (`.handoff-sealed`) — internal watchdog state that prevents repeated fallback generation on the same boundary
- `memory/.handoff-sealed` added to `writePaths` in SKILL.md frontmatter
- `afterTurn` hook wiring example in README

### Fixed
- Repeated watchdog runs no longer destroy good baton with mechanical fallback
- `find` in `recent_changes()` wrapped with `timeout 5` to prevent hanging on large workspaces

## [1.0.3] — 2026-04-06

### Fixed
- Documented actual execution model: OpenClaw does not auto-execute skill scripts
- Watchdog script header no longer claims "runs at the start of every turn"

### Added
- Integration section in README with boot sequence and heartbeat wiring examples
- Layer coverage table (`SKILL.md` / boot / heartbeat)
- `CHANGELOG.md` for ClawHub publishing readiness

### Changed
- Channel 3 description reframed as session-boundary guarantee, not per-turn
- "No configuration needed" replaced with integration pointer
- `requires.bins: [bash]` added to SKILL.md frontmatter

## [1.0.2] — 2026-04-06

### Fixed
- Clean model switches no longer bypass detection — `.handoff-pending` signal is now created on every turn (CONFIRMED, DIRTY SWITCH, INIT)
- README "Zero overhead" claim corrected to "Low overhead" to match actual baton-check mechanics

### Added
- Same-model early-exit in read-side Step 1 — skips full reboot when baton author matches current model
- Safe-fail clause: unparseable or mismatched author names degrade to full read-side, not silent skip
- `requires.bins: [bash]` in SKILL.md frontmatter
- `chmod +x` guidance in README installation and SKILL.md INIT onboarding
- CHANGELOG.md

### Changed
- Detection table rewritten for three-row "baton available" semantics
- Indicator 1 description: "anomaly detected" → "baton available for you"
- Version synced across SKILL.md and README.md

## [1.0.1] — 2026-04-06

### Fixed
- Indicator 1 false-positive: replaced `.prev.md` existence check with `.handoff-pending` sentinel
- Privacy boundary: read-side Step 2 now respects `AGENTS.md` boundaries instead of reading all boot files unconditionally

### Changed
- `current-task.md` update frequency clarified (on task change, not every state-changing moment)
- Security section rewritten with explicit write targets and recovery read scope
- `.handoff-pending` added to `writePaths` in frontmatter

## [1.0.0] — 2026-04-06

### Added
- `SKILL.md`: system prompt with write-side protocol, three-indicator detection, read-side with epistemic reset
- `scripts/handoff.sh`: bash watchdog with INIT / CONFIRMED / DIRTY SWITCH scenarios
- `README.md`: project description with three-channel architecture overview
- `.clawhubignore`: excludes internal design documents from ClawHub publishing
