# Changelog

All notable changes to Lucid will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased] — "Sharper Dreams"

### Planned
- **Memory Section Split**: MEMORY.md → `memory/sections/*.md` via `scripts/migrate_memory.py`. Selective loading, reduced context bloat.

## [0.7.8] - 2026-04-01

### Fixed
- Removed CLAWD_DIR from env metadata entirely — mentioned in note only, eliminating optional/required mismatch

## [0.7.7] - 2026-04-01

### Fixed
- Cleaned up CHANGELOG (removed debugging history, consolidated v0.7.x entries)

## [0.7.0] - 2026-04-01

### Added
- **Session Debrief**: Documented optional ~18:00 quick-capture cron (`prompts/session-debrief.md`) in `SKILL.md` and `README.md`. Reads today's daily note and writes key decisions/facts directly to memory — faster than nightly review.
- **Contradiction Detection**: Step 6b in nightly review scans MEMORY.md vs last 7 daily notes for version/status/existence/value/decision conflicts. Outputs `## ⚡ Contradictions Detected` section. High-confidence factual contradictions auto-apply.

### Changed
- **Auto-apply config**: Added factual contradictions as auto-apply category in `config/auto-apply.md`.

## [0.6.7] - 2026-03-30

### Security
- **CLAWD_DIR hard requirement:** `nightly-review.md` now validates `CLAWD_DIR` is set before any file operations and aborts with a clear error if missing — eliminates silent fallback to cwd causing unintended reads/writes/commits in unknown directories
- **Removed `${CLAWD_DIR:-.}` fallback pattern** from all three git commit calls — replaced with strict `${CLAWD_DIR}` (no cwd fallback)
- **Trend script workspace fix:** `trend_detection.py` invocation now passes `${CLAWD_DIR}` instead of `$(pwd)` for consistent workspace resolution

## [0.6.6] - 2026-03-30

### Security
- **Shell injection hardening:** Git commit messages in `prompts/nightly-review.md` are now static strings instead of AI-generated dynamic content, eliminating potential shell injection via indirect prompt injection from markdown notes.

## [0.6.6] - 2026-03-30

### Fixed
- Version bump (previous version already published)

## [0.6.5] - 2026-03-30

### Added
- **Pre-flight flush prompt** (`prompts/pre-flight-flush.md`): Optional cron at 02:45 Vienna time that appends today's session context to the daily memory file before Lucid runs at 03:00. Ensures Lucid always reads fresh data even when the main session wasn't manually flushed. Use `append` mode — never overwrites existing content.

- **Memory Index**: Auto-generated `memory/index.md` manifest with section descriptions and last-updated timestamps.
- **Memory Index**: Auto-generated `memory/index.md` manifest with section descriptions and last-updated timestamps.
- **Session Debrief** (`prompts/session-debrief.md`): Lightweight end-of-day quick-capture prompt (target: <2 min, <5k tokens).
- **Contradiction Detection**: Step 6b in nightly review — compares memory vs daily notes, classifies as factual vs judgment.
- **Memory Loading Guidance** (`prompts/memory-loading-guidance.md`): Instructions for selective section loading.

