# Changelog

## v4.1.1

- Lead with natural-language requests and plain-language benefits instead of Python commands.
- Give agents a context-first OpenClaw/Hermes workflow with focused ambiguity handling.
- Move technical steps into a lazy-loaded quick-start reference; keep all audits read-only.
- Clarify missing profile/job evidence, installation needs and report expectations.

## v4.1.0

- Add explicit Hermes read-only adapter and isolated upstream cron-store compatibility test.
- Resolve file-evidenced cron model precedence including creation snapshots.
- Recognize no_agent/paused jobs; keep auth, runtime overlays and savings unverified.
- Share the analysis engine and preserve OpenClaw behavior and existing installation slug.
- Document runtime-specific requirements and compatibility boundaries.


## v4.0.2 — 2026-09-19

- Fix false unknown-kind findings for native heartbeat and systemEvent jobs.
- Keep agent-turn-only checks scoped to agent turns; preserve unknown-kind reporting.
- Add three regression tests for native kinds, future kinds and agent-turn linting.
- Rewrite README and ClawHub description for clear OpenClaw token optimization,
  AI cost auditing, model routing and automation discovery, without savings guarantees.

## v4.0.1 — 2026-09-19

- Ship LICENSE.txt and SHA256SUMS.txt through extension-filtering registry clients.
- Pin the installation example; verify actual published file hashes.
- No change to the read-only audit behavior.

## v4.0.0 — 2026-09-19

- Combined compatibility refresh and native-aware audit core.
- Added read-only audit/plan, ordered policy routing, context sizing/duplicates,
  automation linting, coverage flags and honest missing-usage handling.
- Added optional fixed-command OpenClaw adapter and offline JSON mode.
- Removed obsolete static model/pricing tables, blanket 55-minute cache guidance,
  generated workspace instructions, and unmeasured percentage-saving claims.
- Preserved MIT license; unified slug/version; added regression tests and CI.
- Breaking: legacy entrypoints now delegate to explicit v4 CLI arguments.
- Native usage ingestion, automatic budgets, auto-apply and benchmarking remain outside v4.0.


All notable changes to OpenClaw Token Optimizer are documented here.

## [3.2.0] - 2026-06-22

### Changed
- Modernized the ClawHub skill card to match newer Asif2BD releases: stronger title, badges, GitHub/security links, current compatibility, quick commands, savings table, file inventory, and security posture.
- Moved the public listing away from old v3.0-era Haiku/no-system-modification copy and toward OpenClaw 2026.6.x Sonnet/Opus guidance.
- Updated README version badge and license badge to match the repository license.

## [3.1.0] - 2026-06-22

### Fixed
- Addressed the ClawHub security audit's description/behavior mismatch by documenting explicit local workspace writes instead of claiming the skill makes no system modifications.
- Changed `context_optimizer.py generate-agents` to print to stdout by default; writing `AGENTS.md.optimized` now requires `--output` or `--workspace-output`.
- Changed `scripts/optimize.sh heartbeat` to preview by default; installing `HEARTBEAT.md` now requires `heartbeat install` and backs up an existing file first.
- Updated model routing defaults for current OpenClaw 2026.6.x Sonnet/Opus deployments: routine work maps to Sonnet and complex reasoning maps to Opus.
- Refreshed README, SECURITY.md, heartbeat, cronjob, and config-patch guidance for a safer release.

## [1.4.3] - 2026-02-18

### Fixed
- README completely rewritten: correct name ("OpenClaw Token Optimizer"), version badge (1.4.3), install command (clawhub install Asif2BD/openclaw-token-optimizer), license (Apache 2.0), all skill paths corrected to openclaw-token-optimizer, v1.4.x features documented.

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
- Display name corrected to "OpenClaw Token Optimizer" on ClawHub (was truncated in 1.3.1/1.3.2)
- Slug preserved: `openclaw-token-optimizer`

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
