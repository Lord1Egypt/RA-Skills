# Changelog

All notable changes to the Pipedream Connect skill are documented here.

## [1.6.0] - 2026-03-21

### Added
- Documented the current OpenClaw Pipedream architecture around first-class MCP tool exposure, per-agent isolation, live connected-account discovery, dynamic full-catalog browsing, and authenticated icon passthrough
- Synced bundled reference snapshots from the live OpenClaw source so the skill's code references match the current implementation

### Changed
- Updated skill guidance to treat connected Pipedream MCP tools as ordinary agent tools, not just raw mcporter endpoints
- Updated install guidance to reflect current config paths, vault usage, dynamic catalog behavior, and icon handling
- Updated reference documentation to emphasize live catalog loading, `img_src` / `iconUrl`, and the dynamic Browse All Apps flow

## [1.5.0] - 2026-03-17

### Added
- Connected per-agent Pipedream MCP app tools are now injected into the OpenClaw agent runtime as first-class tools
- `tools.catalog` now includes live connected Pipedream tools under a `Pipedream MCP` group so the agent Tools UI reflects callable runtime tools

### Changed
- Agent tool execution now routes connected Pipedream tools through the matching `pipedream-{agentId}-*` mcporter server automatically
- Skill docs updated to describe direct in-chat tool availability, not just raw `mcporter call` usage

## [1.4.0] - 2026-03-01

### Removed
- **1Password integration fully removed** — `--1password` CLI flag, `PIPEDREAM_1PASSWORD_ITEM` env var, `get_credentials_from_1password()` function, and all 1Password references deleted from scripts, docs, and metadata
- `shutil` and `subprocess` imports removed from token refresh script (no longer needed)

### Fixed
- Script paths corrected to `~/.openclaw/workspace/config/` throughout (was `~/clawd/config/` in some places)
- Metadata `configPaths` now explicitly declares all files read/written by the skill
- `installWarnings` updated to remove 1Password references

## [1.3.0] - 2026-03-01

### Security (Breaking — vault migration)
- **clientId and clientSecret moved to `~/.openclaw/secrets.json`** (OpenClaw vault) — no longer stored in `pipedream-credentials.json`
- **`PIPEDREAM_CLIENT_SECRET` removed from all `mcporter.json` env entries** — client secret is never written to mcporter config
- **Auto-migration on first start**: existing plaintext `pipedream-credentials.json` secrets silently moved to vault, file rewritten with non-secrets only
- Token refresh script (`pipedream-token-refresh.py`) now reads vault first; falls back to credentials.json → mcporter.json
- `pipedream-credentials.json` now contains only: `projectId`, `environment`, `externalUserId`
- Resolves VirusTotal "Suspicious" flag — no plaintext credential files

### Changed
- `buildMcporterEntry()` helper centralizes mcporter server entry construction, never includes clientSecret
- `readPipedreamCredentials()` now resolves secrets from vault at runtime, not from file

## [1.2.0] - 2026-03-01

### Added
- **Per-agent app connections** — App connections moved to Agents → [Agent] → Tools → Pipedream tab
- **Agent Pipedream panel** — New UI panel with live connected apps, available apps grid, and OAuth connect flow
- **Multi-agent isolation** — Each agent gets its own `external_user_id` (defaults to agent slug) and isolated OAuth tokens
- **New reference files**: `agent-pipedream-views.ts`, `agent-pipedream-controller.ts`
- **New RPCs**: `pipedream.getToken`, `pipedream.getConnectUrl`, `pipedream.connectApp`, `pipedream.disconnectApp`, `pipedream.refreshToken`, `pipedream.activate`
- **Environment warning** — Agent panel warns when running in development mode (use production for real work)
- **Browse All Apps modal** — Full app browser within the agent panel
- Complete RPC reference table in SKILL.md

### Changed
- Global Pipedream tab is now credentials-only (Client ID / Secret / Project ID / Environment)
- Agent quick-links table on global tab navigates to per-agent config
- Backend doubled in size (493 → 1,006 lines) with full multi-agent implementation
- `pipedream-backend.ts` refactored for per-agent config at `~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json`

## [1.1.0] - 2025-02-11

### Added
- **Security transparency** for ClawHub compliance:
  - Added `capabilities` section documenting all system-modifying behaviors
  - Added `securityNotes` with credential storage warnings
  - Added `installWarnings` array with pre-install considerations
- Security section in SKILL.md with behavior table
- Security notice in INSTALL.md

### Fixed
- Corrected false "Encrypted credential storage" claim — credentials are stored as plaintext JSON with 0600 permissions, NOT encrypted

### Changed
- Bumped version to 1.1.0
- Updated Files Created table to accurately describe storage format
- Enhanced `pipedream-token-refresh.py` credential resolution

## [1.0.0] - 2025-02-10

### Added
- Initial release
- Pipedream OAuth integration with UI dashboard
- Token refresh script with cron setup
- MCP integration via mcporter
- Support for 2,000+ apps via Pipedream Connect
- Reference implementations for backend, controller, and views