### Attribution (for planned features)
Architecture inspired by [ByteRover](https://github.com/openclaw/openclaw/pull/50848)'s Context Engine approach — hierarchical memory tree, after-turn learning, contradiction detection. Lucid adapts these as a zero-dependency skill.

## [0.6.6] - 2026-03-30

### Fixed
- Version bump (previous version already published)

## [0.6.5] - 2026-03-30

### Fixed
- Version bump (previous version already published)

## [0.6.4] - 2026-03-29

### Changed
- **README rewrite:** Cleaner structure, removed bloat, sectioned memory moved to Roadmap, no more false claims about unreleased features. Honest about what's shipped vs planned.

## [0.6.3] - 2026-03-29

### Fixed
- **README honesty:** Sectioned Memory architecture section now clearly marked as "Planned / upcoming" instead of implying it's released. Features exist as experimental scripts but are not part of the default workflow.

## [0.6.2] - 2026-03-29

### Fixed
- Removed fake Telegram token from example review file

## [0.6.1] - 2026-03-29

### Fixed
- **Config defaults now match documentation:** `autoApply.enabled`, `aggressiveCleanup.enabled`, and `announceOnDelivery` all default to `false` in shipped config. Previously shipped as `true`, contradicting README/SKILL.md claims of "opt-in, default off."
- Removed hardcoded notification channel from default config

## [0.6.0] - 2026-03-29

### Added
- **Aggressive Cleanup** (opt-in): When enabled via `aggressiveCleanup.enabled` in config, Lucid auto-removes resolved Open Loops, closed Blockers, and confirmed-stale entries from MEMORY.md. Each removal is a separate git commit for easy rollback. Removed items are listed in the review file under `## 🗑️ Removed (Auto-Cleanup)` with git hashes. Default: off.

### Changed
- `prompts/nightly-review.md`: New Step 7a for aggressive cleanup workflow
- `config/auto-apply.md`: Added aggressive cleanup section with criteria and rollback docs

## [0.5.0] — 2026-03-27

### Fixed
- Portability fixes: removed hardcoded workspace paths, fixed config loading in `trend_detection.py` to look relative to script dir first, fixed loop bug where `args.days` (could be None) was used instead of resolved `days` variable, cleared hardcoded telegram topic from default config

## [0.4.0] — 2026-03-25

### Added
- **Trend Detection** module (`scripts/trend_detection.py`) — analyzes patterns across 14 days of daily notes:
  - **Recurring Issues** — flags topics/problems appearing on 3+ separate days (e.g., "backup failed", "tailscale down")
  - **Stale Project Detection** — finds projects in MEMORY.md not mentioned in any daily note for 30+ days
  - **Escalated Patterns** — detects the same lesson/mistake appearing in 3+ daily notes (repeated mistakes not yet fixed)
- New `## Trends` section in nightly review output (`memory/review/YYYY-MM-DD.md`)
- Trend history tracking in `state.json` under `trends` key (accumulates across runs, keeps last 30 entries)
- Nightly review prompt updated with Step 7b to invoke trend detection script
- Example review and state files updated with trend output samples

### Technical Details
- Standalone Python script with no external dependencies (stdlib only)
- Uses difflib SequenceMatcher for fuzzy clustering of similar issues/lessons
- Configurable via CLI flags: `--days`, `--stale-days`, `--min-recurrence`

## [0.3.0] — 2026-03-21

### Added
- **Extended Auto-Apply categories** (5 new safe classes):
  - Infrastructure facts — cron IDs, script paths, service names, port assignments
  - Lessons Learned — purely factual technical lessons
  - Model Strategy — agent counts, new agent entries when fully documented
  - Closed Open Loops — remove resolved items with explicit closure signal on 2+ days
  - Stale project status — update planning/in-progress to live when URL + service confirmed
- **`config/auto-apply.md`** — configurable file to enable/disable auto-apply categories per project. Edit it to go conservative, aggressive, or anywhere in between.
- **Stricter confidence gate**: medium/low confidence items never auto-applied (only high)
- Prompt reads `config/auto-apply.md` at runtime if present (Step 4b)

## [0.2.0] — 2026-03-18

### Added
- **Auto-Apply** for high-confidence, low-risk suggestions:
  - Version numbers in skill/plugin tables
  - Stale Cron IDs where removal is documented
  - New project entries with complete details (2+ days mentioned)
- **Git integration**: auto-apply commits to local git with descriptive message (`dreamer: auto-apply — DESCRIPTION`)
- **Rollback**: `git revert <hash>` to undo any auto-applied change
- Review file now has `## ✅ Auto-Applied` section showing what was applied automatically

### Changed
- Review format updated: auto-applied changes shown separately from pending decisions
- State ledger: auto-applied suggestions tracked as `accepted` immediately

### Never Auto-Applied (by design)
- Belief Updates, Key Decisions, Family/personal facts
- Model Strategy preferences
- Anything with uncertainty

## [0.1.0] — 2026-03-16

### Added
- Initial release of Lucid V1
- Nightly review prompt with 6 analysis categories:
  - Candidate Updates, Open Loops, Blockers, Belief Updates, Stale Facts, Duplicate/Merge Suggestions
- Suggestion ledger (`state.json`) with status tracking (pending/accepted/rejected/deferred)
- Health sentinel (`.last-success` timestamp)
- Anti-circular reasoning rule (never reads own previous reviews)
- Decision policy with 2-day threshold, confidence labels, output cap
- Negative rules (no credentials, tokens, volatile URLs in memory)
- Memory class awareness (personal facts vs project state vs policies)
- Example review output and state ledger
- Full architecture documentation

### Design process
- Concept reviewed by 4 AI agents across 2 rounds:
  - Round 1: Codex (GPT-5.3) + Claude Code (Sonnet 4.6) — pragmatic + architectural feedback
  - Round 2: Codex (GPT-5.4) + Claude Code (Opus 4.6) — deeper failure mode analysis
- Key insights incorporated:
  - State ledger for idempotency (GPT-5.4)
  - Anti-circular reasoning (Opus)
  - Memory classes (GPT-5.4)
  - "Curator, not journalist" framing (GPT-5.4)
  - Drop morning send from V1 (both)
