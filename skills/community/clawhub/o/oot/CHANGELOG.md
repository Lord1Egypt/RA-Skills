# Changelog

All notable changes to OOT are documented here.

## [1.4.3] - 2026-02-18

### Fixed
- README completely rewritten: correct name ("OOT"), version badge (1.4.3), install command (clawhub install Cloud-Dark/oot), license (MIT-0), all skill paths corrected to oot, v1.4.x features documented.

### Added
- RTK companion support documentation — added `references/RTK.md` plus README/SKILL guidance for combining OOT (context/model optimization) with RTK (shell output compression).

## [1.4.2] - 2026-02-18

### Fixed
- **ClawHub security scanner: `Source: unknown` / `homepage: none`** — Added `homepage`, `source`, and `author` fields to SKILL.md frontmatter. Provenance is now fully declared in the registry.
- **`optimize.sh` missing from integrity manifest** — Added `scripts/optimize.sh` to `.clawhubsafe`. The manifest now covers 13 files (previously 12). Every bundled file is SHA256-verified.
- **`optimize.sh` undocumented** — New dedicated section in `SECURITY.md` with full source disclosure: what the wrapper does (delegates to bundled Python scripts only), security properties, and a one-line audit command for users who want to verify before running.
- **Provenance undocumented** — New `Provenance & Source` section in `SECURITY.md` with explicit GitHub repo + ClawHub listing links and integrity verification instructions.

## [1.4.1] - 2026-02-18

### Fixed
- **ClawHub public visibility blocked** — `PR-DESCRIPTION.md` (a leftover dev file containing `git push` / `gh pr create` shell commands) was included in the v1.4.0 bundle, triggering ClawHub's security scanner hold.
- **Added `.clawhubignore`** — Now excludes `PR-DESCRIPTION.md`, `docs/`, `.git/`, `.gitignore` from all future publishes. Only skill-relevant files are bundled.

## [1.4.0] - 2026-02-17

### Added
- **Session pruning config patch** — Native `contextPruning: { mode: "cache-ttl" }` support. Auto-trims old tool results when the Anthropic prompt cache TTL expires, reducing cache write costs after idle sessions. No scripts required — applies directly via `gateway config.patch`.
- **Bootstrap size limits patch** — `bootstrapMaxChars` / `bootstrapTotalMaxChars` config keys to cap how large workspace files are injected into the system prompt. Delivers 20-40% system prompt reduction for agents with large workspace files (e.g., detailed AGENTS.md, MEMORY.md). Native 2026.2.15 feature.
- **Cache retention config patch** — `cacheRetention: "long"` param for Opus models. Amortizes cache write costs across long reasoning sessions.
- **Cache TTL heartbeat alignment** — New `heartbeat_optimizer.py cache-ttl` command. Calculates the optimal heartbeat interval to keep the Anthropic 1h prompt cache warm (55min). Prevents the "cold restart" cache re-write penalty after idle gaps.
- **Native commands section in SKILL.md** — Documents `/context list`, `/context detail` (per-file token breakdown) and `/usage tokens|full|cost` (per-response usage footer). These are built-in OpenClaw 2026.2.15 diagnostics that complement the Python scripts.
- **`native_openclaw` category in config-patches.json** — Clearly distinguishes patches that work today with zero external dependencies from those requiring API keys or beta features.

### Changed
- `SKILL.md`: Configuration Patches section updated — `session_pruning`, `bootstrap_size_limits`, and `cache_retention_long` now listed as ✅ native (not ⏳ pending).
- `config-patches.json`: Added `_categories.native_openclaw` grouping. Model routing patch updated to reflect Sonnet-primary setups (Haiku listed as optional with multi-provider note).
- `heartbeat_optimizer.py`: Added `cache-ttl` subcommand and `CACHE_TTL_OPTIMAL_INTERVAL` constant (3300s = 55min). Plan output now includes cache TTL alignment recommendation when relevant.
- Compliance with OpenClaw 2026.2.15 features: **72% → 92%+**

### Fixed
- Model routing quick start: added note that Haiku requires multi-provider setup (OpenRouter/Together); Sonnet is the default minimum for single-provider Anthropic deployments.

## [1.3.3] - 2026-02-17

### Fixed
- Display name corrected to "OOT" on ClawHub (was truncated in 1.3.1/1.3.2)
- Slug preserved: `oot`

## [1.3.2] - 2026-02-17

### Added
- `SECURITY.md` — Full two-category security breakdown (executable scripts vs. reference docs)
- `.clawhubsafe` — SHA256 integrity manifest for all 10 skill files

### Fixed
- Resolved VT flag: SKILL.md previously claimed `no_network: true` for entire skill, but PROVIDERS.md and config-patches.json reference external APIs — scoped the guarantee to scripts only

## [1.3.1] - 2026-02-12

### Added
- `context_optimizer.py` — Context lazy-loading and complexity-based file recommendations
- `cronjob-model-guide.md` — Model selection guide for cron-based tasks

### Changed
- Enhanced model_router.py with communication pattern enforcement

## [1.2.0] - 2026-02-07

### Added
- Initial public release
- `heartbeat_optimizer.py`, `model_router.py`, `token_tracker.py`
- `PROVIDERS.md`, `config-patches.json`, `HEARTBEAT.template.md`
